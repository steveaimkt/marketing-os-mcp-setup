---
name: mcp설치-notion
description: |
  Part 2 클립 4-1 (Notion MCP) 전용 설치 스킬. Claude.ai OAuth 통합 활성화 + 노션 페이지 공유 (Add connections) 를 5~7분 안에 완료하고 콘텐츠 캘린더 30개 카드 자동 등록 1건을 시연. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Notion MCP 설치하자"** ⭐ 주요 트리거
  - "노션 MCP 설치"
  - "Notion 연결 도와줘"
  - "노션 자동화 환경 만들자"
  - "Part 2 / 4-1 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (인증 모드 + Claude.ai 통합 + 페이지 공유 + 헬스 체크) →
  ③ 작업 가능 업무 (도구 16개 + 7 시나리오) →
  ④ 결과물 1개 (콘텐츠 캘린더 30개 카드 자동 등록)

  특이점: API key 발급 없음. .mcp.json 등록도 없음. Claude.ai 통합 OAuth 1회 + 페이지 공유 1회로 완료.
---

# Part 2 / 4-1 Notion MCP 설치 (클립 전용)

> 본 스킬은 Notion MCP 를 Claude.ai OAuth 방식으로 활성화하고 콘텐츠 캘린더 30개 카드를 자동 등록하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Notion 의 OAuth 통합 패턴에 맞춰 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📝 Notion MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Notion MCP 는 'Claude 가 본인 노션 워크스페이스에 직접 손을 뻗는 신경' 입니다.
  본 MCP 는 API key 발급·.mcp.json 등록 모두 없습니다.
  Claude.ai 통합 OAuth 1회 + 노션 페이지 공유 1회만 하면 끝.

────────────────────────────────

총 4단계로 진행돼요 (5~7분 예상):

  📖 STEP 1: MCP 소개 (2분)
       1.1 한 줄 정의 + Claude.ai 통합 방식
       1.2 페이지 단위 공유 보안 모델
       1.3 Before vs After 비교 (1~2시간 → 5분)

  ⚙️ STEP 2: MCP 설치 (5~7분)
       2.1 Claude.ai 인증 모드 확인 (사용자 1분)
       2.2 Claude.ai 통합 활성화 · OAuth Allow (사용자 2분)
       2.3 노션 페이지 공유 · Add connections (사용자 2분)
       2.4 Claude Code 헬스 체크 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 16개 (검색·조회·생성·수정·DB·뷰·댓글)
       3.2 7 시나리오 (검색·조회·생성·일괄·수정·DB·댓글)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 (5분)
       4.1 5월 콘텐츠 캘린더 30개 카드 자동 등록
       4.2 결과 표 + Notion 캘린더 뷰 확인

사전 점검 4가지부터:
  □ Notion 무료 계정 (notion.so)
  □ Claude.ai 구독 (notion 통합은 claude.ai 구독 인증 필요)
  □ 본인 워크스페이스 1개 + 새 페이지 만들 권한
  □ Chrome 또는 Safari (OAuth 브라우저 인증용)

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | 노션 워크스페이스의 페이지·DB 를 직접 만들고 검색·수정하는 도구 |
| 제공사 | Notion 공식 (Claude.ai Integrations) |
| 라이선스 | 상업 (Notion 플랜) |
| 인증 방식 | OAuth (Claude.ai 통합) · API key 발급 없음 |
| 도구 prefix | `mcp__claude_ai_Notion__*` (총 16개) |
| 무료 한도 | Notion Free 플랜 (개인 무제한 · 팀 제한) |
| Before | 콘텐츠 캘린더 30~50행 수동 입력 · 1~2시간 |
| After | "30개 카드 등록" 한 줄 → 5분 자동 |

### 1.2 마케터 관점 활용 가능성

- **콘텐츠 캘린더 자동 갱신** · 매주 다음 주 카드 5~7개 자동 등록
- **광고 리포트 아카이브** · Part 6 광고 클립 에이전트가 매주 자동 게시
- **브랜드 가이드 자동 작성** · Part 5 의 `brand-guideline` 에이전트가 보이스·톤·페르소나 페이지 생성
- **고객 응대 위키 검색** · Part 8 의 `cs-responder` 가 위키 검색으로 정확한 답변
- **주간 리포트 자동 게시** · `mkt-weekly-report` 산출물 자동 Notion 게시

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| DB 페이지 열기 + 뷰 선택 | 1분 | 즉시 |
| 제목 30개 작성·복붙 | 30분 | 자동 |
| 날짜 30개 입력 | 10분 | 자동 |
| 채널·카테고리 분배 | 20분 | 자동 (스펙 기반) |
| 상태·담당자 설정 | 15분 | 자동 |
| 톤·키워드 일관성 검토 | 15~30분 | 자동 |
| **30개 카드 등록 1회** | **1~2시간** | **5분** |
| **정기 운영 (주간 갱신)** | **2~3시간/주** | **15분/주** |

연간 환산: 약 100시간 절감 + 데이터 일관성 100%.

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 4단계

### 2.1 STEP 1 / 4 · Claude.ai 인증 모드 확인 (사용자 직접 · 1분)

Claude Code 가 자동 확인:

```bash
# 현재 인증 상태 출력
claude /status
```

또는 사용자가 직접:

```
Claude Code 메뉴 > 인증 확인 또는 Settings
```

확인 사항:
- ✅ **Claude.ai 구독 모드** · 본 MCP 동작 가능
- ❌ **Anthropic API key 모드** · Notion 통합이 안 보임. 다음 명령으로 전환:

```bash
# API key 환경변수가 있으면 제거
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN
# claude.ai 로그인
claude /login
# → 브라우저에서 claude.ai 계정 선택
```

### 2.2 STEP 2 / 4 · Claude.ai 통합 활성화 (사용자 직접 · 2분)

사용자에게 안내:

```
브라우저에서 다음 절차를 진행하세요:

① claude.ai 접속 → 로그인 (구독 계정)
② 우상단 프로필 아이콘 → Settings
③ 좌측 메뉴 "Integrations" 또는 "Connectors" 선택
④ Notion 항목 찾기 → "Connect" 클릭
⑤ Notion OAuth 창 자동 열림
⑥ 본인 워크스페이스 선택 (여러 개면 사용할 것 선택)
⑦ Claude 가 접근할 권한 범위 확인 (Read · Write · Search · Comment)
⑧ "Allow access" 또는 "허용" 클릭
⑨ "✅ Notion connected" 표시 확인
```

✅ 활성화 후 `mcp__claude_ai_Notion__*` 도구 16개가 자동 노출됩니다. 일부 환경에서는 Claude Code 재시작 필요.

### 2.3 STEP 3 / 4 · 노션 페이지 공유 (사용자 직접 · 2분)

⚠️ **이 단계가 가장 자주 빠지는 단계**. 통합이 명시적으로 공유된 페이지만 접근 가능합니다.

```
사용자에게 묻기:
"본인 워크스페이스에 'Marketing' 같은 마케팅 모폴더 페이지가 있나요? (y/n)"

- y: 모폴더에 통합 공유 → 하위 페이지·DB 자동 접근
- n: 새 'Marketing' 페이지 만들고 거기에 공유 권장
```

공유 절차:

```
① Notion 에서 'Marketing' (또는 모폴더 페이지) 열기
② 우상단 ··· 메뉴 클릭
③ "Add connections" 또는 "연결 추가" 선택
④ 검색창에 "Claude" 입력 → 선택
⑤ "Confirm" 또는 "확인" 클릭
⑥ 해당 페이지와 모든 하위 페이지 접근 권한 부여됨
```

권장 패턴 · **워크스페이스 최상위 1개 페이지에 공유** → 하위 모든 페이지·DB 자동 접근. 페이지·DB 개별 공유는 비효율.

### 2.4 STEP 4 / 4 · Claude Code 헬스 체크 (자동 1분)

새 세션 또는 현재 세션에서 검증:

```
"노션 워크스페이스에서 콘텐츠 캘린더 찾아줘"
```

내부적으로 `mcp__claude_ai_Notion__notion-search` 호출됨.

성공 응답 형식:

```
✅ Notion 통합 확인. 검색 결과 N건:
  1. "콘텐츠 캘린더 2026" · 데이터베이스
     URL: notion.so/abc123...
  2. ...

사용 가능 도구 16종:
  - notion-search, notion-fetch
  - notion-create-pages, notion-update-page
  - notion-create-database, notion-query-database-view
  - notion-create-comment, notion-create-view, ...
```

검색 결과 0건이면 STEP 3 페이지 공유 누락. 다시 진행.

### 2.5 보안 점검

설치 직후 확인:
- [ ] 'Marketing' 같은 마케팅 영역에만 통합 공유 (회사 위키·HR·재무 페이지에 공유하지 말 것)
- [ ] OAuth 토큰은 Claude.ai 가 관리 · `.env` 에 저장할 필요 없음
- [ ] 통합 권한은 claude.ai > Settings > Integrations 에서 언제든 Revoke 가능

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 16개 (주요 7개)

| 도구 | 기능 | 마케팅 사례 |
|---|---|---|
| `notion-search` ★ | 워크스페이스 전체 검색 | 과거 페이지·문서 빠르게 찾기 |
| `notion-fetch` | 페이지·DB 내용 가져오기 | DB 스키마 + 카드 조회 |
| `notion-create-pages` ★ | 신규 페이지 또는 DB 카드 | 광고 리포트 게시, 캘린더 카드 등록 |
| `notion-update-page` | 페이지 속성·내용 수정 | 카드 상태 변경 |
| `notion-create-database` | 새 데이터베이스 생성 | 신규 프로젝트의 카탈로그·아카이브 |
| `notion-query-database-view` | DB 뷰 쿼리 (필터·정렬) | "status=approved" 카드 조회 |
| `notion-create-comment` | 페이지에 댓글 | 검수 결과·피드백 기록 |

기타 9개 도구: `notion-update-data-source`, `notion-create-view`, `notion-update-view`, `notion-duplicate-page`, `notion-move-pages`, `notion-get-comments`, `notion-get-users`, `notion-get-teams`, `notion-query-meeting-notes`.

### 3.2 마케터가 자주 쓰는 7 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 워크스페이스 검색 | "봄 캠페인 페이지 찾아줘" | 5초 |
| B. 페이지 조회 | "콘텐츠 캘린더 DB 이번 주 카드" | 10초 |
| C. 페이지 생성 ★ | "주간 리포트 페이지 만들어줘" | 30초 |
| D. DB 카드 일괄 등록 ★ | "5월 캘린더 30개 카드 등록" | 5분 |
| E. 페이지 수정 | "이 카드 상태 발행됨 변경" | 5초 |
| F. 새 DB 생성 | "광고 리포트 DB 만들어줘" | 1분 |
| G. 댓글 등록 | "검수 결과 코멘트 남겨줘" | 5초 |

### 3.3 다른 MCP 와 조합 시나리오

- **+ Google Sheets MCP** · GA4 데이터 → 시트 → Notion 주간 리포트 자동 게시
- **+ Buffer MCP** · Notion 콘텐츠 캘린더 → Buffer 큐 자동 입력
- **+ Discord MCP** · Notion 페이지 생성 완료 시 Discord 알림 자동 발송
- **+ Meta·Google Ads MCP** · 광고 성과 → Notion '광고 리포트 아카이브' DB 자동 게시
- **+ Firecrawl MCP** · 경쟁사 사이트 스크랩 → Notion 경쟁 분석 페이지 자동 작성

---

## 🎯 STEP 4: 결과물 1개 · 5월 콘텐츠 캘린더 30개 자동 등록

### 4.1 작업 선정 · 매주 운영에 그대로 쓰는 일괄 등록

