"""
유튜브 채널 분석기 (Phase 1: Data API v3 공개 데이터)

사용법:
    python tools/analyze_channel.py                         # tools/.env의 YOUTUBE_CHANNEL_ID 사용
    python tools/analyze_channel.py UCfEs5z2Woa_vaB-UtvUmyTw  # 채널 ID 직접 지정
    python tools/analyze_channel.py "@marketing_truman"       # 핸들 지정
    python tools/analyze_channel.py "마케팅 트루먼쇼"          # 검색

출력:
    analysis/{채널 핸들 또는 ID}/raw/
        channel.json                — 채널 메타데이터
        videos.json                 — 영상 목록 + 통계
    analysis/{채널}/reports/
        YYYY-MM-DD-insights.md      — 마크다운 인사이트 리포트

인사이트:
    - 채널 개요 (구독자/총조회수/영상수/평균조회수)
    - 상위 10 영상 (조회수)
    - 상위 10 영상 (참여율 = (좋아요+댓글)/조회수)
    - 최근 30일 / 90일 영상 성과 분석
    - 업로드 패턴 (요일/시간대/주기)
    - 제목 분석 (글자수, 자주 쓰이는 단어)
    - 영상 길이별 성과
    - 트렌드 (최근 5편 vs 이전 5편)
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 같은 폴더의 youtube_api import
sys.path.insert(0, str(Path(__file__).parent))
from youtube_api import YouTubeClient, YouTubeAPIError


# ────────────────────────────────────────────────────────────────
# 데이터 페치
# ────────────────────────────────────────────────────────────────
def fetch_channel_data(query: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    yt = YouTubeClient()
    if not query:
        query = yt._env.get("YOUTUBE_CHANNEL_ID") or yt._env.get("YOUTUBE_CHANNEL_QUERY")
    if not query:
        raise SystemExit("채널 식별자가 없습니다. 인자로 채널 ID/핸들/검색어 전달하거나 tools/.env 설정.")
    print(f"[INFO] 채널 조회: '{query}'")
    channel = yt.find_channel(query)
    if not channel:
        raise SystemExit(f"채널을 찾을 수 없습니다: {query}")
    print(f"[INFO] 채널: {channel['snippet']['title']} ({channel['id']})")
    print(f"[INFO] 영상 목록 수집 중...")
    videos = yt.list_channel_videos(channel["id"])
    print(f"[INFO] {len(videos)}개 영상 수집 완료. Quota 사용: ~{yt.quota_used} units")
    return channel, videos


# ────────────────────────────────────────────────────────────────
# 분석
# ────────────────────────────────────────────────────────────────
DAY_KR = ["월", "화", "수", "목", "금", "토", "일"]


def parse_duration(iso: str) -> int:
    """ISO 8601 duration (PT#M#S) → 초"""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mn, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mn * 60 + s


def fmt_duration(sec: int) -> str:
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


def normalize_videos(videos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """API 응답을 분석하기 좋은 형태로 정규화."""
    out = []
    for v in videos:
        snip = v["snippet"]
        stat = v.get("statistics", {})
        cd = v.get("contentDetails", {})
        views = int(stat.get("viewCount", 0))
        likes = int(stat.get("likeCount", 0))
        comments = int(stat.get("commentCount", 0))
        published = snip.get("publishedAt", "")
        try:
            pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        except Exception:
            pub_dt = None
        duration_sec = parse_duration(cd.get("duration", ""))
        engagement = (likes + comments) / views if views > 0 else 0.0
        out.append(
            {
                "id": v["id"],
                "title": snip.get("title", ""),
                "description": snip.get("description", ""),
                "tags": snip.get("tags", []),
                "published": published,
                "published_dt": pub_dt,
                "duration_sec": duration_sec,
                "is_short": duration_sec > 0 and duration_sec <= 60,
                "views": views,
                "likes": likes,
                "comments": comments,
                "engagement": engagement,  # (likes+comments)/views
                "url": f"https://youtu.be/{v['id']}",
                "thumbnail": (snip.get("thumbnails", {}).get("medium") or {}).get("url", ""),
            }
        )
    return out


def top_n(videos: list[dict[str, Any]], key: str, n: int = 10, reverse: bool = True) -> list[dict[str, Any]]:
    return sorted(videos, key=lambda v: v[key], reverse=reverse)[:n]


def upload_pattern(videos: list[dict[str, Any]]) -> dict[str, Any]:
    """요일별 / 시간대별 업로드 분포 + 평균 조회수."""
    by_dow: dict[int, list[int]] = defaultdict(list)
    by_hour: dict[int, list[int]] = defaultdict(list)
    intervals: list[float] = []
    sorted_by_date = sorted(
        [v for v in videos if v["published_dt"]], key=lambda v: v["published_dt"]
    )
    for v in sorted_by_date:
        dt = v["published_dt"]
        by_dow[dt.weekday()].append(v["views"])
        by_hour[dt.hour].append(v["views"])
    for i in range(1, len(sorted_by_date)):
        delta = sorted_by_date[i]["published_dt"] - sorted_by_date[i - 1]["published_dt"]
        intervals.append(delta.total_seconds() / 86400)  # 일 단위
    return {
        "by_dow": {
            DAY_KR[d]: {
                "count": len(by_dow[d]),
                "avg_views": int(sum(by_dow[d]) / len(by_dow[d])) if by_dow[d] else 0,
            }
            for d in range(7)
        },
        "by_hour": {
            h: {"count": len(by_hour[h]), "avg_views": int(sum(by_hour[h]) / len(by_hour[h])) if by_hour[h] else 0}
            for h in sorted(by_hour.keys())
        },
        "avg_interval_days": round(sum(intervals) / len(intervals), 1) if intervals else 0.0,
        "median_interval_days": round(sorted(intervals)[len(intervals) // 2], 1) if intervals else 0.0,
    }


def title_analysis(videos: list[dict[str, Any]]) -> dict[str, Any]:
    """제목 길이 / 키워드 빈도."""
    lengths = [len(v["title"]) for v in videos]
    avg_len = sum(lengths) / len(lengths) if lengths else 0
    # 한글/영문 단어 빈도 (2자 이상, 불용어 제거)
    stop = {
        "the", "and", "for", "with", "from", "이", "그", "저", "것", "수", "더",
        "있는", "있다", "하는", "위한", "어떻게", "왜", "무엇", "뭐", "왜냐하면",
        "vs", "ai", "is", "of", "to", "by", "in", "on", "or", "an", "a",
    }
    words: Counter[str] = Counter()
    for v in videos:
        # 특수문자 제거, 공백 분리, 소문자
        clean = re.sub(r"[^\w가-힣\s]", " ", v["title"]).lower()
        for w in clean.split():
            if len(w) >= 2 and w not in stop:
                words[w] += 1
    return {
        "avg_length": round(avg_len, 1),
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "top_keywords": words.most_common(20),
    }


def recent_trend(videos: list[dict[str, Any]], days: int = 30) -> dict[str, Any]:
    """최근 N일 영상 분석."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = [v for v in videos if v["published_dt"] and v["published_dt"] >= cutoff]
    if not recent:
        return {"count": 0}
    return {
        "count": len(recent),
        "total_views": sum(v["views"] for v in recent),
        "avg_views": int(sum(v["views"] for v in recent) / len(recent)),
        "avg_engagement_pct": round(sum(v["engagement"] for v in recent) / len(recent) * 100, 2),
        "top": top_n(recent, "views", 3),
    }


def shorts_vs_long(videos: list[dict[str, Any]]) -> dict[str, Any]:
    shorts = [v for v in videos if v["is_short"]]
    longs = [v for v in videos if not v["is_short"]]
    def summary(lst: list[dict[str, Any]]) -> dict[str, Any]:
        if not lst:
            return {"count": 0, "avg_views": 0, "avg_engagement_pct": 0.0}
        return {
            "count": len(lst),
            "avg_views": int(sum(v["views"] for v in lst) / len(lst)),
            "avg_engagement_pct": round(sum(v["engagement"] for v in lst) / len(lst) * 100, 2),
        }
    return {"shorts": summary(shorts), "long": summary(longs)}


def momentum(videos: list[dict[str, Any]], window: int = 5) -> dict[str, Any]:
    """최근 N편 vs 이전 N편 평균 조회수 비교."""
    sorted_by_date = sorted(
        [v for v in videos if v["published_dt"]], key=lambda v: v["published_dt"], reverse=True
    )
    if len(sorted_by_date) < window * 2:
        return {}
    recent = sorted_by_date[:window]
    prior = sorted_by_date[window : window * 2]
    r_avg = sum(v["views"] for v in recent) / window
    p_avg = sum(v["views"] for v in prior) / window
    return {
        "recent_avg": int(r_avg),
        "prior_avg": int(p_avg),
        "change_pct": round((r_avg - p_avg) / p_avg * 100, 1) if p_avg > 0 else 0.0,
        "recent_titles": [v["title"] for v in recent],
    }


# ────────────────────────────────────────────────────────────────
# 리포트 생성
# ────────────────────────────────────────────────────────────────
def fmt_n(n: int) -> str:
    return f"{n:,}"


def fmt_pct(p: float) -> str:
    sign = "+" if p > 0 else ""
    return f"{sign}{p}%"


def render_report(channel: dict[str, Any], videos: list[dict[str, Any]]) -> str:
    snippet = channel["snippet"]
    stats = channel["statistics"]
    title = snippet["title"]
    handle = snippet.get("customUrl", "")
    sub_count = int(stats.get("subscriberCount", 0))
    view_count = int(stats.get("viewCount", 0))
    video_count = int(stats.get("videoCount", 0))
    created = snippet.get("publishedAt", "")[:10]
    avg_views = int(sum(v["views"] for v in videos) / len(videos)) if videos else 0
    today = datetime.now().strftime("%Y-%m-%d")

    # 분석
    by_views = top_n(videos, "views", 10)
    by_engagement = top_n([v for v in videos if v["views"] >= 100], "engagement", 10)  # 노이즈 제거
    pattern = upload_pattern(videos)
    titles = title_analysis(videos)
    recent_30 = recent_trend(videos, 30)
    recent_90 = recent_trend(videos, 90)
    fmt_shorts = shorts_vs_long(videos)
    mom = momentum(videos, window=5)

    md = []
    md.append(f"# {title} — 채널 인사이트 리포트")
    md.append(f"\n_생성일: {today} · 데이터 소스: YouTube Data API v3 (공개 통계)_\n")
    md.append("---\n")

    # 1. 채널 개요
    md.append("## 1. 채널 개요\n")
    md.append(f"| 항목 | 값 |")
    md.append(f"|------|----|")
    md.append(f"| 채널명 | {title} |")
    md.append(f"| 핸들 | {handle or '(없음)'} |")
    md.append(f"| 채널 ID | `{channel['id']}` |")
    md.append(f"| 구독자 | **{fmt_n(sub_count)}** |")
    md.append(f"| 총 영상 수 | {fmt_n(video_count)} (수집 {len(videos)}개) |")
    md.append(f"| 총 조회수 | {fmt_n(view_count)} |")
    md.append(f"| 영상당 평균 조회수 | **{fmt_n(avg_views)}** |")
    md.append(f"| 생성일 | {created} |")
    md.append(f"| URL | https://www.youtube.com/channel/{channel['id']} |\n")

    # 2. 상위 영상
    md.append("\n## 2. 상위 10 영상 (조회수)\n")
    md.append("| # | 제목 | 조회수 | 좋아요 | 댓글 | 길이 | 참여율 |")
    md.append("|---|------|--------|--------|------|------|--------|")
    for i, v in enumerate(by_views, 1):
        short = " 🩳" if v["is_short"] else ""
        md.append(
            f"| {i} | [{v['title'][:50]}]({v['url']}){short} | "
            f"{fmt_n(v['views'])} | {fmt_n(v['likes'])} | {fmt_n(v['comments'])} | "
            f"{fmt_duration(v['duration_sec'])} | {v['engagement']*100:.2f}% |"
        )

    # 3. 참여율 상위
    md.append("\n## 3. 참여율 TOP 10 (조회수 100 이상)\n")
    md.append("좋아요+댓글이 조회수 대비 높은 영상 — 시청자가 반응한 콘텐츠 패턴 파악용.\n")
    md.append("| # | 제목 | 참여율 | 조회수 |")
    md.append("|---|------|--------|--------|")
    for i, v in enumerate(by_engagement, 1):
        short = " 🩳" if v["is_short"] else ""
        md.append(
            f"| {i} | [{v['title'][:50]}]({v['url']}){short} | "
            f"**{v['engagement']*100:.2f}%** | {fmt_n(v['views'])} |"
        )

    # 4. 모멘텀 (최근 vs 이전)
    if mom:
        md.append("\n## 4. 최근 모멘텀 (최근 5편 vs 이전 5편)\n")
        md.append(f"- **최근 5편 평균 조회수**: {fmt_n(mom['recent_avg'])}")
        md.append(f"- **이전 5편 평균 조회수**: {fmt_n(mom['prior_avg'])}")
        md.append(f"- **변화**: {fmt_pct(mom['change_pct'])}")
        md.append("\n최근 5편:")
        for t in mom["recent_titles"]:
            md.append(f"  - {t}")

    # 5. 최근 30일 / 90일
    md.append("\n## 5. 최근 활동\n")
    for label, r in [("30일", recent_30), ("90일", recent_90)]:
        if r.get("count", 0) == 0:
            md.append(f"### 최근 {label}: 업로드 없음")
            continue
        md.append(f"### 최근 {label}")
        md.append(f"- 업로드: {r['count']}편")
        md.append(f"- 총 조회수: {fmt_n(r['total_views'])}")
        md.append(f"- 평균 조회수: {fmt_n(r['avg_views'])}")
        md.append(f"- 평균 참여율: {r['avg_engagement_pct']}%")
        if r.get("top"):
            md.append(f"- 상위 영상:")
            for v in r["top"]:
                md.append(f"  - [{v['title']}]({v['url']}) — {fmt_n(v['views'])} 조회")

    # 6. 업로드 패턴
    md.append("\n## 6. 업로드 패턴\n")
    md.append(f"- 평균 업로드 간격: **{pattern['avg_interval_days']}일** (중앙값 {pattern['median_interval_days']}일)\n")
    md.append("### 요일별 (조회수 평균)")
    md.append("| 요일 | 영상 수 | 평균 조회수 |")
    md.append("|------|---------|-------------|")
    for d in DAY_KR:
        row = pattern["by_dow"][d]
        bar = "█" * min(20, row["avg_views"] // max(1, avg_views // 10))
        md.append(f"| {d} | {row['count']} | {fmt_n(row['avg_views'])} {bar} |")

    # 7. 제목 분석
    md.append("\n## 7. 제목 분석\n")
    md.append(f"- 평균 길이: **{titles['avg_length']}자** (최소 {titles['min_length']}, 최대 {titles['max_length']})")
    md.append(f"- 자주 쓰이는 키워드 TOP 20:\n")
    kw_lines = []
    for kw, cnt in titles["top_keywords"]:
        kw_lines.append(f"  - `{kw}` × {cnt}")
    md.append("\n".join(kw_lines))

    # 8. 숏폼 vs 롱폼
    md.append("\n## 8. 숏폼 vs 롱폼\n")
    md.append("| 타입 | 영상 수 | 평균 조회수 | 평균 참여율 |")
    md.append("|------|---------|-------------|-------------|")
    s = fmt_shorts["shorts"]
    l = fmt_shorts["long"]
    md.append(f"| 숏폼 (≤60s) | {s['count']} | {fmt_n(s['avg_views'])} | {s['avg_engagement_pct']}% |")
    md.append(f"| 롱폼 (>60s) | {l['count']} | {fmt_n(l['avg_views'])} | {l['avg_engagement_pct']}% |")

    # 9. 핵심 인사이트 (자동 생성)
    md.append("\n## 9. 자동 도출 인사이트\n")
    insights = []
    # 모멘텀
    if mom:
        if mom["change_pct"] >= 20:
            insights.append(f"🚀 **최근 모멘텀 양호** — 최근 5편 평균이 이전 5편 대비 {fmt_pct(mom['change_pct'])}. 콘텐츠 방향 유지/강화.")
        elif mom["change_pct"] <= -20:
            insights.append(f"⚠️ **모멘텀 하락** — 최근 5편 평균이 이전 5편 대비 {fmt_pct(mom['change_pct'])}. 최근 영상 톤/주제 재검토 필요.")
    # 숏폼/롱폼
    if s["count"] >= 3 and l["count"] >= 3:
        if s["avg_views"] > l["avg_views"] * 2:
            insights.append(f"📱 **숏폼이 롱폼보다 평균 {s['avg_views']//max(1,l['avg_views'])}배 조회** — 숏폼 비중 확대 검토.")
        elif l["avg_views"] > s["avg_views"] * 2:
            insights.append(f"🎬 **롱폼이 숏폼보다 평균 {l['avg_views']//max(1,s['avg_views'])}배 조회** — 숏폼은 깔때기 용도, 롱폼이 핵심.")
    # 최고 영상
    if by_views:
        top = by_views[0]
        if top["views"] > avg_views * 3:
            insights.append(f"⭐ **돌출 영상 존재** — [{top['title']}]({top['url']})가 평균의 {top['views']//max(1,avg_views)}배. 해당 주제/제목 패턴 분석 후 복제 시도.")
    # 업로드 주기
    if pattern["avg_interval_days"] > 14:
        insights.append(f"📅 **업로드 주기 길음** ({pattern['avg_interval_days']}일) — 알고리즘 유지를 위해 주 1회 이상 권장.")
    # 참여율
    high_eng = [v for v in by_engagement if v["engagement"] > 0.05]
    if high_eng:
        sample_titles = ", ".join([f"\"{v['title'][:30]}\"" for v in high_eng[:3]])
        insights.append(f"💬 **참여율 5%+ 영상 {len(high_eng)}편** — {sample_titles} 등. 댓글 유발 요소(질문/논쟁) 분석 권장.")

    if not insights:
        insights.append("(임계값 미달 — 데이터가 더 쌓이면 자동 인사이트 출력)")
    for ins in insights:
        md.append(f"- {ins}")

    md.append("\n---\n")
    md.append(f"_다음 액션: 상위 영상 분석 → 제목 패턴 추출 → 다음 영상 주제 후보 도출_")

    return "\n".join(md)


# ────────────────────────────────────────────────────────────────
# 메인
# ────────────────────────────────────────────────────────────────
def main():
    query = sys.argv[1] if len(sys.argv) > 1 else None
    channel, videos_raw = fetch_channel_data(query)
    videos = normalize_videos(videos_raw)

    # 채널 핸들로 출력 폴더 결정
    handle = channel["snippet"].get("customUrl", channel["id"])
    handle = handle.lstrip("@")
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "analysis" / handle
    raw_dir = out_dir / "raw"
    reports_dir = out_dir / "reports"
    raw_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 원본 저장
    (raw_dir / "channel.json").write_text(json.dumps(channel, ensure_ascii=False, indent=2), encoding="utf-8")
    (raw_dir / "videos.json").write_text(
        json.dumps(videos_raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 리포트 생성
    report = render_report(channel, videos)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = reports_dir / f"{today}-insights.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"\n[OK] 리포트 생성:")
    print(f"  → {report_path}")
    print(f"\n[OK] 원본 데이터:")
    print(f"  → {raw_dir / 'channel.json'}")
    print(f"  → {raw_dir / 'videos.json'} ({len(videos)}개 영상)")


if __name__ == "__main__":
    main()
