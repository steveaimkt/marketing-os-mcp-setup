---
name: bot-build
description: |
  Discord Channels 연결된 봇을 **"내 업무 비서"** 로 발전시키는 인터랙티브 설계 스킬. 3 질문 (페르소나·업무·권한) → 봇 페르소나 카드 + 우선 가동 에이전트 3개 + 승인 정책 + 필요 MCP 매트릭스 + 비서 구축 문서 (Markdown) 자동 도출.

  자동 호출 트리거:
  - **"나만의 봇 구축을 시작하자"** ⭐ 주요 트리거
  - **"내 봇 구축"** / **"내 봇 만들기"** ⭐
  - **"AI 비서 구축"** / **"마케팅 비서 시작"** ⭐ (구 ai-assistant-build 흡수)
  - **"디스코드 봇 사용법"** / **"봇 운영 가이드"** ⭐
  - "클로드 비서 설계" · "디스코드 봇 비서 만들기"
  - "봇 페르소나 정하기" · "내 비서 설계 시작"
  - "오케스트레이터 점검" · "AI 팀 점검" · "채널 연결 후 뭐 해요"

  특이점:
  - **선행**: Discord Channels 셋업 완료 (`discord-channels-setup` 스킬)
  - **답변 시간**: 약 5분 · **자동 진단 + 문서 생성**: 약 5분
  - **산출물 (필수)**:
    ① `marketing-os/outputs/{YYYY-MM-DD}/bot-design/{date}-my-bot-spec.md` (페르소나·에이전트·정책·라우팅)
    ② `~/.claude/channels/discord/OPERATIONS.md` (봇 발화 매뉴얼 15~20개 + 응급 명령)
  - **산출물 (옵션)**:
    ③ `marketing-os/agents/AI-비서-아키텍처.md` (시스템 7 도메인 팀 매트릭스 + 진단)
    ④ Notion 페이지 미러링 (Notion MCP 활성 시)
  - **이전 통합**: `ai-assistant-build` 스킬 (자동 인벤토리 진단 + 매뉴얼 박제) 흡수
  - 답변 → marketing-os 의 기존 에이전트와 자동 매칭 (daily-briefing · check-ads · cs-responder · weekly-newsletter 등)
  - 미설치 MCP 가 있으면 `mcp설치` 또는 `mcp설치-전체` 스킬 호출 안내
  - **채널별 봇 기능 분리 (선택)**: Q4 응답 시 채널 ID 별 라우팅 표 + `CLAUDE.md` 자동 패치 (소프트 라우팅)
---

# 내 봇 구축 (Discord Channels 비서 설계)

> Discord ↔ Claude 가 연결된 봇을 **내 업무 비서** 로 발전시키는 설계 스킬. 3 질문 답하면 페르소나 + 가동 에이전트 + 승인 정책 + MCP 매트릭스 자동 도출 → 비서 구축 문서 (Markdown) 생성.

---

## 🎬 시작 멘트

스킬이 호출되면 Claude 는 다음과 같이 출력 :

```
🤖 나만의 봇 구축을 시작합니다.

지금 상태:
  ✅ Discord ↔ Claude 양방향 연결 (--channels 세션 가동 중인지 자동 점검)
  ✅ access 정책 잠금 (allowlist · 본인만)
  ⚙️ 다음 단계 = 비서 페르소나 + 업무 + 권한 결정

총 4 질문 · 약 15분 (Q4 는 선택 · 자동 진단 포함).

5단계 흐름 (총 20~30분 · 프리셋 선택 시 10분):

  📋 PHASE 1 · 봇 기획 (Plan)
     사전 점검 + 인벤토리 자동 스캔 (봇·에이전트·MCP·스킬)

  💡 PHASE 2 · 봇 제안 (Propose)
     A. 📊 마케팅 데일리 매니저 (가장 보편적 · 추천 ⭐)
     B. 🚨 광고 옵저버 (광고 운용자 전용)
     C. ✍️ 콘텐츠 큐레이터 (콘텐츠 제작자 전용)
     D. 🎨 자유 설계 (Q1~Q4 직접 답변)

     ⭐ 공통 기본 기능: 매일 아침 07:00 알림 (프리셋 A/B/C 모두 기본 탑재 · D 도 권장 디폴트)

  🔌 PHASE 3 · MCP & 기능 안내 (Inform)
     선택된 봇의 필요 MCP 매트릭스 + 미설치 MCP 안내 + 도구별 권한 매핑

  ⚙️ PHASE 4 · 봇 설치 (Install)
     • my-bot-spec.md · OPERATIONS.md · 아키텍처.md 박제
     • CLAUDE.md 라우팅 패치 + .claude/settings.json 권한 패치
     • launchd plist 자동 등록 (매일·매주 자동화)
     • cron 등록 (즉시 알림 폴링)

  📡 PHASE 5 · 디스코드 채널 연동 (Connect)
     • 필요 채널 목록 안내 + 생성 가이드
     • access.json 의 groups 자동 패치 (채널 ID)
     • 첫 가동 검증 (폰 DM + 채널 멘션)
     • 사용 시작 안내 (OPERATIONS.md)

시작할까요? (y / n)
```

사용자 `y` → STEP 0 진행.

---

## STEP 0 · 사전 점검 (자동 10초)

Claude 가 다음 항목을 자동 확인 :

```bash
# 1. Discord Channels 봇 활성 여부
ls ~/.claude/channels/discord/.env       # 토큰 존재
cat ~/.claude/channels/discord/access.json | grep dmPolicy   # 정책 확인
ps aux | grep "claude --channels" | grep -v grep             # 세션 가동

# 2. 현재 세션의 핵심 MCP 활성 여부 (도구 prefix 노출 체크)
mcp__claude_ai_Gmail__*
mcp__claude_ai_Google_Calendar__*
mcp__claude_ai_Notion__*
mcp__ga4__*
mcp__meta-ads__*
mcp__google-ads__*
mcp__google-sheets__*
mcp__youtube-data__*
mcp__buffer__*
mcp__firecrawl__*
```

게이트 :
```
사전 점검 결과:
  - Discord Channels 봇       : ✅ 가동 중 / ⚠️ 셋업 필요
  - access 정책 (allowlist)   : ✅ / ⚠️
  - 활성 MCP                  : N 개 (gmail · calendar · ads · ...)

✅ 모두 OK → 질문 시작 (y)
⚠️ Discord 셋업 부족 → 먼저 `discord-channels-setup` 스킬 호출 (n)
```

