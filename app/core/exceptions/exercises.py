from fastapi import HTTPException, status


class MuscleGroupNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo muscular no encontrado.",
        )


class ExerciseNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado.",
        )


class ExerciseAccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar o eliminar este ejercicio.",
        )
