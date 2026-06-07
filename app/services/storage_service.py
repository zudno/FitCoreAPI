import uuid
from pathlib import Path
from fastapi import UploadFile
from google.cloud import storage
from app.core.config import settings

class CloudStorageService:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            settings.GCS_CREDENTIALS_FILE,
            project=settings.GCS_PROJECT_ID
        )
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)

    async def upload_avatar(self, file: UploadFile, user_id: str) -> str:
        """
        Sube un avatar al bucket de GCS y devuelve la URL pública.
        """
        # Obtener extensión del archivo original
        extension = Path(file.filename).suffix
        # Crear un nombre único: avatars/{user_id}/{random_uuid}{extension}
        file_path = f"avatars/{user_id}/{uuid.uuid4()}{extension}"
        
        blob = self.bucket.blob(file_path)
        
        # Leer contenido y subir
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)
        
        return blob.public_url

    async def upload_meal_image(self, image_bytes: bytes, mime_type: str, user_id: str) -> str:
        """
        Sube una imagen de comida al bucket de GCS y devuelve la URL pública.
        """
        # Determinar extensión basada en mime_type
        extension = ".jpg"
        if "png" in mime_type: extension = ".png"
        elif "webp" in mime_type: extension = ".webp"
        
        file_path = f"meals/{user_id}/{uuid.uuid4()}{extension}"
        blob = self.bucket.blob(file_path)
        
        blob.upload_from_string(image_bytes, content_type=mime_type)
        
        return blob.public_url

    async def upload_exercise_image(self, file: UploadFile, exercise_id: str) -> str:
        """
        Sube una imagen de ejercicio al bucket de GCS y devuelve la URL pública.
        Ruta: exercises/{exercise_id}/image/{uuid}{extension}
        """
        extension = Path(file.filename).suffix.lower() or ".jpg"
        file_path = f"exercises/{exercise_id}/image/{uuid.uuid4()}{extension}"

        blob = self.bucket.blob(file_path)
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)

        return blob.public_url

    async def upload_program_image(self, file: UploadFile, program_id: str) -> str:
        """
        Sube una imagen de programa al bucket de GCS y devuelve la URL pública.
        Ruta: programs/{program_id}/image/{uuid}{extension}
        """
        extension = Path(file.filename).suffix.lower() or ".jpg"
        file_path = f"programs/{program_id}/image/{uuid.uuid4()}{extension}"

        blob = self.bucket.blob(file_path)
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)

        return blob.public_url

    def delete_program_image(self, image_url: str) -> None:
        """
        Borra la imagen de un programa de GCS dado su URL pública.
        """
        try:
            prefix = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/"
            if image_url.startswith(prefix):
                blob_path = image_url.replace(prefix, "")
                blob = self.bucket.blob(blob_path)
                blob.delete()
        except Exception as e:
            print(f"Error al borrar imagen de programa en GCS: {e}")

    async def upload_exercise_gif(self, file: UploadFile, exercise_id: str) -> str:
        """
        Sube un GIF de ejercicio al bucket de GCS y devuelve la URL pública.
        Ruta: exercises/{exercise_id}/gif/{uuid}.gif
        """
        file_path = f"exercises/{exercise_id}/gif/{uuid.uuid4()}.gif"

        blob = self.bucket.blob(file_path)
        content = await file.read()
        blob.upload_from_string(content, content_type="image/gif")

        return blob.public_url

    def delete_exercise_media(self, media_url: str) -> None:
        """
        Borra una imagen o video de ejercicio de GCS dado su URL pública.
        """
        try:
            prefix = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/"
            if media_url.startswith(prefix):
                blob_path = media_url.replace(prefix, "")
                blob = self.bucket.blob(blob_path)
                blob.delete()
        except Exception as e:
            print(f"Error al borrar media de ejercicio en GCS: {e}")

    def delete_old_avatar(self, avatar_url: str):
        """
        (Opcional) Borra el avatar antiguo de GCS si es necesario.
        """
        try:
            # Extraer el path relativo desde la URL pública
            # https://storage.googleapis.com/bucket-name/avatars/user_id/uuid.png
            prefix = f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/"
            if avatar_url.startswith(prefix):
                blob_path = avatar_url.replace(prefix, "")
                blob = self.bucket.blob(blob_path)
                blob.delete()
        except Exception as e:
            print(f"Error al borrar avatar de GCS: {e}")

# Instancia única para ser usada en los endpoints
storage_service = CloudStorageService()
