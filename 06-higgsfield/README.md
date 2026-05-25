# 클립 2-3. Higgsfield MCP · 이미지 생성·편집 자동화

## 한 줄 요약

Higgsfield(힉스필드) MCP(엠씨피)를 설치하면 Claude(클로드)가 본인 광고용 **이미지·영상·B-roll(비롤)·인트로를 텍스트 명령으로 즉시 생성**한다. Adobe·Blender 반나절 작업이 1~3분으로 줄어든다.

## 마케터에게 왜 필요한가

- 광고 캠페인마다 비주얼 자산 (이미지·영상·인트로) 이 매번 필요 · 디자이너·외주 의존
- 1장당 외주비 5~10만원 · 외주 대기 며칠 · 캠페인 일정 압박
- Adobe Photoshop·Blender 직접 작업 시 1장당 30분 ~ 2시간 + 숙련 필요
- AI 이미지 도구 (Midjourney·DALL-E) 따로 가입 + 별도 워크플로 + 결과를 다시 옮겨야
- Higgsfield MCP 설치 후 **자연어 한 줄 → 1~3분에 광고 비주얼 1장**, 동영상까지 즉시. Claude 안에서 통합 워크플로

## 무엇이 가능해지나

| 케이스 | 자연어 명령 예시 | 시간 |
|---|---|---|
| A. 광고 이미지 생성 ★ | "쿠팡 봄 캠페인 비주얼 1080×1080 · 핑크 톤" | 30초~1분 |
| B. 5초 인트로 영상 ★ | "브랜드 인트로 5초 영상 · 미니멀 모션" | 1~3분 |
| C. 캐러셀 5장 일괄 | "Instagram 캐러셀 5장 · 신학기 챌린지 컨셉" | 3~5분 |
| D. B-roll 클립 | "신상품 클로즈업 회전 B-roll 5초" | 1~3분 |
| E. 바이럴 점수 예측 | "이 영상 바이럴 가능성 점수와 개선점" | 30초 |
| F. 캐릭터·아바타 | "본 브랜드 페르소나 캐릭터 만들기" | 2분 |
| G. 마케팅 스튜디오 템플릿 | "캠페인 템플릿 50종 카탈로그 보여줘" | 10초 |

## MCP 한눈

| 항목 | 값 |
|---|---|
| 등록 방식 | **HTTP MCP** (`https://mcp.higgsfield.ai/mcp`) ⭐ |
| 인증 방식 | OAuth (첫 호출 시 브라우저 자동 · API key 불필요) |
| 도구 prefix | `mcp__higgsfield__*` (또는 Claude.ai 통합 시 `mcp__claude_ai_Higgsfield__*`) |
| 도구 수 | **18개** (생성 2 + 작업 4 + 미디어 3 + 워크스페이스 4 + 기타 5) |
| 무료 한도 | 가입 시 무료 크레딧 부여 · Plus/Pro 유료 플랜 (이미지 약 1~2 크레딧, 영상 5~10 크레딧) |

본 MCP 는 **HTTP MCP 직접 등록 방식**. .env 에 API key 추가 없음 · `.mcp.json` URL 한 줄만으로 등록. 첫 호출 시 브라우저 자동으로 OAuth 인증.

## 노출 도구 18개 (마케터 주요 7)

| 도구 | 기능 | 마케팅 사례 |
|---|---|---|
| `generate_image` ★ | 텍스트 → 이미지 생성 (Flux·SDXL 등) | 광고 비주얼·캐러셀·SNS 카드 |
| `generate_video` ★ | 텍스트 → 5~10초 영상 | 인트로·B-roll·반응 영상 |
| `virality_predictor` ★ | 영상 바이럴 점수·개선점 예측 | 발행 전 효과 점수 |
| `models_explore` | 사용 가능 모델 카탈로그 (Flux Pro · SDXL · 다양) | 스타일별 모델 선택 |
| `show_marketing_studio` | 마케팅 템플릿 카탈로그 50+ | 캠페인 템플릿 검색 |
| `show_characters` | 본인 캐릭터·아바타 라이브러리 | 브랜드 페르소나 유지 |
| `balance` | 잔여 크레딧 조회 | 비용 모니터링 |

