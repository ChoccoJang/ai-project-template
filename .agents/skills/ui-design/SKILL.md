---
name: ui-design
description: 데스크톱 앱(Windows·macOS)과 웹앱(모바일 Android·iOS 브라우저 포함)이 공통으로 쓰는 테마 7종과 시맨틱 컬러 토큰, 플랫폼별 적용 규칙. UI 화면·컴포넌트를 만들거나 고칠 때, 색·테마·다크 모드·CSS 변수를 정할 때, 새 테마를 추가할 때 쓴다.
---

# ui-design — 공통 컬러 토큰과 적용 규칙

데스크톱 앱(Windows·macOS)과 웹앱(모바일 Android·iOS 포함)이 **같은 테마·같은 토큰 이름**으로
색을 쓰게 하는 스킬이다. 값은 생성물이 담고, 이 문서는 **어떻게 쓰는지**만 담는다.

## 파일

| 파일 | 담는 것 | 고치나 |
|---|---|---|
| [`themes.json`](./themes.json) | 테마의 원본 — 이름·모드·base 4색·ANSI 16 | **여기만 고친다** |
| [`tokens.json`](./tokens.json) | 토큰 값·용도·파생 규칙 (네이티브가 읽는다) | 생성물 |
| [`theme.css`](./theme.css) | 웹 CSS 변수 (`[data-theme]`별) | 생성물 |
| [`references/palette.md`](./references/palette.md) | 테마별 값 표 (사람이 훑는 용도) | 생성물 |
| [`references/platforms.md`](./references/platforms.md) | Windows·macOS·모바일 웹 적용 규칙 | 손으로 쓴다 |
| [`scripts/build_tokens.py`](./scripts/build_tokens.py) | 파생 규칙의 단일 출처 · 생성 · 대비 검사 | 규칙을 바꿀 때 |

## 사용 규칙

- **UI 코드는 색 값이 아니라 토큰 이름만 참조한다.** 컴포넌트에 `#RRGGBB`를 두지 않는다.
  웹은 `var(--토큰)`, 네이티브는 `tokens.json`에서 만든 상수·테마 표를 쓴다.
- **토큰을 고르는 기준은 `tokens.json`의 `tokens.<이름>.use`다.** 맞는 토큰이 없으면 값을 직접
  쓰지 말고 토큰 추가를 제안한다(아래 「바꿀 때」).
- **별칭을 새 토큰으로 늘리지 않는다**: 링크·포커스 링 = `accent`, 편집·본문 바탕 = `bg`,
  본문 글자 = `fg`, 가로줄·표 선 = `border`.
- **테마는 id로 저장한다.** id는 영문 소문자+하이픈 고정, 화면에는 `name`을 보인다. 메뉴 순서는
  `themes.json`의 순서다.
- **기본 테마**: 저장값이 없거나 모르는 id면 OS가 다크일 때 `zen-dark`, 아니면 `zen-light`.
- **색 형식**: `#RRGGBB`(불투명 sRGB). 네이티브 정수는 `0xRRGGBB`, Win32 `COLORREF`는
  `0x00BBGGRR`(R·B 교환).

## 적용 규칙

- **표면 층은 `bg → sidebar-bg → panel → pressed → raised`** 순으로 한 겹씩 위다. 층을 건너뛰어
  섞지 않는다.
- **accent 바탕 위 글자는 반드시 `on-accent`**. 흰색 고정이면 밝은 accent에서 안 읽힌다.
- **경계로 컨트롤을 알아봐야 하면 `control-border`, 장식용 구분선은 `border`.** 입력칸·체크박스·
  라디오·토글이 앞쪽이다 — `border`는 대비가 1.4~1.7이라 컨트롤 경계로 쓰면 안 보인다.
- **상태 글자는 `danger`·`success`·`warning`.** 색만으로 상태를 알리지 않고 아이콘이나 문구를
  함께 둔다. 정보성 강조는 `accent`다.
- **`danger-hover`·`on-danger`는 Windows 창 닫기 버튼 전용**이다(테마 무관 고정). 삭제 버튼 같은
  일반 위험 동작에는 `danger`를 쓴다.
- **`highlight`는 노랑 계열 고정** — `selection`과 겹쳐도 갈린다.
- **보조 글자·주석·다이어그램 선은 `text-muted` 계열 하나**로 맞춘다. ANSI 색을 일반 UI에 직접
  쓰지 않는다 — ANSI는 터미널 화면과 파생 입력용이다.
- **그룹 색**(`groups`, 웹은 `--group-N-bg`·`--group-N-border`)은 다이어그램 묶음·태그·카테고리처럼
  여러 무리를 색으로 가를 때 순서대로 쓰고, 7번째부터 1번으로 돌아간다.

**대비는 `build_tokens.py`의 `CONTRAST_CHECKS`에 있는 짝만 보장한다**(글자 WCAG AA 4.5:1,
컨트롤 경계 3:1). 자주 걸리는 것은 다음과 같다.

| 토큰 | 보장하는 바탕 | 그 밖의 바탕에서는 |
|---|---|---|
| `fg` | 모든 표면 층 · `row-hover` · `row-selected` · `selection` · `highlight` | — |
| `text-muted` (placeholder 포함) | `bg` · `sidebar-bg` · `panel` · `code-bg` | 오래 머무는 바탕(선택 행·활성 탭)에서는 `fg`로 올린다 |
| `accent`를 **글자**로 (링크) | `bg` | 사이드바·툴바의 링크·내비게이션은 `fg` 글자에 `accent` 표시(밑줄·막대·아이콘)를 붙인다 |
| `control-border` | `bg` · `sidebar-bg` · `panel` | 입력칸을 `raised` 위에 두지 않는다 |

- **시트·모달·팝오버 본체는 `panel`이다** — 그 안의 입력칸·보조 글자가 위 보장을 그대로 받는다.
  `raised`는 활성 탭·호버한 버튼처럼 **작은 상태 표시**에만 쓴다.

## 플랫폼별 적용

무엇을 만드는지에 따라 [`references/platforms.md`](./references/platforms.md)의 해당 절을 읽는다.

| 만드는 것 | 절 |
|---|---|
| Windows 데스크톱 앱 | 공통 · Windows |
| macOS 데스크톱 앱 | 공통 · macOS |
| 웹앱 (데스크톱 브라우저) | 공통 · 웹 |
| 웹앱 (Android·iOS 브라우저, PWA, 앱 안 WebView) | 공통 · 웹 · 모바일 웹 |

## 바꿀 때

- **새 테마는 `themes.json`에 base(bg·fg·accent·selection + ANSI 16)만 넣는다.** 토큰 값을 손으로
  정하거나 생성물을 고치지 않는다.
- **토큰을 더하거나 파생 규칙을 바꾸는 것은 `build_tokens.py`의 `TOKENS`·`build_theme`을 고친다.**
  기존 앱의 색이 함께 바뀌므로 소유자가 정한다.
- 고친 뒤 스킬 폴더에서 다시 만들고 검사한다(Python 3.11 이상, 표준 라이브러리만).

  ```bash
  python3 scripts/build_tokens.py          # 생성
  python3 scripts/build_tokens.py --check  # 생성물이 최신인지 + 대비 기준 (실패 시 종료 코드 1)
  ```

- **대비 검사가 실패하면 기준을 낮추지 말고 base를 고친다.** 실패 메시지가 어느 테마의 어느 짝인지
  알려 준다.
