#!/usr/bin/env python3
"""작업 결과 문서의 `PR` 필드 규칙. `check_doc_index.py`가 쓰는 모듈이다.

값은 둘 중 하나다 — PR 링크 · `없음(사유)`. 그 판정과, 뒤늦은 기록의 탈출구
(`없음(직접 push, abc1234)`)가 가리키는 커밋이 이 PR 전에 이미 들어와 있던 것인지 보는
git 확인이 여기 있다. 규칙의 뜻은 `.ai/work-result/README.md`가 정한다.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# 작업 결과 문서의 `PR` 필드는 둘 중 하나다(.ai/work-result/README.md). 이 문서는 PR을 연
# 뒤에 만들므로 링크를 모르는 구간이 없다 — `미정` 같은 임시값을 받지 않는다.
# 번호만 적은 `#12`는 어느 저장소인지 알 수 없어 링크를 요구한다. 호스트는 보지 않는다.
# 값 **전체**가 링크여야 하고 끝이 `/숫자`여야 한다 — 채우지 않은 자리표시자(`/pull/NN`)와
# 문구가 섞인 값이 게이트를 통과하는 것을 막는다. 부연은 괄호로.
PR_LINK = re.compile(r"^(\[[^\]]*\]\()?https?://[^\s)]+/\d+\)?(\s*\(.+\))?$")
PR_NONE = re.compile(r"^없음\s*\(.+\)$")   # 사유를 괄호로 붙인 것만 통과 (AGENTS.md 8절)
# 이미 직접 push된 지난 작업을 뒤늦게 기록하는 PR의 탈출구 — 사유가 그때의 커밋을 가리키면
# "PR로 올라오는 중인데 PR 없음"이 아니라 "그때 PR이 없었다"는 사실 기록이다.
PR_NONE_COMMIT = re.compile(r"\b[0-9a-f]{7,40}\b")


@dataclass
class Run:
    """한 번의 검사 실행에서 공유하는 것."""

    root: Path
    added: frozenset[str] = frozenset()
    # PR의 base 커밋. 뒤늦은 기록이 가리키는 커밋이 **이 PR 전에 이미 있던 것**인지 본다.
    base: str | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def history_available(self) -> bool:
        """커밋 실재를 확인할 만한 히스토리가 있는가. 얕은 클론·비 git이면 False."""
        result = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--is-shallow-repository"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0 and result.stdout.strip() == "false"


def git_ok(root: Path, *args: str) -> bool:
    """git 명령이 0으로 끝나는가."""
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False
    )
    return result.returncode == 0


def commit_landed(run: Run, sha: str) -> bool:
    """`sha`가 **이 PR 전에 이미 저장소에 들어와 있던** 커밋인가.

    base를 아는 실행(CI의 PR 실행)에서는 base의 조상인지까지 본다 — 그러지 않으면 자기
    브랜치의 커밋을 적어 탈출구를 빠져나갈 수 있다. base를 모르는 로컬 실행에서는
    실재만 본다.
    """
    if not git_ok(run.root, "cat-file", "-e", f"{sha}^{{commit}}"):
        return False
    if run.base is None:
        return True
    return git_ok(run.root, "merge-base", "--is-ancestor", sha, run.base)


def check_pr_field(rel: str, value: str, run: Run, added_in_pr: bool) -> list[str]:
    """작업 결과 문서의 `PR` 값이 링크 · `없음(사유)` 중 하나인지 본다.

    이 문서는 PR을 연 뒤에 만들므로 첫 커밋부터 값이 확정돼 있다 — 임시값은 통과시키지
    않는다(`.ai/work-result/README.md`).

    `added_in_pr`는 이 PR이 새로 추가한 문서라는 뜻이다. 그때 `없음(...)`은 사실일 수 없다 —
    이미 직접 push된 지난 작업의 기록이라면 사유에 **그때 들어간 커밋**을 적어야 한다.
    """
    if PR_LINK.search(value):
        return []
    if PR_NONE.match(value):
        if not added_in_pr:
            return []
        shas = PR_NONE_COMMIT.findall(value)
        if shas and not run.history_available:
            # 얕은 클론이면 오래된 커밋이 없어 정당한 기록도 거짓으로 걸린다. 형식만 보고
            # 통과시키되 무엇을 확인하지 못했는지 남긴다.
            run.warnings.append(
                f"{rel}: 히스토리가 얕아 `{value}`의 커밋을 확인하지 못했다 —"
                " 형식만 보고 통과시킨다"
            )
            return []
        if any(commit_landed(run, sha) for sha in shas):
            return []
        return [
            f"{rel}: `PR: {value}`인데 이 문서는 PR로 올라오고 있다 — 이 PR의 링크를 적는다."
            " 이미 직접 push된 지난 작업을 뒤늦게 기록하는 것이면 사유에 **그때 들어간**"
            " 커밋을 적는다 — 이 PR의 커밋은 근거가 되지 않는다"
            " (`없음(직접 push, abc1234)`) (.ai/work-result/README.md)"
        ]
    return [
        f"{rel}: `PR` 값이 규칙에 어긋난다 (`{value}`) —"
        " PR 링크(`[#12](https://.../pull/12)`) · `없음(사유)` 중 하나다."
        " PR을 연 뒤 링크를 채운 채로 이 문서를 만든다 (.ai/work-result/README.md)"
    ]
