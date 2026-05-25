---
name: mcp설치-discord
description: |
  Part 2 클립 4-2 (Discord MCP) 전용 설치 스킬. Bot Token 발급 + 본인 서버 초대 + Guild ID 복사 + .mcp.json 등록 (`mcp-discord` 패키지) 을 10~15분 안에 완료하고 주간 리포트 발송 + 승인 reaction 워크플로 1건을 시연. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Discord MCP 설치하자"** ⭐ 주요 트리거
  - "디스코드 MCP 설치"
  - "Discord 봇 만들자"
  - "자동화 알림 봇 셋업"
  - "Part 2 / 4-2 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (서버 준비 + 봇 + Token + 초대 + Guild ID + .env + .mcp.json + 헬스 체크) →
  ③ 작업 가능 업무 (도구 8개 + 7 시나리오) →
  ④ 결과물 1개 (주간 리포트 발송 + 승인 reaction 워크플로)

  특이점: Bot Token 양방향 방식. WebSocket 으로 Discord Gateway 연결. 봇 초대 OAuth URL 필요. 30개 에이전트의 약 절반이 본 MCP 사용.
---

# Part 2 / 4-2 Discord MCP 설치 (클립 전용)

> 본 스킬은 Discord MCP 를 Bot Token 양방향 방식으로 설치하고 주간 리포트 + 승인 reaction 워크플로를 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Discord 의 Bot + OAuth 초대 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
🤖 Discord MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Discord MCP 는 'Claude 가 본인 서버에 봇으로 들어가는 신경' 입니다.
  Webhook (쓰기만) 과 달리 Bot Token 양방향 방식 · 읽기·발송·reaction·슬래시 모두 가능.
  코드 작성 안 합니다. "주간 리포트 발송" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (10~15분 예상):

  📖 STEP 1: MCP 소개 (2분)
       1.1 Bot Token 양방향 + WebSocket 흐름
       1.2 도구 8개 (send_message 가 90% 점유)
       1.3 Before vs After 비교 (30분 → 1~2분)

  ⚙️ STEP 2: MCP 설치 (10~15분)
       2.1 Discord 서버 준비 (사용자 2분 · 없을 때만)
       2.2 봇 + Token 발급 (사용자 5분)
       2.3 봇을 서버에 초대 OAuth (사용자 3분)
       2.4 Guild ID 복사 (사용자 1분)
       2.5 .env + .mcp.json 등록 (자동 2분)
       2.6 헬스 체크 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 8개 (send/read/list/reaction/webhook)
       3.2 7 시나리오 (알림·읽기·검색·자동응답·승인·슬래시·임계치)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 2개 (다른 MCP 조합 시연)
       4.1 유튜브 채널 분석 → 디스코드 자동 보고 (약 1분)
       4.2 이메일 분석 → 디스코드 자동 분류 (약 30초)

사전 점검 5가지부터:
  □ Node.js 18 이상
  □ Discord 무료 계정
  □ 본인 Discord 서버 1개 (없으면 만들기)
  □ Developer Portal 접근 (계정 동일)
  □ Chrome 또는 Safari

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | Discord 서버에 봇으로 들어가서 메시지 발송·읽기·reaction 처리하는 도구 |
| 제공사 | barryyip0625 (커뮤니티 · `mcp-discord`) |
| 라이선스 | MIT |
| 인증 방식 | Bot Token + Guild ID (`DISCORD_TOKEN`, `DISCORD_GUILD_ID`) |
| 연결 방식 | WebSocket (Discord Gateway 양방향) |
| 도구 prefix | `mcp__discord__*` (총 8개) |
| 무료 한도 | Discord 무료 (개발자 봇 무제한) |
| Before | 노션·슬랙 회수 + 의사결정 · 30분/건 |
| After | 봇 자동 발송 + reaction 1번 · 1~2분 |

### 1.2 마케터 관점 활용 가능성

