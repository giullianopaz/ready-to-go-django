import pytest


@pytest.mark.integration
@pytest.mark.django_db
def test_health_check_endpoint(client):
    response = client.get("/up")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] is True
