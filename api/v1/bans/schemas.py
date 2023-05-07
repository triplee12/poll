#!/usr/bin/python3
"""Choice schemas."""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class BanSchema(BaseModel):
    """Ban schema."""

    poll_owner_id: UUID
    banned_by: str
    user_id: UUID


class BanRes(BaseModel):
    """Ban response schema."""

    id: int
    poll_owner_id: UUID
    banned_by: str
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
