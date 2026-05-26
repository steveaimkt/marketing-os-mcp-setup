---
name: mcp설치-youtube
description: |
  Part 2 클립 2-2 (YouTube Data MCP) 전용 설치 스킬. Google Cloud 프로젝트 + YouTube Data API v3 활성화 + API Key 발급 + (선택) 키 제한 + 본인 채널 ID + .mcp.json 등록 (`youtube-data-mcp-server` 패키지) 을 8~10분 안에 완료하고 키워드 검색 헬스 체크 + 가능한 분석 8가지 정리. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"YouTube MCP 설치하자"** ⭐ 주요 트리거
  - "유튜브 MCP 설치"
  - "YouTube Data MCP 연결"
  - "유튜브 채널 분석 자동화 환경"
  - "유튜브 댓글 관리 자동화"
  - "Part 2 / 2-2 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (GCP API + API Key + 키 제한 + 채널 ID + .env + .mcp.json + 헬스 체크) →
  ③ 작업 가능 업무 (도구 6개 + 6 시나리오) →
  ④ 결과물 1개 (연결 확인 헬스 체크) + 가능한 분석 8가지 정리

  특이점: API Key 단일 인증 방식 (GA4 의 Service Account JSON 보다 간단). 공개 데이터(채널·영상·댓글 읽기)는 API Key 만으로 가능. 본인 채널 댓글 쓰기는 OAuth 필요 (별도). Part 4 trend-scanner + Part 5 콘텐츠 기획 에이전트 기반 MCP.
---

# Part 2 / 2-2 YouTube Data MCP 설치 (클립 전용)

> 본 스킬은 YouTube Data MCP 를 API Key 단일 인증 방식으로 설치하고 키워드 검색 헬스 체크 + 가능한 분석 8가지를 안내하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 YouTube 의 API Key + Data API v3 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📺 YouTube Data MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  YouTube Data MCP 는 'Claude 가 유튜브 데이터를 직접 조회하는 신경' 입니다.
  GA4 의 Service Account JSON 보다 간단 · API Key 1개로 끝.
  코드 작성 안 합니다. "우리 채널 최근 영상 정리해줘" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (8~10분 예상):

  📖 STEP 1: MCP 소개 (2분)
       1.1 API Key 인증 + Data API v3 흐름
       1.2 도구 6개 (search_videos · get_channel · get_comments 등)
       1.3 Before vs After 비교 (60분 → 1분)

  ⚙️ STEP 2: MCP 설치 (8~10분) · Google API 연동
       2.1 GCP 프로젝트 + YouTube Data API v3 활성화 (사용자 2분)
       2.2 API Key 발급 (사용자 1분)
       2.3 (권장) API Key 제한 설정 (사용자 1분)
       2.4 본인 채널 ID 확인 (사용자 1분 · 선택)
       2.5 .env + .mcp.json 등록 (자동 2분)
       2.6 헬스 체크 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 6개 (search·channel·videos·video·comments·playlists)
       3.2 6 시나리오 (영상·댓글·트렌드·경쟁사·SEO·기획)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 + 가능한 분석 8가지
       4.1 키워드 검색 헬스 체크 (약 30초)
       4.2 이제 가능한 분석 8가지 정리 (안내만)

사전 점검 5가지부터:
  □ Google 계정 (GCP + 유튜브 접근 가능)
  □ Google Cloud 프로젝트 (GA4 클립에서 만든 거 재사용 가능)
  □ Node.js 18+ (`node --version`)
  □ (있으면) 본인 유튜브 채널 ID
  □ Chrome 또는 Safari

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | YouTube 채널·영상·댓글 데이터를 자연어로 조회하는 도구 |
| 제공사 | Anthropic 공식 MCP 서버 |
| 라이선스 | MIT |
| 인증 방식 | API Key (`YOUTUBE_API_KEY`) · 39자 AIza... |
| 연결 방식 | YouTube Data API v3 (HTTPS) |
| 도구 prefix | `mcp__youtube-data__*` (총 6개) |
| 무료 한도 | 일 10,000 unit (검색 100/회 · 채널·영상 1/회 · 댓글 1/100개) |
| Before | YouTube Studio 클릭·CSV·댓글 일일이 읽기 · 60분/주간 점검 |
| After | "우리 채널 최근 영상 + 댓글 분류" 자연어 한 줄 · 1분 |

### 1.2 마케터 관점 활용 가능성

