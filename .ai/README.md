# .ai — AI 에이전트 공용 작업 메모리

이 폴더는 이 저장소에서 작업하는 **AI 에이전트(Claude Code, Codex)** 가 공유하는
상태·결정 기록·이슈·작업 결과다. 특정 도구에 종속되지 않으며, 개발 과정의 기록을 남기는
내부 작업 공간이다(저장소에서만 본다).

> 진입 규칙은 항상 [`AGENTS.md`](../AGENTS.md)가 단일 출처다. 이 폴더는 거기서 가리킨다.

## 구조

- [`status.md`](./status.md) — **구현 현황(상태의 단일 출처).** 지금 어느 Phase이고 무엇이
  구현되었는지. 다른 문서는 상태를 자체 서술하지 않고 이 문서를 인용한다.
  Phase 표기 규칙(`A`, `A-1`)은 [`AGENTS.md`](../AGENTS.md) 14절이 정한다.
- [`adr/`](./adr/) — **Architecture Decision Records.** 결정 1건 = 파일 1개
  (`NNNN-슬러그.md`). 왜 그렇게 정했는지 배경·결정·결과를 남긴다. 인덱스는
  [`adr/README.md`](./adr/README.md).
- [`issues/`](./issues/) — 미해결이거나 의도적으로 미룬 **오픈 이슈**. 인덱스는
  [`issues/README.md`](./issues/README.md).
- [`work-result/`](./work-result/) — **작업 결과 문서.** 작업 1건 = 파일 1개
  (`yyyymmdd-작업명.md`). 무엇을 요청받아 무엇을 바꿨는지 남긴다(`AGENTS.md` 9절).
  인덱스는 [`work-result/README.md`](./work-result/README.md).

그 밖의 문서(설계 노트, 인터페이스 계약 등)가 필요해지면 이 폴더 아래에 두고 이 목록에
등록한다. 미리 만들어 두지 않는다.

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
- 이슈 상태 어휘(단일 출처, `issues/README.md`는 여기를 가리킨다):
  - `Open` — 미해결
  - `Deferred(사유)` — 의도적으로 미룸. 사유를 괄호에 적는다(예: `Deferred(환경 제약)`).
  - `Resolved` — 해결됨. 날짜와 관련 PR/ADR을 함께 남긴다.

## 작업 결과 문서 남기는 법

1. 작업이 끝나면 [`work-result/0000-작업결과-템플릿.md`](./work-result/0000-작업결과-템플릿.md)를
   복사해 같은 폴더에 `yyyymmdd-작업명.md`로 만든다.
2. 본문(작업내용/최종정리내용)은 `.github/pull_request_template.md`의 각 섹션을 채워서 쓴다.
3. `work-result/README.md` 인덱스 표에 한 줄 추가한다.
