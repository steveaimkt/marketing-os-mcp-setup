---
name: youtube-channel-analyzer
description: |
  Part 2 클립 2-2 (YouTube Data MCP) 실습 스킬. Phase 1 (Data API v3 · 공개 데이터) 시연 4가지
  + Phase 2 (Analytics API · 본인 채널 운영 분석) 시연 5가지 메뉴 자동 노출.
  사용자가 채널 ID 또는 키워드 입력 → Claude 가 적절한 도구 자동 선택 → 마크다운 표 출력.

  자동 호출 트리거:
  - **"유튜브 채널 분석 시작하자"** ⭐ 주요 트리거
  - **"youtube-data 시작하자"** + 채널 ID 또는 키워드
  - "유튜브 영상 성과 정리"
  - "본인 채널 구독 변동 분석"
  - "YouTube Analytics 시연"
  - "유튜브 댓글 분류"
  - "유튜브 실습 시작"

  동작: 사용자 입력 (채널 ID·키워드·기간) → Phase 1·2 메뉴 노출 → 선택 → MCP 도구 자동 호출 →
  마크다운 표 (영상 성과·댓글 분류·트렌드·구독 변동·이탈 영상·트래픽 소스·인구통계) 출력 →
  (옵션) Google Sheets 1page 리포트 자동 적재.
---

# Part 2 / 2-2 · YouTube Data 실습 — 채널 분석 자동화

> 채널 ID·키워드만 던지면 Claude 가 Phase 1·2 데이터를 통합 분석해 마크다운 표로 출력.
> YouTube Data MCP 의 도구 6개 + Analytics API OAuth 토큰을 한 흐름에 시연하는 클립 2-2 실습 스킬.

## 전제 조건

- YouTube Data MCP 연결됨 (`mcp__youtube-data__*` 도구 노출)
- `.env` 에 `YOUTUBE_API_KEY` 등록됨 (Phase 1 필수)
- (Phase 2 사용 시) `YOUTUBE_OAUTH_CLIENT_ID` / `_SECRET` / `_REFRESH_TOKEN` 등록됨
- Phase 2 셋업이 안 되어 있으면 → [`../analytics-api-oauth.md`](../analytics-api-oauth.md) 안내

## 진행 포맷 (4단계 — 끊지 말고 한 흐름으로)

### 1️⃣ 안내 인사

```
📺 YouTube Data 실습을 시작합니다.
Phase 1 (공개 데이터) 4가지 + Phase 2 (본인 채널 운영 분석) 5가지 시나리오를 선택해 시연합니다.
```

### 2️⃣ Phase 자동 감지 + 실습 가능 업무 노출

`.env` 의 `YOUTUBE_REFRESH_TOKEN` 존재 여부로 Phase 1/2 가능 여부 자동 판별 :

```
📋 사용 가능한 시연 메뉴

▼ Phase 1 · Data API v3 (공개 데이터)
  1 ★ 영상별 성과 정리 (본인 채널 또는 경쟁사) → 30초
  2 ★ 댓글 분류 + 답글 초안 → 2~3분
  3   키워드 트렌드 검색 (TOP 30) → 1분
  4   경쟁사 채널 모니터링 (3곳 비교) → 1분

▼ Phase 2 · Analytics API (본인 채널 전용) {OAuth 미설치 시 ⚠ 안내}
  5 ★ 주간 구독 변동 (Gained vs Lost) → 30초
  6 ★ 이탈 영상 TOP 5 (구독 취소 원인) → 1분
  7   트래픽 소스 분석 → 30초
  8   시청자 인구통계 (성별·연령·지역) → 30초
  9   시청 지속률 (영상별·구간별) → 1분

어떤 시연부터 진행할까요? (번호 1~9 또는 자연어)
```

> Phase 2 OAuth 미설치 시 메뉴 5~9 에 `⚠ analytics-api-oauth.md 셋업 필요` 표시 + 사용자에게 셋업 진행 여부 물어봄.

### 3️⃣ 결과물 만들기 (선택된 시연 자동 실행)

#### Phase 1 시연 1 · 영상별 성과 정리

```
도구: youtube-data 의 search / video.list / commentThreads.list
입력: 채널 ID (UCxxxxxx) 또는 키워드 + 기간

처리:
  1. 채널 ID 면 → 최근 N개 영상 ID 조회 (search.list)
  2. 영상 ID 들로 통계 조회 (videos.list with statistics)
  3. 정렬·필터 (조회수·좋아요·댓글)
  4. 마크다운 표

출력:
  | 영상 | 업로드일 | 조회 | 좋아요 | 댓글 | 좋아요율 |
  | --- | --- | --- | --- | --- | --- |
  | ... | ... | ... | ... | ... | ... |
```

