from typing import Generic, TypeVar

from ninja import Schema
from pydantic import Field

T = TypeVar("T")


class MessageResponse(Schema):
    message: str = Field(..., description="Human-readable message")


class HealthResponse(Schema):
    status: str = Field(default="ok")
    database: bool = Field(default=True)
    version: str = Field(default="0.1.0")


class PaginatedResponse(Schema, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
