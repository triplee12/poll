#!/usr/bin/python3
"""Poll schema."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class PollType(str, Enum):
    """Poll type choices."""

    txt = "text"
    image = "image"


class TokenData(BaseModel):
    """Token data."""

    uuid_pk: str
    username: str


class AccessToken(BaseModel):
    """Access Token schema class."""

    access_token: str
    token_type: str


class User(BaseModel):
    """User schema."""

    username: str
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Poll(BaseModel):
    """Poll schema."""

    title: str
    poll_type: PollType
    created_by: Optional[str]
    updated_at: Optional[datetime]
    is_add_choices_active: bool
    is_voting_active: bool


class Choice(BaseModel):
    """Choice schema."""

    poll_id: int
    text: str
    image: str
    votes: int
    created_by: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Moderator(BaseModel):
    """Moderator schema."""

    mod_for: str
    mod_user: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Ban(BaseModel):
    """Ban schema."""

    poll_owner_id: UUID
    banned_by: str
    user_id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
