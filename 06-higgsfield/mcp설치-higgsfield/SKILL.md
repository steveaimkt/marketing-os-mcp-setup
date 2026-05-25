---
name: mcp설치-higgsfield
description: |
  Part 2 클립 2-3 (Higgsfield MCP) 전용 설치 스킬. HTTP MCP 등록 (`https://mcp.higgsfield.ai/mcp`) + OAuth 자동 인증 + 헬스 체크를 5~7분 안에 완료하고 광고 이미지 1장 + 5초 인트로 영상 1개 + 바이럴 점수 1건을 시연. 마케터(비개발자) 기준 4단계 표준 흐름.

  자동 호출 트리거:
  - **"Higgsfield MCP 설치하자"** ⭐ 주요 트리거
  - "힉스필드 MCP 설치"
  - "광고 이미지 생성 도구 설치"
  - "이미지 영상 생성 MCP"
  - "Part 2 / 2-3 설치 시작"

  4단계:
  ① 소개 (한 줄 정의·Before/After) →
  ② 설치 (가입 + .mcp.json 등록 + OAuth 인증 + 헬스 체크) →
  ③ 작업 가능 업무 (도구 18개 + 7 시나리오) →
  ④ 결과물 2개 (광고 이미지 1장 + 5초 인트로 영상 + 바이럴 점수)

  특이점: HTTP MCP 방식 (npm 패키지 설치 없음). OAuth 자동 (API key 없음 · .env 없음). 가장 빠른 MCP 설치 패턴. 광고 비주얼 외주 1일 + 30~50만원 → 1~3분 + 무료 크레딧.
---

# Part 2 / 2-3 Higgsfield MCP 설치 (클립 전용)

> 본 스킬은 Higgsfield MCP 를 HTTP MCP + OAuth 방식으로 설치하고 광고 이미지 + 5초 인트로 영상 + 바이럴 점수 워크플로를 시연하는 흐름. 마스터 스킬 `mcp설치` 의 4단계 표준을 Higgsfield 의 HTTP + OAuth 패턴에 적용한 클립 전용 버전.

## 🎬 스킬 시작 시 메시지

본 스킬이 호출되면 Claude 는 반드시 다음과 같이 시작 멘트를 출력:

```
🖼️ Higgsfield MCP 설치를 시작합니다.

먼저 짚고 갈 게 한 가지 있어요:

  Higgsfield MCP 는 'Claude 가 광고 비주얼·영상을 자연어로 생성하는 채널' 입니다.
  Adobe·Blender·외주 없이 광고 이미지 1장 30초~1분 · 5초 영상 1~3분.
  코드 작성 안 합니다. "쿠팡 봄 캠페인 1080×1080 핑크 톤" 같은 자연어 명령만으로 작동해요.

────────────────────────────────

총 4단계로 진행돼요 (5~7분 예상):

  📖 STEP 1: MCP 소개 (2분)
       1.1 HTTP MCP + OAuth 자동 흐름
       1.2 도구 18개 (생성 2 + 작업 4 + 미디어 3 + 워크스페이스 4 + 기타 5)
       1.3 Before vs After 비교 (1일 → 10분 · 150배)

  ⚙️ STEP 2: MCP 설치 (5~7분)
       2.1 Higgsfield 가입 (사용자 2분 · 없을 때만)
       2.2 .mcp.json 등록 (자동 2분)
       2.3 OAuth 인증 (사용자 2분 · 클릭 1번)
       2.4 헬스 체크 (자동 1분)

  📋 STEP 3: 작업 가능 업무 (2분)
       3.1 도구 18개 (generate_image · generate_video · virality_predictor 핵심 3)
       3.2 7 시나리오 (이미지·영상·바이럴·캐릭터·B-roll·캐러셀·템플릿)
       3.3 모델 선택 (Flux Pro · Schnell · SDXL · 영상)

  🎯 STEP 4: 결과물 2개 (화장품 캠페인 시나리오)
       4.1 화장품 연출컷 1장 1080×1080 (약 1분)
       4.2 인플루언서 제품 사용 숏폼 5초 9:16 + 바이럴 점수 (약 3분)

사전 점검 4가지부터:
  □ Node.js 18 이상
  □ Higgsfield 무료 계정
  □ 본인 워크스페이스 1개 (가입 시 자동 생성)
  □ Chrome 또는 Safari (OAuth 인증용)

전체 진행할까요? (y/n)
```

