# 클립 4-1. Notion MCP · 콘텐츠 캘린더·기획서 자동 관리

## 한 줄 요약

Notion(노션) MCP(엠씨피)를 설치하면 Claude(클로드)가 본인 노션 워크스페이스의 **페이지·데이터베이스를 직접 만들고·검색하고·수정**한다. 콘텐츠 캘린더 30~50행 수동 입력 1시간이 5분으로 줄어든다.

## 마케터에게 왜 필요한가

- 마케팅 업무의 모든 메타데이터가 노션에 모임 · 콘텐츠 캘린더·브랜드 가이드·고객 응대 위키·주간 리포트
- 매주 콘텐츠 캘린더에 30~50개 행을 손으로 입력 (1~2시간)
- 광고 리포트·VoC(브이오씨) 분석 결과를 매번 노션에 정리·복붙 (시간당 약 20행)
- 회사 위키·매뉴얼·기획서가 노션에 흩어져 있는데, 필요할 때 찾기 어려움
- Notion MCP 설치 후 **콘텐츠 캘린더 30행 자동 입력 5분**, 리포트 자동 게시, 자연어 검색

## 무엇이 가능해지나

| 케이스 | 자연어 명령 예시 | 시간 |
|---|---|---|
| A. 워크스페이스 검색 | "노션 워크스페이스에서 '봄 캠페인' 관련 페이지 찾아줘" | 5초 |
| B. 페이지 가져오기 | "콘텐츠 캘린더 DB 의 이번 주 카드 보여줘" | 10초 |
| C. 페이지 생성 ★ | "이 광고 리포트 내용을 '주간 리포트' 페이지로 만들어줘" | 30초 |
| D. DB 카드 일괄 등록 ★ | "5월 콘텐츠 캘린더 30개 카드를 채널·날짜·상태 포함해서 등록" | 5분 |
| E. 페이지 수정 | "이 페이지의 상태를 '발행됨' 으로, 발행일을 오늘로 변경" | 5초 |
| F. 새 DB 생성 | "광고 리포트 아카이브 DB 새로 만들어줘 (날짜·매체·ROAS·인사이트)" | 1분 |
| G. 댓글 등록 | "이 카드에 검수 결과 코멘트 남겨줘" | 5초 |

## MCP 한눈

| 항목 | 값 |
|---|---|
| 인증 방식 | OAuth (Claude.ai 통합) · `.mcp.json` 등록 불필요 |
| 도구 prefix | `mcp__claude_ai_Notion__*` |
| 도구 수 | 16개 (검색·조회·생성·수정·댓글·DB·뷰·페이지 이동) |
| 무료 한도 | Notion Free 플랜 (개인 사용자 무제한 · 팀 협업 제한 있음) |
| 보안 권한 | 통합에 명시적으로 공유된 페이지만 접근 (페이지 단위 Add connections) |

본 MCP 는 Claude.ai 통합으로 **OAuth 한 번 인증 → 모든 세션 자동 사용** 합니다. 별도 패키지 설치·API key 발급 모두 불필요.

## 노출 도구 16개 (주요 7개)

| 도구 | 기능 | 마케팅 사례 |
|---|---|---|
| `notion-search` ★ | 워크스페이스 전체 검색 | 과거 페이지·문서 빠르게 찾기 |
| `notion-fetch` | 페이지·DB 내용 가져오기 | 콘텐츠 캘린더 DB 의 이번 주 카드 조회 |
| `notion-create-pages` ★ | 신규 페이지 또는 DB 카드 생성 | 광고 리포트 자동 게시, 캘린더 카드 등록 |
| `notion-update-page` | 페이지 내용·속성 수정 | 카드 상태·발행일 변경 |
| `notion-create-database` | 새 데이터베이스 생성 | 신규 프로젝트의 카탈로그·아카이브 |
| `notion-query-database-view` | DB 뷰 쿼리 (필터·정렬) | "status=approved 인 카드만" 같은 조회 |
| `notion-create-comment` | 페이지에 댓글 추가 | 검수 결과·피드백 자동 기록 |

기타 9개: `notion-update-data-source`, `notion-create-view`, `notion-update-view`, `notion-duplicate-page`, `notion-move-pages`, `notion-get-comments`, `notion-get-users`, `notion-get-teams`, `notion-query-meeting-notes`.

## 사전 준비물

- Notion 무료 계정 + 본인 워크스페이스
- Claude.ai 계정 (claude.ai 로그인)
- 콘텐츠 캘린더 DB 1개 (자동 생성도 가능)
- 통합 활성화: Claude.ai > Settings > Integrations > Notion > Connect (OAuth 1회)

## 작동 방식

```
[사용자 자연어 명령: "이번 주 콘텐츠 캘린더 30개 카드 등록"]
   ↓
[Claude Code]
   ↓
[Claude.ai OAuth 토큰 자동 사용 · .mcp.json 거치지 않음]
   ↓
[Notion REST API 호출 (notion-create-pages × 30)]
   ↓
[Notion 워크스페이스 · 통합에 공유된 페이지만 접근 가능]
   ↓
[결과: 30개 카드 URL 표 + 캘린더 뷰 갱신]
```

**중요**: 통합이 명시적으로 공유된 페이지만 접근 가능. 보안 측면에서 의도된 설계입니다.

## 호출 스킬

| 시점 | 스킬 | 역할 |
|---|---|---|
| 설치 단계 | [`/mcp설치-notion`](mcp설치-notion/SKILL.md) | OAuth 통합 활성화 + 페이지 공유 가이드 |
| 운영 단계 | "콘텐츠 캘린더 30개 등록" 같은 자연어 | Claude 가 `notion-create-pages` 호출 |

Part 3 콘텐츠 클립의 `content-publisher` · Part 5 의 `brand-guideline` · Part 6 의 광고 리포트 에이전트가 모두 본 MCP 를 자동 호출 (각각 캘린더 등록 · 가이드 페이지 생성 · 리포트 아카이브).

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `Page not found` | 통합에 페이지 미공유 | 해당 페이지 우상단 ··· > Add connections > Claude 선택 |
| `mcp__claude_ai_Notion__*` 도구 안 보임 | Claude.ai 통합 미활성화 | claude.ai > Settings > Integrations > Notion > Connect |
| 한글 페이지 제목 검색 안 됨 | 검색 인덱싱 지연 또는 정확도 | 키워드를 영문·혼합 또는 페이지 URL 직접 사용 |
| DB 속성 미일치 (`Property does not exist`) | DB 스키마와 다른 속성명 사용 | `notion-fetch` 로 스키마 먼저 확인 후 정확한 속성명 사용 |
| 페이지 생성 후 캘린더 뷰에 안 나옴 | 뷰의 필터 조건 미일치 | 카드의 속성 (상태·날짜·채널) 이 뷰 필터를 통과하는지 확인 |
| 워크스페이스 OAuth 안 보임 | Anthropic API key 인증 모드 사용 중 | claude.ai 구독으로 로그인 (`/login` 후 claude.ai 선택) |

## 검증된 산출물

- 콘텐츠 캘린더 5월 30개 카드 자동 등록 (제목·날짜·채널·상태·담당자)
- 광고 리포트 아카이브 DB 자동 생성 + 주간 카드 게시 (날짜·매체·ROAS·인사이트·링크)
- 브랜드 가이드 페이지 자동 작성 (보이스·톤·페르소나·금기어 섹션)
- 고객 응대 위키 검색 (cs-responder 에이전트 호출 패턴)
- 주간 회고 리포트 자동 게시 (`mkt-weekly-report` 에이전트 산출물)

## 다음

→ [`실습.md`](실습.md)
