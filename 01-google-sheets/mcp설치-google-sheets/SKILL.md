---
name: mcp설치-google-sheets
description: |
  Part 2 클립 1-2 (Google Sheets MCP) 전용 설치 스킬. OAuth 2.0 자격증명 발급부터 자체 호스팅 MCP 서버 등록·브라우저 인증·연결 확인까지 15~20분 안에 완료. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Google Sheets MCP 설치하자"** ⭐ 주요 트리거
  - "구글 시트 MCP 설치"
  - "스프레드시트 MCP 설치"
  - "Google Sheets 연결 도와줘"
  - "Part 2 / 1-2 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (OAuth 5단계: 자격증명·서버·등록·인증·확인) →
  ③ 작업 가능 업무 (10 도구 + 5 시나리오) →
  ④ 결과물 1개 ("start" 단어 호출 → 라우터 → google-sheets 분기 → 5번 '자동 리포트' 시나리오 시연)
---

# Part 2 / 1-2 Google Sheets MCP 설치 (클립 전용)

> 본 스킬은 Google Sheets MCP 1 도구를 OAuth 2.0 방식으로 설치하고 첫 자동 리포트 1건을 만드는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📊 Google Sheets MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Google Sheets MCP 는 'Claude 가 본인 시트에 직접 손을 뻗는 신경' 입니다.
  한 번 설치하면 모든 세션에서 자동 사용. 10개 도구가 노출됩니다.
  코드 작성 안 합니다. "채널별 매출 비교해줘" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (15~20분 예상):

  📖 STEP 1: MCP 소개 (2분)
       1.1 한 줄 정의 + 제공사 + 라이선스
       1.2 마케터 관점 활용 가능성
       1.3 Before vs After 비교 (반나절 4시간 → 5분)

  ⚙️ STEP 2: MCP 설치 (14~16분) · OAuth 5단계
       2.1 Google Cloud OAuth 자격증명 발급 (사용자 10분)
       2.2 의존성 설치 (자동 1~2분, 검증된 서버 코드 사용)
       2.3 Claude Code 등록 확인 (자동 30초, 이미 등록됨)
       2.4 브라우저 인증 (사용자 3분)
       2.5 연결 확인 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 10 도구 (읽기 3 + 쓰기 3 + 관리 4)
       3.2 5 시나리오 (탐색·매출·ROAS·재고·리포트)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 (3~5분)
       4.1 "start" 단어 호출 → 라우터 → google-sheets 선택 → 작업 가능 업무 5개 메뉴 표시
       4.2 사용자 '5번 자동 리포트' 선택 → 5단계 자동 실행
       4.3 새 스프레드시트 생성 + URL 공유

사전 점검을 먼저 자동으로 진행할게요 (10초)...
```

### 🔍 자동 사전 점검 (Claude 자동 실행 · 10초)

Claude 는 본격적인 STEP 1 진입 전 다음 5가지를 자동 검증:

```bash
# 1) OS 확인
uname -s  # Darwin (macOS) / Linux / MINGW (Windows Git Bash)

# 2) Node.js 18+ 확인
node --version

# 3) marketing-os 루트 확인
test -f "${CLAUDE_PROJECT_DIR}/.mcp.json" && echo "OK" || echo "MISSING"

# 4) 자체 호스팅 서버 코드 존재 확인
test -f "${CLAUDE_PROJECT_DIR}/mcp-server/index.js" && echo "OK" || echo "MISSING"

