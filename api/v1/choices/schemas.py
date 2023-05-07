#!/usr/bin/python3
"""Choice schemas."""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class ChoiceSchema(BaseModel):
    """Choice schema."""

    poll_id: int
    text: str
    image: str
    created_by: Optional[UUID]


class ChoiceRes(BaseModel):
    """Choice response schema."""

    id: int
    poll_id: int
    text: str
    image: str
    votes: Optional[int]
    created_by: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
