#!/usr/bin/python3
"""Bans user routes."""
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from api.v1.database_config import get_db
from api.v1.models import Ban, User, Moderator
from api.v1.users.oauth import get_current_user
from .schemas import BanSchema, BanRes

ban_router = APIRouter(prefix="/ban", tags=["ban"])


@ban_router.post("/{user_id}", response_model=BanRes)
async def ban_user(
    user_id: str, ban: BanSchema, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Ban a user."""
    user = session.query(User).filter(User.uuid_pk == user_id).first()
    moderator = session.query(
        Moderator
    ).filter(Moderator.mod_user == current_user.uuid_pk).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if not moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    new_ban = Ban(**ban.dict())
    session.add(new_ban)
    session.commit()
    response.status_code = status.HTTP_201_CREATED

    return {"message": "user has been banned from voting"}


@ban_router.get("/users", response_model=BanRes)
async def retrieve_banned_users(
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve banned users."""
    users = await session.query(Ban).all()
    moderator = await session.query(
        Moderator
    ).filter(Moderator.mod_user == current_user.uuid_pk).first()

    if moderator:
        return users

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="not implemented"
    )


@ban_router.get("/users/{user_id}", response_model=BanRes)
async def get_user(
    user_id: str, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve a banned user."""
    user = await session.query(Ban).filter(Ban.user_id == user_id).first()
    moderator = await session.query(
        Moderator
    ).filter(Moderator.mod_user == current_user.uuid_pk).first()

    if not user and moderator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if user and moderator:
        return user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="not implemented"
    )


@ban_router.delete("/users/{user_id}/delete")
async def unban_user(
    user_id: str, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Unban a user from voting."""
    user = session.query(Ban).filter(Ban.user_id == user_id)
    moderator = session.query(
        Moderator
    ).filter(Moderator.mod_user == current_user.uuid_pk).first()

    if not user.first() and moderator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if not user.first() and not moderator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="not implemented"
        )

    if user.first() and not moderator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="not implemented"
        )

    user.delete()
    session.commit()
    return
