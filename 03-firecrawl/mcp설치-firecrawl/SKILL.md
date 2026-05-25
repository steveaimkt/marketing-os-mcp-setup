---
name: mcp설치-firecrawl
description: |
  Part 2 클립 1-4 (Firecrawl MCP) 전용 설치 스킬. API key 발급 + .env 등록 + .mcp.json (`firecrawl-mcp` 패키지) + 헬스 체크를 약 5분 안에 완료하고 경쟁사 3개 도메인 신제품 비교표 자동 생성 1건을 시연. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Firecrawl MCP 설치하자"** ⭐ 주요 트리거
  - "파이어크롤 MCP 설치"
  - "경쟁사 스크레이퍼 설치"
  - "웹 스크레이핑 자동화 셋업"
  - "Part 2 / 1-4 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After·대안 4종) →
  ② 설치 (API key 발급 + .env + .mcp.json + 헬스 체크) →
  ③ 작업 가능 업무 (도구 4개 + 6 시나리오) →
  ④ 결과물 1개 (경쟁사 3개 신제품 비교표 자동 생성)

  특이점: Cloud API 방식이라 노트북 부담 없음. 무료 500크레딧/월 강의용 충분. AI 친화 마크다운 출력. 본 강의 30개 에이전트 중 약 1/3 (리서치·콘텐츠·전략 계열) 이 호출.
---

# Part 2 / 1-4 Firecrawl MCP 설치 (클립 전용)

> 본 스킬은 Firecrawl MCP 를 Cloud API key 방식으로 설치하고 경쟁사 3개 도메인 신제품 비교표 자동 생성을 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Firecrawl 의 API key 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 클로드는 반드시 다음과 같이 시작 멘트를 출력:

```
🔥 Firecrawl MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Firecrawl 은 '경쟁사 사이트·시장 기사·랜딩 페이지를 마크다운으로 자동 변환' 하는 도구.
  헤드리스 브라우저가 Firecrawl 클라우드에서 실행되므로 본인 노트북 부담 없음.
  코드 작성 안 합니다. "도메인 3곳 신제품 비교표" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (약 5분 예상):

  📖 STEP 1: MCP 소개 (1분)
       1.1 도구 4개 (scrape, crawl, search, extract)
       1.2 Before vs After (1h 45m → 1m 20s)
       1.3 대안 4종 (Apify · Bright Data · Tavily · Jina Reader) 비교

  ⚙️ STEP 2: MCP 설치 (약 4분)
       2.1 firecrawl.dev 가입 + API key 발급 (사용자 2분)
       2.2 .env 등록 (자동 30초)
       2.3 .mcp.json 등록 (자동 30초)
       2.4 헬스 체크 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (1분)
       3.1 도구 4개 (scrape/crawl/search/extract)
       3.2 6 시나리오 (신제품 비교·기사 수집·광고 분석·도메인 크롤·정기 모니터링·시트 적재)
       3.3 다른 MCP 와 조합

  🎯 STEP 4: 결과물 1개 (시연)
       4.1 경쟁사 3개 도메인 신제품 비교표 자동 생성 (약 1분)

사전 점검 3가지부터:
  □ Node.js 18 이상
  □ Chrome 또는 Safari (firecrawl.dev 가입용)
  □ 분석할 경쟁사 도메인 3곳 후보

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | 경쟁사 사이트·기사·랜딩 페이지를 마크다운/JSON 으로 자동 수집하는 도구 |
| 제공사 | Mendable AI (공식 · `firecrawl-mcp`) |
| 라이선스 | MIT |
| 인증 방식 | API key (`FIRECRAWL_API_KEY`) |
| 연결 방식 | Cloud API (헤드리스 브라우저 클라우드 실행) |
| 도구 prefix | `mcp__firecrawl__*` (총 4개) |
| 무료 한도 | 500크레딧/월 (하루 약 30~50건 처리) |
| Before | 사이트 5곳 클릭·복사·정리 · 1h 45m/일 |
| After | 한 줄 명령 · 1m 20s |

### 1.2 마케터 관점 활용 가능성

- **경쟁사 신제품 모니터링** · 도메인 3~5곳 가격·용량·USP 비교표 자동 생성
- **시장 트렌드 기사 수집** · 키워드 검색 → 기사 10개 본문 추출 → 트렌드 3개 요약
- **광고 랜딩 페이지 분석** · 경쟁 광고 헤드라인·CTA·USP 추출
- **도메인 사이트맵 크롤** · 경쟁사 전 페이지 구조 파악
- **정기 모니터링** · `competitor-monitor` 에이전트 매일 09시 자동 실행
- **구조화 JSON + 시트 적재** · Google Sheets MCP 와 조합한 주간 비교표 자동 갱신

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| 경쟁사 사이트 5곳 방문 | 30분 | 30초 (자동 scrape) |
| 가격·용량 복사 | 15분 | 즉시 (마크다운 자동 정리) |
| 기사 10개 클릭·읽기 | 45분 | 30초 (자동 search) |
| 표 정리 + 슬랙 공유 | 15분 | 20초 (클로드 자동 표 + Discord 전송) |
| **하루 분량** | **1h 45m** | **1m 20s** |
| **연간 환산 (250일)** | **약 730시간** | **약 5시간** |

연간 약 730시간 절감 + 누락 0건 (사람이 매일 5곳 빠짐없이 확인은 사실상 불가).

### 1.4 대안 4종 간단 비교

본 강의는 Firecrawl 을 기본 채택했으나, 상황별 대안을 알아둘 가치가 있음:

| 대안 | 강점 | 약점 | 권장 상황 |
|---|---|---|---|
| **Apify** | 4,000+ 사전 액터 (인스타·틱톡·구글맵 전용) · 공식 MCP | 가격↑, 학습 비용↑ | 대량·특수 플랫폼이면 |
| **Bright Data** | 엔터프라이즈 안티봇 + 글로벌 프록시 · 공식 MCP | 가격 가장 높음 | 차단 강한 사이트면 |
| **Tavily** | AI 친화 검색 API · 무료 1,000건/월 | 검색 중심 (스크레이프 ✕) | 검색이 중심이면 (Firecrawl 과 보완 관계) |
| **Jina Reader** | 완전 무료 · 가입 불필요 (r.jina.ai/&lt;URL&gt;) | MCP 없음, 단순 변환만 | 임시·소량이면 (Claude WebFetch 와 조합) |

**Firecrawl 채택 이유 3가지**:
1. MCP 통합 가장 매끄럽고 마크다운 출력 품질 최고
2. 무료 500크레딧으로 강의 실습 충분
3. scrape, crawl, search, extract 4 도구가 한 패키지에 (학습 부담 최소)

### 1.5 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 대안 MCP (Apify·Tavily 등) 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 4단계

### 2.1 STEP 1 / 4 · API key 발급 (사용자 직접 · 2분) ★ 가장 중요

사용자에게 안내:

```
브라우저에서 다음 절차를 진행하세요:

① https://www.firecrawl.dev 접속
② 우상단 "Sign Up" 클릭 → Google 계정 또는 GitHub 계정 로그인
③ 가입 완료 후 좌측 메뉴 "API Keys" 클릭
④ "Create New Key" 클릭
⑤ Key 이름 입력 (예: "marketing-os-key")
⑥ 생성된 키 복사 ⚠️ 화면을 닫으면 다시 표시 안 됨
   토큰 형식: fc-xxxxxxxxxxxxxxxxxxxxxxx (영문+숫자, 'fc-' 접두)
```

복사한 key 를 클로드에게 전달.

⚠️ **가장 자주 발생하는 실수**: key 가 한 번만 표시되는 것을 모르고 탭을 닫음. 닫혔다면 Create New Key 로 새로 발급.

확인 사항:
- [ ] 무료 플랜 활성화 (500크레딧/월)
- [ ] Dashboard 의 "Usage" 탭에서 잔량 확인 가능
- [ ] Billing 정보 입력 불필요 (무료 플랜)

### 2.2 STEP 2 / 4 · .env 등록 (클로드 자동 · 30초)

클로드 자동 실행:

```bash
cd "${CLAUDE_PROJECT_DIR}"

# .env 에 추가
if ! grep -q "FIRECRAWL_API_KEY" .env 2>/dev/null; then
  echo "FIRECRAWL_API_KEY=발급받은_API_키" >> .env
fi

# .gitignore 에 .env 등록 여부 확인 (안전 점검)
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
  echo ".env" >> .gitignore
fi

