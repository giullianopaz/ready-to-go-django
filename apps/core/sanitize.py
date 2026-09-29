from typing import Annotated

import nh3
from pydantic import BeforeValidator

ALLOWED_TAGS = {"b", "i", "strong", "em", "p", "br", "ul", "ol", "li", "span", "code"}


def sanitize_text(value: str | None) -> str:
    """Sanitize HTML string using Rust-powered nh3."""
    if not value:
        return ""
    return nh3.clean(value, tags=ALLOWED_TAGS)


# Pydantic type annotation to sanitize incoming string fields automatically
SanitizedStr = Annotated[str, BeforeValidator(sanitize_text)]