---

## STEP 0.5 · 자동 인벤토리 스캔 (자동 1분)

(구 `ai-assistant-build` STEP 1~2 흡수 · 사용자 입력 없음)

Claude 가 5가지를 자동 스캔하고 표로 출력 :

### 스캔 대상

1. **OS / 셸 / 작업 디렉토리** — 산출물 저장 경로 결정
2. **Discord 봇 상태** :
   - `.env` 토큰 존재 (값 노출 X · 길이만 체크)
   - `access.json` 의 정책 (`allowlist` / `pairing`)
   - 페어링 계정 ID + 그룹 채널 ID
3. **에이전트 인벤토리** : `find marketing-os/agents -name "*.md" | wc -l` (기대 28)
4. **스킬 인벤토리** : `find marketing-os/skills -name "SKILL.md" | wc -l` + `~/.claude/skills/` (기대 14)
5. **MCP 활성 매트릭스** : 현재 세션의 도구 prefix 노출 자동 검사

### 출력 (사용자에게 표 형태)

```
인벤토리 스캔 결과:

  ✅ Discord 봇        : marketing-ch (allowlist · 페어링 1명 · 그룹 채널 2)
  ✅ 에이전트          : 28 / 28
  ⚠️ 스킬              : 12 / 14 (mcp설치-figma, mcp설치-buffer 누락)
  ✅ 활성 MCP          : 16 종 (Gmail · Calendar · Notion · GA4 · ads · sheets · firecrawl ...)

이 데이터 기반으로 Q1~Q4 답변을 분석하고 산출물을 박제합니다.

계속 (y), 인벤토리 만 박제 (skip → STEP 5.5 박제로 점프) :
```

`skip` → Q1~Q4 건너뛰고 인벤토리 기반 OPERATIONS.md + 아키텍처.md 만 박제 (구 `ai-assistant-build` 와 동일 결과).

---

## STEP 0.7 · 진입 분기 (프리셋 3개 vs 자유 설계)

⚠️ **잘 모르겠으면 프리셋 추천** — 3개 사전 정의된 비서 중 하나 선택 시 Q1~Q4 자동 채움 → STEP 4 종합 분석으로 즉시 점프 (5분 완료).

```
──────────────────────────────────────────

진입 방식 선택:

  A. 📊 마케팅 데일리 매니저 (가장 보편적 · 추천 ⭐)
     ▸ 매일 07시 통합 브리핑 (광고 + 매출 + CS + 일정)
     ▸ 매주 월 07시 종합 리포트
     ▸ 즉시 알림: ROAS < 2.0 임계치
     ▸ 활용 MCP: ads + sheets + gmail + calendar
     ▸ 적합: 1인 마케터 · 종합 관리 필요

  B. 🚨 광고 옵저버 (광고 운용자 전용)
     ▸ 매일 07시 3매체 ROAS · 캠페인 성과
     ▸ 매주 월 07시 통합 광고 리포트
     ▸ 즉시 알림: ROAS < 2.0 또는 -30% 급락
     ▸ 활용 MCP: meta-ads + google-ads + naver-ads
     ▸ 적합: 광고비 月 300만원+ 운용자

  C. ✍️ 콘텐츠 큐레이터 (콘텐츠 제작자 전용)
     ▸ 매일 07시 트렌드 모니터링 (네이버·구글)
     ▸ 매주 월 07시 뉴스레터 작성 (Gmail Draft)
     ▸ 즉시 알림: 경쟁사 사이트/SNS 변경
     ▸ 활용 MCP: firecrawl + gmail + notion + buffer
     ▸ 적합: 뉴스레터·블로그·SNS 운영자

  D. 🎨 자유 설계 (Q1~Q4 직접 답변)
     ▸ 페르소나·업무·권한·라우팅 본인이 결정
     ▸ 소요 15분

답변 (A / B / C / D) :
──────────────────────────────────────────
```

### 프리셋별 자동 채움 값

#### 📊 프리셋 A · 마케팅 데일리 매니저

| 항목 | 값 |
|---|---|
| **Q1 페르소나** | 단일 사용자 · 부하직원 보고형 · 한국어 + 영문 데이터 · 5줄 이내 |
| **Q2 매일** | `daily-briefing` · 매일 07:00 · 광고 + 매출 + CS + 일정 통합 |
| **Q2 매주** | `weekly-report` · 매주 월 07:00 · GA4 + 3매체 광고 + LTV |
| **Q2 즉시** | `check-ads` · 매시간 cron · ROAS < 2.0 시 디스코드 푸시 |
| **Q3 자동 OK** | 조회·분석 (list/get/search/read 패턴) |
| **Q3 승인 필요** | 메일 발송·SNS 게시·일정 생성 |
| **Q3 금지** | 광고 예산 변경·캠페인 일시중지 |
| **Q4 채널** | 옵션 A (DM 통합) |

#### 🚨 프리셋 B · 광고 옵저버

