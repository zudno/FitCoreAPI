from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserRead


class SignUpRequest(BaseModel):
    username: str = Field(min_length=3, description="Mínimo 3 caracteres")
    email: EmailStr
    password: str = Field(min_length=8, description="Mínimo 8 caracteres")


class LoginRequest(BaseModel):
    identity: str = Field(..., description="Email o nombre de usuario")
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenResponse(BaseModel):
    token: Token
    user: UserRead