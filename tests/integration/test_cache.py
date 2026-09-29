import pytest
from django.core.cache import cache


@pytest.mark.integration
def test_cache_set_and_get():
    cache.set("test_key", {"status": "ok", "value": 42}, timeout=60)
    data = cache.get("test_key")
    assert data is not None
    assert data["status"] == "ok"
    assert data["value"] == 42


@pytest.mark.integration
def test_cache_delete():
    cache.set("temp_key", "temporary", timeout=60)
    assert cache.get("temp_key") == "temporary"
    cache.delete("temp_key")
    assert cache.get("temp_key") is None
