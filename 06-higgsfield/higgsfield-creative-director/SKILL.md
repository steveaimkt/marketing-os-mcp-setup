---
name: higgsfield-creative-director
description: |
  Part 2 클립 2-6 (Higgsfield MCP) 실습 스킬. 사용자 한 줄 명령 → Claude 가 6 게이트로
  ① 사전 점검 → ② 컨셉·자료 → ③ 모델 이미지 → ④ 텍스트 점검 → ⑤ 영상 시나리오 → ⑥ 피드백 루프.
  자동 실행 금지. 각 게이트마다 사용자에게 명시적으로 물은 뒤 답 받고 다음 단계.
  실전 학습 반영: Plus 플랜 제약·라벨 텍스트 모델 분기·start_image 체이닝·라이트 효과 NEGATIVE·프리셋 제안 거절·raw_data 폴링.

  자동 호출 트리거:
  - **"힉스필드 콘텐츠 만들자"** ⭐ 주요 트리거
  - **"힉스필드 시작하자"** / **"힉스필드 시작"**
  - "Higgsfield 이미지+영상"
  - "힉스필드 광고 만들자"
  - "제품 이미지·영상 같이 만들자"
  - "AI 광고 비주얼 만들자"
  - "포토 디렉터 시연"

  동작: 사용자 한 줄 → 6 게이트 인터랙티브 → 이미지 1~2장 + 5초 영상 1편 +
  (옵션) 바이럴 점수 → 결과 URL + 잔여 크레딧 + 다음 액션 5개.
---

# Part 2 / 2-6 · Higgsfield 콘텐츠 — 6 게이트 인터랙티브 흐름

> 사용자가 던진 한 줄을 그대로 힉스필드에 넘기지 않는다. Claude 가 먼저 디렉팅하고,
> **6개 게이트**마다 사용자 확인을 받는다. 자동으로 끝까지 실행 금지.
> **사전 기획·게이트 = 크레딧 절감의 핵심.** 잘못된 한 줄 → 재생성 → 크레딧 낭비를 막는다.

## 전제 조건

- Higgsfield MCP 연결됨 (`mcp__claude_ai_Higgsfield__*` 도구 노출)
- OAuth 인증 완료 (Higgsfield Allow)
- 잔여 크레딧 **30 이상 권장** (이미지 2장 + 영상 1편 = 약 12~15 크레딧)
- 플랜 제약 인지:
  - **Starter** : 대부분 모델 가능. `seedance_2_0` · `cinematic_studio_3_0` 등 일부 차단 → 폴백 필요
  - **Plus+** : 모든 모델 가능

## 진행 원칙 — 6 게이트 인터랙티브 ⛔

자동 실행 금지. 각 단계마다 사용자에게 **명시적으로 묻고 답을 받은 뒤**에만 다음 게이트로.

```
Step 0   사전 점검          → balance + workspaces 자동 호출, 잔여/플랜 표시           ⏸ 인사
게이트 1  컨셉 + 자료 수집    → 콘텐츠 유형 A~E + 제품 정보 (URL/이미지/텍스트)         ⏸ 답 대기
게이트 2  모델 이미지 기획    → 모델 컨셉 M1~M3 + 프로필 + 영문 프롬프트 검토            ⏸ 답 대기
게이트 3  텍스트 점검         → 라벨/텍스트 깨짐 확인 → 깨졌으면 nano_banana_pro 재시도  ⏸ 답 대기
게이트 4  영상 시나리오·견적   → 스토리보드 + 모델 폴백 + get_cost 견적                  ⏸ 답 대기
게이트 5  피드백 루프         → 만족 시 마무리, 아니면 변형/수정                         ⏸ 답 대기
Step 6   마무리              → 산출물 + 비용 + 다음 액션 5개 제안
```

---

## Step 0 · 사전 점검 + 안내 인사

스킬 호출 즉시 다음을 **순차 자동 실행**:

```python
mcp__claude_ai_Higgsfield__balance()
mcp__claude_ai_Higgsfield__list_workspaces()
```

결과를 다음 포맷으로 사용자에게 표시:

```
🎨 Higgsfield 콘텐츠 제작을 시작합니다.

본 흐름의 핵심 : "Claude 가 디렉팅, 힉스필드는 그대로 그린다"
사전 기획 + 6 게이트 → 한 번에 원하는 결과 → 크레딧 절약.

💰 현재 상태
  · 플랜          : {starter / plus / ultra}
  · 잔여 크레딧    : {N}
  · 워크스페이스   : {name} (selected)

📋 오늘 산출물 (총 6 게이트, 약 8~15분)
  ① 모델/제품 이미지 1~2 장   (약 2~4 크레딧)
  ② 5초 광고 영상 1 편       (약 10 크레딧, Starter 기준 kling2_6)
  → 총 약 12~15 크레딧

⚠️ Starter 플랜이면 seedance_2_0 · cinematic_studio_3_0 차단 → 자동 폴백.

👉 게이트 1 진행 : 어떤 콘텐츠 만들까요?
```

크레딧 부족 분기:
- 잔여 15 이하 → 이미지만 진행 권유
- 잔여 5 미만 → `mcp__claude_ai_Higgsfield__show_plans_and_credits` 호출

---

## 게이트 1 · 컨셉 + 자료 수집

다음 메뉴를 표시하고 **하나 골라달라** 묻기:

| # | 콘텐츠 유형 | 비율·길이 | 예상 크레딧 |
|---|---|---|---|
| **A** | 🛍 제품 광고 1편 (URL → 9:16 광고) | 9:16 · 5~8초 | ~12~15 |
| **B** | 📸 제품샷 멀티컷 (다른 앵글 4컷) | 1:1 · 5초 × 4 | ~40 |
| **C** | 🎥 무드컷 시네마틱 (텍스처·발색) | 9:16 · 5~8초 | ~10~20 |
| **D** | 👩 모델 화보 + UGC 영상 (오늘 실습 패턴) ⭐ | 9:16 | ~12~15 |
| **E** | ✂️ 유튜브 리뷰 → 숏폼 10개 | 9:16 | ~50 |

함께 묻기:
1. **선택**: A / B / C / D / E
2. **제품 자료** (다음 중 하나):
   - URL (쿠팡·올리브영·자사몰 등)
   - 제품 이미지 파일 경로
   - 제품명 + 컨셉 텍스트 (이미지는 AI 생성)
3. (선택) 브랜드·타겟·톤 한 줄

⏸ **답 받은 뒤에만 게이트 2로 이동.**

---

## 게이트 2 · 모델 이미지 기획·검토

컨셉이 D(모델 등장) 또는 A(인물 광고)일 때 다음 3 옵션 제시:

| # | 모델 컨셉 | 분위기 | 활용처 |
|---|---|---|---|
| **M1** | 에디토리얼 클로즈업 | 잡지 화보·정제·프리미엄 | 브랜드 키비주얼, 상세페이지 |
| **M2** | 모닝 루틴 라이프스타일 | 햇살·일상감 | 인스타 피드, 콘텐츠 마케팅 |
| **M3** | UGC 발색 리뷰 | 셀카·친근·진정성 | 틱톡·릴스 광고 후크 |

선택 후 **모델 프로필 4가지** 묻기:
- 성별·연령 (예: 20대 후반 여성)
- 인종·외형 (예: 한국인·동아시아)
- 피부·헤어·메이크업 (예: 글로우 클린 · 미디엄 웨이브 · 미니멀)
- 표정·포즈 (예: 차분·잔을 쇄골 근처에)

기본 추천 (M1): 20대 후반 한국인 여성 · 글로우 클린 피부 · 미디엄 웨이브 · 차분 · 9:16

확정 후 **영문 프롬프트 작성 → 사용자에게 보여주고 OK 받기**.

### 모델(MCP) 선택 가이드 ⭐ 오늘 학습 핵심

| 작업 | 1순위 모델 | 이유 |
|---|---|---|
| 포트레이트·UGC·에디토리얼 | `soul_2` | 인물·얼굴 최강 |
| **라벨/텍스트가 컷에 들어가는 경우** | `nano_banana_pro` ⭐ | 텍스트 렌더링 특화. soul_2 는 깨짐 |
| 광고 디테일·1클릭 광고 | `marketing_studio_image` | 광고 톤 자동 |

🚨 **중요**: 제품 라벨 텍스트가 컷에 들어가면 **무조건 `nano_banana_pro` 부터 시작**.
인물만 깨끗하게 잡고 싶고 라벨이 없거나 멀리 흐릿한 경우에만 `soul_2`.

생성 호출:
```python
mcp__claude_ai_Higgsfield__generate_image(params={
  "model": "nano_banana_pro",     # 텍스트 있으면 이걸로
  "aspect_ratio": "9:16",
  "count": 2,                     # 변형 비교용 2장 권장
  "get_cost": true,               # ⭐ 사전 견적 필수
  "prompt": "<영문 프롬프트>"
})
```

견적 본 뒤 `get_cost` 제거하고 실제 생성 호출.

폴링·표시:
```python
mcp__claude_ai_Higgsfield__job_status(jobId="...", sync=true)
mcp__claude_ai_Higgsfield__job_display(id="...")  # widget 렌더
```

⏸ **이미지 2장 보여주고 "어느 컷으로 갈까요?" 답 받기.**

---

## 게이트 3 · 텍스트 점검 (라벨이 있는 경우만)

생성된 이미지에 **제품 라벨·로고·브랜드 텍스트**가 있다면 사용자에게 확인:

```
🔍 라벨 텍스트 점검

생성된 이미지의 라벨이 제대로 읽히나요?
  · 깨끗하게 읽힘 → 게이트 4 (영상) 진행
  · 깨졌거나 가짜 글자 → nano_banana_pro 로 재생성
```

깨졌다면 3가지 조정:

1. **라벨 문구를 3줄 이하로 단순화**
   - ❌ 긴 풀텍스트: `Brand — Product — Tagline — 50ml / 1.7 fl oz` (깨지기 쉬움)
   - ✅ 3줄 분리:
     - Line 1 (large bold) : `Brand`
     - Line 2 (small)      : `Product Name`
     - Line 3 (tiny)       : `Size`

2. **프롬프트에 텍스트 명시 강화**:
   ```
   Product label (must be sharp, perfectly legible, English text,
   no garbled or fake letters): ... exactly three lines of dark navy text ...
   Nothing else on the label. No extra characters. Text must be in proper
   English with correct spelling.
   ```

3. **`nano_banana_pro` 재호출**

⏸ **재생성 결과 확인 후 게이트 4 진행.**

---

## 게이트 4 · 영상 시나리오·견적

선택된 이미지 → 영상의 `start_image`로 체이닝:

```python
medias=[{"role": "start_image", "value": "<image-job-id>"}]
```

이미지 job_id 를 그대로 넣으면 됨 (URL 업로드 불필요).

### 모델 선택 — Starter 폴백 체인 ⭐ 오늘 학습 핵심

```
1순위 시도 : seedance_2_0       → "Requires plus plan or higher" 에러면 ▼
2순위 폴백 : kling2_6           → 시네마틱 + 자동 음향, 5초, ~10 크레딧 ⭐
3순위 폴백 : veo3_1_lite        → 가성비 8초, 무음, ~8 크레딧
4순위 폴백 : minimax_hailuo     → 인물 자연 표정, 6초, ~변동
```

🚨 **반드시 `get_cost: true` 로 견적부터** — 실제 비용이 추정의 2 배 나오는 경우 흔함.
(예: seedance_2_0 std 8 초 720p = **36 크레딧**, 추정 15~20 의 약 2 배)

### 스토리보드 작성 (5 초 표준)

| 시간 | 액션 | 카메라 |
|---|---|---|
| 0–1.5 s | 정지, 자연 호흡 | 매우 느린 푸시-인 (3°) |
| 1.5–3 s | 모델 액션 시작 (눈뜨기·손동작) | 푸시-인 계속 |
| 3–4.5 s | 핵심 액션 (제품 노출·라벨 정면) | 정지 |
| 4.5–5 s | 마무리 (표정·시선) | 정지 |

### 영상 프롬프트 표준 패턴 ⭐ 오늘 학습

```
Calm editorial beauty footage, premium morning mood.
{Subject identical to start image}.
Very subtle slow push-in (about 3 degrees over 5 seconds), breath-like rhythm.

0-1.5s: {still moment, micro motion — breath, hair sway}
1.5-3s: {primary action — eyes open, gaze drift}
3-4.5s: {product reveal — wrist tilt, label faces camera}
4.5-5s: {closing beat — soft smile, gaze settles}

IMPORTANT: ambient natural daylight only, NO dramatic light streaks,
NO sun rays across the face, NO sun flares, NO sparkle effects.
{Subject/product} remain pin-sharp and identical to the start image.
No scene changes, no new objects, one person only.
Ambient sound: {natural environment cue — room tone, breeze}.
```

🚨 **부자연 라이트 효과**(sun ray on face, sun flare, sparkle) 는 **항상 NEGATIVE 명시**.
빼면 얼굴에 어색한 빛이 깔린다 (오늘 v1 실패 → v2 수정 사례).

### 서버 프리셋 제안 거절 (자주 발생) ⭐ 오늘 학습

`generate_video` 응답에 `preset_recommendation` 이 뜨면 (예: "IN THE DARK" 같은 무관 프리셋), 거절하고 리트라이:

```python
mcp__claude_ai_Higgsfield__generate_video(params={
  ...기존 params,
  "declined_preset_id": "<응답의 preset.id>"
})
```

### 폴링 검증 오류 우회 ⭐ 오늘 학습

`job_status` / `job_display` 가 다음 에러 내면:
```
Output validation error: aspect_ratio: expected string, received null
```

→ `raw_data: true` 옵션으로 폴링:

```python
mcp__claude_ai_Higgsfield__job_status(jobId="...", sync=true, raw_data=true)
# 응답의 raw_data.result_url 에서 영상 URL 추출
```

⏸ **견적 보여주고 "이대로 진행 OK?" 답 받기.**

---

## 게이트 5 · 피드백 루프

생성 영상 URL + 메타정보 표시:

```
✅ 영상 생성 완료
  · URL  : https://d8j0ntlcm91z4.cloudfront.net/.../xxx.mp4
  · 모델 : {kling2_6}
  · 스펙 : 5초 · 9:16 · 1080p · 음향 {on/off}
  · 차감 : {N} 크레딧 → 잔여 {M}

👉 다음 액션 :
  A. 만족 → 마무리
  B. 변형 1편 더 (다른 모션·표정 · ~10 크레딧)
  C. 1:1 또는 16:9 추가 비율
  D. 다른 컨셉으로 전환 (M1 → M2/M3)
  E. 카피 오버레이용 한국어 광고 문구 제안
  F. 바이럴 가능성 분석 (virality_predictor, +1 크레딧)
```

⏸ **답 받은 뒤에만 진행.** B/C/D 선택 시 게이트 2 또는 게이트 4 재진입.

---

## Step 6 · 마무리

```
🎉 Higgsfield 콘텐츠 제작 완료

📦 산출물
  · 이미지 1~2 장 (URL)
  · 5초 광고 영상 1 편 (URL)
  · 총 크레딧 소진 : {N} (잔여 {M})

💡 크레딧 절감 핵심 7가지 (오늘 학습)
  1. 사전 기획 + 게이트마다 사용자 확인 → 재생성 0
  2. `get_cost: true` 로 견적부터 (실제 비용이 추정의 2 배 나오는 경우 다수)
  3. 라벨/텍스트가 들어가면 `nano_banana_pro` 1순위
  4. 영상 모델 폴백 체인 인지 (seedance Plus → kling 5초 → veo lite 8초)
  5. start_image chaining 으로 정체성 잠금 (image job_id 재사용)
  6. 부자연 라이트 효과 (sun ray / flare / sparkle) NEGATIVE 명시
  7. 프리셋 추천 자동 거절 (`declined_preset_id`)

🚀 다음 단계 후보
  A. Buffer MCP 결합 → 자동 예약 발행
  B. Part 5 콘텐츠·카피 에이전트로 한국어 카피 합성
  C. 같은 톤 캐러셀 5장 일괄 (~10 크레딧)
  D. 다른 비율 (1:1·16:9) 추가
  E. virality_predictor 로 영상 점수 측정
```

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `Requires plus plan or higher` | seedance_2_0 등 Plus 전용 모델 | kling2_6 (5초) / veo3_1_lite (8초) 폴백 |
| 응답에 `preset_recommendation` | 서버가 무관 프리셋 추천 | `declined_preset_id` 에 preset id 넣고 재호출 |
| `job_status validation error` (aspect_ratio null) | MCP 응답 스키마 미스매치 | `raw_data: true` 옵션 |
| 라벨 텍스트 깨짐 / 가짜 글자 | soul_2 의 약점 | nano_banana_pro 재생성 + 라벨 3줄 단순화 |
| 얼굴에 어색한 햇살·플레어 | 프롬프트에 "sun ray/flare" 포함 | "NO sun rays, NO sun flares, NO sparkle" 명시 |
| 실제 비용 > 추정 (2배 이상) | 모델·해상도·길이 조합 | `get_cost: true` 사전 확인 의무화 |
| OAuth 인증 실패 | 세션 만료 | Claude Code 재시작 후 OAuth 재인증 |
| 영상 모션 부자연 | 동작이 너무 복잡 | 5초 안에 1~2 액션으로 축약 |
| 잔여 크레딧 부족 | 플랜 / 사용량 | `show_plans_and_credits` 호출 |

---

## 호출되는 도구

| 도구 | 단계 | 크레딧 |
|---|---|---|
| `mcp__claude_ai_Higgsfield__balance` | Step 0 | 0 |
| `mcp__claude_ai_Higgsfield__list_workspaces` | Step 0 | 0 |
| `mcp__claude_ai_Higgsfield__models_explore` | (필요시 폴백 확인) | 0 |
| `mcp__claude_ai_Higgsfield__generate_image` | 게이트 2·3 | 2~4 |
| `mcp__claude_ai_Higgsfield__job_status` | 폴링 | 0 |
| `mcp__claude_ai_Higgsfield__job_display` | widget 렌더 | 0 |
| `mcp__claude_ai_Higgsfield__generate_video` | 게이트 4 | 8~36 |
| `mcp__claude_ai_Higgsfield__virality_predictor` | 게이트 5 옵션 | 1 |
| `mcp__claude_ai_Higgsfield__show_plans_and_credits` | 크레딧 부족 시 | 0 |

---

## 모델 라인업 참고 (2026-05 기준)

### 이미지
| 모델 | 강점 | 1순위 용도 |
|---|---|---|
| `nano_banana_pro` | 4K · 텍스트 렌더링 | 라벨·로고·디테일 컷 ⭐ 텍스트 있으면 이걸로 |
| `soul_2` | 포트레이트·UGC·에디토리얼 | 인물 (텍스트 없을 때) |
| `marketing_studio_image` | 광고 톤 자동 | DTC 광고 1클릭 |

### 영상 (Starter 가용)
| 모델 | 길이 | 음향 | 비용 (대략) | 비고 |
|---|---|---|---|---|
| `kling2_6` | 5·10초 | 자동 | 10~ | 시네마틱 · ⭐ Starter 베스트 |
| `veo3_1_lite` | 4·6·8초 | 옵션 | 8~ | 가성비 · Google 안정성 |
| `minimax_hailuo` | 6·10초 | - | 변동 | 인물 표정 강함 |
| `kling3_0` | 3~15초 | 옵션 | 변동 | 멀티샷 (잔여 확인 필수) |

### 영상 (Plus+ 전용)
- `seedance_2_0` · `cinematic_studio_3_0` · `veo3_1` (ultra/preview) · 일부 `marketing_studio_video` 모드

---

## 참고 자료

- 설치 스킬 : [`../mcp설치-higgsfield/SKILL.md`](../mcp설치-higgsfield/SKILL.md)
- 실습 가이드 (수동) : [`../실습.md`](../실습.md)
- 결과물 예시 : [`../결과물-예시.md`](../결과물-예시.md)
