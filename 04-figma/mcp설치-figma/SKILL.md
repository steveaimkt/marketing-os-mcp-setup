---
name: mcp설치-figma
description: |
  Part 2 클립 2-1 (Figma MCP) 전용 설치 스킬. Claude.ai 통합 (Settings > Integrations > Figma > Connect) + 헬스 체크 + 첫 카피 추출 결과물을 약 3분 안에 완료. Personal Access Token / WebSocket / Figma Desktop 플러그인 모두 불필요. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Figma MCP 설치하자"** ⭐ 주요 트리거
  - "피그마 MCP 설치"
  - "Figma 연결 도와줘"
  - "디자인 자동화 환경 만들자"
  - "Part 2 / 2-1 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (Claude.ai > Integrations > Connect 1클릭) →
  ③ 작업 가능 업무 (도구 + 6 시나리오) →
  ④ 결과물 1개 (본인 Figma 파일 카피·디자인 시스템 추출)

  특이점: Claude.ai 통합 hosted MCP (Figma 가 직접 운영). OAuth 자동 갱신. .env 변수 0개. Figma 가 도구 자체 유지보수.
---

# Part 2 / 2-1 Figma MCP 설치 (클립 전용)

> 본 스킬은 Figma MCP 를 Claude.ai 통합으로 한 번 연결하고 본인 Figma 파일에서 카피·디자인 시스템 추출 1건을 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Claude.ai 통합 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

```
🎨 Figma MCP 설치를 시작합니다.

먼저 짚고 갈 게 있어요:

  Figma 가 공식 운영하는 hosted MCP 를 Claude.ai 통합으로 사용:
  - Settings > Integrations > Figma > Connect 1클릭
  - OAuth 자동 (Claude.ai 가 토큰 갱신)
  - Personal Access Token / WebSocket / 플러그인 모두 불필요
  - .env 변수 0개

────────────────────────────────

총 4단계 (약 3분):

  📖 STEP 1: MCP 소개 (1분)
  ⚙️ STEP 2: 연결 (사용자 1클릭 · 1분)
       2.1 claude.ai > Settings > Integrations > Figma > Connect
       2.2 Figma OAuth 허용
       2.3 헬스 체크
  📋 STEP 3: 작업 가능 업무 (1분)
  🎯 STEP 4: 결과물 1개 · 본인 Figma 파일 카피·디자인 시스템 추출 (1분)

사전 점검 3가지:
  □ Claude.ai 계정 (Claude Code 와 동일 계정)
  □ Figma 계정 + 분석할 파일 1개
  □ Chrome 또는 Safari

전체 진행할까요? (y/n)
```

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드

| 항목 | 값 |
|---|---|
| 한 줄 정의 | 본인 Figma 파일을 Claude 가 직접 읽고·분석하고·신규 디자인 생성 |
| 패키지 | Claude.ai 통합 hosted MCP (`https://mcp.figma.com/mcp` · Figma 공식 운영) |
| 인증 방식 | OAuth · Claude.ai 자동 갱신 |
| 도구 prefix | `mcp__claude_ai_Figma__*` |
| 환경변수 | 없음 (0개) |
| 무료 한도 | Figma 무료·유료 플랜 모두 가능 |
| Before | 디자인 분석 30분·카피 변형 60분·코드 변환 2시간 |
| After | 종합 분석 8초·카피 30패턴 30초·코드 변환 2분 |

### 1.2 마케터 관점 활용

- **카피 변형 자동** · 디자인 시안 헤드라인 10개 → 감성·실용·유머 3톤 = 30 패턴
- **디자인 시스템 가이드** · 색상·폰트·간격 markdown 자동 정리
- **디자인 → 코드** · React/HTML/Tailwind 컴포넌트 자동 변환
- **이미지 자산 export** · webp/svg/png 일괄 추출
- **신규 디자인 컨셉** · 본인 브랜드 톤 학습 후 자동 제안

### 1.3 Before/After

| 작업 | Before | After |
|---|---|---|
| 디자인 시안 텍스트 추출 | 30분 | 8초 |
| 카피 톤 변형 (3톤 × 10개) | 60분 | 30초 |
| 디자인 시스템 가이드 | 20분 | 자동 |
| 이미지 자산 export | 15분 | 자동 |
| 디자인 → 코드 | 2시간 | 2분 |
| **캠페인 디자인 분석 1건** | **2시간** | **1~2분** |

연 환산: 약 120시간 절감.

---

## ⚙️ STEP 2: 연결 (사용자 1클릭 · 약 1분)

