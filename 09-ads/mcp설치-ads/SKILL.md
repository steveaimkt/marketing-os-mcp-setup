---
name: mcp설치-ads
description: |
  Part 2 클립 3-2 (Meta·Google Ads MCP) 전용 설치 스킬. Meta 는 공식 hosted MCP (`https://mcp.facebook.com/ads`) OAuth 1분 등록 + Google Ads 는 Google 공식 MCP (`github.com/googleads/google-ads-mcp` · uvx) + Developer Token 1종만 (5분 + 승인 1~2일) + ADC 자동 인증. 후 매체별 ROAS 통합 비교 + 예산 재배분 시뮬레이션 1건을 시연. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Meta Google Ads MCP 설치하자"** ⭐ 주요 트리거
  - "광고 MCP 설치"
  - "Meta Ads · Google Ads 연결 도와줘"
  - "광고 자동화 환경 만들자"
  - "Part 2 / 3-2 설치 시작"

  4단계 (각 MCP 마다):
  ① 소개 → ② 설치 → ③ 가능 업무 → ④ 결과물 1개

  실행 순서: ① Meta Ads hosted MCP (claude mcp add http + OAuth 1클릭) → ② Google 공식 MCP (uvx --from git+https + Developer Token 1개 + ADC) → ③ 통합 결과물 1건

  특이점: 둘 다 공식 MCP (2026-05 신규 출시). Meta 는 Meta 가 직접 운영하는 hosted MCP. Google 은 Google 이 직접 유지보수하는 GitHub MCP · 읽기 전용 강제 (캠페인 변경 불가, 실수 위험 0). ADC 는 GA4 클립과 공유.
---

# Part 2 / 3-2 Meta·Google Ads MCP 설치 (클립 전용)

> 본 스킬은 Meta + Google Ads MCP 2 종을 본인 광고 계정 기준 즉시 운영 가능한 흐름으로 설치하고 매체 통합 ROAS 비교 + 예산 재배분 시뮬레이션 1건을 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 2 MCP 에 순차 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📈 Meta·Google Ads MCP 설치를 시작합니다.

먼저 짚고 갈 게 두 가지 있어요:

  1) Meta 는 2026-05 부터 공식 hosted MCP (mcp.facebook.com/ads) 운영.
     System User Token 발급 불필요 → claude mcp add 한 줄 + OAuth 1분.
     Google 은 2026-05 부터 공식 MCP (github.com/googleads/google-ads-mcp) 운영. ADC + Developer Token 만 (1~2일 승인 대기).

  2) Google MCP 의 안전 잠금:
     - 기본 Read-only 모드
     - 변경 작업은 GOOGLE_ADS_MCP_WRITE=true 명시
     - 모든 create/update 는 PAUSED 상태로 시작 (사용자 enable 후 활성)
     → 사고 위험 0

────────────────────────────────

총 4단계로 진행돼요 (12~17분 예상 · Meta hosted 전환으로 8분 절감):

  📖 STEP 1: MCP 소개 (2분)
       1.1 Meta + Google 한눈 정리
       1.2 안전 잠금 패턴 (PAUSED)
       1.3 Before vs After (1시간 → 3분)

  ⚙️ STEP 2: MCP 설치 (8~12분) · 6단계
       Part A · Meta Ads (1단계 · 1~2분) ★ hosted MCP
       Part B · Google Ads (Step 4~8 · 7~10분) · npm
       Step 9 · 헬스 체크

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 76개 (Meta 32 + Google 44)
       3.2 7 시나리오
       3.3 Part 6 광고 6 에이전트 연동

  🎯 STEP 4: 결과물 2개 (3~5분)
       4.1 2 MCP 연결 헬스 체크 (약 1분)
       4.2 작업 가능 업무 5종 미리보기 (약 2분)
  ※ 본인 활성 캠페인 없어도 OK · 캠페인 시작 시 5종 업무 즉시 자동화

