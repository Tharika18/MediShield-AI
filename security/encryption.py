from cryptography.fernet import Fernet
from flask import current_app


def _fernet():
    key = current_app.config.get("ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("ENCRYPTION_KEY not configured")
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_field(plaintext: str | None) -> str | None:
    if not plaintext:
        return None
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_field(ciphertext: str | None) -> str | None:
    if not ciphertext:
        return None
    return _fernet().decrypt(ciphertext.encode()).decode()


def mask(value: str | None, visible: int = 2) -> str:
    """Mask a sensitive string showing only the last `visible` characters."""
    if not value:
        return "—"
    value = str(value)
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]