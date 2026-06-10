import time
import requests
from jose import jwt

# Caché para las claves públicas de Google
_certs_cache = {}
_certs_expires_at = 0

def get_firebase_public_keys() -> dict:
    global _certs_cache, _certs_expires_at
    now = time.time()
    if not _certs_cache or now > _certs_expires_at:
        try:
            response = requests.get(
                "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
                timeout=10
            )
            if response.status_code == 200:
                _certs_cache = response.json()
                cache_control = response.headers.get("Cache-Control", "")
                max_age = 3600
                for part in cache_control.split(","):
                    if "max-age" in part:
                        try:
                            max_age = int(part.split("=")[1].strip())
                        except ValueError:
                            pass
                _certs_expires_at = now + max_age
            else:
                raise ValueError("No se pudieron obtener las claves públicas de Firebase")
        except Exception as e:
            if _certs_cache:
                # Si falla la petición pero tenemos caché previa, la seguimos usando
                return _certs_cache
            raise ValueError(f"Error al obtener claves públicas de Firebase: {e}")
    return _certs_cache

def verify_firebase_token(token: str, project_id: str) -> dict:
    """
    Verifica un token de ID de Firebase de forma local usando python-jose.
    Valida firma RS256, expiración, issuer y audience.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise ValueError("Token sin 'kid' en el header")
        
        certs = get_firebase_public_keys()
        if kid not in certs:
            raise ValueError("Clave pública no encontrada para el 'kid' especificado")
        
        cert = certs[kid]
        
        # jose.jwt.decode se encarga de verificar la firma, exp, nbf, iss y aud.
        payload = jwt.decode(
            token,
            cert,
            algorithms=["RS256"],
            audience=project_id,
            issuer=f"https://securetoken.google.com/{project_id}"
        )
        
        if not payload.get("email"):
            raise ValueError("El token de Firebase no contiene correo electrónico")
            
        return payload
    except Exception as e:
        raise ValueError(f"Token de Firebase inválido: {e}")
