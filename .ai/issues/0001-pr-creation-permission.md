# 에이전트가 PR을 생성할 수 없다 (pulls API 404)

- 상태: Deferred(환경 제약)
- Phase: 해당 없음
- 관련: `AGENTS.md` 9절, `CLAUDE.md` "PR 추적을 실제로 수행하는 방법", `.ai/work-result/20260819-doc-structure-overhaul.md`

`AGENTS.md` 9절은 "브랜치를 만들어 작업한 변경은 반드시 Pull Request로 올리고, PR 리뷰를
받은 뒤 머지한다"고 정하지만, Claude Code 세션에 연결된 GitHub 앱 설치본에 이 저장소의
**Pull requests 권한이 없어** 에이전트가 PR을 만들 수 없다.

- `POST /repos/ChoccoJang/ai-project-template/pulls` → `404 Not Found`
- `GET /repos/.../pulls` → `404 Not Found` (읽기도 막힌다)
- 같은 토큰으로 `GET /user`, `GET /repos/.../branches`, `git push`는 모두 성공한다.
  즉 저장소 자체는 보이고 쓸 수 있으며, **pulls 엔드포인트만** 막혀 있다.

따라서 404는 "저장소가 없다"가 아니라 "PR 권한이 없다"는 뜻이다. 재시도해도 같다.

영향:

- 에이전트가 브랜치를 푸시한 뒤 PR을 열지 못해, 소유자가 직접 열어야 한다.
- PR이 없으므로 `CLAUDE.md`의 PR 추적 불변 규칙(활동 구독 + 예약 확인)도 걸 수 없다.
- 작업 결과 문서의 `PR` 필드가 비게 된다(ADR 0004).

## 해결 방향

소유자가 GitHub 앱 설치 설정에서 이 저장소에 **Pull requests: Read and write** 권한을
부여하면 해소된다(claude.ai Settings → Connectors, 또는 조직 설정의 Claude GitHub 설정).
권한은 소유자만 바꿀 수 있어 에이전트 쪽에서 할 수 있는 일이 없으므로 `Deferred(환경 제약)`
로 둔다.

권한이 부여될 때까지는 소유자가 compare 링크로 PR을 열고, 그 번호를 해당 작업 결과 문서의
`PR` 필드에 적는다.
