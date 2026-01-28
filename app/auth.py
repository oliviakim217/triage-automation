"""
Authentication with bcrypt password hashing.
"""

import bcrypt

from app.config import AUTH_USERNAME, AUTH_PASSWORD_HASH


def auth_verify_credentials(username: str, password: str) -> bool:
    """Verify username and password. Returns True if valid."""
    username_normalized = username.lower().strip()
    if username_normalized != AUTH_USERNAME.lower():
        return False
    try:
        password_bytes = password.encode()
        hash_bytes = AUTH_PASSWORD_HASH.encode()
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except (ValueError, TypeError):
        return False
