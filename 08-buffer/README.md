# 클립 3-1. Buffer MCP · SNS 다채널 자동 발행·예약

## 한 줄 요약

Buffer(버퍼) MCP(엠씨피)를 설치하면 Claude(클로드)가 본인 SNS 5개 채널 (Instagram·Facebook·X·LinkedIn·Threads) 에 **하나의 명령으로 동시 예약 발행**한다. 5채널 × 30분 작업이 5분으로 줄어든다.

## 마케터에게 왜 필요한가

- 1인 마케터는 같은 콘텐츠를 5개 SNS 에 채널별 톤·길이·해시태그로 다르게 올리는 데 매번 2~3시간
- 콘텐츠 캘린더 (Notion · Sheets) 에서 발행 시간을 매번 직접 옮겨야 함
- 발행 후 시간대별 성과 데이터를 별도 작업으로 가져와야 함
- Buffer MCP 설치 후 **5채널 자동 예약 5분**, 콘텐츠 캘린더 직접 연동, 발행 후 성과까지 자동 회수

## 무엇이 가능해지나

| 케이스 | 자연어 명령 예시 | 시간 |
|---|---|---|
| A. 채널 목록 조회 | "Buffer 에 연결된 내 채널 목록 보여줘" | 5초 |
| B. 단일 채널 예약 | "내일 09:00 Instagram 에 이 캐러셀 5장 예약" | 30초 |
| C. 다채널 동시 예약 ★ | "신제품 발표 메시지를 5채널에 톤·해시태그 자동 조정해서 동시 예약" | 5분 |
| D. 큐 상태 확인 | "이번 주 예약된 게시물 전체 보여줘" | 10초 |
| E. 게시물 취소 | "오늘 18시 X 게시물 취소해줘" | 5초 |
| F. 채널별 성과 분석 | "지난주 채널별 좋아요·도달·노출 비교" | 1~2분 |

## MCP 한눈

| 항목 | 값 |
|---|---|
| 패키지 | `@damusix/buffer-mcp` (npx) |
| 인증 | Personal Access Token (`BUFFER_ACCESS_TOKEN`) |
| 단일 진입점 | `use_buffer_api` (액션 키 방식) |
| 도움말 | `buffer_api_help` (어떤 액션이 가능한지 조회) |
| 무료 한도 | Buffer Free 플랜 · 3채널 · 10개 예약 |
| 유료 한도 | Essentials $6/월 부터 무제한 |

본 MCP 는 다른 MCP 와 달리 **도구 1개 (`use_buffer_api`) 의 액션 키 방식**으로 작동합니다. 액션 키는 `listChannels`, `createPost`, `getPost`, `deletePost`, `listScheduled` 등.

## 노출 도구 2개 + 주요 액션 키

### 도구

| 도구 | 역할 |
|---|---|
| `use_buffer_api` | Buffer API 호출 진입점 (액션 키 + 파라미터) |
| `buffer_api_help` | 사용 가능 액션 목록·파라미터 조회 |

### 주요 액션 키 (사용 빈도순)

| 액션 | 기능 | 마케팅 사례 |
|---|---|---|
| `listChannels` | 연결된 채널 목록 + ID | 본인 Buffer 계정의 채널 확인 |
| `createPost` | 예약 게시물 생성 (텍스트·미디어·시각) | 단일 또는 다채널 동시 예약 |
| `listScheduled` | 예약 대기 큐 조회 | 이번 주 예약 현황 확인 |
| `getPost` | 단일 게시물 상세 | 게시물 ID 로 상태 조회 |
| `updatePost` | 예약 시각·텍스트 수정 | 발행 전 수정 |
| `deletePost` | 예약 취소 | 발행 전 취소 |
| `listAnalytics` | 채널별 성과 (좋아요·도달·노출) | 주간 성과 비교 |

## 사전 준비물

- Node.js(노드 제이에스) 18+ · 터미널에서 `node --version`
- Buffer 무료 계정 (`publish.buffer.com`)
- SNS 채널 1개 이상 Buffer 에 연결 (Instagram · Facebook · X · LinkedIn · Threads)
- Personal Access Token (Buffer Settings · Apps & Extras · API)

## 작동 방식

```
[사용자 자연어 명령: "신제품 5채널 동시 예약"]
   ↓
[Claude Code 가 채널 톤·길이·해시태그 분기]
   ↓
[mcp__buffer__use_buffer_api 호출 × 5번 (채널별)]
   ↓
[Buffer API · Personal Access Token 인증]
   ↓
[Buffer 큐에 5개 게시물 등록 → 각 채널의 예약 시각에 자동 발행]
   ↓
[결과: 게시물 ID 5개 + 예약 시각 + 채널 매핑 표]
```

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-buffer`](mcp설치-buffer/SKILL.md) | Token 발급 + .mcp.json 등록 자동 진행 |
| 운영 단계 | "5채널 동시 예약" 같은 자연어 | Claude 가 채널별 변형 + Buffer 예약 자동 |

Part 3 콘텐츠 파이프라인의 `content-publisher` 에이전트가 본 MCP 를 자동 호출 (콘텐츠 승인 → 자동 예약).

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `401 Unauthorized` | Token 오타·만료·형식 오류 | Buffer Settings > Apps & Extras > API 에서 재발급 (Bearer 토큰 형식 확인) |
| 채널 0개 응답 | Buffer 대시보드에 채널 미연결 | `publish.buffer.com` 에서 SNS 채널 OAuth 연결 후 재시도 |
| 이미지 업로드 실패 | URL 이 외부 접근 불가 | S3·CDN·공개 이미지 URL 사용 (로컬 파일은 안 됨) |
| `mcp__buffer__*` 도구 안 보임 | `.mcp.json` 문법 오류 또는 재시작 안 함 | `python3 -c "import json; json.load(open('.mcp.json'))"` 검증 + Claude 재시작 |
| `Quota exceeded` (Free 플랜) | 10개 예약 한도 초과 | Essentials 플랜으로 업그레이드 또는 큐에서 일부 삭제 |
| 액션 키 오류 | 잘못된 액션 이름 | `mcp__buffer__buffer_api_help` 로 사용 가능 액션 먼저 조회 |

## 검증된 산출물

- 신제품 발표 5채널 동시 예약 (Instagram 캐러셀 + 스토리 + Facebook + X + LinkedIn)
- 주간 캘린더 일괄 적용 (Notion DB → Buffer 큐 자동 입력)
- 발행 후 시간대별 성과 표 (좋아요·도달·노출 채널 비교)

## 다음

→ [`실습.md`](실습.md)