```
사용자: "콘텐츠 캘린더 DB 에 5월 한 달 카드 30개 등록해줘.

카드 스펙:
- 제목: 자동 생성 (5월 신학기 캠페인 컨셉)
- 날짜: 5/1 ~ 5/31 (평일 주 5회 페이스)
- 채널: Instagram 15 / Facebook 8 / X 5 / LinkedIn 2
- 상태: 'draft' (모두 초안)
- 담당자: 본인
- 카테고리: 캠페인 15 / 일반 10 / UGC 5

브랜드 톤: 친근·전문성 균형 · 신학기·새 시작 키워드"
```

### 4.2 5단계 자동 실행

```
Step 1 · notion-search 호출       (3초)
  - '콘텐츠 캘린더' DB URL 검색
  - 결과: notion.so/abc123...

Step 2 · notion-fetch 호출         (5초)
  - DB 스키마 조회
  - 6 속성 확인 (Title · Date · Channel · Status · Owner · Category)
  - 각 속성 타입 (Select / Multi-select / Person) 검증

Step 3 · Claude · 30개 카드 데이터 생성 (1분)
  - 5월 평일 22 영업일 + 주말 8개 = 30개 매핑
  - 채널 비율 (IG 15·FB 8·X 5·LI 2) 분배
  - 카테고리 비율 (캠페인 15·일반 10·UGC 5) 분배
  - 제목 30개 자동 작성 (신학기·새 시작 키워드 + 채널 톤)

Step 4 · notion-create-pages × 30번 호출 (2분)
  - 각 호출: parent (DB URL) + properties (6 속성)
  - rate limit 회피 위해 100ms 간격
  - 페이지 ID 30개 반환

Step 5 · 결과 표 출력              (즉시)
  ✅ 30개 카드 등록 완료
  | # | 날짜    | 채널 | 카테고리 | 제목                        | URL |
  | 1 | 5/2 (목) | IG  | 캠페인   | 신학기, 책상 위 한 줄 응원 | ... |
  | 2 | 5/5 (월) | IG  | UGC     | ...                         | ... |
  ...
```

### 4.3 결과물 검증

성공 기준:
- [ ] 30개 카드 ID 모두 반환됨 (누락 0)
- [ ] Notion 캘린더 뷰에서 5월 30개 모두 표시
- [ ] 채널·카테고리 분포가 스펙과 일치 (IG 15·FB 8·X 5·LI 2)
- [ ] 브랜드 톤 일관성 (신학기·새 시작 키워드 30개에 자연스럽게 분산)
- [ ] 생성 시간 5~7분 이내

### 4.4 다음 단계 제안

```
🎉 첫 캘린더 30개 등록 완성. 이걸 발전시키는 4가지 경로:

  A. 다른 시나리오 시도:
     - "광고 리포트 아카이브 DB 만들어줘" (Case F)
     - "브랜드 가이드 페이지 작성" (Case C · Part 5 brand-guideline)
     - "이 카드 상태 발행됨 변경" (Case E)
     - "지난주 캠페인 페이지 검색" (Case A)

  B. 정기 자동화 (Part 3 · 10):
     - 매주 일요일 21:00 cron → content-publisher 에이전트
     - 다음 주 캘린더 자동 입력
     - 사용자 명령 0회 · 자동 가동

  C. 다른 MCP 결합:
     - "Discord MCP 설치하자" → 캘린더 등록 완료 시 알림
     - "Buffer MCP 설치하자" → 캘린더 → Buffer 큐 자동 입력

  D. 다음 Part 2 클립:
     - 4-2 Discord MCP (자동화 알림·승인 봇)
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 4-1 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-notion` 스킬을 호출해 Claude.ai 통합을 5분 안에 활성화하고, 5월 콘텐츠 캘린더 30개 카드를 한 줄 명령으로 자동 등록.

### 실습 첫 결과물 명령 · 5월 콘텐츠 캘린더 30개