사용자가 OK 하면 STEP 1 로 진행. 거부 시 본 스킬 종료.

---

## 📖 STEP 1: MCP 소개

### 1.1 표준 카드 출력

| 항목 | 값 |
|---|---|
| 한 줄 정의 | 자연어 한 줄로 광고 이미지·영상·B-roll·인트로 생성하는 도구 |
| 제공사 | Higgsfield (공식 HTTP MCP 서버) |
| 라이선스 | Higgsfield 서비스 약관 (상업적 사용 가능) |
| 인증 방식 | OAuth (첫 호출 시 브라우저 자동 · API key 불필요) |
| 연결 방식 | HTTP MCP (`https://mcp.higgsfield.ai/mcp`) |
| 도구 prefix | `mcp__higgsfield__*` (총 18개) |
| 무료 한도 | 가입 시 무료 크레딧 50 · Plus $9/월 · Pro 별도 |
| Before | 외주 의뢰 + 대기 + 수정 · 1~3일 · 30~50만원 |
| After | 자연어 명령 1줄 → 자동 생성 · 1~3분 · 무료 크레딧 |

### 1.2 마케터 관점 활용 가능성

- **캠페인 비주얼 자산 자동 생성** · 광고 이미지·5초 인트로·B-roll·캐러셀 5장 일괄
- **채널별 비율 자동 변형** · 1:1 (Instagram) · 9:16 (Stories) · 16:9 (Facebook·유튜브)
- **바이럴 사전 검증** · 영상 발행 전 점수 + 개선점 3 bullet
- **브랜드 캐릭터·아바타** · 페르소나 비주얼 일관성 유지
- **영상제작 트리오 결합** · Hyperframes + HeyGen + ElevenLabs (Part 2 / 2-4) 와 B-roll 담당
- **외주 의존 0건** · 디자이너 일정·외주비·수정 사이클 모두 제거

### 1.3 Before/After 비교 (수치)

| 작업 | Before | After |
|---|---|---|
| 디자이너 외주 의뢰 | 30분 | 0 (자연어 1줄) |
| 외주 대기 | 1~3일 | 0 |
| 첫 시안 검토 | 30분 | 즉시 (생성 결과 미리보기) |
| 수정 의뢰·재대기 | 하루 | 1분 (프롬프트 재호출) |
| 최종본 수령 | 10분 | 자동 (URL 반환) |
| **캠페인 1건 비주얼 5장** | **1일 + 며칠** | **약 10분** |
| **외주비** | **30~50만원** | **무료 크레딧 또는 $9/월** |

연간 환산 (주 1건 캠페인): 약 1,500~2,500만원 절감 + 외주 의존 0건.

### 1.4 사용자 동의 확인

```
이 MCP 가 본인 작업에 맞는지 확인됐어요?
- y: STEP 2 (설치) 진행
- n: 본 스킬 종료, 다른 MCP 검토
```

---

## ⚙️ STEP 2: MCP 설치 · 4단계

### 2.1 STEP 1 / 4 · Higgsfield 가입 (사용자 직접 · 2분 · 신규만)

사용자에게 묻기:

```
"Higgsfield 계정이 있나요? (y/n)"
- y: 본 단계 스킵
- n: 다음 안내
```

신규 가입자 안내:

```
브라우저에서 다음 절차를 진행하세요:

① higgsfield.ai 접속
② 우상단 "Sign up" 클릭
③ Google 또는 이메일 가입 (무료)
④ 약관 동의 후 가입 완료
⑤ 가입 즉시 무료 크레딧 50 자동 부여
⑥ 워크스페이스 자동 생성 (기본 이름 "My Workspace")
```

