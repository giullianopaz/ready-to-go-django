from ninja.security import HttpBearer

from .models import User
from .services import AuthService


class JWTAuth(HttpBearer):
    """Bearer token authentication for django-ninja endpoints."""

    def authenticate(self, request, token: str) -> User | None:
        payload = AuthService.decode_token(token)
        if not payload or payload.get("type") != "access":
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        try:
            user = User.objects.get(id=user_id, is_active=True)
            request.user = user
            return user
        except User.DoesNotExist:
            return None