| 항목 | 값 |
|---|---|
| **Q1 페르소나** | 광고 운용자 · 데이터 보고형 (간결·숫자) · 한국어 + 영문 캠페인명 · 3줄 + 표 |
| **Q2 매일** | `analyze-meta` + `analyze-google-ads` + `analyze-naver-ads` · 매일 07:00 |
| **Q2 매주** | `integrated-ad-report` · 매주 월 07:00 · 3매체 통합 + HTML 리포트 |
| **Q2 즉시** | `check-ads` · 매시간 cron · ROAS < 2.0 또는 -30% 급락 |
| **Q3 자동 OK** | 광고 조회·분석·인사이트 |
| **Q3 승인 필요** | 광고 콘셉트 변경·A/B 테스트 시작 |
| **Q3 금지** | 예산 변경·캠페인 일시중지·삭제 |
| **Q4 채널** | 옵션 B (#광고 채널 전용 + DM 백업) |

#### ✍️ 프리셋 C · 콘텐츠 큐레이터

| 항목 | 값 |
|---|---|
| **Q1 페르소나** | 콘텐츠 제작자 · 친근한 어시스턴트 (브랜드 보이스 적용) · 한국어 · 본문은 길게 |
| **Q2 매일** | `research-trend` · 매일 07:00 · 네이버·구글 트렌드 키워드 |
| **Q2 매주** | `email-newsletter` + `send-newsletter` · 매주 월 07:00 · Gmail Draft → 승인 → 발송 |
| **Q2 즉시** | `research-competitor` · 매일 06:00 · 경쟁사 사이트/SNS 변경 감지 |
| **Q3 자동 OK** | 트렌드 조회·콘텐츠 Draft 작성 |
| **Q3 승인 필요** | 발송·SNS 게시·노션 페이지 생성 |
| **Q3 금지** | 브랜드 보이스 변경·삭제 |
| **Q4 채널** | 옵션 B (#콘텐츠 채널 전용 + DM 백업) |

### 분기 결과

- **A / B / C 선택** → 위 값으로 자동 채움 → **STEP 4 (종합 분석) 점프** → STEP 5/5.5 산출물 박제
- **D 선택** → STEP 1 (Q1 페르소나) 부터 자유 설계 진행

게이트 :
```
프리셋 A/B/C 선택했나요? 또는 D 자유 설계?

답변 (A / B / C / D) :
```

---

## STEP 1 · Q1 · 봇 페르소나 (사용자 1분)

```
──────────────────────────────────────────

Q1. 봇은 누구의 비서이고, 말투는 어떻게?

  (예시) 나 한 명. 부하직원 톤으로 짧게 보고. 한국어.

  내 답:

──────────────────────────────────────────
```

### Claude 의 분석 (답변 받은 후 자동)

답변에서 5가지 자동 추출 :

| 항목 | 추출 방식 | 예 |
|---|---|---|
| **비서 대상** | "나 한 명" → 단일 / "팀" / "가족" | single-user |
| **톤** | 격식 · 부하직원 · 친구 · 어시스턴트 | subordinate |
| **언어** | 한국어 · 영어 · 혼용 | ko |
| **길이 기본값** | "짧게" → 3~5줄 · "자세히" → 10줄+ | short (3~5L) |
| **강조 표현** | 이모지·표·줄바꿈 사용 빈도 | 절제 (✅/⚠️/🚨 만) |

답변이 추상적이면 한 번 되묻기 :
```
조금 더 구체적으로 알려주세요:
  - "본인" 외에 자동 추가될 사람 있나요? (e.g. 마케팅팀)
  - 톤 예시: "사장님 잠시만요" 같은 격식 vs "오늘 ROAS 3.2" 같은 보고형 — 어느 쪽?
```

게이트 :
```
Q1 분석 결과:
  - 비서 대상  : 단일 사용자 (steve)
  - 톤        : 부하직원 (보고형)
  - 언어      : 한국어 (데이터 영문 그대로)
  - 길이      : 5줄 이내 기본
  - 강조      : ✅/⚠️/🚨 만 (이모지 절제)

맞으면 (y), 수정 (n) :
```

---

## STEP 2 · Q2 · 업무 3개 (사용자 2분)

```
──────────────────────────────────────────

Q2. 1주일 동안 봇이 대신해줬으면 하는 일 3개?

  (예시)
   - 매일 07시: 어제 광고 ROAS 한 줄 요약
   - 매주 월: 뉴스레터 1통 작성 (승인 후 발송)
   - 즉시 알림: ROAS 2.0 이하면 디스코드 푸시

  내 답:
   - 매일:
   - 매주:
   - 즉시 알림:

──────────────────────────────────────────
```

### Claude 의 분석 (답변 받은 후 자동)

각 업무마다 5가지 자동 도출 :

| 업무 항목 | 도출 정보 |
|---|---|
| **트리거** | cron 시각 / 이벤트 조건 / 임계치 |
| **필요 MCP** | 답변 키워드 → MCP 매핑 (아래 표 참조) |
| **호출할 도구** | 예 : `run_report` · `search_threads` · `list_events` |
| **출력 채널** | Discord DM (기본) · Notion · Gmail |
| **기존 에이전트 매핑** | marketing-os/agents/ 안 일치 항목 |

### MCP 자동 매핑 표 (답변 키워드 → MCP)

| 키워드 | 필요 MCP | 활용 도구 |
|---|---|---|
| 광고 · ROAS · CPA · 캠페인 | meta-ads · google-ads | `get_insights` |
| 매출 · 시트 · 재고 | google-sheets | `read_sheet` |
| 일정 · 미팅 · 캘린더 | calendar | `list_events` · `create_event` |
| 메일 · CS · 받은편지함 | gmail | `search_threads` · `create_draft` |
| 트래픽 · GA4 · 전환 | ga4 | `run_report` |
| SNS · 인스타 · X · LinkedIn | buffer | `schedule_post` |
| 유튜브 · 채널 KPI · 댓글 | youtube-data | `getChannelStatistics` |
| 노션 · 캘린더 DB · 페이지 | notion | `notion-create-pages` |
| 경쟁사 · 트렌드 · 크롤링 | firecrawl | `scrape` · `search` |
| 이미지 · 광고 소재 | higgsfield | `generate_image` |
| 영상 · 인트로 | hyperframes · heygen · elevenlabs | (트리오) |

### marketing-os 기존 에이전트 매핑 표

| 사용자 답변 패턴 | 기존 에이전트 |
|---|---|
| "매일 07시 광고/매출/CS 통합" | `daily-briefing` |
| "ROAS 임계치 알림" | `check-ads` (cron 매시간) |
| "CS 메일 자동 응답" | `cs-responder` |
| "주간 뉴스레터" | `email-newsletter` + `send-newsletter` |
| "주간 종합 리포트" | `weekly-report` |
| "콘텐츠 캘린더" | `content-calendar` |
| "콘텐츠 자동 발행" | `content-publisher` |
| "광고 통합 리포트" | `3media-integrated-reporter` |

→ **이미 있는 에이전트면 추가 작성 불필요. 없으면 신규 정의 권장.**

게이트 :
```
Q2 분석 결과 (3가지 업무):

[1] 매일 07시 · 광고 ROAS 한 줄
    트리거    : launchd (매일 07:00)
    MCP       : meta-ads + google-ads
    출력      : Discord DM
    에이전트  : marketing-os/agents/daily-briefing (기존 활용)
    상태      : ✅ 즉시 가동 가능

[2] 매주 월 · 뉴스레터 작성
    트리거    : launchd (월 07:00)
    MCP       : firecrawl (트렌드) + gmail (Draft) + notion (아카이브)
    출력      : Gmail Draft → 사용자 승인 → 발송
    에이전트  : email-newsletter + send-newsletter (기존 활용)
    상태      : ✅ 즉시 가동 가능

[3] 즉시 알림 · ROAS < 2.0
    트리거    : cron (매시간) → 임계치 위반 시 발송
    MCP       : meta-ads + google-ads + Discord Webhook
    출력      : Discord DM (Webhook · 봇 세션 의존 X)
    에이전트  : check-ads (기존 활용)
    상태      : ✅ 즉시 가동 가능

미설치 MCP : 없음 (전부 활성)

맞으면 (y), 수정 (n) :
```

미설치 MCP 가 있다면 :
```
⚠️ 다음 MCP 가 필요한데 미설치입니다:
  - buffer (Q2 의 SNS 자동 게시용)

해결:
  → `mcp설치` 스킬 호출 (1개만)
  → `mcp설치-전체` 스킬 호출 (한 번에 다)
```

---

## STEP 3 · Q3 · 권한 정책 (사용자 1분)

```
──────────────────────────────────────────

Q3. 어디까지 알아서 해도 되고, 뭐는 무조건 물어봐야 해?

  (예시)
   - 자동 OK   : 조회·분석·요약·Draft 작성
   - 승인 필요 : 메일 발송·SNS 게시
   - 금지      : 광고 예산 변경

  내 답:
   - 자동 OK   :
   - 승인 필요 :
   - 금지      :

──────────────────────────────────────────
```

### Claude 의 분석 (답변 받은 후 자동)

3 정책을 도구 prefix 단위로 자동 매핑 :

| 정책 | 도구 prefix 예시 | 구현 방식 |
|---|---|---|
| **자동 OK** | `mcp__claude_ai_Gmail__search_threads` · `mcp__ga4__*` · `mcp__google-sheets__read_sheet` · `mcp__claude_ai_Notion__notion-fetch` 등 | 권한 프롬프트 자동 허용 |
| **승인 필요** | `mcp__claude_ai_Gmail__create_draft` (발송 X) · `mcp__buffer__*` (SNS) · `mcp__claude_ai_Google_Calendar__create_event` | 권한 릴레이로 폰 ✅/❌ |
| **금지** | `mcp__meta-ads__update_*` · `mcp__google-ads__update_*` · 예산 변경 도구 | `.claude/settings.json` 의 `deny` 권한 |

⚠️ 자동 OK 도 신중히 — 페어링된 사람이 폰 DM 으로 "광고 예산 늘려" 같은 명령을 보낼 수 있으므로 **위험 도구는 무조건 승인 또는 금지로**.

게이트 :
```
Q3 분석 결과:

자동 OK (권한 프롬프트 우회 OK):
  - mcp__claude_ai_Gmail__search_threads (메일 조회)
  - mcp__claude_ai_Gmail__list_drafts
  - mcp__ga4__* (GA4 모든 조회)
  - mcp__google-sheets__read_sheet
  - mcp__claude_ai_Notion__notion-fetch
  - mcp__meta-ads__get_insights (조회만)
  - mcp__google-ads__search (조회만)
  - 도구명 list_*, get_*, search_*, read_*

승인 필요 (권한 릴레이 → 폰 ✅/❌):
  - mcp__claude_ai_Gmail__create_draft (Draft 만 → 발송은 사용자)
  - mcp__buffer__schedule_post
  - mcp__claude_ai_Google_Calendar__create_event
  - mcp__claude_ai_Notion__notion-create-pages

금지 (deny 등록):
  - mcp__meta-ads__update_*
  - mcp__google-ads__update_*
  - 도구명 delete_*, update_budget*

맞으면 (y), 수정 (n) :
```

---

## STEP 3.5 · Q4 · 채널별 봇 기능 분리 (선택 · 사용자 1분)

⚠️ **선택 항목**: 디스코드 DM 1개로만 운영할 거면 `skip` 입력. 채널을 여러 개 운영 중이면 채널별로 어떤 기능만 작동할지 분리 가능.

```
──────────────────────────────────────────

Q4. 디스코드 채널별로 기능을 분리할까요?

  옵션 A · DM 통합 (모든 기능 본인 DM 에서 · 가장 단순) [기본]
  옵션 B · 채널 분리 (각 채널마다 다른 기능)
  옵션 C · 하이브리드 (DM 통합 + 특정 채널만 전용)

  내 답: (A / B / C / skip)

  옵션 B 또는 C 선택 시 — 채널 매핑:
   - 채널명 #__________ → 허용 기능 : __________
   - 채널명 #__________ → 허용 기능 : __________
   - 채널명 #__________ → 허용 기능 : __________

──────────────────────────────────────────
```

### Claude 의 분석 (답변 받은 후 자동)

#### 1단계 · 채널 ID 자동 조회

현재 `access.json` 에 등록된 그룹 채널 자동 추출 :

```bash
cat ~/.claude/channels/discord/access.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('등록된 채널 ID:')
for cid in data.get('groups', {}).keys():
    print(f'  - {cid}')
"
```

답변에 적은 채널명과 매칭되는 ID 가 없으면 사용자에게 :
```
다음 채널 ID 를 알려주세요.
Discord 에서 채널명 우클릭 (또는 폰에서 길게 누르기) → '채널 ID 복사':

  - #유튜브-분석 ID:
  - #일정 ID:
  - #광고 ID:
```

(Discord 개발자 모드가 켜져 있지 않으면 : 사용자 설정 → 고급 → 개발자 모드 ON)

#### 2단계 · 라우팅 표 자동 생성 (방법 A · 소프트 라우팅)

채널 ID 가 모이면 다음 표 자동 작성 :

| 채널 ID | 채널명 | 허용 기능 (자연어) | 허용 MCP prefix | 매핑 에이전트 |
|---|---|---|---|---|
| 1508590473525329932 | #유튜브-분석 | 채널 KPI · 댓글 · 트렌딩 | `mcp__youtube-data__*` | (Q2 답변 매핑) |
| 1508590279542706228 | #일정 | 일정 조회·생성·수정 | `mcp__claude_ai_Google_Calendar__*` | (Q2 답변 매핑) |
| (DM) | 본인 DM | 전체 | 전체 | 모든 |

#### 3단계 · Q2 의 3 업무 자동 분배 (옵션 B/C)

Q2 에서 답한 3 업무를 채널에 자동 추천 :
- 매일 광고 ROAS → 추천: #광고 또는 DM
- 매주 뉴스레터 → 추천: DM (승인 게이트 필요)
- 즉시 ROAS 알림 → 추천: #알림 또는 DM

게이트 :
```
Q4 분석 결과:

채널 라우팅 모드: B (채널 분리)

라우팅 표:
  [1] #유튜브-분석 (1508590473525329932)
      허용: 유튜브 채널 KPI·댓글·트렌딩
      MCP : mcp__youtube-data__*
      범위 밖 요청 → "이 채널에서는 유튜브 분석만 가능합니다" 거부

  [2] #일정 (1508590279542706228)
      허용: 일정 조회·생성·수정
      MCP : mcp__claude_ai_Google_Calendar__*
      범위 밖 요청 → 거부

  [3] DM (본인)
      허용: 전체

CLAUDE.md 자동 패치 위치:
  marketing-os/CLAUDE.md (말미에 'Discord 채널 라우팅' 섹션 추가)

맞으면 (y), 수정 (n), 건너뜀 (skip) :
```

⚠️ **소프트 라우팅 한계 · 90% 작동** (Claude 의 룰 준수 의지에 의존). 100% 결정적 차단 필요하면 방법 C (봇 N개 + 세션 N개 분리) 필요 — 호스팅 부담 ↑.

---

## STEP 4 · 종합 분석 + 비서 구축 문서 도출

3 질문 답변이 모이면 Claude 가 자동 종합 :

### 4-1. 봇 페르소나 카드 (Q1)

```markdown
## 페르소나
- 이름: marketing-ch
- 비서 대상: 김스티브 (1인 마케터)
- 톤: 부하직원 (보고형)
- 언어: 한국어 (영문 데이터 그대로)
- 길이: 5줄 이내 기본 (긴 분석 요청 시만 확장)
- 강조: ✅ ⚠️ 🚨 만 사용 (이모지 절제)
- 시그니처 어구 예: "사장님, 어제 광고 ..."
```

### 4-2. 우선 가동 에이전트 3개 (Q2)

각 에이전트마다 :
- 이름 · 트리거 · 호출 MCP · 산출물 · 기존 에이전트 매핑
- 구현 방식 (cron / launchd / Webhook)
- 즉시 가동 / 1주 / 1개월 분류

### 4-3. 승인 정책 표 (Q3)

- 자동 OK · 승인 필요 · 금지 도구 prefix 목록
- `.claude/settings.json` 권한 설정 예시 (allow/deny)
- 권한 릴레이 활성화 안내

### 4-4. 채널 라우팅 표 (Q4 · 선택)

Q4 응답이 옵션 B/C 인 경우만 작성. 옵션 A (DM 통합) 면 본 섹션 생략.

| 채널 ID | 채널명 | 허용 기능 (자연어) | 허용 MCP prefix | 매핑 에이전트 |
|---|---|---|---|---|
| 1508590473525329932 | #유튜브-분석 | 채널 KPI · 댓글 · 트렌딩 | `mcp__youtube-data__*` | youtube-analyzer (예시) |
| 1508590279542706228 | #일정 | 일정 조회·생성·수정 | `mcp__claude_ai_Google_Calendar__*` | calendar-assistant (예시) |
| (DM) | 본인 DM | 전체 | 전체 | 모든 에이전트 |

**CLAUDE.md 자동 패치** — `marketing-os/CLAUDE.md` 말미에 다음 섹션 자동 추가 :

```markdown
## Discord 채널별 봇 라우팅 (소프트 라우팅)

봇이 메시지를 받으면 `<channel source="discord" chat_id="...">` 의 chat_id 를 확인하고,
아래 표에 정의된 범위 내에서만 도구를 호출합니다.

(위 라우팅 표)

위반 시 응답:
  "이 채널에서는 {허용 기능} 만 가능합니다.
   전체 기능은 DM 으로 요청해주세요."
```

⚠️ **소프트 라우팅 한계 (90% 작동)** — Claude 가 룰 준수 의지에 의존. 채널 분리가 결정적으로 필요한 위험 작업 (광고 예산 변경 등) 은 **금지 정책 (Q3 의 deny)** 으로 보강. 100% 결정적 차단은 봇 N개 분리 필요 (현 스킬 범위 밖).

### 4-5. 필요 MCP 매트릭스

| MCP | 활성 | 용도 | 비고 |
|---|---|---|---|
| gmail | ✅ | Q2-2 뉴스레터 Draft | — |
| calendar | ✅ | (옵션) | — |
| ga4 | ✅ | — | — |
| meta-ads + google-ads | ✅ | Q2-1, Q2-3 | — |
| ... | | | |

### 4-6. 구현 우선순위

```
오늘 (즉시 가동):
  - daily-briefing 첫 실행 (Q2-1)
  - 폰 DM 으로 결과 확인

1주 (백그라운드 자동화):
  - launchd plist 작성 (Q2-1, Q2-2)
  - check-ads cron 등록 (Q2-3)
  - .claude/settings.json 권한 정책 적용

1개월 (확장):
  - orchestrator 가동 (Part 10 AX)
  - 새 에이전트 추가 (사용자 발화에 따라)
  - 노션 비서 일지 DB 자동 적재
```

---

## STEP 5 · 산출물 저장

### 5-1. 기본 위치
```
marketing-os/outputs/{YYYY-MM-DD}/bot-design/{date}-my-bot-spec.md
```

### 5-2. 추가 옵션
```
질문: 어디에 더 저장할까요? (복수 선택 가능)
  A. 로컬 파일만 (기본)
  B. + 노션 페이지 (Notion MCP 활성 시)
  C. + Discord DM 으로 핵심 한 줄 푸시 ("비서 설계 완료, 첨부 확인")
  D. + Gmail 본인에게 발송 (Draft)

답변 (A / B / AB / ABCD 등) :
```

### 5-3. 문서 템플릿

```markdown
# 내 클로드 비서 — 설계서 ({YYYY-MM-DD})

## 1. 페르소나
{Q1 분석 결과}

## 2. 우선 가동 에이전트 3개
### 2-1. {업무명 1}
- 트리거 · MCP · 출력 · 에이전트 매핑

### 2-2. {업무명 2}
...

### 2-3. {업무명 3}
...

## 3. 승인 정책
| 영역 | 정책 | 구현 |
|---|---|---|
...

## 4. 채널 라우팅 (Q4 응답 시 · 옵션 B/C)
| 채널 ID | 채널명 | 허용 기능 | 허용 MCP prefix |
|---|---|---|---|
| ... | ... | ... | ... |

→ `marketing-os/CLAUDE.md` 에 자동 패치됨. 위반 응답 문구 포함.
→ Q4 답변이 옵션 A (DM 통합) 면 본 섹션 생략.

## 5. 필요 MCP 매트릭스
...

## 6. 구현 우선순위
- 오늘: ...
- 1주: ...
- 1개월: ...

## 7. 첫 가동 명령
```bash
# Discord 폰 DM 으로 다음 메시지를 보내 첫 가동 검증:
"daily-briefing 한 번 실행해줘"
```

## 8. 다음 단계
- launchd plist 등록 (참고: discord-channels-setup STEP 11 / APPENDIX C)
- 권한 정책 settings.json 적용
- orchestrator 가동 (Part 10)
```

---

## STEP 5.5 · 추가 산출물 박제 (OPERATIONS.md + 아키텍처.md)

(구 `ai-assistant-build` STEP 4~5 흡수 · Q1~Q4 답변 + STEP 0.5 인벤토리 결과로 자동 채움)

### 5.5-1. OPERATIONS.md (봇 발화 매뉴얼 · 필수)

저장 위치 :
- **macOS / Linux** : `~/.claude/channels/discord/OPERATIONS.md`
- **Windows** : `%USERPROFILE%\.claude\channels\discord\OPERATIONS.md`

#### 자동 생성 템플릿

```markdown
# 봇 운영 매뉴얼 — OPERATIONS.md ({date})

## 1. 봇 호출 시작
- 폰 Discord 앱 → marketing-ch 봇 DM (또는 페어링한 채널)
- 정책: allowlist (본인 1명 + 그룹 채널 2)

## 2. 자주 쓰는 발화 (15~20개 · Q2 답변 기반 자동 채움)
- "오늘 일정 알려줘"          → Calendar list_events
- "어제 광고 ROAS 알려줘"      → meta-ads + google-ads get_insights
- "이번주 매출 시트 분석"      → google-sheets read_sheet
- "받은편지함 새 메일 분류"    → gmail search_threads
- "이 답변 노션에 저장"        → notion-create-pages
- "지난주 유튜브 채널 KPI"     → youtube-data getChannelStatistics
- "경쟁사 사이트 신상품 변경"  → firecrawl scrape
- ... (Q2 답변 + 활성 MCP 기반 자동)

## 3. 권한 승인 흐름 (Q3 기반)
| 영역 | 동작 |
|---|---|
| 자동 OK   | 즉시 실행 + 결과 답신 |
| 승인 필요 | 폰 권한 릴레이로 ✅ 클릭 후 실행 |
| 금지      | "이 작업은 금지" 응답 후 사용자에게 위임 |

## 4. 봇이 답 안 할 때 (3분 진단)
1. Discord 멤버 리스트에서 봇 🟢 온라인 확인
2. PC 의 `--channels` 세션 살아있는지 (`ps aux | grep channels`)
3. `/discord:access list` 로 본인 페어링 확인
4. `~/.claude/channels/discord/.env` 토큰 존재 확인

## 5. 응급 명령 카드
```bash
# 봇 재시작
claude --channels plugin:discord@claude-plugins-official

# 정책 확인
cat ~/.claude/channels/discord/access.json | python3 -m json.tool

# 페어링 재요청
/discord:access pair <코드>

# 정책 잠금
/discord:access policy allowlist
```

## 6. 호스팅 (노트북 닫으면 봇 죽음)
- **macOS** : `caffeinate -dis &` + `claude --channels ...`
- **launchd plist** 영구 등록 (참고: discord-channels-setup APPENDIX C)
- **Windows** : 작업 스케줄러 + `Start-Process`

## 7. 다음 단계
- 새 발화 등록: 본 § 2 에 1줄 추가 + 봇에게 "이런 명령 추가해줘"
- 새 에이전트 정의: `marketing-os/agents/<이름>.md` + orchestrator 라우팅
- 채널 라우팅 갱신 (Q4): CLAUDE.md 의 라우팅 표 수정
```

### 5.5-2. AI-비서-아키텍처.md (시스템 도식 · 옵션)

저장 위치 : `marketing-os/agents/AI-비서-아키텍처.md`

#### 자동 생성 템플릿

```markdown
# AI 비서 아키텍처 — 진단 시점: {date}

## 1. 한 줄 요약
"폰 DM 1개 입구 → orchestrator 라우팅 → 28 에이전트 + 14 스킬 + N MCP 결합"

## 2. 다이어그램 (ASCII)
폰 Discord ──DM──> 봇 (marketing-ch · --channels 세션)
                    │
                    ├─ chat_id 확인 (Q4 채널 라우팅)
                    │
                    └─> Claude (--channels 세션)
                         │
                         ├─ Q1 페르소나 적용 (톤·언어·길이)
                         ├─ Q3 권한 게이트 (자동/승인/금지)
                         │
                         └─> orchestrator (또는 직접 에이전트)
                              │
                              ├─ 데이터 분석 팀 (ga4 + sheets + ads)
                              ├─ 콘텐츠 팀 (gmail + notion + buffer)
                              ├─ 리서치 팀 (firecrawl + youtube)
                              ├─ 광고 팀 (meta-ads + google-ads + naver-ads)
                              ├─ CRM 팀 (gmail + ltv)
                              ├─ 콘텐츠 디자인 팀 (notion + figma)
                              └─ 운영 팀 (discord-channels + scheduler)

## 3. 7 도메인 팀 매트릭스
| 팀 | 대표 에이전트 | 주력 MCP | Q2 매칭 |
|---|---|---|---|
| 데이터 분석 | weekly-report · ga4-html-report | ga4·sheets | "매주 종합" |
| 콘텐츠 | email-newsletter · content-publisher | gmail·notion·buffer | "매주 뉴스레터" |
| 리서치 | research-trend · research-voc | firecrawl·youtube | "트렌드 추적" |
| 광고 | check-ads · analyze-meta · analyze-google-ads | meta-ads·google-ads | "ROAS 알림" |
| CRM | cs-responder · ltv-analyzer | gmail·sheets | "CS 자동 응답" |
| 디자인 | landing-copy · brand-voice | notion·figma | "상세페이지" |
| 운영 | orchestrator · daily-briefing | discord-channels·scheduler | "매일 브리핑" |

## 4. 진단 결과 ({date})
- 활성 MCP: N / N
- 가동 우선 에이전트 3개 (Q2 답변 기반)
- 채널 라우팅 모드 (Q4 답변)
- CLAUDE.md 패치 완료 여부

## 5. 한계 5가지
- 세션 의존 (`--channels` 활성)
- `fetch_messages` 100개 한도
- 무인 cron 발송 불가 → Webhook 별도
- 채널 라우팅 90% (소프트)
- 권한 릴레이 페어링 발신자가 도구 승인 가능

## 6. 보강 권장
- [ ] 미설치 MCP 추가
- [ ] 미정의 에이전트 작성
- [ ] CLAUDE.md 라우팅 적용
- [ ] 호스팅 옵션 적용
```

### 5.5-3. Notion 미러링 (옵션 · Notion MCP 활성 시)

3 산출물 (my-bot-spec · OPERATIONS · 아키텍처) 을 노션 페이지 3개로 미러링.
- 위치 : 사용자 노션의 "Marketing OS / Bot Design" DB
- 자동 백링크 : 3개 페이지 상호 참조

### 게이트
```
질문 · 추가 산출물 박제 여부:
  A. OPERATIONS.md 만 (필수 추천)
  B. OPERATIONS.md + AI-비서-아키텍처.md (둘 다)
  C. + Notion 미러링까지

답변 (A / B / C) :
```

---

## STEP 5.7 · PHASE 4 · 봇 설치 자동화 (자동 + 사용자 확인 · 5분)

⚠️ 산출물 문서만 박제하면 **실제 비서는 동작 안 함**. 본 STEP 에서 launchd · cron · settings.json 까지 자동 생성·등록.

### 5.7-1. `.claude/settings.json` 권한 패치 (자동 1분)

Q3 답변 (자동 OK / 승인 필요 / 금지) 기반으로 마케팅-OS 루트의 `.claude/settings.json` 자동 머지 :

```json
{
  "permissions": {
    "allow": [
      "mcp__claude_ai_Gmail__search_threads",
      "mcp__claude_ai_Gmail__list_drafts",
      "mcp__ga4__*",
      "mcp__google-sheets__read_sheet",
      "mcp__claude_ai_Notion__notion-fetch",
      "mcp__meta-ads__get_insights",
      "mcp__google-ads__search"
    ],
    "deny": [
      "mcp__meta-ads__update_*budget*",
      "mcp__google-ads__update_*budget*"
    ]
  }
}
```

⚠️ 기존 `settings.json` 이 있으면 **백업** (`settings.json.bak.{date}`) 후 allow/deny 머지. 덮어쓰기 X.

### 5.7-2. launchd plist 자동 작성 (macOS · 자동 2분)

Q2 의 매일·매주 업무 → launchd 자동 등록 :

```bash
# 매일 07:00 · daily-briefing
~/Library/LaunchAgents/com.marketing-os.daily-briefing.plist

# 매주 월 07:00 · weekly-newsletter
~/Library/LaunchAgents/com.marketing-os.weekly-newsletter.plist
```

자동 활성화 :
```bash
launchctl load ~/Library/LaunchAgents/com.marketing-os.daily-briefing.plist
launchctl load ~/Library/LaunchAgents/com.marketing-os.weekly-newsletter.plist
launchctl list | grep marketing-os   # 검증
```

**Windows 분기** : `schtasks /create ...` 작업 스케줄러 명령 자동 생성·등록.

### 5.7-3. cron 등록 (즉시 알림 폴링 · 자동 1분)

Q2 의 즉시 알림 → cron 등록 :

```bash
# 매시간 ROAS 임계치 체크 (Discord Webhook 사용 · 세션 의존 X)
( crontab -l 2>/dev/null; echo "0 * * * * cd $MARKETING_OS && claude -p 'check-ads 실행'" ) | crontab -
```

⚠️ 본 cron 은 `--channels` 세션과 별개. PC 만 켜져 있으면 동작 (Discord Webhook 발송).

### 5.7-4. 설치 검증 (자동 30초)

```bash
# 1. 권한 패치 확인
cat marketing-os/.claude/settings.json | python3 -m json.tool

# 2. launchd 등록 확인
launchctl list | grep marketing-os

# 3. cron 확인
crontab -l | grep check-ads

# 4. Discord Webhook 검증 (즉시 알림용)
curl -X POST $DISCORD_WEBHOOK_URL -H "Content-Type: application/json" \
  -d '{"content":"🚨 봇 설치 테스트 알림 — 무시 OK"}'
```

게이트 :
```
PHASE 4 봇 설치 결과:
  ✅ settings.json 권한 패치
  ✅ launchd plist N개 등록 (Q2 매일·매주 업무 수)
  ✅ cron 1개 등록 (check-ads 매시간)
  ✅ Discord Webhook 검증 (테스트 메시지 도착 확인)

PHASE 5 디스코드 채널 연동으로 진행할까요? (y / n)
```

---

## STEP 6 · PHASE 5 · 디스코드 채널 연동 + 첫 가동 검증

봇이 설치됐어도 **디스코드 채널 매핑**이 안 되면 사용자가 어디에 말 걸지 모름. 본 STEP 에서 채널 ID 등록 + 첫 가동 검증.

### 6-1. 필요 채널 목록 (프리셋/Q4 답변 기반 자동 도출)

```
프리셋 A · 마케팅 데일리 매니저
  → 필요 채널 : 0개 (DM 통합) · 본인 DM 만 사용

프리셋 B · 광고 옵저버
  → 필요 채널 : 1개 (#광고)

프리셋 C · 콘텐츠 큐레이터
  → 필요 채널 : 1개 (#콘텐츠)

자유 설계 D
  → Q4 답변 기반 (사용자 정의)
```

### 6-2. 채널 생성 가이드 (필요 시)

```
Discord 앱 :
  1. 본인 서버 → '+' 또는 'Create Channel'
  2. 텍스트 채널 선택
  3. 이름 입력 (#광고 · #콘텐츠 · #일정 등)
  4. 권한 : 본인만 보기 권장
  5. 생성 완료

채널 ID 복사 (필수) :
  - Discord 설정 → 고급 → '개발자 모드' ON (1회만)
  - 채널 우클릭 (폰은 길게 누르기) → '채널 ID 복사'
  - 예: 1234567890123456789 (18~19자 숫자)
```

### 6-3. access.json 자동 패치

사용자가 입력한 채널 ID + 채널명 → `access.json` 의 `groups` 자동 추가 :

```bash
python3 -c "
import json, pathlib, sys, shutil
from datetime import datetime
p = pathlib.Path.home() / '.claude/channels/discord/access.json'
shutil.copy(p, str(p) + '.bak.' + datetime.now().strftime('%Y%m%d-%H%M%S'))

data = json.loads(p.read_text())
data['groups'][sys.argv[1]] = {
    'requireMention': True,   # 봇 멘션 시만 응답 (스팸 방지)
    'allowFrom': []           # 빈 리스트 = 본인 상속
}
p.write_text(json.dumps(data, indent=2))
print(f'✅ 채널 추가: {sys.argv[2]} ({sys.argv[1]})')
" "$CHANNEL_ID" "$CHANNEL_NAME"
```

⚠️ `--channels` 세션 **재시작 필수** (정책 갱신 반영) :
```bash
# 기존 세션 Ctrl+C 후
claude --channels plugin:discord@claude-plugins-official
```

### 6-4. 첫 가동 검증

```
폰 Discord :

  [DM 통합 (A)]
    본인 DM → "오늘 매출·광고·CS 통합 알려줘"
    → daily-briefing 실행 + 30초 내 답신

  [채널 분리 (B/C/D)]
    해당 채널 (#광고/#콘텐츠) 에서 봇 멘션 :
      @marketing-ch 어제 ROAS 알려줘
    → 30초 내 답신

  [채널 범위 외 테스트 (B/C/D)]
    #광고 채널에서 → "오늘 일정 알려줘"
    → "이 채널에서는 광고 분석만 가능합니다. 전체는 DM 으로." 거부
    → CLAUDE.md 라우팅 룰 정상 작동 확인
```

게이트 :
```
질문 · 다음 모두 정상?
  ① 봇 30초 내 응답
  ② 라우팅 거부 메시지 (B/C/D 만)
  ③ OPERATIONS.md § 5 응급 명령 동작

답변 (y / 일부 / n) :
```

`일부` 또는 `n` → STEP 5.7 검증 재실행 + 트러블슈팅 표 참조.

### 6-5. 사용 시작 안내

```
🎉 5 PHASE 모두 완료. 봇 비서 가동 시작.

다음 행동:
  📖 OPERATIONS.md 확인 — 자주 쓰는 발화 15~20개
     위치: ~/.claude/channels/discord/OPERATIONS.md

  📊 첫 주 점검 — 매일·매주 자동화 가동 확인
     launchctl list | grep marketing-os
     tail -f /tmp/daily-briefing.out.log

  🔧 새 발화 등록 — OPERATIONS.md § 2 에 1줄 추가 + 봇에게 "이런 명령 추가해줘"

  📡 채널 추가 — 본 스킬 재호출 + PHASE 5 만 진행
```

---

## 🔄 재호출 시 PHASE 점프

이미 봇 셋업이 끝난 사용자가 본 스킬을 재호출하면 :

```
질문 · 어느 PHASE 만 다시 진행할까요?
  1. 처음부터 (전체 5 PHASE)
  2. PHASE 3 만 — 새 MCP 추가·안내
  3. PHASE 4 만 — 권한·자동화 갱신
  4. PHASE 5 만 — 새 디스코드 채널 추가
  5. OPERATIONS.md 갱신만

답변 (1 / 2 / 3 / 4 / 5) :
```

---

# 트러블슈팅 (자주 막히는 곳)

| 증상 | 원인 | 해결 |
|---|---|---|
| 답변이 너무 추상적 ("아무거나") | 사용자 선호 미정 | 한 번 되묻기 (예시 2~3개 보여주기) |
| MCP 미설치라 매핑 실패 | Q2 답변에 필요한 MCP 없음 | `mcp설치` 또는 `mcp설치-전체` 스킬 호출 |
| 권한 너무 넓음 ("다 자동 OK") | 위험 도구도 자동 허용 위험 | 강제 안내: "예산 변경·발송·삭제는 무조건 승인 또는 금지" |
| outputs 폴더 없음 | marketing-os 신규 환경 | `mkdir -p outputs/{date}/bot-design/` 자동 생성 |
| 노션 페이지 생성 실패 | Notion MCP 미활성 | Claude.ai → Settings → Connectors → Notion 연결 |
| 첫 가동 검증 시 봇 응답 없음 | `--channels` 세션 종료됨 | `claude --channels plugin:discord@claude-plugins-official` 재시작 |
| 채널 라우팅이 무시됨 (소프트) | `CLAUDE.md` 패치 누락 또는 Claude 가 룰 무시 | CLAUDE.md 의 라우팅 섹션 강조·재명시 (예시 응답 문구 포함). 위험 작업은 Q3 의 deny 로 보강 |
| 채널 ID 모름 | Discord 개발자 모드 OFF | 사용자 설정 → 고급 → '개발자 모드' ON → 채널 우클릭 → '채널 ID 복사' |
| 채널 라우팅 100% 차단 필요 | 소프트 라우팅 한계 (90%) | 봇 N개 발급 + 채널마다 별도 `--channels` 세션 가동 (호스팅 부담) |

---

# 메모리·문서 연결

- 본 스킬 산출물은 `outputs/{date}/bot-design/` 에 저장 + 노션 옵션 시 비서 일지 DB 에 자동 적재
- 페르소나 결과는 메모리 `bot-persona.md` 로 저장 권장 → 향후 다른 에이전트가 본 페르소나 기준 톤 통일
- Q1~Q3 응답 원본도 같은 폴더에 `{date}-bot-design-raw.md` 로 보존 (재설계 시 참조)
- 본 스킬은 `discord-channels-setup` 의 자연스러운 후속 — 셋업 완료 → 본 스킬로 비서화

# 강의 연결

- `discord-channels-setup` 의 STEP 11-3 (다른 MCP 결합) 안내 직후가 가장 자연스러운 호출 시점
- Part 10 AX 시스템의 30개 에이전트 중 어느 것을 가동할지 결정하는 게이트 역할
- 본 스킬로 도출된 우선순위 3개 에이전트 = 학습자의 첫 "AX 팀" 초기 멤버
