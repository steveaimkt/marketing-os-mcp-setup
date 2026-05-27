---
name: ai-assistant-build
description: |
  Discord ↔ Claude 연결이 끝난 직후 호출하는 AI 비서 활성화 통합 스킬. 28 에이전트 + 14 스킬 + 10 MCP 가 한 흐름으로 작동하는지 진단하고, 본인 환경 기준 발화 매뉴얼·시스템 아키텍처 문서 두 가지를 한 번에 박제한다.

  이전 두 스킬 (discord-bot-operations-guide + ai-비서-구축) 을 하나로 통합한 후속 노선. 인벤토리 스캔을 1회만 돌려 두 산출물을 동시 생성.

  자동 호출 트리거:
  - **"AI 비서 구축"** ⭐
  - **"마케팅 비서 시작"** ⭐
  - **"디스코드 봇 사용법"** ⭐
  - **"봇 운영 가이드"** ⭐
  - **"오케스트레이터 점검"** ⭐
  - **"채널 연결 후 뭐 해요"** ⭐
  - "비서 작동 확인" · "marketing-os 활성화" · "agent team check" · "AI 팀 점검"

  특이점:
  - **새 에이전트·MCP·스킬 만들지 않음** — 이미 적재된 자산 진단만
  - 산출물 3개:
    ① `~/.claude/channels/discord/OPERATIONS.md` (사용자 매뉴얼 — 발화 15~20개 + 응급 명령 + 호스팅)
    ② `agents/AI-비서-아키텍처.md` (시스템 아키텍처 — 7팀 매트릭스 + 라우팅 진단 + 한계)
    ③ (옵션) Notion 페이지 2개 미러링
  - 선행 권장: `discord-channels-setup` STEP 9 완료 (Discord ↔ Claude 양방향 검증)
  - Reactive only · Proactive cron 은 Part 10 AX 시스템에 위임
---

# AI 비서 활성화 (운영 매뉴얼 + 시스템 아키텍처 통합 진단)

> Discord 연결만 끝낸 직후 "그래서 폰에서 뭐라고 말해야 되나요?" + "이 시스템이 진짜 작동해요?" 두 침묵 구간을 한 번에 메우는 통합 진단 스킬.
>
> 인벤토리 1회 스캔 → 발화 매뉴얼 + 아키텍처 문서 동시 박제 → 첫 E2E 테스트 추천까지 15분.

---

## 🎬 시작 멘트

스킬이 호출되면 Claude 는 다음과 같이 출력 :

```
🤖 AI 비서 활성화 통합 진단을 시작합니다.

핵심 두 가지:
  ① 폰에서 봇에게 뭘 시킬 수 있는지 (사용자 매뉴얼)
  ② 시스템이 진짜 한 흐름으로 작동하는지 (아키텍처 진단)
  두 가지를 한 번에 점검하고 영구 문서로 박제.

────────────────────────────────

총 8 STEP · 약 15분.

  STEP 1  환경 헬스 체크 (자동 3분)
  STEP 2  오케스트레이터 카탈로그 검증 (자동 1분)
  STEP 3  자연어 라우팅 시뮬레이션 (대화 2~3분)
  STEP 4  AI-비서-아키텍처.md 박제 (자동 1분)
  STEP 5  OPERATIONS.md 박제 (자동 2분)
  STEP 6  봇 운영 카드 노출 (사용자 1분)
  STEP 7  Notion 페이지 미러링 (자동 1분 · 옵션)
  STEP 8  첫 E2E 테스트 추천 (사용자 선택)

선행 조건 (권장): discord-channels-setup STEP 9 (양방향 검증) 완료

시작할까요? (y / n)
```

---

## STEP 1 · 환경 헬스 체크 (자동 3분)

### 1-1. OS 감지

```bash
uname -s 2>/dev/null || echo "Windows"
```
→ Darwin / Linux / Windows. OPERATIONS.md 저장 경로 결정.

### 1-2. Discord 봇 정보 추출