- **주간 콘텐츠 회고 자동화** · 영상별 조회·좋아요·댓글 표 30초에 출력
- **댓글 응대 효율화** · 댓글 100개 → 4 카테고리 분류 + 답글 후보 TOP 10
- **키워드 트렌드 추적** · 본인 분야 핫 영상 발견 → 콘텐츠 아이디어
- **경쟁사 채널 모니터링** · 신작·구독자 증감 자동 추적
- **Part 4·5 에이전트 기반** · `trend-scanner` + 콘텐츠 기획 에이전트가 본 MCP 위에 구축됨

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| YouTube Studio 로그인 | 1분 | 즉시 (자연어 명령) |
| 영상별 CSV 내보내기 | 15분 | 30초 (get_channel_videos) |
| 댓글 수동 분류 (영상 5개) | 30분 | 20초 (get_comments + Claude 분류) |
| 경쟁사 채널 5개 방문 | 10분 | 10초 (get_channel 반복) |
| 트렌드 검색·메모 | 5분 | 20초 (search_videos) |
| **주간 콘텐츠 점검 1회** | **60분** | **1분** |
| **월간 (4주 + 답글 작성)** | **8~12시간** | **10~15분** |

연간 환산: 약 100~150시간 절감 + 댓글 응대율 50% → 95% (1,000개 댓글도 1분에 분류).

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 6단계

### 2.1 STEP 1 / 6 · GCP 프로젝트 + YouTube 관련 API 2개 활성화 (사용자 직접 · 3분)

사용자에게 안내:

```
브라우저에서 다음 절차를 진행하세요:

① https://console.cloud.google.com 접속 → Google 계정 로그인
② 상단 프로젝트 선택 드롭다운 → 기존 프로젝트(예: "marketing-os") 선택
   ⚠ GA4 클립에서 만든 프로젝트 그대로 재사용 가능
   ⚠ 없으면 "새 프로젝트" 클릭 → 이름 입력 → 만들기
③ 좌측 메뉴 ☰ → APIs & Services → Library

[필수] YouTube Data API v3 활성화
④ 검색창에 "YouTube Data API v3" 입력
⑤ 검색 결과의 첫 항목 클릭 → "Enable" 버튼 클릭
⑥ 활성화 완료 화면 확인 (Manage 버튼이 나타남)

[권장] YouTube Analytics API 활성화 (본인 채널 구독 변동·시청자 분석용)
⑦ 좌측 메뉴 ☰ → APIs & Services → Library 로 다시 이동
⑧ 검색창에 "YouTube Analytics API" 입력
⑨ 검색 결과 첫 항목 클릭 → "Enable" 버튼 클릭
⑩ 활성화 완료 확인
```

**두 API 의 차이** :

| API | 인증 | 데이터 | 본 STEP 에서 |
|---|---|---|---|
| **YouTube Data API v3** | API Key (이 스킬 STEP 2 에서 발급) | 공개 데이터 (조회수·댓글·검색) | 필수 활성화 |
| **YouTube Analytics API** | OAuth refresh_token (별도 셋업) | 본인 채널 (구독 변동·트래픽·인구통계) | 활성화만 미리. OAuth 셋업은 별도 |

→ Analytics API 의 OAuth 셋업은 [`../analytics-api-oauth.md`](../analytics-api-oauth.md) Phase 2 (약 15분) 에서 진행. 본 스킬은 Phase 1 (Data API v3 + API Key) 만 끝까지 다룸.

### 2.2 STEP 2 / 6 · API Key 발급 (사용자 직접 · 1분) ★ 핵심

사용자에게 안내:

```
같은 GCP 콘솔에서:

① 좌측 메뉴 ☰ → APIs & Services → Credentials
② 상단 "+ CREATE CREDENTIALS" 클릭 → "API key" 선택
③ 약 5초 만에 키 생성
④ 표시된 키 복사 (형식: AIza... 39자 문자열)
   예시: AIzaSyB-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
⑤ "CLOSE" 또는 "EDIT API KEY" 클릭
```

복사한 API Key 를 Claude 에게 전달.

⚠️ API Key 는 **시크릿** : git 커밋 금지, 공개 채널 공유 금지. 노출 시 Credentials 화면에서 "DELETE API KEY" 후 재발급.

### 2.3 STEP 3 / 6 · (권장) API Key 제한 설정 (사용자 직접 · 1분)

사용자에게 안내:

```
같은 Credentials 화면에서:

① 발급된 API Key 행 클릭 → "Edit API key" 화면
② "API restrictions" 섹션 → "Restrict key" 선택
③ 드롭다운에서 "YouTube Data API v3" 만 체크
④ 페이지 하단 "SAVE" 클릭
```

⚠️ **생략 가능** 하지만 보안상 강력 권장. 키 노출 시에도 YouTube 외 다른 Google API 호출은 차단되어 피해 최소화. 키 제한 후 반영까지 약 5분 소요.

### 2.4 STEP 4 / 6 · 본인 채널 ID 확인 (사용자 직접 · 1분 · 선택)

사용자에게 안내:

```
브라우저에서 다음 절차:

① https://www.youtube.com 본인 계정 로그인
② 우상단 프로필 아이콘 → "내 채널" 클릭
③ URL 확인 (둘 중 하나):
   - https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxx
     → UC 로 시작하는 24자 문자열이 채널 ID
   - https://www.youtube.com/@핸들이름
     → 채널 ID 확인: https://www.youtube.com/account_advanced 접속 → "채널 ID" 항목
④ 채널 ID 복사 (UC 로 시작하는 24자)
```

복사한 채널 ID 를 Claude 에게 전달.

⚠️ 본인 채널 없어도 OK : 검색·경쟁사 분석만 활용 가능. 그 경우 다음 단계로 스킵.

### 2.5 STEP 5 / 6 · .env + .mcp.json 등록 (Claude 자동 · 2분)

Claude 자동 실행:

```bash
cd "${CLAUDE_PROJECT_DIR}"

# .env 에 추가
if ! grep -q "YOUTUBE_API_KEY" .env 2>/dev/null; then
  echo "YOUTUBE_API_KEY=발급받은_AIza_키" >> .env
  # 본인 채널 ID 있으면 추가 (없으면 스킵)
  echo "YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxxx" >> .env
fi

# 검증
grep YOUTUBE_ .env
```

`marketing-os/.mcp.json` 의 `mcpServers` 에 추가:

```json
"youtube-data": {
  "_part": "2 Ch 2-2 유튜브 채널 분석·댓글 관리",
  "command": "npx",
  "args": ["-y", "youtube-data-mcp-server"],
  "env": {
    "YOUTUBE_API_KEY": "${YOUTUBE_API_KEY}"
  }
}
```

JSON 검증:

```bash
python3 -c "import json; json.load(open('.mcp.json'))"
```

(선택) API 직접 검증 (Key 유효성):

```bash
curl -sS "https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key=$(grep YOUTUBE_API_KEY .env | cut -d= -f2)&maxResults=1" | head -c 300
```

응답에 `"kind": "youtube#searchListResponse"` 가 있으면 키 정상.

### 2.6 STEP 6 / 6 · Claude Code 재시작 + 헬스 체크 (자동 1분)

사용자에게 안내:

```
Claude Code 를 완전 종료 (메뉴 > 종료 또는 ⌘Q) 후 재시작하세요.

새 세션에서 다음 명령으로 검증:
"유튜브에서 클로드코드 마케팅 키워드로 영상 TOP 5 조회수 순으로 검색해줘"
```

내부적으로 `mcp__youtube-data__search_videos` 호출됨.

성공 응답:

```
✅ YouTube 연결 확인. 'claude code marketing' TOP 5:

| # | 제목                          | 채널         | 조회수    | 업로드일   |
|---|------------------------------|--------------|-----------|-----------|
| 1 | Claude Code 마케팅 자동화...  | 한성국 채널  | 28,400   | 2026-05-12|
| 2 | 1인 마케터를 위한 Claude...   | 마케팅 OS    | 12,800   | 2026-05-15|
| ...

사용 가능 도구 6종: search_videos, get_channel, get_channel_videos, get_video, get_comments, get_playlists
일일 쿼터 사용: 100 unit / 10,000 (1%)
```

응답 안 옴 시 → 2.5 의 curl 검증 + Claude Code 재시작 확인.

### 2.7 보안 점검

설치 직후 확인:
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 값은 `${VAR}` 참조 (API Key 평문 직접 입력 금지)
- [ ] API Key 제한 설정 완료 (YouTube Data API v3 만 허용)
- [ ] API Key 가 git log · 슬랙 · 디스코드 등에 노출된 적 없는지
- [ ] 본인 채널 댓글 쓰기·답글이 필요한 경우 OAuth 2.0 별도 설치 안내 (이번 클립은 읽기만)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 6개

