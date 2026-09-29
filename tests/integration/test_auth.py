import pytest

from apps.accounts.models import User


@pytest.mark.integration
@pytest.mark.django_db
def test_user_registration(client):
    payload = {
        "username": "newdev",
        "email": "newdev@example.com",
        "password": "SecurePassword123!",
        "first_name": "New",
        "last_name": "Dev",
    }
    response = client.post("/api/v1/auth/register", data=payload, content_type="application/json")
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert User.objects.filter(username="newdev").exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_user_login_success(client, test_user):
    payload = {
        "username_or_email": "testuser",
        "password": "TestPassword123!",
    }
    response = client.post("/api/v1/auth/login", data=payload, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.integration
@pytest.mark.django_db
def test_user_login_invalid_password(client, test_user):
    payload = {
        "username_or_email": "testuser",
        "password": "WrongPassword!",
    }
    response = client.post("/api/v1/auth/login", data=payload, content_type="application/json")
    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.django_db
def test_get_current_user_profile(client, auth_headers):
    response = client.get("/api/v1/users/me", **auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
