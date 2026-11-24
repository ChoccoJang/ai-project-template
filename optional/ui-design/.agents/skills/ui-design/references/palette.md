# 팔레트 — 테마별 토큰 값

> 생성물이다 — [`../themes.json`](../themes.json)을 고치고 `scripts/build_tokens.py`로 다시 만든다.
> 토큰의 뜻과 쓰는 법은 [`../SKILL.md`](../SKILL.md), 파생 규칙은 [`../tokens.json`](../tokens.json)의 `tokens`.

## 테마 목록

목록 순서가 메뉴·설정 화면의 순서다. 앞의 둘이 기본 테마다.

| id | 표시 이름 | 모드 | bg | fg | accent | selection |
|---|---|---|---|---|---|---|
| `zen-light` | zen light | light | `#F6F7F9` | `#2B2F36` | `#2F6FD0` | `#C2D6F0` |
| `zen-dark` | zen dark | dark | `#181A1F` | `#F2F4F9` | `#7CC4FF` | `#3D5A80` |
| `nord` | Nord | dark | `#2E3440` | `#D8DEE9` | `#88C0D0` | `#434C5E` |
| `flexoki-light` | Flexoki light | light | `#FFFCF0` | `#100F0F` | `#BC5215` | `#E6E4D9` |
| `flexoki-dark` | Flexoki dark | dark | `#100F0F` | `#CECDC3` | `#D0A215` | `#343331` |
| `island-light` | Island light | light | `#FFFFFF` | `#2B2D30` | `#2F6FD0` | `#C8DDF5` |
| `island-dark` | Island dark | dark | `#1E1F22` | `#BCBEC4` | `#5394EC` | `#2E436E` |

## 기본

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `bg` | `#F6F7F9` | `#181A1F` | `#2E3440` | `#FFFCF0` | `#100F0F` | `#FFFFFF` | `#1E1F22` |
| `fg` | `#2B2F36` | `#F2F4F9` | `#D8DEE9` | `#100F0F` | `#CECDC3` | `#2B2D30` | `#BCBEC4` |
| `accent` | `#2F6FD0` | `#7CC4FF` | `#88C0D0` | `#BC5215` | `#D0A215` | `#2F6FD0` | `#5394EC` |
| `selection` | `#C2D6F0` | `#3D5A80` | `#434C5E` | `#E6E4D9` | `#343331` | `#C8DDF5` | `#2E436E` |
| `text-strong` | `#2B2F36` | `#F2F4F9` | `#D8DEE9` | `#100F0F` | `#CECDC3` | `#2B2D30` | `#BCBEC4` |
| `text-muted` | `#636A77` | `#898F99` | `#A1A9B7` | `#575653` | `#878580` | `#6E6F6F` | `#8F9195` |
| `on-accent` | `#FFFFFF` | `#141416` | `#141416` | `#FFFFFF` | `#141416` | `#FFFFFF` | `#141416` |
| `border` | `#D1D3D6` | `#3F4146` | `#4D535E` | `#D4D1C8` | `#32312F` | `#D9D9DA` | `#3A3C3F` |
| `control-border` | `#85888C` | `#6E7075` | `#828893` | `#8D8B85` | `#696863` | `#8C8D8F` | `#717377` |

## 표면 층 (아래 → 위)

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `sidebar-bg` | `#F1F2F4` | `#1F2126` | `#343A46` | `#FAF7EB` | `#171616` | `#FAFAFA` | `#252629` |
| `panel` | `#ECEDEF` | `#24252A` | `#383E4A` | `#F5F2E6` | `#1C1B1B` | `#F5F5F5` | `#292A2D` |
| `pressed` | `#E5E6E8` | `#2D2F33` | `#414651` | `#EDEADF` | `#262525` | `#EDEDED` | `#323336` |
| `raised` | `#DDDEE0` | `#383A3E` | `#4B505B` | `#E6E3D8` | `#313131` | `#E6E6E6` | `#3E3E41` |

