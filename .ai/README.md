# .ai — AI 에이전트 공용 작업 메모리

이 폴더는 이 저장소에서 작업하는 **AI 에이전트(Claude Code, Codex)** 가 공유하는
상태·결정 기록·이슈·작업 결과다. 특정 도구에 종속되지 않으며, 개발 과정의 기록을 남기는
내부 작업 공간이다(저장소에서만 본다).

> 진입 규칙은 항상 [`AGENTS.md`](../AGENTS.md)가 단일 출처다. 이 폴더는 거기서 가리킨다.

## 구조

문서를 나누는 축은 주제가 아니라 **어떻게 갱신되는가**다(ADR 0006). 덮어쓰는 문서와 추가만
하는 문서를 한 파일에 섞지 않는다.

| 질문 | 문서 | 갱신 |
|---|---|---|
| 규칙이 뭔가 | [`../AGENTS.md`](../AGENTS.md) | 덮어씀 |
| 만들고 싶은 게 뭔가 | [`backlog.md`](./backlog.md) | 덮어씀 |
| 지금 어디까지 왔나 | [`status.md`](./status.md) | 덮어씀 |
| 지금 어떤 모습인가 | [`design/`](./design/) | 덮어씀 |
| 왜 그렇게 정했나 | [`adr/`](./adr/) | **추가만** |
| 왜 아직 안 됐나 | [`issues/`](./issues/) | 상태만 갱신 |
| 무엇을 했나 | [`work-result/`](./work-result/) | **추가만** |

- [`status.md`](./status.md) — **구현 현황(상태의 단일 출처).** 지금 어느 Phase이고 무엇이
  구현되었는지. 이 문서의 구현 현황 표가 곧 **범위**다(ADR 0007). 다른 문서는 상태를 자체 서술하지 않고 이 문서를 인용한다.
  Phase 표기 규칙(`A`, `A-1`)은 [`AGENTS.md`](../AGENTS.md) 14절이 정한다.
- [`backlog.md`](./backlog.md) — **만들고 싶은 것.** 아직 범위가 아니고 지금 할 일도 아닌
  아이디어를 모아 둔다. 채택되면 `status.md`의 구현 현황 표에 `🚧 시작 전`으로 옮기고
  백로그에서 지운다(ADR 0006·0007).
- [`design/`](./design/) — **지금의 설계.** 컴포넌트 1개 = 파일 1개. 현재 모습만 담고
  덮어쓴다. "왜 그렇게 정했는가"는 담지 않고 `adr/`을 링크한다(ADR 0006).
  미리 만들지 않고, 컴포넌트가 실제로 생겼을 때 만든다.
- [`adr/`](./adr/) — **Architecture Decision Records.** 결정 1건 = 파일 1개
  (`NNNN-slug.md`). 왜 그렇게 정했는지 배경·결정·결과를 남긴다. 인덱스는
  [`adr/README.md`](./adr/README.md).
- [`issues/`](./issues/) — 미해결이거나 의도적으로 미룬 **오픈 이슈**. 인덱스는
  [`issues/README.md`](./issues/README.md).
- [`work-result/`](./work-result/) — **작업 결과 문서.** 작업 1건 = 파일 1개
  (`yyyymmdd-slug.md`). 무엇을 요청받아 무엇을 바꿨는지 남긴다(`AGENTS.md` 9절).
  목적·검증 등 PR 본문과 겹치는 내용은 담지 않는다(ADR 0004).
  인덱스는 [`work-result/README.md`](./work-result/README.md).

그 밖의 문서(인터페이스 계약 등)가 필요해지면 이 폴더 아래에 두고 이 목록에 등록한다.
미리 만들어 두지 않는다.

## 새 결정(ADR) 추가하는 법

1. `adr/`의 다음 번호로 `NNNN-slug.md`를 만든다(마지막 번호 +1, 4자리 zero-pad).
   슬러그는 **영문 소문자·숫자·하이픈**만 쓴다(ADR 0003 — 브랜치명과 같은 이유).
   한글 제목은 파일 안의 H1과 인덱스 표의 링크 텍스트가 담는다.
