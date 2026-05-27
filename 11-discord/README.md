# 클립 4-2. Discord Channels · 폰 ↔ Claude 양방향 자동화 봇 구축

> ⚠️ **노선 변경 안내 (2026-05-26)** · 본 클립은 **Anthropic 공식 Channels Discord 플러그인** (`discord@claude-plugins-official`) 단독 노선으로 전면 전환됨. 기존 서드파티 `mcp-discord` (barryyip0625) 노선은 폐기. 폐기된 스킬은 `_deprecated_` 마커 + 참고용으로만 보존.
>
> 새 표준 스킬: [`mcp설치-discord-channels/SKILL.md`](mcp설치-discord-channels/SKILL.md)

## 한 줄 요약

Discord(디스코드) **공식 Channels 플러그인**을 설치하면 폰의 Discord DM 이 Claude Code 세션에 자동 푸시되고, Claude 가 작업·분석·답신을 모두 디스코드로 돌려보낸다. 출장 중 폰에서 Claude 한테 명령하고 답신 받는 일이 핵심 시나리오.

## 마케터에게 왜 필요한가

- 1인 마케터가 책상에 24시간 앉아 있을 수 없음. **외출·이동 중에도 마케팅 작업 지시·확인** 필요
- 디스코드는 **무료·실시간·모바일 푸시**. 1인 마케터 운영실로 가장 적합
- 본 클립의 Channels 단독 노선으로 **폰 DM 한 줄 → Claude 분석 → 폰 답신** 패턴 완성
- Gmail·Google Calendar 와 결합해 **"오늘 일정"·"CS 메일 분류"·"내일 미팅 추가"** 같은 자동화가 폰 한 대로 가능

## 무엇이 가능해지나 (시나리오 8개)

| # | 시나리오 | 자연어 명령 또는 트리거 | 시간 |
|---|---|---|---|
| 1 | 폰 DM 양방향 채팅 ★ | 폰에서 "지난 광고 어땠어?" | 30초 |
| 2 | Gmail 결합 분석 ★ | 폰에서 "지난 24시간 CS 메일 분류해줘" | 30초 |
| 3 | Calendar 결합 ★ | 폰에서 "오늘 일정 알려줘" / "내일 14시 미팅 추가" | 30초 |
| 4 | 첨부 파일 분석 | 폰에서 PDF 첨부 → "이 보고서 요약" | 1분 |
| 5 | 진행 상황 라이브 업데이트 | Claude 가 `edit_message` 로 5초마다 갱신 | 자동 |
| 6 | 최근 100개 메시지 요약 | 폰에서 "이 DM 의 최근 10개 요약" | 10초 |
| 7 | 도구 권한 원격 승인 | 채널 권한 릴레이로 폰에서 승인/거부 | 자동 |
| 8 | 멀티 채널 동시 운영 | Discord + Telegram + iMessage 한 세션 | — |

## 🎯 노선 비교 (구버전 vs 신버전)

| 항목 | 구버전 (폐기 · 2026-05-26) | 신버전 (현행 · 공식 단독) |
|---|---|---|
| 패키지 | `mcp-discord` (npm · barryyip0625 · 서드파티) | `discord@claude-plugins-official` (Anthropic 공식) |
| 봇 수 | 1~2개 (서드파티 단독 또는 하이브리드) | 1개 (공식 단독) |
| 도구 수 | 30+ 개 (채널·역할·포럼·웹훅·메시지) | 5개 (`reply`·`react`·`edit_message`·`fetch_messages`·`download_attachment`) |
| 통신 패턴 | 단방향 (Claude → Discord) | 양방향 (Discord ↔ Claude) |
| 무인 cron 발송 | ✅ 가능 | ❌ 세션 의존 (대신 Discord Webhook 으로 우회) |
| 양방향 채팅 | ❌ | ✅ |
| 인증 위치 | `marketing-os/.env` | `~/.claude/channels/discord/.env` |
| 실행 명령 | 일반 `claude` | `claude --channels plugin:discord@...` |
| 런타임 | Node.js | **Bun 필수** |
| 단계 | 안정 (npm publish) | **Research Preview** (v2.1.80+) |
| 유지보수 | 1인 개발자 | Anthropic 공식 |

