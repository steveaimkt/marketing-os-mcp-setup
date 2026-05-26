# Claude Code Channels (Discord) 셋업 가이드 — Phase 2 응용

> **위치** : Part 2 / Clip 4-2 (Discord MCP) 의 **Phase 2 응용 셋업**
> **목적** : 외부 Discord 메시지를 **실행 중인 Claude Code 세션으로 푸시** 받아 양방향 대화·반응 처리
> **선행 조건** : Phase 1 (mcp-discord) 설치 완료 권장 (없어도 진행 가능)
> **소요 시간** : 약 10~15분 (Bot B 새로 만들기 + 페어링)
> **비용** : 무료
> **중요** : Anthropic **Research Preview** 단계 · Claude Code v2.1.80+ · claude.ai 로그인 필수

---

## Phase 1 vs Phase 2 차이 (한 줄)

| Phase | 패키지 | 본질 |
|---|---|---|
| **Phase 1 (필수)** | `mcp-discord` (npm) | Claude 가 Discord 로 **발송** · cron 무인 자동화 |
| **Phase 2 (응용)** | `discord@claude-plugins-official` (Anthropic 공식 플러그인) | Discord 가 Claude 세션으로 **푸시** · 양방향 채팅 브리지 |

두 봇을 **같은 Discord 서버에서 동시 가동** (토큰 분리). 무인 자동화는 Phase 1, 출장 중 폰으로 Claude 호출은 Phase 2.

---

## 사전 조건

- Claude Code v2.1.80 이상 (Pro / Max / Enterprise 계정)
- claude.ai 로그인 (API Key 인증으로는 작동 안 함)
- Discord 무료 계정 + 본인 서버 1개 (Phase 1 과 같은 서버 사용 권장)
- **Bun** 설치 필수 (Channels 플러그인이 Bun 스크립트) — `bun --version` 확인, 없으면 https://bun.sh/docs/installation

---

## STEP 1 — 새 Discord Bot 만들기 (Bot B · 채팅 전용 · 약 5분)

> ⚠️ Phase 1 의 Bot A 와 **다른 새 봇** 으로 생성. 토큰 분리해야 두 봇이 동일 서버에서 충돌 없이 가동.

1. https://discord.com/developers/applications 접속 → **New Application** → 이름 예 : `Claude Channels Bot`
2. 왼쪽 **Bot** 탭 → username 설정 → **Reset Token** → 토큰 복사 (1회만 표시 · 안전한 곳에 보관)
3. **Privileged Gateway Intents** 섹션 → **Message Content Intent** 활성화 ⭐ 필수
4. **OAuth2 → URL Generator**
   - Scopes : `bot`
   - Bot Permissions :
     - View Channels
     - Send Messages
     - Send Messages in Threads
     - Read Message History
     - Attach Files
     - Add Reactions
5. 생성된 URL 복사 → 브라우저로 열기 → Phase 1 과 같은 서버 선택 → **Authorize**
6. 서버에서 Bot B 가 추가됐는지 확인

---

## STEP 2 — Channels 플러그인 설치 (Claude Code 안에서)

Claude Code 세션 열기 후 슬래시 명령으로 :

```
/plugin install discord@claude-plugins-official
```