# 5) 기존 설치 상태 확인 (재진입 시 빠른 처리)
test -f "${CLAUDE_PROJECT_DIR}/mcp-server/oauth_credentials.json" && echo "creds:OK" || echo "creds:NEED"
test -f "${CLAUDE_PROJECT_DIR}/mcp-server/token.json" && echo "token:OK" || echo "token:NEED"
test -d "${CLAUDE_PROJECT_DIR}/mcp-server/node_modules" && echo "deps:OK" || echo "deps:NEED"
```

검증 결과에 따른 분기:

| 상태 | 의미 | 진행 |
|---|---|---|
| 모두 OK + token:OK | 이미 설치 완료 | STEP 2.5 (연결 확인) 로 점프 |
| creds:OK + token:NEED | 자격증명만 있음 | STEP 2.2 부터 |
| creds:NEED | 처음 설치 | STEP 1 부터 정석 진행 |
| index.js MISSING | marketing-os 손상 | 사용자에게 git pull 안내 |
| Node < 18 | Node 업그레이드 필요 | `nvm install 18` 안내 |

### OS 분기 명령어

| 동작 | macOS / Linux | Windows (Git Bash / WSL) |
|---|---|---|
| Claude Code 재시작 | `⌘Q` 후 재실행 | 작업관리자에서 종료 후 재실행 |
| 다운로드 폴더 | `~/Downloads/` | `/c/Users/<user>/Downloads/` |
| 절대경로 확인 | `pwd` | `pwd` (Git Bash) 또는 `cd` (cmd) |
| 브라우저 열기 (서버측) | `open` 자동 호출 | `start` 자동 호출 (코드에 분기 있음) |

### 사용자 확인

```
사전 점검 결과:
  ✓ macOS · Node v20.10.0
  ✓ marketing-os 정상
  ✓ 서버 코드 정상
  ⚠ oauth_credentials.json 없음 → STEP 1 부터 진행

총 14~16분 예상. 진행할까요? (y/n)
```

사용자가 OK 하면 위 분기 표에 따라 적절한 STEP 으로 진입. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | Google 스프레드시트를 Claude 가 직접 읽고 쓰고 서식까지 만드는 도구 |
| 제공사 | 자체 호스팅 (mcp-server/index.js · @modelcontextprotocol/sdk + googleapis) |
| 라이선스 | MIT (사용자 본인 소유 코드) |
| 인증 방식 | OAuth 2.0 (Google Cloud Desktop App credentials) |
| 무료 한도 | Google API 무료 할당량 (분당 60회 읽기·쓰기) |
| Before | 시트 다운로드 → CSV → 수동 피벗·VLOOKUP → 서식 수동 → 결과 복붙 (반나절) |
| After | "주간 리포트 만들어줘" → 새 스프레드시트 자동 생성 + URL 공유 (5분) |

### 1.2 마케터 관점 활용 가능성

- **데이터 통합** · 쿠팡·네이버·자사몰 매출 + Meta·Google 광고 + 재고가 한 곳에 모임. 시트 자동화 = 마케팅 데이터 80% 자동화
- **분석 자동화** · 채널별 매출·플랫폼별 ROAS·재고 긴급 알림이 자연어 한 줄로 끝남
- **실시간 공유** · 분석 결과를 시트에 즉시 기록 → 팀 전체가 URL 클릭으로 확인
- **재사용성** · 한 번 만든 분석 파이프라인을 매주 "start" 단어 호출 → google-sheets · 5번 선택으로 재실행

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| 시트 구조 파악 | 5~10분 | 5초 |
| 매출 분석 | 30분 | 30초 |
| ROAS 분석 + 시뮬레이션 | 30분 | 1~2분 |
| 재고 알림 (조건부 서식) | 15분 | 30초 |
| 결과 기록 + 서식 | 30~60분 | 1분 |
| **종합 리포트 1회** | **반나절 (3~4시간)** | **5~10분** |
| **정기 운영 (주당 5회)** | **22시간/주** | **30분/주** |

연간 환산: 약 180시간 절감. 숙련 비용도 0 (피벗 테이블·VLOOKUP 불필요).

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · OAuth 5단계

### 2.1 STEP 1 / 5 · Google Cloud OAuth 자격증명 발급 (사용자 직접 · 10분)

사용자에게 안내:

```
브라우저에서 다음 5개 절차를 진행하세요. Claude 는 진행 상황만 묻습니다.

① 프로젝트 생성
   https://console.cloud.google.com 접속 → 로그인
   상단 프로젝트 선택 > "새 프로젝트" > 이름: `sheets-mcp` > 만들기

② Google Sheets API 활성화
   좌측 ≡ > "API 및 서비스" > "라이브러리"
   `Google Sheets API` 검색 > 클릭 > "사용" 클릭

③ OAuth 동의 화면 설정
   "API 및 서비스" > "OAuth 동의 화면"
   User Type "외부" > 만들기
   앱 이름: `Sheets MCP` / 이메일 입력 > "저장 후 계속" (나머지 기본값)

④ 테스트 사용자 추가 ⚠️ 필수
   OAuth 동의 화면 > "테스트 사용자" 또는 "Audience" 탭
   "+ 사용자 추가" > 본인 Google 이메일 입력 > 저장
   ⚠️ 이 단계 빠뜨리면 인증 시 "액세스 차단됨" 오류 발생

⑤ OAuth 클라이언트 ID 생성
   "사용자 인증 정보" > "+ 사용자 인증 정보 만들기" > "OAuth 클라이언트 ID"
   애플리케이션 유형: "데스크톱 앱" ⚠️ 반드시 이것 선택
   "만들기" > JSON 다운로드 (⬇ 버튼)
   파일명을 `oauth_credentials.json` 으로 변경
```

검증 (Claude 가 묻기):

```
다운로드한 JSON 파일을 열어서 다음 중 어떤 키가 있는지 확인하세요:
  - "installed" → 정상. 다음 단계 진행.
  - "web"       → "데스크톱 앱" 이 아닌 "웹 애플리케이션" 을 선택한 것. ⑤ 다시 진행.

준비 완료 시 'y' 입력하세요. 파일 경로도 알려주세요 (보통 ~/Downloads/).
```

### 2.2 STEP 2 / 5 · 의존성 설치 (Claude 자동 · 1~2분)

> ⚡ marketing-os 에는 **검증된 서버 코드(mcp-server/index.js · 10 도구 + OAuth2 구현)** 가 이미 포함되어 있어요. 작성 단계 없이 의존성만 설치합니다.

#### 2.2.1 사전 검증

```bash
# 서버 코드 존재 확인
test -f "${CLAUDE_PROJECT_DIR}/mcp-server/index.js" \
  && echo "✓ 서버 코드 존재" \
  || echo "✗ marketing-os 손상 — git pull 필요"

# package.json 무결성
cat "${CLAUDE_PROJECT_DIR}/mcp-server/package.json" | grep -E "modelcontextprotocol|googleapis"
```

손상 시 사용자에게 안내 후 종료. 정상이면 다음으로.

#### 2.2.2 oauth_credentials.json 이동

```bash
cd "${CLAUDE_PROJECT_DIR}/mcp-server"

# macOS / Linux
mv ~/Downloads/oauth_credentials.json ./

# Windows (Git Bash)
mv /c/Users/$USER/Downloads/oauth_credentials.json ./

# 검증
test -f ./oauth_credentials.json && \
  grep -q '"installed"' ./oauth_credentials.json && \
  echo "✓ Desktop App credentials 확인됨" || \
  echo "✗ 'web' credentials 입니다 — STEP 1 ⑤ 데스크톱 앱 재선택 필요"
```

#### 2.2.3 의존성 설치

```bash
cd "${CLAUDE_PROJECT_DIR}/mcp-server"

# node_modules 이미 있으면 스킵
test -d node_modules && echo "✓ 의존성 이미 설치됨" && exit 0

# npm install 실행 (재시도 1회 포함)
npm install || npm install --legacy-peer-deps
```

설치되는 패키지 (`mcp-server/package.json`):
- `@modelcontextprotocol/sdk ^1.27.1` · MCP 프로토콜 표준
- `googleapis ^171.4.0` · Google Sheets API v4 클라이언트
- `zod` · 도구 입력 스키마 검증

#### 2.2.4 npm install 실패 대응

| 증상 | 원인 | 해결 |
|---|---|---|
| `EACCES: permission denied` | 권한 문제 | `sudo chown -R $USER ~/.npm` 후 재시도 |
| `ETIMEDOUT` / 회사 프록시 | 네트워크 차단 | `npm config set registry https://registry.npmmirror.com` 임시 사용 |
| `node-gyp` 빌드 실패 | Python/C++ 도구 부재 | macOS: `xcode-select --install` / Windows: `npm install -g windows-build-tools` |
| `peer deps` 충돌 | SDK 버전 차이 | `npm install --legacy-peer-deps` |

서버 코드 구현 (`mcp-server/index.js` · 약 480줄):
- OAuth2 데스크톱 플로우 (localhost:3456 콜백 + 토큰 자동 갱신)
- 10 도구: `get_spreadsheet_info`, `read_sheet`, `batch_read_sheet`, `write_sheet`, `append_sheet`, `clear_sheet`, `add_sheet`, `delete_sheet`, `create_spreadsheet`, `format_cells`
- 한국어 에러 메시지 · macOS `open` 으로 브라우저 자동 열림 (Windows 는 코드 패치 필요시 트러블슈팅 참고)

### 2.3 STEP 3 / 5 · Claude Code 등록 (Claude 자동 · 30초)

> ⚡ marketing-os 의 `.mcp.json` 에는 **이미 google-sheets 항목이 등록되어 있어요**. 별도 추가 작업 없이 확인만 진행합니다.

`marketing-os/.mcp.json` 의 `mcpServers` 안 google-sheets 항목 확인:

```json
"google-sheets": {
  "_part": "2 Ch1-2 스프레드시트 자동화 (자체 호스팅 MCP)",
  "command": "node",
  "args": ["${CLAUDE_PROJECT_DIR}/mcp-server/index.js"]
}
```

`${CLAUDE_PROJECT_DIR}` 변수는 Claude Code 가 자동으로 marketing-os 루트로 해석해요. 절대경로 입력 불필요.

#### 등록 확인

```bash
claude mcp list 2>&1 | grep google-sheets
# 출력 예: google-sheets: ... node mcp-server/index.js - ✓ Connected
```

`Connected` 가 아니면 STEP 2.4 (브라우저 인증) 가 아직 완료 안 된 상태. 다음 단계 진행.

### 2.4 STEP 4 / 5 · 브라우저 인증 (사용자 1회 · 3분)

사용자에게 안내:

```
Claude Code 를 완전히 종료 후 재시작하세요.

OS 별 종료 방법:
  macOS    · ⌘Q  또는 메뉴 > Claude Code > Quit
  Windows  · 작업관리자 > Claude Code 프로세스 종료 후 재실행
  Linux    · pkill -f claude  또는 시스템 트레이 > 종료

재시작 후 server.listen 이 호출되면 브라우저가 자동으로 열려요:

  ① Google 계정 선택 (Step 1 ④ 에서 테스트 사용자로 추가한 계정)
  ② "이 앱은 확인하지 않았습니다" → "고급" → "이동" 클릭
  ③ 스프레드시트 읽기/쓰기 권한 → "허용"
  ④ "✅ 인증 완료!" 페이지 표시 → 브라우저 닫기

성공 시 `mcp-server/token.json` 이 자동 생성됩니다.
이후 60일 이내 사용 시 자동 로그인 (토큰 만료 시 자동 갱신).

브라우저가 자동으로 안 열리면 (방화벽·자동실행 차단 등):
  터미널에 출력된 https://accounts.google.com/o/oauth2/v2/auth?... URL 을
  수동으로 복사해서 브라우저 주소창에 붙여넣기 하세요.

브라우저 인증 완료하셨으면 'y' 입력하세요.
```

### 2.5 STEP 5 / 5 · 연결 확인 (Claude 자동 · 1분)

3단계 자동 검증:

#### 2.5.1 MCP 서버 등록 상태

```bash
claude mcp list 2>&1 | grep google-sheets
# 기대 출력: google-sheets: node ... mcp-server/index.js - ✓ Connected
```

`Connected` 가 아니면:
- `Failed to connect` → mcp-server/index.js 실행 에러. 다음 명령으로 로그 확인:
  ```bash
  node "${CLAUDE_PROJECT_DIR}/mcp-server/index.js" 2>&1 | head -20
  ```
- 항목 없음 → `.mcp.json` 미인식. Claude Code 완전 종료 후 재실행.

#### 2.5.2 도구 노출 확인

Claude 에게 다음 도구 호출을 요청:

```
사용자: "google-sheets MCP 도구 목록 보여줘"

Claude 자동 응답 (예):
  ✅ google-sheets MCP 연결됨 · 10 도구 노출
    1. mcp__google-sheets__get_spreadsheet_info
    2. mcp__google-sheets__read_sheet
    3. ... (총 10개)
```

#### 2.5.3 첫 도구 실행 (필수)

```
사용자: "다음 시트 정보 보여줘: https://docs.google.com/spreadsheets/d/{ID}"

Claude 자동 실행:
  mcp__google-sheets__get_spreadsheet_info(spreadsheet_id="{ID}")

기대 출력:
  📊 스프레드시트: '<제목>'
     - 시트1: 1247행 × 8열
     - 시트2: 382행 × 12열
     ...
```

스프레드시트 정보가 정상 출력되면 설치 완료. 다음 STEP 3 진행.

오류 시 → 본 스킬 하단 「트러블슈팅」 섹션 참고.

### 2.6 보안 점검

설치 직후 확인:
- [ ] `mcp-server/oauth_credentials.json` 이 `.gitignore` 에 등록됨
- [ ] `mcp-server/token.json` 이 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 경로는 `${CLAUDE_PROJECT_DIR}` 변수 사용 (절대경로 직접 입력 시 팀 공유 불가)
- [ ] git log 에 토큰·credentials 가 노출된 적 없는지

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 10개

| 그룹 | 도구 | 역할 |
|---|---|---|
| **읽기** | `get_spreadsheet_info` | 시트 목록·메타 조회 |
| | `read_sheet` | 특정 범위 데이터 읽기 |
| | `batch_read_sheet` ★ | 여러 시트 동시 읽기 (API 1회) |
| **쓰기** | `write_sheet` | 데이터 덮어쓰기 |
| | `append_sheet` | 행 추가 (기존 유지) |
| | `clear_sheet` | 범위 삭제 |
| **관리** | `add_sheet` | 새 시트 탭 생성 |
| | `delete_sheet` | 시트 탭 삭제 |
| | `create_spreadsheet` ★ | 새 스프레드시트 파일 생성 |
| | `format_cells` ★ | 서식 적용 (배경·글꼴·정렬·굵게) |

### 3.2 마케터가 자주 쓰는 작업 5 시나리오

| 시나리오 | 자연어 명령 예시 | 소요 시간 |
|---|---|---|
| A. 시트 탐색 | "어떤 시트가 있어?" | 5초 |
| B. 매출 분석 | "채널별 매출 비교해줘" | 30초 |
| C. ROAS 분석 | "플랫폼별 ROAS 비교하고 예산 재배분 안 만들어줘" | 1~2분 |
| D. 재고 알림 | "긴급 상품 상태 업데이트하고 빨간 배경 강조" | 30초 |
| E. 자동 리포트 ★ | "주간 리포트 스프레드시트 새로 만들어줘" | 3~5분 |

### 3.3 다른 MCP 와 조합 시나리오

- **+ GA4 MCP** · GA4 데이터를 자동으로 시트에 기록 → 시트에서 분석 → 새 리포트 생성 (전 과정 자연어 1줄)
- **+ Meta·Google Ads MCP** · 어제 광고 성과를 광고 매니저에서 직접 가져와 시트에 자동 적재 + 임계치 위반 시 디스코드 알림
- **+ Discord MCP** · 분석 완료 시 디스코드 채널에 URL 자동 발송
- **+ Notion MCP** · 시트 분석 인사이트를 노션 페이지로 자동 정리

---

## 🎯 STEP 4: 결과물 1개 · "start" 단어 호출 → 라우터 → google-sheets · 5번 '자동 리포트' 시연

### 4.1 작업 선정 · 매주 운영에 그대로 쓰는 종합 리포트

```
사용자: "start" (또는 "시작" · "마케팅 시작")
  ↓
라우터: google-sheets MCP 1개 감지 → 자동 진입
  ↓
라우터: "🎯 google-sheets · 작업 가능한 업무를 알려드릴게요."
  → 5개 시나리오 메뉴 표시 (시트 탐색·매출 분석·ROAS·재고·자동 리포트)
  ↓
사용자: "5" (또는 "주간 종합 리포트 만들어줘")
  ↓
하단 5단계 자동 실행
```

### 4.2 5단계 자동 실행

