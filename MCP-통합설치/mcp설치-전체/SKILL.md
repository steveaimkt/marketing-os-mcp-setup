---
name: mcp설치-전체
description: |
  marketing-os 의 12개 MCP 를 강의 순서대로 순차 설치하는 마스터 스킬 (11 스텝 = Step 7 영상 3개·Step 9 광고 2개 묶음). 사용자는 키 발급·OAuth 클릭만, Claude 가 .env 등록 + 헬스체크 + 진행률 추적. 호출 즉시 모드(A 실제설치 / B 교육시연 / C 점검)부터 질문.

  자동 호출 트리거:
  - "MCP 전체 설치하자" ⭐ / "MCP 12개 한 번에 설치" / "marketing-os 전체 환경 셋업" / "모든 MCP 셋업"
  - "MCP 설치 전 과정 보여줘" ⭐ (→ B 교육 시연) / "MCP 설치 시연" / "다 깔려 있는데 설치 과정 설명해줘"

  11 스텝 (✋사용자 · 🤖자동):
  ✋1 Google Sheets (10분·OAuth·1-2) / ✋2 GA4 (15분·서비스계정·1-3) / ✋3 Firecrawl (2분·API키·1-4)
  ✋4 Figma (5분·TalkToFigma·2-1) / ✋5 YouTube (5분·API키·2-2) / ✋6 Higgsfield (1분·커넥터·2-3)
  ✋7 영상 트리오 (15분·Hyperframes+HeyGen+ElevenLabs·2-4) / ✋8 Buffer (5분·토큰·3-1)
  ✋9 Meta+Google Ads (6분+승인대기·3-2) / ✋10 Notion (1분·커넥터·4-1) / ✋11 Discord (10분·봇토큰·4-2)

  중단해도 재호출 시 마지막 위치부터 재개.
---

# /mcp설치-전체 · 마스터 설치 스킬

12개 MCP 를 강의 순서대로 순차 설치. 사용자는 키 발급/클릭만, Claude 가 등록·검증·추적.

## 핵심 원칙 (작업 전 필독)
- **검증된 설정 우선**: 현재 프로젝트의 `.mcp.json`/`.env` 실제 구성을 따른다. 기억·추측 금지.
- **비파괴**: 기존 키·인증을 덮어쓰지 않는다. 읽기전용 검증 명령만 실행.
- **기준 경로**: 모든 경로는 `${CLAUDE_PROJECT_DIR}` (= Claude Code 를 실행한 프로젝트 루트) 기준. `.env`·`.mcp.json`·`claude mcp list` 전부 여기. **절대경로 하드코딩 금지** — 사용자가 클론한 위치는 사람마다 다르다.
  ```bash
  echo "$CLAUDE_PROJECT_DIR"          # 비어 있으면 pwd 사용
  PRJ="${CLAUDE_PROJECT_DIR:-$(pwd)}"
  ```

---

## 0단계 · 모드 선택 (호출 즉시 첫 질문)

```
🚀 marketing-os MCP 통합 설치. 진행 모드를 골라주세요.
  A. 실제 설치 — 미설치 MCP 만 설치, 완료분 자동 스킵 (첫 셋업용)
  B. 교육 시연 — 12개를 1개씩 전 과정 설명·검증, 이미 깔려도 스킵 안 함, 비파괴 (강의·복습용)
  C. 점검만 — 현재 상태 표 출력 후 종료
어떤 모드? (A / B / C)
```

- **A** → `## 사전 점검` → 완료 스텝 스킵 → 미완료만 안내
- **B** → `## B 교육 시연 규칙` (스킵 금지)
- **C** → `## 헬스 체크` 만 실행 후 종료
- "전체 과정 보여줘/시연/복습/녹화" 로 호출 시 → 질문 없이 B 로 진입 가능

---

## B 교육 시연 규칙

이미 다 설치된 PC 에서도 설치 전 과정을 보여준다 (강의 녹화용).

1. **스킵 금지** — `.env` 에 키 있어도, Connected 여도 12개 전부 1개씩.
2. **비파괴** — 변경 명령(`.env` 수정·`mv`·`install`)은 코드블록으로 *보여주기만*. 실제 실행은 읽기전용 검증뿐.
3. **4토막 고정 포맷**: ① 무엇·왜 / ② 발급 절차(설치 안 한 사람이 따라할 수 있게) / ③ 설치 방법(정확한 명령) / ④ 작동 증명(읽기전용 헬스체크 1개 → "이미 작동 중" 확인).
4. **상태 숨기지 않기** — ④ 에서 Connected 면 "이미 됨 ✅", 아니면 "③ 을 실행하면 됨".

