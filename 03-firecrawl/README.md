# 클립 1-4. Firecrawl MCP · 경쟁사·시장 정보 자동 수집

## 한 줄 요약
**경쟁사 사이트·블로그·랜딩페이지·뉴스 기사**를 자연어로 긁어와 JSON·마크다운으로 정리합니다.

## 마케터에게 왜 필요한가
- 경쟁사 신제품 출시 → 매번 사이트 들어가서 캡처·메모 → 30분
- 시장 트렌드 기사 10개를 요약하려면 일일이 클릭 → 1시간
- 광고 랜딩 페이지 카피 분석 → 페이지 소스 봐야 함

Firecrawl이 있으면:
- "이 도메인의 신제품 페이지를 모두 긁어서 핵심 변경점만 표로" → 1줄
- Part 4 **`competitor-monitor` 에이전트**가 매일 자동 실행

## 무엇이 가능해지나
- `firecrawl_scrape` · 단일 URL → 마크다운/HTML/JSON
- `firecrawl_crawl` · 도메인 전체 크롤 (sitemap 기반)
- `firecrawl_search` · 키워드로 웹 검색 후 결과 페이지 크롤
- `firecrawl_extract` · 구조화 추출 (스키마 지정 가능)

## 사전 준비물
- Firecrawl 계정 (firecrawl.dev) · 무료 500크레딧/월
- API 키 1개

## 작동 방식

```
[Claude Code]
   ↓
[Firecrawl MCP] → [Firecrawl Cloud API] → 헤드리스 브라우저 → 타겟 사이트
   ↓
마크다운/JSON 반환
```

## 트러블슈팅 미리보기

| 증상 | 원인 | 해결 |
|---|---|---|
| `Rate limit exceeded` | 무료 플랜 분당 호출 제한 | 60초 대기 또는 유료 플랜 |
| 페이지가 비어 있음 | JS 렌더 필요 | `waitFor: 3000` 옵션 추가 |
| `403 Forbidden` | 사이트가 봇 차단 | `mobile: true` 또는 다른 user-agent |
| 한국어 깨짐 | 인코딩 자동 감지 실패 | `formats: ["markdown"]` 명시 |

→ [`실습.md`](실습.md)