### 2.1 Claude.ai Settings 진입

```
1. https://claude.ai 접속 (Claude Code 와 같은 계정 로그인)
2. 우상단 프로필 ⓘ 또는 ⚙ > "Settings"
3. 좌측 메뉴 "Integrations" 클릭
4. 통합 목록에서 "Figma" 찾기 → "Connect" 버튼 클릭
```

### 2.2 Figma OAuth 허용

```
5. 브라우저 자동으로 Figma OAuth 페이지 열림
   - Figma 로그인 (이미 로그인 상태면 패스)
   - "Allow" 또는 "Authorize Claude" 클릭
6. Claude.ai > Integrations 화면으로 자동 복귀
   → Figma 항목에 ✓ Connected 표시 확인
```

### 2.3 헬스 체크

```bash
claude mcp list | grep -i figma
# → claude.ai Figma: https://mcp.figma.com/mcp - ✓ Connected
```

`✓ Connected` 가 아니면:
- Claude.ai 와 Claude Code 의 로그인 계정 동일한지 확인
- Claude Code 완전 종료 후 재시작

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 (Claude.ai 통합 figma)

| 도구 | 기능 |
|---|---|
| `get_design_context` ★ | 파일 종합 추출 (컴포넌트·텍스트·이미지) |
| `get_screenshot` | 특정 프레임 스크린샷 |
| `get_metadata` | 파일 메타데이터 (페이지·프레임 구조) |
| `search_design_system` | 본인 디자인 시스템 검색 |
| `get_variable_defs` | 디자인 토큰 (컬러·간격·폰트) |
| `use_figma` / `generate_figma_design` | 디자인 생성·수정 |
| `create_new_file` | 새 Figma 파일 생성 |
| `get_figjam` | FigJam 보드 다이어그램 |

> 도구 prefix 와 정확한 갯수는 Claude Code 에서 `claude mcp list` 후 자동완성으로 확인. Figma 가 직접 유지보수하므로 수시 업데이트.

### 3.2 마케터 자주 쓰는 6 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 카피 추출 + 톤 변형 ★ | "이 Figma 파일 헤드라인 10개 + 감성/실용/유머 3톤씩" | 30초 |
| B. 디자인 시스템 가이드 | "이 파일의 컬러·폰트·간격 markdown" | 1분 |
| C. 디자인 → 코드 | "이 프레임을 React + Tailwind 코드로" | 2분 |
| D. 이미지 자산 export | "이 페이지의 모든 이미지를 webp 로" | 1분 |
| E. 신규 디자인 컨셉 | "Spring 톤으로 여름 캠페인 디자인 컨셉" | 3~5분 |
| F. 디자인 diff | "이 파일 지난주 vs 이번주 변경" | 30초 |

### 3.3 다른 MCP 와 조합

- **+ Part 5 콘텐츠 에이전트** · Figma 카피 → Buffer 4채널 동시 예약
- **+ Higgsfield MCP** · Figma 디자인 톤 → 신규 이미지·영상 생성
- **+ Notion MCP** · 디자인 시스템 가이드 → Notion 페이지 자동 게시
- **+ 영상제작 (Hyperframes)** · Figma 슬라이드 → 영상 자동 변환

---

## 🎯 STEP 4: 결과물 1개 · Figma 파일 종합 추출

### 4.1 한 줄 명령

```
사용자: "이 Figma 파일의 모든 텍스트 + 컴포넌트 추출해줘:
       <본인 Figma URL>"
```

본인 Figma 파일 URL 형식:
- `https://www.figma.com/design/<file_id>/<file_name>`
- `https://www.figma.com/file/<file_id>/<file_name>` (구버전 URL 도 OK)

### 4.2 자동 실행

```
1. Claude → mcp__claude_ai_Figma__get_design_context 호출
   - file URL 또는 file_id 자동 추출
   - 페이지·프레임·컴포넌트·텍스트·이미지 모두 회수

2. Claude → 결과 정리:
   - 헤드라인·CTA·본문 텍스트 추출
   - 컬러 시스템 (hex)
   - 폰트 (이름·크기 분포)
   - 이미지 자산 갯수

3. 마크다운 표 + 요약 응답 (약 8초)
```