| 항목 | 출처 |
|---|---|
| `.env` 경로 | macOS/Linux `~/.claude/channels/discord/.env` · Windows `%USERPROFILE%\.claude\channels\discord\.env` |
| 봇 이름 / Application ID | Developer Portal · 사용자 확인 |
| 페어링 계정 | `/discord:access list` 출력 |
| 정책 | `allowlist` / `pairing` / `groups` |

### 1-3. 에이전트 · 스킬 인벤토리

```bash
find agents -name "*.md" -type f | sort
find skills -name "SKILL.md" -type f | sort
```

기대: `agents/orchestrator.md` + 28 서브에이전트 / 14 스킬. 부족 시 빠진 폴더 표시.

### 1-4. MCP 활성 스캔

현재 세션 도구 prefix 로 :

| MCP | prefix | 활성? |
|---|---|---|
| Notion | `mcp__claude_ai_Notion__*` | ✅ / ❌ |
| Gmail | `mcp__claude_ai_Gmail__*` | ✅ / ❌ |
| Calendar | `mcp__claude_ai_Google_Calendar__*` | ✅ / ❌ |
| Sheets | `mcp__google-sheets__*` 또는 `mcp__google_sheets__*` | ✅ / ❌ |
| GA4 | `mcp__ga4__*` | ✅ / ❌ |
| Buffer | `mcp__buffer__*` | ✅ / ❌ |
| Meta Ads | `mcp__meta-ads__*` | ✅ / ❌ |
| Google Ads | `mcp__google-ads__*` | ✅ / ❌ |
| Firecrawl | `mcp__firecrawl__*` | ✅ / ❌ |
| YouTube | `mcp__youtube-data__*` | ✅ / ❌ |
| Higgsfield | `mcp__claude_ai_Higgsfield__*` | ✅ / ❌ |
| Figma | `mcp__claude_ai_Figma__*` 또는 `mcp__figma__*` | ✅ / ❌ |
| Discord Channels | plugin 로드 + `--channels` 모드 | ✅ / ❌ |

### STEP 1 종료 게이트

```
헬스 체크 결과:
  - OS                : macOS / Windows / Linux
  - 봇 이름           : {입력}
  - 페어링 계정       : @{handle}
  - 정책              : allowlist (안전)
  - 에이전트          : 28/28 (✅) 또는 X/28
  - 스킬              : 14/14
  - MCP               : N/12 (활성 목록)
  - Discord 봇 세션   : ✅ (Channels 모드) / ❌

⚠️ 미활성 MCP 가 있어도 진단은 계속 — 해당 MCP 쓰는 에이전트는 STEP 4~5 에서 비활성 표시.

STEP 2 진행할까요? (y / n)
```

---

## STEP 2 · 오케스트레이터 카탈로그 검증 (자동 1분)

### 2-1. orchestrator.md 라우팅 표 출력

`agents/orchestrator.md` 의 "30개 서브에이전트 카탈로그" 섹션 파싱 :

```
출력:
  Part 3 Content (2):
    · email-newsletter        → Gmail + Notion + skill(newsletter-writing)
    · content-publisher       → Buffer + Notion
  Part 4 Research (5):
    · trend-scanner           → Firecrawl + Notion
    · voc-analyzer            → ...
    ...
```

### 2-2. 갭 자동 감지

오케스트레이터 카탈로그 vs `agents/part{N}-*/` 폴더 비교 :

| 검출 케이스 | 의미 |
|---|---|
| 폴더 → 카탈로그 누락 | 라우팅 누락 (오케스트레이터가 호출 못 함) |
| 카탈로그 → 폴더 없음 | 카탈로그 오타 또는 미작성 |
| 발화 예시 0개 | 자연어 분기 불가 |

### STEP 2 종료 게이트

```
카탈로그 상태:
  - 행 수            : N개
  - 빠진 매핑        : M개
  - 발화 예시 평균   : K개/에이전트

STEP 3 (라우팅 시뮬레이션) 진행할까요? (y / n)
```

---

## STEP 3 · 자연어 라우팅 시뮬레이션 (대화 2~3분)

### 3-1. 5개 발화 추론