사전 점검 5가지부터:
  □ Node.js 18 이상
  □ Meta Business Manager + 본인 광고 계정 1개 (캠페인 운영 안 해도 OK)
  □ Google Ads 본인 광고 계정 (Manager 모드 권장, 캠페인 불필요)
  □ Google Cloud Console 접근
  □ Chrome 또는 Safari

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | Meta Ads | Google Ads |
|---|---|---|
| 패키지 | Meta 공식 hosted MCP (`https://mcp.facebook.com/ads`) | **Google 공식 MCP** (`github.com/googleads/google-ads-mcp` · uvx) |
| 도구 수 | Meta 공식 (수시 업데이트) | 3개 (list_accessible_customers, search, get_resource_metadata) |
| 인증 방식 | OAuth 2.1 · Claude.ai 자동 (5 scope) | **Developer Token 1종만** + ADC 자동 |
| App Review | 불필요 (OAuth scope 활용) | Developer Token 신청 (1~2일 승인 대기) |
| 안전 잠금 | OAuth scope 제어 | **읽기 전용 강제** (Google 정책) |
| Before | 매체별 매니저 왕복 30분/회 | 같음 |
| After | "매체별 ROAS 비교" → 2분 | 자동 통합 |

### 1.2 마케터 관점 활용 가능성

- **3매체 통합 ROAS 리포트** · Meta + Google + (Part 6) Naver 한 표로 비교
- **예산 자동 재배분** · 한계 ROAS 모델 + PAUSED 안전 모드
- **임계치 자동 모니터링** · ROAS < 1.5 매시 감지 → Discord 알림 → 일시정지 권장
- **A/B 테스트** · 변형 자동 생성 + 통계적 유의성 검증
- **신규 캠페인 자동 생성** · Demand Gen, 비즈니스 목표 기반 (모두 PAUSED 시작)

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| Meta 광고 매니저 접속 + 조회 | 20분 | 30초 |
| Google 광고 매니저 같은 작업 | 20분 | 30초 |
| 통합 비교 표 + 인사이트 | 20분 | 1분 |
| 예산 재배분 (8 캠페인) | 30분 | 3분 (PAUSED) |
| 임계치 매니저 수동 확인 | 매일 30분 | 자동 (cron) |
| **주간 광고 점검 1회** | **1~1.5시간** | **3분** |
| **정기 운영 (매일 + 주간 + 임계치)** | **주 8~10h** | **주 30분** |

연간 환산: 약 400시간 절감 + 광고비 손실 90% ↓ + 실수 0건 (PAUSED 안전 잠금).

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치

### Part A · Meta Ads (1 단계 · 약 1~2분) ★ Meta 공식 hosted MCP

> 2026-05 부터 Meta 가 **공식 hosted MCP 서버** (`https://mcp.facebook.com/ads`) 를 운영합니다. System User Token / App / Permissions 발급 불필요. OAuth 한 번 클릭으로 끝.

#### STEP A1 · Claude Code 에 Meta hosted MCP 등록 (자동 30초)

Claude 자동 실행:

```bash
claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
```

검증:
```bash
claude mcp list | grep meta-ads
# 출력 예: meta-ads: https://mcp.facebook.com/ads (HTTP) - ! Needs authentication
```

`! Needs authentication` 상태가 정상. 다음 단계에서 인증.

#### STEP A2 · 브라우저 OAuth 인증 (사용자 1회 · 1분)

Claude Code 를 완전 종료 후 재시작. 재시작 후 Claude 에게 다음 질의:

```
사용자: "내 Meta 광고 계정 캠페인 목록 보여줘"
```

→ 브라우저 자동 열림 → Facebook 로그인 → 5개 권한 허용 → 자동 닫힘 → 인증 완료.

요청되는 OAuth scope (5개):
- `ads_management` · 광고 캠페인 조회·생성·수정
- `ads_read` · 광고 성과·통계 읽기
- `catalog_management` · 카탈로그 (커머스) 관리
- `business_management` · Business Manager 접근
- `pages_show_list` · 연결된 페이지 목록

