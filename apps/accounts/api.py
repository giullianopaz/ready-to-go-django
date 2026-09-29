from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError
from ninja.responses import Response

from .backends import JWTAuth
from .models import User
from .schemas import LoginIn, RefreshTokenIn, RegisterIn, TokenOut, UserOut
from .services import AuthService
from .tasks import send_welcome_email

router = Router(tags=["Authentication & Users"])


@router.post("/auth/register", response={201: TokenOut, 400: dict})
def register(request, payload: RegisterIn):
    """Register a new user account and dispatch a welcome email via PostgreSQL task queue."""
    try:
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
    except IntegrityError:
        raise HttpError(400, "Username or email already in use.") from None

    # Enqueue background task (passes only PK string to broker)
    try:
        send_welcome_email.enqueue(str(user.id))
    except Exception:
        pass  # In local dev if worker not running, non-fatal

    tokens = AuthService.generate_tokens(user)
    return Response(tokens, status=201)


@router.post("/auth/login", response={200: TokenOut, 401: dict})
def login(request, payload: LoginIn):
    """Authenticate with username/email and password to receive JWT tokens."""
    user = AuthService.authenticate_user(payload.username_or_email, payload.password)
    if not user:
        raise HttpError(401, "Invalid username or password.")

    tokens = AuthService.generate_tokens(user)
    return Response(tokens, status=200)


@router.post("/auth/refresh", response={200: TokenOut, 401: dict})
def refresh(request, payload: RefreshTokenIn):
    """Exchange a valid refresh token for a fresh access token."""
    decoded = AuthService.decode_token(payload.refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise HttpError(401, "Invalid or expired refresh token.")

    user_id = decoded.get("sub")
    try:
        user = User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        raise HttpError(401, "User no longer exists or is inactive.") from None

    tokens = AuthService.generate_tokens(user)
    return Response(tokens, status=200)


@router.get("/users/me", response=UserOut, auth=JWTAuth())
def get_me(request):
    """Retrieve profile of currently authenticated user."""
    return request.user