```
다음 발화 5개에 대해 어떤 에이전트가 호출될지 예측합니다:

  1. "어제 광고 ROAS 알려줘"
  2. "이번주 콘텐츠 캘린더 짜줘"
  3. "이 PDF 분석 후 노션에 저장"
  4. "지난 24시간 CS 메일 분류해줘"
  5. [본인이 던질 발화 1개]

진행할까요? (y / 발화 추가)
```

### 3-2. 추론 결과

각 발화마다 :

```
1. "어제 광고 ROAS 알려줘"
   → 3media-integrated-reporter  (확신도 85%)
   대안: meta-ads-analyzer (40%) / google-ads-analyzer (35%)
   근거: "ROAS" 단일 키워드 + 매체명 미명시 = 통합 리포트
   
2. "이번주 콘텐츠 캘린더 짜줘"
   → content-calendar  (확신도 95%)
   근거: 명시적 1:1 매핑
   
3. ...
```

### STEP 3 종료 게이트

```
질문 · 5개 중 라우팅이 명백히 틀린 케이스?

  none      → STEP 4 진행
  1~5 번호  → 해당 발화를 아키텍처.md 의 "갭" 으로 기록
  reroute   → 사용자가 정답 에이전트 지정 → orchestrator.md 보강 후보로 기록
```

---

## STEP 4 · `AI-비서-아키텍처.md` 박제 (자동 1분)

### 4-1. 저장 경로

`agents/AI-비서-아키텍처.md` (marketing-os 루트 상대).

### 4-2. 7 블록 본문 (Write 도구)

```markdown
# 마케팅 OS · AI 비서 아키텍처

작성일: {YYYY-MM-DD} · ai-assistant-build 스킬 자동 생성.

## 1. 한 줄 요약
1개 오케스트레이터가 10개 MCP 를 7개 도메인 팀 (28개 서브에이전트) 으로
분배해 관리. Discord 봇 DM 이 사용자 진입점.

## 2. 다이어그램
                    Discord 봇 DM
                          ↓
                    Orchestrator
                          ↓ (자연어 라우팅)
   ┌─────┬─────┬─────┼─────┬─────┬─────┐
 Part3 Part4 Part5 Part6 Part7 Part8 Part9
Content Research Copy  Ads  GA4  CRM  Strategy

## 3. 7 도메인 팀 매트릭스
| 팀 (폴더) | 에이전트 수 | 공유 MCP | 주력 스킬 |
| Part 3 Content (2) | email-newsletter · content-publisher | Gmail + Buffer + Notion | newsletter-writing |
| Part 4 Research (5) | trend-scanner · voc-analyzer · seo-keyword-research · competitor-monitor · ad-reference-collector | Firecrawl + Notion + YouTube | - |
| Part 5 Copy (5) | ad-copy-ab · brand-guidelines · content-calendar · landing-copy · quality-reviewer-6axis | Notion | brand-voice · ad-copy-ab · quality-review-6axis |
| Part 6 Ads (6) | meta · google · naver · 3media · ab-test · ad-performance-checker | Meta-Ads + Google-Ads + Webhook | html-report-template |
| Part 7 GA4 (3) | analyzer · html-report · notion-publisher | GA4 + Sheets + Notion | html-report-template |
| Part 8 CRM (3) | cs-responder · customer-data-unifier · ltv-analyzer | Gmail + Sheets + Notion | - |
| Part 9 Strategy (3) | strategy-report · marketing-calendar-builder · claude-design-prototype | Multi-MCP + Figma | - |

## 4. 진단 결과 (이 스킬 실행 시점)
- 활성 MCP        : {STEP 1 결과}
- 빠진 라우팅     : {STEP 2 결과}
- 라우팅 시뮬 갭  : {STEP 3 결과}

## 5. 한계 5가지
1. 각 Agent 호출 = 독립 컨텍스트 200K · 상태 공유는 Notion DB 경유
2. 병렬 N개 = N× 토큰 비용
3. 중첩 hop 마다 latency 5~15초 — 평탄 2계층 유지
4. 오케스트레이터 도구 가로채기 불가 — 승인 게이트는 서브에이전트 내장
5. 무인 cron 발송은 Channels 단독 불가 — Discord Webhook + launchd (Part 10)

## 6. 검증 절차 (다음 단계)
- E2E Test 1: email-newsletter 발송 한 통 (단순)
- E2E Test 2: daily-briefing 조합 호출 (Calendar + Gmail + Ads)
- E2E Test 3: Part 10 cron 등록 (무인 가동)

## 7. 보강 권장 (이 스킬이 찾아낸 갭)
{STEP 2~3 의 갭 자동 박제}
```

