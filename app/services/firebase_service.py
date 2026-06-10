import firebase_admin
from firebase_admin import auth
from app.core.config import settings

# Variable para controlar el estado de inicialización
_firebase_initialized = False

def initialize_firebase():
    """
    Inicializa el SDK de Firebase Admin de manera segura
    utilizando el ID del proyecto configurado.
    """
    global _firebase_initialized
    if _firebase_initialized or firebase_admin._apps:
        _firebase_initialized = True
        return

    try:
        firebase_admin.initialize_app(options={'projectId': settings.FIREBASE_PROJECT_ID})
        _firebase_initialized = True
        print(f"Firebase Admin inicializado con project_id: {settings.FIREBASE_PROJECT_ID}")
    except Exception as e:
        print(f"Error al inicializar Firebase Admin: {e}")


def verify_firebase_token(token: str, project_id: str) -> dict:
    """
    Verifica la validez de un token de ID de Firebase usando el SDK oficial.
    Retorna los reclamos decodificados o lanza ValueError si el token no es válido.
    """
    try:
        initialize_firebase()
        
        # Validación del token con tolerancia para desfases de reloj locales (clock skew)
        decoded_token = auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=60)
        
        if not decoded_token.get("email"):
            raise ValueError("El token de Firebase no contiene correo electrónico")
            
        return decoded_token
    except Exception as e:
        raise ValueError(f"Token de Firebase inválido: {e}")
