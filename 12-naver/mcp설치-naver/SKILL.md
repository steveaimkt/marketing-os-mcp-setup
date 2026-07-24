---
name: mcp설치-naver
description: |
  네이버 데이터랩(MCP) + 네이버 검색광고(REST) 설치 스킬. 둘은 인증도 발급처도 완전히 다른 별개 시스템이라 혼동이 잦음 — 이 스킬은 그 구분부터 잡고 필요한 쪽만 설치한다. 데이터랩은 `npx -y naver-datalab-mcp-server` 로 동작해 Node.js 가 필수이며, 미설치가 연결 실패 1순위 원인이라 STEP 0 에서 먼저 막는다.

  자동 호출 트리거:
  - **"네이버 MCP 설치하자"** ⭐ 주요 트리거
  - "네이버 데이터랩 연결" / "데이터랩 MCP 설치"
  - "네이버 검색광고 API 연결" / "네이버 ROAS 보고 싶어"
  - "네이버 트렌드 뽑고 싶어" / "네이버 키워드 검색량"

  4단계:
  ① 어느 쪽이 필요한지 판별 (데이터랩 / 검색광고 / 둘 다) →
  ② STEP 0 Node.js 확인 (데이터랩 선택 시 필수) →
  ③ 키 발급 + .env + .mcp.json 등록 →
  ④ 헬스 체크 (트렌드 1건 또는 캠페인 목록 HTTP 200)

  특이점: 데이터랩은 광고 성과를 못 주고, 검색광고는 트렌드를 못 준다. 사용자가 원하는 게 "요즘 뜨는 키워드"면 데이터랩, "얼마 쓰고 얼마 벌었나"면 검색광고.
---

# 네이버 MCP 설치 (데이터랩 + 검색광고)

## 🎬 스킬 시작 시 메시지

```
🟢 네이버 연결을 시작합니다.

먼저 짚고 갈 게 있어요. 네이버는 이름만 같지 완전히 다른 두 시스템이에요.

  A. 데이터랩 (DataLab)    → "이 키워드 요즘 뜨나?"        · 검색어·쇼핑 트렌드
  B. 검색광고 (SearchAd)   → "얼마 쓰고 얼마 벌었나?"      · 광고비·ROAS·검색량

  ⚠️ 키가 서로 호환되지 않습니다. 데이터랩 키로 광고 성과를 못 보고, 그 반대도 안 됩니다.
  실습에서 가장 많이 헤매는 지점이라 먼저 정합니다.

────────────────────────────────

  A 데이터랩만    · 3분 · 광고 계정 불필요 · Node.js 필요
  B 검색광고만    · 3분 · 광고 계정 필요   · Node.js 불필요 (python3)
  C 둘 다         · 6분

어느 쪽이 필요하세요? (A / B / C)
```

- **A 또는 C** → STEP 0 (Node.js) → STEP A
- **B** → STEP B 로 바로 (Node.js 불필요)

---

## ⚠️ STEP 0: Node.js 확인 (데이터랩 선택 시 필수 · 30초)

> 데이터랩 MCP 는 `npx -y naver-datalab-mcp-server` 로 실행됩니다.
> **Node.js 가 없으면 Client ID·Secret 을 아무리 정확히 넣어도 연결되지 않습니다.**
> 실습 실패 사례 1순위라 키 발급보다 **먼저** 확인합니다.

클로드 자동 실행:

```bash
node --version && npm --version
```

| 결과 | 조치 |
|---|---|
| `v18` 이상 + npm 버전 출력 | ✅ STEP A 로 진행 |
| `command not found` | ⛔ 아래 안내 출력 후 설치 완료까지 대기 |
| `v16` 이하 구버전 | ⛔ 동일 (구버전은 패키지 실행 실패) |

⚠️ **Claude Code 가 돌아간다고 Node 가 깔린 건 아닙니다.** 네이티브 설치 스크립트로 Claude Code 를 깔았다면 Node 없이도 작동하며, 이 경우 npx 기반 MCP 만 전부 실패합니다.

미설치 시 사용자에게 안내:

```
Node.js 가 필요합니다 (약 3분).

  macOS   → https://nodejs.org → 왼쪽 LTS 버튼 → .pkg 다운로드 → 더블클릭 설치
  Windows → https://nodejs.org → LTS 버튼 → .msi 다운로드 → 실행
            (설치 중 "Add to PATH" 체크 확인 · 기본값으로 체크되어 있음)

설치 후 ⚠️ 터미널(또는 PowerShell)을 완전히 종료했다가 다시 열어주세요.
안 그러면 계속 command not found 가 납니다.

다 되면 "설치했어" 라고 알려주세요.
```

설치 후 `node --version` 재확인 → **통과해야 STEP A 진행.**
자세한 진단: [00-Node설치.md](../../00-Node설치.md)

---

## 🅰️ STEP A: 데이터랩 (검색어·쇼핑 트렌드)

### A.1 키 발급 (사용자 직접 · 약 3분)

```
① https://developers.naver.com 접속 → 네이버 계정 로그인
② 상단 "Application" → "애플리케이션 등록"
③ 애플리케이션 이름 입력 (예: marketing-os)
④ 사용 API 선택 ⚠️ 여기가 핵심
     ☑ 데이터랩 (검색어트렌드)
     ☑ 데이터랩 (쇼핑인사이트)
   → 두 개 다 체크하세요. 하나만 하면 절반이 작동 안 합니다.
⑤ 환경 추가 → "WEB 설정" 선택 → 서비스 URL 에 http://localhost 입력
⑥ 등록 완료 → "내 애플리케이션" 에서 Client ID · Client Secret 확인
```

두 값을 클로드에게 전달.

### A.2 `.env` 등록 (클로드 자동 · 30초)

```bash
PRJ="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PRJ"

grep -q "NAVER_CLIENT_ID" .env 2>/dev/null || cat >> .env <<'EOF'
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
EOF

# 검증 (값이 비어 있지 않은지)
grep "^NAVER_CLIENT_" .env
```

⚠️ 기존 값이 있으면 덮어쓰지 않는다. 비어 있을 때만 채운다.

### A.3 `.mcp.json` 등록 (클로드 자동 · 30초)

`mcpServers` 에 추가:

```json
"naver-datalab": {
  "_part": "12 네이버 데이터랩 · 검색어/쇼핑 트렌드",
  "command": "bash",
  "args": ["-c", "set -a; source \"${CLAUDE_PROJECT_DIR:-$PWD}/.env\"; set +a; exec npx -y naver-datalab-mcp-server"]
}
```

> **절대경로를 박지 말 것.** 위 형태는 클론 위치가 사람마다 달라도 동작한다.
> `env` 블록에 `${NAVER_CLIENT_ID}` 를 직접 쓰는 방식은 VSCode 확장 Claude Code 에서 빈 값이 되는 사례가 있어, `.env` 를 `source` 하는 위 패턴을 쓴다 (firecrawl·buffer 와 동일).

JSON 검증:
```bash
python3 -c "import json; json.load(open('.mcp.json'))" && echo "✓ JSON OK"
```

### A.4 헬스 체크 (1분)

```
Claude Code 를 완전 종료(⌘Q / 창 닫기 아님) 후 재시작하세요.

새 세션에서:
  "네이버 데이터랩으로 '마케팅 자동화' 최근 3개월 검색 트렌드 뽑아줘"
```

시계열 숫자가 나오면 성공. `/mcp` 목록에 `naver-datalab` 이 **Connected** 로 보이는지도 확인.

---

## 🅱️ STEP B: 검색광고 (광고비·ROAS·검색량)

> Node.js 불필요. python3 만 있으면 됩니다 (macOS·대부분 Windows 에 기본 포함).

### B.1 키 발급 (사용자 직접 · 약 3분 · 광고 계정 필요)

```
① https://manage.searchad.naver.com 로그인
② 상단 "도구" → "API 사용 관리"
③ "네이버 검색광고 API 라이선스" 발급 → 3개 값 확보
     · API_KEY      (액세스 라이선스)
     · SECRET_KEY   (AQAA...== 형태 · 끝의 == 까지 전부 복사)
     · CUSTOMER_ID  (계정 번호 · 숫자)
```

⚠️ **가장 흔한 실수**: `SECRET_KEY` 끝 `==` 를 빼먹고 복사 → `HTTP 401`.

### B.2 `.env` 등록 (클로드 자동)

```bash
NAVER_SEARCHAD_API_KEY=액세스_라이선스
NAVER_SEARCHAD_SECRET_KEY=비밀키
NAVER_SEARCHAD_CUSTOMER_ID=계정번호
```

