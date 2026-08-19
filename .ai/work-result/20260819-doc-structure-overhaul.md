# 문서 구조 정비 — 파일명·기록 역할·Phase 필드·status 통합·규약 검사

---

- **작업일시** : 2026-08-19
- **작업자** : Claude Code (homepia123@gmail.com)
- **PR** : 없음(에이전트 권한 제약 — `.ai/issues/0001-pr-creation-permission.md`)
- **Phase** : 해당 없음

## 작업요청사항

"만들고 싶은 것을 리스트업하고 설계를 ADR에 남기고 있는데 구조적으로 어떤지" 검토 요청을
받았다. 검토 결과 다섯 가지 문제를 지적했고, 그에 대한 수정 제안을 만든 뒤 **제안대로 전부
진행**하라는 지시를 받았다. 기존 작업 결과 문서는 **삭제하고 새로 작성**하는 방향으로
정해졌다.

지적한 다섯 가지:

1. ADR 파일명이 한글 — ADR 0002가 브랜치명 한글을 배척한 근거와 어긋난다.
2. 작업 결과 문서가 PR 본문과 100% 중복이다.
3. `Phase`가 자유 텍스트라 기록 간 교차 추적이 안 된다.
4. CI가 링크만 검사하고 인덱스 등록 여부는 검사하지 않는다.
5. `.ai/status.md`가 같은 사실을 두 표로 관리해 갱신 지점이 둘이다.

## 변경 내용

**결정 기록 (신규 ADR 3건)**

- `.ai/adr/0003-ascii-doc-filenames.md`: `.ai/` 문서 파일명을 영문 소문자 슬러그로 통일.
- `.ai/adr/0004-work-result-vs-pr-body.md`: 작업 결과 문서와 PR 본문의 섹션별 소유자 분리.
- `.ai/adr/0005-phase-field-and-single-status-table.md`: `Phase` 머리말 필드, status 단일 표,
  규약의 CI 검사.

**파일명 (ADR 0003)**

- `.ai/adr/`: `0000-template.md`, `0001-phase-naming.md`, `0002-branch-naming-and-deletion.md`로 rename.
- `.ai/issues/0000-template.md`, `.ai/work-result/0000-template.md`로 rename.
- `.ai/adr/0001`·`0002` 머리말에 `Phase` 필드 소급 추가(머리말은 본문이 아니므로 불변 규칙에
  걸리지 않는다 — `.ai/README.md`에 예외를 명시).

**작업 결과 문서 (ADR 0004)**

- `.ai/work-result/0000-template.md`: `검증`·`체크리스트` 절 삭제, `PR`·`Phase` 필드 추가,
  `작업내용` → `변경 내용`(요약)으로 축소.
- `.ai/work-result/`의 기존 기록 4건 삭제, 인덱스 표 초기화 후 이 문서 1건 등록.
- `AGENTS.md` 9절·`.ai/README.md`·`CLAUDE.md`: PR 템플릿을 채워 쓰라는 지침을 역할 분리표로 교체.

**Phase 필드와 status (ADR 0005)**

- 세 템플릿 머리말에 `Phase` 필드 추가, 세 인덱스 표에 `Phase` 열 추가.
- `.ai/status.md`: "Phase 구성"과 "컴포넌트별 구현 현황"을 `구현 현황` 표 하나로 통합
  (`소분류 | 컴포넌트·기능 | 목표 | 상태 | 근거`), 상태 어휘 통일, `근거` 열 필수화.
- `AGENTS.md` 8·13·14절 개정.

**검사 (ADR 0005)**

- `.github/scripts/check_doc_index.py` 신규 — 파일명 규칙·번호 중복·인덱스 등록·`Phase` 필드·
  상태 어휘·인덱스와 머리말의 상태 일치를 검사한다(표준 라이브러리만 사용).
- `.github/workflows/docs-check.yml`: 새 워크플로 없이 step 추가, `paths` 필터를
  `.github/scripts/*.py`로 확장.
- `README.md`: 구성 트리·"문서 검사" 절·"설계 의도" 갱신.

## 최종정리내용

다섯 지적이 모두 반영됐고, 그중 셋(파일명·`Phase` 필드·인덱스 등록)은 문서상의 약속이 아니라
CI가 막는 조건이 됐다. 검사 두 개 모두 로컬에서 통과한다.

```text
문서 17개 검사 — 깨진 상대 링크 없음.
문서 인덱스·머리말 규약 이상 없음.
```

`check_doc_index.py`는 사본 저장소에서 위반 7종(미등록·한글 파일명·`Phase` 누락·`Phase` 형식
오류·상태 어휘 오타·상태 불일치·번호 중복)을 의도적으로 만들어 전부 잡히는 것을 확인했다.

후속 작업: 소유자가 PR을 열면 이 문서의 `PR` 필드를 그 번호로 교체한다.

## 참고사항

- **PR을 열지 못했다.** `POST /repos/.../pulls`가 404를 반환한다 — 같은 토큰으로 `git push`와
  `GET /repos/.../branches`는 성공하므로 저장소가 아니라 **Pull requests 권한**이 없는 것이다.
  두 번 시도해 같은 결과였고, `.ai/issues/0001-pr-creation-permission.md`로 남겼다.
  PR이 없어 `CLAUDE.md`의 PR 추적 불변 규칙(활동 구독 + 예약 확인)도 걸지 못했다.
- ADR 0003은 ADR 0002를 뒤집지 않고 그 근거를 파일명까지 확장한 것이라 `Superseded` 처리를
  하지 않았다.
- 앞선 검토에서 지적한 더 큰 구조 문제 두 가지 — **백로그 축 부재**(만들고 싶은 것을 담을
  자리가 규칙 파일·상태 문서 어디에도 맞지 않음)와 **living 설계 문서 부재**(진화하는 설계를
  불변 ADR에 넣는 모순) — 는 이번 범위에 포함되지 않았다.

## 제안사항

- `.ai/backlog.md`와 `.ai/design/`을 신설해 위 참고사항의 두 축을 채우는 것을 권한다.
  갱신 방식이 다른 문서(덮어쓰는 것 / 추가만 하는 것)를 한 파일에 섞지 않는다는 원칙에서
  나온 제안이다.
