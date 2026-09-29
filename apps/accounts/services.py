from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import authenticate

from .models import User


class AuthService:
    """Authentication and JWT lifecycle service."""

    @staticmethod
    def create_token(payload: dict[str, Any], expires_delta: timedelta) -> str:
        to_encode = payload.copy()
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

    @classmethod
    def generate_tokens(cls, user: User) -> dict[str, Any]:
        access_delta = timedelta(minutes=settings.JWT_ACCESS_MINUTES)
        refresh_delta = timedelta(days=settings.JWT_REFRESH_DAYS)

        access_payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "type": "access",
        }
        refresh_payload = {
            "sub": str(user.id),
            "type": "refresh",
        }

        access_token = cls.create_token(access_payload, access_delta)
        refresh_token = cls.create_token(refresh_payload, refresh_delta)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": int(access_delta.total_seconds()),
        }

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            return {}

    @classmethod
    def authenticate_user(cls, username_or_email: str, password: str) -> User | None:
        user = None
        # Check by email first
        if "@" in username_or_email:
            try:
                candidate = User.objects.get(email=username_or_email)
                if candidate.check_password(password):
                    user = candidate
            except User.DoesNotExist:
                pass

        if not user:
            user = authenticate(username=username_or_email, password=password)

        if user and user.is_active:
            return user
        return None
