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


class MuscleGroupAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un grupo muscular con este nombre.",
        )


class ExerciseAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya has creado un ejercicio personalizado con este nombre.",
        )


class InvalidGifError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo debe ser un GIF (image/gif).",
        )