⚠️ 무료 크레딧 50 으로 이미지 약 30~50장 또는 영상 5~10개 가능.

### 2.2 STEP 2 / 4 · .mcp.json 등록 (Claude 자동 · 2분)

`marketing-os/.mcp.json` 의 `mcpServers` 에 추가:

```json
"higgsfield": {
  "_part": "2 Ch 2-3 이미지·영상 생성",
  "type": "http",
  "url": "https://mcp.higgsfield.ai/mcp"
}
```

⚠️ **`.env` 등록 불필요** · HTTP MCP 는 OAuth 토큰을 Claude.ai 가 자동 관리.
⚠️ **npm 패키지 설치 없음** · HTTP MCP 는 URL 직접 호출.

JSON 검증:

```bash
cd "${CLAUDE_PROJECT_DIR}"
python3 -c "import json; json.load(open('.mcp.json'))"
```

성공 시 에러 없이 종료.

### 2.3 STEP 3 / 4 · OAuth 인증 (사용자 직접 · 2분)

사용자에게 안내:

```
Claude Code 를 완전 종료 (메뉴 > 종료 또는 ⌘Q) 후 재시작하세요.

첫 호출 시 브라우저가 자동으로 열립니다:

① Higgsfield 로그인 페이지 자동 열림
② 본인 계정 선택 (이미 로그인 상태면 자동 진행)
③ Claude 가 접근할 권한 확인:
   - 이미지·영상 생성
   - 워크스페이스·미디어 조회
   - 잔여 크레딧·플랜 조회
④ "Allow" 또는 "허용" 클릭
⑤ "✅ Higgsfield connected" 표시 → 브라우저 닫기
```

⚠️ **팝업 차단 시**: 브라우저 자동 열림 실패 → 터미널에 표시된 URL 을 수동 복사 후 새 탭에서 열기.

⚠️ **재인증 필요 시**: OAuth 토큰 만료 시 같은 흐름 반복 (보통 30일~90일 주기).

### 2.4 STEP 4 / 4 · 헬스 체크 (자동 1분)

사용자에게 안내:

```
새 세션에서 다음 명령으로 검증:
"Higgsfield 워크스페이스 + 잔여 크레딧 보여줘"
```

내부적으로 `mcp__higgsfield__balance` + `list_workspaces` + `models_explore` 호출됨.

성공 응답:

```
✅ Higgsfield 연결 확인:
  - 워크스페이스: My Workspace (default)
  - 잔여 크레딧: 50 (가입 무료 · 이미지 5~10장 가능)
  - 현재 플랜: Free
  - 사용 가능 모델: Flux Pro, Flux Schnell, SDXL Lightning, ...

사용 가능 도구 18개: generate_image, generate_video, virality_predictor, ...
```

### 2.5 보안 점검

설치 직후 확인:
- [ ] `.mcp.json` 에 `higgsfield` 항목 정상 추가
- [ ] `.env` 에 Higgsfield 관련 키 없음 (OAuth 방식 · API key 불필요)
- [ ] OAuth 토큰은 Claude.ai 가 관리 (사용자 직접 보관 안 함)
- [ ] 워크스페이스 권한이 필요한 범위에만 부여 (Higgsfield 설정 페이지 확인)

---

## 📋 STEP 3: 작업 가능 업무

### 3.1 노출 도구 18개

| 도구 | 기능 |
|---|---|
| `generate_image` ★ | 텍스트 → 이미지 생성 (Flux·SDXL 등) |
| `generate_video` ★ | 텍스트 → 5~10초 영상 |
| `virality_predictor` ★ | 영상 바이럴 점수·개선점 예측 |
| `models_explore` | 사용 가능 모델 카탈로그 |
| `show_marketing_studio` | 마케팅 템플릿 50+ 카탈로그 |
| `show_characters` | 본인 캐릭터·아바타 라이브러리 |
| `balance` | 잔여 크레딧 조회 |
| `job_display` | 생성 작업 상세 정보 |
| `job_status` | 비동기 작업 폴링 (pending → processing → completed) |
| `list_workspaces` | 워크스페이스 목록 |
| `select_workspace` | 워크스페이스 선택 |
| `show_generations` | 생성 이력 조회 |
| `show_medias` | 본인 미디어 라이브러리 |
| `media_upload` | 로컬 파일 업로드 (영상 분석용) |
| `media_confirm` | 업로드 완료 확인 |
| `sync_agents` | 에이전트 동기화 |
| `transactions` | 크레딧 사용 이력 |
| `show_plans_and_credits` | 플랜·크레딧 카탈로그 |

### 3.2 마케터가 자주 쓰는 7 시나리오

| 시나리오 | 자연어 명령 | 소요 |
|---|---|---|
| A. 광고 이미지 ★ | "쿠팡 봄 1080×1080 핑크 톤" | 30초~1분 |
| B. 5초 인트로 영상 ★ | "브랜드 인트로 5초 미니멀 모션" | 1~3분 |
| C. 캐러셀 5장 일괄 | "Instagram 캐러셀 5장 신학기" | 3~5분 |
| D. B-roll 클립 | "신상품 회전 B-roll 5초" | 1~3분 |
| E. 바이럴 점수 예측 ★ | "이 영상 바이럴 점수와 개선점" | 30초 |
| F. 캐릭터·아바타 | "본 브랜드 페르소나 캐릭터" | 2분 |
| G. 마케팅 템플릿 | "캠페인 템플릿 50종 카탈로그" | 10초 |

### 3.3 모델 선택 가이드

| 모델 | 용도 | 특징 |
|---|---|---|
| Flux Pro | 사실적 사진·광고 비주얼 | 고품질·약간 느림·크레딧 2 |
| Flux Schnell | 빠른 시안 | 빠름·크레딧 1 |
| SDXL Lightning | 일러스트·아트워크 | 스타일라이즈드·크레딧 1~2 |
| 영상 모델 (자동) | 5~10초 영상 | 크레딧 5~10 |

`models_explore` 호출로 사용 가능 모델 카탈로그 + 모델별 지원 비율·해상도 확인.

### 3.4 다른 MCP 와 조합 시나리오

- **+ Notion MCP** · 캠페인 컨셉 가이드 페이지 → Higgsfield 자동 생성 → 같은 페이지에 결과 첨부
- **+ Buffer MCP** · Higgsfield 비주얼 5장 → Buffer 5채널 예약 발행
- **+ Discord MCP** · Higgsfield 생성 완료 → 디스코드 자동 알림 + embed
- **+ Hyperframes/HeyGen MCP** · Higgsfield 가 B-roll 담당 + Hyperframes 가 본 영상 (Part 2 / 2-4)
- **+ Meta·Google Ads MCP** · Higgsfield 비주얼 → 광고 캠페인 자동 등록 (Part 6)

본 MCP 는 **마케팅 OS 의 비주얼 생성 엔진** · Part 5 콘텐츠·카피 에이전트 + Part 6 광고 에이전트가 결합.

---

## 🎯 STEP 4: 결과물 2개 · 화장품 캠페인 시나리오

본 STEP 의 핵심은 **화장품 브랜드의 정적 자산 (연출컷) + 동적 자산 (인플루언서 숏폼) 을 동일 톤으로 한 번에 완성**됨을 보여주는 것. 스튜디오 촬영 + 인플루언서 의뢰 며칠 + 80~250만원이 4분 + 무료 크레딧으로 해결.

### 4.1 시연 A · 화장품 연출컷 1장 생성 (약 1분)

**사전 조건**: STEP 2 헬스 체크 통과 + 잔여 크레딧 2 이상.

사용자 명령:

