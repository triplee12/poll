#!/usr/bin/python3
"""Poll schema."""
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr


class PollType(Enum, str):
    """Poll type choices."""

    text = "text"
    image = "image"


class User(BaseModel):
    """User schema."""

    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class Poll(BaseModel):
    """Poll schema."""

    title: str
    poll_type: PollType
    created_by: str
    created_at: datetime
    updated_at: datetime
    is_add_choices_active: bool
    is_voting_active: bool


class Choice(BaseModel):
    """Choice schema."""

    poll_id: int
    text: str
    image: str
    votes: int
    created_by: str
    created_at: datetime
    updated_at: datetime


class Moderator(BaseModel):
    """Moderator schema."""

    mod_for: str
    mod_user: str
    created_at: datetime
    updated_at: datetime


class Ban(BaseModel):
    """Ban schema."""

    poll_owner_id: UUID
    banned_by: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
