#!/usr/bin/env python3
"""CI 이벤트에 맞춰 문서 검사를 실행한다. 일반 PR은 첫 실행부터 결과 문서가 필수다."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# 저장소 정체성으로 한정한다. 복제한 프로젝트에는 템플릿의 기록 예외가 적용되지 않는다.
TEMPLATE_REPOSITORY = "ChoccoJang/ai-project-template"


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    command = [sys.executable, str(root / ".github/scripts/check_doc_index.py"), str(root)]
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        try:
            # checkout의 PR test-merge 커밋 첫 부모가 실제 base다.
            base = subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD^1"], cwd=root,
                check=True, capture_output=True, text=True,
            ).stdout.strip()
            added = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=A", base, "HEAD", "--", ".ai/work-result"],
                cwd=root, check=True, capture_output=True, text=True,
            ).stdout
        except subprocess.CalledProcessError as error:
            print(f"::error::PR 비교 기준을 확인하지 못했다 (git 종료 코드 {error.returncode}).")
            return 1
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if repository.casefold() == TEMPLATE_REPOSITORY.casefold():
            mode = "off"
        elif os.environ.get("PR_DRAFT") == "true":
            mode = "warn"
        else:
            mode = "fail"
        command += ["--added", added, "--base", base, "--require-work-result", mode]
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
