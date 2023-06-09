#!/usr/bin/python3
"""Pall models."""
from sqlalchemy import (
    BOOLEAN, TIMESTAMP, Column, DateTime, String,
    Enum, Integer, ForeignKey, text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database_config import Base


class User(Base):
    """User class model."""

    __tablename__ = 'users'
    uuid_pk = Column(
        "id", UUID(as_uuid=False), primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    polls = relationship("Poll", back_populates="user")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=None,
        index=False
    )

    def __repr__(self):
        """User representation."""
        return f"{self.username} joined on {self.created_at}"


class Poll(Base):
    """Poll class model."""

    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=150), nullable=False)
    poll_type = Column(
        Enum("text", "image", name="poll_type_enum", create_type=False),
        nullable=False
    )
    created_by = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship("User", back_populates="polls",
                        foreign_keys=[created_by])
    choices = relationship("Choice", back_populates="poll")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=None,
        index=False
    )
    is_add_choices_active = Column(BOOLEAN, nullable=True, default=False)
    is_voting_active = Column(BOOLEAN, nullable=True, default=False)

    def __repr__(self):
        """Poll string representation."""
        return f"{self.id}: {self.title} created by {self.created_by}"


class Choice(Base):
    """Choice class model."""

    __tablename__ = 'choices'
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(
        Integer, ForeignKey("polls.id", ondelete="CASCADE"),
        nullable=False
    )
    poll = relationship("Poll", back_populates="choices",
                        foreign_keys=[poll_id])
    txt = Column("text", String(length=50), nullable=True)
    image = Column(String(length=250), nullable=True)
    votes = relationship("Vote", back_populates="choice")
    created_by = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=None, index=False
    )

    def __repr__(self):
        """Choice str representation."""
        return f"{self.id} created by {self.created_by}"


class Vote(Base):
    """User vote."""

    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    choice_id = Column(
        Integer, ForeignKey("choices.id", ondelete="CASCADE"),
        nullable=False
    )
    choice = relationship(
        "Choice", back_populates="votes",
        foreign_keys=[choice_id]
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )


class Moderator(Base):
    """Moderator model."""

    __tablename__ = 'moderators'
    id = Column(Integer, primary_key=True, index=True)
    mod_for = Column(String(length=150), nullable=False)
    mod_user = Column(
        UUID, ForeignKey("users.id"),
        nullable=False
    )
    created_by = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=None,
        index=False
    )

    def __repr__(self):
        """Moderator interface."""
        return f"{self.mod_user} moderator for {self.mod_for}"


class Ban(Base):
    """Ban a user from voting."""

    __tablename__ = "ban"
    id = Column(Integer, index=True, primary_key=True)
    poll_owner_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    banned_by = Column(
        String, ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )

    def __repr__(self):
        """Banned users string representation."""
        return f"""
            Ban id: {self.id} - user: {self.user_id} banned by {self.banned_by}
            """
