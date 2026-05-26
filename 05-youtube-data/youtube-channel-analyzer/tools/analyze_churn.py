"""
구독자 취소율 분석 리포트

사용법:
    python3 tools/analyze_churn.py                  # 최근 7일
    python3 tools/analyze_churn.py --days 30        # 최근 30일
    python3 tools/analyze_churn.py --start 2026-05-01 --end 2026-05-25
    python3 tools/analyze_churn.py --no-videos      # 영상별 분석 스킵

출력:
    analysis/marketing_truman/reports/YYYY-MM-DD-churn-Nd.md
"""
from __future__ import annotations

import sys
import argparse
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from youtube_oauth import OAuthError, _load_env, _env_path
from youtube_analytics import (
    AnalyticsError,
    daily_subscriber_changes,
    per_video_subscriber_changes,
)
from youtube_api import YouTubeClient, YouTubeAPIError


def _fetch_video_titles(video_ids: list[str]) -> dict[str, str]:
    """videoId → title 매핑 (Data API)"""
    if not video_ids:
        return {}
    try:
        yt = YouTubeClient()
        data = yt._get("videos", {"part": "snippet", "id": ",".join(video_ids)})
        return {item["id"]: item["snippet"]["title"] for item in data.get("items", [])}
    except YouTubeAPIError:
        return {}


def _fetch_current_subscribers() -> int | None:
    env = _load_env(_env_path())
    cid = env.get("YOUTUBE_CHANNEL_ID", "").strip()
    if not cid:
        return None
    try:
        yt = YouTubeClient()
        channel = yt.get_channel(channel_id=cid)
        if channel:
            return int(channel["statistics"].get("subscriberCount", 0))
    except YouTubeAPIError:
        return None
    return None


