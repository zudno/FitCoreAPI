from fastapi import FastAPI

import app.models  # noqa: F401 — registra todos los modelos en SQLModel metadata
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import init_db
from app.core.middleware import register_middlewares
from app.services.firebase_service import initialize_firebase


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    init_db()
    initialize_firebase(settings.FIREBASE_PROJECT_ID)
    register_middlewares(app)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["Health"])
    def root():
        return {"status": "ok", "version": settings.PROJECT_VERSION}

    return app


app = create_app()