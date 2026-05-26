---
name: mcp설치-figma
description: |
  Part 2 클립 2-1 Figma MCP **통합 진입점**. 자체호스팅 Talk To Figma MCP Plugin 설치 +
  WebSocket 브릿지(port 3055) + Figma Desktop 플러그인 연결 + 카드뉴스 흐름 진입까지 한 흐름.
  Figma 공식 호스팅 MCP 의 한 달 6번 사용 제약 우회. 디자인 생성·수정 가능.
  **이미 설치돼 있으면** 환경 점검 후 곧바로 채널 연결 → /카드뉴스 스킬로 핸드오프.

  자동 호출 트리거:
  - **"피그마 mcp 시작하자"** ⭐ 통합 진입 (설치 + 카드뉴스까지)
  - **"Figma MCP 설치하자"** ⭐ 설치 강조
  - "피그마 MCP 설치" / "피그마 시작" / "Figma 시작"
  - "talk to figma 설치"
  - "Figma WebSocket 연결"
  - "디자인 자동화 환경 만들자"
  - "Part 2 / 2-1 설치 시작"

  흐름 (상태 자동 라우팅, **빠진 단계는 묻지 않고 즉시 자동 진행**):
  Step 0. 환경 점검 — 서버·플러그인·MCP 도구 상태 감지
    ├ 미설치 → Step 1~5 (사전점검 → 설치 → MCP등록 → 플러그인 → 결과물1개)
    └ 설치됨 → 소켓 미기동 시 백그라운드 자동 기동 → Step 6 으로 점프
  Step 6. 채널 ID 받기 → join_channel + 3단 검증 (read→write→delete) 자동 → /카드뉴스 핸드오프

  특이점: WebSocket 브릿지 (Claude ↔ MCP ↔ WS ↔ Figma Plugin). 사용 횟수 제한 없음. 보기 전용 계정 OK.
---

# Part 2 / 2-1 Figma MCP 설치 (클립 전용)

> 본 스킬은 **Talk To Figma MCP Plugin** (자체호스팅 패키지) 을 설치하고 Figma Desktop 플러그인 + WebSocket 서버를 한 흐름에 연결한다.
> Figma 공식 호스팅 MCP (mcp.figma.com) 와 달리 **사용 횟수 제한 없음 + 보기 전용 계정도 OK + 디자인 생성·수정 가능**.

## 🎬 스킬 시작 시 메시지

```
🎨 Figma MCP 가동을 시작합니다.

이 스킬은 두 단계를 한 흐름으로 진행해요:
  1단계: 설치 — talk-to-figma 자체호스팅 (WebSocket 브릿지) 환경 셋업
  2단계: 카드뉴스 제작 — /카드뉴스 스킬로 자동 핸드오프 (레퍼런스→기획→디자인)

────────────────────────────────
왜 자체호스팅인가:

  Talk To Figma MCP Plugin (Claude ↔ MCP ↔ WebSocket(3055) ↔ Figma Plugin)
  · 사용 횟수 제한 없음 (Figma 공식 호스팅은 보기 전용 계정 한 달 6번 제약)
  · 디자인 생성·수정·요소 편집 모두 가능 (공식 호스팅은 주로 읽기)
  · 도구 약 60개 (생성 11 + 수정 9 + 텍스트 12 + 컴포넌트 3 + 페이지 5 + 문서 8 등)
  · 마케터 활용 시나리오 (카드뉴스·캠페인 배너·로그인 페이지) 모두 가능

────────────────────────────────
먼저 Step 0 (환경 점검) 으로 현재 상태부터 확인합니다.
이미 설치된 부분은 건너뛰고, 빠진 단계만 안내해요.
```

→ Step 0 (환경 점검) 으로 진행.

---

## Step 0. 환경 점검 (자동 라우팅)

사용자에게 묻기 전에 아래 6가지를 자동 확인하고, **빠진 항목만** 보완 단계로 안내한다.

