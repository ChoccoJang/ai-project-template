#!/usr/bin/env python3
"""`.ai/` 문서가 폴더 규약을 지키는지 검사한다.

파일을 만들고 인덱스에 등록하지 않은 경우, 파일명 규칙 위반, 머리말 필드 누락,
상태 어휘 위반, 인덱스 표와 파일 머리말의 상태 불일치를 잡는다.
(링크가 실제 파일을 가리키는지는 `check_markdown_links.py`가 본다.)

사용법:
    python3 .github/scripts/check_doc_index.py [기준경로]

위반이 하나라도 있으면 종료 코드 1로 끝난다.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# 각 폴더의 규약. 템플릿(`0000-template.md`)과 인덱스(`README.md`)는 검사 대상이 아니다.
# 상태 값은 영어로 고정한다(.ai/README.md). 부연은 값 뒤에 괄호로만 붙인다.
ADR_STATUS = re.compile(r"^(Accepted|Proposed|Deprecated|Superseded by \d{4})$")
ISSUE_STATUS = re.compile(r"^(Open|Deferred|Resolved)(\s*\(.+\))?$")
# Phase 표기(AGENTS.md 9절): 대문자 한 글자 또는 `A-1`. 없으면 "해당 없음".
PHASE_VALUE = re.compile(r"^([A-Z](-\d+)?|해당 없음)$")


@dataclass
class Section:
    directory: str
    filename: re.Pattern
    filename_hint: str
    unique_prefix: bool  # 파일명 앞 번호가 고유해야 하는가
    status: re.Pattern | None  # None이면 상태 필드를 쓰지 않는 폴더
    needs_phase: bool = True
    extra_fields: list[str] = field(default_factory=list)


SECTIONS = [
    Section(".ai/adr", re.compile(r"^\d{4}-[a-z0-9-]+\.md$"), "NNNN-slug.md", True, ADR_STATUS),
    Section(".ai/issues", re.compile(r"^\d{4}-[a-z0-9-]+\.md$"), "NNNN-slug.md", True, ISSUE_STATUS),
    Section(
        ".ai/work-result",
        re.compile(r"^\d{8}-[a-z0-9-]+\.md$"),
        "yyyymmdd-slug.md",
        False,  # 같은 날 여러 작업이 있을 수 있다
        None,
        extra_fields=["PR"],
    ),
    # 설계 문서는 컴포넌트 이름으로 부르므로 번호가 없다. Phase도 두지 않는다 —
    # 한 컴포넌트의 설계는 여러 Phase에 걸쳐 이어지기 때문이다.
    Section(
        ".ai/design",
        re.compile(r"^[a-z0-9-]+\.md$"),
        "{component}.md",
        False,
        None,
        needs_phase=False,
        extra_fields=["갱신일"],
    ),
]

SKIP_NAMES = {"README.md"}
TEMPLATE_PREFIX = "0000-"


def read_field(text: str, name: str) -> str | None:
    """머리말의 `- 이름: 값` 또는 `- **이름** : 값`에서 값을 읽는다. 없으면 None."""
    pattern = re.compile(rf"^-\s+(?:\*\*)?{re.escape(name)}(?:\*\*)?\s*:\s*(.*)$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return None
    value = match.group(1)
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)  # 안내 주석 제거
    return value.strip()


def normalize_status(value: str) -> str:
    """상태 비교 기준. 첫 쉼표·괄호 앞까지만 본다.

    `Resolved (2026-08-19, PR #12)`와 `Resolved`를 같게 본다.
    """
    return re.split(r"[(,]", value, maxsplit=1)[0].strip()


def index_rows(index_text: str) -> dict[str, list[str]]:
    """인덱스 표에서 `파일명 -> 그 행의 셀 목록`을 만든다.

    코드 블록 안의 "기입 예시"는 세지 않는다 — 예시를 실제 등록으로 오인하면 등록되지 않은
    파일이 통과한다.
    """
    rows: dict[str, list[str]] = {}
    in_fence = False
    for line in index_text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        for target in re.findall(r"\]\(\./([^)]+)\)", line):
            rows.setdefault(target, cells)
    return rows


def check_section(section: Section, root: Path) -> list[str]:
    problems: list[str] = []
    directory = root / section.directory
    if not directory.is_dir():
        return [f"{section.directory}: 폴더가 없다"]

    index_path = directory / "README.md"
    if not index_path.is_file():
        return [f"{section.directory}/README.md: 인덱스 파일이 없다"]
    rows = index_rows(index_path.read_text(encoding="utf-8"))

    seen_prefix: dict[str, str] = {}
    for path in sorted(directory.glob("*.md")):
        name = path.name
        if name in SKIP_NAMES or name.startswith(TEMPLATE_PREFIX):
            continue
        rel = f"{section.directory}/{name}"

        if not section.filename.match(name):
            problems.append(
                f"{rel}: 파일명이 규칙에 어긋난다 — `{section.filename_hint}`"
                " (영문 소문자·숫자·하이픈만, AGENTS.md 10절)"
            )
            continue

        prefix = name.split("-", 1)[0]
        if section.unique_prefix:
            if prefix in seen_prefix:
                problems.append(f"{rel}: 번호 {prefix}이(가) {seen_prefix[prefix]}와 중복된다")
            seen_prefix[prefix] = name

        text = path.read_text(encoding="utf-8")

        if section.needs_phase:
            phase = read_field(text, "Phase")
            if phase is None:
                problems.append(f"{rel}: 머리말에 `Phase` 필드가 없다 (AGENTS.md 10절)")
            elif not PHASE_VALUE.match(phase):
                problems.append(
                    f"{rel}: `Phase: {phase}`는 표기 규칙에 어긋난다 —"
                    " `A` 또는 `A-1`, 없으면 `해당 없음` (AGENTS.md 9절)"
                )

        for name_ in section.extra_fields:
            if read_field(text, name_) is None:
                problems.append(f"{rel}: 머리말에 `{name_}` 필드가 없다")

        cells = rows.get(name)
        if cells is None:
            problems.append(
                f"{rel}: {section.directory}/README.md 인덱스 표에 등록되지 않았다"
            )

        if section.status is None:
            continue

        status = read_field(text, "상태")
        if status is None:
            problems.append(f"{rel}: 머리말에 `상태` 필드가 없다")
            continue
        if not section.status.match(status):
            problems.append(f"{rel}: `상태: {status}`는 허용된 어휘가 아니다 (.ai/README.md)")
        if cells is not None:
            wanted = normalize_status(status)
            if not any(normalize_status(cell) == wanted for cell in cells):
                problems.append(
                    f"{rel}: 인덱스 표의 상태가 파일 머리말(`{status}`)과 다르다"
                )

    return problems


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems: list[str] = []
    for section in SECTIONS:
        problems.extend(check_section(section, root))

    if problems:
        print("문서 규약 위반:")
        for problem in problems:
            print(f"  - {problem}")
        print(f"\n총 {len(problems)}건. 규약은 .ai/README.md 참고.")
        return 1

    print("문서 인덱스·머리말 규약 이상 없음.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