## 목록·트리

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `row-hover` | `#E8E9EB` | `#27292E` | `#3A404C` | `#EEEBE0` | `#1D1C1C` | `#F0F0F1` | `#292A2D` |
| `row-selected` | `#CEDCF1` | `#2C3C4C` | `#40505D` | `#F2DAC4` | `#362C10` | `#D5E2F6` | `#29364A` |
| `tree-guide` | `#DCDDE0` | `#34363B` | `#444A56` | `#E0DDD3` | `#292826` | `#E3E4E4` | `#333437` |

## 상태

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `highlight` | `#DACDAE` | `#665D4B` | `#676157` | `#E6D8A8` | `#554411` | `#E3D2B3` | `#544E30` |
| `danger` | `#B8423D` | `#F2969C` | `#CB9CA6` | `#AF3029` | `#D16055` | `#C62828` | `#FF8785` |
| `success` | `#4C7534` | `#B8E2A3` | `#A3BE8C` | `#5D750B` | `#879A39` | `#1A7F37` | `#C0D94B` |
| `warning` | `#8C6207` | `#F2D59A` | `#EBCB8B` | `#876704` | `#D0A215` | `#986403` | `#FFE15C` |
| `danger-hover` | `#C42B1C` | `#C42B1C` | `#C42B1C` | `#C42B1C` | `#C42B1C` | `#C42B1C` | `#C42B1C` |
| `on-danger` | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` |

## 코드

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `code-bg` | `#EAEBED` | `#25272C` | `#383E4A` | `#F1EEE3` | `#1B1A1A` | `#F2F2F3` | `#27292C` |
| `code-action-bg` | `#E2E3E5` | `#2F3135` | `#434853` | `#EBE8DD` | `#282727` | `#EBEBEB` | `#353538` |
| `code-inline` | `#A63D8B` | `#E0A9EC` | `#BC9FBA` | `#A02F6F` | `#CE5D97` | `#9C27B0` | `#D1A2E0` |
| `syntax-comment` | `#636A77` | `#898F99` | `#A1A9B7` | `#575653` | `#878580` | `#6E6F6F` | `#8F9195` |
| `syntax-string` | `#4C7534` | `#B8E2A3` | `#A3BE8C` | `#5D750B` | `#879A39` | `#1A7F37` | `#C0D94B` |
| `syntax-number` | `#2A747B` | `#7FD8E3` | `#8FBCBB` | `#227770` | `#3AA99F` | `#107A84` | `#6CDADA` |
| `syntax-keyword` | `#2F69C1` | `#8EC8FF` | `#8FABC7` | `#205EA6` | `#4988BE` | `#2F6DCB` | `#7EAEF1` |

## 다이어그램

| 토큰 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| `diagram-node-bg` | `#D6E1F2` | `#283543` | `#3C4A57` | `#F4E1CD` | `#2F2710` | `#DEE8F7` | `#263242` |
| `diagram-node-border` | `#9CBAE7` | `#456784` | `#577381` | `#E1B08D` | `#665112` | `#A1BEEA` | `#36547D` |
| `diagram-line` | `#636A77` | `#898F99` | `#A1A9B7` | `#575653` | `#878580` | `#6E6F6F` | `#8F9195` |

## 그룹 색 (`bg` / `border`, 6벌 순환)