| # | 항목 | 확인 방법 | 통과 의미 |
|---|---|---|---|
| 1 | Figma Desktop · Node · Bun | `ls /Applications/Figma.app && node -v && which bun` | Step 1 통과 |
| 2 | 패키지 빌드 산출물 | `ls ~/dev/claude-talk-to-figma-mcp/dist/talk_to_figma_mcp/server.js` | Step 2 통과 |
| 3 | `.mcp.json` 에 figma 서버 | `grep '"figma"' .mcp.json` | Step 3 통과 |
| 4 | `mcp__figma__*` 도구 로드 | `ToolSearch select:mcp__figma__join_channel` 로 존재 확인 | Claude 세션에 도구 활성 |
| 5 | WebSocket 서버 (3055) | `curl -s http://localhost:3055/status` 응답 OK | 서버 가동 중 |
| 6 | 플러그인 연결 (activeConnections ≥ 1) | status 응답의 `stats.activeConnections` | Figma Desktop 측 플러그인 실행 + 채널 보유 |

### 결과에 따른 분기

상태 표를 사용자에게 보여주고 다음 중 하나로 분기:

- **1~6 모두 ✓** → 상태 1줄 보고 후 **즉시 Step 6** 진입 (채널 ID 요청). 별도 확인 없음.
- **1~5 ✓, 6 ✗ (플러그인 미연결)** → 사용자에게 Figma Desktop 에서 플러그인 실행 + 채널 ID 안내 → **Step 6**
- **1~4 ✓, 5 ✗ (서버 안 떠 있음)** → **즉시** `cd ~/dev/claude-talk-to-figma-mcp && bun socket` 을 `run_in_background: true` 로 기동 → `lsof -nP -iTCP:3055` 로 LISTEN 확인 → 플러그인 실행 안내 → **Step 6**
- **3 ✗ (.mcp.json 미등록)** 또는 **4 ✗ (도구 미로드)** → Step 3 부터 진행 (등록 후 Claude Code 재시작 안내 필요)
- **2 ✗ (패키지 미설치)** → Step 1 부터 정식 진행
- **1 ✗ (사전 준비물 부족)** → Step 1 에서 사용자에게 설치 안내

> **자동 진행 원칙**: 빠진 단계 중 **사용자 액션이 필요 없는 항목** (소켓 기동, MCP 도구 검증, 채널 join, 3단 검증) 은 묻지 않고 즉시 실행. **사용자 액션이 필요한 항목** (Figma Desktop 플러그인 실행 → 채널 ID 발급, .mcp.json 등록 후 재시작) 에서만 멈춰서 안내한다.

---

## Step 1. 사전 준비물 (3가지)

```
✅ 필수 체크리스트
  □ Figma Desktop 앱 설치됨 (https://www.figma.com/downloads/)
  □ Node.js 설치됨 (v18+ 권장)
  □ Bun 설치됨 (없으면 npx 가 자동 설치 시도)
  □ Figma 계정 (무료 요금제 OK · 계정 종류 무관)
```

확인 명령:

```bash
which node && node --version  # v18 이상이면 OK
which bun                       # 없으면 다음 단계에서 자동 설치
ls /Applications/Figma.app      # Figma Desktop 설치 확인
```

→ 모두 OK 면 Step 2.

---

## Step 2. Talk To Figma MCP Plugin 패키지 설치 (1줄)

설치 폴더 선택 후 한 줄 실행:

```bash
# 원하는 폴더로 이동 (예: marketing-os 옆)
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Desktop/0.마케터를\ 위한\ 클로드코드

# 한 줄 설치 (git clone + Bun 의존성 + WebSocket 서버 자동 기동)
npx claude-talk-to-figma-mcp
```

`npx` 가 자동으로 다음 5가지를 수행 :
1. GitHub 에서 `arinspunk/claude-talk-to-figma-mcp` 클론
2. Bun 런타임 자동 감지·설치 (없으면)
3. TypeScript 빌드 (`bun run build`)
4. WebSocket 서버 기동 (`bun socket` · port 3055)
5. 상태 확인 URL 출력 : `http://localhost:3055/status`

> 💡 수동 방식 선호 시 :
> ```bash
> git clone https://github.com/arinspunk/claude-talk-to-figma-mcp.git
> cd claude-talk-to-figma-mcp
> bun install
> bun run build
> bun socket
> ```

---

## Step 3. Claude Code 에 MCP 등록

