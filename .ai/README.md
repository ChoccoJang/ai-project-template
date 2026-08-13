# .ai — AI 에이전트 공용 작업 메모리

이 폴더는 이 저장소에서 작업하는 **모든 AI 에이전트**(Claude Code, Codex, Cursor 등)가
공유하는 설계·결정 기록과 이슈 트래커다. 특정 도구에 종속되지 않으며, 개발 과정의 설계·결정·이슈를
남기는 내부 작업 공간이다.

> 진입 규칙은 항상 [`AGENTS.md`](../AGENTS.md)가 단일 출처다. 이 폴더는 거기서 가리킨다.

## 구조

- [`docs/`](./docs/) — **개발용 설계·현황 문서.** 컴포넌트 상세 설계, 구현 현황(`00-status`),
  API 계약 등. 저장소에서만 본다. 인덱스는 [`docs/README.md`](./docs/README.md).
- [`adr/`](./adr/) — **Architecture Decision Records.** 결정 1건 = 파일 1개
  (`NNNN-슬러그.md`). 왜 그렇게 정했는지 배경·결정·결과를 남긴다. 인덱스는
  [`adr/README.md`](./adr/README.md).
- [`issues/`](./issues/) — 미해결이거나 의도적으로 미룬 **오픈 이슈**. 인덱스는
  [`issues/README.md`](./issues/README.md).

## 새 결정(ADR) 추가하는 법

1. `adr/`의 다음 번호로 `NNNN-슬러그.md`를 만든다(마지막 번호 +1, 4자리 zero-pad).
   슬러그는 제목을 한글 그대로 쓰되 공백은 하이픈(`-`)으로 바꾼다.
2. [`adr/0000-adr-템플릿.md`](./adr/0000-adr-템플릿.md) 형식을 따른다.

   ```markdown
   # 0001. 제목

   - 상태: Accepted
   - 날짜: YYYY-MM-DD
   - 관련: PR #NN, `adr/0000-...`

   ## 배경
   왜 이 결정이 필요했는가.

   ## 결정
   무엇을 정했는가.

   ## 결과
   그로 인한 영향/트레이드오프, 후속 작업.
   ```

3. `adr/README.md` 인덱스 표에 한 줄 추가한다.
4. 기존 결정을 뒤집으면, 옛 ADR의 상태를 `Superseded by NNNN`으로 바꾸고 새 ADR에서 링크한다.
   **과거 ADR 본문은 고쳐 쓰지 않는다**(그 시점의 기록으로 보존).

## 상태(status) 어휘

- `Accepted` — 확정되어 적용됨
- `Proposed` — 제안됨/미확정
- `Superseded by NNNN` — 후속 결정으로 대체됨
- `Deprecated` — 더 이상 유효하지 않음

## 이슈 관리

- 새 이슈는 `issues/`에 `NNNN-슬러그.md`로 추가하고 `issues/README.md`에 등록한다.
- 해결되면 상태를 `Resolved`로 바꾸고(관련 ADR/PR 링크), 완전히 무의미해지면 항목을 제거한다.
- 이슈 상태 어휘: `Open` · `Deferred`(의도적으로 미룸) · `Resolved` · `환경 제약`.