기타 11개: `job_display`, `job_status`, `list_workspaces`, `select_workspace`, `show_generations`, `show_medias`, `media_upload`, `media_confirm`, `sync_agents`, `transactions`, `show_plans_and_credits`.

## 사전 준비물

- Node.js(노드 제이에스) 18+ · 터미널에서 `node --version`
- Higgsfield 무료 계정 (`higgsfield.ai`)
- 본인 워크스페이스 1개 (가입 시 자동 생성)
- 가입 무료 크레딧 (이미지 5~10장 또는 영상 1~2개 가능)
- Chrome 또는 Safari (OAuth 인증용)

## 작동 방식

```
[사용자 자연어 명령: "쿠팡 봄 캠페인 비주얼 1080×1080 핑크 톤"]
   ↓
[Claude Code]
   ↓
[mcp__higgsfield__generate_image 호출]
   ↓
[HTTP MCP 서버 (mcp.higgsfield.ai) · OAuth 토큰 자동]
   ↓
[Higgsfield 백엔드 · Flux/SDXL 모델 추론]
   ↓
[비동기 job 생성 → job_status 폴링]
   ↓
[1~3분 후 결과 이미지 URL 반환]
   ↓
[Claude 가 결과 표시 + 다운로드 안내]
```

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-higgsfield`](mcp설치-higgsfield/SKILL.md) | HTTP MCP 등록 + OAuth 인증 + 헬스 체크 |
| 운영 단계 | "광고 비주얼 만들어줘" 같은 자연어 | Claude 가 `generate_image`·`generate_video` 자동 호출 |

본 클립의 영상제작 트리오 (Hyperframes + HeyGen + ElevenLabs · Part 2 / 2-4) 와 결합 시 Higgsfield 가 **B-roll·3D 인트로** 를 담당.

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `OAuth 인증 실패` | 브라우저 팝업 차단 또는 세션 만료 | claude.ai 로그인 확인 + 팝업 허용 + Claude Code 재시작 |
| `Insufficient credits` | 무료 크레딧 소진 | `show_plans_and_credits` 로 잔액 확인 + Plus/Pro 플랜 |
| `Generation failed` | 프롬프트 정책 위반 (성인·폭력 등) | 프롬프트 다듬기 또는 다른 모델 선택 (`models_explore`) |
| `job_status` 가 계속 `pending` | 큐 적체 또는 대규모 요청 | 1~3분 대기 (영상은 5~10분) · 큰 작업은 새벽 시간 |
| `mcp__higgsfield__*` 도구 안 보임 | `.mcp.json` 등록 누락 또는 재시작 안 함 | `claude mcp list` 확인 + Claude Code 완전 종료 후 재시작 |
| 한국어 프롬프트 결과 어색 | 영어로 자동 번역 안 되거나 모델 한국어 약함 | 영문 프롬프트로 시도 또는 Claude 가 자동 번역 후 호출 |
| 이미지 비율·해상도 미적용 | 모델별 지원 비율 다름 | `models_explore` 로 모델별 지원 사양 확인 |

## 검증된 산출물

- 1080×1080 광고 비주얼 (Instagram 정사각형) · 30초~1분
- 5초 인트로 영상 (브랜드 로고 + 모션) · 1~3분
- Instagram 캐러셀 5장 일괄 (같은 톤·다른 컨셉) · 3~5분
- 신상품 클로즈업 회전 B-roll (영상제작 트리오 결합용) · 1~3분
- 바이럴 점수 예측 + 개선점 (발행 전 검증)

## 다음

→ [`실습.md`](실습.md)
