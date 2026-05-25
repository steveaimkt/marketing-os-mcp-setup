# 클립 2-1. Figma MCP · 디자인 분석·카피 추출·신규 디자인 생성

## 한 줄 요약

Figma(피그마) MCP(엠씨피)를 Claude.ai 통합으로 한 번 연결하면 Claude(클로드)가 본인 피그마 파일을 **읽고·분석하고·신규 디자인 생성** 한다. 디자인 자료에서 카피 추출·디자인 시스템 가이드·React 코드 변환까지 자연어로.

## 마케터에게 왜 필요한가

- 캠페인 디자인을 매번 디자이너 외주 (반나절~며칠, 비용 30~50만원)
- 디자인 시안에서 카피 추출·톤 변형 (인스타·광고·콘텐츠 톤 각각) 수동 작업
- 디자인 시스템 가이드 (색상·폰트·간격) 정리 매번 새로 작성
- Figma MCP 설치 후 **카피 변형 30패턴 자동 생성**, **디자인 → React 코드 변환**, **본인 브랜드 톤 학습한 신규 디자인 컨셉 자동 제안**

### Before / After

| 작업 | Before | After |
|---|---|---|
| 디자인 시안 텍스트 추출 | 30분 | 8초 |
| 카피 톤 변형 (3톤 × 10개) | 60분 | 30초 |
| 디자인 시스템 가이드 정리 | 20분 | 자동 |
| 이미지 자산 export | 15분 | 자동 |
| **캠페인 디자인 분석 1건** | **약 2시간** | **1~2분** |

월 5건 분석 시 연 환산: **약 120시간 절감**.

## 핵심 도구 (Claude.ai 통합 figma 도구)

| 도구 | 기능 |
|---|---|
| `get_design_context` ★ | 본인 Figma 파일에서 컴포넌트·텍스트·이미지 종합 추출 |
| `get_screenshot` | 특정 프레임 스크린샷 다운로드 |
| `get_metadata` | 파일 메타데이터 (페이지·프레임·컴포넌트 구조) |
| `search_design_system` | 본인 디자인 시스템 검색 |
| `get_variable_defs` | 디자인 토큰 (컬러·간격·폰트) 추출 |
| `use_figma` / `generate_figma_design` | 디자인 생성·수정 (코드/의도 → Figma) |
| `create_new_file` | 새 Figma 파일 생성 |
| `get_figjam` | FigJam 보드 다이어그램 추출 |

> Claude.ai 통합 figma 도구는 Figma 가 직접 유지보수. 도구 prefix 와 정확한 갯수는 `claude mcp list` 후 `mcp__claude_ai_Figma__*` 자동완성으로 확인.

## 마케터 활용 시나리오 (6가지)

| # | 시나리오 | 자연어 명령 | 소요 |
|---|---|---|---|
| A | 카피 추출 + 톤 변형 | "이 Figma 파일 헤드라인 10개 추출 → 감성/실용/유머 3톤씩" | 30초 |
| B | 디자인 시스템 가이드 | "이 파일의 컬러·폰트·간격 markdown 으로 정리" | 1분 |
| C | 디자인 → 코드 | "이 프레임을 React 컴포넌트 코드로" | 2분 |
| D | 이미지 자산 export | "이 페이지의 모든 이미지를 webp로 추출" | 1분 |
| E | 신규 디자인 컨셉 | "Spring 캠페인 톤으로 여름 캠페인 디자인 컨셉" | 3~5분 |
| F | 디자인 diff | "이 파일 지난주 vs 이번주 변경 사항" | 30초 |

## 설치 방법 한눈

### 채택 방식: Claude.ai 통합 (OAuth 자동)

```
1. Claude.ai 접속 (claude.ai)
2. 우상단 프로필 > Settings
3. 좌측 메뉴 Integrations
4. "Figma" 항목 찾기 → "Connect" 버튼 클릭
5. 브라우저에서 Figma 로그인 + 권한 허용
6. 자동 인증 완료
```

→ **사용자 작업 1분**. Personal Access Token 발급·WebSocket 서버 설정·Figma Desktop 플러그인 설치 **모두 불필요**.

### 트리거 1줄

```
"Figma MCP 설치하자"
```