→ 강의는 신버전 공식 노선만 다룸. 구버전은 `_deprecated_` 마커 + 참고용.

## MCP 한눈 (공식 단독 · 현행 노선)

| 항목 | 값 |
|---|---|
| 패키지 | `discord@claude-plugins-official` (Anthropic 공식) |
| 출처 | https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord |
| 인증 | Bot Token (`DISCORD_BOT_TOKEN`) — Channels 자동 관리 |
| 런타임 | Bun 1.0+ |
| Claude Code 최소 | v2.1.80 |
| 인증 요구 | claude.ai 로그인 (API Key 인증 불가) |
| 단계 | Research Preview (`--channels` 플래그·프로토콜 변경 가능성) |
| 무료 한도 | Discord 무료 (개발자 봇 무제한 · Pro/Max 무관) |

## 노출 도구 5개

| 도구 | 기능 | 마케팅 사례 |
|---|---|---|
| `reply` ★ | 채널·DM 메시지 전송 (text + 선택적 reply_to + 파일 ≤10개/25MB) | 폰 DM 답신·일정·메일 분류 결과 |
| `react` | 이모지 반응 (`👍` 또는 `<:name:id>`) | 처리 완료 ✅ 표시 |
| `edit_message` | 봇이 보낸 메시지 편집 | 진행 상황 5초마다 갱신 |
| `fetch_messages` | 채널 최근 메시지 (최대 100개 · 시간순) | DM 히스토리 요약 |
| `download_attachment` | 메시지 첨부 다운로드 → `~/.claude/channels/discord/inbox/` | PDF·이미지 분석 |

## Gmail + Google Calendar 결합 (강의 STEP 4)

본 클립의 핵심 결합 시나리오 — 폰 DM 한 줄로 Gmail · Calendar 까지 운영:

```
폰 DM: "오늘 일정 알려줘"
   ↓
Channels 메시지 수신
   ↓
mcp__claude_ai_Google_Calendar__list_events 호출
   ↓
정리 (시간순 · 위치 · 참석자)
   ↓
reply 도구로 폰 DM 답신
   ↓
📅 오늘 일정 (3건) ... (가독성 있는 텍스트)
```

같은 패턴으로 가능한 결합:
- **Gmail** · `search_threads` + 분류 → reply (CS 인박스 자동 분류)
- **Calendar** · `create_event` → reply (폰에서 일정 추가)
- **Sheets** · `read_sheet` → reply (마케팅 시트 분석)
- **GA4** · `run_report` → reply (트래픽 한 줄 답신)
- **Meta·Google Ads** · `get_insights` → reply (ROAS 답신)
- **Notion** · `notion-create-page` → reply (답변 저장)

## 한계 4가지 + 보완 방법

| # | 한계 | 우회 |
|---|---|---|
| 1 | **세션 의존** · `--channels` 활성 세션이 떠 있을 때만 작동 | 아래 "호스팅 옵션" 표 참조 |
| 2 | **메시지 검색 미지원** · 100개 한도 + 시간순만 | 100개씩 페이지네이션 또는 외부 도구 |
| 3 | **무인 cron 발송 불가** · `reply` 는 수신 후에만 호출 | 단순 알림은 Discord Webhook (`curl -X POST $WEBHOOK_URL`) |
| 4 | **채널/역할 자동 생성 불가** · 5개 도구만 노출 | 채널 구조는 사용자가 수동으로 만들기 |

## ⚠️ 호스팅 옵션 5종 (노트북 닫으면 종료 문제)

⚠️ **본 노선의 가장 큰 트레이드오프**: Channels 는 활성 Claude Code 세션이 떠 있어야 메시지가 도착. **노트북 닫으면 sleep → 세션 종료 → 폰 DM 보내도 답신 없음**. 마케팅 자동화로 본격 운영하려면 항상 켜진 환경 필요.

