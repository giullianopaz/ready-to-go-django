from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr, Field

from apps.core.sanitize import SanitizedStr


class RegisterIn(Schema):
    email: EmailStr
    username: SanitizedStr = Field(..., min_length=3, max_length=150)
    password: str = Field(..., min_length=8)
    first_name: SanitizedStr = Field(default="")
    last_name: SanitizedStr = Field(default="")


class LoginIn(Schema):
    username_or_email: str
    password: str


class TokenOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenIn(Schema):
    refresh_token: str


class UserOut(Schema):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