→ `/mcp설치-figma` 스킬이 자동 호출되어 Claude.ai 통합 연결 안내.

> ⚡ 이전 (npm 2 MCP · `figma-developer-mcp` 읽기 + `claude-talk-to-figma-mcp` 쓰기 + WebSocket + Figma Desktop 플러그인) 방식과 달리, 이번 채택은 **Claude.ai 통합 1개 MCP**. 설치 단계 80% 단순화. Bun 런타임·플러그인 채널 모두 사라짐.

## 사전 준비물

- Claude.ai 계정 (Claude Code 와 동일 계정 권장)
- 본인 Figma 계정 + 분석할 Figma 파일 1개 (공개 또는 본인 접근 가능)
- Figma Desktop 또는 Web 어느 쪽이든 OK (플러그인 설치 불필요)

## 작동 방식

```
[사용자 자연어 명령: "이 Figma 파일 카피 추출해줘 + URL"]
   ↓
[Claude Code]
   ↓
[Claude.ai 통합 Figma MCP (mcp.figma.com)]
   ↓ OAuth 자동 (Claude.ai 가 토큰 갱신)
[Figma API]
   ↓
[본인 Figma 파일 · 접근 권한 있는 것 모두]
   ↓
[Claude 가 컴포넌트·텍스트·이미지 통합 추출]
   ↓
[결과: 마크다운 표 + 카피 변형 + 인사이트]
```

## 실습으로 만들 결과물 1건

설치 완료 후 즉시 만들 첫 결과물 (자세히는 [결과물-예시.md](결과물-예시.md)):

```
사용자: "이 Figma 파일의 모든 텍스트 + 컴포넌트 추출해줘:
       https://www.figma.com/design/abc123/Spring-Campaign-2026"

결과: 디자인 자산 종합 추출 (8초)
  📁 Spring Campaign 2026
  ├── 헤드라인 10개 (감성·실용·유머 3톤 변형 가능)
  ├── 컬러 시스템 (Primary #BC4749 / Secondary #2D3047 / Accent #FFBC42)
  ├── 폰트 (Pretendard Bold 48~96px / Regular 16~20px)
  └── 이미지 12개 (export 가능)
```

- 활용 6가지 (카피 추출·디자인 시스템·코드 변환·이미지 export·신규 컨셉·diff)
- 매주 자동화: Part 5 콘텐츠 카피 에이전트 + Buffer + Discord 알림

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-figma`](mcp설치-figma/SKILL.md) | Claude.ai 통합 연결 안내 (Connect 버튼 1클릭) |
| 운영 단계 | "이 Figma 파일 분석" 등 자연어 | Claude 가 figma 도구 자동 호출 |

Part 5 콘텐츠·카피 에이전트 5종이 본 MCP 를 자동 호출 (디자인 → 카피 → 발행).

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| Claude.ai > Integrations 에 Figma 없음 | 지역·계정 권한 차이 | claude.ai/integrations 직접 접근 또는 Claude Code 안에서 `claude mcp list \| grep figma` 확인 |
| `mcp__claude_ai_Figma__*` 도구 안 보임 | Claude.ai 통합 미연결 | Settings > Integrations > Figma > Connect 클릭 |
| `Permission denied` (특정 파일) | 본인 접근 권한 없는 파일 | Figma 에서 본인 계정에 공유 권한 추가 |
| FigJam 보드 추출 안 됨 | 일반 Figma 파일 도구로 호출 | `get_figjam` 도구 명시적 사용 |
| 한국어 카피 추출 깨짐 | 거의 없음 (UTF-8) | 폰트 한글 지원 (Pretendard·Spoqa Han Sans) 확인 |

## 검증된 산출물

- 디자인 시안 → 카피 30패턴 (감성·실용·유머 × 10개)
- 디자인 시스템 가이드 (markdown · 색상·폰트·간격)
- 디자인 프레임 → React/HTML 컴포넌트 코드
- 캠페인별 자산 export (webp / svg / png)
- 본인 브랜드 톤 학습한 신규 디자인 컨셉 (use_figma 도구)

## 다음

→ [`실습.md`](실습.md)
→ [`../05-youtube-data/README.md`](../05-youtube-data/README.md) · YouTube Data MCP (채널·키워드 분석)