OAuth 토큰은 Claude.ai 가 자동 관리 (만료 시 자동 갱신). System User Token / .env 변수 불필요.

#### STEP A3 · 헬스 체크 (자동 30초)

```bash
claude mcp list | grep meta-ads
# 출력 예 (성공): meta-ads: https://mcp.facebook.com/ads (HTTP) - ✓ Connected
```

또는 자연어로:
```
사용자: "Meta 광고 도구 목록 보여줘"
→ Claude: mcp__meta-ads__* 또는 hosted 패턴 도구 목록 출력
```

⚠️ **이전 npm 방식 사용자**: `@getscaleforge/mcp-meta-ads` 항목이 `.mcp.json` 에 남아있으면 충돌 가능. `.mcp.json` 에서 해당 항목 제거 (이미 마스터 스킬 `/mcp설치-전체` 가 자동 정리).



### Part B · Google Ads (2 단계 · 약 5분 + 승인 1~2일 대기) ⭐ Google 공식 MCP

> Google 이 직접 운영하는 공식 MCP (`github.com/googleads/google-ads-mcp` · Python · FastMCP 3.3.1) 사용. 읽기 전용 강제 + ADC 자동 인증 + 환경변수 2개만. 이전 5종 환경변수 발급 절차 (OAuth Client ID/Secret/Refresh Token/Customer ID) 모두 **불필요**.

#### STEP B1 · Developer Token 신청 (사용자 직접 · 5분 + 승인 1~2일)

```
① ads.google.com → wmbb.kr 계정 로그인
② Manager 계정 필요 (없으면 무료 생성)
   상단 ⚙ "관리자 계정 만들기"
   또는 https://ads.google.com/intl/ko_kr/home/tools/manager-accounts/

③ Manager 계정 안에서:
   상단 ⚙ "도구" > "설정" > "API 센터"
   또는 https://ads.google.com/aw/apicenter

④ "Developer Token 신청" / "Apply for Basic access" 클릭

⑤ 신청 양식:
   - 회사명: WMBB
   - 회사 웹사이트: wmbb.kr
   - 사용 목적: "Internal marketing automation and analytics
     for our own Google Ads accounts. Read-only."
   - 예상 호출량: ~1,000 calls/day (Basic Access 한도)
   - 데이터 정책: "Stored locally, not shared"

⑥ "Pending" 상태 → 1~2 영업일 내 이메일 알림 (steve@wmbb.kr)
⑦ 승인 후 Developer Token (22자) 복사
```

⚠️ **Developer Token 발급은 비동기**. 신청 후 1~2일 대기. 그 사이 본 스킬 다른 부분 그대로 진행 가능.

#### STEP B2 · MCP 등록 (Claude 자동 · 1분 · ADC 활용)

> ADC 는 Step 6 GA4 와 동일하게 이미 발급됨 (`~/.config/gcloud/application_default_credentials.json`). 별도 OAuth Client ID/Secret/Refresh Token 발급 불필요.

`.env` 에 1줄만 추가:

```bash
# Developer Token 만 명시 (Project ID 는 .mcp.json 에 하드코딩)
echo "GOOGLE_ADS_DEVELOPER_TOKEN=발급받은_22자_토큰" >> .env
```

`.mcp.json` 의 `google-ads` 항목 확인 (이미 등록됨):

```json
"google-ads": {
  "_part": "2 Ch3-2 Google 광고 분석 (Google 공식 MCP)",
  "command": "uvx",
  "args": [
    "--from",
    "git+https://github.com/googleads/google-ads-mcp.git",
    "google-ads-mcp"
  ],
  "env": {
    "GOOGLE_PROJECT_ID": "marketing-os-497122",
    "GOOGLE_ADS_DEVELOPER_TOKEN": "${GOOGLE_ADS_DEVELOPER_TOKEN}"
  }
}
```

