from fastapi import HTTPException, status


class WorkoutSessionNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión de entrenamiento no encontrada.",
        )


class WorkoutSessionAlreadyEndedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta sesión de entrenamiento ya ha finalizado y no se puede modificar.",
        )


class WorkoutSetNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serie de entrenamiento no encontrada.",
        )