```
콘텐츠 캘린더 DB 에 5월 한 달 카드 30개 등록해줘.

카드 스펙:
- 제목: 자동 생성 (5월 신학기 캠페인 컨셉)
- 날짜: 5월 1일 ~ 5월 31일 (주 5회 페이스 · 평일 위주)
- 채널: Instagram (15) · Facebook (8) · X (5) · LinkedIn (2)
- 상태: "draft" (모두 초안)
- 담당자: 자기 (admin 또는 본인 이메일)
- 카테고리: 캠페인 (15) · 일반 콘텐츠 (10) · 후기·UGC (5)

브랜드 톤: 친근·전문성 균형 · 신학기·새 시작 키워드
```

→ 약 5분 (수동 입력 1~2시간).

### 실습 두 번째 결과물 · 광고 리포트 아카이브 DB 자동 생성

```
광고 리포트 아카이브 DB 새로 만들어줘.

스키마:
- 제목 (Title)
- 날짜 (Date · 발행일)
- 매체 (Select · Meta·Google·네이버·Kakao)
- ROAS (Number · 소수점 2자리)
- 인사이트 (Text · 3~5문장)
- 상태 (Select · 검토중·승인·보관)
- 첨부 (URL · HTML 리포트 링크)
- 담당자 (Person)

위치: "Marketing > 광고" 하위 페이지.
뷰: 기본 캘린더 뷰 + "이번 달 ROAS 높은 순" 보조 뷰.
```

→ 약 1~2분. Part 6 광고 클립 에이전트들이 이 DB 에 매주 자동 게시.

### 실습 세 번째 결과물 · 브랜드 가이드 페이지 자동 작성

```
"브랜드 가이드라인" 페이지 만들어줘.

섹션:
1. 브랜드 보이스 (3 키워드 + 1줄 설명)
2. 톤 (Casual · Professional 비중)
3. 페르소나 (이상적 고객 1명 묘사)
4. 금기어 (사용 금지 5개)
5. 자주 쓰는 표현 (Do 10개 · Don't 5개)
6. 예시 카피 3종 (인스타·페북·LinkedIn 톤별)

위치: "Marketing > 콘텐츠" 하위.
```

→ 약 2분. Part 5 의 `brand-guideline` 에이전트가 이 패턴으로 자동 생성.

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
D2C 브랜드 콘텐츠 매니저 + 광고 운영 어시스턴트

[입력]
- 콘텐츠 캘린더 DB URL (월간 30개 카드 등록 대상)
- 광고 리포트 아카이브 DB URL (주간 게시 대상)
- 브랜드 가이드 페이지 (참조용)

[산출물]
매주 월요일 자동 수행:
  ① 광고 리포트 카드 1개 (notion-create-pages) · 매체별 ROAS·인사이트
  ② 콘텐츠 캘린더 다음 주 카드 5~7개 등록 (브랜드 톤 적용)
  ③ Discord #marketing 채널에 Notion URL 발송

[제약]
- DB 속성명 정확히 일치 (notion-fetch 로 사전 확인)
- 페이지 본문 마크다운 형식
- 브랜드 가이드 페이지 톤·금기어 준수
- 한국어 페이지 제목 (검색 안 되면 영문 키워드 병행 추가)