JSON 검증:
```bash
python3 -c "import json; json.load(open('.mcp.json'))"
```

⚠️ **uv 가 없으면 먼저 설치** (마케팅os 다른 MCP 와 공유):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Google 공식 MCP 의 도구 (3개)

| 도구 | 역할 |
|---|---|
| `list_accessible_customers` | 인증된 사용자가 액세스 가능한 Google Ads 고객 ID + 계정 이름 목록 |
| `search` | GAQL (Google Ads Query Language) 요청 실행 |
| `get_resource_metadata` | 리소스 유형 (예: campaign) 의 메타데이터 조회 |

→ Customer ID 발급 절차 **불필요**: `list_accessible_customers` 도구로 자동 조회.

#### STEP 9 · Claude Code 재시작 + 헬스 체크 (자동 1분)

```
"내 Meta·Google 광고 계정 보여줘"
```

성공 응답:

```
✅ Meta Ads 연결 확인:
  - 광고 계정: act_1234567890 ("My Brand Ad Account")
  - 활성 캠페인: 5개
  - 통화: KRW

✅ Google Ads 연결 확인:
  - Customer ID: 123-456-7890
  - 활성 캠페인: 8개
  - 통화: KRW

도구: Meta 32 + Google 44 = 76개
```

### 2.X 보안 점검

설치 직후 확인:
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 값은 `${VAR}` 참조 (Token 평문 직접 입력 금지)
- [ ] Meta Token + Google 5종 모두 git log 에 노출된 적 없는지
- [ ] `GOOGLE_ADS_MCP_WRITE=true` 는 본인 광고 운영 시에만 (대행사용은 신중)
- [ ] System User 권한이 본인 광고 계정에만 부여됨 (다른 광고 계정 권한 부여 금지)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 (Meta 32 + Google 44 = 76개)

#### Meta Ads 주요 6개

| 도구 | 기능 |
|---|---|
| `list_ad_accounts` | 광고 계정 조회 |
| `list_campaigns` | 캠페인 목록·상태 |
| `get_campaign_insights` ★ | 캠페인 성과 (ROAS·CPA·CTR·노출·클릭) |
| `update_campaign_budget` ★ | 캠페인 일·총 예산 변경 |
| `pause_campaign` / `resume_campaign` | 캠페인 상태 변경 |
| `create_campaign` | 신규 캠페인 (PAUSED 기본) |

#### Google Ads 주요 6개

| 도구 | 기능 |
|---|---|
| `list_accounts` | MCC + 클라이언트 계정 |
| `search_gaql` ★ | GAQL 쿼리 (강력) |
| `get_campaign_performance` ★ | 캠페인 성과 (지표·기간) |
| `update_campaign_budget` ★ | 예산 변경 (PAUSED) |
| `pause_campaign` / `enable_campaign` | 캠페인 상태 |
| `create_demand_gen_campaign` | Demand Gen 캠페인 (PAUSED) |

### 3.2 마케터가 자주 쓰는 7 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 광고 계정 조회 | "내 광고 계정 보여줘" | 10초 |
| B. ROAS 분석 ★ | "지난 7일 매체별 ROAS 비교" | 1~2분 |
| C. Top/Bottom | "상위 5 + 하위 5 캠페인" | 30초 |
| D. 예산 재배분 ★ | "ROAS 4x 이상 30% 증액 PAUSED" | 1~3분 |
| E. 캠페인 일시정지 | "ROAS 1.0 이하 모두 PAUSE" | 30초 |
| F. 신규 캠페인 생성 | "Demand Gen 신규 PAUSED 시작" | 2~3분 |
| G. 임계치 자동 알림 | (cron) ROAS < 1.5 → Discord | 자동 |

### 3.3 Part 6 광고 6 에이전트 연동

본 MCP 는 Part 6 의 6개 광고 에이전트가 모두 자동 호출:

