# ADR 인덱스

아키텍처 결정 기록(Architecture Decision Record). 결정 1건 = 파일 1개.
새 결정은 다음 번호로 `NNNN-slug.md`를 추가하고 이 표에 한 줄 넣는다(슬러그는 영문
소문자·숫자·하이픈만 — ADR 0003).
작성 규약은 [`../README.md`](../README.md), 형식은 [`0000-template.md`](./0000-template.md) 참고.

| # | 날짜 | Phase | 제목 | 상태 |
|---|---|---|---|---|
| [0001](./0001-phase-naming.md) | 2026-08-19 | 해당 없음 | Phase는 대문자 한 글자, 소분류는 `A-1`까지만 나눈다 | Accepted |
| [0002](./0002-branch-naming-and-deletion.md) | 2026-08-19 | 해당 없음 | 브랜치명은 영문으로 쓰고, 재명명하지 않으며, 원격 삭제는 소유자가 한다 | Accepted |
| [0003](./0003-ascii-doc-filenames.md) | 2026-08-19 | 해당 없음 | `.ai/` 문서 파일명은 영문 소문자 슬러그로 쓴다 | Accepted |
| [0004](./0004-work-result-vs-pr-body.md) | 2026-08-19 | 해당 없음 | 작업 결과 문서와 PR 본문은 역할을 나누고, 같은 내용을 두 번 쓰지 않는다 | Accepted |
| [0005](./0005-phase-field-and-single-status-table.md) | 2026-08-19 | 해당 없음 | Phase는 머리말 필드로 적고, status는 표 하나로 유지하며, 규약은 CI가 검사한다 | Accepted |
| [0006](./0006-backlog-and-living-design-docs.md) | 2026-08-19 | 해당 없음 | 만들고 싶은 것은 백로그에, 현재 설계는 덮어쓰는 문서에 둔다 | Accepted |
| [0007](./0007-agents-md-holds-rules-only.md) | 2026-08-19 | 해당 없음 | `AGENTS.md`는 규칙만 담는다 — 범위·계약·프로젝트 소개는 각자의 문서로 | Accepted |

표의 `상태`는 각 파일 머리말의 `상태`와 같아야 한다 — CI가 확인한다(ADR 0005).
