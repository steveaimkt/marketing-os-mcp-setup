---
name: discord-channels-setup
description: |
  Discord Channels (Anthropic 공식 `discord@claude-plugins-official`) 셋업 스킬. 폰 디스코드 DM ↔ Claude Code 세션 양방향. **맥북 + 윈도우** 모두 지원. 11 STEP 인터랙티브 게이트형:

  ① STEP 0~9 · Discord ↔ Claude 연동 (필수)
  ② STEP 10 · Gmail + Calendar Connector 연동 (완성)
  ③ STEP 11 · 마케팅 MCP 10종을 Discord 에서 함께 사용 (안내)

  자동 호출 트리거:
  - **"디스코드 채널 설치"** ⭐
  - **"디스코드 채널 세팅"** ⭐
  - **"디스코드 channels 설치하자"** ⭐
  - **"폰으로 디스코드에서 클로드 부르기"** ⭐
  - "Discord Channels 셋업" · "discord channels setup"
  - "claude --channels 디스코드 연결"

  특이점:
  - **macOS + Windows + Linux** 모두 지원 · 셸·경로 자동 분기
  - **Claude Code v2.1.80+** · **claude.ai 로그인** · **Bun** 필수
  - 노출 도구 5개: `reply` · `react` · `edit_message` · `fetch_messages` · `download_attachment`
  - **Team / Enterprise** 계정은 관리자가 `channelsEnabled: true` 활성화 필요
  - 출처: https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord
---

# Discord Channels 셋업 (맥북 + 윈도우)