- **30개 에이전트 산출물 단일 도착지** · 주간 리포트·임계치 알림·콘텐츠 발행·CS 응답 모두 디스코드
- **승인 워크플로 reaction** · 광고 예산 변경·콘텐츠 발행 1번 클릭 승인
- **자동 응답 봇** · #cs-inbox 채널 FAQ 매칭 즉시 답변
- **슬래시 명령** · `/weekly-report`, `/ax-team-run` 으로 봇 즉시 호출
- **임계치 자동 알림** · ROAS·CPA 위반 시 `@마케팅팀` 멘션 (사람보다 먼저 발견)

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| 노션 페이지 열기 | 1분 | 즉시 (모바일 푸시) |
| 광고 리포트 읽기 | 5분 | 30초 (embed 보기) |
| 임계치 위반 확인 | 3분 | 즉시 (자동 멘션) |
| 슬랙·이메일 공유 | 5분 | 즉시 (자동 발송) |
| 의견·승인 받기 | 15분 | 5초 (reaction 클릭) |
| **산출물 회수 1건** | **30분** | **1~2분** |
| **정기 운영 (하루 5~10건)** | **2.5~5h/일** | **5~20분/일** |

연간 환산: 약 500~1,000시간 절감 + 광고 사고 대응 평균 5분 이내.

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 7단계

### 2.1 STEP 1 / 7 · Discord 서버 준비 (사용자 직접 · 2분 · 신규만)

사용자에게 묻기:

```
"본인 Discord 서버가 있나요? (y/n)"
- y: 본 단계 스킵
- n: 다음 안내
```

신규 가입자 안내:

```
① Discord 좌측 사이드바 + 버튼 → "Create My Own" 선택
② "For me and my friends" 선택 (개인용)
③ 서버 이름 입력 (예: "marketing-os")
④ 서버 생성 완료

권장 채널 4개 만들기 (각각 + 채널 클릭):
  - #general (기본 · 자동 생성)
  - #marketing (주간 리포트·캠페인 알림)
  - #cs-inbox (고객 응대 큐)
  - #approvals (예산·발행 승인)
```

### 2.2 STEP 2 / 7 · 봇 + Token 발급 (사용자 직접 · 5분) ★ 가장 중요

사용자에게 안내:

```
브라우저에서 다음 절차를 진행하세요:

① discord.com/developers/applications 접속 → 로그인
② 우상단 "New Application" 클릭
③ 이름 입력 (예: "Marketing OS Bot") → Create
④ 좌측 메뉴 "Bot" 선택
⑤ "Reset Token" 클릭 → "Yes, do it!" 확인
⑥ 표시된 Token 복사 ⚠️ 한 번만 표시
   토큰 형식: 영문+숫자 약 70자 (점 2개 포함)

⚠️ Privileged Gateway Intents 3개 모두 활성화 ★ 필수:
   - PRESENCE INTENT 토글 ON
   - SERVER MEMBERS INTENT 토글 ON
   - MESSAGE CONTENT INTENT 토글 ON ★ 메시지 읽기 필수

⑦ "Save Changes" 클릭
```

복사한 토큰을 Claude 에게 전달.

⚠️ **MESSAGE CONTENT INTENT 누락이 가장 자주 발생하는 실수**. 읽기 작업이 모두 빈 응답으로 옴.

### 2.3 STEP 3 / 7 · 봇을 본인 서버에 초대 (사용자 직접 · 3분)

```
같은 Developer Portal 페이지에서:

① 좌측 메뉴 "OAuth2" 선택
② "URL Generator" 클릭
③ Scopes 체크 (2개):
   ✅ bot
   ✅ applications.commands

④ Bot Permissions 체크 (7개 필수):
   ✅ Send Messages
   ✅ Read Message History
   ✅ Manage Messages
   ✅ Add Reactions
   ✅ Use Slash Commands
   ✅ Embed Links
   ✅ Attach Files

⑤ 화면 하단 생성된 URL 복사
⑥ 새 탭에서 URL 열기
⑦ 본인 서버 선택 → "Continue"
⑧ 권한 확인 → "Authorize"
⑨ reCAPTCHA 통과
⑩ "✅ Authorized" 표시
⑪ Discord 서버로 돌아가서 좌측 회원 목록 확인 → 봇이 "Online" 으로 표시
```

