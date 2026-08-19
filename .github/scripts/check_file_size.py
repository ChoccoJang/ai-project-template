#!/usr/bin/env python3
"""파일이 정해진 줄 수 상한을 넘지 않는지 검사한다.

규칙은 `.github/file-size.json`이 정한다(상한·예외·baseline).

**래칫(ratchet) 방식이다.** 규칙을 도입할 때 이미 상한을 넘던 파일은 `baseline`에 적어 두고,
그보다 **늘어날 때만** 실패시킨다. 줄어들면 baseline을 낮춘다. 소급 적용해 한꺼번에
쪼개게 만들면, 줄 수만 맞춘 기계적 분할(`FooImpl2`, `utils2`)이 나오기 때문이다.

사용법:
    python3 .github/scripts/check_file_size.py [기준경로]
    python3 .github/scripts/check_file_size.py --update-baseline

위반이 하나라도 있으면 종료 코드 1로 끝난다.
"""

from __future__ import annotations

import json
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

CONFIG_PATH = ".github/file-size.json"


def matches(path: str, pattern: str) -> bool:
    """패턴을 상대 경로에 맞춘다. `build/**`는 하위 디렉터리의 build/도 잡는다."""
    return fnmatch(path, pattern) or fnmatch(path, f"*/{pattern}")


def tracked_files(root: Path) -> list[str]:
    """git이 추적하는 파일만 본다 — 빌드 산출물과 의존성을 자동으로 걸러준다."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        print("git ls-files 실패 — git 저장소에서 실행한다.", file=sys.stderr)
        raise SystemExit(2)
    return [line for line in result.stdout.splitlines() if line]


def limit_for(path: str, config: dict) -> int:
    for rule in config.get("overrides", []):
        if matches(path, rule["pattern"]):
            return int(rule["max"])
    return int(config["default"])


def count_lines(path: Path) -> int | None:
    """텍스트 파일의 줄 수. 바이너리면 None."""
    try:
        with path.open("rb") as handle:
            data = handle.read()
    except OSError:
        return None
    if b"\0" in data:
        return None
    return data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    update = "--update-baseline" in sys.argv[1:]
    root = Path(args[0] if args else ".").resolve()

    config_file = root / CONFIG_PATH
    if not config_file.is_file():
        print(f"{CONFIG_PATH}가 없다 — 파일 크기 검사를 건너뛴다.")
        return 0
    config = json.loads(config_file.read_text(encoding="utf-8"))
    baseline: dict[str, int] = dict(config.get("baseline", {}))
    exempt = config.get("exempt", [])

    over_limit: dict[str, int] = {}   # 상한을 넘은 파일 → 현재 줄 수
    problems: list[str] = []
    notes: list[str] = []

    for rel in tracked_files(root):
        if any(matches(rel, pattern) for pattern in exempt):
            continue
        lines = count_lines(root / rel)
        if lines is None:
            continue
        limit = limit_for(rel, config)
        if lines <= limit:
            if rel in baseline:
                notes.append(f"{rel}: {lines}줄로 내려와 상한({limit})을 지킨다 — baseline에서 뺀다")
                baseline.pop(rel)
            continue

        over_limit[rel] = lines
        allowed = baseline.get(rel)
        if allowed is None:
            problems.append(
                f"{rel}: {lines}줄 (상한 {limit})."
                " 새로 상한을 넘었다 — 줄 수에 맞춰 자르지 말고 개념 단위로 나눈다"
            )
        elif lines > allowed:
            problems.append(
                f"{rel}: {lines}줄 (baseline {allowed}). 이미 상한을 넘던 파일이 더 늘었다"
                " — 이 파일에 더 넣지 말고 다른 곳에 두거나 먼저 줄인다"
            )
        elif lines < allowed:
            notes.append(f"{rel}: {allowed} → {lines}줄로 줄었다 — baseline을 낮춘다")
            baseline[rel] = lines

    if update:
        config["baseline"] = dict(sorted(over_limit.items()))
        config_file.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"baseline을 갱신했다 — {len(over_limit)}개 파일.")
        return 0

    for note in notes:
        print(f"  · {note}")

    if problems:
        print("파일 크기 규칙 위반:")
        for problem in problems:
            print(f"  - {problem}")
        print(
            f"\n총 {len(problems)}건. 상한과 예외는 {CONFIG_PATH},"
            " 쪼개는 기준은 AGENTS.md 6절 참고."
        )
        return 1

    if notes:
        print("  (위 항목은 `--update-baseline`으로 반영한다)")
    print("파일 크기 규칙 이상 없음.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
