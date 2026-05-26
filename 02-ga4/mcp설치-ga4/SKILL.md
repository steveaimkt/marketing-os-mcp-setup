---
name: mcp설치-ga4
description: |
  Part 2 클립 1-3 (GA4 MCP) 전용 설치 스킬. gcloud CLI + ADC (Application Default Credentials) + .mcp.json 등록 (`mcp-server-ga4` npm 패키지) + 채널별 주간 표 헬스 체크를 약 10분 안에 완료. Service Account JSON 불필요 (조직 정책 우회). 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"GA4 MCP 설치하자"** ⭐ 주요 트리거
  - "Google Analytics MCP 설치"
  - "구글 애널리틱스 연결"
  - "GA4 자동화 환경 만들자"
  - "주간 트래픽 리포트 자동화"
  - "Part 2 / 1-3 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (gcloud CLI + ADC + .env GA_PROPERTY_ID + .mcp.json 등록 + 헬스 체크) →
  ③ 작업 가능 업무 (도구 5개 + 6 시나리오) →
  ④ 결과물 1개 (채널별 주간 표)

  특이점: 본인 Google 계정 ADC 방식 (Service Account JSON 불필요). Google Workspace 조직 정책 `iam.disableServiceAccountKeyCreation` 우회. gcloud 기본 client ID 는 조직에 차단되므로 `--client-id-file=mcp-server/oauth_credentials.json` (Sheets 발급 분 재활용) 필수. 환경변수명은 `GA_PROPERTY_ID` (GA4_ 아님).
---

# Part 2 / 1-3 GA4 MCP 설치 (클립 전용)

> 본 스킬은 GA4 MCP 를 ADC 방식으로 설치하고 채널별 주간 표 1건을 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 GA4 의 ADC + Data API 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📊 GA4 MCP 설치를 시작합니다.

먼저 짚고 갈 게 있어요:

  이전 (Service Account JSON 방식) 과 다르게 본 스킬은 ADC 방식 사용:
  - gcloud CLI + 본인 Google 계정 OAuth (1회 클릭)
  - Service Account 키 발급 X (Google Workspace 조직 정책 우회)
  - .env 환경변수 1개만 (GA_PROPERTY_ID · GA4_ 아님)

────────────────────────────────

총 4단계 (약 10분):

  📖 STEP 1: MCP 소개 (2분)
       1.1 한 줄 정의 + 패키지 + 인증 방식
       1.2 마케터 관점 활용 가능성
       1.3 Before vs After (60분 → 1분)

  ⚙️ STEP 2: MCP 설치 (5~7분) · 3단계
       2.1 gcloud CLI 설치 (자동 5분)
       2.2 ADC 발급 (사용자 OAuth 1회, 1분)
       2.3 GA_PROPERTY_ID + .env 등록 (자동 1분)
       2.4 헬스 체크 (자동 30초)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 5개
       3.2 6 시나리오
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 (1분)
       4.1 채널별 주간 표 (Claude 자동 호출)

사전 점검 4가지:
  □ Google Analytics 4 속성 1개 (UA 구버전 ✕)
  □ 본인이 그 GA4 속성에 접근 권한 있는 Google 계정
  □ macOS / Linux / Windows + Node.js 18+
  □ GA4 속성에 지난 28일 트래픽 데이터 존재

전체 진행할까요? (y/n)
```

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드

| 항목 | 값 |
|---|---|
| 한 줄 정의 | GA4 속성을 본인 Google 계정 OAuth 로 조회·분석 |
| 패키지 | `mcp-server-ga4` npm v1.0.2 (okamoto53515606 · MIT · ADC 대응) |
| 실행 | `npx -y mcp-server-ga4` |
| 인증 방식 | **ADC** (Application Default Credentials · gcloud 발급) |
| API | Google Analytics Data API v1 |
| 도구 prefix | `mcp__ga4__*` (총 5개) |
| 환경변수 | `GOOGLE_APPLICATION_CREDENTIALS` + `GA_PROPERTY_ID` (GA4_ 아님) |
| 무료 한도 | Google API 무료 한도 (개인 사용 무제한급) |
| Before | GA4 콘솔 클릭·CSV·표 정리·코멘트 · 60분/주간 리포트 |
| After | "지난 7일 채널별 세션·전환" 자연어 한 줄 · 1분 |

### 1.2 마케터 관점 활용

- **주간 리포트 자동화** · 채널·랜딩·전환 표 3개를 30초에 출력
- **이상치 즉시 감지** · "이번 주 오가닉 트래픽 전주 대비 변화율"
- **콘텐츠 성과 추적** · 랜딩 페이지별 이탈률·체류시간
- **캠페인 효과 즉시 확인** · 푸시·광고 런칭 직후 실시간 활성 사용자
- **Part 7 에이전트 기반** · `ga4-html-report`, `ga4-channel-analysis`, `ga4-notion-publisher` 3종이 본 MCP 위에 구축됨

### 1.3 Before/After (수치)

| 작업 | Before | After |
|---|---|---|
| GA4 로그인 + 속성 선택 | 1분 | 즉시 |
| 채널별 리포트 + CSV | 10분 | 30초 |
| 랜딩 페이지 리포트 | 10분 | 30초 |
| 신규 vs 재방문 | 10분 | 20초 |
| 노션 표 정리 + 차트 | 20분 | 자동 |
| 인사이트 코멘트 수기 | 10분 | 자동 |
| **주간 리포트 1건** | **60분** | **1분** |

연 환산: 약 120시간 절감.

---

## ⚙️ STEP 2: MCP 설치 (5~7분 · 4단계)

### 2.1 gcloud CLI 설치 (자동 5분)

#### macOS (arm64)

```bash
cd ~
curl -fSL "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz" -o gcloud-cli.tar.gz
tar -xzf gcloud-cli.tar.gz
~/google-cloud-sdk/install.sh --quiet --usage-reporting=false --command-completion=true --path-update=true --rc-path=$HOME/.zshrc

# 검증
~/google-cloud-sdk/bin/gcloud --version | head -3
# → "Google Cloud SDK 569.0.0" 정도 출력
```

#### macOS (x86_64) · Linux

```bash
# Intel Mac: 위 URL 의 -darwin-arm.tar.gz → -darwin-x86_64.tar.gz
# Linux: -linux-x86_64.tar.gz
```

#### Windows (PowerShell)

```powershell
(New-Object Net.WebClient).DownloadFile(
  "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-windows-x86_64.zip",
  "$env:Temp\gcloud.zip"
)
Expand-Archive "$env:Temp\gcloud.zip" -DestinationPath $env:UserProfile
& "$env:UserProfile\google-cloud-sdk\install.bat" --quiet
```

### 2.2 ADC 발급 (사용자 1회 OAuth · 1분)

⚠️ **반드시 본인 OAuth credentials 사용**. Google 기본 client ID 는 wmbb.kr 같은 Workspace 조직 + `analytics.readonly` 스코프 차단에 걸림 (`차단된 앱` 오류). 2026-05 검증상 **데스크톱 앱 유형 자체 클라이언트**가 확실 (발급 절차는 아래 트러블슈팅 "⚠️ 실전 검증 · 벽 1" 참고). Sheets MCP 의 `oauth_credentials.json` 재활용도 가능하나, 그 클라이언트에 analytics 스코프 동의가 없으면 실패하므로 신규 발급 권장.

```bash
# ① 권장: 신규 데스크톱 클라이언트  ② 대안: Sheets MCP 발급분 재활용
~/google-cloud-sdk/bin/gcloud auth application-default login \
  --client-id-file="$HOME/.config/gcloud/ga4_oauth_client.json" \
  --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform

# → 브라우저 자동 열림 (localhost:8085 콜백)
# → 본인 Google 계정 로그인 + "허용"
# → ~/.config/gcloud/application_default_credentials.json 자동 생성
# → "Credentials saved to file" 메시지
```

ADC 검증:
```bash
ls -la ~/.config/gcloud/application_default_credentials.json
# → 약 360 bytes · type: authorized_user · refresh_token 포함
```

### 2.3 GA_PROPERTY_ID + `.env` 등록 (사용자 + 자동 · 2분)

사용자 작업: GA4 속성 ID 확인

```
1. analytics.google.com 접속 (위 ADC 와 같은 계정)
2. 본인 GA4 속성 선택
3. 좌하단 ⚙ "관리"
4. 우측 "속성" 컬럼 > "속성 설정"
5. 우상단 영역에 "속성 ID" 라벨 + 9자리 숫자 (예: 471063826)
6. 9자리 숫자만 복사 (G-XXX 형식 측정 ID 아님)
```

자동 작업: `.env` + `.mcp.json` 등록

```bash
# .env (Claude 자동 추가)
echo "" >> .env
echo "# GA4 MCP (Part 2-1-3 웹사이트 트래픽 자동 리포트)" >> .env
echo "GA_PROPERTY_ID=471063826" >> .env  # ⚠️ 9자리 숫자만 (GA4_ 아닌 GA_)
```

`.mcp.json` 의 `ga4` 항목 (이미 등록됨, 확인만):

```json
"ga4": {
  "_part": "2 Ch1-3 웹사이트 성과 자동 리포트",
  "command": "npx",
  "args": ["-y", "mcp-server-ga4"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "${HOME}/.config/gcloud/application_default_credentials.json",
    "GA_PROPERTY_ID": "427641480"
  }
}
```

> ⚠️ **속성 ID 는 평문 고정 권장.** `"${GA4_PROPERTY_ID}"` 처럼 `.env` 참조로 두면, claude 를 **marketing-os 루트가 아닌 서브폴더에서 실행**할 때 `.env` 가 안 읽혀 `Invalid property ID: ${GA4_PROPERTY_ID}` 에러가 난다 (`${HOME}` 같은 시스템 변수만 치환됨). 속성 ID 는 비밀값이 아니므로 직접 박는 게 안전. 다른 속성으로 바꾸려면 이 값 교체 후 재시작.

### 2.4 헬스 체크 (자동 30초)

```bash
claude mcp list | grep ga4
# → ga4: npx -y mcp-server-ga4 - ✓ Connected
```

`✓ Connected` 가 아니면:
- ADC 파일 확인: `ls ~/.config/gcloud/application_default_credentials.json`
- `GA_PROPERTY_ID` 확인: `grep GA_PROPERTY_ID .env`
- 실제 시작 시도: `GA_PROPERTY_ID="..." npx -y mcp-server-ga4` 직접 실행 후 에러 메시지 확인

### 2.5 보안 점검

- [ ] `~/.config/gcloud/` 권한 700 (자동 설정됨)
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 ADC 경로는 `${HOME}` 변수 사용 (절대경로 직접 입력 시 팀 공유 불가)
- [ ] 본인 Google 계정 (analytics.readonly + cloud-platform 권한만 부여됨)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 5개

| 도구 | 기능 |
|---|---|
| `run_report` ★ | 차원·지표 자유 조합 리포트 (90% 호출 점유) |
| `batch_run_reports` | 여러 리포트 동시 실행 (기간 비교용) |
| `get_realtime_data` | 현재 활성 사용자·페이지 (5초) |
| `list_metrics` | 사용 가능 지표 카탈로그 |
| `list_dimensions` | 사용 가능 차원 카탈로그 |

### 3.2 마케터가 자주 쓰는 6 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 채널별 성과 ★ | "지난 7일 채널별 세션·전환·전환율" | 30초 |
| B. 랜딩 TOP 10 | "지난 28일 랜딩 페이지 TOP 10 + 이탈률" | 30초 |
| C. 신규 vs 재방문 | "newVsReturning 차원으로 전환율 비교" | 20초 |
| D. 기간 비교 ★ | "이번 주 vs 지난 주 오가닉 변화율" | 1분 |
| E. 실시간 활성 | "지금 활성 사용자 몇 명, 어떤 페이지?" | 5초 |
| F. 전환 경로 | "소스/매체 → 랜딩 → 전환 다단계" | 1분 |

### 3.3 다른 MCP 와 조합

- **+ Sheets MCP** · GA4 데이터 → 시트 적재 + 차트 자동 갱신
- **+ Notion MCP** · GA4 표 → 노션 페이지 자동 게시 (장기 보관)
- **+ Discord MCP** · 주간 트래픽 리포트 → #marketing 채널 자동 발송
- **+ Meta·Google Ads MCP** · 광고 트래픽 + 전환 합산 (ROAS 계산)

본 MCP 는 **Part 7 에이전트 3종의 기반** · 데이터 분석 파트의 핵심.

---

## 🎯 STEP 4: 결과물 1개 · 채널별 주간 표

### 4.1 한 줄 명령

```
사용자: "지난 7일 채널별 세션 수와 전환 수를 표로 정리해줘"
```

### 4.2 자동 실행

```
1. Claude → mcp__ga4__run_report 호출
   - 차원: sessionDefaultChannelGroup
   - 지표: sessions · conversions
   - 기간: last_7_days
   - 정렬: sessions 내림차순

2. mcp-server-ga4 → Data API v1 호출 (ADC 인증)

3. GA4 속성 (properties/471063826) 조회

4. 결과 → 마크다운 표 변환·출력
   소요: 약 30초
```

성공 응답 예시:
```
✅ GA4 연결 · 속성 ID 471063826 · 기간 2026-05-17 ~ 2026-05-23

| 채널 | 세션 | 전환 | 전환율 |
|---|---|---|---|
| Organic Search | 12,340 | 248 | 2.01% |
| Paid Search    |  4,820 | 192 | 3.98% |
| Direct         |  3,210 |  87 | 2.71% |
| Email          |  1,940 | 108 | 5.57% |
| Referral       |    820 |  14 | 1.71% |

📌 인사이트 (Claude 자동 도출)
  · Paid Search 전환율 3.98% — 채널 평균 대비 우수
  · Email 전환율 5.57% — 가장 높음, 캠페인 강화 권장
```

자세히는 [결과물-예시.md](../결과물-예시.md) · 활용 8가지 + 마케터 5가지 시나리오 + Before/After 시간 비교.

### 4.3 다음 단계

```
🎉 GA4 MCP 설치 + 첫 결과물 완성. 발전 경로:

  A. 위 6 시나리오 직접 호출:
     - "지난 28일 랜딩 페이지 TOP 10" (콘텐츠)
     - "이번 주 vs 지난 주 오가닉 변화율" (추세)
     - "디바이스별 전환율" (디바이스)

  B. 다른 MCP 와 조합:
     - + Sheets MCP: GA4 데이터 시트 적재 + 차트
     - + Discord MCP: 주간 리포트 디스코드 자동 발송
     - + Notion MCP: 리포트 노션 페이지 자동 게시

  C. Part 7 데이터 분석 에이전트 (3개) · 위 6 시나리오 자동화:
     - ga4-html-report · 매주 월요일 09시 HTML 리포트 자동
     - ga4-channel-analysis · 채널별 심층 분석 (4주 추세)
     - ga4-notion-publisher · 노션 페이지 자동 게시

  D. 다음 MCP 설치:
     - 1-4 firecrawl · 경쟁사 사이트 크롤링
```

---

## 🚨 트러블슈팅 (GA4 MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `차단된 앱` (브라우저 OAuth 화면) | Google 기본 client ID 가 Workspace 조직 정책 + `analytics.readonly` 스코프 차단에 걸림 | **자체 OAuth 데스크톱 클라이언트** 발급 후 `--client-id-file=` 로 ADC 재로그인 (아래 ⚠️ 실전 참고) |
| `invalid_grant / invalid_rapt` (MCP 호출) | ① ADC 스코프 부족(analytics 누락) ② 또는 MCP 서버가 옛 토큰 캐싱 | 스코프 명시해 재로그인 + **Claude Code 재시작** (직접 curl 은 되는데 MCP 만 실패하면 캐싱) |
| `ACCESS_TOKEN_SCOPE_INSUFFICIENT (403)` | ADC 에 `analytics.readonly` 스코프 없음 | 로그인 시 `--scopes=https://www.googleapis.com/auth/analytics.readonly,...` 명시 |
| `Invalid property ID: ${GA4_PROPERTY_ID}` | `.mcp.json` 의 `${...}` 가 치환 안 됨 — claude 를 **서브폴더에서 실행**(루트 .env 미로드) | (A) marketing-os 루트에서 `claude` 실행 또는 (B) `.mcp.json` 에 속성 ID 평문 고정 (`"GA_PROPERTY_ID":"427641480"`) |
| `PERMISSION_DENIED` | 본인 Google 계정이 GA4 속성에 접근 권한 없음 | analytics.google.com > 관리 > 속성 액세스에 본인 이메일 권한 확인 |
| `GA_PROPERTY_ID is not set` | 환경변수 이름 오타 (`GA_PROPERTY_ID` 잘못) | `.mcp.json` env 키는 **`GA_PROPERTY_ID`** (GA4_ 아님). 값은 평문 또는 `${GA4_PROPERTY_ID}` |
| `INVALID_ARGUMENT` property ID | `properties/` 접두사 중복 | 9자리 숫자만 (MCP 자동 prefix) |
| `404 Not Found: API` | Analytics Data API 미활성화 | console.cloud.google.com > APIs & Services > Library > "Google Analytics Data API" 사용 설정 |
| `mcp__ga4__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `python3 -c "import json; json.load(open('.mcp.json'))"` 검증 + Claude Code 완전 종료 후 재시작 |
| 응답이 비어 있음 (행 0개) | 데이터 범위에 트래픽 없음 | 기간을 `last_90_days` 로 늘려 재시도 + 속성 ID 재확인 (속성마다 수집 기간 다름) |
| ADC 파일 없음 | gcloud auth 미실행 | STEP 2.2 명령 재실행 |
| ADC 만료 (`reauth required`) | 토큰 갱신 필요 | `gcloud auth application-default login --client-id-file=...` 재실행 + Claude Code 재시작 |

### ⚠️ 실전 검증 (2026-05-25, wmbb.kr) — 2개의 벽

**벽 1 · gcloud 기본 클라이언트의 GA4 스코프 차단**: 기본 client ID 는 이제 `analytics.readonly` 를 차단(브라우저 "액세스 차단"). Service Account 키도 wmbb.kr 정책상 막힘 → **자체 OAuth 데스크톱 클라이언트** 발급이 유일한 길:
1. GCP 콘솔 → `analyticsdata.googleapis.com` **사용 설정**
2. OAuth 동의 화면(대상=Internal 권장) → **OAuth 클라이언트 ID → 데스크톱 앱** → JSON 다운로드 → `~/.config/gcloud/ga4_oauth_client.json`
3. `gcloud auth application-default login --client-id-file="$HOME/.config/gcloud/ga4_oauth_client.json" --scopes="https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform"`
4. 검증: `TOKEN=$(gcloud auth application-default print-access-token)` 로 `analyticsdata.googleapis.com/.../runReport` 직접 curl → KRW/Asia-Seoul 응답이면 성공.

**벽 2 · `${GA4_PROPERTY_ID}` 미치환**: 서브폴더에서 claude 실행 시 루트 `.env` 가 안 읽혀 변수가 문자 그대로 전달됨(`${HOME}`·`${PWD}` 시스템 변수만 치환). → 루트 실행하거나, **비밀값 아닌 속성 ID 는 `.mcp.json` 에 평문 고정** 권장.

**공통 · MCP 서버 토큰 캐싱**: ADC/`.mcp.json` 갱신 후에도 떠 있는 서버는 옛 값 사용 → **반드시 Claude Code 재시작**.

## 📝 강의 실습 (실습.md 통합)

> 클립 1-3 실습.md 와 본 스킬을 함께 운영.

### 실습 한 줄 요약

`gcloud auth application-default login` 1회 + `.env` 의 `GA_PROPERTY_ID` 1줄 + Claude 재시작. 첫 결과물은 "지난 7일 채널별 세션 수" 표.

### 헬스 체크 명령

```bash
claude mcp list | grep ga4
# → ga4: ... - ✓ Connected
```

### 마케터 5패턴 · 정기 운영

```
[역할] D2C 브랜드의 그로스 마케터

[입력] GA4 속성 (지난 28일)

[산출물] 다음 3개 표:
  1. 채널별 세션·전환·전환율
  2. 랜딩 페이지 TOP 10
  3. 전환 경로 (소스/매체 → 랜딩 → 전환)

[제약] 한국어 표 헤더. 매출 원화. 비율 소수점 둘째 자리.

[검증] 데이터 행 수 + 기간 범위 함께 표시.
```

### 응용 과제

1. "이번 달 오가닉 트래픽이 지난 달 대비 몇 % 변화?" 비교 질의
2. **Part 7 GA4 에이전트 3종**이 사용할 데이터 추출 사양 미리 정의

## 강의 연결

- 본 스킬은 [클립 1-3 GA4 MCP 대본](../대본/1-3-ga4.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됨
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준을 GA4 의 ADC 패턴에 적용
- 본 스킬로 설치된 MCP 는 **Part 7 데이터 분석 에이전트 3종의 기반**:
  - `ga4-html-report` · 매주 월요일 09시 HTML 리포트 자동
  - `ga4-channel-analysis` · 채널별 심층 분석 (4주 추세)
  - `ga4-notion-publisher` · 노션 페이지 자동 게시
- 본 스킬은 클립 폴더 내부 (`curriculum/part02-MCP12개/02-ga4/mcp설치-ga4/`) · 클립과 함께 자체 보관

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 |
| gcloud CLI 설치 | `dl.google.com/dl/cloudsdk/channels/rapid/downloads/` |
| MCP 패키지 | `mcp-server-ga4` (npm v1.0.2 · okamoto53515606) |
| Google API | Google Analytics Data API v1 |
| 인증 방식 | ADC · `gcloud auth application-default login` |
| 자체 OAuth client | `~/.config/gcloud/ga4_oauth_client.json` (GCP 콘솔 데스크톱 앱 신규 발급 · 권장) |
| ADC 스코프 | `analytics.readonly` + `cloud-platform` (로그인 시 명시 필수) |
| ADC 파일 위치 | `~/.config/gcloud/application_default_credentials.json` |
| `.mcp.json` env 키 | `GA_PROPERTY_ID` (GA4_ 아님) · 값은 **평문 고정 권장** (서브폴더 실행 시 ${} 미치환) |
| 속성 ID 형식 | 숫자 9자리 (검증 계정 WMBB 메일리 = `427641480`) |
| 노출 도구 | 5개 (`run_report`, `batch_run_reports`, `get_realtime_data`, `list_metrics`, `list_dimensions`) |
| 자주 쓰는 차원 | `sessionDefaultChannelGroup` · `landingPagePlusQueryString` · `newVsReturning` · `sessionSource` · `sessionMedium` |
| 자주 쓰는 지표 | `sessions` · `conversions` · `conversionRate` · `totalRevenue` · `bounceRate` · `averageSessionDuration` · `activeUsers` |

## 메모리·문서 연결

- 사용자의 GA4 속성 ID + 주요 차원 매핑은 메모리로 저장 (자주 사용)
- 본 스킬 종료 후 사용자가 "주간 리포트 자동화" 라고 하면 Part 7 의 `ga4-html-report` 에이전트로 전달
- 사용자가 "광고 + GA4 합쳐서" 라고 하면 Meta·Google Ads MCP + GA4 MCP 조합 안내