### 2.4 STEP 4 / 7 · Guild ID 복사 (사용자 직접 · 1분)

방법 1 (개발자 모드 사용):

```
① Discord 좌하단 톱니바퀴 (User Settings)
② "Advanced" 선택 (한국어 "고급")
③ "Developer Mode" 토글 ON
④ 본인 서버 이름 우클릭 → "Copy Server ID"
⑤ 숫자 약 18~19자 복사됨
```

방법 2 (Widget 사용):

```
① 본인 서버 이름 우클릭 → "Server Settings"
② 좌측 메뉴 "Widget" 선택
③ "Server ID" 항목의 ID 복사
```

복사한 Server ID 를 Claude 에게 전달.

### 2.5 STEP 5 / 7 · .env 등록 (Claude 자동 · 1분)

Claude 자동 실행:

```bash
cd "${CLAUDE_PROJECT_DIR}"

# .env 에 추가
if ! grep -q "DISCORD_TOKEN" .env 2>/dev/null; then
  echo "DISCORD_TOKEN=발급받은_봇_토큰" >> .env
  echo "DISCORD_GUILD_ID=서버_ID" >> .env
fi

# 검증
grep DISCORD_ .env
```

### 2.6 STEP 6 / 7 · .mcp.json 등록 (Claude 자동 · 1분)

`marketing-os/.mcp.json` 의 `mcpServers` 에 추가:

```json
"discord": {
  "_part": "2 Ch 4-2 자동화 알림·승인 봇",
  "command": "npx",
  "args": ["-y", "mcp-discord"],
  "env": {
    "DISCORD_TOKEN": "${DISCORD_TOKEN}",
    "DISCORD_GUILD_ID": "${DISCORD_GUILD_ID}"
  }
}
```

JSON 검증:

```bash
python3 -c "import json; json.load(open('.mcp.json'))"
```

### 2.7 STEP 7 / 7 · Claude Code 재시작 + 헬스 체크 (자동 1분)

사용자에게 안내:

```
Claude Code 를 완전 종료 (메뉴 > 종료 또는 ⌘Q) 후 재시작하세요.

새 세션에서 다음 명령으로 검증:
"디스코드 서버 채널 목록 보여줘"
```

내부적으로 `mcp__discord__list_channels` 호출됨.

성공 응답:

```
✅ Discord 봇 연결 확인. 서버 "marketing-os" 채널 4개:
  - #general (text)
  - #marketing (text)
  - #cs-inbox (text)
  - #approvals (text)

봇 상태: 온라인 · 권한: Send/Read/React/Manage 7종
사용 가능 도구 8종: send_message, read_messages, list_messages, ...
```

### 2.8 보안 점검

설치 직후 확인:
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 값은 `${VAR}` 참조 (Token 평문 직접 입력 금지)
- [ ] Bot Token 이 git log 에 노출된 적 없는지 (노출 시 즉시 Reset Token)
- [ ] 봇 권한이 필요한 채널에만 부여 (재무·HR 채널 권한 부여 금지)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 8개

| 도구 | 기능 |
|---|---|
| `send_message` ★ | 채널·DM·스레드 메시지 발송 (90% 호출 점유) |
| `read_messages` | 채널 최근 메시지 N개 |
| `list_messages` | 시간·키워드·작성자 검색 |
| `list_channels` | 서버 채널 목록 |
| `get_channel` | 채널 메타데이터 |
| `add_reaction` | 메시지 이모지 반응 |
| `read_reactions` | 메시지의 reaction 수집 |
| `create_webhook` | 채널 webhook 생성 (보조) |

