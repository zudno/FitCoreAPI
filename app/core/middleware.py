from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def register_middlewares(app: FastAPI) -> None:
    """Registra todos los middlewares de la aplicación."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
