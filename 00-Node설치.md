# Node.js · npm 설치 (MCP 연결 실패 1순위 원인)

> **MCP 서버가 연결이 안 될 때 가장 먼저 확인할 것.**
> Firecrawl · 네이버 데이터랩 · YouTube · Buffer · GA4 · Meta/Google Ads MCP 는 전부
> `npx` 명령으로 실행됩니다. `npx` 는 Node.js 에 딸려오는 도구라서,
> **Node.js 가 없으면 이 MCP 들은 전부 조용히 연결에 실패합니다.**

---

## 1. 내 증상이 이건가? (30초 진단)

아래 중 하나라도 해당되면 Node.js 문제입니다.

| 증상 | 어디서 보이나 |
|---|---|
| `/mcp` 목록에 firecrawl·naver 가 **아예 안 보임** | Claude Code 안에서 `/mcp` 입력 |
| 목록에 뜨는데 `failed` · `✗ Failed to connect` | 같은 화면 |
| "Firecrawl 로 가져와줘" 했더니 클로드가 그냥 웹 검색으로 대체 | 대화 중 |
| 터미널에 `npx: command not found` | 설치 명령 실행 시 |
| 터미널에 `node: command not found` | 아래 2번 확인 시 |

> ⚠️ **Claude Code 가 잘 돌아가니까 Node 도 깔려 있겠지 — 아닙니다.**
> Claude Code 를 공식 설치 스크립트(네이티브 설치)로 깔았다면 Node.js 없이도 작동합니다.
> 이 경우 Claude Code 는 멀쩡한데 npx 기반 MCP 만 전부 실패합니다. 수강생 실패 사례 대부분이 이 경우입니다.

---

## 2. 확인 (10초)

터미널(macOS: 터미널 / Windows: PowerShell)에 붙여넣기:

```bash
node --version
npm --version
```

**정상**
```
v22.14.0        ← v18 이상이면 OK (v22 이상 권장)
10.9.2
```

**설치 필요**
```
zsh: command not found: node          ← macOS
'node'은(는) 내부 또는 외부 명령... ← Windows
```

버전이 `v18` 미만(`v16`, `v14` 등)이어도 3번으로 진행하세요. 구버전은 MCP 패키지가 실행되지 않습니다.

---

## 3. 설치

### macOS

**방법 A · 공식 설치 파일 (권장 · 터미널 몰라도 됨)**
1. <https://nodejs.org> 접속
2. 왼쪽 **LTS** 버튼 클릭 → `.pkg` 파일 다운로드
3. 파일 더블클릭 → 계속 → 동의 → 설치 (비밀번호 입력)
4. **터미널을 완전히 종료 후 다시 열기** ⚠️ 안 하면 계속 not found

**방법 B · Homebrew (이미 brew 쓰는 경우)**
```bash
brew install node@22
brew link --overwrite node@22
```

### Windows

**방법 A · 공식 설치 파일 (권장)**
1. <https://nodejs.org> 접속
2. **LTS** 버튼 클릭 → `.msi` 파일 다운로드
3. 파일 실행 → Next → 라이선스 동의 → **`Add to PATH` 체크 확인**(기본 체크됨) → Install
4. **PowerShell 을 완전히 종료 후 다시 열기** ⚠️ 필수

**방법 B · winget**
```powershell
winget install OpenJS.NodeJS.LTS
```

### 설치 후 재확인

```bash
node --version    # v22.x.x
npm --version     # 10.x.x
```

---

## 4. Node 를 깔았는데도 MCP 가 안 붙을 때

순서대로 확인하세요.

**① Claude Code 를 완전히 재시작했는가**
탭만 닫은 게 아니라 프로그램 종료(macOS `⌘Q`) 후 재실행. MCP 서버는 시작할 때만 뜹니다.

**② 패키지가 실제로 받아지는가**
```bash
npx -y firecrawl-mcp --help
```
처음엔 다운로드가 있어 10~30초 걸립니다. 여기서 에러가 나면 MCP 문제가 아니라 네트워크·프록시 문제입니다.

**③ `.env` 키가 실제로 읽히는가**
```bash
grep FIRECRAWL_API_KEY .env      # 값이 비어 있지 않은지
grep NAVER_CLIENT_ID .env
```

**④ 회사 노트북 · 사내망이라면**
`npx` 가 npm 저장소(registry.npmjs.org)에 접속하지 못해 막히는 경우가 있습니다.
```bash
npm config get proxy
npm ping
```
`npm ping` 이 실패하면 사내 프록시 설정이 필요합니다 (IT 담당자 문의 또는 개인 네트워크에서 1회 설치).

**⑤ macOS 에서 권한 오류(`EACCES`)**
```bash
sudo chown -R $(whoami) ~/.npm
```

---

## 5. 자주 나오는 오류 메시지

| 메시지 | 원인 | 해결 |
|---|---|---|
| `npx: command not found` | Node.js 미설치 | 3번 설치 |
| `node: command not found` | 같음 (또는 PATH 누락) | 3번 설치 + 터미널 재시작 |
| `Unsupported engine` / `requires Node >=18` | Node 구버전 | 3번으로 LTS 재설치 |
| `EACCES: permission denied` | npm 캐시 권한 | `sudo chown -R $(whoami) ~/.npm` |
| `ETIMEDOUT` / `ECONNREFUSED` | 사내망·프록시 차단 | 4번 ④ |
| `MCP server "firecrawl" failed to connect` | 위 전부의 결과 | 1→4 순서대로 |

---

## 6. Node 가 필요한 MCP / 필요 없는 MCP

| Node 필요 (npx 실행) | Node 불필요 |
|---|---|
| Firecrawl · 네이버 데이터랩 · YouTube Data · Buffer · GA4 · Meta/Google Ads | Figma · Notion · Higgsfield (Claude.ai 커넥터 = 브라우저 OAuth) |
| Google Sheets (`npm install` 필요) | 네이버 검색광고 (python3 스크립트) |

즉 **커넥터 3종(Figma·Notion·Higgsfield)만 되고 나머지가 전부 안 된다면 Node.js 문제가 거의 확실합니다.**

---

## 참고

- 전체 사전 준비물: [00-사전준비물.md](00-사전준비물.md)
- 통합 설치: [MCP-통합설치/](MCP-통합설치/)
