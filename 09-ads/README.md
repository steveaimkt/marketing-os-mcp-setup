# 클립 3-2. Meta·Google Ads MCP · 광고 성과 분석·집행·수정

## 한 줄 요약

Meta·Google Ads 공식 MCP(엠씨피) 2종을 설치하면 Claude(클로드)가 본인 광고 계정을 **직접 조회·분석·예산 조정·캠페인 생성**한다. ROAS(로아스) 점검 1시간이 3분으로, 예산 재배분 30분이 즉시로 줄어든다.

## 마케터에게 왜 필요한가

- 광고 매니저 (Meta + Google + Naver) 3개 탭을 매일 왕복 · 같은 데이터를 매체별로 다시 조회
- 주간 ROAS 종합 리포트 작성 1시간 · 매체별 캠페인 조회 + 표 정리 + 인사이트
- 예산 재배분 결정 후 매니저 UI 에서 캠페인별로 수동 변경 · 30분 + 실수 위험
- 임계치 위반 (ROAS < 1.5) 발견까지 며칠 걸리는 경우 다수 · 광고비 손실
- Meta·Google Ads MCP 설치 후 **3매체 통합 ROAS 리포트 3분**, 예산 조정 한 줄 명령, 임계치 자동 감지·알림

### Before / After

| 작업 | Before | After |
|---|---|---|
| 매니저 UI 로그인·필터 (Meta+Google) | 10분 | 0초 |
| 데이터 추출·통합 (Excel) | 30분 | 자동 |
| ROAS 계산·정렬 | 20분 | 자동 |
| 예산 재배분 시뮬레이션 | 30분 | 1분 |
| **일일 통합 분석** | **약 1시간 30분** | **1~2분** |

연 환산: **약 580시간 절감** (매일 1회 분석 기준).

## 무엇이 가능해지나

| 케이스 | 자연어 명령 예시 | 시간 |
|---|---|---|
| A. 광고 계정 조회 | "내 Meta·Google 광고 계정 + 활성 캠페인 보여줘" | 10초 |
| B. ROAS 분석 ★ | "지난 7일 매체별 ROAS·CPA·CTR 비교 표" | 1~2분 |
| C. Top/Bottom 캠페인 | "ROAS 상위 5개 + 하위 5개 광고세트" | 30초 |
| D. 예산 재배분 시뮬레이션 ★ | "Google ROAS 4x 이상 캠페인 예산 30% 증액 시 추가 매출" | 1분 |
| E. GAQL 쿼리 (Google) | "지난 7일 키워드별 ROAS TOP 20" | 30초 |
| F. 임계치 자동 알림 | (cron) ROAS < 1.5 감지 → Discord 멘션 | 자동 |

## 2개 MCP 한눈 (모두 공식 · 2026-05 채택)

| MCP | 패키지 | 도구 | 인증 |
|---|---|---|---|
| **Meta Ads** | **Meta 공식 hosted MCP** (`https://mcp.facebook.com/ads`) | Meta 공식 (수시 업데이트) | OAuth 2.1 · Claude.ai 자동 (5 scope) |
| **Google Ads** | **Google 공식 MCP** (`github.com/googleads/google-ads-mcp` · Python · FastMCP 3.3.1) | 3개 (`list_accessible_customers`, `search` GAQL, `get_resource_metadata`) | ADC 자동 + Developer Token 1개 |

**둘 다 공식 출시 (2026-05 신규)** · 이전 npm 커뮤니티 패키지보다 안정·신뢰도 압도적.

## 노출 도구 한눈

### Meta Ads (공식 hosted)

| 영역 | 가능 작업 |
|---|---|
| 광고 계정 조회 | `list_ad_accounts`, `list_campaigns`, 활성 상태 |
| 캠페인 성과 | `get_campaign_insights` · ROAS·CPA·CTR·노출·클릭 |
| 캠페인 관리 | `update_campaign_budget`, `pause_campaign`, `resume_campaign` |
| 카탈로그·페이지 | catalog_management, pages_show_list scope 활용 |

> Meta 공식 hosted MCP 의 도구 수는 Meta 가 직접 업데이트. 정확한 prefix·갯수는 Claude Code 에서 `claude mcp list` 후 `mcp__meta-ads__*` 자동완성으로 확인.

### Google Ads (공식 · 읽기 전용 강제)

| 도구 | 기능 | 사용 사례 |
|---|---|---|
| `list_accessible_customers` ★ | 접근 가능 광고 계정 ID + 이름 | 헬스 체크 + Customer ID 자동 조회 |
| `search` ★ | GAQL(지에이큐엘) 쿼리 실행 | 자유 분석 (캠페인·키워드·광고 그룹·전환 등) |
| `get_resource_metadata` | 리소스 메타데이터 (`campaign`, `keyword` 등) | 쿼리 구조 학습 |

⚠️ **Google Ads MCP 는 읽기 전용 (Google 정책)**. 캠페인 변경·예산 수정·생성 모두 **불가**. 변경 작업은 Google Ads Manager UI 또는 별도 도구 사용.

## 설치 방법 한눈

### 채택 자산

#### Meta Ads (1분 · ★★★ 가장 간단)

```bash
claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
```

→ Claude Code 재시작 후 첫 사용 시 OAuth 자동 인증 (5 scope: `ads_management`, `ads_read`, `catalog_management`, `business_management`, `pages_show_list`).

System User Token 발급·App·Permissions 불필요. `.env` 변수 0개.

