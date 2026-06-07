import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# Formato estándar de error                                                    #
# --------------------------------------------------------------------------- #

def _error_response(status_code: int, message: str, detail: object = None) -> JSONResponse:
    content = {"success": False, "message": message}
    if detail is not None:
        content["detail"] = detail
    return JSONResponse(status_code=status_code, content=content)


# --------------------------------------------------------------------------- #
# Handlers                                                                     #
# --------------------------------------------------------------------------- #

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    field_errors = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        msg = _translate_validation_error(error["type"], error.get("ctx", {}))
        field_errors.append({"field": field, "message": msg})

    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Los datos enviados no son válidos.",
        detail=field_errors,
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    logger.warning("IntegrityError: %s", exc.orig)
    return _error_response(
        status_code=status.HTTP_409_CONFLICT,
        message="Ya existe un registro con esos datos.",
    )


async def operational_error_handler(request: Request, exc: OperationalError) -> JSONResponse:
    logger.error("OperationalError (DB): %s", exc.orig)
    return _error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message="No se pudo conectar a la base de datos. Intenta más tarde.",
    )


async def gemini_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Gemini API error: %s", exc)
    message = "Error al comunicarse con el servicio de análisis de imágenes."

    exc_str = str(exc).lower()
    if "quota" in exc_str or "resource_exhausted" in exc_str:
        message = "Se agotó la cuota de la API de análisis. Intenta más tarde."
    elif "timeout" in exc_str or "deadline" in exc_str:
        message = "El servicio de análisis tardó demasiado. Intenta de nuevo."

    return _error_response(
        status_code=status.HTTP_502_BAD_GATEWAY,
        message=message,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Ocurrió un error interno. Por favor intenta más tarde.",
    )


# --------------------------------------------------------------------------- #
# Traducción de errores de validación                                          #
# --------------------------------------------------------------------------- #

def _translate_validation_error(error_type: str, ctx: dict) -> str:
    translations = {
        "missing": "Este campo es requerido.",
        "string_too_short": f"Debe tener al menos {ctx.get('min_length', '?')} caracteres.",
        "string_too_long": f"No puede tener más de {ctx.get('max_length', '?')} caracteres.",
        "value_error": "Valor inválido.",
        "type_error": "Tipo de dato incorrecto.",
        "int_parsing": "Debe ser un número entero.",
        "float_parsing": "Debe ser un número.",
        "bool_parsing": "Debe ser verdadero o falso.",
        "value_error.email": "El correo electrónico no es válido.",
        "string_pattern_mismatch": "El formato no es válido.",
        "greater_than": f"Debe ser mayor a {ctx.get('gt', '?')}.",
        "greater_than_equal": f"Debe ser mayor o igual a {ctx.get('ge', '?')}.",
        "less_than": f"Debe ser menor a {ctx.get('lt', '?')}.",
        "less_than_equal": f"Debe ser menor o igual a {ctx.get('le', '?')}.",
        "enum": f"Valores permitidos: {ctx.get('expected', '?')}.",
    }
    return translations.get(error_type, "Valor inválido.")


# --------------------------------------------------------------------------- #
# Registro en la app                                                           #
# --------------------------------------------------------------------------- #

def register_exception_handlers(app: FastAPI) -> None:
    from google.api_core.exceptions import GoogleAPIError

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(OperationalError, operational_error_handler)
    app.add_exception_handler(GoogleAPIError, gemini_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)