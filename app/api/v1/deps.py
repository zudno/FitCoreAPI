from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.exceptions import InactiveUserError, InvalidTokenError
from app.core.security import decode_token
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    """
    Extrae y valida el JWT del header Authorization: Bearer <token>.
    Inyectable en cualquier endpoint que requiera autenticación.
    """
    try:
        email = decode_token(credentials.credentials, expected_type="access")
    except JWTError:
        raise InvalidTokenError()

    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise InvalidTokenError()

    if not user.is_active:
        raise InactiveUserError()

    return user