```
Step 0/5 · 세팅 확인           (5초)
  - mcp__google-sheets__get_spreadsheet_info 호출
  - 스프레드시트 ID 확인 + 시트 목록 조회
  - "MCP 서버: 연결됨 · 시트 목록: 4개"

Step 1/5 · 데이터 탐색         (10초)
  - mcp__google-sheets__batch_read_sheet 호출
  - 3 시트 (매출·광고·재고) 헤더 + 샘플 5행 동시 읽기

Step 2/5 · 데이터 분석         (30~60초)
  - mcp__google-sheets__read_sheet 호출 (전체 데이터)
  - 채널별 매출·플랫폼별 ROAS·재고 긴급 분석
  - 인사이트 + 액션 아이템 도출

Step 3/5 · 시트 기록 + 서식    (30초)
  - mcp__google-sheets__add_sheet → '분석결과' 시트 생성
  - mcp__google-sheets__write_sheet → 분석 결과 기록
  - mcp__google-sheets__format_cells → 헤더 파란 배경 (#4285f4) 흰 글씨 + 굵게

Step 4/5 · 추가 분석 (선택)    (사용자 후속 질문)
  - "ROAS 하위 3개 캠페인 공통점은?"
  - 즉시 답변

Step 5/5 · 최종 리포트         (1~2분)
  - mcp__google-sheets__create_spreadsheet 호출
  - 새 스프레드시트 '주간 리포트 {날짜}' 생성
  - 4 시트에 각각 분석 결과 기록 + 서식 적용
  - URL 반환 + 사용자에게 공유 안내
```

### 4.3 결과물 검증

성공 기준:
- [ ] 새 스프레드시트 URL 클릭 시 정상 열림
- [ ] 4 시트 모두 헤더 서식 적용됨 (파란 배경 + 흰 글씨)
- [ ] 총합 수치가 원본 시트와 ±1% 이내
- [ ] 분석 인사이트가 단순 수치 나열이 아닌 액션 가능한 문장
- [ ] 생성 시간 5분 이내

### 4.4 다음 단계 제안

```
🎉 첫 자동 리포트 완성. 결과물 예시 + 활용법 5가지는:
   📖 ../결과물-예시.md
      ├ 4 시트 구조 (요약·채널매출·플랫폼ROAS·긴급재고) 미리보기
      ├ 마케터 활용 5가지 (자동화·캠페인 회고·임원 보고·신규 채널·브랜드 표준화)
      ├ Before/After 시간 비교 (190분 → 3~5분, 연 156시간 절감)
      └ 자주 묻는 질문 5개

이걸 발전시키는 3가지 경로:

  A. 정기 자동화 (Part 10):
     - 매주 월요일 09:00 cron 트리거로 자동 실행
     - 디스코드 #marketing 채널에 URL 자동 발송
     - 사용자 명령 0회 · 자동 가동
     - 연 환산 절감: 약 156시간

  B. 다른 MCP 결합:
     - "GA4 MCP 설치하자" → GA4 데이터를 시트에 자동 적재
     - "Discord MCP 설치하자" → 리포트 완료 시 자동 알림

  C. 다음 Part 2 클립:
     - 1-3 GA4 MCP (웹 트래픽 자동 리포트)
     - 1-4 Firecrawl MCP (경쟁사·시장 자동 스크랩)

  D. 본인 데이터로 즉시 따라하기:
     사용자 발화 예: "다음 시트로 주간 리포트 만들어줘: <본인_시트_URL>"
```

---

## ✅ 전체 진행 완료 체크리스트

본 스킬이 끝나면 다음 7개가 모두 만족되어야 클립 1-2 완료:

| # | 검증 항목 | 확인 방법 | 통과 기준 |
|---|---|---|---|
| 1 | OAuth 자격증명 발급 | `cat mcp-server/oauth_credentials.json \| grep installed` | `"installed"` 키 존재 |
| 2 | 의존성 설치 | `ls mcp-server/node_modules/@modelcontextprotocol` | 폴더 존재 |
| 3 | .mcp.json 항목 | `grep google-sheets .mcp.json` | `node mcp-server/index.js` 라인 표시 |
| 4 | MCP 서버 연결 | `claude mcp list \| grep google-sheets` | `✓ Connected` 표시 |
| 5 | OAuth 토큰 발급 | `ls mcp-server/token.json` | 파일 존재 (60일 유효) |
| 6 | 첫 도구 호출 성공 | `"시트 목록 보여줘"` 입력 | 시트 이름·행·열 출력됨 |
| 7 | 결과물 생성 성공 | `"주간 리포트 만들어줘"` 입력 | 새 스프레드시트 URL 수신됨 |

