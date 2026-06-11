from jose import JWTError
from sqlmodel import Session, select, or_
import uuid
import random

from app.core.config import settings
from app.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UserAlreadyExistsError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.enums import AuthProvider
from app.models.user import User
from app.schemas.auth import SignUpRequest, Token, TokenResponse
from app.services.firebase_service import verify_firebase_token


def create_user(payload: SignUpRequest, session: Session) -> User:
    # Chequear si existe el email o el username
    existing = session.exec(
        select(User).where(or_(User.email == payload.email, User.username == payload.username))
    ).first()
    
    if existing:
        raise UserAlreadyExistsError()

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(identity: str, password: str, session: Session) -> TokenResponse:
    # Buscar por email O por username
    user = session.exec(
        select(User).where(or_(User.email == identity, User.username == identity))
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveUserError()

    return TokenResponse(
        token=Token(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
        user=user,
    )


def refresh_access_token(refresh_token: str, session: Session) -> TokenResponse:
    try:
        email = decode_token(refresh_token, expected_type="refresh")
    except JWTError:
        raise InvalidRefreshTokenError()

    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not user.is_active:
        raise InvalidCredentialsError()

    return TokenResponse(
        token=Token(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
        user=user,
    )


def authenticate_google_user(id_token: str, session: Session) -> TokenResponse:
    # 1. Verificar el token de Firebase
    try:
        payload = verify_firebase_token(id_token)
    except ValueError:
        raise InvalidCredentialsError()

    email = payload["email"]
    picture: str | None = payload.get("picture")

    # 2. Buscar si existe el usuario
    user = session.exec(select(User).where(User.email == email)).first()

    # 3. Si no existe, crear un nuevo usuario
    if not user:
        base_username = email.split("@")[0]
        base_username = "".join(c for c in base_username if c.isalnum() or c in ("_", ".")).lower()
        if not base_username:
            base_username = "user"

        username = base_username
        while True:
            existing = session.exec(select(User).where(User.username == username)).first()
            if not existing:
                break
            username = f"{base_username}{random.randint(1000, 9999)}"

        dummy_password = uuid.uuid4().hex + uuid.uuid4().hex
        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(dummy_password),
            auth_provider=AuthProvider.GOOGLE,
            avatar_url=picture,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    elif user.avatar_url != picture:
        # Refrescar avatar en cada login por si el usuario cambió su foto en Google
        user.avatar_url = picture
        session.add(user)
        session.commit()
        session.refresh(user)

    if not user.is_active:
        raise InactiveUserError()

    return TokenResponse(
        token=Token(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
        user=user,
    )
