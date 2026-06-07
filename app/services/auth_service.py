from fastapi import HTTPException, status
from jose import JWTError
from sqlmodel import Session, select, or_

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
from app.models.user import User
from app.schemas.auth import SignUpRequest, TokenResponse


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
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
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
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )
