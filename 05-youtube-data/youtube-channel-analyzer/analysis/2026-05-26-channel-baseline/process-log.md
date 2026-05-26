# 분석 진행 로그 · 2026-05-26

> 본 분석을 어떻게 진행했는지의 **재현 가능한 절차 기록**. 다음 분석 시 동일 흐름으로 진행.

## 진행 흐름 (1시간 소요)

```
[1] /mcp설치-youtube 스킬 호출 (설치 체크)
    ↓
[2] 설치 검증: .env + .mcp.json + Data API curl + Analytics API OAuth
    ↓
[3] 분석 메뉴 5개 중 A/B/E 선택
    ↓
[4] 병렬 데이터 수집:
    - A: 톱5 영상 (search → videos)
    - B: 30일 일별 (Analytics API + Python 집계)
    - E: 톱1 자막 (youtube-transcript-api)
    ↓
[5] 통합 인사이트 도출 + 액션 3가지
    ↓
[6] 구글 시트 1page 리포트 (6섹션)
    ↓
[7] 폴더 정리 (본 폴더)
```

## 핵심 명령 (재실행 시 그대로 사용)

### A. 톱5 영상 + KPI

```bash
cd "${CLAUDE_PROJECT_DIR}" && set -a && source .env && set +a && \
curl -sS "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=$YOUTUBE_CHANNEL_ID&order=viewCount&maxResults=5&type=video&key=$YOUTUBE_API_KEY" > /tmp/top5_search.json
VIDEO_IDS=$(python3 -c "import json; d=json.load(open('/tmp/top5_search.json')); print(','.join([i['id']['videoId'] for i in d['items']]))")
curl -sS "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=$VIDEO_IDS&key=$YOUTUBE_API_KEY" > /tmp/top5_details.json
```

### B. 30일 구독 변동 (Analytics API)

```bash
ACCESS_TOKEN=$(curl -sS -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=$YOUTUBE_OAUTH_CLIENT_ID" \
  -d "client_secret=$YOUTUBE_OAUTH_CLIENT_SECRET" \
  -d "refresh_token=$YOUTUBE_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -sS "https://youtubeanalytics.googleapis.com/v2/reports?ids=channel==$YOUTUBE_CHANNEL_ID&startDate=2026-04-26&endDate=2026-05-25&metrics=views,subscribersGained,subscribersLost,estimatedMinutesWatched&dimensions=day&sort=day" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### E. 톱1 영상 자막 추출

```bash
uvx --from youtube-transcript-api python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
fetched = api.fetch('q50nmbs7PN0', languages=['ko'])
for s in fetched:
    print(f'[{s.start:.1f}s] {s.text}')
"
```

## 발생한 이슈 + 해결

| 이슈 | 원인 | 해결 |
|---|---|---|
| `mcp__youtube-data__getChannelTopVideos` API key invalid | MCP 서버가 세션 시작 시점의 .env를 캐시 | curl 우회 (직접 API 호출) |
| `getTranscripts(lang="ko")` 빈 결과 | MCP가 자동생성 자막 미지원 | youtube-transcript-api uvx 사용 |

## 다음 분석 (2026-06-26 예정) 체크리스트

- [ ] `/mcp설치-youtube` 헬스 체크 통과 (Data + Analytics 둘 다)
- [ ] 같은 명령으로 A/B/E 재실행
- [ ] 본 리포트 KPI와 비교 → 액션 효과 검증
- [ ] 새 톱5 진입 영상 발견 시 후킹 7요소 분석 추가
- [ ] 구글 시트 새 탭 추가 (베이스라인과 비교)