```
화장품 신제품 연출컷 만들어줘.

스펙:
- 제품: 글로우 세럼 30ml 앰버 유리 보틀 (골드 캡)
- 크기: 1080×1080 (Instagram 정사각형)
- 톤: 베이지·아이보리 그라데이션 + 따뜻한 자연광
- 연출: 대리석 트레이 위 제품 1개 + 마른 꽃잎 2~3장 + 실크 천 일부
- 카메라: 위에서 약간 비스듬한 45° 앵글 · 얕은 심도
- 스타일: 럭셔리 뷰티 매거진 표지 · 사실적 사진 (Flux Pro 모델)
- 텍스트 없음 (캡션 자리만 비워둠)

생성 후 결과 이미지 URL 과 다운로드 안내.
```

자동 실행:

```
1. mcp__higgsfield__models_explore 호출
   - "Flux Pro" 모델 선택 (사실적·럭셔리 뷰티)

2. mcp__higgsfield__generate_image 호출
   - prompt: 한글 → 영문 자동 번역 (Claude 가 변환)
   - aspect_ratio: 1:1
   - model: flux-pro
   - style: photorealistic, luxury beauty editorial
   - 크레딧 차감: 1~2

3. mcp__higgsfield__job_status 폴링 (10~30초)
   - 상태: pending → processing → completed

4. 결과:
   ✅ 이미지 생성 완료
   - URL: https://higgsfield.ai/media/xxx.jpg
   - 다운로드: 우클릭 > 이미지 저장
   - 크레딧 잔액: 48 (-2)
```

성공 기준:
- [ ] Flux Pro 모델 자동 선택
- [ ] 한글 프롬프트 → 영문 자동 번역 성공
- [ ] 1080×1080 화장품 연출컷 정상 생성 (앰버 보틀·골드 캡 인식)
- [ ] 베이지·아이보리 톤 + 자연광 반영
- [ ] 크레딧 정상 차감 (1~2)
- [ ] 결과 URL 접근 가능

### 4.2 시연 B · 인플루언서 제품 사용 숏폼 + 바이럴 점수 (약 3분)

**사전 조건**: STEP 2 헬스 체크 통과 + 잔여 크레딧 10 이상 + 시연 A 연출컷 톤 기억 (동일 톤 유지용).

사용자 명령:

```
인플루언서가 화장품 사용하는 숏폼 영상 5초 만들어줘.

스펙:
- 제품: 글로우 세럼 (시연 A 연출컷 동일 제품)
- 길이: 5초
- 비율: 9:16 (Instagram Reels · TikTok · Shorts)
- 장면: 20대 후반 여성 인플루언서가 거울 앞에서 세럼 펌프 누르고
        손등에 1~2 방울 떨어뜨린 후 얼굴에 가볍게 발라 흡수시키는 모습
- 톤: 따뜻한 자연광 · 베이지·아이보리 배경 (연출컷과 동일 톤)
- 카메라: 가까운 클로즈업 + 부드러운 핸드헬드
- 스타일: 자연스러운 데일리 브이로그 · 광고가 아닌 듯한 느낌
- 모델: 영상 모델 (자동 선택)

생성 후 영상 URL + 다운로드 안내.
바이럴 점수 예측도 함께.
```

자동 실행:

```
1. mcp__higgsfield__generate_video 호출
   - prompt: 한글 → 영문 자동 번역
   - duration: 5s
   - aspect_ratio: 9:16
   - 크레딧 차감: 5~10

2. mcp__higgsfield__job_status 폴링 (1~3분)
   - 영상은 이미지보다 오래 걸림 (큐 적체 시 5~10분)

3. mcp__higgsfield__virality_predictor 호출
   - 생성된 영상의 바이럴 점수 예측
   - 결과: 점수 (0~100) + 개선점 3 bullet

4. 결과:
   ✅ 영상 생성 완료
   - URL: https://higgsfield.ai/media/xxx.mp4
   - 길이 5초 · 9:16 · 1080p (숏폼 최적)
   - 바이럴 점수: 74/100
   - 개선점: 첫 1초 손동작 클로즈업 ↑, 제품 라벨 노출 시간 ↑, 마지막 표정 컷 추가
   - 크레딧 잔액: 38 (-10)
```