### STEP 4 종료 게이트

```
박제 완료: agents/AI-비서-아키텍처.md
다음 STEP 5 (OPERATIONS.md 박제) 진행. (y / open)
```

---

## STEP 5 · `OPERATIONS.md` 박제 (자동 2분)

### 5-1. 저장 경로

| OS | 경로 |
|---|---|
| macOS / Linux | `~/.claude/channels/discord/OPERATIONS.md` |
| Windows | `%USERPROFILE%\.claude\channels\discord\OPERATIONS.md` |

⚠️ Windows OneDrive 동기화 폴더 안이면 잠금 위험 — channels-setup STEP 0.5-3 으로 백업 해제 권장.

### 5-2. 7 블록 본문 (Write 도구)

```markdown
# Discord 봇 운영 매뉴얼 · {봇 이름}

작성일: {YYYY-MM-DD} · 본인 환경 기준 동적 생성.

## 1. 봇 호출 시작
폰 Discord 앱 → 본인 서버 → 멤버 리스트 봇 클릭 → 'Message'.
⚠️ PC Channels 세션이 켜져 있어야 작동:
   claude --channels plugin:discord@claude-plugins-official

## 2. 자주 쓰는 발화 (본인 활성 MCP 기준)
   [5-3 큐레이션 규칙으로 동적 생성]

## 3. 권한 승인 흐름 (위험 작업)
   위험 작업 시 봇이 권한 프롬프트 DM 발송 → 본인 답신:
     ✅ "yes" / "approve"   → 진행
     ❌ "no"  / "deny"      → 중단
   30초 무응답 → 자동 거부

## 4. 봇이 답 안 할 때 (3분 진단)
   봇 오프라인 (회색)   → PC 세션 종료     → 새 터미널 + claude --channels ...
   봇 온라인 + 무응답   → 페어링 풀림      → /discord:access list → pair <코드>
   페어링 코드 안 옴    → Intent OFF       → Developer Portal Bot → Intent ON + 세션 재시작

## 5. 응급 명령 카드 (PC)
   /discord:access list                — 페어링 계정 확인
   /discord:access pair <코드>         — 재페어링
   /discord:access policy allowlist    — 정책 확인
   /discord:configure <new-token>      — 토큰 재발급 후 등록
   토큰 재발급: https://discord.com/developers/applications

   봇 정보:
     이름           : {봇 이름}
     Application ID : {ID}
     .env 경로      : {OS 별 경로}

## 6. 호스팅 옵션 (노트북 닫으면 봇이 죽는 문제)
   1. caffeinate -dis     · 0원 · macOS 외부 전원
   2. 데스크톱 24h         · 0원 · 책상 PC ⭐ 권장 1
   3. Mac mini 홈서버      · 600~1,400$ · 본격 ⭐ 권장 2
   4. Raspberry Pi 5       · 80~150$
   5. Linux VPS            · 월 6~12$ · OAuth 어려움
   자세한 launchd / tmux 는 Part 10 AX 시스템.

## 7. 다음 단계
   매뉴얼 정상 작동하면:
     → curriculum/part03-콘텐츠파이프라인/01-email-newsletter/실습.md
   추가 MCP 필요하면:
     → "X MCP 설치하자" (개별) 또는 "MCP 전체 설치하자"
```

### 5-3. 발화 큐레이션 규칙 (활성 MCP 기준)