성공 응답 예시:
```
📁 Spring Campaign 2026
├── 페이지 4개 / 프레임 12개 / 컴포넌트 38개 / 텍스트 87개

🎨 컬러 시스템
  - Primary:    #BC4749
  - Secondary:  #2D3047
  - Accent:     #FFBC42

🖋️ 폰트
  - 헤드: Pretendard Bold (48~96px)
  - 본문: Pretendard Regular (16~20px)

📝 헤드라인 10개 추출 완료 (카피 변형 가능)
🖼️ 이미지 12개 export 가능
```

자세히는 [결과물-예시.md](../결과물-예시.md).

### 4.3 다음 단계

```
🎉 Figma MCP 연결 완료. 발전 경로:

  A. 카피 변형 30패턴:
     "위 헤드라인 10개를 감성·실용·유머 3톤씩"

  B. 디자인 → React 코드:
     "이 프레임을 React + Tailwind 컴포넌트로 변환"

  C. 신규 디자인 컨셉:
     "Spring 톤으로 여름 캠페인 디자인 컨셉 + 컬러 팔레트 제안"

  D. 다른 MCP 와 조합:
     - Figma 카피 → Buffer 4채널 예약
     - Figma 디자인 시스템 → Notion 가이드 페이지
     - Figma 톤 → Higgsfield 이미지·영상 생성

  E. 다음 MCP 설치:
     - 2-2 youtube-data · YouTube 채널·키워드 분석
```

---

## 🚨 트러블슈팅 (Figma MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| Claude.ai > Integrations 에 Figma 없음 | 지역·계정 권한 차이 | claude.ai/integrations 직접 접속 시도 |
| `mcp__claude_ai_Figma__*` 도구 안 보임 | 통합 미연결 또는 Claude Code 재시작 안 함 | Settings > Integrations > Figma > Connect 확인 + Claude Code 재시작 |
| `Permission denied` (특정 파일) | 본인 접근 권한 없는 파일 | Figma 에서 본인 계정에 공유 권한 추가 |
| `Figma file not found` | URL 오타 또는 비공개 파일 | URL 정확성 + 본인 접근 권한 확인 |
| FigJam 보드 추출 안 됨 | 일반 Figma 도구로 호출 | `get_figjam` 도구 명시적 사용 |
| 한국어 카피 깨짐 (드뭄) | 폰트 한글 미지원 | Pretendard / Spoqa Han Sans 설정 확인 |
| OAuth 토큰 만료 | 장기 미사용 | Settings > Integrations > Figma > Disconnect > Connect 재진행 |

## 📝 강의 실습 (실습.md 통합)

### 실습 한 줄 요약

claude.ai > Settings > Integrations > Figma > Connect 1클릭 + 본인 Figma 파일 URL 전달 → 8초 안에 종합 분석.

### 마케터 5패턴 · 정기 운영

```
[역할] D2C 브랜드의 콘텐츠 마케터

[입력] 디자이너가 보낸 Figma 캠페인 시안 URL

[산출물]
1. 헤드라인 10개 + 톤별 3패턴 (30 패턴)
2. 컬러 시스템 markdown
3. 추천 조합 (인스타·광고·콘텐츠별)

[제약]
- 한국어 자연어
- 본인 브랜드 톤 유지

[검증]
- 추출 텍스트 갯수 ≥ 실제
- 컬러 hex 100% 정확
```

### 응용 과제

1. 디자인 → React + Tailwind 컴포넌트 변환
2. 본인 브랜드 톤 학습 후 신규 캠페인 컨셉
3. Figma + Buffer 결합 (디자인 → 카피 → 4채널 예약)

## 강의 연결

- 본 스킬은 [클립 2-1 Figma MCP 대본](../대본/2-1-figma.md) 의 슬라이드 06 "설치 실습" 시연에서 호출
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준을 Claude.ai 통합 패턴에 적용
- 본 스킬로 연결된 MCP 는 **Part 5 콘텐츠·카피 에이전트 5종의 기반**:
  - `social-copy-writer`, `newsletter-writer`, `ad-copy-ab`, `brand-voice`, `landing-page-copy`
- Part 10 의 `weekly-campaign-publisher` 가 Figma + Buffer + Discord 통합 자동화

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| 패키지 | Claude.ai 통합 hosted MCP (`mcp.figma.com`) |
| 인증 방식 | OAuth · Claude.ai 자동 갱신 |
| 설치 위치 | Claude.ai > Settings > Integrations > Figma > Connect |
| 환경변수 | 없음 (0개) |
| 도구 prefix | `mcp__claude_ai_Figma__*` |
| Figma 플랜 | 무료 / Professional / Organization 모두 가능 |
| 접근 권한 | 본인 Figma 계정이 접근 가능한 모든 파일 |