✅ 모두 통과 시 → 학습자는 본인 환경에서 매주 한 줄로 종합 리포트 자동 생성 가능 상태.

## 🚦 단계별 진행 상태 (스킬 내부 추적용)

Claude 는 본 스킬 실행 중 각 단계 완료 시 다음과 같이 진행률을 출력:

```
[1/12 ✓] 사전 점검 (OS·Node·코드)               (10초)
[2/12 ✓] STEP 1: MCP 소개 + 동의                (2분)
[3/12 ✓] STEP 2.1: OAuth 자격증명 발급           (사용자 10분)
[4/12 ✓] STEP 2.2.1: 서버 코드 무결성             (5초)
[5/12 ✓] STEP 2.2.2: oauth_credentials 이동      (10초)
[6/12 ✓] STEP 2.2.3: 의존성 설치 npm install     (1~2분)
[7/12 ✓] STEP 2.3: .mcp.json 등록 확인           (30초)
[8/12 ✓] STEP 2.4: 브라우저 인증 + token.json   (3분)
[9/12 ✓] STEP 2.5.1: MCP 서버 등록 상태          (10초)
[10/12 ✓] STEP 2.5.2: 도구 노출 확인              (10초)
[11/12 ✓] STEP 2.5.3: 첫 도구 실행                (20초)
[12/12 ✓] STEP 4: 결과물 1개 생성 ("start" → 메뉴 → 5번)  (3~5분)

🎉 클립 1-2 Google Sheets MCP 설치 완료 (총 14~16분)
```

각 단계 실패 시 진행 멈추고 트러블슈팅 섹션 안내.

---

## 📝 강의 실습 (실습.md 통합)

> 클립 1-2 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-google-sheets` 스킬을 호출해 OAuth 5단계를 15~20분 안에 설치하고, "start" 단어 → google-sheets 메뉴 → 5번 '자동 리포트' 선택으로 5단계 자동 리포트를 생성한다.

### 실습 첫 결과물 · "start" → 메뉴 5번 시나리오 예시

```
[사용자 발화]
start

[라우터 응답]
🎯 google-sheets · 작업 가능한 업무를 알려드릴게요.
  1. 시트 탐색      "어떤 시트가 있어?"                  5초
  2. 매출 분석      "채널별 매출 비교해줘"               30초
  3. ROAS 분석      "플랫폼별 ROAS + 예산 재배분"        1~2분
  4. 재고 알림      "긴급 상품 빨간 배경 강조"           30초
  5. 자동 리포트 ★  "주간 리포트 새 스프레드시트"        3~5분
어느 업무를 시연해볼까요?

[사용자 발화]
5

[결과물]
🔗 '주간 종합 리포트' 스프레드시트 (4개 시트)
   - 총매출 ₩47,004,000
   - ROAS 857%
   - 긴급재고 3건
   - URL 공유로 팀 즉시 열람 가능
```

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
이커머스 마케팅 데이터 분석가

[입력]
Google Sheets 의 매출·광고·재고 3 시트 (지난주 데이터)

[산출물]
새 스프레드시트 '주간 리포트 {날짜}' (4개 시트)
→ 채널별 매출 분석 + 플랫폼별 ROAS + 재고 긴급 리스트 + 종합 요약
→ Discord #marketing 채널에 URL 자동 발송

[제약]
- 헤더 서식 통일: 파란 배경 #4285f4 + 흰 글씨 + 굵게
- 긴급 항목 빨간 배경 #fce4ec 로 강조
- 분석 인사이트 1줄씩 추가 (수치만 나열 금지)
- 액션 아이템 3개 이내로 제시

[검증]
- 4개 시트 모두 헤더 서식 적용 확인
- 총합 수치가 원본 시트와 ±1% 이내
- Discord URL 클릭 시 정상 열림
- 생성 시간 5분 이내
```

### 응용 과제