2. [`adr/0000-template.md`](./adr/0000-template.md) 형식을 따른다.

   ```markdown
   # 0001. 제목

   - 상태: Accepted
   - 날짜: YYYY-MM-DD
   - Phase: A-2
   - 관련: PR #NN, `adr/0000-...`

   ## 배경
   왜 이 결정이 필요했는가.

   ## 결정
   무엇을 정했는가.

   ## 결과
   그로 인한 영향/트레이드오프, 후속 작업.
   ```

3. `adr/README.md` 인덱스 표에 한 줄 추가한다(`Phase` 열 포함).
4. 기존 결정을 뒤집으면, 옛 ADR의 상태를 `Superseded by NNNN`으로 바꾸고 새 ADR에서 링크한다.
   **과거 ADR 본문은 고쳐 쓰지 않는다**(그 시점의 기록으로 보존). 머리말 필드(`상태`,
   `Phase`)와 파일명은 본문이 아니므로 규약이 바뀌면 맞춰 고친다.

## 머리말 `Phase` 필드

ADR·이슈·작업 결과는 머리말에 `Phase` 필드를 둔다. 값은 소분류 표기(`A-2`) 또는 Phase
표기(`A`)이고, 특정 Phase에 속하지 않으면 **`해당 없음`** 으로 적는다 — 비워두지 않는다.
표기 규칙은 [`AGENTS.md`](../AGENTS.md) 14절이 단일 출처다.

이 필드 덕분에 한 소분류에 얽힌 결정·이슈·작업을 한 번에 모을 수 있다.

```bash
grep -l "Phase.*A-2" .ai/adr/*.md .ai/issues/*.md .ai/work-result/*.md
```

## 상태(status) 어휘

- `Accepted` — 확정되어 적용됨
- `Proposed` — 제안됨/미확정
- `Superseded by NNNN` — 후속 결정으로 대체됨
- `Deprecated` — 더 이상 유효하지 않음

## 이슈 관리

- 새 이슈는 `issues/`에 `NNNN-slug.md`로 추가하고 `issues/README.md`에 등록한다.
- 해결되면 상태를 `Resolved`로 바꾸고(관련 ADR/PR 링크), 완전히 무의미해지면 항목을 제거한다.
- 이슈 상태 어휘(단일 출처, `issues/README.md`는 여기를 가리킨다):
  - `Open` — 미해결
  - `Deferred(사유)` — 의도적으로 미룸. 사유를 괄호에 적는다(예: `Deferred(환경 제약)`).
  - `Resolved` — 해결됨. 날짜와 관련 PR/ADR을 함께 남긴다.

## 작업 결과 문서 남기는 법

1. 작업이 끝나면 [`work-result/0000-template.md`](./work-result/0000-template.md)를
   복사해 같은 폴더에 `yyyymmdd-slug.md`로 만든다.
2. **PR 본문과 중복해서 쓰지 않는다**(ADR 0004). 목적·배경·검증·체크리스트는 PR이 담고,
   이 문서는 작업요청사항·변경 요약·최종정리내용·참고사항·제안사항을 담는다. 머리말
   `PR` 필드로 PR을 가리키고, PR 없이 직접 push한 작업이면 그 사유와 함께 근거까지 적는다.
3. `work-result/README.md` 인덱스 표에 한 줄 추가한다(`Phase` 열 포함).

## 인덱스 정합성 검사

위 규약(파일명·인덱스 등록·`Phase` 필드·상태 어휘·인덱스와 파일의 상태 일치)은
`.github/scripts/check_doc_index.py`가 CI에서 확인한다(ADR 0005). 로컬에서도 같은 명령으로
먼저 돌린다.

```bash
python3 .github/scripts/check_markdown_links.py
python3 .github/scripts/check_doc_index.py
```