| # | 옵션 | 1회 비용 | 월 비용 | 복잡도 | 적합 마케터 |
|---|---|---|---|---|---|
| 1 | **`caffeinate -dis`** | 0 | 0 (외부 전원 필요) | ⭐ | 임시·간헐 사용 |
| 2 | **데스크톱 PC 24시간** + caffeinate | 0 (있다면) | 전기료 5~10$ | ⭐ | 책상에 PC 있는 사람 · ⭐ 권장 1 |
| 3 | **Mac mini 홈 서버** | 600~1,400$ | 전기료 2~5$ | ⭐⭐ | 본격 운영 · ⭐ 권장 2 |
| 4 | **Raspberry Pi 5** | 80~150$ | 전기료 1$ | ⭐⭐⭐ | 기술 관심 있는 사람 |
| 5 | **Linux VPS** | 0 | 6~12$ | ⭐⭐⭐⭐ | 진입장벽 큼 (claude.ai OAuth 브라우저 없음) |

권장 흐름:
1. **임시·검증 단계** → `caffeinate -dis` (옵션 1) · 0 비용
2. **본격 운영 시작** → 데스크톱 PC 24시간 (옵션 2) · 책상 PC 활용
3. **장기 안정 운영** → Mac mini 홈 서버 (옵션 3) + launchd plist 상시 가동

자세한 실행 명령 + launchd plist 골격은 [`mcp설치-discord-channels/SKILL.md`](mcp설치-discord-channels/SKILL.md) 의 STEP 4.5 참조.

## 🔧 부가 기능 4가지 (공식 문서에서 추가 발견 · 마케터 가치)

| # | 기능 | 역할 | 마케터 활용 |
|---|---|---|---|
| 1 | **권한 릴레이** | 도구 사용 권한을 폰 DM 으로 푸시 → 원격 ✅/❌ 클릭 승인 | 광고 예산·콘텐츠 발행 같은 위험 작업에서 안전장치 |
| 2 | **멀티 채널** | `--channels` 에 Discord + Telegram + iMessage 공백 나열 → 한 세션 동시 수신 | 본인이 메신저 여러 개 쓸 때 통합 운영 |
| 3 | **access 정책 3가지** | `pairing` / `allowlist` / `groups` | 본인만 (allowlist · 기본) / 팀 + 가족 (groups) / 오픈 (pairing) |
| 4 | **`--dangerously-skip-permissions`** | 권한 프롬프트 모두 우회 | ⚠️ 신뢰 환경 무인 자동화만. 광고 예산 같은 위험 작업은 권한 릴레이 권장 |

자세한 시나리오는 [`mcp설치-discord-channels/SKILL.md`](mcp설치-discord-channels/SKILL.md) 의 STEP 3.5 참조.

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| ⭐ **연결 (1단계)** | [`discord-channels-setup/SKILL.md`](discord-channels-setup/SKILL.md) | 11 STEP · 30~40분. Discord ↔ Claude 양방향 연결 + Gmail/Calendar Connector + 마케팅 MCP 결합 안내. Windows 사전 최적화 (STEP 0.5) 자동 분기 |
| ⭐ **활성화 (2단계)** | [`ai-assistant-build/SKILL.md`](ai-assistant-build/SKILL.md) | 8 STEP · 약 15분. 인벤토리 1회 스캔 → 운영 매뉴얼 (OPERATIONS.md) + 시스템 아키텍처 (AI-비서-아키텍처.md) 두 문서 동시 박제 + 첫 E2E 테스트 추천. channels-setup STEP 11 종료 후 자동 핸드오프. 이전 두 스킬 (discord-bot-operations-guide + ai-비서-구축) 통합본 |
| 운영 | 폰 DM "오늘 일정" 같은 자연어 | Claude 가 `reply`·`fetch_messages` 등 호출 |
| ⚠️ 폐기 | [`mcp설치-discord/SKILL.md`](mcp설치-discord/SKILL.md) | 구버전 서드파티 `mcp-discord` 노선. 참고용. |
| ⚠️ 폐기 | [`mcp설치-discord-하이브리드/SKILL.md`](mcp설치-discord-하이브리드/SKILL.md) | 구버전 두 봇 동시 운영. 참고용. |

