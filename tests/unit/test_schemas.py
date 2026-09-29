import pytest

from apps.core.schemas import HealthResponse, MessageResponse


@pytest.mark.unit
def test_message_response_schema():
    msg = MessageResponse(message="Success")
    assert msg.message == "Success"


@pytest.mark.unit
def test_health_response_schema():
    health = HealthResponse(status="ok", database=True)
    assert health.status == "ok"
    assert health.database is True
