from fastapi import HTTPException, status


class WorkoutProgramNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa de entrenamiento no encontrado o acceso denegado.",
        )
