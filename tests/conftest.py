"""Test package configuration and shared fixtures."""

import pytest
from django.test import Client

from apps.accounts.models import User


@pytest.fixture
def client():
    """Unauthenticated Django test client."""
    return Client()


@pytest.fixture
def test_user(db):
    """Standard active test user."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="TestPassword123!",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def superuser(db):
    """Administrative superuser."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="SuperPassword123!",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def auth_headers(test_user):
    """Bearer authorization header for API requests."""
    from apps.accounts.services import AuthService

    tokens = AuthService.generate_tokens(test_user)
    return {"HTTP_AUTHORIZATION": f"Bearer {tokens['access_token']}"}
