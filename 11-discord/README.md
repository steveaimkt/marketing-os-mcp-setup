# 클립 4-2. Discord MCP · 자동화 알림·승인 AI 봇 구축

## 한 줄 요약

Discord(디스코드) MCP(엠씨피)를 설치하면 Claude(클로드)가 본인 서버에 **메시지를 보내고·읽고·답하고·반응을 받는 자동화 봇**이 된다. 알림·승인·CS 응답·주간 리포트가 모두 봇 한 개로 처리된다.

## 마케터에게 왜 필요한가

- 1인 마케터의 작업 결과를 **어디서 받을지** 가 늘 문제 · 슬랙은 회사용, 노션은 정적, 이메일은 너무 무거움
- 자동화 산출물 (주간 리포트·이상치 알림·발행 완료·CS 응답) 을 한 곳에서 받고 즉시 응답하고 싶음
- Discord 는 **무료·실시간·모바일 푸시·봇 친화적** · 1인 마케터 운영실로 가장 적합
- Discord MCP 설치 후 **30개 에이전트의 모든 산출물이 디스코드 한 채널에 흘러옴**. 봇에 답장·승인 reaction 도 가능

## 무엇이 가능해지나

| 케이스 | 자연어 명령 또는 트리거 | 시간 |
|---|---|---|
| A. 알림 발송 ★ | "이번 주 ROAS 리포트 #marketing 채널에 발송" | 5초 |
| B. 메시지 읽기 | "지난 24시간 #cs-inbox 채널 메시지 가져와줘" | 10초 |
| C. 메시지 검색 | "#marketing 채널에서 'campaign' 검색" | 5초 |
| D. 자동 응답 (CS) ★ | 고객이 #cs-inbox 에 질문 → Claude 자동 답변 (FAQ 매칭) | 30초 |
| E. 승인 워크플로 ★ | "광고 예산 변경 승인 요청 보내고 reaction 기다려" | 봇 대기 |
| F. 슬래시 명령 | `/weekly-report` → 봇이 즉시 응답 | 1분 |
| G. 임계치 알림 | ROAS < 1.5 자동 감지 → "@마케팅팀 광고 점검 필요" | 자동 |

## MCP 한눈

| 항목 | 값 |
|---|---|
| 패키지 | `mcp-discord` (npx · 커뮤니티 · barryyip0625) |
| 인증 | Bot Token (`DISCORD_TOKEN`) + Guild ID (`DISCORD_GUILD_ID`) |
| 의존 | `discord.js` v14 · WebSocket 양방향 연결 |
| 양방향 | ✅ 읽기·쓰기·이벤트 수신·reaction 처리 |
| 무료 한도 | Discord 무료 (개발자 봇 무제한) |

본 MCP 는 **Bot Token 방식 (양방향)**. Webhook (쓰기만) 보다 강력해서 자동 응답·승인 워크플로까지 가능합니다.

## 노출 도구 (주요 8개)

| 도구 | 기능 | 마케팅 사례 |
|---|---|---|
| `send_message` ★ | 채널·DM·스레드 메시지 발송 | 주간 리포트·알림·완료 통보 |
| `read_messages` | 채널 최근 메시지 N개 읽기 | CS 인박스 점검 |
| `list_messages` | 시간·키워드·작성자로 검색 | 과거 캠페인 메시지 조회 |
| `create_webhook` | 채널 webhook 생성 | 외부 시스템 → 디스코드 우회 발송 |
| `get_channel` | 채널 메타데이터 조회 | 권한·이름 확인 |
| `list_channels` | 서버 채널 목록 | 채널 매핑 |
| `add_reaction` | 메시지에 이모지 반응 | 승인 ✅ · 거절 ❌ 표시 |
| `read_reactions` | 메시지의 reaction 수집 | 승인 워크플로 결과 회수 |

## 사전 준비물

- Discord 무료 계정
- 본인 Discord 서버 1개 (없으면 새로 생성 · 2분)
- Node.js(노드 제이에스) 18+ · 터미널에서 `node --version`
- Discord Developer Portal 접근 (Bot Token 발급용)
- 봇 초대 가능한 서버 권한 (관리자)

## 작동 방식 (Bot Token 양방향)

```
[사용자 자연어 명령 또는 이벤트 트리거]
   ↓
[Claude Code]
   ↓
[mcp-discord 서버 (Bun · WebSocket)]
   ↓
[Discord Gateway · WebSocket 양방향 연결]
   ↓
[봇 계정 (사용자 서버에 초대된 봇)]
   ↓
[채널 · DM · 스레드에서 발송·읽기·reaction]
   ↓
[결과: 메시지 ID, reaction 결과, 이벤트 수신]
```

봇이 서버에 초대되어 있어야 작동 · OAuth2 URL 로 1회 초대.

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-discord`](mcp설치-discord/SKILL.md) | Bot 발급 + 서버 초대 + .mcp.json 등록 자동 진행 |
| 운영 단계 | "#marketing 에 발송" 같은 자연어 | Claude 가 `send_message` 호출 |

본 MCP 는 **거의 모든 에이전트가 호출**합니다 · 산출물의 최종 도착지가 대부분 디스코드. Part 3~10 의 30개 에이전트 중 약 절반이 본 MCP 사용.

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `Invalid Bot Token` | Token 오타·만료·재발급됨 | Discord Developer Portal > Bot > Reset Token 재발급 |
| 봇이 채널에 접근 못 함 | 채널 권한 부족 | 서버 Settings > Roles > 봇 역할에 채널 권한 부여 |
| `Guild not found` | Guild ID 오타 또는 봇 미초대 | Server Settings > Widget > Server ID 재확인 + OAuth URL 로 재초대 |
| 메시지 보내기 권한 거부 | 채널 권한에 "Send Messages" 없음 | 채널 우클릭 > Edit Channel > Permissions > 봇 역할 권한 확인 |
| `mcp__discord__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `python3 -c "import json; json.load(open('.mcp.json'))"` 검증 + Claude 재시작 |
| Bot 이 오프라인 표시 | mcp-discord 프로세스 미실행 | Claude Code 재시작 → 새 세션에서 봇 자동 온라인 |
| reaction 안 받아짐 | "Add Reactions" 권한 누락 | 봇 역할 권한 + Privileged Gateway Intents (Message Content) 활성화 |

## 검증된 산출물

- 주간 ROAS 리포트 디스코드 자동 발송 (`mkt-weekly-report` 에이전트)
- 광고 임계치 위반 시 채널 자동 알림 (`mkt-anomaly` 에이전트)
- 슬래시 명령으로 봇 즉시 응답 (`/weekly-report`, `/ax-team-run`)
- 승인 워크플로 (광고 예산 변경 → reaction ✅ → 자동 집행)
- CS 자동 응답 (FAQ DB 검색 → 매칭 시 즉시 답변)
- 매주 월요일 09시 cron → 디스코드 자동 발송 (Part 10 AX 시스템)

## 다음

→ [`실습.md`](실습.md)
