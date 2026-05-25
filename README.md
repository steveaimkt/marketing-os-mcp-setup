# marketing-os MCP Setup — 12개 MCP 한 번에 설치하기

> 패스트캠퍼스 「24시간 Full 가동 마케팅 자동화! 30개 에이전트로 완성하는 클로드코드」 Part 2 부속 자료
> 1인 마케터가 Claude Code에 12개 MCP를 연결해 시트·노션·광고·SNS·디자인·영상을 직접 만지게 만드는 설치 가이드

---

## 이 repo는 무엇인가요

Claude Code에 12개 MCP(Model Context Protocol) 서버를 연결하는 **실습 설치 가이드** 모음입니다.
- 각 폴더 = 1개 MCP, 3분 안에 설치·헬스체크
- 마케터(비개발자) 기준 한국어 설명
- 보안 키는 `.env`에 보관, 절대 커밋되지 않음

## 빠른 시작 (5분)

```bash
# 1) repo 클론
git clone https://github.com/steveaimkt/marketing-os-mcp-setup.git
cd marketing-os-mcp-setup

# 2) 환경 변수 템플릿 복사
cp .env.example .env

# 3) Claude Code 실행
claude

# 4) Claude에게 안내 요청
# "MCP 전체 설치하자" 라고 입력하면 강의 진행 순서대로 12개 MCP 자동 설치
```

> 처음이라면 [`00-사전준비물.md`](00-사전준비물.md) 부터 확인하세요.

## 12개 MCP 한눈에 보기

| Ch | # | MCP | 마케터에게 의미 | API 키 |
|---|---|---|---|---|
| **Ch 1. MCP 이해 + 데이터 분석** | | | | |
| | 1-1 | [MCP란 무엇인가](00-MCP란-무엇인가/) | AI에게 손발 달아주기 | - |
| | 1-2 | [Google Sheets](01-google-sheets/) | 스프레드시트 업무 자동화 | OAuth |
| | 1-3 | [GA4](02-ga4/) | 웹사이트 성과 자동 리포트 | GCP 서비스 계정 |
| | 1-4 | [Firecrawl](03-firecrawl/) | 경쟁사·시장 정보 자동 수집 | API 키 |
| **Ch 2. 콘텐츠·영상·디자인** | | | | |
| | 2-1 | [Figma](04-figma/) | 디자인 시안 기획·수정 | OAuth (Claude.ai) |
| | 2-2 | [YouTube Data](05-youtube-data/) | 유튜브 채널 분석·댓글 관리 | API 키 |
| | 2-3 | [Higgsfield](06-higgsfield/) | 이미지 생성·편집 자동화 | OAuth (Claude.ai) |
| | 2-4 | [영상제작](07-영상제작/) | Hyperframes + HeyGen + ElevenLabs 트리오 | MCP 2종 + 로컬 |
| **Ch 3. 배포와 광고** | | | | |
| | 3-1 | [Buffer](08-buffer/) | SNS 다채널 자동 발행·예약 | Access Token |
| | 3-2 | [Meta·Google Ads](09-ads/) | 광고 성과 분석·집행·수정 | 광고주 토큰 |
| **Ch 4. 협업과 관리** | | | | |
| | 4-1 | [Notion](10-notion/) | 콘텐츠 캘린더·기획서 관리 | OAuth (Claude.ai) |
| | 4-2 | [Discord](11-discord/) | 자동화 알림·승인 AI 봇 | Bot Token |

## 각 클립 폴더 구성

```
0X-{도구명}/
├── README.md            ← 이 MCP가 무엇이고 왜 필요한가
├── 실습.md              ← 3분 설치 + 헬스 체크
├── 결과물-예시.md       ← 실습 후 어떤 산출물이 나오는가
├── mcp설치-{도구}/      ← /mcp설치-{도구} 스킬 정의
└── {도구별 보조 자료}
```

## 보안 원칙

- `.env` 는 **절대 커밋 금지** (`.gitignore` 등록됨)
- `.env.example` 만 추적 — 빈 키 템플릿
- `mcp-server/oauth_credentials.json`, `token.json` 등 인증 파일도 제외
- 푸시 전에는 항상 `git status` 로 변경 파일 확인하세요

## 사전 준비물

- macOS / Linux / Windows (WSL 권장)
- Claude Code 설치 완료 (`claude --version` 작동)
- 각 MCP별 계정 (강의 진행하며 하나씩 생성, 본인이 안 쓰는 채널은 건너뛰기 가능)
- 결제 정보: Firecrawl·Buffer·일부 광고 계정은 유료 (스타터 플랜으로 충분)

> 자세한 사항은 [`00-사전준비물.md`](00-사전준비물.md) 참고

## 진행 순서

각 클립은 **번호 순서대로** 따라가시면 됩니다:

→ 시작: [`00-MCP란-무엇인가/README.md`](00-MCP란-무엇인가/)

## 체크리스트 (Part 2 종료 후)

- [ ] `claude mcp list` 명령으로 12개 MCP가 모두 보인다
- [ ] 각 MCP에 대해 최소 1개 명령으로 헬스 체크 통과
- [ ] `.env` 파일에 필요한 API 키 입력 완료
- [ ] `.mcp.json` 한 번 열어 12개 서버 구성 이해
- [ ] Part 3로 진행 준비 완료 (콘텐츠 파이프라인)

## 라이선스 · 사용 안내

- 강의 수강생의 학습 목적 사용 환영
- 본 가이드는 패스트캠퍼스 강의 [「24시간 Full 가동 마케팅 자동화! 30개 에이전트로 완성하는 클로드코드」](https://fastcampus.co.kr) 의 부속 자료입니다
- 문의: 강의 Q&A 게시판