def main():
    parser = argparse.ArgumentParser(description="구독자 취소율 분석")
    parser.add_argument("--days", type=int, default=7, help="분석 기간 (기본: 7일)")
    parser.add_argument("--start", help="시작일 YYYY-MM-DD (--days보다 우선)")
    parser.add_argument("--end", help="종료일 YYYY-MM-DD (기본: 오늘)")
    parser.add_argument("--output", help="리포트 저장 경로 (.md). 미지정 시 analysis/.../reports/ 자동")
    parser.add_argument("--no-videos", action="store_true", help="영상별 분석 스킵")
    args = parser.parse_args()

    # 기간 결정
    today = date.today()
    if args.start and args.end:
        start_date, end_date = args.start, args.end
        days = (date.fromisoformat(end_date) - date.fromisoformat(start_date)).days + 1
    else:
        end_date = args.end or today.isoformat()
        end_d = date.fromisoformat(end_date)
        if args.start:
            start_date = args.start
            days = (end_d - date.fromisoformat(start_date)).days + 1
        else:
            days = args.days
            start_date = (end_d - timedelta(days=days - 1)).isoformat()

    print(f"📊 분석 기간: {start_date} ~ {end_date} ({days}일)\n")

    # API 호출
    try:
        daily = daily_subscriber_changes(start_date, end_date)
        videos = [] if args.no_videos else per_video_subscriber_changes(
            start_date, end_date, max_results=10
        )
    except (OAuthError, AnalyticsError) as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not daily:
        print("⚠️  데이터 없음 (해당 기간 활동이 없거나 API 권한 문제)")
        sys.exit(0)

    # 집계
    total_g = sum(r["gained"] for r in daily)
    total_l = sum(r["lost"] for r in daily)
    net = total_g - total_l

    current_subs = _fetch_current_subscribers()
    starting_subs = (current_subs - net) if current_subs is not None else None
    churn_rate = (total_l / starting_subs * 100) if starting_subs else None
    daily_churn = (churn_rate / days) if churn_rate is not None else None

    # ─── 리포트 작성 ───
    lines: list[str] = [
        "# 구독자 취소율 리포트",
        "",
        f"- **기간**: {start_date} ~ {end_date} ({days}일)",
        f"- **생성일**: {today.isoformat()}",
        f"- **채널**: 마케팅 트루먼쇼",
        "",
        "## 요약",
        "",
        "| 지표 | 값 |",
        "|------|-----|",
        f"| 신규 구독 | **+{total_g:,}** |",
        f"| 구독 취소 | **-{total_l:,}** |",
        f"| 순증 | **{net:+,}** |",
        f"| 일평균 순증 | {net / days:+.1f} |",
    ]
    if churn_rate is not None:
        lines += [
            f"| 시작 구독자 (추정) | {starting_subs:,} |",
            f"| 현재 구독자 | {current_subs:,} |",
            f"| **기간 취소율** | **{churn_rate:.2f}%** |",
            f"| 일평균 취소율 | {daily_churn:.3f}% |",
        ]
    if total_l > 0:
        retention = (1 - total_l / max(total_g, 1)) * 100 if total_g else 0
        lines.append(f"| 유입 대비 유지 효율 | {retention:.0f}% (취소가 신규의 {total_l/max(total_g,1)*100:.0f}%) |")
    lines.append("")

    # 자동 인사이트
    insights: list[str] = []
    if churn_rate is not None:
        if churn_rate >= 2.0:
            insights.append(f"🔴 **취소율 높음** ({churn_rate:.2f}% / {days}일). 최근 영상 톤·주제가 기존 구독자 기대와 어긋나는지 점검 필요.")
        elif churn_rate >= 1.0:
            insights.append(f"🟡 **취소율 보통** ({churn_rate:.2f}% / {days}일). 평균선 — 모니터링 지속.")
        else:
            insights.append(f"🟢 **취소율 낮음** ({churn_rate:.2f}% / {days}일). 구독자 유지력 양호.")
    if total_g > 0:
        ratio = total_l / total_g
        if ratio >= 0.5:
            insights.append(f"⚠️ 신규 1명 대비 취소 {ratio:.2f}명 — 깔때기 누수 큼. 영상별 분석에서 원인 영상 식별.")
        elif ratio <= 0.15:
            insights.append(f"✅ 신규 대비 취소 비율 {ratio:.0%} — 매우 건강한 유입.")
    if insights:
        lines += ["## 자동 인사이트", ""] + [f"- {i}" for i in insights] + [""]

    # 일별 표
    lines += [
        "## 일별 변동",
        "",
        "| 날짜 | 신규 | 취소 | 순증 |",
        "|------|------|------|------|",
    ]
    for r in daily:
        net_d = r["gained"] - r["lost"]
        lines.append(f"| {r['date']} | +{r['gained']} | -{r['lost']} | {net_d:+d} |")
    lines.append("")

    # 영상별
    if videos:
        titles = _fetch_video_titles([v["videoId"] for v in videos])
        lines += [
            "## 영상별 구독 변동 (Top 10, 취소 많은 순)",
            "",
            "| # | 영상 | 신규 | 취소 | 순증 |",
            "|---|------|------|------|------|",
        ]
        for i, v in enumerate(videos, 1):
            raw_title = titles.get(v["videoId"], v["videoId"])
            title = (raw_title[:60] + "…") if len(raw_title) > 60 else raw_title
            net_v = v["gained"] - v["lost"]
            url = f"https://youtu.be/{v['videoId']}"
            lines.append(f"| {i} | [{title}]({url}) | +{v['gained']} | -{v['lost']} | {net_v:+d} |")
        lines.append("")

        # 영상 분석 인사이트
        top_loss = videos[0] if videos else None
        if top_loss and top_loss["lost"] >= 5:
            title = titles.get(top_loss["videoId"], top_loss["videoId"])
            lines += [
                "## 영상 분석 권고",
                "",
                f"🔍 **취소 1위 영상**: [{title}](https://youtu.be/{top_loss['videoId']}) "
                f"— 취소 {top_loss['lost']}명 (신규 {top_loss['gained']}명)",
                "",
                "다음 항목 점검 권장:",
                "- 썸네일/제목과 실제 내용 일치 여부 (낚시성 점검)",
                "- 영상 톤이 채널 평소와 다른지",
                "- 댓글에 '실망' '구독 취소' 키워드가 있는지",
                "",
            ]

    report = "\n".join(lines)

    # 콘솔 출력
    print(report)

    # 파일 저장
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = Path(__file__).parent.parent / "analysis" / "marketing_truman" / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{today.isoformat()}-churn-{days}d.md"
    out.write_text(report, encoding="utf-8")
    print(f"\n💾 저장됨: {out}")


if __name__ == "__main__":
    main()
