# ADR 인덱스

아키텍처 결정 기록(Architecture Decision Record). 결정 1건 = 파일 1개.

아직 등록된 결정이 없다. 첫 결정을 `0001-slug.md`로 만들고 아래 표에 한 줄 추가한다.
작성 규약은 [`../README.md`](../README.md), 형식은 [`0000-template.md`](./0000-template.md).

| # | 날짜 | Phase | 제목 | 상태 |
|---|---|---|---|---|
| — | — | — | (없음) | — |

기입 예시(실제 파일이 생기면 이 형식으로 바꾼다):

```markdown
| [0001](./0001-storage-adapter.md) | 2026-07-31 | A-2 | 저장소는 어댑터 뒤에 둔다 | Accepted |
```

### 상태 범례

| 값 | 뜻 |
|---|---|
| `Accepted` | 확정되어 적용됨 |
| `Proposed` | 제안됨, 미확정 |
| `Superseded by NNNN` | 후속 결정으로 대체됨 (대체한 ADR 번호를 붙인다) |
| `Deprecated` | 대체 없이 폐기됨 |

**값은 이 넷뿐이고 영어로 쓴다.** 각 값의 뜻과 쓰는 때는 [`../README.md`](../README.md)의
상태 어휘 표가 단일 출처다. 위 표의 `상태`는 각 파일 머리말의 `상태`와 같아야 하며,
CI가 확인한다.
