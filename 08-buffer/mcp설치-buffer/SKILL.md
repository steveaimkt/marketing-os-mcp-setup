---
name: mcp설치-buffer
description: |
  Part 2 클립 3-1 (Buffer MCP) 전용 설치 스킬. Personal Access Token 발급 + .mcp.json 등록 (`@damusix/buffer-mcp` 패키지) 을 5~10분 안에 완료하고 신제품 5채널 동시 예약 1건을 자동 생성. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Buffer MCP 설치하자"** ⭐ 주요 트리거
  - "버퍼 MCP 설치"
  - "Buffer 연결 도와줘"
  - "SNS 자동 발행 환경 만들자"
  - "Part 2 / 3-1 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (Token + 채널 + .env + .mcp.json + 헬스 체크) →
  ③ 작업 가능 업무 (도구 2개 + 액션 7종 + 6 시나리오) →
  ④ 결과물 1개 (5채널 동시 예약 발행)

  특이점: 본 MCP 는 단일 진입점 (`use_buffer_api`) + 액션 키 방식. 도구 2개로 컨텍스트 절약.
---

# Part 2 / 3-1 Buffer MCP 설치 (클립 전용)

> 본 스킬은 Buffer MCP 를 Personal Access Token 방식으로 설치하고 5채널 동시 예약 1건을 자동 생성하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Buffer 1 도구에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
📣 Buffer MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Buffer MCP 는 'Claude 가 본인 SNS 채널에 직접 손을 뻗는 신경' 입니다.
  한 번 설치하면 모든 세션에서 자동 사용. 도구 2개 (단일 진입점) 만 노출됩니다.
  코드 작성 안 합니다. "5채널 동시 예약해줘" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (신규 가입 10~15분 · 기존 사용자 5분):

  📖 STEP 1: MCP 소개 (2분)
       1.1 한 줄 정의 + 제공사 + 라이선스
       1.2 단일 진입점 방식 설명
       1.3 Before vs After 비교 (2~3시간 → 5분)

  ⚙️ STEP 2: MCP 설치 (5~10분)
       2.1 Buffer Personal Access Token 발급 (사용자 3분)
       2.2 SNS 채널 연결 (Buffer 가입 시 1회, 5분)
       2.3 .env 토큰 추가 (자동 1분)
       2.4 .mcp.json 등록 (자동 1분)
       2.5 Claude Code 재시작 + 헬스 체크 (1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 2개 (use_buffer_api + buffer_api_help)
       3.2 액션 키 7종 (listChannels, createPost ...)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 (5분)
       4.1 신제품 5채널 동시 예약 발행
       4.2 결과 표 + Buffer 대시보드 확인

사전 점검 4가지부터:
  □ Node.js 18 이상
  □ Buffer 무료 계정 (publish.buffer.com)
  □ SNS 채널 1개 이상 (Instagram·Facebook·X·LinkedIn·Threads)
  □ Chrome 또는 Safari (Token 발급용)

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | SNS 5채널 (Instagram·Facebook·X·LinkedIn·Threads) 에 동시 예약 발행하는 도구 |
| 제공사 | damusix (커뮤니티 · `@damusix/buffer-mcp`) |
| 라이선스 | MIT |
| 인증 방식 | Personal Access Token (`BUFFER_ACCESS_TOKEN`) |
| 무료 한도 | Buffer Free 플랜 · 3채널 · 10개 예약 |
| 유료 한도 | Essentials $6/월 · 무제한 채널·예약 |
| Before | 5채널 손 발행 사이클 · 2~3시간/건 |
| After | "5채널 동시 예약" 한 줄 → 5분 자동 |

### 1.2 마케터 관점 활용 가능성

- **콘텐츠 캘린더 자동 연동** · Notion DB → Buffer 큐 자동 입력
- **채널별 톤·해시태그·길이 자동 조정** · 인스타 친근, X 280자, LinkedIn B2B 톤
- **시각 분배** · 채널별 ROAS 좋은 시간대 매핑
- **발행 후 모니터링** · 좋아요·도달·노출 회수 + 다음 주 기획 데이터

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| Instagram 캐러셀 캡션 | 30분 | 30초 |
| Story 변형 | 10분 | 10초 |
| Facebook 톤 변환 | 20분 | 20초 |
| X 280자 + 해시태그 | 15분 | 15초 |
| LinkedIn B2B 톤 | 30분 | 30초 |
| 5채널 발행 클릭 + 시각 설정 | 25분 | 0분 (자동) |
| **5채널 동시 발행 1건** | **2~3시간** | **5분** |
| **정기 운영 (주 5건)** | **10~15시간/주** | **25분/주** |

연간 환산: 약 600시간 절감 + 톤 일관성 100%.

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 5단계

### 2.1 STEP 1 / 5 · Buffer Personal Access Token 발급 (사용자 직접 · 3분)

사용자에게 안내:

```
브라우저에서 다음 5개 절차를 진행하세요.

① publish.buffer.com 접속 → 로그인 (또는 회원가입)
② 우상단 프로필 또는 좌하단 Settings 클릭
③ Apps & Extras 메뉴 → API 섹션
④ "Create Token" 또는 "Access Tokens" 클릭
⑤ 토큰 이름: "MCP-Token" (자유)
⑥ Generate → 생성된 토큰 복사 ⚠️ 한 번만 표시
⑦ 토큰 형식: 영문 + 숫자 + 특수문자 약 40~50자
```

토큰을 Claude 에게 전달 ("Token 은 abc123... 이야").

### 2.2 STEP 2 / 5 · SNS 채널 Buffer 연결 (사용자 직접 · 5분 · 신규 가입자만)

이미 Buffer 채널 연결되어 있으면 스킵:

```
사용자에게 묻기: "publish.buffer.com 에 이미 SNS 채널이 연결되어 있나요? (y/n)"
- y: 본 단계 스킵, STEP 3 로 진행
- n: 다음 안내
```

신규 가입자 안내:

```
① publish.buffer.com 메인 → "Add a channel" 클릭
② 연결할 SNS 선택 (Instagram · Facebook · X · LinkedIn · Threads)
③ 각 SNS 의 OAuth 인증 (Buffer 가 본인 SNS 에 발행 권한 요청)
④ 채널 이름 확인 후 저장
⑤ 여러 채널 반복 (Free 3개, Essentials 무제한)
```

### 2.3 STEP 3 / 5 · .env 토큰 추가 (Claude 자동 · 1분)

Claude 자동 실행:

```bash
cd "${CLAUDE_PROJECT_DIR}"

# .env 에 토큰 추가 (없으면 파일 생성)
if ! grep -q "BUFFER_ACCESS_TOKEN" .env 2>/dev/null; then
  echo "BUFFER_ACCESS_TOKEN=발급받은_토큰" >> .env
fi

# 검증
grep BUFFER_ACCESS_TOKEN .env
```

### 2.4 STEP 4 / 5 · .mcp.json 등록 (Claude 자동 · 1분)

`marketing-os/.mcp.json` 의 `mcpServers` 에 추가:

```json
"buffer": {
  "_part": "2 Ch 3-1 SNS 다채널 자동 발행",
  "command": "npx",
  "args": ["-y", "@damusix/buffer-mcp"],
  "env": {
    "BUFFER_ACCESS_TOKEN": "${BUFFER_ACCESS_TOKEN}"
  }
}
```

JSON 검증:

```bash
python3 -c "import json; json.load(open('.mcp.json'))"
```

### 2.5 STEP 5 / 5 · Claude Code 재시작 + 헬스 체크 (1분)

사용자에게 안내:

```
Claude Code 를 완전히 종료 (메뉴 > 종료 또는 ⌘Q) 후 재시작하세요.

새 세션에서 다음 명령으로 검증:
"Buffer 에 연결된 내 채널 목록 보여줘"

성공 응답 형식:
✅ Buffer 연결 확인. 사용자 채널 N개:
  1. @brand_instagram (Instagram · service_id: abc123)
  2. ...
```

내부적으로 `mcp__buffer__use_buffer_api(action="listChannels")` 호출됨.

### 2.6 보안 점검

설치 직후 확인:
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 값은 `${BUFFER_ACCESS_TOKEN}` 참조 (평문 직접 입력 금지)
- [ ] Token 이 git log 에 노출된 적 없는지 (실수로 commit 된 경우 즉시 Buffer 에서 재발급)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 2개

| 도구 | 역할 |
|---|---|
| `use_buffer_api` | Buffer API 호출 진입점 (액션 키 + 파라미터) |
| `buffer_api_help` | 사용 가능 액션 목록·파라미터 조회 |

### 3.2 액션 키 7종 (사용 빈도순)

| 액션 | 기능 | 마케팅 사례 |
|---|---|---|
| `listChannels` | 연결된 채널 목록 + service_id | 본인 Buffer 계정 채널 확인 |
| `createPost` ★ | 예약 게시물 생성 (텍스트·미디어·시각) | 단일 또는 다채널 동시 예약 |
| `listScheduled` | 예약 대기 큐 조회 | 이번 주 예약 현황 |
| `getPost` | 단일 게시물 상세 | 게시물 ID 로 상태 |
| `updatePost` | 예약 시각·텍스트 수정 | 발행 전 수정 |
| `deletePost` | 예약 취소 | 발행 전 취소 |
| `listAnalytics` | 채널별 성과 (좋아요·도달·노출) | 주간 성과 비교 |

### 3.3 마케터가 자주 쓰는 6 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 채널 조회 | "내 채널 보여줘" | 5초 |
| B. 단일 예약 | "내일 09시 Instagram 캐러셀" | 30초 |
| C. 다채널 동시 ★ | "신제품 5채널 동시 예약" | 5분 |
| D. 큐 상태 | "이번 주 예약 보여줘" | 10초 |
| E. 게시물 취소 | "오늘 18시 X 취소" | 5초 |
| F. 채널별 성과 | "지난주 좋아요·도달 비교" | 1~2분 |

### 3.4 다른 MCP 와 조합 시나리오

- **+ Notion MCP** · Notion DB 콘텐츠 카드 → Buffer 큐 자동 입력
- **+ Google Sheets MCP** · 콘텐츠 캘린더 시트 → 채널별 자동 분배
- **+ Discord MCP** · Buffer 예약 완료 시 Discord 알림 자동 발송
- **+ Figma MCP** · 캠페인 비주얼 Figma 생성 → Buffer 미디어 자동 첨부 (이미지 export 후 URL)

---

## 🎯 STEP 4: 결과물 1개 · 신제품 5채널 동시 예약

### 4.1 작업 선정 · 매주 운영에 그대로 쓰는 다채널 발행

```
사용자: "신제품 발표 메시지를 5채널에 동시 예약해줘.

핵심 메시지:
  '나이아신아마이드 10% 토너 출시. 모공·피지 케어 21일 챌린지 모집.'

채널·시각·톤:
  1. Instagram   - 2026-05-22 09:00 - 캐러셀 5장 + 친근 톤
  2. Instagram Story - 2026-05-22 12:00 - 짧은 1줄 + 스와이프업
  3. Facebook    - 2026-05-22 14:00 - 긴 글 + 스토리텔링
  4. X           - 2026-05-22 18:00 - 280자 + 해시태그 1~2
  5. LinkedIn    - 2026-05-23 09:00 - B2B 톤 + 성분·R&D"
```

### 4.2 4단계 자동 실행

```
Step 1 · listChannels 호출       (3초)
  - 채널 5개 service_id 매핑 확인
  - { instagram: "abc123", facebook: "def456", ... }

Step 2 · Claude · 5채널 톤 변환  (2분)
  - Instagram 캐러셀 캡션 (2,200자 이내, 해시태그 7개, 친근 이모지)
  - Story 짧은 1줄 (10자 이내, 스와이프업 액션)
  - Facebook 긴 글 (스토리텔링 + 후기 인용)
  - X 280자 압축 (해시태그 1~2개)
  - LinkedIn B2B 톤 (성분 과학 + R&D 강조 + 이모지 최소)

Step 3 · createPost × 5번 호출   (1분)
  - 각 호출: text, channels[service_id], scheduled_at (ISO 8601 UTC), media[]
  - Free 플랜 한도 (10개 예약) 사전 확인

Step 4 · 결과 표 출력             (즉시)
  ✅ 5개 게시물 큐에 등록 완료
  | # | 채널 | 예약 시각 (KST) | 게시물 ID | 미디어 |
  | 1 | Instagram | 2026-05-22 09:00 | post_abc | 5장 |
  ...
```

### 4.3 결과물 검증

성공 기준:
- [ ] 5개 게시물 ID 모두 반환됨
- [ ] Buffer 대시보드 (`publish.buffer.com`) 에서 5개 예약 모두 확인
- [ ] 각 채널 톤 일관성 (브랜드 보이스 유지)
- [ ] 발행 시각 ±5분 정확도 (UTC ↔ KST 변환 확인)
- [ ] 이미지 5장 모두 정상 업로드 (Instagram 캐러셀)

### 4.4 다음 단계 제안

```
🎉 첫 5채널 동시 예약 완성. 이걸 발전시키는 3가지 경로:

  A. 정기 자동화 (Part 3 · 10):
     - 매주 월요일 09:00 cron → content-publisher 에이전트
     - Notion '발행 캘린더' DB → Buffer 큐 자동 입력
     - 사용자 명령 0회 · 자동 가동

  B. 다른 MCP 결합:
     - "Notion MCP 설치하자" → 콘텐츠 캘린더 자동 연동
     - "Discord MCP 설치하자" → 예약 완료 알림 자동
     - "Figma MCP 설치하자" → 비주얼 생성 → Buffer 미디어 첨부

  C. 다음 Part 2 클립:
     - 3-2 Meta·Google Ads MCP (광고 성과 분석)
     - 4-1 Notion MCP (콘텐츠 캘린더)
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 3-1 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-buffer` 스킬을 호출해 Token 발급 + `.mcp.json` 등록을 5~10분 안에 완료하고, 신제품 발표 메시지를 5채널에 동시 예약.

### 실습 첫 결과물 명령 · 신제품 5채널 동시 예약

```
신제품 발표 메시지를 5채널에 동시 예약해줘.

핵심 메시지:
  "나이아신아마이드 10% 토너 출시. 모공·피지 케어 21일 챌린지 신청자 모집."

채널·시각·톤 설정:
  1. Instagram   - 2026-05-22 09:00 - 캐러셀 5장 (제품·전후·후기·할인·CTA)
  2. Instagram   - 2026-05-22 12:00 - 스토리 (간략 + 링크 스티커)
  3. Facebook    - 2026-05-22 14:00 - 긴 글 + 사진 1장
  4. X           - 2026-05-22 18:00 - 280자 이내 + 해시태그
  5. LinkedIn    - 2026-05-23 09:00 - B2B 톤 (성분·R&D 강조)

각 채널 톤·해시태그·이모지는 채널 특성에 맞게 자동 조정.
```

→ 약 5분 (사람 손으로 2~3시간).

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
D2C 화장품 브랜드 SNS 매니저

[입력]
신제품 발표 핵심 메시지 1개 (자연어 또는 마크다운)
+ 채널 매트릭스: 시각·톤·미디어 사양

[산출물]
5채널 동시 예약 + 결과 표 반환
→ Discord #marketing 채널에 예약 완료 알림
→ Notion '발행 캘린더' DB 자동 갱신 (status: scheduled)

[제약]
- Instagram: 캡션 2,200자 이내 · 해시태그 30개 이내
- X: 280자 이내 · 해시태그 1~2개
- LinkedIn: B2B 톤 · 성분·R&D 강조
- 이모지: 채널 특성에 맞춰 자동 조정 (LinkedIn 은 최소)
- 시각: 채널별 ROAS 히스토리 시간대 우선 사용

[검증]
- 5개 게시물 ID 표 반환
- Buffer 대시보드에서 5개 예약 모두 확인
- 각 채널 톤 일관성 (브랜드 보이스 가이드 준수)
- 발행 시각 ±5분 정확도
```

### 응용 과제

1. 본인 SNS 1개 채널로 "테스트 포스트" 즉시 발행 → Buffer 대시보드에서 확인
2. Notion DB 에 콘텐츠 카드 5개 준비 → "이 5개 카드를 이번 주 채널별 시간대에 자동 분배 예약"
3. 어제 발행 게시물의 성과 (`listAnalytics`) → 시간대별 평균 도달 표
4. **Part 3 콘텐츠 클립의 `content-publisher` 에이전트가 본 MCP 를 자동 호출** · 미리 채널 3개 이상 연결해 두기

---

## 트러블슈팅 (Buffer MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `401 Unauthorized` | Token 만료·오타·Bearer 형식 오류 | publish.buffer.com > Settings > Apps & Extras > API 에서 재발급 |
| 채널 목록이 비어 있음 | Buffer 대시보드에 SNS 채널 미연결 | publish.buffer.com 에서 SNS OAuth 연결 후 재시도 |
| `mcp__buffer__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `python3 -c "import json; json.load(open('.mcp.json'))"` 검증 + Claude Code 완전 종료 후 재시작 |
| 이미지 업로드 실패 | 로컬 파일 경로 사용 또는 비공개 URL | 공개 S3·CDN·Imgur URL 사용 (로컬 파일 안 됨) |
| `createPost` 후 게시물 발행 안 됨 | `scheduled_at` 시각 형식 오류 (UTC vs KST) | ISO 8601 UTC 형식 사용 (예: `2026-05-22T00:00:00Z` = KST 09:00) |
| Free 플랜 4번째 예약 실패 | `Quota exceeded` (Free 10개 한도) | Essentials 플랜 ($6/월) 또는 큐에서 일부 삭제 |
| 액션 키 오류 (`Unknown action`) | 잘못된 액션 이름 | `mcp__buffer__buffer_api_help` 로 사용 가능 액션 먼저 조회 |
| Instagram 캐러셀 실패 | 5장 미디어 URL 중 1개라도 접근 불가 | 5장 모두 공개 URL · 권장 사이즈 1080×1080 |
| LinkedIn 발행 권한 거부 | LinkedIn Personal Profile 만 연결 | Buffer 가 지원하는 LinkedIn Company Page 연결 필요 (Business 플랜 이상) |
| `npx @damusix/buffer-mcp` 첫 실행 느림 | npx 캐시 미생성 | 1회 사전 실행 후 캐시 생성 |

## 강의 연결

- 본 스킬은 [클립 3-1 Buffer MCP 대본](../대본/3-1-buffer.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Buffer 1 도구에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 Part 3 의 `content-publisher` 에이전트가 이어받아 활용 (콘텐츠 승인 → 자동 예약).
- Part 10 의 `weekly-content-publisher` 같은 자동화 에이전트가 본 스킬로 설치된 MCP 를 매주 월요일 cron 으로 호출.
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/08-buffer/mcp설치-buffer/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2) `marketing-agents/agents/mkt-channel-publish.md` · `marketing-agents/.mcp.json`

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| MCP 패키지 | `@damusix/buffer-mcp` (npx · 커뮤니티 fork) |
| Token 발급 URL | <https://publish.buffer.com> > Settings > Apps & Extras > API |
| Token 형식 | 영문 + 숫자 + 특수문자 약 40~50자 |
| Free 플랜 한도 | 3채널 · 10개 예약 큐 |
| Essentials 가격 | $6/월 · 무제한 채널·예약 |
| 지원 채널 | Instagram · Facebook · X · LinkedIn · Threads · TikTok · YouTube Shorts · Pinterest 등 |
| 시각 형식 | ISO 8601 UTC (KST = UTC+9) |
| Instagram 캐러셀 사이즈 | 1080×1080 (정사각형 권장) |
| 노출 도구 | `use_buffer_api`, `buffer_api_help` (단일 진입점 + 액션 키) |
| 주요 액션 키 | `listChannels`, `createPost`, `listScheduled`, `getPost`, `updatePost`, `deletePost`, `listAnalytics` |

## 메모리·문서 연결

- 사용자의 채널 service_id 매핑은 메모리로 저장 가능 (자주 사용)
- 브랜드 보이스 가이드 (채널별 톤·해시태그 규칙) 는 메모리 또는 `brand-voice` 스킬과 연결
- 본 스킬 종료 후 사용자가 "매주 자동 발행" 이라고 하면 Part 3 의 `content-publisher` 에이전트 또는 Part 10 의 `/agent-builder` 스킬로 전달