| 도구 | 기능 | 쿼터 비용 |
|---|---|---|
| `search_videos` ★ | 키워드·기간·언어로 영상 검색 | 100 unit/회 |
| `get_channel` | 채널 통계 (구독자·조회수·영상 수) | 1 unit |
| `get_channel_videos` | 채널의 영상 목록 (최근 N개) | 1 unit/페이지 |
| `get_video` | 영상 상세 (조회·좋아요·댓글·태그) | 1 unit |
| `get_comments` | 영상 댓글 수집 (최대 100개/페이지) | 1 unit/100개 |
| `get_playlists` | 채널 재생목록 | 1 unit |

### 3.2 마케터가 자주 쓰는 6 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 채널 영상별 성과 ★ | "우리 채널 최근 30일 영상 조회·좋아요·댓글 표로" | 30초 |
| B. 댓글 분류·답글 ★ | "최근 영상 5개 댓글 분류 + 답글 우선순위" | 1분 |
| C. 키워드 검색 트렌드 | "'클로드코드 마케팅' 최근 30일 TOP 10" | 20초 |
| D. 경쟁사 채널 모니터링 ★ | "경쟁 채널 UCxxx 최근 7일 신작" | 30초 |
| E. 태그·카테고리 분석 | "우리 영상 50개 태그·카테고리 분포" | 1분 |
| F. 베스트 영상 패턴 | "평균 1.5배 조회수 영상 TOP 3 공통점" | 1분 |

### 3.3 다른 MCP 와 조합 시나리오

- **+ Discord MCP** · 주간 콘텐츠 리포트 → 디스코드 #marketing 채널 자동 발송
- **+ Notion MCP** · 영상별 성과 표 → 노션 콘텐츠 캘린더 자동 갱신
- **+ Google Sheets MCP** · 영상 데이터 → 시트 자동 적재 + 차트
- **+ Firecrawl MCP** · YouTube 검색 결과 + 경쟁사 사이트 동시 분석
- **+ Higgsfield MCP** · 베스트 패턴 분석 → 새 인트로 영상 자동 생성

본 MCP 는 **Part 4 trend-scanner + Part 5 콘텐츠 기획 에이전트의 기반** · 콘텐츠 분석 파트의 핵심.

---

## 🎯 STEP 4: 결과물 1개 (연결 확인) + 가능한 분석 8가지

본 STEP 의 핵심은 **설치가 정상적으로 작동하는지 헬스 체크 한 줄로 확인**한 뒤, 이제 어떤 분석이 가능한지 카탈로그를 보여주는 것. 본격 활용은 Part 4·5 의 에이전트에서.

### 4.1 시연 · 연결 확인 헬스 체크 (약 30초)

**사전 조건**: API Key 정상 등록 + Claude Code 재시작 완료.

```
사용자 명령:

  유튜브에서 "클로드코드 마케팅" 키워드로 영상 TOP 5 조회수 순으로 검색해줘
```

자동 실행:

```
1. Claude → mcp__youtube-data__search_videos 호출
   - q: "클로드코드 마케팅"
   - order: viewCount
   - maxResults: 5
   - type: video

2. mcp-server-youtube → YouTube Data API v3 호출

3. 결과 → 마크다운 표 변환·출력
   소요: 약 30초 (검색 100 unit 사용)
```

성공 기준 (헬스 체크):
- [ ] 응답에 영상 5건 표시
- [ ] 제목 · 채널명 · 조회수 · 업로드일 4열 모두 반환
- [ ] 도구 6종(`search_videos`, `get_channel`, `get_channel_videos`, `get_video`, `get_comments`, `get_playlists`) 모두 활성화 확인
- [ ] `403 Forbidden` 또는 `quotaExceeded` 에러 없음
- [ ] 약 30초 안에 응답

이 한 줄이 응답하면 **설치 검증 완료**. 본격 분석은 Part 4·5 에이전트에서.

### 4.2 이제 가능한 분석 8가지 (안내)

설치 검증 후 본인 채널 또는 경쟁사 채널에서 자연어 한 줄 명령으로 가능한 분석을 8개 카테고리로 정리:

| # | 분석 | 자연어 명령 예시 | 핵심 도구 |
|---|---|---|---|
| 01 | 채널 통계 | "우리 채널 구독자·총 조회수·영상 수" | `get_channel` |
| 02 | 영상별 TOP 10 | "최근 30일 영상 조회·좋아요·댓글 표" | `get_channel_videos` + `get_video` |
| 03 | 댓글 감정 분석 | "최근 영상 5개 댓글 100개 긍정·부정·질문 분류" | `get_comments` |
| 04 | 키워드 트렌드 | "'클로드코드 마케팅' 핫 영상 TOP 10" | `search_videos` |
| 05 | 경쟁사 채널 추적 | "경쟁 채널 UCxxx 최근 7일 신작 + 구독자" | `get_channel` + `get_channel_videos` |
| 06 | 답글 우선순위 | "VIP·질문·부정 댓글 TOP 10 추출" | `get_comments` |
| 07 | 태그·SEO 분석 | "우리 영상 50개 태그·카테고리 분포" | `get_video` |
| 08 | 베스트 영상 패턴 | "평균 1.5배 조회수 영상 TOP 3 공통점" | `get_channel_videos` + `get_video` |

채널 ID·차원 이름 외울 필요 없음 : Claude 가 자연어를 자동 매핑.

### 4.3 다음 단계 제안

```
🎉 YouTube Data MCP 설치 + 연결 확인 완료. 다음 가능합니다:

  A. 위 8가지 분석 직접 호출:
     - "우리 채널 최근 30일 영상 표" (02 영상별 TOP)
     - "최근 영상 댓글 100개 분류" (03 감정 분석)
     - "경쟁 채널 UCxxx 신작 추적" (05 경쟁사)

  B. 다른 MCP 와 조합:
     - + Discord MCP: 주간 콘텐츠 리포트 디스코드 자동 발송
     - + Notion MCP: 영상 성과 → 노션 콘텐츠 캘린더 자동 갱신
     - + Higgsfield MCP: 베스트 패턴 → 새 인트로 영상 자동 생성

  C. Part 4·5 에이전트 · 위 8가지를 자동화:
     - trend-scanner (Part 4): 키워드 트렌드 매일 자동 추적
     - youtube-content-analysis (Part 5): 주간 영상 성과 자동 리포트
     - youtube-comment-responder (Part 5): 댓글 자동 분류 + 답글 우선순위

  D. 다음 MCP 설치 (Part 2 진행):
     - 06-higgsfield: AI 영상·이미지 생성
     - 또는 본인 채널 댓글 쓰기 OAuth (별도)
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 2-2 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴.

### 실습 한 줄 요약

GCP 에서 YouTube Data API v3 활성화 → API Key 발급 → `.mcp.json` 등록 → 본인 채널 없이도 키워드 검색으로 헬스 체크.

### 실습 헬스 체크 명령 (본인 채널 없어도 OK)

```bash
claude "유튜브에서 '클로드코드 마케팅' 키워드로 검색한 영상 TOP 10을 조회수 순으로 정리"
```

### 마케터 5패턴 · 본인 채널 분석

```
[역할] D2C 브랜드의 유튜브 콘텐츠 마케터.

[입력] 본인 채널 ID (UCxxxxxx) 최근 30일.

[산출물]
  1. 영상별 (제목 · 업로드일 · 조회 · 좋아요 · 댓글) 표
  2. 평균 대비 1.5배 이상 잘된 영상 TOP 3 + 공통 패턴
  3. 댓글 100개 샘플 → 긍정/부정/질문 분류

[제약] 한국어. 통계는 정수 + 콤마.

