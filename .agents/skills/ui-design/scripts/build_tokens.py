#!/usr/bin/env python3
"""themes.json(base)에서 컬러 토큰을 만들고 대비를 검사한다.

    python3 scripts/build_tokens.py           # tokens.json · theme.css · references/palette.md 생성
    python3 scripts/build_tokens.py --check   # 생성물이 최신인지와 대비 기준을 확인 (실패 시 1)

표준 라이브러리만 쓴다(Python 3.11 이상). 파생 규칙은 아래 TOKENS 표 하나가 단일 출처다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE = SKILL_DIR / "themes.json"
TOKENS_JSON = SKILL_DIR / "tokens.json"
THEME_CSS = SKILL_DIR / "theme.css"
PALETTE_MD = SKILL_DIR / "references" / "palette.md"

TEXT_CONTRAST = 4.5  # WCAG 2.x AA 본문
NON_TEXT_CONTRAST = 3.0  # WCAG 2.x AA 컨트롤 경계·그래픽
DARK_ON_LIGHT = "#141416"
LIGHT_ON_DARK = "#FFFFFF"
MIX_STEPS = 100

# 문법 색·그룹 색이 ANSI 몇 번을 쓰는지 — (dark 테마 번호, light 테마 번호)
ANSI_RED, ANSI_GREEN, ANSI_YELLOW = (9, 1), (10, 2), (11, 3)
ANSI_BLUE, ANSI_MAGENTA, ANSI_CYAN = (12, 4), (13, 5), (14, 6)
ANSI_MUTED = 8
GROUP_HUES = [ANSI_GREEN, ANSI_MAGENTA, ANSI_YELLOW, ANSI_BLUE, ANSI_RED, ANSI_CYAN]

DERIVATION = {
    "mix(a, b, t)": "채널별 a + (b - a) * t, 반올림",
    "up": "dark 테마 #FFFFFF, light 테마 #000000",
    "x/y": "dark 테마 값 / light 테마 값",
    "contrast(a, b)": "WCAG 2.x 대비 (Lmax + 0.05) / (Lmin + 0.05), L은 선형화한 상대 휘도",
    "text-surfaces": "bg · sidebar-bg · panel · code-bg — 글자가 놓이는 바탕",
    "readable(c, n)": "mix(c, fg, t)에서 text-surfaces 모두와 contrast >= n이 되는 가장 작은 t (0.01 단위). n을 생략하면 4.5",
    "group": "hue = ANSI 초록·자홍·노랑·파랑·빨강·청록 (dark 10,13,11,12,9,14 / light 2,5,3,4,1,6), "
    "accent와 가장 가까운 hue를 맨 뒤로. bg = mix(bg, hue, 0.11), border = mix(bg, hue, 0.45)",
}


# ── 색 계산 ──────────────────────────────────────────────────────────────


def to_rgb(color: str) -> tuple[int, int, int]:
    return tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))


def to_hex(rgb: tuple[int, ...]) -> str:
    return "#%02X%02X%02X" % rgb


def mix(a: str, b: str, t: float) -> str:
    ra, rb = to_rgb(a), to_rgb(b)
    return to_hex(tuple(int(ra[i] + (rb[i] - ra[i]) * t + 0.5) for i in range(3)))


def luminance(color: str) -> float:
    def channel(v: int) -> float:
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = map(channel, to_rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def push_until(color: str, toward: str, surfaces: list[str], target: float) -> str:
    """color를 toward 쪽으로 조금씩 옮겨 모든 surfaces와 target 대비를 넘는 첫 값."""
    for step in range(MIX_STEPS + 1):
        candidate = mix(color, toward, step / MIX_STEPS)
        if all(contrast(candidate, s) >= target for s in surfaces):
            return candidate
    return toward


def hue_distance(a: str, b: str) -> float:
    return sum((x - y) ** 2 for x, y in zip(to_rgb(a), to_rgb(b)))


# ── 토큰 표: (이름, 분류, 용도, 규칙 설명, 계산) ─────────────────────────


def build_theme(theme: dict) -> tuple[dict, list[dict]]:
    dark = theme["mode"] == "dark"
    bg, fg, accent, ansi = theme["bg"], theme["fg"], theme["accent"], theme["ansi"]
    up = "#FFFFFF" if dark else "#000000"

    def pick(pair):  # (dark, light)
        return pair[0] if dark else pair[1]

    def a(pair):
        return ansi[pick(pair)]

    t: dict[str, str] = {}
    t["bg"], t["fg"], t["accent"], t["selection"] = bg, fg, accent, theme["selection"]
    t["text-strong"] = fg
    t["sidebar-bg"] = mix(bg, up, pick((0.03, 0.02)))
    t["panel"] = mix(bg, up, pick((0.05, 0.04)))
    t["pressed"] = mix(bg, up, pick((0.09, 0.07)))
    t["raised"] = mix(bg, up, pick((0.14, 0.10)))
    t["code-bg"] = mix(bg, fg, 0.06)
    surfaces = [bg, t["sidebar-bg"], t["panel"], t["code-bg"]]

    def readable(color, target=TEXT_CONTRAST):
        return push_until(color, fg, surfaces, target)

    t["text-muted"] = readable(ansi[ANSI_MUTED])
    t["on-accent"] = max((DARK_ON_LIGHT, LIGHT_ON_DARK), key=lambda c: contrast(c, accent))
    t["border"] = mix(bg, fg, 0.18)
    t["control-border"] = push_until(t["border"], fg, [bg, t["sidebar-bg"], t["panel"]], NON_TEXT_CONTRAST)
    t["row-hover"] = mix(bg, fg, 0.07)
    t["row-selected"] = mix(bg, accent, 0.20)
    t["tree-guide"] = mix(bg, fg, 0.13)

    yellow, ratio = a(ANSI_YELLOW), pick((0.36, 0.30))
    while contrast(fg, mix(bg, yellow, ratio)) < TEXT_CONTRAST and ratio > 0:
        ratio = round(ratio - 0.01, 2)
    t["highlight"] = mix(bg, yellow, ratio)

    t["danger"] = readable(a(ANSI_RED))
    t["success"] = readable(a(ANSI_GREEN))
    t["warning"] = readable(a(ANSI_YELLOW))
    t["danger-hover"], t["on-danger"] = "#C42B1C", "#FFFFFF"
    t["code-action-bg"] = mix(bg, up, pick((0.10, 0.08)))
    t["code-inline"] = readable(a(ANSI_MAGENTA))
    t["syntax-comment"] = t["text-muted"]
    t["syntax-string"] = readable(a(ANSI_GREEN))
    t["syntax-number"] = readable(a(ANSI_CYAN))
    t["syntax-keyword"] = readable(a(ANSI_BLUE))
    t["diagram-node-bg"] = mix(bg, accent, 0.16)
    t["diagram-node-border"] = mix(bg, accent, 0.45)
    t["diagram-line"] = t["text-muted"]

    hues = [a(h) for h in GROUP_HUES]
    nearest = min(range(len(hues)), key=lambda i: hue_distance(hues[i], accent))
    hues.append(hues.pop(nearest))
    groups = [{"bg": mix(bg, h, 0.11), "border": mix(bg, h, 0.45)} for h in hues]

    return {name: t[name] for name, *_ in TOKENS}, groups


TOKENS = [
    ("bg", "기본", "앱·본문·편집 영역 바탕", "base.bg"),
    ("fg", "기본", "본문 글자", "base.fg"),
    ("accent", "기본", "강조·링크·포커스 링", "base.accent"),
    ("selection", "기본", "텍스트 선택 영역", "base.selection"),
    ("text-strong", "기본", "제목·활성 라벨", "fg"),
    ("text-muted", "기본", "보조 글자·placeholder·비활성", "readable(ansi8)"),
    ("on-accent", "기본", "accent 바탕 위 글자", "#141416·#FFFFFF 중 accent와 contrast가 큰 쪽"),
    ("border", "기본", "구분선·표 선 (장식용)", "mix(bg, fg, 0.18)"),
    ("control-border", "기본", "입력칸·체크박스·토글처럼 경계가 있어야 알아보는 컨트롤 테두리",
     "border를 fg 쪽으로 옮겨 bg·sidebar-bg·panel과 contrast >= 3"),
    ("sidebar-bg", "표면 층 (아래 → 위)", "사이드바·트리 바탕", "mix(bg, up, 0.03/0.02)"),
    ("panel", "표면 층 (아래 → 위)", "타이틀바·툴바·상태바·탭 줄·하단 탭바·시트·모달·팝오버 바탕", "mix(bg, up, 0.05/0.04)"),
    ("pressed", "표면 층 (아래 → 위)", "눌린 버튼·터치 중인 항목", "mix(bg, up, 0.09/0.07)"),
    ("raised", "표면 층 (아래 → 위)", "활성 탭·호버한 버튼", "mix(bg, up, 0.14/0.10)"),
    ("row-hover", "목록·트리", "행 호버", "mix(bg, fg, 0.07)"),
    ("row-selected", "목록·트리", "행 선택", "mix(bg, accent, 0.20)"),
    ("tree-guide", "목록·트리", "들여쓰기 가이드선", "mix(bg, fg, 0.13)"),
    ("highlight", "상태", "검색 일치 바탕",
     "mix(bg, ansi11/ansi3, t), t는 0.36/0.30에서 contrast(fg, 결과) >= 4.5가 될 때까지 0.01씩 줄인다"),
    ("danger", "상태", "오류·삭제 글자와 아이콘, 오류 입력칸 테두리", "readable(ansi9/ansi1)"),
    ("success", "상태", "성공·완료 글자와 아이콘", "readable(ansi10/ansi2)"),
    ("warning", "상태", "경고 글자와 아이콘", "readable(ansi11/ansi3)"),
    ("danger-hover", "상태", "창 닫기 버튼 호버 — Windows 전용, 테마 무관 고정", "#C42B1C"),
    ("on-danger", "상태", "danger-hover 위 글자 (고정)", "#FFFFFF"),
    ("code-bg", "코드", "코드 블록 바탕", "mix(bg, fg, 0.06)"),
    ("code-action-bg", "코드", "코드 블록 위 버튼(복사 등)", "mix(bg, up, 0.10/0.08)"),
    ("code-inline", "코드", "인라인 코드 글자", "readable(ansi13/ansi5)"),
    ("syntax-comment", "코드", "주석", "text-muted"),
    ("syntax-string", "코드", "문자열", "readable(ansi10/ansi2)"),
    ("syntax-number", "코드", "숫자", "readable(ansi14/ansi6)"),
    ("syntax-keyword", "코드", "키워드", "readable(ansi12/ansi4)"),
    ("diagram-node-bg", "다이어그램", "노드 바탕", "mix(bg, accent, 0.16)"),
    ("diagram-node-border", "다이어그램", "노드 테두리", "mix(bg, accent, 0.45)"),
    ("diagram-line", "다이어그램", "연결선·화살표", "text-muted"),
]

# (글자·선 토큰, 바탕 토큰들, 기준) — 생성 결과가 이 표를 못 넘으면 base를 고쳐야 한다
CONTRAST_CHECKS = [
    ("fg", ["bg", "sidebar-bg", "panel", "raised", "row-hover", "row-selected", "selection", "highlight", "code-bg"], TEXT_CONTRAST),
    ("text-muted", ["bg", "sidebar-bg", "panel", "code-bg"], TEXT_CONTRAST),
    ("accent", ["bg"], TEXT_CONTRAST),
    ("on-accent", ["accent"], TEXT_CONTRAST),
    ("control-border", ["bg", "sidebar-bg", "panel"], NON_TEXT_CONTRAST),
    ("danger", ["bg", "panel"], TEXT_CONTRAST),
    ("success", ["bg", "panel"], TEXT_CONTRAST),
    ("warning", ["bg", "panel"], TEXT_CONTRAST),
    ("on-danger", ["danger-hover"], TEXT_CONTRAST),
    ("code-inline", ["bg", "code-bg"], TEXT_CONTRAST),
    ("syntax-string", ["code-bg"], TEXT_CONTRAST),
    ("syntax-number", ["code-bg"], TEXT_CONTRAST),
    ("syntax-keyword", ["code-bg"], TEXT_CONTRAST),
    ("diagram-line", ["bg"], NON_TEXT_CONTRAST),
]


# ── 출력물 ───────────────────────────────────────────────────────────────


def dump_json(value, indent: int = 0) -> str:
    """사람이 훑기 좋게: 스칼라만 담은 리스트·짧은 객체는 한 줄로."""
    pad, inner = "  " * indent, "  " * (indent + 1)
    if isinstance(value, list) and all(not isinstance(v, (dict, list)) for v in value):
        return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in value) + "]"
    if isinstance(value, dict):
        flat = "{" + ", ".join(f"{json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in value.items()) + "}"
        if all(not isinstance(v, (dict, list)) for v in value.values()) and len(flat) <= 110:
            return flat
        body = ",\n".join(f"{inner}{json.dumps(k, ensure_ascii=False)}: {dump_json(v, indent + 1)}" for k, v in value.items())
        return "{\n" + body + "\n" + pad + "}"
    if isinstance(value, list):
        body = ",\n".join(inner + dump_json(v, indent + 1) for v in value)
        return "[\n" + body + "\n" + pad + "]"
    return json.dumps(value, ensure_ascii=False)


def render_tokens_json(source: dict, built: dict) -> str:
    data = {
        "version": 2,
        "_안내": "생성물이다 — themes.json을 고치고 scripts/build_tokens.py로 다시 만든다.",
        "format": "#RRGGBB (sRGB, opaque)",
        "default": {**source["default"], "rule": "저장값이 없거나 모르는 id면 OS 모드에 따라 light/dark 기본 테마"},
        "derivation": DERIVATION,
        "tokens": {name: {"use": use, "rule": rule} for name, _, use, rule in TOKENS},
        "themes": {
            tid: {
                "name": theme["name"],
                "mode": theme["mode"],
                "base": {k: theme[k] for k in ("bg", "fg", "accent", "selection", "ansi")},
                "tokens": built[tid][0],
                "groups": built[tid][1],
            }
            for tid, theme in source["themes"].items()
        },
    }
    return dump_json(data) + "\n"


def css_declarations(tokens: dict, groups: list[dict], pad: str) -> list[str]:
    lines = []
    for category in dict.fromkeys(c for _, c, _, _ in TOKENS):
        names = [n for n, c, _, _ in TOKENS if c == category]
        lines.append(pad + " ".join(f"--{n}: {tokens[n]};" for n in names))
    for start in (0, 3):
        lines.append(pad + " ".join(
            f"--group-{i + 1}-bg: {g['bg']}; --group-{i + 1}-border: {g['border']};"
            for i, g in enumerate(groups[start : start + 3], start)))
    return lines


def render_css(source: dict, built: dict) -> str:
    themes, default = source["themes"], source["default"]
    out = [
        "/* 생성물이다 — themes.json을 고치고 scripts/build_tokens.py로 다시 만든다. */",
        '/* <html data-theme="nord">처럼 루트에 id를 건다. 없거나 모르는 id면 OS 모드를 따른다. */',
        "",
    ]
    # :root와 [data-theme]는 명시도가 같아 뒤에 오는 쪽이 이긴다 — 기본 테마 블록을 맨 앞에 둔다
    ordered = [default["light"]] + [tid for tid in themes if tid != default["light"]]
    for tid in ordered:
        theme = themes[tid]
        selector = f'[data-theme="{tid}"]'
        if tid == default["light"]:
            selector = ":root, " + selector
        out += [selector + " {", f"  color-scheme: {theme['mode']};"]
        out += css_declarations(*built[tid], "  ") + ["}", ""]
    known = ",\n".join(f'    [data-theme="{tid}"]' for tid in themes)
    dark_id = default["dark"]
    out += [
        f"/* data-theme가 없거나 모르는 id일 때 OS가 다크면 {dark_id} (라이트면 위 :root의 {default['light']}) */",
        "@media (prefers-color-scheme: dark) {",
        f"  :root:not(:is(\n{known}\n  )) {{",
        "    color-scheme: dark;",
        *css_declarations(*built[dark_id], "    "),
        "  }",
        "}",
    ]
    return "\n".join(out) + "\n"


def render_palette(source: dict, built: dict) -> str:
    ids = list(source["themes"])
    head = "| " + " | ".join(f"`{i}`" for i in ids) + " |"
    rule = "|" + "---|" * len(ids)
    out = [
        "# 팔레트 — 테마별 토큰 값",
        "",
        "> 생성물이다 — [`../themes.json`](../themes.json)을 고치고 `scripts/build_tokens.py`로 다시 만든다.",
        "> 토큰의 뜻과 쓰는 법은 [`../SKILL.md`](../SKILL.md), 파생 규칙은 [`../tokens.json`](../tokens.json)의 `tokens`.",
        "",
        "## 테마 목록",
        "",
        "목록 순서가 메뉴·설정 화면의 순서다. 앞의 둘이 기본 테마다.",
        "",
        "| id | 표시 이름 | 모드 | bg | fg | accent | selection |",
        "|---|---|---|---|---|---|---|",
    ]
    for tid, th in source["themes"].items():
        out.append(f"| `{tid}` | {th['name']} | {th['mode']} | `{th['bg']}` | `{th['fg']}` | `{th['accent']}` | `{th['selection']}` |")
    for category in dict.fromkeys(c for _, c, _, _ in TOKENS):
        out += ["", f"## {category}", "", "| 토큰 " + head, "|---" + rule]
        for name, c, _, _ in TOKENS:
            if c == category:
                out.append(f"| `{name}` | " + " | ".join(f"`{built[i][0][name]}`" for i in ids) + " |")
    out += ["", "## 그룹 색 (`bg` / `border`, 6벌 순환)", "", "| 순서 " + head, "|---" + rule]
    for n in range(6):
        out.append(f"| {n + 1} | " + " | ".join(f"`{built[i][1][n]['bg']}` / `{built[i][1][n]['border']}`" for i in ids) + " |")
    names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    out += ["", "## base — ANSI 16", "", "0~7 기본, 8~15 밝은 짝. 터미널 화면과 파생 규칙의 입력이다.", "",
            "| ANSI " + head, "|---" + rule]
    for n in range(16):
        label = f"{n} {'bright ' if n >= 8 else ''}{names[n % 8]}"
        out.append(f"| {label} | " + " | ".join(f"`{source['themes'][i]['ansi'][n]}`" for i in ids) + " |")
    return "\n".join(out) + "\n"


# ── 실행 ─────────────────────────────────────────────────────────────────


def contrast_failures(built: dict) -> list[str]:
    failures = []
    for tid, (tokens, _) in built.items():
        for front, backs, target in CONTRAST_CHECKS:
            for back in backs:
                ratio = contrast(tokens[front], tokens[back])
                if ratio < target:
                    failures.append(f"{tid}: {front} on {back} = {ratio:.2f} < {target}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="파일을 쓰지 않고 최신인지·대비 기준을 확인한다")
    args = parser.parse_args()

    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    built = {tid: build_theme(theme) for tid, theme in source["themes"].items()}
    outputs = {
        TOKENS_JSON: render_tokens_json(source, built),
        THEME_CSS: render_css(source, built),
        PALETTE_MD: render_palette(source, built),
    }

    problems = contrast_failures(built)
    if args.check:
        for path, text in outputs.items():
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != text:
                problems.append(f"{path.relative_to(SKILL_DIR)}: themes.json과 어긋난다 — build_tokens.py를 다시 돌린다")
    else:
        for path, text in outputs.items():
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"생성: {path.relative_to(SKILL_DIR)}")

    for problem in problems:
        print(f"실패: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