#### Phase 1 시연 2 · 댓글 분류 + 답글 초안

```
입력: 영상 URL 또는 영상 ID
처리:
  1. commentThreads.list 로 최신 100개 댓글
  2. Claude 가 긍정·부정·질문·스팸 4분류
  3. 우선 답변 5개 골라 답글 초안 작성

출력: 분류 표 + 답글 초안 5개 (수동 검토 후 게시)
```

#### Phase 2 시연 5 · 주간 구독 변동

```
도구: Analytics API · reports.query
파라미터:
  - dimensions: day
  - metrics: subscribersGained, subscribersLost, views
  - startDate: 7일 전 / endDate: 오늘

출력:
  | 일자 | 구독 증 | 구독 감 | 순증감 | 시청수 |
  | --- | --- | --- | --- | --- |
  + 일별 그래프 (텍스트 차트 또는 옵션 A 의 Google Sheets 차트)
```

#### Phase 2 시연 6 · 이탈 영상 TOP 5

```
파라미터:
  - dimensions: video
  - metrics: subscribersLost
  - sort: -subscribersLost
  - maxResults: 5
  - startDate: 30일 전

출력:
  | 영상 | 업로드일 | 길이 | 구독 취소 | 가설 |
  | --- | --- | --- | --- | --- |
  | ... | ... | ... | ... | Claude 가 영상 특성·업로드 시점·주제 분석해 가설 작성 |
```

### 4️⃣ 추가 가능 업무 안내 (마무리)

```
✅ 시연 완료. 이 결과로 다음 3가지를 추가로 할 수 있어요.

A. **Google Sheets 1page 종합 리포트**
   → "이 결과 1page 시트 보고서 양식으로 만들어" 한 줄.
   → 클립 1-2 결과물 양식 그대로 (제목·KPI·표·액션 박스).

B. **매주 자동 리포트 (Part 7 데이터 분석 에이전트)**
   → youtube-channel-analyzer 에이전트가 매주 월요일 09시 자동 실행
   → 주간 구독 변동 + 이탈 영상 TOP 5 + 트래픽 변화를 Discord #marketing 채널 발송
   → 본인 명령 0회 · 영구 자동

C. **Phase 2 OAuth 미설치였다면 지금 셋업** (15분 한 번)
   → analytics-api-oauth.md 의 STEP 1~6 진행 → 구독 변동 분석 가능해짐
```

## 트러블슈팅

| 증상 | 해결 |
|---|---|
| `quotaExceeded` (Phase 1) | Data API v3 일일 10,000 유닛 초과. 새벽 12시 리셋 또는 quota 증액 |
| `403 forbidden` (댓글 쓰기) | API Key 만으로는 불가. OAuth 전환 필요 |
| `access_denied` (Phase 2) | OAuth 테스트 사용자 미등록. analytics-api-oauth.md STEP 2-5 |
| `invalid_grant` (Phase 2) | refresh_token 만료. `.env` 의 `YOUTUBE_REFRESH_TOKEN=` 비우고 `--auth` 재실행 |
| 영상 ID 조회 실패 | 채널 ID 가 `UC` 로 시작하는지 확인 (UCxxxxxxx 22자) |

## 호출되는 도구

| 도구 | 역할 | Phase |
|---|---|---|
| `search` / `videos.list` / `commentThreads.list` | Phase 1 핵심 (영상·댓글) | 1 |
| `channels.list` | 채널 메타 정보 | 1 |
| Analytics `reports.query` | 구독 변동·이탈·트래픽·인구통계·시청 지속률 | 2 |
| Google Sheets MCP (옵션 A) | 1page 리포트 자동 적재 | 1+2 |
| Part 7 `youtube-channel-analyzer` 에이전트 (옵션 B) | 매주 자동 발송 | 1+2 |

## 참고 자료

- 5분 대본 : [`../대본/2-2-youtube-5min.md`](../대본/2-2-youtube-5min.md)
- 실습 가이드 (수동 명령) : [`../실습.md`](../실습.md)
- Phase 1 설치 스킬 : [`../mcp설치-youtube/SKILL.md`](../mcp설치-youtube/SKILL.md)
- Phase 2 OAuth 셋업 : [`../analytics-api-oauth.md`](../analytics-api-oauth.md)
