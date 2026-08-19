#!/usr/bin/env python3
"""저장소 안 마크다운 문서의 상대 링크가 실제 파일을 가리키는지 검사한다.

인덱스 표(`.ai/adr/README.md` 등)가 존재하지 않는 파일을 가리키는 실수를 막는 용도다.
외부 링크(http/https/mailto)와 자리표시자(`{{...}}`)가 든 링크는 건너뛴다.

사용법:
    python3 .github/scripts/check_markdown_links.py [기준경로]

깨진 링크가 하나라도 있으면 종료 코드 1로 끝난다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

# [텍스트](대상) 형태의 인라인 링크. 이미지(![...])도 같은 형태라 함께 잡힌다.
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:")
SKIP_DIRS = {".git", "node_modules", "build", "dist", "out", "target", "__pycache__"}


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def check_file(md_path: Path, root: Path) -> list[str]:
    """md_path 안의 깨진 링크 목록을 사람이 읽을 수 있는 문자열로 돌려준다."""
    problems: list[str] = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    in_fence = False

    for lineno, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            # 코드 블록 안의 예시 링크는 검사하지 않는다.
            continue

        for target in LINK_RE.findall(line):
            if target.startswith(SKIP_PREFIXES):
                continue
            if "{{" in target:
                # 치환 전 자리표시자 경로.
                continue

            # 앵커(#...)와 쿼리는 떼어 낸다.
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue

            base = root if path_part.startswith("/") else md_path.parent
            resolved = (base / unquote(path_part).lstrip("/")).resolve()

            if not resolved.exists():
                rel = md_path.relative_to(root)
                problems.append(f"{rel}:{lineno}: 깨진 링크 -> {target}")

    return problems


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems: list[str] = []
    checked = 0

    for md_path in iter_markdown_files(root):
        checked += 1
        problems.extend(check_file(md_path, root))

    if problems:
        print(f"문서 {checked}개 검사 — 깨진 링크 {len(problems)}건:\n")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"문서 {checked}개 검사 — 깨진 상대 링크 없음.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