성공 기준:
- [ ] 영상 모델 자동 선택
- [ ] 5초 영상 정상 생성 (9:16 숏폼 · 1080p)
- [ ] 인플루언서 동작 시퀀스 자연스럽게 표현 (펌프 → 손등 → 얼굴)
- [ ] 시연 A 연출컷과 동일 톤 유지 (베이지·아이보리·자연광)
- [ ] 바이럴 점수 출력 (0~100 범위)
- [ ] 개선점 최소 3개 bullet 출력
- [ ] 크레딧 정상 차감 (5~10)
- [ ] 결과 URL 재생 가능

### 4.3 다음 단계 제안

```
🎉 Higgsfield MCP 설치 + 화장품 연출컷 + 인플루언서 숏폼 + 바이럴 점수 완성. 다음 가능합니다:

  A. 더 많은 시나리오 시도:
     - "캐러셀 5장 (연출컷·사용컷·텍스처·결과·인플루언서)" · C 시나리오
     - "제품 회전 클로즈업 B-roll 5초" · D 시나리오
     - "본 브랜드 페르소나 캐릭터" · F 시나리오
     - "뷰티 캠페인 템플릿 50종 카탈로그" · G 시나리오

  B. 정기 자동화 (Part 5 · 6 · 10):
     - mkt-content-visual · 콘텐츠 캘린더 따라 매주 비주얼 자동 생성
     - mkt-ad-creative · 광고 캠페인 등록 시 비주얼 자동 첨부
     - mkt-viral-check · 영상 발행 전 바이럴 점수 자동 검증

  C. 다른 MCP 와 조합:
     - + Notion · 캠페인 가이드 → 자동 생성 → 같은 페이지 첨부
     - + Buffer · 5채널 예약 발행과 결합
     - + Discord · 생성 완료 자동 알림
     - + 영상제작 트리오 (Part 2 / 2-4) · B-roll 담당

  D. Part 2 의 다음 클립:
     - 2-4 영상제작 트리오 (Hyperframes + HeyGen + ElevenLabs) · Higgsfield 와 결합
```

---

## 📝 강의 실습 (실습.md 통합)

> 클립 2-3 실습.md 와 본 스킬을 함께 운영. 본 섹션은 강의 진행 시 시연용 명령·5패턴·응용 과제.

### 실습 한 줄 요약

`/mcp설치-higgsfield` 스킬을 호출해 HTTP MCP + OAuth 인증을 5~7분 안에 완료하고, 광고 비주얼 1장 + 5초 인트로 영상 1개를 자동 생성.

### 실습 첫 결과물 명령 · 화장품 연출컷 1장

```
화장품 신제품 연출컷 만들어줘.

스펙:
- 제품: 글로우 세럼 30ml 앰버 유리 보틀 (골드 캡)
- 크기: 1080×1080 (Instagram 정사각형)
- 톤: 베이지·아이보리 그라데이션 + 따뜻한 자연광
- 연출: 대리석 트레이 위 제품 1개 + 마른 꽃잎 2~3장 + 실크 천 일부
- 카메라: 위에서 약간 비스듬한 45° 앵글 · 얕은 심도
- 스타일: 럭셔리 뷰티 매거진 표지 · 사실적 사진 (Flux Pro 모델)
- 텍스트 없음 (캡션 자리만 비워둠)

생성 후 결과 이미지 URL 과 다운로드 안내.
```

→ 약 30초~1분 (스튜디오 촬영 1일 + 30~50만원 → MCP 1분 · 무료).

### 실습 두 번째 결과물 명령 · 5초 숏폼 영상

```
인플루언서가 화장품 사용하는 숏폼 영상 5초 만들어줘.

스펙:
- 제품: 글로우 세럼 (위 연출컷 동일 제품)
- 길이: 5초
- 비율: 9:16 (Instagram Reels · TikTok · Shorts)
- 장면: 20대 후반 여성 인플루언서가 거울 앞에서 세럼 펌프 누르고
        손등에 1~2 방울 떨어뜨린 후 얼굴에 가볍게 발라 흡수시키는 모습
- 톤: 따뜻한 자연광 · 베이지·아이보리 배경 (연출컷과 동일 톤)
- 카메라: 가까운 클로즈업 + 부드러운 핸드헬드
- 스타일: 자연스러운 데일리 브이로그 · 광고가 아닌 듯한 느낌

생성 후 영상 URL + 다운로드 안내.
바이럴 점수 예측도 함께.
```