[검증]
- 30개 카드 등록 시 누락 0건
- DB 뷰의 캘린더에 30개 모두 표시
- 브랜드 톤 일관성 (가이드 페이지의 금기어 0건)
- 생성 시간 10분 이내
```

### 응용 과제

1. 본인 워크스페이스의 페이지 1개 (예: "테스트 페이지") 만들고 통합에 공유 → "내 워크스페이스 페이지 찾아줘" 로 검색 확인
2. 콘텐츠 캘린더 DB 본인 1개 만들고 → "5월 첫 주 콘텐츠 5개 카드 등록" 1회 시연
3. `notion-fetch` 로 DB 스키마 가져온 후 → AI 가 자동으로 카드 속성 채우기
4. **Part 5 콘텐츠·카피 클립에서 `brand-guideline` 에이전트가 본 MCP 를 자동 호출** · 미리 "브랜드 가이드라인" 페이지 위치 정해두기

---

## 트러블슈팅 (Notion MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `mcp__claude_ai_Notion__*` 도구 안 보임 | Claude.ai 통합 미활성화 또는 API key 모드 | claude.ai > Settings > Integrations > Notion > Connect + `/login` 으로 claude.ai 인증 |
| `Page not found` | 통합에 페이지 미공유 | 해당 페이지 우상단 ··· > Add connections > Claude 선택 |
| 워크스페이스 검색 0건 | 통합에 어떤 페이지도 미공유 | 최상위 모폴더 (예: 'Marketing') 에 공유하면 하위 자동 |
| `Property does not exist` | DB 속성명 오타 또는 영/한 불일치 | `notion-fetch <DB URL>` 로 정확한 속성명·타입 먼저 확인 |
| 한글 페이지 제목 검색 안 됨 | 검색 인덱스 지연 또는 토큰화 정확도 | URL 직접 사용 또는 영문 키워드 병행 |
| Calendar 뷰에 카드 안 나옴 | Date 속성 누락 또는 뷰 필터 차단 | 카드의 Date 속성 채워졌는지 확인 + 뷰 필터 점검 |
| 30개 등록 중 일부 실패 | Notion API rate limit (3 req/sec) | 자동 재시도 (100ms 간격 내장). 수동 시 1초 간격 |
| 페이지 삭제 후에도 검색 결과에 나옴 | Notion 휴지통에 남아 있음 | Notion UI 에서 휴지통 비우기 (영구 삭제) |
| `Insufficient permissions` | OAuth 권한 범위 부족 | claude.ai > Integrations > Notion > Manage permissions 확인 |
| Multi-select 속성에 새 옵션 추가 안 됨 | DB 의 Select 옵션 미정의 | Notion UI 에서 옵션 먼저 추가 후 재시도 |

## 강의 연결

- 본 스킬은 [클립 4-1 Notion MCP 대본](../대본/4-1-notion.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Notion 의 OAuth 통합 패턴에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 Part 3 의 `content-publisher` · Part 5 의 `brand-guideline` · Part 6 의 광고 리포트 에이전트 · Part 8 의 `cs-responder` 가 자동 호출.
- Part 10 의 `weekly-calendar-builder` 같은 자동화 에이전트가 본 스킬로 설치된 MCP 를 매주 cron 으로 호출.
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/10-notion/mcp설치-notion/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2)
  - `marketing-agents/agents/mkt-content-draft.md`
  - `marketing-agents/agents/mkt-brand-guideline.md`
  - `marketing-agents/agents/mkt-weekly-report.md`
  - `marketing-agents/docs/workflows/publishing.md`

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| 인증 방식 | OAuth (Claude.ai 통합) |
| 도구 prefix | `mcp__claude_ai_Notion__*` |
| 도구 수 | 16개 |
| .mcp.json 등록 | ✕ (불필요) |
| API key | ✕ (불필요) |
| Claude.ai 통합 URL | <https://claude.ai/settings/integrations> |
| 노션 페이지 공유 메뉴 | 페이지 우상단 ··· > Add connections > Claude |
| Notion API rate limit | 약 3 req/sec (개별 사용자 기준) |
| 권장 모폴더 공유 패턴 | 워크스페이스 최상위 1개 페이지 (예: 'Marketing') 에 공유 → 하위 자동 |
| 주요 7 도구 | search, fetch, create-pages, update-page, create-database, query-database-view, create-comment |
| 인증 모드 요구 | Claude.ai 구독 (Anthropic API key 모드 X) |

## 메모리·문서 연결

- 사용자의 콘텐츠 캘린더 DB URL · 브랜드 가이드 페이지 URL 은 메모리로 저장 가능 (자주 사용)
- 통합 공유 모폴더 (예: 'Marketing') 도 메모리로 저장 권장
- 본 스킬 종료 후 사용자가 "매주 캘린더 자동 갱신" 이라고 하면 Part 3 의 `content-publisher` 에이전트 또는 Part 10 의 `/agent-builder` 로 전달
- DB 속성 스키마는 메모리로 저장하지 말기 (변경될 수 있음 · `notion-fetch` 로 매번 확인)