| 활성 MCP | 카테고리 | 발화 예시 (3개) |
|---|---|---|
| 항상 | 일반 채팅 | "지금 작업 중인 디렉토리?" · "마지막 작업 요약" · "오늘 한 일 정리" |
| Gmail | 메일 운영 | "지난 24시간 CS 메일 분류" · "VIP 라벨 3개 요약" · "이 메일 답신 초안" |
| Calendar | 일정 운영 | "오늘 일정" · "내일 14시 미팅 추가" · "이번주 비는 시간" |
| Sheets | 시트 조회 | "어제 매출 시트 핵심 3가지" · "광고 시트 평균 ROAS" |
| GA4 | 트래픽 | "어제 트래픽·전환·이탈률" · "지난주 톱 채널" · "이번 캠페인 페이지뷰" |
| Notion | 저장·검색 | "이 답변 노션 저장" · "콘텐츠 캘린더 이번주" · "VoC 페이지 검색" |
| Buffer | SNS 예약 | "이 글 5채널 예약" · "내일 09시 인스타 게시" |
| Meta + Google Ads | 광고 점검 | "어제 ROAS" · "오늘 알람 광고" · "Top 3 키워드 CPC" |
| Firecrawl | 경쟁사 | "이 사이트 신상품 알려줘" · "경쟁사 가격 비교" |
| YouTube | KPI | "지난주 유튜브 KPI" · "조회수 톱 3 영상" |
| Higgsfield | 이미지 | "오늘 광고 이미지 1장" |
| Figma | 디자인 | "현재 Figma 페이지 톤 일관성 체크" |

⚠️ 미활성 MCP 카테고리는 본문에서 제외 → 매뉴얼 끝 "다음에 추가할 만한 발화 5개" 섹션으로 후크.

### STEP 5 종료 게이트

```
박제 완료: OPERATIONS.md (절대경로 출력)
  - 발화 템플릿     : N 개 (활성 MCP 기준)
  - 응급 명령 카드  : 박제
  - 봇 정보         : 박제
  - 호스팅 옵션 5종  : 박제

STEP 6 (봇 운영 카드 노출) 진행. (y)
```

---

## STEP 6 · 봇 운영 카드 노출 (사용자 1분)

⚠️ Channels 구조상 봇이 **먼저 DM 못 보냄** (`reply` 는 수신 후만).
→ 본인이 폰에서 한 줄 발화 → 봇이 운영 카드로 응답하는 트릭.

### 6-1. 폰에서 한 줄 발화
```
📱 폰 Discord 봇 DM 으로 정확히 :

   "운영 가이드 보여줘"
```

### 6-2. 봇 응답
PC Claude 가 위 발화 감지 시 OPERATIONS.md 의 1~3 블록을 발화 5~7개로 압축해 `reply`:

```
🤖 Discord 봇 운영 카드

📧 메일 (Gmail)
  · "지난 24시간 CS 메일 분류"
  · "어제 받은 메일 3개 요약"

📅 일정 (Calendar)
  · "오늘 일정"
  · "내일 14시 미팅 추가"

📊 광고 (Meta+Google Ads)
  · "어제 ROAS"

⚠️ 위험 작업 시 ✅/❌ 답신으로 승인.
전체 매뉴얼: ~/.claude/channels/discord/OPERATIONS.md
```

(활성 MCP 에 따라 카테고리 동적 추가/제외)

### STEP 6 종료 게이트
```
질문 · 폰에서 "운영 가이드 보여줘" → 봇이 운영 카드 응답?

답변 (y / n / no-response) :
```

`n` / `no-response` → channels-setup STEP 7 (--channels 모드) + STEP 8 (페어링) 재확인.

---

## STEP 7 · Notion 페이지 미러링 (자동 1분 · 옵션)

### 7-1. 사전 조건
`mcp__claude_ai_Notion__*` 활성. 미활성 → 건너뜀.

### 7-2. 2개 페이지 자동 생성
- `마케팅 OS · Discord 봇 운영 매뉴얼` (OPERATIONS.md 미러)
- `마케팅 OS · AI 비서 아키텍처` (AI-비서-아키텍처.md 미러)
- 도구: `mcp__claude_ai_Notion__notion-create-pages`
- 위치: 워크스페이스 루트 또는 "Marketing OS" 페이지 하위

### 7-3. 폰 활용
폰 Notion 앱 → 두 페이지 모두 열람 가능. 외출 중에도 발화 템플릿 + 아키텍처 확인.

