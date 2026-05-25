# 클립 2-4. 영상제작: Hyperframes + HeyGen + ElevenLabs 트리오

## 한 줄 요약

영상은 3 레이어로 분해된다. 그래픽(Hyperframes), 사람(HeyGen), 음성(ElevenLabs). 트리오를 한 번 설치하면 영상 1편이 30분 안에 나온다.

## 마케터에게 왜 필요한가

- 영상 제작은 마케팅 작업 중 손이 가장 많이 가는 영역. 1분 광고 영상 1편에 반나절(4시간 30분)이 보통
- 매주 5편 광고 영상을 만든다면 주당 22시간. 마케터 시간의 가장 큰 단일 항목
- 트리오로 자동화하면 1편당 20분. **주당 20시간 절감, 연간 1,040시간**

## 무엇이 가능해지나

| 케이스 | 도구 조합 | 길이 | 사례 |
|---|---|---|---|
| A. 데이터 KPI 영상 | Hyperframes + ElevenLabs | 6~30초 | 매주 광고 ROAS · 신제품 출시 카드 |
| B. 아바타 광고 | HeyGen + Hyperframes | 30~60초 | 인스타·페북 광고 · 임원 인사말 |
| C. 다국어 콘텐츠 | HeyGen translate + Hyperframes | 1~3분 | 글로벌 캠페인 다국어 동시 배포 |
| D. 풀 마케팅 영상 | 트리오 + Higgsfield | 1~3분 | 채널 본편 · 제품 데모 풀 영상 |

## 3 도구 한눈

| 도구 | 역할 | 인증 | 무료 한도 |
|---|---|---|---|
| **Hyperframes** | 그래픽 레이어 (HTML+CSS+GSAP) | 로컬 CLI (인증 없음) | 무제한 (Apache 2.0) |
| **HeyGen MCP** | 사람 레이어 (아바타 토킹헤드) | API key | 월 10 크레딧 |
| **ElevenLabs MCP** | 음성 레이어 (한국어 TTS · 음성 클론) | API key | 월 1만 크레딧 (10분) |

## 사전 준비물

- Node.js 22+
- Chrome 브라우저
- ffmpeg (없으면 본 클립에서 자동 설치 안내)
- uv 패키지 매니저 (없으면 자동 설치)
- HeyGen 계정 (무료 가입)
- ElevenLabs 계정 (무료 가입)

## 작동 방식

```
[사용자 명령 한 줄]
   ↓
[mcp설치-영상제작 스킬]
   ↓
① Hyperframes 설치 → 6초 KPI 영상 1편
   ↓
② HeyGen MCP 설치 → 60초 한국어 아바타 영상 1편
   ↓
③ ElevenLabs MCP 설치 → 30초 한국어 mp3 1개
   ↓
④ 통합 결과물: 53초 데이터 영상 자동 생성
   ↓
[Discord · Notion 발송]
```

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-영상제작`](../../../skills/mcp설치-영상제작/SKILL.md) | 3 도구 4단계 순차 설치 |
| 운영 단계 | [`/영상제작`](../../../skills/영상제작/SKILL.md) | 트리오 통합 파이프라인 (8단계) |

## 트러블슈팅 미리보기

| 증상 | 해결 |
|---|---|
| Pretendard 한국어 폰트 깨짐 | CDN URL 을 `cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/static/woff2/` 패턴으로 |
| HeyGen 영상 생성 1~3분 대기 | 큐 적체. 한국 새벽 또는 짧은 길이로 테스트 |
| ElevenLabs 한국어 받침 어색 | `model_id=eleven_v3`, `language=ko` 명시 |
| Hyperframes `npm run check` 실패 | `data-track-index` 다른 값으로 분리 (같은 트랙 시간 겹침) |

## 검증된 산출물

- 6초 WeeklyKPI 영상: [`산출물예시/2-4-weekly-kpi-6초.mp4`](산출물예시/2-4-weekly-kpi-6초.mp4) (386KB, 9:16, 데이터 KPI 영상 패턴)
- 53초 통합 영상: [`산출물예시/2-4-clip-1-1-변환-53초.mp4`](산출물예시/2-4-clip-1-1-변환-53초.mp4) (13MB, 16:9, 강의 1-1 슬라이드 9장 자동 변환)

## 다음

→ [`실습.md`](실습.md)