**플러그인 마켓플레이스가 없다고 나오면** :

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install discord@claude-plugins-official
```

설치 후 :

```
/reload-plugins
```

→ `/discord:configure`, `/discord:access` 같은 슬래시 명령이 활성화됨.

---

## STEP 3 — 토큰 등록

STEP 1 에서 복사한 Bot B 토큰으로 :

```
/discord:configure <Bot-B-Token>
```

→ `~/.claude/channels/discord/.env` 에 자동 저장.

> 💡 셸 환경 변수 `DISCORD_BOT_TOKEN` 으로 설정해도 됨 (Claude Code 시작 전에 export).

---

## STEP 4 — Channels 활성화된 상태로 Claude Code 재시작

기존 Claude Code 세션 종료 → 새 터미널에서 :

```bash
claude --channels plugin:discord@claude-plugins-official
```

→ Bot B 가 Discord 에서 온라인으로 표시 + Claude Code 세션이 메시지 수신 대기.

> 💡 `--channels` 에 여러 플러그인 공백으로 나열 가능 (예: telegram + discord).

---

## STEP 5 — 봇 페어링 (본인 계정만 허용)

1. Discord 앱에서 Bot B 찾기 → **DM 보내기** (예: "hi")
2. 봇이 페어링 코드로 회신 (예: `ABCD-1234`)
3. Claude Code 세션으로 돌아가서 :

```
/discord:access pair ABCD-1234
```

4. 본인 Discord 계정이 허용목록에 자동 추가
5. 본인만 메시지 보낼 수 있도록 잠그기 :

```
/discord:access policy allowlist
```

> ⚠️ 페어링하지 않은 사람의 메시지는 자동 폐기됨 (보안)

---

## STEP 6 — 양방향 대화 검증

폰의 Discord 앱에서 Bot B 에게 DM :

```
지금 작업 중인 파일 뭐야?
```

→ Claude Code 세션에 `<channel source="discord">` 이벤트 도착 → Claude 가 현재 작업 디렉토리 분석 후 reply 도구 호출 → Discord DM 으로 답변.

> 💡 터미널에는 도구 호출과 "전송됨" 만 표시. 실제 답신 텍스트는 Discord 에 나타남.

---

## 두 봇 충돌 방지 체크리스트

같은 서버에 Bot A (mcp-discord) + Bot B (Channels) 동시 가동 시 :

- [ ] **봇 이름 다르게** (예: `marketing-os` / `Claude-Chat`)
- [ ] **토큰 다른 .env 위치** :
  - Bot A → `marketing-os/.env` (`DISCORD_BOT_TOKEN`)
  - Bot B → `~/.claude/channels/discord/.env` (Channels 자동 관리)
- [ ] **권한 분리** (선택)
  - Bot A : 모든 채널 발송·reaction
  - Bot B : DM 위주 (또는 특정 채널)
- [ ] **활성화 트리거 분리**
  - Bot A : `marketing-os` 디렉토리에서 일반 `claude` 명령
  - Bot B : 별도 터미널에서 `claude --channels plugin:discord@...`

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `/plugin install` 실패 | 마켓플레이스 등록 안 됨 | `/plugin marketplace add anthropics/claude-plugins-official` 먼저 |
| Bot B 가 페어링 코드 응답 안 함 | `--channels` 플래그 없이 Claude 시작 | Claude Code 재시작 시 `--channels plugin:discord@...` 추가 |
| `bun: command not found` | Bun 미설치 | `curl -fsSL https://bun.sh/install \| bash` |
| 권한 거부 (메시지 발송) | Message Content Intent 비활성 | Discord Developer Portal → Bot → Privileged Gateway Intents 토글 ON |
| Channels 비활성화 안내 | Team/Enterprise 관리자 차단 | claude.ai → Admin Settings → Claude Code → Channels 활성화 |
| `API Key 인증으로 작동 안 함` | claude.ai 로그인 아님 | `claude login` 으로 claude.ai 계정 인증 |

---

## 보안 주의

- Bot B 토큰은 **본인 PC 의 ~/.claude/channels/discord/.env** 에만 저장. git commit 금지
- `--channels` 활성화된 세션에서는 페어링된 발신자가 **권한 프롬프트 승인·거부 가능** (도구 사용 허용 게이트)
- 신뢰하는 본인 계정만 허용목록에 추가. 팀원 추가는 `/discord:access allow @user` 신중히
- 토큰 노출 시 Discord Developer Portal → Bot → Reset Token 으로 재발급 + `/discord:configure` 재실행

---

## 활용 시나리오 (Phase 1 + Phase 2 하이브리드)

| 시나리오 | 담당 봇 | 흐름 |
|---|---|---|
| 매주 월요일 09:00 광고 리포트 자동 발송 | Bot A (Phase 1) | cron → mcp-discord `send_message` → #marketing 채널 |
| 광고 임계치 위반 알림 + 승인 reaction 대기 | Bot A (Phase 1) | 에이전트 자동 발송 → ✅ reaction 폴링 → 집행 |
| 출장 중 폰에서 "어제 광고 어땠어?" 물어보기 | Bot B (Phase 2) | DM → Claude 세션 푸시 → 분석 → DM 답신 |
| 외부 시스템 (CI 빌드 실패) 알림 → Claude 가 자동 디버그 | Bot B (Phase 2) | 웹훅 → Bot B 채널 → 세션 도착 → 작업 |
| Discord 채널 모니터링 + 실시간 응답 | Bot B (Phase 2) | 멘션 도착 → Claude 분석 → 답변 |

## 다음 단계

- 본 셋업 완료 후 → 일반 `claude` 명령은 mcp-discord (Bot A) 가동 / `claude --channels plugin:discord@...` 명령은 Channels (Bot B) 가동
- Part 10 AX 협업 클립에서 두 봇 통합 운영 시연 가능