| 에이전트 | 사용 도구 |
|---|---|
| `mkt-meta-roas` | Meta `get_campaign_insights` |
| `mkt-google-ads` | Google `get_campaign_performance` + `search_gaql` |
| `mkt-naver-ads` | (별도 에이전트 · 본 MCP 외) |
| `mkt-anomaly` | 양 매체 + Discord MCP (멘션) |
| `mkt-3media-report` | 양 매체 + Notion MCP (게시) + Discord (알림) |
| `mkt-ab-test` | 양 매체 + Sheets MCP (통계) |

### 3.4 다른 MCP 와 조합 시나리오

- **+ Discord MCP** · 임계치 위반 자동 알림 + 승인 reaction 워크플로
- **+ Google Sheets MCP** · 광고 데이터 시트 자동 적재 + 시계열 추적
- **+ Notion MCP** · 주간 종합 리포트 Notion 페이지 자동 게시
- **+ GA4 MCP** · 광고 + 전환 데이터 통합 분석
- **+ Gmail MCP** · 광고 성과 이메일 자동 발송 (Claude.ai 통합)

---

## 🎯 STEP 4: 결과물 2개 · 연결 헬스 체크 + 도구·GAQL 학습

본 STEP 의 핵심: **활성 캠페인이 없어도 연결 자체는 정상 작동** 검증 + 캠페인 시작하는 날 즉시 자동화 가능하도록 도구·쿼리 학습. Part 6 광고 에이전트로 이어지는 진입점.

### 4.1 시연 A · 2 MCP 연결 헬스 체크 (약 1분)

```
사용자: "내 Meta·Google 광고 계정 정보 보여줘.
        활성 캠페인 + 권한 + 통화 + 도구 수 모두 확인."
```

자동 실행:

```
1. mcp__meta-ads__list_ad_accounts
   → Ad Account ID, 이름, 통화, 권한

2. mcp__meta-ads__list_campaigns
   → 활성 캠페인 (0개여도 정상 응답)

3. mcp__google-ads__list_accounts
   → Customer ID, 이름, 통화, MCC 권한, 시간대

4. mcp__google-ads__search_gaql (검증 쿼리):
   SELECT customer.id, customer.descriptive_name
   FROM customer LIMIT 1
   → 권한·접근 확인

5. 결과 표 출력:
   ✅ Meta Ads · Ad Account act_xxx · 통화 KRW · 권한 Admin · 캠페인 0개
   ✅ Google Ads · Customer ID xxx · 통화 KRW · MCC · 캠페인 0개
   ✅ 도구 76개 호출 가능 (Meta 32 + Google 44)
```

성공 기준:
- [ ] 양 매체 응답 정상 (캠페인 0개여도 연결 OK)
- [ ] 통화·권한 정보 확인
- [ ] 도구 호출 가능 여부 명시
- [ ] 본인 광고 계정 ID 노출

핵심 메시지: **활성 캠페인 0개여도 연결 성공**. 캠페인 시작하는 날 즉시 자동화 가능.

### 4.2 시연 B · 작업 가능 업무 5종 미리보기 (약 2분)

```
사용자: "본 MCP 로 마케터가 할 수 있는 업무 정리해줘.
        각 업무별 사용자 명령 예시 한 줄 + 다른 MCP 와 조합도 함께."
```

자동 실행:

