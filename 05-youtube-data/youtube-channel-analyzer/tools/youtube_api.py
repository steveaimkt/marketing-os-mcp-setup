"""
YouTube Data API v3 클라이언트 (requests 기반, 의존성 최소)

사용법:
    from youtube_api import YouTubeClient
    yt = YouTubeClient()  # tools/.env 자동 로드
    channel = yt.find_channel("마케팅 트루먼쇼")
    videos = yt.list_channel_videos(channel["id"])

API 비용 (quota / 일 10,000 한도):
    - search.list:        100 units (채널 검색 한 번)
    - channels.list:      1 unit
    - playlistItems.list: 1 unit (페이지당)
    - videos.list:        1 unit (최대 50개 동시 조회)

전체 채널 분석 (200영상 가정): ~10 units = 일일 한도의 0.1%
"""
from __future__ import annotations

import os
import sys
import time
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError


BASE_URL = "https://www.googleapis.com/youtube/v3"


def _load_env(env_path: Path) -> dict[str, str]:
    """간단한 .env 로더 (외부 의존성 없음)"""
    env: dict[str, str] = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


class YouTubeAPIError(Exception):
    """API 호출 실패"""


class YouTubeClient:
    def __init__(self, api_key: str | None = None, env_path: Path | None = None):
        if env_path is None:
            env_path = Path(__file__).parent / ".env"
        env = _load_env(env_path)
        self.api_key = api_key or env.get("YOUTUBE_API_KEY") or os.environ.get("YOUTUBE_API_KEY")
        if not self.api_key:
            raise YouTubeAPIError(
                f"YOUTUBE_API_KEY가 설정되지 않았습니다. {env_path} 또는 환경변수 확인."
            )
        self._env = env
        self._env_path = env_path
        self.quota_used = 0  # 대략적인 quota 트래킹

    # ────────────────────────────────────────────────────────────────
    # HTTP
    # ────────────────────────────────────────────────────────────────
    def _get(self, endpoint: str, params: dict[str, Any], quota_cost: int = 1) -> dict[str, Any]:
        params = {**params, "key": self.api_key}
        url = f"{BASE_URL}/{endpoint}?{urlencode(params)}"
        req = Request(url, headers={"Accept": "application/json"})
        try:
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            try:
                err_body = json.loads(e.read().decode("utf-8"))
                msg = err_body.get("error", {}).get("message", str(e))
            except Exception:
                msg = str(e)
            raise YouTubeAPIError(f"HTTP {e.code} ({endpoint}): {msg}") from e
        self.quota_used += quota_cost
        return data

    # ────────────────────────────────────────────────────────────────
    # 채널 찾기 / 메타데이터
    # ────────────────────────────────────────────────────────────────
    def find_channel(self, query: str) -> dict[str, Any] | None:
        """채널명/핸들로 검색. 가장 관련도 높은 채널 반환."""
        # 핸들 (@xxx) 또는 채널 ID(UC...)면 검색 스킵하고 직접 조회
        if query.startswith("UC") and len(query) == 24:
            return self.get_channel(channel_id=query)
        if query.startswith("@"):
            return self.get_channel(handle=query)

        data = self._get(
            "search",
            {"part": "snippet", "q": query, "type": "channel", "maxResults": 5},
            quota_cost=100,
        )
        items = data.get("items", [])
        if not items:
            return None
        # 첫 결과의 channelId로 자세한 정보 조회
        channel_id = items[0]["snippet"]["channelId"]
        return self.get_channel(channel_id=channel_id)

    def get_channel(self, channel_id: str | None = None, handle: str | None = None) -> dict[str, Any] | None:
        """채널 ID 또는 핸들(@xxx)로 상세 조회."""
        params = {"part": "snippet,statistics,contentDetails,brandingSettings"}
        if channel_id:
            params["id"] = channel_id
        elif handle:
            params["forHandle"] = handle.lstrip("@")
        else:
            raise ValueError("channel_id 또는 handle 중 하나는 필수")
        data = self._get("channels", params)
        items = data.get("items", [])
        return items[0] if items else None

    # ────────────────────────────────────────────────────────────────
    # 영상 목록
    # ────────────────────────────────────────────────────────────────
    def list_channel_videos(self, channel_id: str, max_videos: int = 500) -> list[dict[str, Any]]:
        """채널의 모든(또는 max_videos 까지) 업로드 영상 반환."""
        channel = self.get_channel(channel_id=channel_id)
        if not channel:
            raise YouTubeAPIError(f"채널을 찾을 수 없습니다: {channel_id}")
        uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]

        video_ids: list[str] = []
        page_token: str | None = None
        while True:
            params: dict[str, Any] = {
                "part": "contentDetails",
                "playlistId": uploads_playlist,
                "maxResults": 50,
            }
            if page_token:
                params["pageToken"] = page_token
            data = self._get("playlistItems", params)
            for item in data.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])
                if len(video_ids) >= max_videos:
                    break
            page_token = data.get("nextPageToken")
            if not page_token or len(video_ids) >= max_videos:
                break

        # 50개씩 묶어서 영상 상세 조회
        videos: list[dict[str, Any]] = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i : i + 50]
            data = self._get(
                "videos",
                {"part": "snippet,statistics,contentDetails", "id": ",".join(batch)},
            )
            videos.extend(data.get("items", []))
        return videos

    # ────────────────────────────────────────────────────────────────
    # 댓글 (선택)
    # ────────────────────────────────────────────────────────────────
    def list_video_comments(self, video_id: str, max_comments: int = 100) -> list[dict[str, Any]]:
        """영상의 top-level 댓글 (relevance 순)."""
        comments: list[dict[str, Any]] = []
        page_token: str | None = None
        while len(comments) < max_comments:
            params: dict[str, Any] = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": min(100, max_comments - len(comments)),
                "order": "relevance",
                "textFormat": "plainText",
            }
            if page_token:
                params["pageToken"] = page_token
            try:
                data = self._get("commentThreads", params)
            except YouTubeAPIError as e:
                # 댓글 비활성화 영상 등 — 조용히 스킵
                if "disabled" in str(e).lower() or "forbidden" in str(e).lower():
                    return comments
                raise
            for item in data.get("items", []):
                top = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(
                    {
                        "text": top.get("textDisplay", ""),
                        "author": top.get("authorDisplayName", ""),
                        "likes": top.get("likeCount", 0),
                        "publishedAt": top.get("publishedAt", ""),
                    }
                )
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        return comments[:max_comments]

    # ────────────────────────────────────────────────────────────────
    # .env 업데이트 (채널 ID 캐시)
    # ────────────────────────────────────────────────────────────────
    def save_channel_id(self, channel_id: str) -> None:
        """tools/.env의 YOUTUBE_CHANNEL_ID 값을 업데이트."""
        if not self._env_path.exists():
            return
        lines = self._env_path.read_text(encoding="utf-8").splitlines()
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("YOUTUBE_CHANNEL_ID="):
                lines[i] = f"YOUTUBE_CHANNEL_ID={channel_id}"
                updated = True
                break
        if not updated:
            lines.append(f"YOUTUBE_CHANNEL_ID={channel_id}")
        self._env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    # 간단한 self-test
    yt = YouTubeClient()
    query = sys.argv[1] if len(sys.argv) > 1 else "마케팅 트루먼쇼"
    print(f"[INFO] 채널 검색: '{query}'")
    channel = yt.find_channel(query)
    if not channel:
        print(f"[ERROR] 채널을 찾을 수 없습니다.")
        sys.exit(1)
    snippet = channel["snippet"]
    stats = channel["statistics"]
    print(f"  채널명     : {snippet['title']}")
    print(f"  채널 ID    : {channel['id']}")
    print(f"  핸들       : {snippet.get('customUrl', '(없음)')}")
    print(f"  구독자     : {int(stats.get('subscriberCount', 0)):,}")
    print(f"  영상 수    : {int(stats.get('videoCount', 0)):,}")
    print(f"  총 조회수  : {int(stats.get('viewCount', 0)):,}")
    print(f"  생성일     : {snippet.get('publishedAt', '')[:10]}")
    print(f"  설명       : {snippet.get('description', '')[:120]}...")
    print(f"\nQuota 사용  : ~{yt.quota_used} units")
