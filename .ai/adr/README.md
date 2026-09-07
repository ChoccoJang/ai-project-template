# ADR 인덱스

아키텍처 결정 기록(Architecture Decision Record). 결정 1건 = 파일 1개.

새 결정은 다음 번호로 `NNNN-slug.md`를 만들고 아래 표에 한 줄 추가한다.
작성 규약은 [`../README.md`](../README.md), 형식은 [`0000-template.md`](./0000-template.md).

| # | 날짜 | Phase | 제목 | 상태 |
|---|---|---|---|---|
| [0001](./0001-work-result-after-pr.md) | 2026-09-07 | 해당 없음 | 작업 결과 문서는 PR을 연 뒤에 링크를 채운 채로 만든다 | Accepted |

### 상태 범례

`Accepted` · `Proposed` · `Superseded by NNNN` · `Deprecated` — **이 넷뿐이다.**

각 값의 뜻과 쓰는 때는 [`../README.md`](../README.md)의 상태 어휘 표가 단일 출처다(여기에
중복하지 않는다). 위 표의 `상태`는 각 파일 머리말의 `상태`와 같아야 하며, CI가 확인한다.