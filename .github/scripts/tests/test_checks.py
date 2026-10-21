"""지침 바이트 한도와 PR 이벤트별 문서 게이트의 회귀 테스트."""

import importlib.util
from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / ".github/scripts"


class ByteBudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".github").mkdir()

    def check(self, contents, cap, *flags):
        files = []
        for name, data in contents.items():
            (self.root / name).write_bytes(data)
            files.append(name)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        config = {
            "default": 700,
            "byte_budgets": [{"name": "test", "files": files, "max": cap}],
        }
        (self.root / ".github/file-size.json").write_text(json.dumps(config))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "check_file_size.py"), str(self.root), *flags],
            capture_output=True, text=True,
        )

    def test_korean_utf8_exact_limit(self):
        result = self.check({"AGENTS.md": "한글\n".encode()}, 7)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_korean_utf8_over_limit(self):
        result = self.check({"AGENTS.md": "한글\n".encode()}, 6)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("7바이트", result.stdout)

    def test_combined_budget_includes_separator(self):
        result = self.check({"AGENTS.md": b"abc", "AGENTS.override.md": b"def"}, 7)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("8바이트", result.stdout)

    def test_update_cannot_bypass_byte_limit(self):
        result = self.check({"AGENTS.md": b"abc"}, 2, "--update-baseline", "--accept-new")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertNotIn("baseline", json.loads((self.root / ".github/file-size.json").read_text()))

    def test_invalid_utf8_fails(self):
        result = self.check({"AGENTS.md": b"\xff\n"}, 100)
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_missing_budget_file_fails(self):
        self.check({"AGENTS.md": b"abc"}, 100)
        (self.root / "AGENTS.md").unlink()
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_file_size.py"), str(self.root)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout)


class CiDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(SCRIPTS, self.root / ".github/scripts",
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / ".ai/work-result").mkdir(parents=True)
        (self.root / ".ai/work-result/README.md").write_text("# 결과\n\n아직 등록된 결과가 없다.\n")
        shutil.copyfile(ROOT / "AGENTS.md", self.root / "AGENTS.md")
        self.git("init", "-q", "-b", "main")
        self.git("add", ".")
        self.git("commit", "-qm", "base")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "user.name=Tests", "-c", "user.email=tests@example.invalid", *args],
            cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout.strip()

    def merge_feature(self, result_document=False, invalid_pr=False):
        self.git("checkout", "-qb", "feature")
        if result_document:
            directory = self.root / ".ai/work-result"
            name = "20261021-regression.md"
            pr = "없음(직접 push)" if invalid_pr else "[#1](https://github.com/example/project/pull/1)"
            (directory / name).write_text(f"# 검사\n\n- **PR** : {pr}\n- **Phase** : 해당 없음\n")
            (directory / "README.md").write_text(f"# 결과\n\n| 제목 |\n|---|\n| [검사](./{name}) |\n")
        (self.root / "change.txt").write_text("change\n")
        self.git("add", ".")
        self.git("commit", "-qm", "feature")
        self.git("checkout", "-q", "main")
        self.git("merge", "--no-ff", "-qm", "test merge", "feature")

    def check(self, event="pull_request", action="opened", draft="false", repository="example/project"):
        env = {**os.environ, "GITHUB_EVENT_NAME": event, "PR_ACTION": action,
               "PR_DRAFT": draft, "GITHUB_REPOSITORY": repository, "GITHUB_ACTIONS": "true"}
        return subprocess.run(
            [sys.executable, str(self.root / ".github/scripts/check_ci_docs.py")],
            cwd=self.root, env=env, capture_output=True, text=True,
        )

    def test_all_ready_pr_events_require_result(self):
        self.merge_feature()
        for action in ("opened", "synchronize", "reopened", "ready_for_review"):
            with self.subTest(action=action):
                result = self.check(action=action)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("결과 문서를 새로 추가하지 않았다", result.stdout)

    def test_draft_warns(self):
        self.merge_feature()
        result = self.check(draft="true")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("::warning::", result.stdout)

    def test_only_original_template_is_exempt(self):
        self.merge_feature()
        for repository, expected in (("ChoccoJang/ai-project-template", 0),
                                     ("other/ai-project-template", 1),
                                     ("ChoccoJang/project", 1), ("", 1)):
            with self.subTest(repository=repository):
                result = self.check(repository=repository)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_missing_base_fails_even_for_template(self):
        for repository in ("example/project", "ChoccoJang/ai-project-template"):
            with self.subTest(repository=repository):
                result = self.check(repository=repository)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("PR 비교 기준", result.stdout)

    def test_non_pr_does_not_require_result(self):
        for event in ("push", "workflow_dispatch"):
            with self.subTest(event=event):
                result = self.check(event=event)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_result_document_allows_opened(self):
        self.merge_feature(result_document=True)
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_template_still_checks_existing_document_fields(self):
        self.merge_feature(result_document=True, invalid_pr=True)
        result = self.check(repository="ChoccoJang/ai-project-template")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_diff_failure_does_not_disable_gate(self):
        spec = importlib.util.spec_from_file_location("ci_docs", SCRIPTS / "check_ci_docs.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        calls = [subprocess.CompletedProcess([], 0, stdout="base\n"),
                 subprocess.CalledProcessError(128, ["git", "diff"])]
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "pull_request"}):
            with patch.object(module.subprocess, "run", side_effect=calls):
                with redirect_stdout(StringIO()) as output:
                    self.assertEqual(module.main(), 1)
                self.assertIn("PR 비교 기준", output.getvalue())


if __name__ == "__main__":
    unittest.main()
