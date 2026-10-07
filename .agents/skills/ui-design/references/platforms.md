# 플랫폼별 적용

토큰의 뜻과 공통 규칙은 [`../SKILL.md`](../SKILL.md)가 정한다. 이 문서는 **플랫폼마다 달라지는
것**만 담는다.

## 공통

- **테마 전환은 표 하나를 갈아 끼우는 일이다.** 활성 테마 id 하나를 상태로 두고, 화면은 그 테마의
  토큰 표에서 색을 꺼낸다. 컴포넌트가 테마 id로 분기하지 않는다.
- **OS 모드 변경을 따라간다.** 사용자가 테마를 고른 적이 없으면(저장값 없음) OS가 라이트↔다크로
  바뀔 때 기본 테마도 바로 바꾼다. 고른 적이 있으면 OS 모드를 무시한다.
- **고대비·강제 색 모드에서는 토큰을 내려놓고 OS 시스템 색을 쓴다.** 사용자가 OS에서 고른 색이
  우선이다.
- **비활성 컨트롤**은 글자에 `text-muted`, 바탕은 그 층 그대로 둔다. 불투명도로 흐리게 만들지
  않는다 — 토큰이 불투명 색이라 겹치는 층에 따라 값이 달라진다.

## Windows

- **네이티브 정수 색은 `COLORREF` = `0x00BBGGRR`**이다. `tokens.json`을 읽어 변환할 때 R·B를 바꾼다.
- **제목 표시줄을 직접 그리면** 바탕은 `panel`, 최소화·최대화 버튼은 호버 `raised`·눌림 `pressed`,
  **닫기 버튼만** 호버 `danger-hover` + 글자 `on-danger`다(OS 관례).
- **시스템 제목 표시줄을 쓰면** 다크 테마일 때 `DwmSetWindowAttribute`로
  `DWMWA_USE_IMMERSIVE_DARK_MODE`를 켜고, Windows 11에서는 `DWMWA_CAPTION_COLOR`를 `panel`로
  맞춘다. 켜지 않으면 다크 테마 창에 흰 제목 표시줄이 붙는다.
- **OS 모드**는 `UISettings`의 배경색(또는 레지스트리 `AppsUseLightTheme`)으로 읽고,
  `WM_SETTINGCHANGE`(`ImmersiveColorSet`)를 받아 다시 읽는다.
- **고대비 모드**(`SPI_GETHIGHCONTRAST`)에서는 `GetSysColor`의 시스템 색을 쓴다.

## macOS

- **신호등 버튼(닫기·최소화·확대)은 직접 그리지 않는다.** 시스템 것을 그대로 두므로
  `danger-hover`·`on-danger`는 쓰지 않는다.
- **창의 `NSAppearance`를 테마 모드에 맞춘다** — dark 테마면 `.darkAqua`, light면 `.aqua`. 그래야
  스크롤바·메뉴·시스템 컨트롤이 토큰 색과 어긋나지 않는다.
- **색은 sRGB로 만든다** — `NSColor(srgbRed:green:blue:alpha:)`, SwiftUI는
  `Color(.sRGB, red:green:blue:)`. 기본 색 공간(Display P3 등)으로 만들면 값이 달라 보인다.
- **사이드바에 `NSVisualEffectView`(반투명)를 쓰면 `sidebar-bg`와 함께 쓰지 않는다.** 둘 중
  하나를 고르고, 반투명을 고르면 그 위 글자 대비는 직접 확인한다.
- **OS 모드**는 `NSApp.effectiveAppearance`를 관찰해 따라간다. "대비 증가" 설정
  (`accessibilityDisplayShouldIncreaseContrast`)이 켜지면 `border` 대신 `control-border`를 쓴다.

## 웹

- **[`../theme.css`](../theme.css)를 그대로 가져다 쓴다.** 루트에 `<html data-theme="nord">`처럼 id를
  건다. 없거나 모르는 id면 OS 모드를 따른다.
- **첫 화면이 깜빡이지 않게** 저장된 id를 `<head>` 안 인라인 스크립트에서 CSS가 칠해지기 전에
  `data-theme`으로 건다. 저장소 접근은 실패할 수 있으니 `try`로 감싸고, 실패하면 속성을 걸지
  않는다(OS 모드를 따른다).
- **선택 영역**: `::selection { background: var(--selection); color: var(--fg); }`
- **포커스**: `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }` —
  `outline: none`만 하고 대신할 표시를 두지 않는 것은 금지다.
- **강제 색 모드**: `@media (forced-colors: active)`에서는 토큰 대신 `Canvas`·`CanvasText`·
  `Highlight`·`ButtonText` 같은 시스템 색 키워드를 쓴다.
- **모달 뒤 가림막(scrim)은 토큰이 아니다.** 검정에 불투명도 — light 40%, dark 60% — 로 고정한다.
  모달 본체는 `panel`이다(대비 보장 — [`../SKILL.md`](../SKILL.md)의 대비 표).

## 모바일 웹 (Android·iOS 브라우저 · PWA · 앱 안 WebView)

**웹 절을 먼저 지키고 아래를 더한다.**

- **브라우저 UI 색을 테마에 맞춘다.** `<meta name="theme-color">`를 활성 테마의 `panel`로 두고,
  테마를 바꿀 때 함께 바꾼다. 기본 테마용으로는 `media="(prefers-color-scheme: dark)"`가 붙은
  것과 안 붙은 것 두 개를 둔다. `<meta name="color-scheme" content="light dark">`도 둔다.
  PWA는 `manifest`의 `theme_color`·`background_color`를 기본 테마의 `panel`·`bg`로 맞춘다.
- **호버가 없다.** `:hover` 스타일은 `@media (hover: hover)` 안에만 두고, 터치에는 `:active`에
  `pressed`를 준다. `-webkit-tap-highlight-color: transparent`로 기본 회색 번쩍임을 끄되 그
  대신 `:active` 표시를 반드시 둔다.
- **터치 대상은 최소 44×44 CSS px**(iOS 44pt), 여유가 있으면 48px(Android 48dp). 행·아이콘
  버튼의 보이는 크기가 작으면 패딩으로 누르는 영역을 키운다.
- **입력칸 글자는 16px 이상**이다 — 그보다 작으면 iOS Safari가 포커스 때 화면을 확대한다.
  입력칸 테두리는 `control-border`, 오류일 때 `danger`다.
- **노치·홈 인디케이터**: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`로
  두고, 상단 바·하단 탭 바에 `env(safe-area-inset-*)`만큼 패딩을 준다. 그 패딩 영역도 같은
  `panel`로 칠해 바가 화면 끝까지 이어지게 한다.
- **하단 탭 바·상단 앱 바·바텀 시트는 `panel`**, 시트의 손잡이는 `control-border`다. 시트가 바탕과
  갈리는 것은 색 차이가 아니라 가림막(scrim)이 맡는다.
- **앱 안 WebView(하이브리드 앱)**는 네이티브 셸이 상태 표시줄·내비게이션 바 색을 `panel`로
  맞추고, 아이콘 밝기를 테마 모드에 맞춘다(dark 테마면 밝은 아이콘). 활성 테마 id는 웹과
  네이티브가 하나의 값을 공유한다.