`marketing-os/.mcp.json` 에 다음 항목 추가 :

```json
{
  "mcpServers": {
    "figma": {
      "command": "bun",
      "args": [
        "run",
        "<설치_경로>/claude-talk-to-figma-mcp/dist/talk_to_figma_mcp/server.js"
      ]
    }
  }
}
```

`<설치_경로>` 는 Step 2 에서 `npx` 가 클론한 폴더 (보통 현재 디렉토리 아래 `claude-talk-to-figma-mcp/`).

또는 DXT 패키지 방식 (Claude Desktop only) :

1. https://github.com/arinspunk/claude-talk-to-figma-mcp/releases 에서 최신 `.dxt` 다운로드
2. `.dxt` 파일 더블클릭 → Claude Desktop 자동 설치
3. Claude Desktop 재시작

등록 검증 :

```bash
claude mcp list | grep figma
# figma: bun run .../server.js - ✓ Connected
```

---

## Step 4. Figma Plugin 임포트 + 채널 연결

### 4-1. 플러그인 임포트 (Figma Desktop 에서)

1. Figma Desktop 앱 실행
2. 메뉴 `Plugins` → `Development` → `Import plugin from manifest...`
3. 파일 선택 : `<설치_경로>/claude-talk-to-figma-mcp/src/claude_mcp_plugin/manifest.json`
4. 임포트 완료 후 디자인 파일 1개 열고 `Plugins` → `Development` → `Claude MCP Plugin` 실행

### 4-2. 채널 ID 발급

플러그인 창에서 자동으로 channel ID 가 표시됨 (예: `channel-abc123`).

### 4-3. Claude Code 에서 연결

```
> Talk to Figma, channel channel-abc123
```

Claude 가 응답 :

```
✅ Connected to Figma channel channel-abc123.
   Document: 본인 파일명
   Pages: N
   Ready to create / modify designs.
```

---

## Step 5. 결과물 1개 직접 만들기 (자연어로 디자인 생성)

연결 검증 + 첫 디자인 생성을 한 번에 :

```
> 다크모드 로그인 페이지를 만들어줘:
   - 1440x900 프레임
   - 중앙에 로그인 카드 (480x520, radius 16)
   - 헤드라인 "Welcome back" (32pt, white)
   - 이메일·비밀번호 input 2개
   - 파란 로그인 버튼 (480x56, radius 8)
   - 배경은 진한 네이비 #0F172A
```

Claude 가 약 30초~1분 내 Figma 화면에 디자인을 직접 그려냅니다. 호출 도구 (자동) :

- `create_frame` × 2 (배경 · 로그인 카드)
- `create_text` × 4 (헤드라인 · placeholder × 2 · 버튼 텍스트)
- `create_rectangle` × 3 (input × 2 · 버튼)
- `set_fill_color` × N
- `set_corner_radius` × N
- `set_auto_layout` × 1 (카드 정렬)

---

## Step 6. 채널 연결 + 카드뉴스 흐름 진입

설치(Step 1~5)가 끝났거나 Step 0 에서 점프해 온 경우, **여기가 카드뉴스 제작으로 넘어가는 다리.**

### 6-1. 채널 연결 + 3단 자동 검증

> **사용자에게 묻는다**: "Figma 플러그인 창에 표시된 channel ID 를 알려주세요."
>   (보통 8자 임의 문자열. 플러그인 창 우측 상단 또는 본문에 노출.)

받은 ID 로 즉시 **3단 검증 자동 실행** (사용자 확인 없이 연달아 호출):

| 단계 | 호출 | 검증 의미 |
|---|---|---|
| ① join | `mcp__figma__join_channel({ channel: "<ID>" })` | 소켓·채널 라이브 |
| ② read | `mcp__figma__get_document_info()` | 파일 접근 OK · 페이지·노드 수 표시 |
| ③ write | `mcp__figma__create_text({ x:100, y:100, text:"connection-test", parentId:"<page-id>" })` | 편집 권한 OK |
| ④ delete | `mcp__figma__delete_node({ nodeId:"<just-created>" })` | 흔적 제거 + 정리 |