1. 본인 광고 데이터를 시트에 넣고 "지난 7일 ROAS 그래프 데이터로 정리" 요청
2. **Part 6 에서 Meta 광고 분석 에이전트가 자동으로 이 시트에 데이터를 적재** · 미리 시트 만들어 두기
3. `format_cells` 도구로 본인 브랜드 색상으로 시트 디자인 표준화

---

## 트러블슈팅 (Google Sheets MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| 브라우저 인증 시 "액세스 차단됨" | STEP 1 ④ 테스트 사용자 미등록 | OAuth 동의 화면 > 테스트 사용자 탭에 본인 이메일 추가 후 재시도 |
| `Cannot find module @modelcontextprotocol/sdk` | npm install 누락 | `cd mcp-server && npm install` 재실행 |
| `Error: ENOENT: oauth_credentials.json` | 파일 위치 오류 | 파일이 `mcp-server/` 폴더 안에 있는지 확인 |
| 다운로드한 JSON 에 `"web"` 키 | "데스크톱 앱" 이 아닌 "웹 애플리케이션" 선택 | STEP 1 ⑤ 다시 진행 (데스크톱 앱 선택) |
| `mcp__google-sheets__*` 도구 안 보임 | `.mcp.json` 경로 오타 또는 Claude 재시작 안 함 | `claude mcp list` 로 등록 확인 + Claude Code 완전 종료 후 재시작 |
| `Quota exceeded for quota metric 'Read requests'` | 분당 60회 초과 | 60초 대기 후 재시도 · 또는 `batch_read_sheet` 사용 |
| `Token has been expired` (60일 미사용) | OAuth 토큰 만료 | `rm mcp-server/token.json` 후 Claude 재시작 → 재인증 |
| `Permission denied` (시트 접근 불가) | 본인 소유 아닌 시트 | 시트 공유 권한에 본인 이메일 추가 또는 본인 시트로 시작 |
| OAuth 후 브라우저 안 닫힘 | 자동 종료 실패 | 수동으로 닫고 Claude 재시작 |
| 한국어 시트 이름 깨짐 | 인코딩 문제 | 시트 이름을 영문으로 변경 또는 시트 ID 사용 |

## 강의 연결

- 본 스킬은 [클립 1-2 Google Sheets MCP 대본](../대본/1-2-google-sheets.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Google Sheets 1 도구에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 [skills/start/SKILL.md](../../../../skills/start/SKILL.md) (라우터: 메뉴 5개 → 선택 시연) 가 이어받아 활용. google-sheets 분기의 5번이 자동 리포트.
- Part 10 의 `weekly-sheets-reporter` 같은 자동화 에이전트가 본 스킬로 설치된 MCP 를 cron 스케줄로 호출.
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/01-google-sheets/mcp설치-google-sheets/`) · 클립과 함께 자체 보관.

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| 자체 호스팅 서버 위치 | `marketing-os/mcp-server/index.js` |
| OAuth 자격증명 파일 | `mcp-server/oauth_credentials.json` (gitignore) |
| OAuth 토큰 파일 | `mcp-server/token.json` (gitignore, 자동 생성) |
| OAuth 클라이언트 타입 | 데스크톱 앱 (Desktop App) |
| 의존성 패키지 | `@modelcontextprotocol/sdk`, `googleapis` |
| API key 발급 URL | <https://console.cloud.google.com/apis/credentials> |
| Google Sheets API URL | <https://console.cloud.google.com/apis/library/sheets.googleapis.com> |
| 무료 한도 | 분당 60회 (`Quota: Read requests per minute per user`) |
| 토큰 자동 갱신 | 60일 이내 사용 시 자동. 만료 시 token.json 삭제 후 재인증 |

## 메모리·문서 연결

- 사용자의 스프레드시트 ID 는 `.env` 의 `GOOGLE_SHEETS_DEFAULT_ID` 에 저장 (선택)
- 자주 사용하는 시트 이름은 메모리로 저장하지 말기 (사용자가 매번 다를 수 있음)
- 본 스킬 종료 후 사용자가 "주간 리포트 자동화 등록하자" 라고 하면 Part 10 의 `/agent-builder` 스킬로 전달
