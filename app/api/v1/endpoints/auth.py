from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.auth import LoginRequest, SignUpRequest, TokenRefreshRequest, TokenResponse
from app.services.auth_service import authenticate_user, create_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
)
def signup(payload: SignUpRequest, session: Session = Depends(get_session)) -> TokenResponse:
    user = create_user(payload, session)
    return authenticate_user(user.email, payload.password, session)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    return authenticate_user(payload.identity, payload.password, session)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Renovar access token",
)
def refresh(payload: TokenRefreshRequest, session: Session = Depends(get_session)) -> TokenResponse:
    return refresh_access_token(payload.refresh_token, session)
