import base64
import hashlib

from cryptography.fernet import Fernet

from app.core.config import settings


def _get_fernet() -> Fernet:
    if settings.encryption_key:
        key = settings.encryption_key.encode()
    else:
        key = base64.urlsafe_b64encode(hashlib.sha256(settings.secret_key.encode()).digest())
    return Fernet(key)


def encrypt_text(value: str) -> str:
    return _get_fernet().encrypt(value.encode()).decode()


def decrypt_text(value: str) -> str:
    return _get_fernet().decrypt(value.encode()).decode()


def get_phone_hash(phone: str) -> str:
    """Returns a deterministic SHA-256 hash of the phone number seeded with the secret key."""
    salted = f"{settings.secret_key}:{phone}"
    return hashlib.sha256(salted.encode()).hexdigest()