→ 약 2~3분 (인플루언서 촬영 의뢰 며칠 + 50~200만원 → MCP 3분 · 무료 크레딧).

### 마케터 5패턴 · 정기 운영 결합

```
[역할]
1인 마케터의 광고 비주얼 자동 생성 어시스턴트

[입력]
- 캠페인 컨셉 (자연어 한 줄)
- 채널·비율 매트릭스 (Instagram 1:1, Stories 9:16, Facebook 16:9 등)
- 브랜드 가이드 (색상·톤·스타일)

[산출물]
캠페인 1건 = 비주얼 자산 5장 자동 생성:
  ① Instagram 1080×1080 메인 비주얼
  ② Stories 9:16 세로 버전
  ③ Facebook 16:9 가로 버전
  ④ 5초 인트로 영상 (16:9)
  ⑤ B-roll 5초 클립

[제약]
- 모든 비주얼 동일 브랜드 톤·색상
- 이미지: Flux Pro (사실적) 또는 SDXL (일러스트)
- 영상: 바이럴 점수 70+ 목표
- 크레딧 사용량 monitoring (영상 5~10, 이미지 1~2)

[검증]
- 생성된 비주얼 모두 다운로드 URL 반환
- 바이럴 점수 70+ 영상 비중
- 잔여 크레딧 확인 + 부족 시 알림
- Discord MCP 결합 시 → 생성 완료 자동 알림
```

### 응용 과제

1. 본인 화장품·뷰티 브랜드의 연출컷 1장 즉시 생성 → 다운로드
2. 인플루언서 제품 사용 숏폼 5초 + `virality_predictor` 점수 확인 → 점수 70+ 목표로 프롬프트 개선
3. Instagram 캐러셀 5장 일괄 생성 (연출컷·사용컷·텍스처·결과 비교·인플루언서) → 비주얼 일관성 검증
4. **Part 2 / 2-4 영상제작 트리오 (Hyperframes + HeyGen + ElevenLabs) 와 결합** · Higgsfield 가 B-roll 담당

---

## 트러블슈팅 (Higgsfield MCP 한정)

| 증상 | 원인 | 해결 |
|---|---|---|
| `OAuth 인증 실패` | 브라우저 팝업 차단 또는 세션 만료 | 팝업 허용 + Claude Code 재시작 + 수동 URL 복사·붙여넣기 |
| `Insufficient credits` | 무료 크레딧 소진 | `show_plans_and_credits` 잔액 확인 + Plus 플랜 ($9/월) 또는 Pro |
| `Generation failed` (이미지·영상) | 프롬프트 정책 위반 (성인·폭력·저작권) | 프롬프트 다듬기 또는 다른 모델 선택 |
| `job_status` 계속 pending | 큐 적체 | 1~3분 대기 (영상은 5~10분) · 새벽 시간대 재시도 |
| `mcp__higgsfield__*` 도구 안 보임 | `.mcp.json` 등록 누락 또는 재시작 안 함 | `claude mcp list` 확인 + Claude Code 완전 종료 후 재시작 |
| 한국어 결과 어색 | 모델 한국어 약함 | 영문 프롬프트로 재시도 또는 Claude 가 자동 번역 |
| 비율·해상도 미적용 | 모델별 지원 비율 다름 | `models_explore` 로 모델별 사양 확인 |
| 이미지 품질 낮음 | Schnell (빠른) 모델 사용됨 | Flux Pro 명시 (`model: flux-pro`) |
| 영상 결과 부자연스러움 | 5초 영상 모델 한계 | 프롬프트 단순화 (요소 3개 이하) · 모션 묘사 강화 |
| 다운로드 URL 만료 | URL 유효기간 경과 | `show_medias` 또는 `show_generations` 로 재조회 |
| 결과 한 번 더 받기 | 같은 프롬프트 결과 다양화 | 동일 명령 재호출 (모델은 매번 다른 결과) |

