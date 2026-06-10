import logging

import firebase_admin
from firebase_admin import auth

logger = logging.getLogger(__name__)


def initialize_firebase(project_id: str) -> None:
    if firebase_admin._apps:
        return
    firebase_admin.initialize_app(options={"projectId": project_id})
    logger.info("Firebase Admin inicializado con project_id: %s", project_id)


def verify_firebase_token(token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=60)

        if not decoded_token.get("email"):
            raise ValueError("El token de Firebase no contiene correo electrónico")

        if not decoded_token.get("email_verified"):
            raise ValueError("El correo electrónico del token de Firebase no está verificado")

        return decoded_token
    except Exception as e:
        raise ValueError(f"Token de Firebase inválido: {e}")
