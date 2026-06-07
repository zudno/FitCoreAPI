from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def init_db() -> None:
    """Crea todas las tablas definidas con SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependencia de FastAPI que provee una sesión de DB por request."""
    with Session(engine) as session:
        yield session
