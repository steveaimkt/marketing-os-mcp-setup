# 클립 2-4 산출물 예시

본 클립 실습으로 만들 수 있는 영상 산출물 2개. 강의·검수·시연용 참조.

## 파일 목록

| 파일 | 길이 | 크기 | 해상도 | 패턴 | 사용 도구 |
|---|---|---|---|---|---|
| `2-4-weekly-kpi-6초.mp4` | 6초 | 386KB | 1080×1920 (9:16) | 데이터 KPI 영상 (케이스 A) | Hyperframes (단독) |
| `2-4-clip-1-1-변환-53초.mp4` | 53초 | 13MB | 1920×1080 (16:9) | 슬라이드 덱 → 영상 자동 변환 | Hyperframes (sub-comp 9개) |

## 검증 메타데이터

### 2-4-weekly-kpi-6초.mp4

- 내용: ROAS(로아스) 3.2x · CTR 4.8% · CPA 12,500원 KPI 카드 영상
- 사용 효과: 키네틱 타이포 · 마커 강조 · 스태거 등장
- 폰트: Pretendard(프리텐다드) 결정성 임베드
- 비율: 9:16 (인스타 릴스, 유튜브 쇼츠 호환)
- 생성 명령 예시: `"ROAS 3.2x 들어가는 6초 KPI 영상 만들어줘"`

### 2-4-clip-1-1-변환-53초.mp4

- 내용: 강의 클립 1-1 슬라이드 9장 (Cover → Manifesto → 사례·결론 → Closing) 자동 변환
- 사용 효과: 마커 하이라이트 · SVG 시계 다이얼 · 12방 광선 burst · 키네틱 타이포 · 게이지 차오름
- 폰트: Pretendard 결정성 임베드 (Linux/Docker 렌더에서도 동일 결과 보장)
- 비율: 16:9 (유튜브 본편, 강의 인트로용)
- 생성 명령 예시: `"클립 1-1 슬라이드 9장을 영상으로 변환해줘. 사용 가능한 효과 모두 적용해서"`
- 자동 처리 단계: slides.html 읽기 → 9 sub-composition 분리 → 등장 애니메이션 → 효과 적용 → lint·validate·inspect 검수 → mp4 렌더 (12분 자동, 수정 포함)

## 시간 비교

| 작업 | 사람이 만들 때 | 자동화 |
|---|---|---|
| 6초 KPI 영상 | 약 30분~1시간 | **약 5~8분** |
| 53초 강의 인트로 영상 | 약 2시간 (외주 시 반나절) | **약 12분** |

약 6~10배 빠름. 외주비 30~50만 원 → 0원에 가까움.

## 재생

macOS 기준:
```bash
open 2-4-weekly-kpi-6초.mp4
open 2-4-clip-1-1-변환-53초.mp4
```

또는 본 폴더를 Finder 에서 열어 더블클릭.

## 참고

본 영상은 [hyperframes/](../../../../hyperframes/) 작업 폴더에서 다음 명령으로 재생성 가능:
```bash
cd marketing-os/hyperframes
npm run check    # lint + validate + inspect
npm run render   # → renders/{timestamp}.mp4
```

원본 렌더 위치: [`hyperframes/renders/`](../../../../hyperframes/renders/) (전체 렌더 이력 보관)