### STEP 7 종료 게이트
```
Notion 페이지 2개 생성 완료 (또는 건너뜀)?
답변 (y / skip / error) :
```

---

## STEP 8 · 첫 E2E 테스트 추천 (사용자 선택)

### 8-1. 3개 후보

| 추천 | 에이전트 | 의존 MCP | 난이도 | 학습 가치 |
|---|---|---|---|---|
| **A (입문)** ⭐ | `email-newsletter` | Gmail + Notion | 낮음 | 첫 에이전트 6 블록 패턴 |
| **B (조합)** | `daily-briefing` (commands/) | Calendar + Gmail + Ads | 중간 | 멀티 에이전트 라우팅 |
| **C (광고)** | `analyze-meta` 또는 `check-ads` | Meta-Ads + Notion + Webhook | 중간 | 광고 임계치 알림 |

### 8-2. 발화

```
A. "1-1 email-newsletter 실습 시작하자"
B. "오늘 데일리 브리핑 보여줘"
C. "어제 메타 광고 ROAS 알려줘"

선호 (A / B / C / 사용자 정의) :
```

### STEP 8 종료 게이트

```
🎉 AI 비서 활성화 진단 완료.

박제된 결과 :
  ① OPERATIONS.md                    (사용자 매뉴얼)
  ② agents/AI-비서-아키텍처.md       (시스템 아키텍처)
  ③ (옵션) Notion 페이지 2개
  ④ (옵션) orchestrator.md 보강 후보

다음 : 위 A/B/C 중 선택 발화 → 해당 에이전트 가동.

본 스킬은 언제든 재호출 가능 ("AI 비서 점검") — 자산 변경되면 재진단.
```

---

## 🛠 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| STEP 1 에이전트 0개 | `marketing-os/` 루트 외에서 실행 | `cd marketing-os/` 후 `claude --channels ...` 재시작 |
| STEP 1 MCP 0/12 | `.mcp.json` 미로드 / 권한 거부 | `claude --mcp-config .mcp.json --channels ...` 또는 `/mcp` 재인증 |
| STEP 2 카탈로그 vs 폴더 불일치 | 오케스트레이터 수동 편집 | 갭 리스트를 STEP 4 박제 후 `orchestrator.md` 수동 보강 |
| STEP 3 라우팅 추론 매번 다름 | 발화 키워드 부족 | 박제 문서에 "결정적 키워드" 룰 추가 |
| OPERATIONS.md 쓰기 실패 (Windows) | OneDrive 동기화 | channels-setup STEP 0.5-3 백업 해제 |
| AI-비서-아키텍처.md 쓰기 실패 (Windows) | 동일 | 동일 |
| STEP 6 폰 발화 무응답 | 페어링 풀림 / 세션 종료 | `/discord:access list` → `/discord:access pair <코드>` |
| Notion 페이지 생성 실패 | 통합에 워크스페이스 미연결 | claude.ai → Connectors → Notion → workspace 권한 추가 |
| 발화 템플릿 5개 미만 | 활성 MCP 1~2개뿐 | `mcp설치-전체` 추가 후 본 스킬 재호출 |
| 한국어 발화에 봇이 영어 답변 | 시스템 프롬프트 언어 미고정 | OPERATIONS.md 1번 블록에 "답신은 한국어로" 추가 |

---

## 📂 강의 연결

- **선행 스킬**: [`../discord-channels-setup/SKILL.md`](../discord-channels-setup/SKILL.md) STEP 0~11 완료
- **호출 시점**: channels-setup STEP 11 종료 게이트에서 본 스킬로 자동 핸드오프
- **후속 단계**:
  - Part 3 `email-newsletter` E2E (가장 추천)
  - Part 10 AX 시스템 (Webhook + cron 무인 가동)
- **재호출 트리거**: 자산 변경 후 "AI 비서 점검" 발화로 재진단
- **심볼릭 링크 권장**: `~/.claude/skills/ai-assistant-build` → 본 폴더
- **흡수한 이전 스킬**:
  - `discord-bot-operations-guide` (운영 매뉴얼 영역) — 2026-05-27 통합
  - `ai-비서-구축` (아키텍처 진단 영역) — 2026-05-27 통합