### 3.2 마케터가 자주 쓰는 7 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 알림 발송 ★ | "#marketing 에 주간 리포트 발송" | 5초 |
| B. 메시지 읽기 | "지난 24시간 #cs-inbox 가져와줘" | 10초 |
| C. 메시지 검색 | "#marketing 에서 campaign 검색" | 5초 |
| D. 자동 응답 ★ | (이벤트 트리거) FAQ 매칭 → 답변 자동 | 30초 |
| E. 승인 워크플로 ★ | "예산 변경 reaction 받아줘" | 1~5분 |
| F. 슬래시 명령 | `/weekly-report` | 1분 |
| G. 임계치 알림 | (이벤트) ROAS < 1.5 → @멘션 | 자동 |

### 3.3 다른 MCP 와 조합 시나리오

- **+ Google Sheets MCP** · 시트 분석 완료 → 디스코드 자동 알림
- **+ Meta·Google Ads MCP** · 광고 ROAS 위반 → 디스코드 임계치 멘션
- **+ Notion MCP** · 콘텐츠 캘린더 갱신 → 디스코드 발행 큐 통보
- **+ Buffer MCP** · 5채널 예약 완료 → 디스코드 결과 표 발송
- **+ GA4 MCP** · 주간 트래픽 리포트 → 디스코드 자동 게시

본 MCP 는 **30개 에이전트 중 약 절반이 사용** · 마케팅 OS 의 신경 매개.

---

## 🎯 STEP 4: 결과물 2개 · 다른 MCP 조합 시연

본 STEP 의 핵심은 **Discord MCP 는 매개일 뿐, 다른 MCP 와 조합되는 패턴이 진짜 가치**임을 보여주는 것. 봇이 슬래시 명령·채널 멘션을 받아서 → 다른 MCP 를 호출하고 → 결과를 디스코드로 자동 발송하는 흐름.

### 4.1 시연 A · 유튜브 채널 분석 → 디스코드 자동 보고 (약 1분)

**사전 조건**: YouTube Data MCP 사전 설치 (Part 2 / 2-2 클립). 본인 유튜브 채널 1개 (분석 대상).

```
사용자: 디스코드 #marketing 채널에서 멘션 또는 슬래시 명령:

  @봇 우리 채널 지난 7일 분석해줘
  또는
  /youtube-analyze weekly
```

자동 실행:

```
1. Discord MCP · 채널 멘션 또는 슬래시 명령 이벤트 수신
   - 이벤트 종류: messageCreate · interactionCreate
   - 트리거 키워드: "분석" 또는 command "youtube-analyze"

2. YouTube Data MCP 호출 (3건):
   - mcp__youtube-data__get_channel_stats (구독자·조회수·기간)
   - mcp__youtube-data__list_recent_videos (상위 5개 영상)
   - mcp__youtube-data__get_comments (영상별 최근 댓글)

3. Claude 가 댓글 감정 분석 (긍정·부정·중립 비율)

4. Discord MCP · send_message 호출:
   - channel_id: marketing
   - embed:
     * 제목: 📺 W19 채널 성과 요약
     * 필드: 구독자 변화 + 조회수 + 댓글 감정
     * Top 5 영상 표
     * 인사이트 3 bullet (어떤 콘텐츠가 잘 됐는지)
   - 색상: YouTube 레드 (0xFF0000)

5. 결과: 사용자 모바일에 푸시 도착 + 채널에 embed 표시
   소요: 약 1분 (사람 손 30분 → 30배 단축)
```

성공 기준:
- [ ] YouTube API 호출 3건 성공
- [ ] Discord embed 가 #marketing 채널에 정상 표시
- [ ] 모바일 푸시 알림 확인
- [ ] 댓글 감정 분석 합계 100% (긍정+부정+중립)

### 4.2 시연 B · 이메일 분석 → 디스코드 자동 분류 (약 30초)

**사전 조건**: Gmail MCP (Claude.ai 통합) 사전 활성화. CS 메일 받는 Gmail 계정.

```
사용자: 디스코드 #cs-inbox 채널에서 슬래시 명령:

  /email-triage 24h
  또는
  @봇 지난 24시간 CS 메일 분석해줘
```

자동 실행:

```
1. Discord MCP · 슬래시 명령 이벤트 수신
   - command: email-triage
   - param: 24h

2. Gmail MCP 호출:
   - mcp__claude_ai_Gmail__list_messages
     query: "label:CS newer_than:24h"
     max_results: 100

3. Claude 가 메일 N개를 4 카테고리로 분류:
   - 🚨 긴급 (배송 분실 · 결제 오류 · VIP 컴플레인)
   - 💰 환불·교환 (제품 하자 · 단순 변심)
   - 💬 일반 문의 (사이즈 · 재입고)
   - 🚫 스팸 (광고 · 외부 영업)

4. 긴급 3건 본문 발췌 (제목·발신자·요지 3줄)

5. Discord MCP · send_message 호출:
   - channel_id: cs-inbox
   - embed:
     * 제목: 📧 CS 메일 N건 분류
     * 카테고리 4종 카운트 표
     * 긴급 3건 미리보기
     * 권장 액션 (예: 환불 8건 일괄 처리)
   - 색상: Gmail 레드 (0xEA4335)

6. 결과: 마케터는 채널에서 긴급 3건만 먼저 처리
   소요: 약 30초 (사람 손 20분 → 40배 단축)
```

성공 기준:
- [ ] Gmail API 호출 1건 (배치) 성공
- [ ] 분류 정확도 ≥ 90% (긴급 인식 우선)
- [ ] Discord embed 4 카테고리 카운트 합 = 전체 메일 수
- [ ] 긴급 3건 미리보기 본문 발췌 정확

### 4.3 다음 단계 제안

```
🎉 Discord MCP 설치 + 다른 MCP 조합 2건 완성. 다음 가능합니다:

  A. 더 많은 MCP 조합 시도:
     - "/weekly-roas" · Discord + Meta Ads + Google Ads (광고 성과)
     - "/ga4-traffic" · Discord + GA4 + Sheets (웹 트래픽)
     - "/content-cal" · Discord + Notion (콘텐츠 캘린더 발행)
     - "/competitor-check" · Discord + Firecrawl (경쟁사 스크랩)

  B. 정기 자동화 (Part 5 · 7 · 8 · 10):
     - youtube-monitor · 매일 09시 유튜브 채널 자동 분석 발송
     - cs-responder · 메일 도착 즉시 자동 응답 + 분류
     - mkt-weekly-report · 매주 월요일 종합 리포트
     - orchestrator · 슬래시 명령으로 30개 에이전트 호출

  C. 디스코드 봇 고급 패턴:
     - 임계치 자동 알림 (Case G · ROAS < 1.5 → @멘션)
     - 승인 reaction 워크플로 (Case E · 광고비 변경)
     - FAQ 자동 응답 봇 (Case D · #cs-inbox 채널 봇)

  D. Part 3 콘텐츠 파이프라인:
     - Part 2 의 12개 MCP 설치 완료. 본격적인 에이전트 구축 시작.
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 4-2 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-discord` 스킬을 호출해 Discord Bot Token 발급 + 서버 초대 + `.mcp.json` 등록을 10~15분 안에 완료하고, **첫 자동화 봇** (주간 리포트 + 승인 reaction 워크플로) 1건을 시연.

### 실습 첫 결과물 명령 · YouTube 채널 분석 → 디스코드 자동 보고

**사전 조건**: YouTube Data MCP 사전 설치 (Part 2 / 2-2 클립). 본인 유튜브 채널 1개.

디스코드 `#marketing` 채널에서:

```
@봇 우리 채널 지난 7일 분석해줘

또는 슬래시 명령:
/youtube-analyze weekly
```

→ Discord MCP 가 매개. YouTube Data 호출 → embed 형식 자동 발송. 수동 약 30분 → MCP 약 1분 (**30배 단축**).

### 실습 두 번째 결과물 명령 · 이메일 분석 → 디스코드 자동 분류

**사전 조건**: Gmail MCP (Claude.ai 통합) 사전 활성화. CS 메일 받는 Gmail 계정.

