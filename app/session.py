"""
Session management with signed cookies.
"""

from itsdangerous import URLSafeTimedSerializer, BadSignature
from starlette.requests import Request
from starlette.responses import Response

from app.config import (
    SESSION_SECRET_KEY,
    SESSION_COOKIE_NAME,
    SESSION_MAX_AGE_SECONDS,
)

_serializer = URLSafeTimedSerializer(SESSION_SECRET_KEY)


def session_is_logged_in(request: Request) -> bool:
    """Check if user has valid session."""
    cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if not cookie:
        return False
    try:
        _serializer.loads(cookie, max_age=SESSION_MAX_AGE_SECONDS)
        return True
    except BadSignature:
        return False


def session_set_logged_in(response: Response) -> None:
    """Set session cookie."""
    response.set_cookie(
        SESSION_COOKIE_NAME,
        _serializer.dumps({"logged_in": True}),
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
    )


def session_clear(response: Response) -> None:
    """Clear session cookie."""
    response.delete_cookie(SESSION_COOKIE_NAME)
