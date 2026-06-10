from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- API ---
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "FitCoreAPI"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = (
        "Analiza imágenes de comida y devuelve información nutricional "
        "detallada (calorías, macros e ingredientes) usando Gemini Vision."
    )

    # --- Database ---
    DATABASE_URL: str

    # --- JWT ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # --- Gemini ---
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3-flash-preview"
    GEMINI_TEMPERATURE: float = 0.0

    # --- Google Cloud Storage ---
    GCS_PROJECT_ID: str
    GCS_BUCKET_NAME: str
    GCS_CREDENTIALS_FILE: str

    # --- Firebase ---
    FIREBASE_PROJECT_ID: str = "fitcoreapp-7d1ff"
    FIREBASE_CREDENTIALS_FILE: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()