#### Google Ads (5분 + 1~2일 승인 대기 · ★)

```bash
# (이미 .mcp.json 에 등록됨)
"google-ads": {
  "command": "uvx",
  "args": ["--from", "git+https://github.com/googleads/google-ads-mcp.git", "google-ads-mcp"],
  "env": {
    "GOOGLE_PROJECT_ID": "marketing-os-497122",
    "GOOGLE_ADS_DEVELOPER_TOKEN": "${GOOGLE_ADS_DEVELOPER_TOKEN}"
  }
}
```

**환경변수 1개만** (`GOOGLE_ADS_DEVELOPER_TOKEN`). ADC 는 GA4 와 공유 (별도 OAuth 작업 불필요).

> ⚡ 이전 (npm `mcp-google-ads` v1.5.0) 의 5종 환경변수 (Developer Token + Client ID/Secret + Refresh Token + Customer ID) 발급 절차 모두 **불필요**. Google 공식 MCP 채택으로 80% 단순화.

### 트리거 1줄

```
"Meta Google Ads MCP 설치하자"
```

→ `/mcp설치-ads` 스킬이 자동 호출되어 진행.

## 사전 준비물

- Node.js 18+ · uv (`uvx` 명령)
- Meta Business Manager + 본인 광고 계정 1개 (System User Token 불필요)
- Google Ads Manager 계정 1개 (없으면 무료 생성 · 광고비 0원 OK)
- gcloud CLI + ADC 발급 (GA4 와 공유)
- 광고 캠페인 1개 이상 실제 운영 중 (시연용, 선택)

## 작동 방식

```
[사용자 자연어 명령: "지난 7일 Meta·Google ROAS 비교"]
   ↓
[Claude Code]
   ↓
   ├─→ Meta hosted MCP (https://mcp.facebook.com/ads · OAuth 2.1)
   │     ↓
   │   Meta Graph API · 5 scope 토큰 자동 갱신
   │
   └─→ Google 공식 MCP (uvx --from git+https · ADC)
         ↓
       Google Ads API v17 · GAQL 쿼리
   ↓
[Claude 가 매체별 데이터 통합·비교]
   ↓
[결과: 매체별 ROAS·CPA·CTR 표 + 인사이트 + 다음 액션]
```

## 실습으로 만들 결과물 1건

설치 완료 후 즉시 만들 첫 결과물 (자세히는 [결과물-예시.md](결과물-예시.md)):

```
사용자: "어제 Meta + Google 광고 통합 성과 표로 + 예산 재배분 안"

결과: 6개 캠페인 통합 KPI + Claude 자동 인사이트
  | 플랫폼 | 캠페인 | 광고비 | ROAS |
  | Meta   | Advantage+ Shopping | ₩820K | 412% |
  | Meta   | 리타게팅            | ₩412K | 1,247% |
  | Google | Performance Max     | ₩684K | 821% |
  | Google | Search Generic      | ₩388K | 198% |
  ...

📌 권장 예산 재배분: Generic ↓30%, 리타게팅 ↑50%
   예상 추가 매출: ₩2.8M/일
```

- 활용 6가지 (일일 KPI, 캠페인 순위, 예산 재배분, GAQL 쿼리, 소재 A/B, 자동 알림)
- 매일 자동화: Part 6 `mkt-anomaly` 에이전트 + cron

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-ads`](mcp설치-ads/SKILL.md) | Meta hosted + Google 공식 2 MCP 순차 등록 |
| 운영 단계 | "주간 ROAS 비교" 등 자연어 | Claude 가 2 MCP 도구 자동 호출 |

Part 6 광고 클립 6개 (`mkt-meta-roas`, `mkt-google-ads`, `mkt-naver-ads`, `mkt-3media-report`, `mkt-anomaly`, `mkt-ab-test`) 가 모두 본 MCP 를 자동 호출.

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| Meta `Needs authentication` | OAuth 미인증 | Claude Code 재시작 후 "Meta 광고 캠페인 보여줘" → 자동 OAuth |
| Meta `Permission denied` | 5 scope 중 일부 거부 | OAuth 재인증 시 5 scope 모두 허용 |
| Google `Developer token not approved` | Pending 상태 | 1~2 영업일 승인 대기 (이메일 알림) |
| Google `An executable named ... not provided` | 패키지명 오타 | `.mcp.json` 의 args 가 `--from git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp` 형식 확인 |
| `mcp__google-ads__*` 도구 안 보임 | uv 미설치 또는 재시작 안 함 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` + Claude 재시작 |
| ADC 만료 | gcloud 토큰 갱신 필요 | `gcloud auth application-default login --client-id-file=...` 재실행 |
| `차단된 앱` (Google OAuth) | 기본 client ID 가 Workspace 차단 | 본인 OAuth credentials 파일 활용 (`mcp-server/oauth_credentials.json`) |

## 검증된 산출물

- 매체 통합 일일 KPI 표 (Meta + Google · 광고비·노출·CTR·전환·CPA·ROAS)
- GAQL 쿼리 결과 (키워드별·캠페인별 자유 분석)
- 예산 재배분 시뮬레이션 (한계 ROAS 모델)
- ROAS < 1.5 자동 감지 → Discord 알림 (Part 6 `mkt-anomaly`)
- 매주 종합 리포트 → Notion 페이지 자동 게시

## 다음

→ [`실습.md`](실습.md)
→ [`../10-notion/README.md`](../10-notion/README.md) · Notion MCP (리포트 자동 게시)