### B.3 헬스 체크

```bash
python3 scripts/naver_searchad.py GET /ncc/campaigns
```

| 응답 | 의미 |
|---|---|
| `HTTP 200` + 캠페인 배열 | ✅ 성공 |
| `HTTP 200` + `[]` | ✅ 인증 성공 (광고 미집행 계정일 뿐) |
| `HTTP 401` | ✗ SECRET_KEY 오타 (`==` 확인) |
| `HTTP 403` | ✗ CUSTOMER_ID 불일치 |

**인증 방식(참고)**: HMAC-SHA256 · 서명 `Base64(HMAC(SECRET, "{ms타임스탬프}.{METHOD}.{path}"))` · 헤더 `X-Timestamp·X-API-KEY·X-Customer·X-Signature`

> `scripts/naver_searchad.py` 는 marketing-os 배포판에 포함된 의존성 0 스크립트입니다. 이 저장소만 클론한 경우 해당 스크립트가 없으므로 데이터랩(A)만 진행하세요.

---

## 📋 STEP 3: 무엇을 할 수 있나

| 질문 | 어느 쪽 | 예시 명령 |
|---|---|---|
| 이 키워드 요즘 뜨나? | 데이터랩 | "'제로 슈가' 최근 1년 검색 트렌드" |
| 20대 여성이 많이 찾나? | 데이터랩 | "'비건 화장품' 성별·연령별 트렌드" |
| 어떤 쇼핑 분야가 성장 중? | 데이터랩 | "화장품/미용 분야 쇼핑인사이트 3개월" |
| 광고비 대비 매출은? | 검색광고 | "지난달 캠페인별 ROAS 정리" |
| 이 키워드 월 검색량은? | 검색광고 | "'마케팅 자동화' 월간 검색수·경쟁도" |
| 브랜드 검색과 일반 검색 분리 | 검색광고 | "브랜드 키워드 제외한 ROAS 다시" |

조합: 데이터랩으로 **뜨는 키워드**를 찾고 → 검색광고로 **그 키워드에 돈이 되는지** 확인하는 흐름이 실무 기본형입니다.

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| **`naver-datalab` 이 목록에 없음 / `failed to connect`** ★ | **Node.js 미설치** (1순위) | `node --version` → not found 면 <https://nodejs.org> LTS 설치 후 터미널 재시작. [00-Node설치.md](../../00-Node설치.md) |
| `npx: command not found` | 동일 | 위와 같음 |
| `.env` 채웠는데 인증 오류 | Claude Code 재시작 안 함 | 완전 종료(⌘Q) 후 재실행 |
| 트렌드는 되는데 쇼핑인사이트가 안 됨 | 애플리케이션 사용 API 에 쇼핑인사이트 미체크 | developers.naver.com → 내 애플리케이션 → API 설정에서 추가 |
| 데이터랩 키로 광고 성과 요청 → 실패 | 별개 시스템 | STEP B 로 검색광고 키 별도 발급 |
| SearchAd `HTTP 401` | SECRET_KEY 끝 `==` 누락 | 전체 재복사 |
| SearchAd `[]` | 광고 미집행 (정상) | 인증은 성공한 상태 |
| `ETIMEDOUT` / `npm ping` 실패 | 사내망 프록시가 npm 저장소 차단 | 개인 네트워크에서 1회 실행해 캐시 생성 |

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| 데이터랩 MCP 패키지 | `naver-datalab-mcp-server` (icraft2170/naver-data-mcp-server) |
| Node.js 최소 버전 | 18 (`node --version`) |
| 데이터랩 발급처 | <https://developers.naver.com> |
| 데이터랩 환경변수 | `NAVER_CLIENT_ID` · `NAVER_CLIENT_SECRET` |
| 검색광고 발급처 | <https://manage.searchad.naver.com> (도구 → API 사용 관리) |
| 검색광고 환경변수 | `NAVER_SEARCHAD_API_KEY` · `NAVER_SEARCHAD_SECRET_KEY` · `NAVER_SEARCHAD_CUSTOMER_ID` |
| 검색광고 구현 | `scripts/naver_searchad.py` (의존성 0 · python3) |
| 검색광고 인증 | HMAC-SHA256 서명 |
