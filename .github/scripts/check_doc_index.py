#!/usr/bin/env python3
"""`.ai/` 문서가 폴더 규약을 지키는지 검사한다.

파일을 만들고 인덱스에 등록하지 않은 경우, 파일명 규칙 위반, 머리말 필드 누락,
상태 어휘 위반, 인덱스 표와 파일 머리말의 상태 불일치, 존재하지 않는 절을 가리키는
"N절" 참조를 잡는다.
(링크가 실제 파일을 가리키는지는 `check_markdown_links.py`가 본다.)

사용법:
    python3 .github/scripts/check_doc_index.py [기준경로] [--merge-gate]

`--merge-gate`는 작업 결과 문서의 `PR: 미정`을 실패로 본다. CI는 항상 켜고, 작업 중 로컬
실행에서는 끈다 — 아직 PR이 없어 `미정`이 정상인 구간이 있기 때문이다
(`.ai/work-result/README.md`의 `PR` 필드 채우는 순서).

위반이 하나라도 있으면 종료 코드 1로 끝난다.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# 각 폴더의 규약. 템플릿(`0000-template.md`)과 인덱스(`README.md`)는 검사 대상이 아니다.
# 상태 값은 영어로 고정한다(.ai/README.md). 부연은 값 뒤에 괄호로만 붙인다.
ADR_STATUS = re.compile(r"^(Accepted|Proposed|Deprecated|Superseded by \d{4})(\s*\(.+\))?$")
ISSUE_STATUS = re.compile(r"^(Open|Deferred|Resolved)(\s*\(.+\))?$")
# Phase 표기(.ai/README.md): 대문자 한 글자 또는 `A-1`. 없으면 "해당 없음".
PHASE_VALUE = re.compile(r"^([A-Z](-\d+)?|해당 없음)$")
# 작업 결과 문서의 `PR` 필드는 셋 중 하나다(.ai/work-result/README.md).
# 번호만 적은 `#12`는 어느 저장소인지 알 수 없어 링크를 요구한다. 호스트는 보지 않는다.
# 값 **전체**가 링크여야 하고 끝이 `/숫자`여야 한다 — 채우지 않은 자리표시자(`/pull/NN`)와
# `미정 https://...`처럼 문구가 섞인 값이 게이트를 통과하는 것을 막는다. 부연은 괄호로.
PR_LINK = re.compile(r"^(\[[^\]]*\]\()?https?://[^\s)]+/\d+\)?(\s*\(.+\))?$")
PR_NONE = re.compile(r"^없음\s*\(.+\)$")   # 사유를 괄호로 붙인 것만 통과 (AGENTS.md 8절)
PR_PENDING = re.compile(r"^미정$")


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
    # 콜론 뒤는 `[ \t]*`로 묶는다 — `\s*`면 값이 빈 필드가 다음 줄을 통째로 삼킨다.
    pattern = re.compile(
        rf"^-[ \t]+(?:\*\*)?{re.escape(name)}(?:\*\*)?[ \t]*:[ \t]*(.*)$", re.MULTILINE
    )
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


def check_pr_field(rel: str, value: str, merge_gate: bool) -> list[str]:
    """작업 결과 문서의 `PR` 값이 링크 · `없음(사유)` · `미정` 중 하나인지 본다.

    `미정`은 PR을 열기 전 한 커밋 동안만 정상이다. `merge_gate`가 켜지면 실패로 본다 —
    CI는 늘 켜므로 PR을 연 직후 한 번 빨개지고, 링크를 채워 push하면 초록이 된다.
    """
    if PR_LINK.search(value) or PR_NONE.match(value):
        return []
    if PR_PENDING.match(value):
        if not merge_gate:
            return []
        return [
            f"{rel}: `PR: 미정`이 남아 있다 — PR을 연 뒤 받은 링크를 적어 같은 브랜치에"
            " 한 번 더 커밋한다 (.ai/work-result/README.md)"
        ]
    return [
        f"{rel}: `PR` 값이 규칙에 어긋난다 (`{value}`) —"
        " PR 링크(`[#12](https://.../pull/12)`) · `없음(사유)` · `미정` 중 하나"
        " (.ai/work-result/README.md)"
    ]


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
        for target in re.findall(r"\]\((?:\./)?([^)/][^)]*)\)", line):
            rows.setdefault(target, cells)
    return rows


def check_section(section: Section, root: Path, merge_gate: bool = False) -> list[str]:
    problems: list[str] = []
    directory = root / section.directory
    if not directory.is_dir():
        return []          # 폴더는 남길 것이 생겼을 때 만든다(.ai/README.md)

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
                " (영문 소문자·숫자·하이픈만, AGENTS.md 7절)"
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
            if not phase:
                problems.append(f"{rel}: 머리말에 `Phase` 필드가 없다 (.ai/README.md)")
            elif not PHASE_VALUE.match(phase):
                problems.append(
                    f"{rel}: `Phase: {phase}`는 표기 규칙에 어긋난다 —"
                    " `A` 또는 `A-1`, 없으면 `해당 없음` (.ai/README.md)"
                )

        for name_ in section.extra_fields:
            value = read_field(text, name_)
            if not value:
                problems.append(f"{rel}: 머리말 `{name_}` 필드가 없거나 비어 있다")
            elif name_ == "PR":
                problems.extend(check_pr_field(rel, value, merge_gate))

        cells = rows.get(name)
        if cells is None:
            problems.append(
                f"{rel}: {section.directory}/README.md 인덱스 표에 등록되지 않았다"
            )

        if section.status is None:
            continue

        status = read_field(text, "상태")
        if not status:
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


SECTION_HEADING = re.compile(r"^## (\d+)\. ", re.MULTILINE)
# "AGENTS.md 4절", "AGENTS 8·9절", "`AGENTS.md` 6절" 등. 앞의 문서 이름이 있어야 잡는다.
# 다른 문서에서는 `AGENTS`가 앞에 붙은 참조만 본다 — `4.10절`, 노래 `3절` 같은 평범한
# 본문을 잡지 않기 위해서다. 이름 없는 `9절`은 AGENTS.md 자기 자신에서만 자기 절로 읽는다.
SECTION_REF = re.compile(r"AGENTS(?:\.md)?`?(?:의)?\s*((?:\d+[·,]\s*)*\d+)\s*절")
SECTION_REF_SELF = re.compile(r"(?:^|[^0-9A-Za-z.])((?:\d+[·,]\s*)*\d+)\s*절")


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        print("git ls-files 실패 — git 저장소에서 실행한다.", file=sys.stderr)
        raise SystemExit(2)
    # `-z`로 받는다 — 기본 출력은 비ASCII·공백 경로를 C 이스케이프로 인용해
    # 그대로 열면 파일을 못 찾고 조용히 검사에서 빠진다.
    return [name for name in result.stdout.split("\0") if name]


def check_section_refs(root: Path) -> list[str]:
    """저장소 전체에서 `AGENTS.md N절` 참조가 실제 절을 가리키는지 확인한다."""
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return []
    valid = set(SECTION_HEADING.findall(agents.read_text(encoding="utf-8")))
    problems: list[str] = []
    for rel in tracked_files(root):
        path = root / rel
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json"} and path.name != ".gitignore":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # AGENTS.md 자신은 자기 절을 이름 없이 가리킨다. 다른 문서는 이름이 붙은 참조만 본다.
        pattern = SECTION_REF_SELF if rel == "AGENTS.md" else SECTION_REF
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for group in pattern.findall(line):
                for num in re.split(r"[·,]\s*", group):
                    if num not in valid:
                        problems.append(
                            f"{rel}:{lineno}: `AGENTS.md {num}절`은 없는 절이다"
                            f" (있는 절: {', '.join(sorted(valid, key=int))})"
                        )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="`.ai/` 문서의 폴더 규약을 검사한다.")
    parser.add_argument("root", nargs="?", default=".", help="검사할 기준 경로 (기본: 현재 디렉터리)")
    parser.add_argument(
        "--merge-gate",
        action="store_true",
        help="작업 결과 문서의 `PR: 미정`을 실패로 본다 (PR을 연 다음 실행부터 켠다)",
    )
    options = parser.parse_args()
    root = Path(options.root).resolve()
    if options.merge_gate:
        print("`PR: 미정` 게이트: 켜짐")
    problems: list[str] = []
    for section in SECTIONS:
        problems.extend(check_section(section, root, options.merge_gate))
    problems.extend(check_section_refs(root))

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