### 인터랙티브 게이트 (강의 기본값)
- **한 MCP = 한 게이트**. 1→12 순서. 한 개 끝나면 멈추고 "다음" 받은 뒤 진행. 몰아 출력 금지.
- ② 발급은 **한 클릭씩** 공개 + 실제 URL 링크.
- ③ 설치 명령은 **직접 실행** (보여주기만 ✗). 단 기존 키는 절대 덮어쓰지 않음 — 검증용 실명령(`set -a; source .env` 후 헬스체크)으로.

④ 읽기전용 헬스체크 예: Sheets=시트목록 / GA4=7일 활성사용자 / Firecrawl=example.com 1p / Figma=get_document_info / YouTube=영상검색 / Higgsfield=크레딧 / 영상=hyperframes --version·elevenlabs 모델 / Buffer=채널목록 / Meta=계정목록 / Google Ads=list_accessible_customers / Notion=검색 / Discord=`claude mcp list | grep discord`. (쓰기 도구는 시연 금지)

---

## 사전 점검 (A·B·C 공통 · 30초)

```bash
PRJ="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# ⛔ 게이트 0 — Node.js (없으면 npx 기반 MCP 6개가 전부 실패)
node --version && npm --version || echo "⛔ Node.js 미설치 → 아래 '게이트 0' 처리"

test -f "$PRJ/.mcp.json" || echo "⚠ .mcp.json 없음 → 설치 진행하며 생성"
node --version | grep -E "v(2[2-9]|[3-9][0-9])\." || echo "⚠ Node 22+ 권장 (Hyperframes)"
which uv ffmpeg bun || echo "⚠ 누락 도구 설치 필요"
test -f "$PRJ/.env" || cp "$PRJ/.env.example" "$PRJ/.env"
claude mcp list 2>&1 | grep -E "Figma|Notion|Higgsfield"   # 커넥터 현황
```
→ 완료 스텝 자동 스킵, 미완료만 안내.

### ⛔ 게이트 0 · Node.js (통과해야 Step 1 진행)

`node --version` 이 `command not found` 면 **여기서 멈추고** 설치를 안내한다. 진행해도 Firecrawl·네이버·YouTube·Buffer·GA4·Ads 가 전부 `failed to connect` 로 끝난다.

```
Node.js 가 필요합니다 (약 3분).

  macOS   → https://nodejs.org → 왼쪽 LTS 버튼 → .pkg 다운로드 → 더블클릭 설치
  Windows → https://nodejs.org → LTS 버튼 → .msi 다운로드 → 실행
            (설치 중 "Add to PATH" 체크 확인 · 기본값으로 체크되어 있음)

설치 후 ⚠️ 터미널을 완전히 종료했다가 다시 열어주세요.
```

⚠️ **Claude Code 가 돌아간다 ≠ Node 설치됨.** 네이티브 설치 스크립트로 Claude Code 를 깔았으면 Node 없이도 작동한다. 커넥터 3종(Figma·Notion·Higgsfield)만 연결되고 나머지가 전부 실패하면 Node 문제로 확정.

상세: [00-Node설치.md](../../00-Node설치.md)

---

## 11 스텝

각 스텝 헤더: `[N/11] 이름 · 인증방식 · [클립]`. A 모드는 발급 안내 후 키 입력받아 자동 처리, B 모드는 4토막.

### ✋1 Google Sheets · OAuth(자체호스팅) · 1-2
- 발급: console.cloud.google.com → Sheets API 사용 → OAuth 동의화면(⚠️ 테스트 사용자에 본인 추가) → OAuth 클라이언트 ID **데스크톱 앱** → JSON 다운 → `oauth_credentials.json` 으로 변경
- 설치: `mv ~/Downloads/oauth_credentials.json mcp-server/` + `cd mcp-server && npm install`. 검증 `grep '"installed"'` (데스크톱앱이면 정상). 최초 1회 브라우저 OAuth.
- ④ 서버 부팅 → 10개 도구 응답 (get_spreadsheet_info 등)

### ✋2 GA4 · 서비스계정 / ADC · 1-3
- 발급: GA4 Data API 사용 → 서비스계정 생성 → 키(JSON) → GA4 속성 액세스에 client_email 뷰어 추가 → 속성 ID(9자리)
- 설치: JSON → `~/.config/gcp/`, `.env` 에 `GA4_SERVICE_ACCOUNT_JSON`·`GA4_PROPERTY_ID`, `.mcp.json` 의 `GA_PROPERTY_ID` 평문 교체. 서버 `npx -y mcp-server-ga4`.
- ⚠️ **Workspace(wmbb.kr) 는 서비스계정 키 발급 차단 → ADC 경로**. GA4·Google Ads 가 ADC 공유 → 스코프 3개 한 번에 (안 그러면 한쪽 403):
  ```bash
  gcloud auth application-default login \
    --client-id-file="$HOME/Downloads/oauth_credentials.json" \
    --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/adwords,https://www.googleapis.com/auth/cloud-platform
  ```
  기본 gcloud 클라이언트는 "차단된 앱"으로 막힘 → 본인 데스크톱 클라이언트(`--client-id-file`) 필수. 재로그인 후 재시작.