[검증] 데이터 추출 기간과 영상 수를 명시.
```

---

## 트러블슈팅 (YouTube Data MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `403 Forbidden` 또는 `keyInvalid` ★ | API Key 오타 또는 키 제한 잘못 설정 | `.env` 의 키 재확인 + 키 제한에 "YouTube Data API v3" 추가 |
| `quotaExceeded` | 일일 10,000 unit 초과 | 새벽 12시(태평양시간) 리셋 또는 GCP 콘솔 → Quotas 증가 신청 |
| `404 Not Found: API` | YouTube Data API v3 비활성화 | GCP 콘솔 → APIs & Services → Library → Data API v3 활성화 |
| `Analytics API not enabled` | 잘못된 API 활성화 (수익·인구통계용) | "YouTube Data API v3" 활성화 · Analytics API 는 OAuth 별도 |
| `mcp__youtube-data__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `python3 -c "import json; json.load(open('.mcp.json'))"` 검증 + Claude Code 완전 종료 후 재시작 |
| 응답이 비어 있음 (검색 0건) | 키워드에 매칭 영상 없음 또는 지역 제한 | 더 일반적인 키워드 시도 + `regionCode: KR` 명시 |
| 댓글 안 가져옴 | 영상의 댓글 비활성화 또는 비공개 | 다른 영상 ID 로 시도 + 영상 댓글 설정 확인 |
| 댓글 쓰기·답글 안 됨 | API Key 만으로는 불가 (읽기 전용) | OAuth 2.0 인증 별도 설정 (본 클립 범위 외) |
| `npx -y youtube-data-mcp-server` 실행 실패 | Node.js 미설치 또는 18 미만 | `node --version` 확인 + 18+ 설치 |
| 한글 검색 결과 깨짐 | 인코딩 또는 regionCode 미설정 | 명령에 "한국 영상" 명시 또는 regionCode: KR 지정 |
| 채널 ID UC 접두사 미인식 | 핸들(@) 형식 사용 | https://www.youtube.com/account_advanced 에서 UC 형식 ID 복사 |
| 첫 호출 시 느림 (10~20초) | npx 첫 다운로드 | 두 번째 호출부터 빠름 |

## 강의 연결

- 본 스킬은 [클립 2-2 YouTube Data MCP 대본](../대본/2-2-youtube.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 YouTube 의 API Key + Data API v3 패턴에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 **Part 4·5 콘텐츠 에이전트의 기반**:
  - Part 4 · `trend-scanner` · 키워드 트렌드 매일 자동 추적
  - Part 5 · `youtube-content-analysis` · 주간 영상 성과 자동 리포트
  - Part 5 · `youtube-comment-responder` · 댓글 자동 분류 + 답글 우선순위
- 다른 활용 에이전트:
  - Part 4 · `competitor-monitor` · 경쟁사 채널 + 사이트 통합 추적
  - Part 10 · `orchestrator` · "/weekly-content" 슬래시 명령 라우팅
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/05-youtube-data/mcp설치-youtube/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2)
  - `marketing-agents/.mcp.json` (mcp-server-youtube 등록 예시)
  - `marketing-agents/agents/trend-scanner.md`
  - `marketing-agents/agents/youtube-content-analysis.md`
  - `marketing-agents/agents/youtube-comment-responder.md`

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| MCP 패키지 | `youtube-data-mcp-server` (npx) |
| Google API | YouTube Data API v3 (Data API · NOT Analytics API) |
| 인증 방식 | API Key 단일 (Service Account 불필요) |
| API Key 형식 | `AIza` 로 시작하는 39자 문자열 |
| 채널 ID 형식 | `UC` 로 시작하는 24자 (예: UCxxxxxxxxxxxxxxxxxxxxxx) |
| 일일 쿼터 | 10,000 unit · 자정(태평양시간) 리셋 |
| 쿼터 단가 | 검색 100 · 채널 1 · 영상 1 · 댓글 100개 1 |
| 환경 변수 | `YOUTUBE_API_KEY` (+ 선택 `YOUTUBE_CHANNEL_ID`) |
| GCP Console | <https://console.cloud.google.com> |
| YouTube Studio | <https://studio.youtube.com> |
| 채널 ID 찾기 | <https://www.youtube.com/account_advanced> |
| Data API v3 문서 | <https://developers.google.com/youtube/v3> |
| 쿼터 계산기 | <https://developers.google.com/youtube/v3/determine_quota_cost> |
| 노출 도구 | 6개 (`search_videos`, `get_channel`, `get_channel_videos`, `get_video`, `get_comments`, `get_playlists`) |
| 자주 쓰는 파라미터 | `q` · `order` · `maxResults` · `regionCode` · `videoDuration` |

## 메모리·문서 연결

- 사용자의 본인 채널 ID + 경쟁사 채널 ID 목록은 메모리로 저장 (자주 사용)
- 본 스킬 종료 후 사용자가 "댓글 자동 답글" 이라고 하면 OAuth 별도 설정 가이드 안내 (본 클립 범위 외)
- 사용자가 "트렌드 매일 추적" 이라고 하면 Part 4 의 `trend-scanner` 에이전트로 전달
- 사용자가 "주간 콘텐츠 리포트" 라고 하면 Part 5 의 `youtube-content-analysis` 에이전트로 전달
- 영상 댓글 쓰기·답글 같은 쓰기 작업 요청 시 OAuth 2.0 + `youtube.force-ssl` 스코프 안내
