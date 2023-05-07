#!/usr/bin/python3
"""Poll schema."""
from datetime import datetime
from enum import Enum
from imaplib import Int2AP
from typing import Optional
from pydantic import BaseModel


class PollType(str, Enum):
    """Poll type choices."""

    txt = "text"
    image = "image"


class PollSchema(BaseModel):
    """Poll schema."""

    title: str
    poll_type: PollType
    created_by: Optional[str]
    is_add_choices_active: bool
    is_voting_active: bool


class PollRes(BaseModel):
    """Poll response schema."""

    id: int
    title: str
    poll_type: PollType
    created_by: Optional[str]
    is_add_choices_active: bool
    is_voting_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
