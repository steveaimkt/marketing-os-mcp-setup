"""
YouTube OAuth 2.0 클라이언트 (stdlib만 사용, 외부 의존성 없음)

사용법:
    # 최초 1회 인증 (브라우저 오픈 → 권한 승인 → refresh_token 자동 .env 저장)
    python3 tools/youtube_oauth.py --auth

    # 다른 모듈에서 access_token 얻기
    from youtube_oauth import get_access_token
    token = get_access_token()  # 1시간 캐싱, 자동 갱신

스코프: yt-analytics.readonly (YouTube Analytics API 읽기 전용)
"""
from __future__ import annotations

import sys
import json
import time
import webbrowser
import secrets
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import HTTPServer, BaseHTTPRequestHandler


SCOPES = "https://www.googleapis.com/auth/yt-analytics.readonly"
REDIRECT_URI = "http://localhost:8765"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


class OAuthError(Exception):
    """OAuth 인증/토큰 처리 실패"""


# ────────────────────────────────────────────────────────────────
# .env 입출력
# ────────────────────────────────────────────────────────────────
def _env_path() -> Path:
    return Path(__file__).parent / ".env"


def _load_env(env_path: Path) -> dict[str, str]:
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


def _save_env_value(env_path: Path, key: str, value: str) -> None:
    if not env_path.exists():
        env_path.write_text(f"{key}={value}\n", encoding="utf-8")
        return
    lines = env_path.read_text(encoding="utf-8").splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break
    if not updated:
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _credentials() -> tuple[str, str]:
    env = _load_env(_env_path())
    cid = env.get("YOUTUBE_OAUTH_CLIENT_ID", "").strip()
    sec = env.get("YOUTUBE_OAUTH_CLIENT_SECRET", "").strip()
    if not cid or not sec:
        raise OAuthError(
            "YOUTUBE_OAUTH_CLIENT_ID / YOUTUBE_OAUTH_CLIENT_SECRET 가 .env에 없습니다.\n"
            ".claude/skills/yt-analyze/oauth-setup.md STEP 1~4 먼저 완료하세요."
        )
    return cid, sec


# ────────────────────────────────────────────────────────────────
# 로컬 콜백 서버 (localhost:8765)
# ────────────────────────────────────────────────────────────────
class _CallbackHandler(BaseHTTPRequestHandler):
    received_code: str | None = None
    received_state: str | None = None
    received_error: str | None = None

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        _CallbackHandler.received_code = (params.get("code") or [None])[0]
        _CallbackHandler.received_state = (params.get("state") or [None])[0]
        _CallbackHandler.received_error = (params.get("error") or [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if _CallbackHandler.received_code:
            html = (
                "<html><body style='font-family:sans-serif;text-align:center;padding:60px;background:#f7f7f7;'>"
                "<h1 style='color:#2ecc71;'>✅ 인증 완료</h1>"
                "<p>이 창은 닫아도 됩니다. 터미널로 돌아가세요.</p>"
                "</body></html>"
            )
        else:
            err = _CallbackHandler.received_error or "알 수 없는 오류"
            html = (
                "<html><body style='font-family:sans-serif;text-align:center;padding:60px;'>"
                f"<h1 style='color:#e74c3c;'>❌ 인증 실패</h1><p>{err}</p>"
                "</body></html>"
            )
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):  # noqa: A002
        pass  # 콘솔 스팸 방지


def _wait_for_callback(timeout: int = 180) -> None:
    server = HTTPServer(("localhost", 8765), _CallbackHandler)
    server.timeout = timeout
    server.handle_request()


# ────────────────────────────────────────────────────────────────
# OAuth 인증 플로우 (최초 1회)
# ────────────────────────────────────────────────────────────────
def run_auth_flow() -> str:
    """브라우저 OAuth flow 실행 → refresh_token 발급 + .env 저장 → 반환"""
    client_id, client_secret = _credentials()
    state = secrets.token_urlsafe(16)

    auth_params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",   # refresh_token 발급
        "prompt": "consent",        # 매번 권한 다시 묻기 → refresh_token 보장
        "state": state,
    }
    url = f"{AUTH_URL}?{urlencode(auth_params)}"

    print("\n🌐 브라우저를 엽니다. Google 계정 로그인 + 권한을 승인하세요.")
    print(f"\n자동으로 안 열리면 이 URL을 복사해 브라우저에 붙여넣으세요:\n  {url}\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    print("⏳ localhost:8765 콜백 대기 중 (최대 3분)...")
    _wait_for_callback()

    if _CallbackHandler.received_error:
        raise OAuthError(f"Google 측 인증 거부: {_CallbackHandler.received_error}")
    code = _CallbackHandler.received_code
    if not code:
        raise OAuthError("타임아웃 또는 코드 미수신")
    if _CallbackHandler.received_state != state:
        raise OAuthError("CSRF state 불일치 — 보안 검증 실패")

    # code → tokens 교환
    body = urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode("utf-8")
    req = Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urlopen(req, timeout=30) as resp:
            tokens = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise OAuthError(f"토큰 교환 실패 (HTTP {e.code}): {detail}")

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise OAuthError(
            "응답에 refresh_token이 없습니다. "
            "기존 인증을 https://myaccount.google.com/permissions 에서 취소 후 재시도하세요."
        )
    _save_env_value(_env_path(), "YOUTUBE_REFRESH_TOKEN", refresh_token)
    print(f"\n✅ Refresh token saved to {_env_path()}")
    print(f"   access_token (1시간 유효): {tokens['access_token'][:24]}...")
    return refresh_token


# ────────────────────────────────────────────────────────────────
# access_token 발급/갱신 (외부 모듈이 호출)
# ────────────────────────────────────────────────────────────────
_cached_token: str | None = None
_cached_expires_at: float = 0.0


def get_access_token(force_refresh: bool = False) -> str:
    """refresh_token으로 access_token 발급. 50분 캐싱."""
    global _cached_token, _cached_expires_at
    if not force_refresh and _cached_token and time.time() < _cached_expires_at:
        return _cached_token

    env = _load_env(_env_path())
    refresh_token = env.get("YOUTUBE_REFRESH_TOKEN", "").strip()
    if not refresh_token:
        raise OAuthError(
            "YOUTUBE_REFRESH_TOKEN이 비어있습니다.\n"
            "먼저 인증하세요: python3 tools/youtube_oauth.py --auth"
        )
    client_id, client_secret = _credentials()
    body = urlencode({
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise OAuthError(
            f"access_token 갱신 실패 (HTTP {e.code}): {detail}\n"
            "refresh_token이 만료/취소되었을 수 있습니다. `--auth` 재실행 필요."
        )
    _cached_token = data["access_token"]
    _cached_expires_at = time.time() + data.get("expires_in", 3600) - 600  # 10분 여유
    return _cached_token


if __name__ == "__main__":
    if "--auth" in sys.argv:
        try:
            run_auth_flow()
        except OAuthError as e:
            print(f"\n❌ 인증 실패: {e}")
            sys.exit(1)
    else:
        # 동작 확인: 캐시된 refresh_token으로 access_token 얻을 수 있는지
        try:
            token = get_access_token()
            print(f"✅ access_token OK (앞 24자): {token[:24]}...")
        except OAuthError as e:
            print(f"❌ {e}")
            sys.exit(1)