디스코드 `#cs-inbox` 채널에서:

```
@봇 지난 24시간 CS 메일 분석해줘

또는 슬래시 명령:
/email-triage 24h
```

→ Gmail 호출 → 카테고리 분류 (긴급·환불·일반·스팸) → embed 발송. 수동 약 20분 → MCP 약 30초 (**40배 단축**).

### 실습 세 번째 결과물 · 봇 + 슬래시 명령 확장 패턴

| 슬래시 명령 | 조합 MCP | 결과 도착 채널 |
|---|---|---|
| `/youtube-analyze` | Discord + YouTube Data | #marketing |
| `/email-triage` | Discord + Gmail | #cs-inbox |
| `/weekly-roas` | Discord + Meta Ads + Google Ads | #marketing |
| `/ga4-traffic` | Discord + GA4 + Sheets | #marketing |
| `/content-cal` | Discord + Notion | #marketing |
| `/competitor-check` | Discord + Firecrawl | #marketing |
| `/cs-respond` | Discord + Gmail + Notion (FAQ DB) | #cs-inbox |

본 클립의 Discord MCP 는 **30개 에이전트의 진입점이자 도착지**. 클립 끝나면 본인의 모든 마케팅 흐름이 디스코드 한 채널로 자동 모임.

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
1인 마케터의 디스코드 운영 어시스턴트

[입력]
- 봇이 초대된 서버 (4채널 구조: general · marketing · cs-inbox · approvals)
- 30개 에이전트 결과를 디스코드로 받기 위한 채널 매핑

[산출물]
매일 자동:
  ① 09:00 · 어제 광고 성과 요약 → #marketing
  ② 12:00 · 오전 #cs-inbox 자동 응답 처리
  ③ 18:00 · 오늘 콘텐츠 발행 결과 → #marketing
  ④ ROAS < 1.5 감지 즉시 → @마케팅팀 알림

매주 월요일 09:00 추가:
  ⑤ 주간 종합 리포트 (HTML 첨부) → #marketing
  ⑥ 다음 주 콘텐츠 캘린더 → #marketing 의 thread

승인 워크플로:
  ⑦ 예산 변경 · 콘텐츠 발행 · 신규 캠페인 → #approvals

[제약]
- 멘션 @here · @everyone 은 긴급 시에만 (월 5회 한도)
- 모든 봇 발송 메시지는 embed 형식 (가독성)
- 색상 코드: 그린 (정상) · 옐로우 (주의) · 레드 (긴급)
- 슬래시 명령 등록: /weekly-report, /ax-team-run, /cs-search

[검증]
- 30개 에이전트 결과의 90% 이상이 디스코드로 도착
- 승인 워크플로 응답 시간 평균 5분 이내
- CS 자동 응답 정확도 80% 이상 (FAQ 매칭률)
```

### 응용 과제

1. 본인 서버에 봇 초대 후 "안녕 봇" 메시지 → 즉시 응답 자동화
2. 슬래시 명령 `/echo <text>` 등록 → 봇이 그대로 메아리
3. 4개 채널 매핑 메모리에 저장 (`#marketing`, `#cs-inbox`, `#approvals`, `#general`)
4. **Part 6 광고 클립의 `mkt-anomaly` 에이전트가 본 MCP 를 자동 호출** · 미리 #marketing 채널 준비

---

