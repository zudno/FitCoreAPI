from fastapi import HTTPException, status


class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese correo electrónico.",
        )


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está desactivada.",
        )


class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidRefreshTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )