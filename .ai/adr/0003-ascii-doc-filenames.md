# 0003. `.ai/` 문서 파일명은 영문 소문자 슬러그로 쓴다

- 상태: Accepted
- 날짜: 2026-08-19
- Phase: 해당 없음
- 관련: `.ai/adr/0002-branch-naming-and-deletion.md`, `.ai/README.md`

## 배경

ADR 0002는 브랜치명에서 한글을 배척했다. 근거는 인코딩이었다 — 터미널·git 출력에서
`\353\252\205` 형태로 보이고 URL·CI 설정에서 다루기 번거롭다는 것이다.

그런데 같은 문제가 `.ai/` 문서 **파일명**에 그대로 남아 있었다. ADR·이슈·작업 결과 문서의
슬러그를 한글로 쓰도록 `.ai/README.md`가 정하고 있었기 때문이다. 실제 출력:

```text
$ git show --stat 714f329
 ...52\205\353\252\205-\352\267\234\354\271\231.md" | 50 ++++++
```

파일명이 어디서 문제가 되는가:

- `git show --stat`, `git log --name-only`, `git status`가 파일명을 octal escape로 출력한다
  (`core.quotepath` 기본값). 어떤 파일이 바뀌었는지 눈으로 못 읽는다.
- 셸에서 경로를 따옴표 없이 다루기 어렵고, 자동완성·`grep -r` 결과가 깨져 보인다.
- GitHub 링크는 퍼센트 인코딩(`%ED%8E%98...`)이 되어 사람이 읽을 수 없는 URL이 된다.

검토했으나 채택하지 않은 대안:

- **`core.quotepath=false` 설정으로 해결** — 로컬 설정이라 저장소가 강제할 수 없고, CI·GitHub
  UI·URL 문제는 그대로 남는다.
- **신규 파일부터만 적용** — 검사 스크립트에 예외 목록이 필요해지고, 두 규칙이 공존하는
  기간이 무한정 길어진다.

## 결정

### 1. 파일명은 ASCII 슬러그, 제목은 한글

- `.ai/adr/`·`.ai/issues/`: `NNNN-slug.md` (4자리 zero-pad)
- `.ai/work-result/`: `yyyymmdd-slug.md`
- 슬러그는 **영문 소문자·숫자·하이픈**만 쓴다. 한글·공백·대문자·밑줄을 쓰지 않는다.
- **한글 제목은 파일 안의 H1이 담는다.** 인덱스 표의 링크 텍스트도 한글 제목을 쓰므로,
  사람이 목록에서 찾는 경험은 그대로다.
- 각 폴더의 템플릿 파일명은 `0000-template.md`로 통일한다.

### 2. 기존 파일도 함께 옮긴다

- 예외 목록 없이 전부 rename한다. 파일명은 ADR 본문이 아니므로 "과거 ADR 본문은 고쳐 쓰지
  않는다"(`.ai/README.md`)에 걸리지 않는다.

### 3. 검사로 강제한다

- 파일명 규칙 위반은 `.github/scripts/check_doc_index.py`가 CI에서 잡는다(ADR 0005 · `AGENTS.md` 13절).

## 결과

- `git log --name-only`·`git status`에서 어떤 문서가 바뀌었는지 그대로 읽힌다.
- 문서 경로를 셸·스크립트·GitHub URL에서 인용부호 없이 다룰 수 있다.
- 트레이드오프: 파일 트리만 봤을 때 한글 제목만큼 즉시 내용이 읽히지 않는다. 인덱스 표
  (`README.md`)가 한글 제목을 유지하므로 그쪽을 진입점으로 삼는다.
- ADR 0002의 근거를 저장소 전체에 일관되게 적용한 것이지 그 결정을 뒤집지 않는다.

## 영향 파일

- `.ai/adr/`: `0000-template.md`, `0001-phase-naming.md`, `0002-branch-naming-and-deletion.md`로 rename.
- `.ai/issues/0000-template.md`, `.ai/work-result/0000-template.md`로 rename.
- `.ai/README.md`: 슬러그 규칙을 영문으로 교체.
- `.ai/adr/README.md`, `.ai/issues/README.md`, `.ai/work-result/README.md`: 링크·예시 갱신.
- `AGENTS.md` 8절, `README.md` 구성 트리: 템플릿 경로 갱신.
