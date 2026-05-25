# 클립 1-3. GA4 MCP · 웹사이트 성과 자동 리포트 생성

## 한 줄 요약
Claude가 **GA4 속성에 직접 접속해 트래픽·전환·채널 데이터를 가져와** 주간 리포트를 자동 작성하게 합니다.

## 마케터에게 왜 필요한가

- 매주 월요일 아침, GA4 화면을 열어 보고서 캡처·정리하는 데 **1~2시간**
- 채널별 성과를 손으로 시트에 옮기는 단순 반복
- "신규 vs 재방문 전환율 차이" 같은 질문에 답하려면 익숙해진 마케터도 5분 이상 클릭

### Before / After

| 작업 | Before | After |
|---|---|---|
| GA4 로그인 + 속성 선택 | 1분 | 즉시 (자연어 명령) |
| 채널별 리포트 + CSV | 10분 | 30초 |
| 신규 vs 재방문 | 10분 | 20초 |
| 노션 표 정리 + 코멘트 | 20분 | 자동 |
| **주간 리포트 1건** | **약 60분** | **약 1분** |

GA4 MCP가 있으면 "지난 7일 동안 채널별 세션·전환·전환율을 표로 정리해줘" → 1줄로 끝. Part 7의 **`ga4-html-report` 에이전트**가 이걸 매주 자동 생성.

## 핵심 도구 5개

| 도구 | 역할 |
|---|---|
| `run_report` ★ | 차원·지표 조합으로 리포트 추출 (90% 호출 점유) |
| `batch_run_reports` | 여러 리포트 동시 실행 (기간 비교용) |
| `get_realtime_data` | 현재 활성 사용자·페이지 (5초) |
| `list_metrics` | 사용 가능 지표 카탈로그 조회 |
| `list_dimensions` | 사용 가능 차원 카탈로그 조회 |

## 마케터 활용 시나리오 (6가지)

| # | 시나리오 | 자연어 명령 | 소요 |
|---|---|---|---|
| A | 채널별 성과 | "지난 7일 채널별 세션·전환·전환율" | 30초 |
| B | 랜딩 TOP 10 | "지난 28일 랜딩 페이지 TOP 10 + 이탈률" | 30초 |
| C | 신규 vs 재방문 | "newVsReturning 차원으로 전환율 비교" | 20초 |
| D | 기간 비교 | "이번 주 vs 지난 주 오가닉 변화율" | 1분 |
| E | 실시간 활성 | "지금 활성 사용자 몇 명, 어떤 페이지?" | 5초 |
| F | 디바이스 분포 | "모바일·데스크탑·태블릿 전환율 차이" | 30초 |

## 설치 방법 한눈

### 채택 패키지

**`mcp-server-ga4`** (npm v1.0.2 · okamoto53515606 · ADC 대응)

- 실행: `npx -y mcp-server-ga4`
- 인증 방식: **ADC (Application Default Credentials)** · 사용자 본인 Google 계정 OAuth
- 환경변수 2개:
  - `GOOGLE_APPLICATION_CREDENTIALS` · `~/.config/gcloud/application_default_credentials.json` (자동)
  - `GA_PROPERTY_ID` · GA4 속성 ID 9자리 숫자

> ⚠️ 변수명은 `GA4_PROPERTY_ID` 가 아닌 **`GA_PROPERTY_ID`** (GA4 → GA). 패키지가 요구하는 정확한 이름.

### 트리거 1줄

```
"GA4 MCP 설치하자"
```

`/mcp설치-ga4` 스킬이 자동 호출되어 3단계 진행:
1. gcloud CLI 설치 + ADC 발급 (사용자 OAuth 1회)
2. `.env` 에 `GA_PROPERTY_ID` 등록
3. 헬스 체크 + 첫 호출 검증

## 사전 준비물

- Google Analytics 4 속성 1개 (GA4 ID = 숫자 9자리)
- 본인이 그 GA4 속성에 **접근 권한** 있는 Google 계정 (Service Account 발급 불필요)
- macOS / Linux / Windows + Node.js 18+
- gcloud CLI (스킬에서 자동 설치 안내)

> ⚡ 이전 버전 (`mcp-google-analytics` PyPI · Service Account JSON 키 방식) 과 달리, 이번 패키지는 **본인 계정 ADC** 로 작동. Google Workspace 조직의 Service Account 키 발급 차단 정책 (`iam.disableServiceAccountKeyCreation`) 도 우회.

## 실습으로 만들 결과물 1건

설치 완료 후 즉시 만들 첫 결과물 (자세히는 [결과물-예시.md](결과물-예시.md)):

```
사용자: "지난 7일 채널별 세션 수와 전환 수를 표로 정리해줘"

결과: 채널별 주간 표 + Claude 자동 인사이트
  | 채널 | 세션 | 전환 | 전환율 |
  | Organic Search | 12,340 | 248 | 2.01% |
  | Paid Search    |  4,820 | 192 | 3.98% |
  ...
```

- 활용 8가지 (랜딩 TOP 10, 추세 비교, UTM 캠페인, 디바이스, 지역, 실시간 등)
- 매주 자동화: Part 10 의 `ga4-html-report` 에이전트 + cron

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `PERMISSION_DENIED` | 본인 계정이 GA4 속성에 접근 권한 없음 | GA4 관리 → 속성 액세스 → 본인 이메일 권한 확인 |
| `GA_PROPERTY_ID is not set` | 환경변수 이름 오타 (`GA_PROPERTY_ID` 잘못) | `.mcp.json` 의 env 키를 **`GA_PROPERTY_ID`** 로 (GA4_ 아님) |
| `ADC not found` | gcloud ADC 미발급 | `gcloud auth application-default login --client-id-file=...` |
| `차단된 앱` (브라우저) | gcloud 기본 client ID 가 조직에 차단 | 본인 OAuth credentials 로 ADC 재발급 (스킬에서 자동) |

→ 설치는 [`실습.md`](실습.md), 자동화는 [`mcp설치-ga4/SKILL.md`](mcp설치-ga4/SKILL.md).

## 다음

→ [`../03-firecrawl/README.md`](../03-firecrawl/README.md) · Firecrawl MCP (경쟁사·시장 자동 스크랩)
