"""
Admin credentials storage (in-memory, encrypted).

Stores Jira credentials after admin authenticates.
Credentials are encrypted using Fernet symmetric encryption.
Cleared on logout or server restart.
"""

from cryptography.fernet import Fernet

# Generate a fresh encryption key when server starts
# This key lives only in memory and is lost on restart
_encryption_key: bytes = Fernet.generate_key()
_cipher = Fernet(_encryption_key)

# Encrypted credentials storage (None = not authenticated)
_encrypted_username: bytes | None = None
_encrypted_password: bytes | None = None


def admin_set_credentials(username: str, password: str) -> None:
    """Store admin credentials in memory (encrypted)."""
    global _encrypted_username, _encrypted_password
    _encrypted_username = _cipher.encrypt(username.encode())
    _encrypted_password = _cipher.encrypt(password.encode())


def admin_clear_credentials() -> None:
    """Clear admin credentials from memory."""
    global _encrypted_username, _encrypted_password
    _encrypted_username = None
    _encrypted_password = None


def admin_is_authenticated() -> bool:
    """Check if admin has authenticated."""
    return _encrypted_username is not None and _encrypted_password is not None


def admin_get_credentials() -> tuple[str, str] | None:
    """
    Get stored credentials (decrypted).
    Returns (username, password) or None if not authenticated.
    """
    if _encrypted_username is None or _encrypted_password is None:
        return None
    
    decrypted_username = _cipher.decrypt(_encrypted_username).decode()
    decrypted_password = _cipher.decrypt(_encrypted_password).decode()
    
    return (decrypted_username, decrypted_password)