- ④ 7일 활성 사용자 실데이터

### ✋3 Firecrawl · API키 · 1-4
- 발급: firecrawl.dev/app/api-keys → Create (fc-xxx)
- 설치: `.env` `FIRECRAWL_API_KEY`. 서버 `npx -y firecrawl-mcp`.
- ④ example.com 1페이지 실제 스크랩

### ✋4 Figma · TalkToFigma(WebSocket+플러그인) · 2-1
> ⚠️ Claude.ai 커넥터 아님. 본체는 `cursor-talk-to-figma-mcp` 사용 (rate limit 없음·디자인 생성 가능). 구조: Claude ↔ MCP ↔ WS(:3055) ↔ Figma **데스크톱** 플러그인. 웹 Figma 불가.
- 설치: ① 서버 `cd ~/dev/cursor-talk-to-figma-mcp && bun socket` (켜둠, "port 3055" 확인. ⚠️ `bunx ... --server` 는 클라이언트라 안 됨) ② Figma Community "Cursor Talk to Figma MCP Plugin" 실행 → Connect → 채널 ID ③ "talk to figma 채널 <ID> join"
- ④ get_document_info 가 실제 프레임 반환

### ✋5 YouTube Data · API키(+OAuth) · 2-2
- 발급: console → YouTube Data API v3 사용 → API 키(AIza…). 본인 채널 Analytics 까지면 OAuth 4종 추가.
- 설치: `.env` `YOUTUBE_API_KEY`. 서버 `npx -y youtube-data-mcp-server`.
- ④ 영상 검색 (searchVideos)

### ✋6 Higgsfield · Claude.ai 커넥터 · 2-3
> 커넥터 방식 정석. API 키 없음. (직접 MCP 등록도 가능하나 커넥터와 중복 → 커넥터 하나만 권장)
- 연결: claude.ai → Settings → Connectors → Higgsfield → Connect → OAuth. **커넥터는 Claude Code 에 자동 동기화** (`claude mcp add` 불필요, 같은 계정이면 `claude mcp list` 에 자동 표시). 새로 연결 후 안 보이면 재시작 1회.
- ④ 크레딧 잔액 조회

### ✋7 영상 트리오 · 로컬+API키 · 2-4
- **Hyperframes**(로컬 CLI): `npm install -g hyperframes`. 의존성 Chrome·ffmpeg. 검증 `hyperframes --version`.
- **ElevenLabs**(MCP): `.env` `ELEVENLABS_API_KEY` (elevenlabs.io/app/settings/api-keys). 서버 `uvx elevenlabs-mcp`. ④ check_subscription.
- **HeyGen**(선택): `.env` `HEYGEN_API_KEY`. 서버 `uvx heygen-mcp`.

### ✋8 Buffer · Access Token · 3-1
- 사전: buffer.com 가입 + SNS 채널 연결. 발급: publish.buffer.com/account/apps → Create Access Token (1/xxx)
- 설치: `.env` `BUFFER_ACCESS_TOKEN`. 서버 `npx -y @damusix/buffer-mcp`.
- ④ listOrganizations → listChannels (연결 채널 확인)

### ✋9 Meta + Google Ads · 3-2
**9.1 Meta Ads** (hosted OAuth, 즉시):
- `claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads` → 재시작 → "광고 계정 보여줘" → 브라우저 OAuth(5 scope). .env 키 없음.
- ④ 광고 계정 목록