```
마케터 작업 5종 카테고리별 출력:

🔍 1. 모니터링 · 매체별 성과 자동 회수
   명령 예시: "지난 7일 Meta·Google ROAS·CPA·CTR 비교 표"
   호출: list_campaigns + get_campaign_insights + search_gaql
   소요: 약 1~2분 (수동 1시간)
   조합: + Notion (리포트 게시) · + Discord (요약 알림)

⚖️ 2. 예산 최적화 · 한계 ROAS 모델 + PAUSED 안전
   명령 예시: "ROAS 4x 이상 30% 증액, 1.5 이하 정지 (PAUSED)"
   호출: update_campaign_budget × N + pause_campaign
   소요: 약 1~3분 (수동 30분)
   안전: 모든 변경 PAUSED 시작 · 매니저에서 enable 후 활성

🚨 3. 임계치 자동 알림 · ROAS·CPA 매시 감지
   명령 예시: "ROAS < 1.5 매시 감지 → #marketing 멘션"
   호출: cron + get_campaign_insights + Discord send_message
   소요: 자동 (cron 매시)
   효과: 광고비 손실 평균 90% ↓

🆕 4. 신규 캠페인 자동 생성 · Demand Gen·검색 (PAUSED)
   명령 예시: "Meta Demand Gen PAUSED 생성 (봄 신학기 컨셉)"
   호출: create_campaign + create_demand_gen_campaign
   소요: 약 2~3분
   안전: PAUSED 시작 · 매니저 검토 후 enable

🧪 5. A/B 테스트 · 변형 자동 + 통계적 유의성
   명령 예시: "이 캠페인 A/B 변형 3개 자동 생성 + 유의성 검증"
   호출: create_campaign × N + Sheets MCP (통계)
   소요: 약 5분
   결과: 통계적 승자 자동 선택

다른 MCP 와 조합 시나리오:
+ Discord MCP · 임계치 알림 + 승인 reaction 워크플로
+ Sheets MCP · 광고 데이터 시계열 적재
+ Notion MCP · 주간 리포트 자동 게시
+ GA4 MCP · 광고 + 전환 통합 분석
+ Gmail MCP · 광고 성과 이메일 자동 발송
```

성공 기준:
- [ ] 5종 작업이 각각 카테고리·명령 예시·소요·조합 정리됨
- [ ] 안전 잠금 (PAUSED) 강조됨
- [ ] 다른 MCP 조합 5종 이상 포함
- [ ] 캠페인 시작 시 그대로 호출 가능한 형태로 제시

### 4.3 다음 단계 제안

```
🎉 Meta·Google Ads MCP 설치 + 헬스 체크 + 학습 완성.
   캠페인 시작하는 날 즉시 자동화 가능. 다음 가능합니다:

  A. 캠페인 없을 때 학습 (지금 가능):
     - GAQL 쿼리 5종을 본인 Customer ID 로 직접 호출 (빈 응답 정상)
     - 신규 캠페인 PAUSED 생성 테스트 (즉시 삭제 가능)
     - 도구 학습 + 안전 잠금 검증

  B. 캠페인 시작 후 시나리오 (자동 호출):
     - "지난 7일 매체별 ROAS 비교" (한 줄)
     - "ROAS 4x 이상 30% 증액 PAUSED" (한 줄 + 매니저 enable)
     - "ROAS < 1.5 캠페인 자동 알림 등록" (cron + Discord)
     - "신규 Demand Gen 캠페인 PAUSED 생성"

  C. 정기 자동화 (Part 6 광고 6 에이전트):
     - mkt-anomaly · 매시 임계치 자동 감지
     - mkt-3media-report · 매주 종합 리포트
     - mkt-meta-roas · Meta 단독 깊은 분석
     - mkt-google-ads · Google 단독 깊은 분석
     - mkt-ab-test · A/B 변형 자동
     - mkt-naver-ads · Naver 보조 (별도)

  D. 다른 MCP 결합:
     - "Discord MCP 설치하자" → 임계치 알림 + 승인 워크플로
     - "Sheets MCP 설치하자" → 광고 데이터 시계열 적재
     - "Notion MCP 설치하자" → 주간 리포트 자동 게시
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 3-2 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-ads` 스킬을 호출해 Meta + Google 2 MCP 를 15~25분 안에 설치하고 **연결 헬스 체크 + 도구·GAQL 학습** 으로 마무리. 본인 활성 캠페인 없어도 OK.

### 실습 첫 결과물 명령 · 2 MCP 연결 헬스 체크

```
내 Meta·Google 광고 계정 정보 보여줘.
활성 캠페인 + 권한 + 통화 + 사용 가능 도구 수 모두 확인.
```

