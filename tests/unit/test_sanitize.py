import pytest

from apps.core.sanitize import sanitize_text


@pytest.mark.unit
def test_sanitize_strips_malicious_script():
    dirty = '<script>alert("pwned")</script>Hello World'
    clean = sanitize_text(dirty)
    assert "<script>" not in clean
    assert "alert" not in clean
    assert "Hello World" in clean


@pytest.mark.unit
def test_sanitize_preserves_safe_html():
    safe = "<p>Welcome <strong>user</strong>!</p>"
    clean = sanitize_text(safe)
    assert clean == safe


@pytest.mark.unit
def test_sanitize_handles_none_and_empty():
    assert sanitize_text(None) == ""
    assert sanitize_text("") == ""
