#!/usr/bin/python3
"""User schemas."""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    """Access Token schema class."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    uuid_pk: str
    username: str


class UserSchema(BaseModel):
    """User schema."""

    username: str
    email: EmailStr
    password: str


class UserRes(BaseModel):
    """User response schema."""

    uuid_pk: UUID
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Dict config."""

        orm_mode = True


class ModeratorSchema(BaseModel):
    """Moderator schema."""

    mod_for: str
    mod_user: str


class ModeratorRes(BaseModel):
    """Moderator schema."""

    id: int
    mod_for: str
    mod_user: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
