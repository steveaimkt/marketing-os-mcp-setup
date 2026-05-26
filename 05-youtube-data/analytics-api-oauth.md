# YouTube Analytics API OAuth 셋업 가이드 (Phase 2 · 채널 소유자 전용 데이터)

> **위치** : Part 2 / Clip 2-2 (YouTube Data MCP) 의 **Phase 2 응용 셋업**
> **목적** : 구독자 취소율 (`subscribersLost`) 등 **채널 소유자만 볼 수 있는 데이터** 를 자동 수집하기 위한 일회성 인증
> **선행 조건** : Clip 2-2 메인 흐름 (YouTube Data API Key 발급) 완료
> **소요 시간** : 약 15분
> **비용** : 무료 (Analytics API quota 는 Data API 와 별도, 사실상 무제한)
> **보안** : 발급된 토큰은 본인 PC `.env` 에만 저장. 외부 전송 없음.

---

## Phase 1 vs Phase 2 차이

| 구분 | Phase 1 (Clip 2-2 메인) | Phase 2 (본 가이드) |
|---|---|---|
| 인증 방식 | API Key | OAuth 2.0 (refresh_token) |
| 접근 가능 데이터 | 공개 데이터 (조회수·댓글·구독자수) | **채널 소유자 전용** (구독 변동·트래픽 소스·시청자 인구통계) |
| 셋업 시간 | 5분 | 15분 (일회성) |
| 사용 케이스 | 경쟁사·트렌드 분석 | 본인 채널 깊이 있는 운영 분석 |

---

## 사전 조건

- Google 계정 (분석하려는 YouTube 채널의 **소유 계정**)
- 브라우저
- 기존에 `YOUTUBE_API_KEY` 를 발급받은 **Google Cloud 프로젝트** (Clip 2-2 메인에서 만들었음)

---

## STEP 1 — YouTube Analytics API 활성화 (3분)

> 💡 Phase 1 (`/mcp설치-youtube` 스킬) STEP 1 의 ⑦~⑩ 에서 이미 Analytics API 를 활성화했다면 본 STEP 은 건너뛰고 STEP 2 로 이동하세요.

1. https://console.cloud.google.com/ 접속 (채널 소유 Google 계정으로 로그인)
2. **좌상단 프로젝트 선택기** 클릭 → 기존 `YOUTUBE_API_KEY` 가 있는 프로젝트 선택 (Phase 1 에서 만든 프로젝트와 동일)
3. **상단 검색창** 에 `YouTube Analytics API` 입력 → 첫 결과 클릭
4. **사용 (ENABLE)** 버튼 클릭 (이미 활성화돼 있으면 `관리됨` 표시 · 그대로 다음 단계)
5. (확인) 같은 방법으로 `YouTube Data API v3` 도 활성화 상태인지 점검 (Phase 1 에서 활성화됐어야 함)

> ✅ **체크** : 두 API 모두 "관리됨" 상태면 완료

---

## STEP 2 — OAuth 동의 화면 구성 (5분, 첫 1회만)

이미 다른 OAuth 앱을 만든 적 있으면 STEP 3 으로 점프.

1. 좌측 메뉴 → **API 및 서비스 → OAuth 동의 화면**
2. **User Type** : `외부 (External)` 선택 → 만들기
3. **앱 정보** 입력 :
   - 앱 이름 : `Marketing OS YouTube Analytics` (본인 채널 식별 가능한 이름이면 OK)
   - 사용자 지원 이메일 : 본인 이메일
   - 개발자 연락처 : 본인 이메일
   - 나머지 빈칸 그대로 → **저장하고 계속**
4. **범위 (Scopes)** : 그냥 **저장하고 계속** (코드에서 동적으로 요청함)
5. **테스트 사용자** : **+ ADD USERS** → 본인 이메일 추가 → **저장하고 계속**
6. 마지막 요약 페이지 → **대시보드로 돌아가기**

> ⚠️ **중요** : `테스트 사용자` 에 본인 이메일이 들어있어야 인증이 작동합니다. (게시 상태 = "테스트" 그대로 두면 됨)

---

## STEP 3 — OAuth 클라이언트 ID 생성 (3분) ⭐

1. 좌측 메뉴 → **API 및 서비스 → 사용자 인증 정보 (Credentials)**
2. 상단 **+ 사용자 인증 정보 만들기** → **OAuth 클라이언트 ID**
3. **애플리케이션 유형** : `데스크톱 앱` 선택
4. **이름** : `Marketing OS Local Analytics`
5. **만들기** 클릭
6. 팝업으로 **클라이언트 ID** + **클라이언트 보안 비밀번호** 표시됨
   - 👉 두 값 **복사해서 메모장에 잠깐 붙여두기** (다음 단계에서 .env 에 넣음)
   - 또는 **JSON 다운로드** 버튼 클릭