**9.2 Google Ads** (Developer Token + ADC, 승인 1~2일):
- Developer Token: ads.google.com/aw/apicenter (Manager 계정) → Apply for Basic → 승인 대기 → `.env` `GOOGLE_ADS_DEVELOPER_TOKEN`
- 서버: `uvx --from git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp` (`.mcp.json` 등록, `GOOGLE_PROJECT_ID` 필요)
- ADC: **Step 2 와 공유** — adwords 스코프 포함 3개로 로그인돼 있어야 함 (Step 2 참고). 없으면 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT`.
- ④ customers_list_accessible_customers

### ✋10 Notion · Claude.ai 커넥터 · 4-1
- 연결: claude.ai → Connectors → Notion → Connect → 워크스페이스 + 페이지 권한 부여(권한 준 페이지만 보임). 자동 동기화.
- ④ 워크스페이스 검색

### ✋11 Discord Channels · 공식 플러그인 + Bot Token · 4-2
> Anthropic 공식 `discord@claude-plugins-official` 단독. 폰 DM ↔ 세션 양방향. 요건: Claude Code v2.1.80+ · Bun · Anthropic 인증. 📚 https://code.claude.com/docs/ko/channels#discord

- **A. Bot 발급**: discord.com/developers/applications → New Application → Bot → Reset Token. **Message Content Intent ON** ⭐ (+Presence·Server Members). OAuth2 URL Generator → `bot` + 권한(Send Messages·Read History·Attach Files 등) → 서버 초대.
- **B. 플러그인 설치** (둘 중 하나):
  - 👤 TUI: `/plugin install discord@claude-plugins-official` (없으면 `/plugin marketplace add anthropics/claude-plugins-official` 먼저) → `/reload-plugins`
  - 🤖 CLI(Claude 대행 가능): `claude plugin install discord@claude-plugins-official`
  - 확인: `claude plugin list | grep discord`. 이미 설치면 스킵.
- **C. 토큰 등록**: `/discord:configure <Bot-Token>` → `~/.claude/channels/discord/.env` 저장
- **D. ⭐ 채널 세션 띄우기** (양방향 핵심·빠뜨리기 쉬움 · 👤 사용자 직접, Claude 대행 불가):
  ```bash
  claude --channels plugin:discord@claude-plugins-official   # 새 터미널, 한 줄
  ```
  - cd 선택(연결만이면 불필요·토큰은 전역 .env). ⚠️ `claude mcp list` Connected 여도 이 단계 없이는 폰→세션 푸시 안 됨. `--channels` 는 Research Preview 라 `--help` 에 안 보여도 정상.
- **E. 페어링**: 폰에서 봇 DM → 페어링 코드 → `/discord:access pair <코드>` → `/discord:access policy allowlist`
- ⚠️ **조직 정책** (claude.ai Team/Enterprise): 관리자가 `channelsEnabled` 켜야 메시지 도착 (claude.ai → Admin settings → Claude Code → Channels). Pro/Max 개인·Console API 키는 무관.

---

## 최종 · 재시작 + 헬스 체크

모든 키·인증 완료 후 Claude Code 완전 종료(⌘Q) → marketing-os 에서 재시작 (google-sheets 는 첫 실행 브라우저 OAuth 1회).
```bash
bash "$PRJ/scripts/healthcheck-all.sh"
```

진행률·헬스 표 형식 (예):
```
[████████░░] 8/11 · Ch1 데이터(Sheets·GA4·Firecrawl) Ch2 콘텐츠(Figma·YouTube·Higgsfield·영상) Ch3 광고(Buffer·Meta·Ads) Ch4 협업(Notion·Discord)
✅ Connected / ⚠️ Pending(google-ads 승인대기) / ○ 미설치
```

---

## 트러블슈팅

| 증상 | 해결 |
|---|---|
| ga4/google-ads 403 SCOPE_INSUFFICIENT | ADC 를 analytics+adwords+cloud-platform 3스코프로 재로그인 (Step 2) |
| gcloud "차단된 앱" | 본인 데스크톱 OAuth 클라이언트 `--client-id-file` 사용 |
| Figma 연결 안 됨 | `bun socket` 먼저 + Figma **데스크톱** 앱 + 플러그인 Connect |
| 커넥터(figma·higgsfield·notion) 안 보임 | claude.ai 재로그인 + Claude Code 재시작 |
| 재시작 후 MCP 안 보임 | marketing-os 폴더에서 실행했는지 확인 |
| Discord 폰 DM 무응답 | `claude --channels …` 세션 떠 있나 + 페어링 했나 + (조직)channelsEnabled |
| Discord 봇 교체 후 충돌 | `pkill -f "claude-plugins-official/discord"` 후 재시작 |
| Hyperframes 렌더 실패 | Chrome·ffmpeg 설치 |
| google-ads DEVELOPER_TOKEN 거절 | 사용 목적 명확히 재신청 / Test Account |

---

## 설치 완료 후
- **"start"** → 설치된 MCP 로 첫 결과물 (작업 메뉴 5개)
- **Part 3~6 에이전트** → 30개 에이전트가 본 MCP 자동 호출
- **Part 10 자동화** → cron 정기 실행 + Discord 알림

> Discord 상세 문서: `11-discord/channels-setup.md`