## 트러블슈팅 (Discord MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `Invalid Bot Token` | Token 만료·오타·재발급됨 | Developer Portal > Bot > Reset Token 재발급 |
| 봇이 오프라인 표시 | mcp-discord 프로세스 미실행 또는 .mcp.json 오류 | Claude Code 재시작 (새 세션에서 자동 온라인). 오프라인 지속 시 .mcp.json + .env 검증 |
| `Guild not found` | Guild ID 오타 또는 봇 미초대 | Server Settings > Widget > Server ID 재확인 + OAuth URL 로 재초대 |
| 메시지 보내기 실패 (`Missing Access`) | 채널 권한 부족 | 채널 우클릭 > Edit Channel > Permissions > 봇 역할 권한 추가 (Send Messages) |
| 메시지 읽기 안 됨 (빈 응답) ★ | MESSAGE CONTENT INTENT 미활성화 | Developer Portal > Bot > Privileged Gateway Intents > MESSAGE CONTENT INTENT 토글 ON |
| `mcp__discord__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `claude mcp list` 등록 확인 + Claude Code 완전 종료 후 재시작 |
| reaction 자동 처리 안 됨 | "Add Reactions" 권한 누락 또는 PRESENCE INTENT 비활성 | 봇 역할 권한 + Developer Portal Intents 모두 ON |
| Embed 색상 안 보임 | 색상값 형식 오류 (HEX 대신 정수 필요) | `0x5AE2A8` 형식 또는 정수 변환 (`5957288`) |
| 메시지 100개 이상 못 가져옴 | Discord API limit | 페이지네이션 (before/after 파라미터) 자동 분할 |
| 슬래시 명령 등록 안 됨 | applications.commands scope 누락 | OAuth URL 재생성 시 `applications.commands` 체크 후 재초대 |
| 봇이 채널을 못 봄 | 비공개 채널에 봇 역할 미부여 | 채널 우클릭 > Edit Channel > Permissions > Roles & Members 에 봇 역할 추가 |

## 강의 연결

- 본 스킬은 [클립 4-2 Discord MCP 대본](../대본/4-2-discord.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Discord 의 Bot + WebSocket 패턴에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 **30개 에이전트 중 약 절반이 자동 호출** · 모든 알림·승인·CS 응답의 매개.
- 주요 활용 에이전트:
  - Part 6 · `mkt-anomaly` · 광고 임계치 자동 알림
  - Part 7 · `mkt-weekly-report` · 매주 월요일 자동 발송
  - Part 8 · `cs-responder` · CS 채널 자동 응답
  - Part 10 · `orchestrator` · 슬래시 명령 라우팅
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/11-discord/mcp설치-discord/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2)
  - `marketing-agents/.mcp.json` (mcp-discord 등록 예시)
  - `marketing-agents/agents/mkt-discord-weekly.md`
  - `marketing-agents/agents/mkt-anomaly.md`
  - `marketing-agents/agents/mkt-cs-response.md`

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| MCP 패키지 | `mcp-discord` (npx · barryyip0625) |
| GitHub 저장소 | <https://github.com/barryyip0625/mcp-discord> |
| 의존성 | `@modelcontextprotocol/sdk` + `discord.js` v14 |
| Developer Portal | <https://discord.com/developers/applications> |
| Token 형식 | 영문+숫자 약 70자 (점 2개 포함) |
| Guild ID 형식 | 숫자 약 18~19자 |
| 필요 Intents (3개) | PRESENCE · SERVER MEMBERS · MESSAGE CONTENT |
| 필요 OAuth Scopes | bot · applications.commands |
| 필요 Bot Permissions (7개) | Send Messages · Read Message History · Manage Messages · Add Reactions · Use Slash Commands · Embed Links · Attach Files |
| 노출 도구 | 8개 (`send_message`, `read_messages`, `list_messages`, `list_channels`, `get_channel`, `add_reaction`, `read_reactions`, `create_webhook`) |
| Embed 색상 형식 | 0x5AE2A8 또는 정수 |
| Discord API 제한 | 메시지 100개/요청 (페이지네이션 자동) |

## 메모리·문서 연결

- 사용자의 Guild ID + 채널 4개 ID 매핑은 메모리로 저장 (자주 사용)
- 봇 권한 역할 이름도 메모리 저장 (디버깅 시 빠른 확인)
- 본 스킬 종료 후 사용자가 "자동 알림 만들자" 라고 하면 Part 6 의 `mkt-anomaly` 또는 Part 10 의 `/agent-builder` 로 전달
- 슬래시 명령 등록 요청 시 `discord.js` SlashCommandBuilder 패턴 안내