---

## STEP 4 — `.env` 파일에 자격증명 추가 (1분)

`marketing-os/.env` 파일 열고 아래 3줄을 **맨 아래에 추가** :

```bash
# YouTube Analytics API (구독 변동 분석용 · Phase 2 · OAuth)
YOUTUBE_OAUTH_CLIENT_ID=<여기에-클라이언트-ID-붙여넣기>
YOUTUBE_OAUTH_CLIENT_SECRET=<여기에-시크릿-붙여넣기>
YOUTUBE_REFRESH_TOKEN=
```

- `YOUTUBE_REFRESH_TOKEN` 은 **빈 값으로 두세요**. 다음 STEP 에서 자동 채워집니다.

---

## STEP 5 — 최초 인증 실행 (3분, 한 번만)

`tools/youtube_oauth.py` 도구가 만들어진 후 (Part 7 데이터 분석 에이전트 단계) 다음과 같이 실행합니다 :

```bash
python3 tools/youtube_oauth.py --auth
```

**일어나는 일** :
1. 터미널에 인증 URL 출력 + 브라우저 자동 오픈
2. Google 로그인 페이지 → 채널 소유 계정 선택
3. **"이 앱은 Google 에서 확인하지 않았습니다"** 경고 화면 등장
   - **고급 (Advanced)** 클릭 → **앱 이름 (안전하지 않음) 으로 이동** 클릭
   - ⚠️ 본인이 만든 앱이라 안전합니다 (테스트 모드라서 뜨는 표준 경고)
4. 권한 승인 : `YouTube Analytics 데이터 보기` → **허용**
5. `localhost:8765` 로 리다이렉트 → 자동으로 코드 수신
6. 터미널에 `✅ Refresh token saved to .env` 출력
7. **이후 영원히 자동 동작** (refresh_token 만료 없음, 1회 인증으로 끝)

---

## STEP 6 — 동작 확인 (1분)

```bash
python3 tools/analyze_churn.py --days 7
```

7일 구독 변동 리포트가 나오면 성공 🎉

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `redirect_uri_mismatch` | 데스크톱 앱으로 안 만듦 | STEP 3 에서 **데스크톱 앱** 다시 선택 |
| `access_denied` | 테스트 사용자 미등록 | STEP 2-5 에서 본인 이메일 추가 |
| `invalid_grant` | refresh_token 만료/취소 | `.env` 의 `YOUTUBE_REFRESH_TOKEN=` 비우고 `--auth` 재실행 |
| 브라우저 자동으로 안 열림 | 터미널 환경 | 터미널에 출력된 URL 을 수동 복사해 브라우저 붙여넣기 |
| `403 channelNotMonetized` 비슷한 메시지 | API 미활성화 | STEP 1 재확인 |
| `quotaExceeded` | Analytics quota 도달 (드물게) | 24시간 대기 또는 Google Cloud Console 에서 quota 증액 신청 |

---

## 보안 메모

- `.env` 는 **절대 git commit 금지** (`.gitignore` 에 등록 확인)
- 토큰 노출 시 : Google Cloud Console → 사용자 인증 정보 → 해당 클라이언트 삭제 후 STEP 3 부터 재발급
- refresh_token 은 사용자가 Google 계정에서 직접 권한 취소 가능 : https://myaccount.google.com/permissions

---

## 활용 시나리오 (Part 7 데이터 분석 에이전트 연결)

본 OAuth 셋업이 끝나면 Part 7 의 데이터 분석 에이전트가 다음 자료를 자동 생성 가능 :

| 분석 | 호출 데이터 | 산출물 |
|---|---|---|
| **주간 구독 변동 리포트** | `subscribersGained` / `subscribersLost` / `views` | Discord 발송 + Notion 저장 |
| **이탈 영상 TOP 5** | 영상별 `subscribersLost` 순 | 콘텐츠 개선 백로그 |
| **트래픽 소스 분석** | `insightTrafficSourceType` | SEO·외부 유입 채널 점검 |
| **시청자 인구통계** | `viewerPercentage` (성별·연령) | 페르소나 검증 |
| **시청 지속률** | `audienceWatchRatio` | 영상 길이·구성 최적화 |

→ Part 7 의 `youtube-channel-analyzer` 에이전트가 본 OAuth 자격증명을 자동 활용합니다.

---

## 다음 단계

- 본 셋업 완료 후 → Clip 2-2 메인 [`실습.md`](실습.md) 의 Phase 2 응용 과제 진행
- Part 7 데이터 분석 에이전트 → 자동화된 주간 리포트 발송 (cron + Discord)
