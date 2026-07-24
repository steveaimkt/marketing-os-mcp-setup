# 12 · 네이버 (데이터랩 + 검색광고)

> ⚠️ **네이버는 완전히 다른 두 API 세계**가 있습니다. 혼동하면 설치가 안 됩니다.
> - **A. 데이터랩 (DataLab)** = 검색어 트렌드·쇼핑인사이트 → `developers.naver.com` → **npm MCP (Node.js 필요)**
> - **B. 검색광고 (SearchAd)** = 광고비·ROAS·키워드 검색량 → `manage.searchad.naver.com` → **REST (공식 MCP 없음 · Python)**

| | 데이터랩 | 검색광고 |
|---|---|---|
| 답하는 질문 | "이 키워드 요즘 뜨나?" | "이 키워드에 얼마 쓰고 얼마 벌었나?" |
| 발급처 | developers.naver.com | manage.searchad.naver.com |
| 연결 방식 | MCP (`naver-datalab-mcp-server`) | REST 서명 호출 (`scripts/naver_searchad.py`) |
| **Node.js** | **필요** ⚠️ | 불필요 (python3) |
| 광고 계정 | 불필요 | 필요 |

설치는 [`mcp설치-naver/SKILL.md`](mcp설치-naver/SKILL.md) 가 단계별로 안내합니다.
Claude Code 에서 **"네이버 MCP 설치하자"** 라고 입력하세요.

---

## A. 데이터랩 DataLab (MCP · 검색어·쇼핑 트렌드)

**0. Node.js 확인** ⚠️ 이걸 건너뛰어서 실패하는 사례가 가장 많습니다
```bash
node --version    # v18 이상이어야 함
```
`command not found` 면 → [00-Node설치.md](../00-Node설치.md) 먼저 처리.

**1. 키 발급** (약 3분)
1. <https://developers.naver.com> → 로그인 → **Application → 애플리케이션 등록**
2. 사용 API에서 **「데이터랩(검색어트렌드)」 + 「데이터랩(쇼핑인사이트)」 둘 다 체크** ⚠️ 하나만 체크하면 절반이 안 됨
3. 등록 후 **Client ID · Client Secret** 발급

**2. `.env` 등록**
```bash
NAVER_CLIENT_ID=발급받은_클라이언트_ID
NAVER_CLIENT_SECRET=발급받은_시크릿
```

**3. `.mcp.json` 등록** (패키지 `naver-datalab-mcp-server`)
```json
"naver-datalab": {
  "command": "bash",
  "args": ["-c", "set -a; source \"${CLAUDE_PROJECT_DIR:-$PWD}/.env\"; set +a; exec npx -y naver-datalab-mcp-server"]
}
```
> 경로를 절대경로로 박지 마세요. 위 형태는 클론 위치가 어디든 동작합니다.

**4. 검증** — Claude Code 완전 재시작 후
> "네이버 데이터랩으로 '마케팅 자동화' 검색 트렌드 뽑아줘"

시계열 데이터가 나오면 성공입니다.

**할 수 있는 것**: 검색어 트렌드(시계열·성별·연령·디바이스), 쇼핑인사이트(분야·키워드 트렌드)
**못 하는 것**: 광고 성과(ROAS·광고비) → 아래 B가 필요합니다.

---

## B. 검색광고 SearchAd (REST · 광고 성과)

> 공식 MCP가 없어 REST 서명 호출을 씁니다. 구현체는 `scripts/naver_searchad.py`(의존성 0)라 **별도 설치 불필요**하고 **Node.js 도 불필요**합니다.

**1. 키 발급** (약 3분 · 광고 계정 필요)
1. <https://manage.searchad.naver.com> 로그인
2. **도구 → API 사용 관리** → 3개 발급
   - `API_KEY` (액세스 라이선스)
   - `SECRET_KEY` (`AQAA...==` 형태)
   - `CUSTOMER_ID` (계정 번호, 숫자)

**2. `.env` 등록**
```bash
NAVER_SEARCHAD_API_KEY=액세스_라이선스
NAVER_SEARCHAD_SECRET_KEY=비밀키
NAVER_SEARCHAD_CUSTOMER_ID=계정번호
```

**3. 검증**
```bash
python3 scripts/naver_searchad.py GET /ncc/campaigns
```
`HTTP 200`이면 성공입니다. 빈 배열 `[]`은 **광고 미집행 계정**이라는 뜻이고 인증 자체는 정상입니다.

**인증 방식(참고)**: HMAC-SHA256 · 서명 `Base64(HMAC(SECRET, "{ms타임스탬프}.{METHOD}.{path}"))` · 헤더 `X-Timestamp·X-API-KEY·X-Customer·X-Signature`

---

## 자주 막히는 지점

| 증상 | 원인·해결 |
|---|---|
| **데이터랩 MCP 가 목록에 아예 안 뜸 / `failed to connect`** ★ | **Node.js 미설치** — `node --version` 확인 → [00-Node설치.md](../00-Node설치.md) |
| `npx: command not found` | 동일 (Node.js 미설치) |
| 데이터랩 MCP가 빈 값/인증 오류 | `.env`에 `NAVER_CLIENT_ID/SECRET`이 없거나 오타. **SearchAd 키와 혼동 주의**(별개 인증) |
| 애플리케이션 등록했는데 트렌드가 안 나옴 | 사용 API에 **데이터랩 2종을 체크**하지 않음 → 애플리케이션 설정에서 추가 |
| `.env` 는 채웠는데 계속 인증 오류 | Claude Code 를 완전 종료(⌘Q) 후 재시작했는지 확인 |
| SearchAd `HTTP 401` | `SECRET_KEY` 끝의 `==`까지 정확히 복사했는지 확인 |
| SearchAd `[]` 빈 결과 | 정상(광고 미집행). 인증 성공 상태 |
| 둘 중 뭘 써야 할지 모르겠음 | 트렌드·시장조사 = **데이터랩** / 광고비·ROAS = **검색광고** |