## 강의 연결

- 본 스킬은 [클립 2-3 Higgsfield MCP 대본](../대본/2-3-higgsfield.md) 의 슬라이드 06 "설치 실습" 시연에서 호출됩니다.
- 마스터 스킬 [skills/mcp설치/SKILL.md](../../../../skills/mcp설치/SKILL.md) 의 4단계 표준 흐름을 Higgsfield 의 HTTP MCP + OAuth 패턴에 적용한 클립 전용 버전.
- 본 스킬로 설치된 MCP 는 **광고 비주얼·영상 생성의 표준 채널** · Part 5·6 의 비주얼 자동화 에이전트가 호출.
- 주요 활용 에이전트:
  - Part 5 · `mkt-content-visual` · 콘텐츠 캘린더 → 매주 비주얼 자동 생성
  - Part 6 · `mkt-ad-creative` · 광고 캠페인 등록 시 비주얼 자동 첨부
  - Part 5 · `mkt-viral-check` · 영상 발행 전 바이럴 점수 자동 검증
  - Part 2 / 2-4 · 영상제작 트리오 결합 시 B-roll 담당
- 본 스킬은 클립 폴더 내부에 위치 (`curriculum/part02-MCP12개/06-higgsfield/mcp설치-higgsfield/`) · 클립과 함께 자체 보관.
- 참조 자산: 패캠 프로젝트 (2)
  - `marketing-agents/.mcp.json` (HTTP MCP 등록 예시)
  - `marketing-agents/agents/mkt-video-gen.md` (Higgsfield + 영상제작 결합)
  - `marketing-agents/agents/mkt-video-remotion.md` (B-roll 결합)

## 사전 검증된 설정값

| 항목 | 값 |
|---|---|
| Node.js 최소 버전 | 18 (`node --version`) |
| MCP 등록 방식 | HTTP MCP (URL 직접 등록 · npm 패키지 없음) |
| MCP 서버 URL | <https://mcp.higgsfield.ai/mcp> |
| 인증 방식 | OAuth (Claude.ai 자동 관리 · API key 없음) |
| 가입 무료 크레딧 | 50 (이미지 5~10장 또는 영상 1~2개 분량) |
| 이미지 크레딧 | 1~2 (모델별) |
| 영상 크레딧 | 5~10 (길이·모델별) |
| 바이럴 예측 크레딧 | 1 |
| Plus 플랜 | $9/월 (크레딧 200+) |
| Pro 플랜 | 별도 (대량 크레딧 + 고급 모델) |
| 노출 도구 | 18개 (`generate_image`, `generate_video`, `virality_predictor`, `models_explore`, ...) |
| 사용 가능 모델 | Flux Pro · Flux Schnell · SDXL Lightning · 영상 모델 (`models_explore` 확인) |
| 지원 이미지 비율 | 1:1, 9:16, 16:9, 4:5, 3:2 (모델별 상이) |
| 영상 길이 | 5초 또는 10초 (모델별) |
| OAuth 토큰 갱신 주기 | 30~90일 (만료 시 자동 재인증 안내) |

## 메모리·문서 연결

- 사용자의 워크스페이스 이름 + 선호 모델 (Flux Pro 등) 은 메모리로 저장 (자주 사용)
- 캠페인별 자주 쓰는 프롬프트 패턴도 메모리 저장 (재사용 효율)
- 본 스킬 종료 후 사용자가 "광고 비주얼 자동 생성하자" 라고 하면 Part 5 의 `mkt-content-visual` 또는 Part 10 의 `/agent-builder` 로 전달
- 영상제작 결합 요청 시 Part 2 / 2-4 영상제작 트리오 (Hyperframes + HeyGen + ElevenLabs) 안내
- 한글 프롬프트 결과 어색할 때 자동 영문 번역 흐름 안내