# 검증
grep FIRECRAWL_ .env
```

### 2.3 STEP 3 / 4 · .mcp.json 등록 (클로드 자동 · 30초)

`marketing-os/.mcp.json` 의 `mcpServers` 에 추가:

```json
"firecrawl": {
  "_part": "2 Ch 1-4 경쟁사·시장 정보 자동 수집",
  "command": "npx",
  "args": ["-y", "firecrawl-mcp"],
  "env": {
    "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
  }
}
```

JSON 검증:

```bash
python3 -c "import json; json.load(open('.mcp.json'))"
```

### 2.4 STEP 4 / 4 · 헬스 체크 (클로드 자동 · 1분)

사용자에게 안내:

```
클로드 코드를 완전 종료 (메뉴 > 종료 또는 ⌘Q) 후 재시작하세요.

새 세션에서 다음 명령으로 검증:
"https://example.com 페이지를 마크다운으로 가져와줘"
```

내부적으로 `mcp__firecrawl__firecrawl_scrape` 호출됨.

성공 응답:

```
✅ Firecrawl 연결 확인. example.com 마크다운 응답 수신:

# Example Domain

This domain is for use in illustrative examples in documents...
(이하 본문)

크레딧 사용: 1
잔량: 499 / 500
도구 prefix: mcp__firecrawl__* (4개)
```

### 2.5 보안 점검

설치 직후 확인:
- [ ] `.env` 가 `.gitignore` 에 등록됨
- [ ] `.mcp.json` 의 값은 `${VAR}` 참조 (API key 평문 직접 입력 금지)
- [ ] API key 가 git log 에 노출된 적 없는지 (노출 시 Dashboard 에서 즉시 Revoke + 재발급)
- [ ] firecrawl.dev 계정에 2단계 인증 권장 (Account Settings)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 4개

| 도구 | 기능 | 크레딧 |
|---|---|---|
| `firecrawl_scrape` ★ | 단일 URL → 마크다운/HTML/JSON (가장 자주) | 1/URL |
| `firecrawl_crawl` | 도메인 전체 sitemap 기반 순회 | 1/page |
| `firecrawl_search` | 키워드 검색 + 상위 결과 페이지 크롤 | 1/result |
| `firecrawl_extract` | 스키마 지정 구조화 JSON 추출 | 1~5/URL |

### 3.2 마케터가 자주 쓰는 6 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 경쟁사 신제품 비교 ★ | "경쟁사 3곳 신제품 가격·용량·USP 표로" | 1분 |
| B. 시장 트렌드 기사 수집 ★ | "K뷰티 D2C 최신 기사 10개 → 트렌드 3개로 요약" | 2분 |
| C. 광고 랜딩 페이지 카피 분석 | "경쟁 광고 페이지 헤드라인·CTA·USP 추출" | 30초 |
| D. 도메인 사이트맵 크롤 | "경쟁사 도메인 전 페이지 제목·URL 목록" | 3~5분 |
| E. 정기 변경 모니터링 ★ | (자동 트리거) 매일 09시 어제 대비 변경분 알림 | 자동 |
| F. 구조화 추출 + 시트 적재 | "JSON 추출 후 Google Sheets 행 추가" | 2분 |

### 3.3 다른 MCP 와 조합 시나리오

- **+ Discord MCP** · 경쟁사 변경분 발견 시 #marketing 채널 자동 알림
- **+ Google Sheets MCP** · 추출 JSON 을 시트 행으로 적재, 주간 비교표 자동 갱신
- **+ Notion MCP** · 시장 트렌드 요약을 노션 페이지로 장기 보관
- **+ Meta·Google Ads MCP** · 경쟁사 광고 카피와 본인 광고 카피 비교
- **+ Buffer MCP** · 시장 트렌드 → 콘텐츠 캘린더 자동 제안

본 MCP 는 **30개 에이전트 중 약 1/3 (리서치·콘텐츠·전략 계열) 이 호출** · 본 강의 Part 4 의 핵심 자산.

---

## 🎯 STEP 4: 결과물 1개 · 경쟁사 3개 신제품 비교표 자동 생성

본 STEP 의 핵심은 **한 줄 명령으로 표가 완성되는 경험** 을 제공하는 것. 사이트 직접 방문 0번, 복사 0번을 체감.

### 4.1 시연 · 경쟁사 3개 도메인 신제품 비교 (약 1분)

**사전 조건**: 헬스 체크 통과 + 크레딧 잔량 100 이상.

```
사용자: 클로드에 다음 명령 입력:

  경쟁사 3곳의 메인 신제품 1개씩을 가져와서
  가격, 용량, 핵심 USP 3가지를 표로 만들어줘.

  도메인:
    - https://medicube.co.kr
    - https://torriden.com
    - https://numbuzin.com
```

자동 실행:

```
1. 클로드: 명령 해석 후 Firecrawl MCP 호출 판단

