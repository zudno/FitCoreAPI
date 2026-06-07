from fastapi import HTTPException, status


class InvalidImageError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo debe ser una imagen (image/*).",
        )


class EmptyFileError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo recibido está vacío.",
        )