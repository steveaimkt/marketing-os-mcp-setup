# Part 2 · MCP 11개 폴더 종합 정리

> 위치: `curriculum/part02-MCP12개/` · 클립 1-2 ~ 4-2
> **11개 폴더 · 실제 MCP 13개** (07 트리오 3개, 09 광고 2개 포함)
> 작성일: 2026-05-26

---

## 한눈에 보기

| Ch | # | 폴더 | MCP | 한 줄 정의 | 인증 |
|---|---|---|---|---|---|
| **1. 데이터 분석** | 1-2 | `01-google-sheets/` | google-sheets | 매출·광고·재고 시트 4개 → 자연어 종합 리포트 | OAuth |
| | 1-3 | `02-ga4/` | ga4 | GA4 트래픽·전환 → 주간 리포트 자동화 | GCP 서비스 계정 |
| | 1-4 | `03-firecrawl/` | firecrawl | 쿠팡·경쟁사 리뷰 60건 비교 분석 | API Key |
| **2. 콘텐츠·영상·디자인** | 2-1 | `04-figma/` | figma (자체호스팅) | PPT 의뢰서 폐기 · Figma 와이어프레임 자동 생성 | bun socket + Plugin |
| | 2-2 | `05-youtube-data/` | youtube-data + analytics | 채널 KPI · 댓글 · 트래픽 분석 | API Key + OAuth |
| | 2-3 | `06-higgsfield/` | higgsfield | 광고 이미지·인트로·B-roll 1~3분 생성 | Claude.ai OAuth |
| | 2-4 | `07-영상제작/` | **Hyperframes + HeyGen + ElevenLabs** | 영상 1편 4.5h → 20분 (그래픽/사람/음성) | 로컬 CLI + API Key 2종 |
| **3. 배포·광고** | 3-1 | `08-buffer/` | buffer | 5채널 SNS 동시 예약 + 성과 회수 | Personal Access Token |
| | 3-2 | `09-ads/` | **meta-ads + google-ads** | 3매체 ROAS 통합 분석 + 예산 조정 | hosted OAuth + Dev Token |
| **4. 협업·운영** | 4-1 | `10-notion/` | notion | 콘텐츠 캘린더 30행 자동 입력 · 리포트 게시 | Claude.ai OAuth |
| | 4-2 | `11-discord/` | **discord-channels (공식)** | 폰 DM ↔ Claude 양방향 + Gmail·Calendar 결합 | Bot Token |

---

## Ch 1 · 데이터 분석 3종

### 1-2. Google Sheets MCP — `01-google-sheets/`
- **마케터에게**: 매출·광고·재고가 흩어진 시트 4개 → 자연어 한 줄로 종합 리포트
- **Before/After**: 분석 1건 15~30분 → 5~10분, 주간 종합 리포트 반나절 → 5분
- **절감**: 주 3시간 30분, **연 약 180시간**
- **대표 도구 10개**: `get_spreadsheet_info` / `read_sheet` / `batch_read_sheet` / `write_sheet` / `append_sheet` / `format_cells` / `create_chart` / 외
- **인증**: OAuth (Google Cloud 데스크톱 클라이언트)
- ⚠ **루트에서 claude 실행** 안 하면 로드 실패

### 1-3. GA4 MCP — `02-ga4/`
- **마케터에게**: GA4 화면 캡처·정리 매주 1~2시간 → 자연어 1줄
- **Before/After**: 주간 리포트 60분 → 1분
- **대표 도구**: `run_report` ★ / `batch_run_reports` / `get_realtime_data`
- **인증**: GCP 서비스 계정 + GA4 속성 권한
- ⚠ ADC 스코프 차단 시 자체 OAuth 데스크톱 클라이언트 사용

### 1-4. Firecrawl MCP — `03-firecrawl/`
- **마케터에게**: 쿠팡 JS 렌더·봇 차단으로 일반 크롤러 불가 → Firecrawl로 가능
- **Before/After**: 본인+경쟁사 60건 비교 90분 → 2분
- **대표 도구 9개**: `monitor_create` ⭐ / `scrape` / `crawl` / `extract` / `search` / `parse` / `map` / `interact` / `agent`
- **인증**: API Key
- ⚠ `.mcp.json`의 `${FIRECRAWL_API_KEY}` 환경변수 **export 필수**
- ⚠ 쿠팡: 상품정보=markdown scrape, 리뷰=브라우저 in-page, 상세=차단

---

## Ch 2 · 콘텐츠·영상·디자인 4종

### 2-1. Figma MCP — `04-figma/`
- **마케터에게**: PPT 의뢰서 1~2시간 폐기 · Figma 네이티브 공동작업
- **Before/After**: 카드뉴스 8장 기획안 2시간 → 1~2분
- **노선**: 2026-05-26 부터 자체호스팅 `cursor-talk-to-figma-mcp@latest` (bunx)
- **인증**: bun socket 3055 + Figma Community Plugin Connect + `join_channel`
- ⚠ write timeout 시 view-only 파일 또는 parentId 누락 · 사전 3단 검증 필수

### 2-2. YouTube Data MCP — `05-youtube-data/`
- **마케터에게**: 채널 영상 100개 성과 자동 정리 + 댓글 분류 + 구독 이탈 원인
- **2개 API 분리**:
  - Phase 1: **YouTube Data API v3** + API Key (공개 데이터)
  - Phase 2: **YouTube Analytics API** + OAuth refresh_token (소유자 전용)
- **대표 도구**: `searchVideos` / `getChannelStatistics` / `getVideoDetails` / `getTranscripts` / `getTrendingVideos` 외

### 2-3. Higgsfield MCP — `06-higgsfield/`
- **마케터에게**: 외주 5~10만원/장 · 며칠 대기 → 1~3분 자체 생성
- **케이스**: 광고 이미지 / 5초 인트로 / 캐러셀 5장 / B-roll / 바이럴 점수 예측 / 캐릭터·아바타
- **인증**: Claude.ai 통합 (OAuth 1클릭)

### 2-4. 영상제작 트리오 — `07-영상제작/`
영상은 **3 레이어**로 분해 → 트리오로 1편 30분 내 완성. **주당 20시간 절감, 연 1,040시간**.

| 레이어 | 도구 | 역할 | 인증 | 무료 한도 |
|---|---|---|---|---|
| 그래픽 | **Hyperframes** | HTML+CSS+GSAP | 로컬 CLI | 무제한 (Apache 2.0) |
| 사람 | **HeyGen MCP** | 아바타 토킹헤드 | API Key | 월 10 크레딧 |
| 음성 | **ElevenLabs MCP** | 한국어 TTS · 음성 클론 | API Key | 월 1만 크레딧 (10분) |

- **케이스 4종**: 데이터 KPI 영상 / 아바타 광고 / 다국어 / 풀 마케팅 영상

---

## Ch 3 · 배포·광고 2종

### 3-1. Buffer MCP — `08-buffer/`
- **마케터에게**: 5개 SNS 채널별 톤·길이·해시태그 다르게 올리는 2~3시간 → 5분
- **케이스**: 채널 조회 / 단일 예약 / 다채널 동시 예약 ★ / 큐 확인 / 취소 / 성과 분석
- **패키지**: `@damusix/buffer-mcp` (npx)
- **인증**: `BUFFER_ACCESS_TOKEN` (Personal Access Token)

### 3-2. Meta · Google Ads MCP — `09-ads/`
- **마케터에게**: 3매체 매니저 UI 왕복 → 통합 ROAS 리포트 3분, 예산 조정 1줄
- **Before/After**: 일일 분석 1.5시간 → 1~2분 · **연 약 580시간 절감**
- **2개 MCP**:
  - **Meta Ads MCP** — hosted OAuth
  - **Google Ads MCP** — Developer Token + OAuth (승인 1~2일 대기)
- **케이스**: 통합 ROAS / 예산 재배분 / 임계치 자동 감지 / 캠페인 생성·수정

---

## Ch 4 · 협업·운영 2종

### 4-1. Notion MCP — `10-notion/`
- **마케터에게**: 콘텐츠 캘린더 30~50행 수동 입력 1시간 → 5분
- **케이스**: 워크스페이스 검색 / 페이지 가져오기 / **페이지 생성 ★** / **DB 카드 일괄 등록 ★** / 페이지 수정 / 새 DB 생성 / 댓글
- **인증**: Claude.ai 통합 (OAuth 1클릭)

### 4-2. Discord Channels — `11-discord/`
> ⚠ **2026-05-26 단독 노선 전환**: Anthropic 공식 `discord@claude-plugins-official` 단독 · 서드파티 `mcp-discord` (barryyip0625) **폐기**

- **마케터에게**: 외출·이동 중 폰 DM → Claude 분석 → 폰 답신
- **시나리오 8개**:
  1. 폰 DM 양방향 채팅 ★
  2. **Gmail 결합** 분석 ★ (CS 메일 분류)
  3. **Calendar 결합** ★ (오늘 일정 · 미팅 추가)
  4. 첨부 파일 분석 (PDF 요약)
  5. 진행 상황 라이브 업데이트 (`edit_message`)
  6. 최근 100개 메시지 요약
  7. 도구 권한 원격 승인
  8. 멀티 채널 동시 운영
- **인증**: Bot Token (공식 Bot B · marketing-ch)

---

## 인증 방식 분포

| 방식 | MCP |
|---|---|
| 로컬 CLI / 무인증 | Hyperframes · Figma 자체호스팅 |
| API Key 단순 | Firecrawl · YouTube Data · HeyGen · ElevenLabs · Buffer |
| OAuth (자체 발급) | Google Sheets · GA4(서비스 계정) · YouTube Analytics · Meta Ads · Google Ads |
| Claude.ai OAuth 1클릭 | Higgsfield · Notion |
| Bot Token | Discord |

## 폴더 수 vs MCP 수

- **11 폴더** (01~11) · 인트로 `00-MCP란-무엇인가` 제외
- **실제 MCP 13개**: 07 트리오(+2) + 09 광고(+1) - 05 YouTube는 단일 MCP에 2 API
- `05-youtube-data`: API 2개(Data v3 + Analytics)지만 단일 MCP 서버

## 학습 우선순위 (강의 진행 순)

```
1-2 → 1-3 → 1-4         (데이터 기반)
2-1 → 2-2 → 2-3 → 2-4   (콘텐츠 자산)
3-1 → 3-2               (배포·광고 실행)
4-1 → 4-2               (협업·자동화 허브)
```

## 체크리스트 (Part 2 종료 후)

- [ ] `claude mcp list` 명령으로 13개 MCP 모두 보임
- [ ] 각 MCP 최소 1개 명령으로 헬스 체크 통과
- [ ] `.env` 파일에 모든 API 키 입력 완료
- [ ] `.mcp.json` 한 번 열어 서버 구성 이해
- [ ] Part 3 진입 준비 완료