2. mcp__firecrawl__firecrawl_scrape 3회 호출:
   - URL: medicube.co.kr (formats: ["markdown"])
   - URL: torriden.com (formats: ["markdown"])
   - URL: numbuzin.com (formats: ["markdown"])
   - 각 사이트 본문 마크다운 자동 수신

3. 클로드: 마크다운에서 필드 추출
   - 신제품 이름 (제목 패턴)
   - 가격 (₩ 또는 원 단위)
   - 용량 (ml, 매, g 단위)
   - USP 3가지 (목록 또는 강조 문구)

4. 마크다운 표 형식으로 출력:

   | 브랜드 | 신제품 | 가격 | 용량 | USP 3가지 |
   |---|---|---|---|---|
   | Medicube | 콜라겐 마스크 | 36,000원 | 30매 | 저자극, 야간 보습, 즉시 진정 |
   | Torriden | 다이브인 세럼 | 22,000원 | 50ml | 5D 히알루론, 산뜻함, 톤업 |
   | Numbuzin | No.5 에센스 | 28,000원 | 100ml | 비건, 발효 콜라겐, 탄력 |

5. 결과 표 출력 + 크레딧 사용량 표시:
   ✅ 비교표 생성 완료
   - Firecrawl 호출: 3건 (크레딧 3 사용)
   - 잔량: 497 / 500
   - 총 소요: 약 1분
   - 사람 손 비교: 약 20분 (20배 단축)
```

성공 기준:
- [ ] Firecrawl 호출 3건 성공 (도메인별)
- [ ] 마크다운에서 가격·용량·USP 추출 정확
- [ ] 표 형식 정상 출력
- [ ] 크레딧 잔량 표시 정확

### 4.2 확장 제안

```
🎉 Firecrawl MCP 설치 + 경쟁사 비교표 1건 완성. 다음 가능합니다:

  A. 다른 MCP 와 조합 시도:
     - "+ Discord" · 비교표를 #marketing 채널 자동 발송
     - "+ Google Sheets" · 비교 결과를 시트 행으로 적재
     - "+ Notion" · 시장 트렌드 요약을 노션 페이지로 보관

  B. 다른 시나리오 시도:
     - "시장 기사 10개 → 트렌드 3개로" (firecrawl_search)
     - "경쟁사 광고 랜딩 페이지 카피 분석" (firecrawl_scrape)
     - "도메인 전체 사이트맵 크롤" (firecrawl_crawl)

  C. Part 4 정기 자동화 (다음 학습 단계):
     - competitor-monitor · 매일 09시 자동 비교 + 변경분 알림
     - market-trend-watcher · 매주 월요일 트렌드 기사 자동 요약
     - landing-page-decoder · 광고 클릭 시 자동 카피 추출

  D. Part 2 다음 MCP:
     - 1-5 Figma MCP · 시장 트렌드 → 디자인 자산 연결
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 1-4 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

Firecrawl API 키 발급 → `.env` 설정 → `.mcp.json` 등록 → 본인 경쟁사 사이트 1개를 마크다운으로 추출.

### 실습 헬스 체크 명령

```bash
claude
> /mcp   # firecrawl ✅
> "https://example.com 페이지를 마크다운으로 가져와줘"
# → 페이지 본문이 마크다운으로 응답
```

### 마케터 5패턴 · 경쟁사 분석

```
[역할] 너는 K-뷰티 D2C 카테고리 분석가야.

[입력] 경쟁사 도메인 3개:
  - https://medicube.co.kr
  - https://torriden.com
  - https://numbuzin.com

[산출물] 각 도메인의 (1) 메인 신제품 1개 (2) 가격 (3) 핵심 USP 3가지를 표로.

[제약] 마크다운 표 형식. 한국어. 가격은 원화 정수.

[검증] 추출 실패한 도메인이 있으면 사유 표시.
```

### 응용 과제

- 경쟁사 블로그를 매주 모니터링하는 워크플로 설계 (Part 4 에서 자동화)

---