> Anthropic 공식 Channels 플러그인으로 **외부 Discord 메시지를 실행 중인 Claude Code 세션으로 푸시**. 폰에서 봇에게 DM → PC 의 Claude 가 분석·답신.
> 출처: [공식 README](https://github.com/anthropics/claude-plugins-official/blob/main/external_plugins/discord/README.md) · [Channels 문서](https://code.claude.com/docs/ko/channels)

---

## 🎬 시작 멘트

스킬이 호출되면 Claude 는 다음과 같이 출력 :

```
🤖 Discord Channels 셋업을 시작합니다 (맥북 / 윈도우 / Linux 공통).

핵심 한 가지:
  Channels = 실행 중인 Claude Code 세션으로 Discord 메시지를 푸시하는 MCP 서버.
  폰 디스코드 → 봇 DM → PC 의 Claude 가 분석·답신.
  ⚠️ Claude Code 세션이 켜져 있는 동안에만 작동.

  ⚠️ 실행 위치 (가장 중요) : 반드시 "터미널에서 켠 claude" 여야 합니다.
     · 맥    → Terminal / iTerm 에서  claude
     · 윈도우 → PowerShell 에서        claude
     VSCode · Cursor 등 IDE 확장 안에서는 STEP 5(/plugin)·STEP 7(--channels)
     이 동작하지 않습니다("/plugin isn't available"). 확장에서 시작했다면
     지금 터미널 창을 열어 claude 로 다시 들어온 뒤 진행하세요.

────────────────────────────────

총 11 STEP · 약 30~40분.

▶ Discord ↔ Claude 연동 (필수)
  STEP 0  OS 자동 감지
  STEP 0.5 [Windows 만] 사전 최적화 (Defender·OneDrive·실행정책·LongPath)
  STEP 1  사전 점검 (Bun·Claude Code·claude.ai·Discord 서버·계정 타입)
  STEP 2  Discord Bot 생성
  STEP 3  Message Content Intent 활성화
  STEP 4  봇 서버 초대 (OAuth + 6 권한)
  STEP 5  Channels 플러그인 설치
  STEP 6  Bot 토큰 등록
  STEP 7  --channels 모드 재시작
  STEP 8  페어링 + allowlist 잠금
  STEP 9  폰 DM 양방향 검증

▶ 외부 도구 연결 (완성)
  STEP 10 Gmail + Calendar Connector 연동 (5단계)

▶ 마케팅 MCP 결합 안내
  STEP 11 마케팅 MCP 10종을 Discord 에서 함께 사용

각 단계마다 사용자 입력을 기다리며 진행. 막히면 'help' 라고 답하세요.

시작할까요? (y / n)
```

사용자 `y` → STEP 0 진행.

---

# ⚙️ Discord ↔ Claude 연동 (STEP 0~9)

## STEP 0 · 사용자 OS 자동 감지 (자동 5초)

```bash
uname -s 2>/dev/null || echo "Windows"
```

- `Darwin` → macOS
- `Linux` → Linux (macOS 명령과 호환 대부분)
- `Windows` / `MINGW*` / `CYGWIN*` → Windows (PowerShell)

게이트 :
```
감지된 OS: macOS (또는 Windows / Linux)

맞나요? (y → 진행 / n → 수동 지정)
```

→ **macOS / Linux** 면 STEP 1 로. **Windows** 면 STEP 0.5 (사전 최적화) 진행.

---

## STEP 0.5 · 윈도우 사전 최적화 (Windows 만 · 3분) ⭐

⚠️ **STEP 0 에서 Windows 로 감지된 경우에만 진행. macOS / Linux 는 건너뜁니다.**

윈도우에서 셋업이 5~10배 느려지는 5가지 함정을 먼저 풉니다. 미조치 시 STEP 1 Bun 설치·STEP 5 플러그인 설치·STEP 7 첫 기동에서 누적 30분~수 시간 지연.

### 0.5-1. 5가지 원인 (영향 큰 순)

| # | 원인 | 폭발 지점 | 미조치 시 |
|---|---|---|---|
| 1 | OneDrive 가 `%USERPROFILE%\.claude\` 동기화 | STEP 5 플러그인 · STEP 7 첫 기동 | 5~10배 느려짐 + 파일 락 |
| 2 | Defender 실시간 보호가 Bun 캐시·plugin 폴더 스캔 | STEP 1 Bun · STEP 5 `/plugin install` | 3~5배 + CPU 100% |
| 3 | PowerShell 실행 정책 Restricted | STEP 1 Bun 설치 스크립트 거부 | 사용자 5~10분 헤맴 |
| 4 | PATH 미반영 → 같은 창에서 재시도 루프 | STEP 1 직후 `bun --version` 실패 | 무한 재시도 |
| 5 | claude.ai OAuth 방화벽 첫 프롬프트 | STEP 1-3 `claude login` | 30초~영구 멈춤 |

선택: **한국어 사용자명 (`C:\Users\홍길동\`)** + Long Path 260자 한계로 `npm i -g @anthropic-ai/claude-code` 가 스톨하는 케이스 → 0.5-2 의 `LongPathsEnabled` 로 해결.

### 0.5-2. 일괄 최적화 스크립트 (관리자 PowerShell · 1분)

**Windows 시작 메뉴 → PowerShell 우클릭 → '관리자 권한으로 실행'** 후 :

```powershell
# (1) Defender 예외 등록 — 가장 큰 효과
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.bun"
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.claude"
Add-MpPreference -ExclusionPath "$env:APPDATA\npm"
Add-MpPreference -ExclusionProcess "bun.exe"
Add-MpPreference -ExclusionProcess "node.exe"
Add-MpPreference -ExclusionProcess "claude.exe"

# (2) PowerShell 실행 정책 (현재 사용자만 · Bun 설치 스크립트용)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force

# (3) Long Path 지원 (관리자 1회 · 한국어 사용자명 대응)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

3개 모두 성공 메시지 (또는 "already exists") 가 나와야 합니다.

### 0.5-3. OneDrive 백업 해제 (수동 1분)

```
설정 → 계정 → Windows 백업 → 'OneDrive 폴더 동기화 관리' →
  '문서' / '바탕 화면' 백업 OFF

(이미 동기화 중이라면)
  탐색기에서 %USERPROFILE% 입력 →
  .claude / .bun 폴더가 'C:\Users\<이름>\OneDrive\...' 안에 있는지 확인 →
  있으면 OneDrive 밖 (예: 'C:\Users\<이름>\.claude') 으로 이동 →
  OneDrive 아이콘 → 일시 중지 (셋업 동안)
```

### 0.5-4. STEP 1 진행 전 필수 주의사항

- Bun / Claude Code 설치 후엔 **반드시 새 PowerShell 창** 열기 (PATH 반영)
- `claude login` 직후 **Windows 방화벽 프롬프트가 뜨면 'Allow' 클릭** (개인 + 공용 네트워크 모두 체크 권장)
- WSL 의 Bun 과 네이티브 Windows Bun 은 별개. **본 강의는 네이티브 PowerShell 사용**

### STEP 0.5 종료 게이트
```
질문 · 윈도우 사전 최적화 완료했나요?
  - Defender 예외 3개          : ✅ / 건너뜀
  - 실행 정책 RemoteSigned     : ✅ / 이미 설정
  - LongPathsEnabled           : ✅ / 이미 설정
  - OneDrive 백업 해제         : ✅ / 해당 없음
  - 방화벽 'Allow' 클릭 준비   : ✅

답변 (y / skip / help) :
```

`skip` → STEP 1 진행하되 셋업 중 멈추면 본 STEP 0.5 로 복귀.

---

## STEP 1 · 사전 점검 (자동 + 사용자 확인)

### 1-0. 실행 환경 확인 (가장 먼저 · 양 OS 공통) ⭐

이 셋업은 **터미널에서 켠 `claude`** 에서만 완료된다. IDE 확장 세션이면 STEP 5·7 에서 반드시 막힌다.

빠른 자가 진단 — 사용자에게 묻는다:
> **지금 Claude 를 어디서 켰나요?**
> - ⓐ 맥 Terminal / iTerm 또는 윈도우 PowerShell 에서 `claude` 입력 → ✅ 그대로 진행
> - ⓑ VSCode · Cursor 등 편집기 안의 Claude 패널 → ⚠️ **여기서 멈추고** 터미널 창을 열어 해당 프로젝트 폴더에서 `claude` 로 다시 시작

판단 팁: 지금 세션에서 `/plugin` 입력 시 `isn't available in this environment` 가 뜨면 ⓑ 환경이다. 이 경우 STEP 5 도 실패하므로 터미널로 옮긴 뒤 본 스킬을 다시 호출한다.

### 1-1. Bun 런타임

| OS | 확인 | 설치 |
|---|---|---|
| **macOS / Linux** | `bun --version` | `curl -fsSL https://bun.sh/install \| bash` |
| **Windows** | `bun --version` (PowerShell) | `powershell -c "irm bun.sh/install.ps1 \| iex"` |

설치 후 새 터미널 / PowerShell 창 필요.

#### ⚠️ 윈도우 Bun 설치 누락 / 실패 시 (가장 자주 발생)

증상: 설치 명령은 완료된 것 같은데 새 PowerShell 창에서 `bun --version` 이 "명령을 찾을 수 없음" 으로 뜸.

체크 순서 :

```powershell
# (1) 실제로 설치된 위치 확인
Test-Path "$env:USERPROFILE\.bun\bin\bun.exe"
#  True  → 설치 OK, PATH 만 빠진 상태 → (3) 으로
#  False → 설치 자체 실패 → (2) 재설치

# (2) 강제 재설치 (관리자 PowerShell 권장)
Remove-Item -Recurse -Force "$env:USERPROFILE\.bun" -ErrorAction SilentlyContinue
powershell -ExecutionPolicy Bypass -c "irm bun.sh/install.ps1 | iex"

# (3) PATH 수동 추가 (사용자 환경변수 · 영구)
[Environment]::SetEnvironmentVariable(
  "Path",
  [Environment]::GetEnvironmentVariable("Path","User") + ";$env:USERPROFILE\.bun\bin",
  "User"
)

# (4) 현재 창에서 즉시 적용
$env:Path += ";$env:USERPROFILE\.bun\bin"
bun --version
```

여전히 실패하면 **수동 설치 (Plan B)** :
```
1. https://github.com/oven-sh/bun/releases/latest 접속
2. 'bun-windows-x64.zip' 다운로드
3. 압축 해제 후 bun.exe → C:\Users\<이름>\.bun\bin\ 에 복사
4. 위 (3) PATH 수동 추가 실행
5. 새 PowerShell 창 → bun --version 확인
```

⚠️ **WSL 의 Bun 은 사용 금지**. Claude Code 가 네이티브 Windows 에서 실행되면 WSL Bun 을 찾을 수 없음. 반드시 PowerShell 에서 위 절차로 설치.

### 1-2. Claude Code 버전 (v2.1.80+)

```bash
claude --version
```

v2.1.80 미만 → `npm i -g @anthropic-ai/claude-code@latest` (OS 공통)

### 1-3. claude.ai 로그인 확인

```
질문 1 · claude.ai 계정으로 로그인되어 있나요?
  (Pro / Max / Team / Enterprise 모두 가능 · API Key 인증 불가)

  - 확인: 'claude' 실행 후 상태표시줄에 본인 이메일 보이면 OK
  - 안 보이면: 'claude login' 으로 OAuth 로그인

답변 (y / n / unsure) :
```

### 1-4. Discord 계정 + 본인 서버

```
질문 2 · 봇을 추가할 본인 Discord 서버가 있나요?
  - 없으면 Discord 앱 좌측 '+' → 'Create My Own' → 'For me and my friends'

답변 (y / n) :
```

### 1-5. 계정 타입 (Team/Enterprise 만 추가 확인)

```
질문 3 · 본인 계정 타입은? (1 / 2)
  1. Pro 또는 Max (개인)
  2. Team 또는 Enterprise (회사)
```

`2` 응답 시 :
```
⚠️ Team/Enterprise 는 관리자가 channelsEnabled: true 활성화 필수.
   claude.ai → Admin Settings → Claude Code → Channels 토글 ON
   본인이 관리자가 아니면 관리자에게 요청 후 재시작.
```

### STEP 1 종료 게이트
```
사전 점검 결과:
  - Bun                 : ✅ 1.x.x
  - Claude Code         : ✅ v2.1.123
  - claude.ai 로그인    : (응답)
  - Discord 서버 보유   : (응답)
  - 계정 타입           : Pro/Max 또는 Team 관리자 활성 확인

STEP 2 진행할까요? (y / n)
```

---

## STEP 2 · Discord Bot 생성 (사용자 5분)

```
브라우저에서 https://discord.com/developers/applications 열기

순서 :
  1. 우측 상단 'New Application' 클릭
  2. 이름 입력 (예: 'My Claude Bot' · 한국어 가능)
  3. 약관 동의 → 'Create'
  4. 좌측 메뉴 'Bot' 탭
  5. 'Reset Token' → 'Yes, do it!' → 토큰 복사 ⭐
     ⚠️ 토큰은 1회만 표시. 메모장에 즉시 임시 보관.
```

게이트 :
```
질문 · 토큰을 복사했나요?
  - 토큰 형식: 'MTI4Njk...' (70자 내외)
  - 여기에 붙여넣지 마세요. STEP 6 에서 별도 안내.

답변 (y / n / lost) :
```

`lost` → 'Reset Token' 재실행으로 재발급.

---

## STEP 3 · Message Content Intent 활성화 (사용자 30초)

```
같은 Bot 페이지에서 아래로 스크롤 :

  'Privileged Gateway Intents' 섹션 →
    ✅ Message Content Intent 토글 ON ⭐ (필수)
    (Presence·Members 는 불필요)

  하단 'Save Changes' 클릭
```

⚠️ Intent 누락이 가장 자주 발생하는 실수. 페어링 단계에서 봇이 응답 안 함.

게이트 :
```
질문 · Intent ON + Save Changes 완료했나요?

답변 (y / n) :
```

---

## STEP 4 · 봇 서버 초대 (사용자 1분)

```
같은 Developer Portal 에서 :

  좌측 메뉴 'OAuth2' → 'URL Generator'

  Scopes (1개) : ✅ bot
  Bot Permissions (6개) :
    ✅ View Channels
    ✅ Send Messages
    ✅ Send Messages in Threads
    ✅ Read Message History
    ✅ Attach Files
    ✅ Add Reactions

  하단 'Generated URL' 복사 → 새 탭에 붙여넣기 →
    본인 서버 선택 → 'Authorize' → 캡차 통과

  Discord 서버 → 멤버 리스트에 봇 추가 확인.
```

게이트 :
```
질문 · 봇이 서버 멤버 리스트에 보이나요? (오프라인 — 정상)

답변 (y / n) :
```

---

## STEP 5 · Channels 플러그인 설치 (Claude Code 안에서 1분)

### 5-1. 사전 점검 (특히 윈도우)

플러그인 설치는 Claude Code 가 **내부 서브프로세스로 Bun 을 실행** 하고, **`/plugin marketplace add` 는 git 으로 마켓플레이스를 clone** 하기 때문에 :
- `bun` 이 Claude 서브프로세스의 PATH 에 보여야 함
- **`git` 이 설치돼 있어야 함** (마켓플레이스 clone 에 필수)
- claude.ai 로그인 상태여야 함
- 네트워크가 `github.com` 접근 가능해야 함

```
# Claude Code 내부 셸에서 (또는 Claude 에게 시켜서) 2줄 확인 :
!bun --version   ← 버전 출력되면 OK
!git --version   ← 버전 출력되면 OK
```

`bun: command not found` → STEP 1-1 의 Bun PATH 절차로 복귀.
`git: command not found` (⚠️ **윈도우에서 자주 발생**) → git 먼저 설치 :
- **Windows**: https://git-scm.com/download/win 다운로드 → 설치 (기본 옵션) → **새 PowerShell 창** 에서 `git --version` 확인
- **macOS**: `xcode-select --install` (보통 이미 설치됨)
- 설치 후 Claude Code 완전 재시작 (서브프로세스 PATH 반영) → 다시 STEP 5

### 5-2. 설치 실행

현재 세션에서 직접 실행 :

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install discord@claude-plugins-official
/reload-plugins
```

(이미 마켓 등록되어 있으면 `/plugin marketplace update claude-plugins-official` 로 갱신)

→ `/discord:configure`, `/discord:access` 슬래시 명령 활성화.

### 5-3. 설치 실패 시 (윈도우에서 가장 자주 발생)

| 증상 | 원인 | 해결 |
|---|---|---|
| `marketplace not found` | 마켓 추가 순서 누락 | `/plugin marketplace add` 를 먼저, 그 다음 install |
| 진행률 멈춤 (3분+) | OneDrive 가 plugin 폴더 동기화 중 | STEP 0.5-3 OneDrive 백업 해제 후 재실행 |
| `bun: command not found` | Claude 서브프로세스가 Bun 못 찾음 | 5-1 의 `!bun --version` 확인 → 1-1 의 PATH 절차 |
| `ENOTFOUND github.com` / SSL 오류 | 회사 프록시·SSL 검사 | `git config --global http.sslVerify false` (임시) 또는 사내 네트워크 외 환경 |
| 무한 "Installing..." 로 멈춤 | Defender 가 plugin 다운로드 파일 스캔 | STEP 0.5-2 Defender 예외 등록 후 재실행 |
| 설치는 됐는데 슬래시 명령 안 보임 | `/reload-plugins` 누락 | `/reload-plugins` 실행 또는 Claude Code 재시작 |
| `Authentication required` | claude.ai 로그아웃 상태 | `claude login` 으로 OAuth 재로그인 |
| 한국어 사용자명에서 풀림 | Long Path 미설정 | STEP 0.5-2 `LongPathsEnabled` |

### 5-4. 강제 재설치 (위 표로 안 풀릴 때 · 1분)

```
# Claude Code 안에서 :
/plugin uninstall discord@claude-plugins-official
/plugin marketplace remove claude-plugins-official

# 외부 셸 (PowerShell) — 캐시 청소 :
#   macOS / Linux
rm -rf ~/.claude/plugins/cache
#   Windows
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache" -ErrorAction SilentlyContinue

# Claude Code 재시작 후 다시 :
/plugin marketplace add anthropics/claude-plugins-official
/plugin install discord@claude-plugins-official
/reload-plugins
```

### STEP 5 종료 게이트
```
질문 · /plugin install 출력에 "Installed" 같은 성공 메시지 보였나요?
       그리고 /discord:configure 입력 시 자동완성에 명령이 보이나요?

답변 (y / n / error) :
```

`n` 또는 `error` → 5-3 표 확인 → 5-4 강제 재설치 → 그래도 안 되면 트러블슈팅 표 (페이지 하단) 참조.

---

## STEP 6 · Bot 토큰 등록 (사용자 30초)

```
/discord:configure <STEP 2 에서 복사한 토큰>
```

저장 위치 :

| OS | 경로 |
|---|---|
| **macOS / Linux** | `~/.claude/channels/discord/.env` |
| **Windows** | `%USERPROFILE%\.claude\channels\discord\.env` |

⚠️ 토큰 입력 시 화면 녹화·터미널 히스토리 노출 주의.

게이트 :
```
질문 · .env 저장 메시지 보였나요?

답변 (y / n) :
```

---

## STEP 7 · --channels 모드로 Claude Code 재시작 (가장 중요)

⚠️ **이 단계가 없으면 봇이 응답하지 않습니다.**

```
1. 현재 Claude Code 세션 종료 (Ctrl + C 또는 'exit')
2. 새 터미널 열기
3. 작업 디렉토리로 이동
4. 다음 명령 실행 :

   claude --channels plugin:discord@claude-plugins-official
```

명령은 OS 공통 (단 PATH 에 `claude` 등록 필요).
멀티 채널 : `claude --channels plugin:discord@... plugin:telegram@...`

성공 시 :
- Discord 멤버 리스트에서 봇이 🟢 온라인
- 터미널에 `Channels enabled: discord` 출력

게이트 :
```
질문 · Discord 에서 봇 온라인 (초록 점) 으로 보이나요?

답변 (y / n) :
```

`n` → 트러블슈팅 표 참조 (페이지 하단).

---

## STEP 8 · 봇 페어링 + 허용목록 잠금 (보안)

### 8-1. 봇에게 DM
```
Discord 앱 (폰 또는 PC) :
  1. 본인 서버 멤버 리스트 → 봇 클릭
  2. 'Message' / '메시지 보내기'
  3. 아무 텍스트 입력 (예: 'hi')

봇이 즉시 페어링 코드로 회신 (예: 'ABCD-1234')
⚠️ 응답 없으면: Channels 세션 살아있는지 + Intent ON 재확인
```

### 8-2. 페어링
```
/discord:access pair ABCD-1234
```
→ 본인 Discord 계정 허용목록에 자동 추가.

### 8-3. 허용목록 잠그기 ⭐
```
/discord:access policy allowlist
```
→ 페어링 안 된 사람의 메시지 자동 폐기.

게이트 :
```
질문 · 페어링 + policy allowlist 모두 성공했나요?

답변 (y / n) :
```

---

## STEP 9 · 폰 DM 양방향 검증 (최종)

```
📱 폰 Discord 앱 :
  1. 본인 서버 → 봇 → DM 열기
  2. 메시지:  "지금 작업 중인 디렉토리 알려줘"
  3. 30초 안에 봇이 답변하는지 확인
```

PC 의 Channels 세션 :
- `<channel source="discord" chat_id="..." user="...">` 이벤트 도착
- Claude 가 도구 호출 + reply
- 터미널에는 도구 호출과 "전송됨" 만 (실제 답신은 Discord 앱에)

게이트 :
```
질문 · 폰 Discord 에서 봇 답변 받았나요?

답변 (y / n) :
```

`y` → 🎉 **Discord ↔ Claude 양방향 연동 완료**. STEP 10 진행.

---

# 🔗 STEP 10 · Gmail + Calendar Connector 연동 (5단계 · 3~5분)

Discord 만으로는 "오늘 일정", "어제 메일" 같은 일상 질의를 못 받음. Gmail + Calendar Connector 를 연결해야 양방향 어시스턴트가 완성.

## 10-1. 헬스 체크 (자동 30초)

Claude 가 현재 세션에서 도구 prefix 노출 여부 확인 :

```
필요 prefix:
  mcp__claude_ai_Gmail__*           (search_threads · create_draft · label_message · ...)
  mcp__claude_ai_Google_Calendar__* (list_events · create_event · ...)
```

게이트 :
```
- Gmail 통합            : ✅ / ❌
- Google Calendar 통합  : ✅ / ❌

둘 다 ✅ → 10-4 (활성 검증) 로 점프 (y)
하나라도 ❌ → 10-2 진행 (n)
```

## 10-2. Gmail Connector 연결 (사용자 1분)

```
브라우저:
  ① URL 직접: https://claude.ai/settings/connectors
  ② 메뉴: claude.ai → 우측 상단 아바타 → Settings → Connectors

순서:
  1. 'Gmail' 카드 → 'Connect'
  2. Google 계정 선택 (마케팅용 계정 권장)
  3. 권한 동의:
     ✅ Gmail 메시지 읽기
     ✅ 라벨 보기 및 관리
     ✅ 임시 보관함 (Draft) 작성
     ⚠️ '메일 발송' 권한은 선택 (자동 답신 쓰려면 ON · 분석만이면 OFF 안전)
  4. 'Allow' → 'Connected' 표시
```

게이트 :
```
질문 · Gmail Connector 가 'Connected' 표시되나요?

답변 (y / n / scope-error) :
```

`scope-error` → Workspace (회사) 의 third-party app 차단. 개인 Gmail 로 재시도 또는 관리자에게 Anthropic 화이트리스트 요청.

## 10-3. Google Calendar Connector 연결 (사용자 1분)

같은 페이지에서 :
```
  1. 'Google Calendar' 카드 → 'Connect'
  2. Google 계정 선택 (Gmail 과 같은 계정 권장)
  3. 권한 동의:
     ✅ 캘린더 목록 보기
     ✅ 일정 보기·생성·수정·삭제 (primary 캘린더)
     ⚠️ 공유 캘린더 (부서·팀) 는 OAuth 기본 scope 밖 → 필요 시 ID 직접 사용
  4. 'Allow' → 'Connected'
```

게이트 :
```
질문 · Calendar Connector 'Connected' 표시되나요?

답변 (y / n / scope-error) :
```

## 10-4. 활성 검증 (사용자 + 자동 · 1분)

⚠️ Connector 변경 후 Claude Code 세션 재시작 필요할 수 있음.

```
1. 현재 세션 종료 (Ctrl + C)
2. 새 터미널 (Channels 활성 유지):

   claude --channels plugin:discord@claude-plugins-official

3. Claude 에게:
   "오늘 받은 메일 3개만 보여줘"
   → mcp__claude_ai_Gmail__search_threads 호출 + 메일 3건 표시

4. 이어서:
   "오늘 일정 알려줘"
   → mcp__claude_ai_Google_Calendar__list_events 호출 + 일정 표시
```

게이트 :
```
질문 · 두 명령 모두 정상 응답?

답변 (y / n) :
```

## 10-5. 자주 막히는 곳

| 증상 | 원인 | 해결 |
|---|---|---|
| 'Connect' 권한 거부 화면 | Workspace third-party app 차단 | 개인 Gmail 재연결 또는 관리자 화이트리스트 |
| 'Connected' 인데 prefix 노출 X | 세션 캐시 | Ctrl+C → `claude --channels ...` 재시작 |
| 한국어 라벨 (`고객문의`) 검색 실패 | system label vs 사용자 라벨 매칭 차이 | 라벨 영문화 (`CS`·`VIP`) 또는 라벨 ID 사용 |
| 일정 생성됐는데 캘린더에 없음 | 다른 캘린더에 생성됨 | `calendarId: primary` 명시 |
| 공유 캘린더 안 보임 | OAuth 기본 scope 외 | Calendar 설정에서 ID 복사 → 명령에 전달 |
| 'Send email' 권한 거부 | 발송 스코프 미동의 | Connectors → Gmail → Reconnect, 발송 권한 ON |
| 회사 메일 (Outlook · Naver) 연동 안 됨 | Anthropic Connector 는 Google 만 | Gmail 으로 포워딩 또는 IMAP 별 MCP |

### STEP 10 종료 게이트
```
🎉 Gmail + Calendar 연동 완료.

이제 폰 DM 으로 메일 분류·일정 조회·일정 추가 모두 가능.

STEP 11 (다른 MCP 결합 안내) 진행할까요? (y / n)
```

---

# 🔌 STEP 11 · 마케팅 MCP 10종을 Discord 에서 함께 사용

⭐ **별도 "연결" 절차 없음**. 이미 설치된 MCP 는 `--channels` 세션에 **자동 노출**됨. 폰 DM 한 줄로 어떤 MCP 든 호출 가능.

## 11-1. 결합 가능한 MCP 10종 (강의 폴더 기준)

| # | 폴더 | MCP | 폰 DM 활용 예시 |
|---|---|---|---|
| 1 | `01-google-sheets` | google-sheets | "어제 매출 시트 핵심 3가지 알려줘" |
| 2 | `02-ga4` | ga4 | "어제 트래픽·전환·이탈률 알려줘" |
| 3 | `03-firecrawl` | firecrawl | "이 경쟁사 사이트 크롤링해서 신상품 알려줘" |
| 4 | `04-figma` | figma (자체호스팅) | "지금 띄운 Figma 페이지 카드뉴스 톤 일관성 점검" |
| 5 | `05-youtube-data` | youtube-data + analytics | "지난주 유튜브 채널 KPI 요약해줘" |
| 6 | `06-higgsfield` | higgsfield | "오늘 광고 이미지 1장 생성" |
| 7 | `07-영상제작` | Hyperframes + HeyGen + ElevenLabs | "이 슬라이드 영상 콘티 짜줘" |
| 8 | `08-buffer` | buffer | "이 글 5채널 (인스타·X·LinkedIn·페북·스레드) 예약" |
| 9 | `09-ads` | meta-ads + google-ads | "어제 3매체 ROAS 통합 알려줘" |
| 10 | `10-notion` | notion | "이 답변 노션 콘텐츠 캘린더에 저장" |

## 11-2. 자동 헬스 체크 (어떤 MCP 가 이미 활성?)

Claude 가 현재 세션에서 prefix 노출 여부 자동 확인 :

| MCP | 필요 prefix | 활성 여부 |
|---|---|---|
| google-sheets | `mcp__google-sheets__*` 또는 `mcp__google_sheets__*` | ✅ / ❌ |
| ga4 | `mcp__ga4__*` | ✅ / ❌ |
| firecrawl | `mcp__firecrawl__*` | ✅ / ❌ |
| figma | `mcp__claude_ai_Figma__*` 또는 `mcp__figma__*` | ✅ / ❌ |
| youtube-data | `mcp__youtube-data__*` | ✅ / ❌ |
| higgsfield | `mcp__claude_ai_Higgsfield__*` | ✅ / ❌ |
| 영상제작 | Hyperframes (로컬) + HeyGen API + ElevenLabs API | ✅ / ❌ |
| buffer | `mcp__buffer__*` | ✅ / ❌ |
| meta+google-ads | `mcp__meta-ads__*` · `mcp__google-ads__*` | ✅ / ❌ |
| notion | `mcp__claude_ai_Notion__*` | ✅ / ❌ |

게이트 :
```
헬스 체크 결과:
  활성   : N 개
  미설치 : M 개

미설치된 MCP 추가하시려면 STEP 11-3, 결합 예시 보려면 11-4, 종료는 stop.

답변 (3 / 4 / stop) :
```

## 11-3. 미설치 MCP 추가 (필요 시)

미설치된 MCP 가 있다면 별도 스킬을 호출 :

| 상황 | 호출할 스킬 |
|---|---|
| 1개 추가 | **`mcp설치` (개별)** — "X MCP 설치하자" 발화 |
| 한 번에 다 | **`mcp설치-전체` (마스터)** — "MCP 전체 설치하자" 발화 |
| 영상 트리오만 | **`mcp설치-영상제작`** — "영상제작 MCP 설치하자" |
| 유튜브만 | **`mcp설치-youtube`** — "유튜브 mcp 시작하자" |

설치 완료 후 :
```
1. 새 .mcp.json 적용 위해 Channels 세션 재시작:
   Ctrl+C → claude --channels plugin:discord@claude-plugins-official
2. 폰 DM 으로 해당 MCP 활용 테스트
```

## 11-4. 결합 예시 5개 (폰 DM 한 줄)

| # | 폰 DM | 호출되는 MCP | 흐름 |
|---|---|---|---|
| 1 | "어제 광고 ROAS + 매출 시트 비교해줘" | google-sheets + meta-ads + google-ads | 시트 read + 광고 insights → reply |
| 2 | "이 PDF 분석 후 노션에 저장" (첨부 포함) | download_attachment + notion | 첨부 다운 → 요약 → notion-create-page → reply |
| 3 | "오늘 일정 + 어제 트래픽" | calendar + ga4 | list_events + run_report → reply |
| 4 | "유튜브 채널 KPI 보고서 만들고 매주 월요일 09시 자동 발송" | youtube + ga4 + 노션 + Webhook cron | 보고서 1회 작성 → cron 등록 → 매주 자동 |
| 5 | "이 경쟁사 사이트 크롤링 + 우리 광고 카피 비교" | firecrawl + ads | scrape + ads 카피 → 차이 분석 → reply |

⚠️ 위험 작업 (광고 예산 변경·발송) 은 권한 릴레이로 폰 ✅ 승인 게이트 권장.

### STEP 11 종료 게이트
```
🎉 연결 + 확장 완료 (STEP 0~11).
   Discord ↔ Claude 양방향 + Gmail/Calendar + 마케팅 MCP 결합 가능 상태.

────────────────────────────────

⚠️ 그런데 아직 두 가지가 비어 있음:
   ① "폰에서 뭐라고 말해야 되나요?" (사용자 매뉴얼)
   ② "이 시스템이 진짜 한 흐름으로 작동해요?" (아키텍처 진단)

   → 다음 스킬이 인벤토리 1회 스캔으로 두 문서를 동시에 박제합니다.

다음 스킬 (필수 권장):
  💬 "AI 비서 구축" 또는 "봇 운영 가이드" 라고 말하세요.

  → ai-assistant-build 스킬이 :
       ① 인벤토리 스캔 (28 에이전트 + 14 스킬 + 10 MCP + 봇 정보)
       ② 오케스트레이터 카탈로그 검증 (라우팅 갭 검출)
       ③ 자연어 라우팅 시뮬레이션 (발화 5개 + 확신도)
       ④ agents/AI-비서-아키텍처.md 박제 (시스템 아키텍처)
       ⑤ ~/.claude/channels/discord/OPERATIONS.md 박제 (사용자 매뉴얼)
       ⑥ 폰에서 "운영 가이드 보여줘" → 봇이 운영 카드 응답
       ⑦ (notion 활성 시) Notion 페이지 2개 미러링
       ⑧ 첫 E2E 테스트 추천 (A: email-newsletter / B: daily-briefing / C: 광고)
       소요: 약 15분.

skip 하고 바로 첫 에이전트로 가려면:
  "1-1 email-newsletter 실습 시작하자" 라고 말하세요.

장기 운영 추가 (옵션):
  - 매일 09시 자동 브리핑     → Part 10 daily-briefing (Webhook + cron)
  - 광고 임계치 자동 점검     → Part 10 check-ads
  - 주간 종합 리포트          → Part 10 weekly-report
```

---

# 🛠 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `/plugin install` "marketplace not found" | 마켓플레이스 미등록 | `/plugin marketplace add anthropics/claude-plugins-official` 먼저 |
| `bun: command not found` | Bun 미설치 / PATH 미반영 | 설치 후 새 터미널 (macOS: `source ~/.zshrc` · Windows: 새 PowerShell) |
| 봇 Offline 표시 | `--channels` 플래그 누락 / 세션 종료 | 새 터미널 + `claude --channels plugin:discord@...` |
| 페어링 코드 안 옴 | Channels 세션 꺼짐 또는 Intent OFF | STEP 3 + STEP 7 재확인 |
| Bot 메시지 못 읽음 | Message Content Intent OFF | Developer Portal → Bot → Intent 토글 ON + Save |
| "API Key 인증 작동 안 함" | claude.ai 로그인 아님 | `claude login` 으로 OAuth |
| `Channels disabled` 경고 | Team/Enterprise 관리자 미활성화 | claude.ai Admin → Claude Code → Channels 활성화 |
| 봇 온라인인데 답신 없음 | 페어링 안 됨 / allowlist 인데 본인 미등록 | `/discord:access list` 확인 → `/discord:access pair <코드>` 재실행 |
| reply 텍스트 안 보임 | 답신은 Discord 도착 (터미널엔 도구 호출만) | 폰/PC Discord 앱에서 확인 |
| 첨부 25MB 초과 | 공식 제한 | 파일 분할 또는 Google Drive 링크 |
| `claude --version` < 2.1.80 | 구버전 | `npm i -g @anthropic-ai/claude-code@latest` |
| Connector 추가했는데 도구 prefix 노출 X | 세션 캐시 | Ctrl+C → `claude --channels ...` 재시작 |

### 윈도우 전용 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| STEP 5 `/plugin marketplace add` 에서 `git not found` / clone 실패 | 윈도우에 git 미설치 (마케터 PC 흔함) | https://git-scm.com/download/win 설치 → 새 PowerShell → Claude 재시작 후 재실행 |
| STEP 5 `/plugin install` 3~10분 멈춤 | OneDrive 가 `%USERPROFILE%\.claude` 동기화 | STEP 0.5-3 OneDrive 백업 해제 후 재실행 |
| STEP 1 Bun 설치 중 CPU 100% · 매우 느림 | Defender 실시간 보호가 Bun 캐시 스캔 | STEP 0.5-2 `Add-MpPreference` 예외 등록 |
| `irm bun.sh/install.ps1 \| iex` 거부 / 무반응 | PowerShell 실행 정책 Restricted | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Bun 설치했는데 `bun --version` 실패 | PATH 미반영 또는 사용자 PATH 누락 | STEP 1-1 의 PATH 수동 추가 절차 (`[Environment]::SetEnvironmentVariable`) |
| `bun` 은 되는데 Claude 가 못 찾음 | Claude 서브프로세스 PATH 분리 | Claude Code 완전 재시작 (현재 창 종료 → 새 PowerShell) |
| `claude login` 영구 멈춤 | Windows 방화벽 첫 프롬프트 미응답 | 방화벽 알림에서 'Allow' (개인 + 공용 체크) 후 재시도 |
| 한국어 사용자명 + `npm i -g` 스톨 | Long Path 260자 한계 | STEP 0.5-2 `LongPathsEnabled` 등록 후 재시도 |
| WSL Bun 은 되는데 PowerShell 에선 안 됨 | WSL ↔ Windows PATH 분리 | 네이티브 Windows Bun 별도 설치 (강의 표준) |
| `/plugin install` 중간에 SSL/proxy 오류 | 사내 SSL 검사 또는 회사 프록시 | 개인 네트워크로 셋업 또는 IT 에 `github.com` · `anthropic.com` 화이트리스트 요청 |

---

# 🔒 보안 체크리스트

- [ ] Bot 토큰은 `.env` 에만 보관 · Git commit / 채팅 / 화면 공유 금지
- [ ] `/discord:access policy allowlist` 로 잠금 (open 정책 위험)
- [ ] 페어링된 발신자는 **권한 프롬프트도 승인 가능** → 신뢰하는 본인 계정만
- [ ] 광고 예산·메일 발송 같은 위험 작업은 권한 릴레이로 폰 승인 게이트
- [ ] 토큰 노출 의심 즉시 Developer Portal Reset Token + `/discord:configure <new>` 재실행

---

# 📂 강의 연결

- 본 스킬은 [클립 4-2 Discord 대본](../대본/4-2-discord-5min.md) 의 슬라이드 06 "설치 실습" 에서 호출.
- 마스터 스킬 [`skills/mcp설치`](../../../../skills/mcp설치/) 의 4단계 표준을 Channels + Gmail/Calendar + 10종 MCP 결합으로 확장.
- `~/.claude/skills/discord-channels-setup` 은 본 폴더로의 심볼릭 링크.
- Part 10 AX 시스템 연결 :
  - `daily-briefing` · 매일 09시 자동 브리핑 (Calendar + Gmail + 광고)
  - `cs-responder` · 메일 도착 자동 응답 + 디스코드 통보
  - `orchestrator` · 폰 DM 슬래시 → 30개 에이전트 호출