본 MCP 는 **Part 10 AX 시스템의 양방향 진입점**. Part 8 CRM 의 `cs-responder`·Part 10 의 `daily-briefing`·`orchestrator` 가 본 채널로 통신.

## 사전 준비물

- Discord 무료 계정 + 본인 서버 1개 (없으면 2분 생성)
- **Bun 1.0+** · 터미널에서 `bun --version`
- **Claude Code v2.1.80+** · `claude --version`
- **claude.ai 로그인** (API Key 인증 불가)
- Discord Developer Portal 접근 (Bot Token 발급용)
- (Pro/Max 는 자동 가능 · Team/Enterprise 는 관리자가 `channelsEnabled` 활성화 필수)

## 작동 방식 (Channels 양방향 푸시)

```
[폰 Discord 앱에서 봇 DM]
   ↓
[Discord Gateway · WebSocket]
   ↓
[봇 계정 (사용자 서버에 초대된 봇 · marketing-ch)]
   ↓
[로컬 PC 의 claude --channels 세션 (Bun 프로세스)]
   ↓
[Claude 가 메시지 분석 + 도구 호출 (Gmail·Calendar·Sheets 등)]
   ↓
[reply 도구로 답신 → Discord Gateway → 폰 DM 도착]
```

⚠️ **세션이 종료되면 메시지가 도착하지 않음.** 항상 켜진 운영은 launchd / tmux 백그라운드 가동 필요 (Part 10 AX 시스템에서 다룸).

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `/plugin install` 실패 | 마켓 미등록 | `/plugin marketplace add anthropics/claude-plugins-official` 먼저 |
| Bun: command not found | Bun 미설치 | `curl -fsSL https://bun.sh/install \| bash` |
| 봇 Offline 표시 | `--channels` 플래그 누락 | 새 터미널 + `claude --channels plugin:discord@claude-plugins-official` |
| 페어링 코드 안 옴 | Channels 세션 꺼짐 또는 Message Content Intent OFF | 세션 + Developer Portal Intent 재확인 |
| `Channels disabled` 경고 | Team/Enterprise 인데 관리자 미활성화 | claude.ai Admin → Claude Code → Channels |
| reply 텍스트 안 보임 | 답신은 Discord 에 도착 (터미널엔 도구 호출만) | 폰/PC Discord 앱에서 확인 |
| 권한 프롬프트 일시중지 | 도구 권한 대기 | 채널 권한 릴레이로 폰 승인 또는 `--dangerously-skip-permissions` (신뢰 환경) |
| 첨부 25MB 초과 | 공식 제한 | 분할 또는 Google Drive 링크 |

자세한 트러블슈팅은 [`mcp설치-discord-channels/SKILL.md`](mcp설치-discord-channels/SKILL.md) 참조.

## 검증된 산출물

- 폰 DM "오늘 일정" → Calendar 조회 → 답신 (Gmail/Calendar 결합 시연)
- 폰 DM "CS 메일 분류" → Gmail search_threads → 4 카테고리 분류 → embed 답신
- 폰 DM "내일 14시 미팅 추가" → Calendar create_event → htmlLink 답신
- PDF 첨부 분석 → 요약 답신 (`download_attachment` + `reply`)
- 진행 상황 라이브 업데이트 (`edit_message` 5초마다)

## 다음

→ [`mcp설치-discord-channels/SKILL.md`](mcp설치-discord-channels/SKILL.md) (⭐ 본 클립 메인 스킬 · 4단계 흐름)
→ [`channels-setup.md`](channels-setup.md) (Phase 2 셋업 문서 · 신스킬에 흡수됨 · 참고용)
→ [`실습.md`](실습.md) (구버전 실습 · 현행 노선 갱신 예정)
→ Part 10 AX 시스템 (`cs-responder`·`daily-briefing`·`orchestrator`) — 본 채널 기반
