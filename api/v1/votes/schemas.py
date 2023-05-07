#!/usr/bin/python3
"""Vote schemas."""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class VoteSchema(BaseModel):
    """Vote schema."""

    user: Optional[UUID]
    choice_id: int


class VoteRes(BaseModel):
    """Vote response schema."""

    id: int
    user: UUID
    choice_id: int
    created_at: datetime