| 순서 | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| 1 | `#E4E9E3` / `#ABBFA0` | `#2A302E` / `#60745A` | `#3B4348` / `#637262` | `#EEEED7` / `#BAC489` | `#1D1E14` / `#464E22` | `#E6F1E9` / `#98C5A5` | `#303327` / `#677334` |
| 2 | `#EDE3ED` / `#D2A3C8` | `#2E2A36` / `#725A7B` | `#3D3E4C` / `#6A5D71` | `#F5E5E2` / `#D4A0B6` | `#25181E` / `#66324C` | `#F4E7F6` / `#D29EDB` | `#322D37` / `#6F5A78` |
| 3 | `#ECE7DE` / `#CDB889` | `#302F2D` / `#7A6E56` | `#434548` / `#837862` | `#F6EFD6` / `#DAC684` | `#161C22` / `#27445E` | `#F5EEE3` / `#D4BB8C` | `#373428` / `#83763C` |
| 4 | `#F1E3E4` / `#E0A6A5` | `#30282D` / `#7A5257` | `#37404E` / `#53657A` | `#E6EBE8` / `#9BB5CF` | `#251615` / `#672B26` | `#F9E7E7` / `#E59E9E` | `#372A2D` / `#834E4F` |
| 5 | `#E0ECEE` / `#9AC8CC` | `#232F35` / `#467077` | `#3E3945` / `#6F4853` | `#E7EFE3` / `#9CC6BB` | `#15201F` / `#235450` | `#E5F1F2` / `#93C4C9` | `#273436` / `#417375` |
| 6 | `#E0E8F4` / `#9CBAE7` | `#252D38` / `#4D6884` | `#39434E` / `#5A7177` | `#F6E6DA` / `#DBA096` | `#251F10` / `#665112` | `#E8EFFA` / `#A1BEEA` | `#292F39` / `#495F7F` |

## base — ANSI 16

0~7 기본, 8~15 밝은 짝. 터미널 화면과 파생 규칙의 입력이다.

| ANSI | `zen-light` | `zen-dark` | `nord` | `flexoki-light` | `flexoki-dark` | `island-light` | `island-dark` |
|---|---|---|---|---|---|---|---|
| 0 black | `#2B2F36` | `#454B54` | `#3B4252` | `#100F0F` | `#100F0F` | `#000000` | `#1E1F22` |
| 1 red | `#C4443E` | `#E5757E` | `#BF616A` | `#AF3029` | `#AF3029` | `#C62828` | `#FF6B68` |
| 2 green | `#4F7A34` | `#A3D98E` | `#A3BE8C` | `#66800B` | `#66800B` | `#1A7F37` | `#A8C023` |
| 3 yellow | `#9A6A00` | `#ECC481` | `#EBCB8B` | `#AD8301` | `#AD8301` | `#A06800` | `#D6BF55` |
| 4 blue | `#2F6FD0` | `#6CB6FF` | `#81A1C1` | `#205EA6` | `#205EA6` | `#2F6FD0` | `#5394EC` |
| 5 magenta | `#A63D8B` | `#D191E0` | `#B48EAD` | `#A02F6F` | `#A02F6F` | `#9C27B0` | `#AE8ABE` |
| 6 cyan | `#2A8F96` | `#5FC9D6` | `#88C0D0` | `#24837B` | `#24837B` | `#0F7C86` | `#299999` |
| 7 white | `#C9CCD2` | `#CCD2DE` | `#E5E9F0` | `#CECDC3` | `#CECDC3` | `#E5E5E5` | `#BCBEC4` |
| 8 bright black | `#6B7280` | `#6B727E` | `#4C566A` | `#575653` | `#878580` | `#7F7F7F` | `#8B8D91` |
| 9 bright red | `#B8352F` | `#F2969C` | `#BF616A` | `#D14D41` | `#D14D41` | `#E53935` | `#FF8785` |
| 10 bright green | `#3F6B28` | `#B8E2A3` | `#A3BE8C` | `#879A39` | `#879A39` | `#2EA043` | `#C0D94B` |
| 11 bright yellow | `#8A5D00` | `#F2D59A` | `#EBCB8B` | `#D0A215` | `#D0A215` | `#C28B00` | `#FFE15C` |
| 12 bright blue | `#1F5FC0` | `#8EC8FF` | `#81A1C1` | `#4385BE` | `#4385BE` | `#4F8CE0` | `#7EAEF1` |
| 13 bright magenta | `#8F2F79` | `#E0A9EC` | `#B48EAD` | `#CE5D97` | `#CE5D97` | `#B44CC4` | `#D1A2E0` |
| 14 bright cyan | `#17787E` | `#7FD8E3` | `#8FBCBB` | `#3AA99F` | `#3AA99F` | `#1F9AA5` | `#6CDADA` |
| 15 bright white | `#2B2F36` | `#F2F5FB` | `#ECEFF4` | `#FFFCF0` | `#FFFCF0` | `#FFFFFF` | `#FFFFFF` |
