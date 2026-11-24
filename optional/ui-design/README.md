# 선택 항목 — ui-design 스킬

데스크톱 앱(Windows·macOS)과 웹앱이 함께 쓰는 테마·시맨틱 컬러 토큰·플랫폼별 적용 규칙을 담은
공용 스킬이다. **UI가 없는 프로젝트가 늘 들고 다니지 않도록 기본 세트에서 뺐다.** UI를 만드는
프로젝트만 아래 순서로 넣는다.

이 폴더는 저장소 루트와 같은 배치로 되어 있다 — `.agents/`와 `.claude/`를 그대로 루트에 옮기면
스킬 본문과 Claude Code 진입점이 제자리에 놓이고 상대 링크도 그대로 맞는다.

## 넣는 법

1. 스킬 두 곳을 루트로 복사한다.

   ```bash
   mkdir -p .agents/skills .claude/skills
   cp -R optional/ui-design/.agents/skills/ui-design .agents/skills/
   cp -R optional/ui-design/.claude/skills/ui-design .claude/skills/
   ```

   ```powershell
   New-Item -ItemType Directory -Force .agents/skills, .claude/skills | Out-Null
   Copy-Item -Recurse optional/ui-design/.agents/skills/ui-design .agents/skills/
   Copy-Item -Recurse optional/ui-design/.claude/skills/ui-design .claude/skills/
   ```

2. `.github/workflows/checks.yml`의 `파일 크기 규칙 확인` step 뒤에 생성물·대비 검사 step을
   더한다. 워크플로를 새로 만들지 않고 기존 job에 step으로 넣는다(`AGENTS.md` 9절).

   ```yaml
         - name: UI 토큰 생성물·대비 확인
           if: ${{ !cancelled() }}
           run: python3 .agents/skills/ui-design/scripts/build_tokens.py --check
   ```

3. 로컬에서 한 번 돌려 통과하는지 확인한다. Windows는 `python3` 대신 `py` 또는 `python`으로
   실행한다.

   ```bash
   python3 .agents/skills/ui-design/scripts/build_tokens.py --check
   ```

4. 넣었든 넣지 않았든 도입이 끝나면 `optional/` 폴더를 지운다 — 원본은 템플릿 저장소에 남아
   있다.

## 고치는 법

테마 원본은 `themes.json` 하나이고, 나머지는 `scripts/build_tokens.py`가 만드는 생성물이다.
자세한 규칙은 [스킬 본문](./.agents/skills/ui-design/SKILL.md)이 정한다. 템플릿 저장소에서
스킬을 고쳤다면 이 폴더 안에서 `build_tokens.py --check`를 돌려 생성물이 최신인지 확인한다.