## 트러블슈팅 (Firecrawl MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `Invalid API key` | Key 오타·만료·Revoke 됨 | Dashboard > API Keys > Create New Key 재발급 |
| `Rate limit exceeded` | 무료 플랜 분당 호출 제한 | 60초 대기 또는 유료 플랜 검토. 자동 재시도는 클로드에 위임 |
| `Insufficient credits` | 월 500크레딧 소진 | 다음 달 갱신 대기 또는 유료 플랜 |
| 페이지가 비어 있음 | JS 렌더 필요 | "waitFor 3000ms 옵션으로 다시 가져와줘" 명시 |
| `403 Forbidden` | 사이트가 봇 차단 | "mobile: true 옵션으로 재시도" 또는 Bright Data 대안 검토 |
| 한국어 깨짐 | 인코딩 자동 감지 실패 | "formats=['markdown'] 명시" |
| `mcp__firecrawl__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `claude mcp list` 등록 확인 + 클로드 코드 완전 종료 후 재시작 |
| 응답이 너무 길어 잘림 | 페이지 분량 과다 | `maxLength` 또는 `extract` 로 필요 필드만 추출 |
| 무한 크롤 | `firecrawl_crawl` 의 limit 미지정 | "최대 20페이지로 제한" 명시 |
| `Domain blacklisted` | 일부 사이트는 정책상 차단 | Apify 또는 Bright Data 대안 검토 |

## 강의 연결

- 본 스킬은 [클립 1-4 Firecrawl MCP 대본](../대본/1-4-firecrawl.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Firecrawl 의 API key 패턴에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 **30개 에이전트 중 약 1/3 (리서치·콘텐츠·전략 계열) 이 자동 호출** · 본 강의 Part 4 의 핵심 자산.
- 주요 활용 에이전트:
  - Part 4 · `competitor-monitor` · 매일 경쟁사 변경 자동 모니터링
  - Part 4 · `market-trend-watcher` · 주간 시장 기사 트렌드 요약
  - Part 4 · `landing-page-decoder` · 광고 랜딩 페이지 카피 추출
  - Part 5 · `content-ideation` · 시장 트렌드 → 콘텐츠 주제 제안
  - Part 9 · `strategy-brief` · 분기별 전략 브리프에 경쟁사 데이터 포함
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/03-firecrawl/mcp설치-firecrawl/`) · 클립과 함께 자체 보관.

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| MCP 패키지 | `firecrawl-mcp` (npx · Mendable AI 공식) |
| GitHub 저장소 | <https://github.com/mendableai/firecrawl-mcp-server> |
| Firecrawl Dashboard | <https://www.firecrawl.dev> |
| API key 형식 | `fc-` + 영문+숫자 약 32자 |
| 무료 플랜 | 500크레딧/월 (하루 약 30~50건) |
| 분당 호출 제한 | 무료 10회/분 (Pro 100회/분) |
| 노출 도구 | 4개 (`firecrawl_scrape`, `firecrawl_crawl`, `firecrawl_search`, `firecrawl_extract`) |
| 출력 포맷 | `markdown`, `html`, `rawHtml`, `screenshot`, `links`, `json` |
| 권장 옵션 | `waitFor: 3000` (JS 렌더), `mobile: true` (차단 우회), `onlyMainContent: true` (광고 제외) |

## 대안 MCP 빠른 참조

본 강의 채택은 Firecrawl 이나, 사용자가 특정 상황에 부닥치면 다음 대안 검토:

| 상황 | 권장 대안 | 설치 비용 |
|---|---|---|
| 인스타·틱톡·구글맵 전용 스크레이프 | Apify MCP (`apify/actors-mcp-server`) | API key + 사전 액터 학습 |
| 차단 강한 사이트 (정부·금융) | Bright Data MCP (`brightdata/brightdata-mcp`) | API key + 유료 플랜 |
| 검색 기반 리서치 중심 | Tavily MCP (`tavily-ai/tavily-mcp`) | 무료 1,000건/월 |
| 임시 1회 변환 (가입 부담) | Jina Reader (r.jina.ai) | 가입·key 불필요, WebFetch 와 조합 |

대안 도입 요청 시: 사용자 상황 확인 후 `mcp설치` 마스터 스킬에 위 패키지명 전달, 동일 4단계로 자동 진행.

## 메모리·문서 연결

- 사용자의 자주 쓰는 경쟁사 도메인 3~5곳은 메모리로 저장 (정기 모니터링 시 반복 호출)
- 본 스킬 종료 후 사용자가 "매일 자동으로 돌리고 싶다" 라고 하면 Part 4 의 `competitor-monitor` 에이전트로 전달
- 카테고리·언어 차단 등 특수 요구가 발생하면 위 "대안 MCP 빠른 참조" 표에서 매핑 후 마스터 스킬로 전달
- 무료 크레딧 70% 도달 시 사용자에게 사전 알림 (다음 달 갱신 시점 + 유료 플랜 비용 안내)
