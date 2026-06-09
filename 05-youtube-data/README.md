# 클립 2-2. YouTube Data MCP · 유튜브 채널 분석·댓글 관리

## 한 줄 요약
유튜브 채널의 **영상별 조회수·반응·댓글**을 자연어로 분석하고, 자동 답글까지 작성합니다. 본인 채널은 **구독 변동·트래픽 소스·시청자 인구통계** 까지 깊이 있는 운영 분석 가능.

## 마케터에게 왜 필요한가
- 유튜브 광고/콘텐츠 마케터는 영상별 성과를 매주 손으로 정리
- 댓글에 일일이 답글 다는 데 1~2시간/주
- 어떤 영상이 잘 됐는지 분석 → 어떤 후속 영상을 만들지 결정에 시간 소요
- 구독자 이탈 원인 파악이 YouTube Studio 수동 확인밖에 안 됨

YouTube Data MCP 가 있으면 :
- 채널 영상 100개의 성과를 시트에 자동 정리
- 댓글을 카테고리별로 분류해 우선순위 답글 제안
- 본인 채널의 주간 구독 변동 + 이탈 영상 TOP 5 자동 리포트
- Part 4 **`trend-scanner` 에이전트** 가 키워드 트렌드 추적에 활용

---

## 🔑 활성화할 Google API 2개

본 클립에서는 **Google Cloud 프로젝트** 에 다음 2개의 API 를 활성화합니다.

| # | API | 인증 방식 | 접근 데이터 | 설치 가이드 |
|---|---|---|---|---|
| 1 | **YouTube Data API v3** | API Key | 공개 데이터 (조회수·댓글·구독자수·검색) | [`mcp설치-youtube/SKILL.md`](mcp설치-youtube/SKILL.md) |
| 2 | **YouTube Analytics API** | OAuth 2.0 (refresh_token) | **채널 소유자 전용** (구독 변동·트래픽 소스·시청자 인구통계) | [`analytics-api-oauth.md`](analytics-api-oauth.md) |

### 설치 순서

1. **Phase 1 (필수, 5분)** : Data API v3 + API Key → 메인 설치 스킬 `/mcp설치-youtube` 호출
2. **Phase 2 (응용, 15분 · 본인 채널 운영 분석용)** : Analytics API + OAuth → [`analytics-api-oauth.md`](analytics-api-oauth.md) 따라 진행

> 💡 두 API 모두 **같은 Google Cloud 프로젝트** 안에서 활성화됩니다. 신규 프로젝트 만들 필요 없음.

---

## 무엇이 가능해지나

### Phase 1 (Data API v3 · 공개 데이터)
- 채널·플레이리스트 메타데이터
- 영상별 통계 (조회수·좋아요·댓글수)
- 댓글·답글 읽기
- 검색 (키워드·기간·언어)
- 경쟁사 채널 분석

### Phase 2 (Analytics API · 본인 채널)
- 주간 구독 변동 (`subscribersGained` / `subscribersLost`)
- 영상별 이탈 분석 (어떤 영상에서 구독 취소가 일어났나)
- 트래픽 소스 (검색·외부 유입·추천 영상)
- 시청자 인구통계 (성별·연령·지역)
- 시청 지속률 (영상 길이·구간별)

---

## 사전 준비물
- Google 계정 (분석할 채널의 **소유 계정**)
- Google Cloud 프로젝트 (GA4 와 공유 가능)
- YouTube Data API v3 + YouTube Analytics API 활성화
- API Key (Data v3 용)
- OAuth 클라이언트 ID + refresh_token (Analytics 용 · Phase 2)
- 본인 채널 ID

## 작동 방식

```
[Claude 자연어 명령]
   ↓
[YouTube Data MCP]
   ├─ Data API v3  (API Key)        → 공개 데이터 (영상·댓글·검색)
   └─ Analytics API (OAuth)         → 본인 채널 전용 (구독 변동·시청자 분석)
   ↓
[자동 정리·분석 결과 출력]
```

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `quotaExceeded` (Data v3) | 일일 10,000 유닛 초과 | 새벽 12시 리셋 또는 쿼터 증가 신청 |
| `forbidden` (댓글 쓰기) | API Key 만으로는 불가 | OAuth 로 전환 필요 |
| `access_denied` (Analytics) | OAuth 테스트 사용자 미등록 | analytics-api-oauth.md STEP 2-5 참조 |
| `invalid_grant` (Analytics) | refresh_token 만료 | analytics-api-oauth.md STEP 5 재실행 |

→ [`실습.md`](실습.md) (Phase 1 메인 실습)
→ [`analytics-api-oauth.md`](analytics-api-oauth.md) (Phase 2 OAuth 셋업)
