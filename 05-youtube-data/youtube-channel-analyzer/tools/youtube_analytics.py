"""
YouTube Analytics API v2 클라이언트 (stdlib + youtube_oauth.py만 사용)

채널 소유자 권한으로만 접근 가능한 데이터:
  - subscribersGained / subscribersLost (취소율 계산)
  - estimatedMinutesWatched / averageViewDuration
  - 트래픽 소스, 시청 유지 곡선 등

사용법:
    from youtube_analytics import daily_subscriber_changes
    rows = daily_subscriber_changes("2026-05-18", "2026-05-25")
"""
from __future__ import annotations

import sys
import json
from datetime import date, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from youtube_oauth import get_access_token


BASE_URL = "https://youtubeanalytics.googleapis.com/v2/reports"


class AnalyticsError(Exception):
    """Analytics API 호출 실패"""


def _query(params: dict, _retried: bool = False) -> dict:
    token = get_access_token()
    url = f"{BASE_URL}?{urlencode(params)}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        # 401 → access_token 만료 → 강제 갱신 후 1회 재시도
        if e.code == 401 and not _retried:
            get_access_token(force_refresh=True)
            return _query(params, _retried=True)
        detail = e.read().decode("utf-8", errors="ignore")
        raise AnalyticsError(f"HTTP {e.code}: {detail}")


# ────────────────────────────────────────────────────────────────
# 구독 변동
# ────────────────────────────────────────────────────────────────
def daily_subscriber_changes(
    start_date: str,
    end_date: str,
    channel: str = "MINE",
) -> list[dict]:
    """일별 신규/취소 구독자.

    Returns:
        [{"date": "2026-05-18", "gained": 45, "lost": 12}, ...]
    """
    data = _query({
        "ids": f"channel=={channel}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "subscribersGained,subscribersLost",
        "dimensions": "day",
        "sort": "day",
    })
    rows = data.get("rows") or []
    return [{"date": r[0], "gained": int(r[1]), "lost": int(r[2])} for r in rows]


def per_video_subscriber_changes(
    start_date: str,
    end_date: str,
    channel: str = "MINE",
    max_results: int = 20,
) -> list[dict]:
    """영상별 구독 변동 (취소 많은 순).

    Returns:
        [{"videoId": "abc", "gained": 10, "lost": 18}, ...]
    """
    data = _query({
        "ids": f"channel=={channel}",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "subscribersGained,subscribersLost",
        "dimensions": "video",
        "sort": "-subscribersLost",
        "maxResults": max_results,
    })
    rows = data.get("rows") or []
    return [{"videoId": r[0], "gained": int(r[1]), "lost": int(r[2])} for r in rows]


# ────────────────────────────────────────────────────────────────
# CLI 셀프 테스트
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    today = date.today()
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    start = (today - timedelta(days=days)).isoformat()
    end = today.isoformat()
    print(f"\n📊 일별 구독 변동 ({start} ~ {end}, {days}일)\n")
    try:
        rows = daily_subscriber_changes(start, end)
    except AnalyticsError as e:
        print(f"❌ {e}")
        sys.exit(1)
    if not rows:
        print("  (데이터 없음)")
        sys.exit(0)
    total_g, total_l = 0, 0
    for r in rows:
        net = r["gained"] - r["lost"]
        total_g += r["gained"]
        total_l += r["lost"]
        print(f"  {r['date']}  신규 +{r['gained']:3}  취소 -{r['lost']:3}  순증 {net:+d}")
    print(f"\n  합계        신규 +{total_g}  취소 -{total_l}  순증 {total_g - total_l:+d}")
