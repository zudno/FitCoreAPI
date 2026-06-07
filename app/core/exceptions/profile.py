from fastapi import HTTPException, status


class ProfileNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario aún no ha completado su perfil de onboarding.",
        )