→ 약 1분. **활성 캠페인 0개여도 연결은 성공**. 캠페인 시작하는 날 즉시 자동화 가능.

### 실습 두 번째 결과물 · 작업 가능 업무 5종 미리보기

```
본 MCP 로 마케터가 할 수 있는 업무 정리해줘.
각 업무별 사용자 명령 예시 한 줄 + 다른 MCP 와 조합 시나리오도 함께.
```

→ 5종 업무 (모니터링 / 예산 최적화 / 임계치 알림 / 신규 캠페인 / A/B 테스트) 카탈로그 자동 출력.

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
1인 마케터의 광고 통합 매니저 어시스턴트

[입력]
- Meta + Google 광고 계정 (Naver 는 Part 6 클립에서 추가)
- 한계 ROAS 목표: 3.0 (이상이면 예산 증액 · 이하면 정지 검토)
- 일 총 예산: ₩200,000

[산출물]
매일 자동:
  ① 09:00 · 어제 매체별 성과 표 → Discord #marketing
  ② 18:00 · 오늘 마감 임박 광고 점검 → 임계치 위반 시 알림

매주 월요일 09:00:
  ③ 지난주 3매체 통합 ROAS 리포트 (HTML 첨부) → Discord
  ④ 예산 재배분 권장안 (PAUSED 적용 + Discord reaction 승인)

임계치 자동 (매시간):
  ⑤ ROAS < 1.5 즉시 알림 + 일시정지 권장

[제약]
- 모든 변경은 PAUSED 상태로 시작 (사용자 enable 필수)
- 캠페인 일 한도: 매체별 ₩50,000 (총 ₩100,000)
- Naver 광고는 Part 6 추가 후 통합
- 통화 KRW 통일

[검증]
- 매체별 ROAS 합계 = 일 광고비 × 평균 ROAS
- 예산 변경 후 PAUSED 상태 100%
- 임계치 알림 누락 0건
```

### 응용 과제

1. 본인 Meta + Google 광고 계정 1개씩 연결 후 "내 광고 계정 정보" 1회 시연 (캠페인 없어도 OK)
2. GAQL 쿼리 5종 본인 Google Ads Customer ID 로 직접 호출 (캠페인 없으면 빈 응답 정상)
3. **신규 캠페인 PAUSED 생성 시도** (테스트용 · 즉시 삭제 가능) → 안전 잠금 검증
4. **Part 6 광고 클립의 6개 에이전트가 본 MCP 를 자동 호출** · 캠페인 시작하는 날 즉시 자동화 시작

---

## 트러블슈팅 (Meta·Google Ads MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| Meta `Invalid OAuth Token` | Access Token 만료 (60일) 또는 권한 부족 | Business Manager > System User > Generate Token (영구 발급) |
| Meta `Permission denied` | System User 광고 계정 권한 부족 | Add Assets > 광고 계정 + Manage permissions 부여 |
| Meta App Review 요구 | 다른 사용자의 광고 계정 접근 시도 | 본인 광고 계정만 사용 · 또는 정식 App Review 진행 |
| Google `Developer token not approved` | Test Access 상태 + Production 계정 호출 | Basic Access 신청 (자동 승인 즉시 ~ 수시간) · 또는 Test MCC 사용 |
| Google `Refresh token expired` | 6개월 미사용 또는 권한 변경 | `npx mcp-google-ads-auth` 또는 OAuth Playground 재발급 |
| `Customer ID format` | 하이픈·공백 혼재 | 숫자만 (`1234567890`) 또는 표준 (`123-456-7890`) 둘 다 시도 |
| 변경 작업 거부 | `GOOGLE_ADS_MCP_WRITE` 환경변수 미설정 또는 false | `.env` 에 `GOOGLE_ADS_MCP_WRITE=true` 추가 후 재시작 |
| 두 매체 통화 불일치 | Meta KRW · Google USD 같은 경우 | 광고 계정 통화 통일 또는 Claude 가 자동 환율 변환 |
| `mcp__meta-ads__* / mcp__google-ads__*` 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `claude mcp list` 확인 + Claude Code 완전 종료 후 재시작 |
| 변경 후 광고가 즉시 enable 됨 | Google MCP 가 아닌 직접 광고 매니저 수정 가정 | Google MCP 는 PAUSED 시작 보장 · 매니저 UI 에서 enable 클릭 필요 확인 |
| Meta 메트릭이 매니저와 다름 | Meta Attribution Setting 불일치 | get_campaign_insights 호출 시 attribution_setting 명시 |
| Google GAQL 쿼리 오류 | 잘못된 필드명 · 함수 사용 | <https://developers.google.com/google-ads/api/fields/v17/overview> 참조 |

## 강의 연결

- 본 스킬은 [클립 3-2 Meta·Google Ads MCP 대본](../대본/3-2-ads.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 2 광고 MCP 에 순차 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 **Part 6 의 6개 광고 에이전트가 모두 자동 호출**:
  - `mkt-meta-roas` · `mkt-google-ads` · `mkt-anomaly` · `mkt-3media-report` · `mkt-ab-test` · (보조) `mkt-naver-ads`
- Part 10 의 광고 자동화 에이전트가 매시 cron 으로 임계치 모니터링 + 매주 월요일 통합 리포트.
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/09-ads/mcp설치-ads/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2)
  - `marketing-agents/.mcp.json` (Ads MCP 등록 예시 · `mcp-server-meta-ads` 는 npm 없음 → `@getscaleforge/mcp-meta-ads` 로 교체)
  - `marketing-agents/agents/mkt-meta-roas.md`
  - `marketing-agents/agents/mkt-anomaly.md`
  - `marketing-agents/agents/mkt-3media-report.md`
  - `marketing-agents/agents/mkt-3media-ax.md`

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| Meta MCP 패키지 | `@getscaleforge/mcp-meta-ads` v0.2.3 (npm · 2026-04) |
| Google MCP 패키지 | `mcp-google-ads` v1.5.0 (npm · MIT) |
| Meta Token 형식 | 영문+숫자 약 200자 (System User 영구 토큰) |
| Meta Ad Account ID 형식 | `act_1234567890` 또는 `1234567890` |
| Google Developer Token 등급 | Basic Access (Production 광고 계정 · 일 15,000 호출 한도) |
| Google Customer ID 형식 | `123-456-7890` (하이픈) 또는 `1234567890` (숫자만) |
| Google Refresh Token 발급 | `npx mcp-google-ads-auth` (OAuth 자동) |
| 안전 모드 | `GOOGLE_ADS_MCP_WRITE=true` 필요 + 모든 변경 PAUSED |
| Meta API 버전 | Graph API v24.0 |
| Google API 버전 | Google Ads API v17 |
| 노출 도구 | Meta 32 + Google 44 = 76개 |
| 인증 만료 (Meta) | 영구 (System User) · 만료 안 됨 |
| 인증 만료 (Google Refresh Token) | 6개월 미사용 시 만료 |
| App Review (Meta) | 본인 광고 계정 한정 불필요 · 타인 광고 계정 접근 시 필요 |
| Developer Token 승인 (Google) | 본인 운영자 보통 즉시 ~ 수시간 · 대행사 1~2 business days |

## 메모리·문서 연결

- 사용자의 Meta Ad Account ID + Google Customer ID 매핑은 메모리로 저장 (자주 사용)
- 한계 ROAS 모델 임계치 (예: 3.0 / 1.5) 도 메모리 저장 (재사용)
- 본 스킬 종료 후 사용자가 "매시 임계치 알림 자동" 이라고 하면 Part 6 의 `mkt-anomaly` 에이전트 또는 Part 10 의 `/agent-builder` 로 전달
- Google Ads GAQL 쿼리 패턴은 메모리로 저장 가능 (자주 변형해서 재사용)