- ① 실패 ("Failed to verify connection...") → 플러그인이 그 채널에 없는 상태. **Figma Desktop 에서 플러그인 재실행** 안내 + 새 ID 받기. 임의 재시도 금지.
- ③ timeout (`write timeout`) → 파일이 view-only 거나 parentId 누락. 사용자에게 **편집 권한 있는 파일 열기** 안내 후 ②부터 재시도.

3단 검증 성공 시 1줄 요약 (파일명·페이지 수·노드 수) 보여주고 6-2 로 즉시 진행.

### 6-2. /카드뉴스 스킬 핸드오프

연결 확인되면 사용자에게:

> "이제 카드뉴스 제작 흐름으로 넘어갑니다. **/카드뉴스 스킬**이 게이트 0(레퍼런스·콘텐츠·카드수)부터 단계별로 물어봅니다. 시작할까요?"

OK 받으면 [`/카드뉴스`](../../../../.claude/skills/카드뉴스/SKILL.md) 스킬을 호출 (또는 사용자가 "카드뉴스 만들어줘" 발화).

### 핸드오프 시 전달할 컨텍스트

`/카드뉴스` 스킬 게이트 0 의 4가지 질문 중 이미 확정된 것은 건너뛰도록 전달:
- 채널 ID (이미 join 함) → 게이트 0 질문 4 스킵
- 기본 레퍼런스 경로 `curriculum/part02-MCP12개/04-figma/디자인 레퍼런스/marketor_cards.pdf` 가 있으면 후보로 제시

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `npx` 가 멈춤 | Bun 미설치 + 네트워크 느림 | 별도 터미널에서 `curl -fsSL https://bun.sh/install \| bash` 먼저 |
| `localhost:3055` 응답 없음 | `bun socket` 미기동 | 설치 폴더에서 `bun socket` 수동 실행 |
| Figma Plugin 임포트 실패 | manifest.json 경로 오타 | 절대 경로로 다시 선택 |
| `Plugin not found` (Claude) | Figma 에 플러그인 미실행 | Figma 메뉴 → Plugins → Development → Claude MCP Plugin |
| `Channel ID mismatch` | 플러그인 재시작 후 ID 변경 | 새 channel ID 복사 후 다시 "Talk to Figma, channel <ID>" |
| `Font not found` | 본인 PC 에 폰트 없음 | `load_font_async` 자동 호출. 또는 영문 폰트 (Inter) 로 우회 |
| `Permission denied` | Figma 파일 편집 권한 없음 | 본인 계정으로 새 파일 생성 또는 편집자 권한 받기 |
| Port 3055 충돌 | 다른 프로세스 점유 | `lsof -i :3055` 확인 후 종료 |

---

## 검증된 산출물 (5분 안에 가능)

- 다크모드 로그인 페이지 (위 Step 5)
- 캠페인 배너 1080×1080 (헤드라인 + CTA 버튼)
- 인스타 카드뉴스 5장 (브랜드 컬러 적용)
- 가격표 비교 표 (3 플랜)
- 모바일 앱 첫 화면 (360×800)

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 통합 진입 | 본 스킬 (`/mcp설치-figma`) | Step 0 환경점검 → 설치 → Step 6 카드뉴스 핸드오프 |
| 카드뉴스 제작 | [`/카드뉴스`](../../../../.claude/skills/카드뉴스/SKILL.md) | 레퍼런스→기획→디자인 3 게이트 (인터랙티브) |
| 자유 운영 | 자연어 ("로그인 페이지 만들어줘") | Claude 가 60개 도구 자동 호출 |
| 디자인 분석 | `get_document_info` · `scan_text_nodes` | 본인 파일 카피 추출 |

Part 5 콘텐츠·카피 에이전트 5종이 본 MCP 를 자동 호출 (Figma 디자인 → 카피 → 발행).

## 참고 자료

- 패키지 공식 : https://github.com/arinspunk/claude-talk-to-figma-mcp
- 원본 (Cursor 버전) : https://github.com/sonnylazuardi/cursor-talk-to-figma-mcp
- 도구 60개 카탈로그 : [`../README.md`](../README.md)
- 실습 시나리오 : [`../실습.md`](../실습.md)
