from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": subject,
        "exp": expire,
        "type": token_type,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: str) -> str:
    return _create_token(
        subject=subject,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: str) -> str:
    return _create_token(
        subject=subject,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str, expected_type: str) -> str:
    """
    Decodifica y valida un JWT. Devuelve el 'sub' (email del usuario).
    Lanza JWTError si el token es inválido, expirado o del tipo incorrecto.
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    token_type: str | None = payload.get("type")
    if token_type != expected_type:
        raise JWTError(f"Token type mismatch: expected '{expected_type}', got '{token_type}'")

    subject: str | None = payload.get("sub")
    if subject is None:
        raise JWTError("Token missing 'sub' claim")

    return subject
