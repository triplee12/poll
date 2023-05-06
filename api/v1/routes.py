#!/usr/bin/python3
"""Routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from api.v1.users.oauth import get_current_user

from .models import Poll
from .database_config import get_db
from .schema import Poll as PollSchema

poll_router = APIRouter(prefix="/polls", tags=["poll"])


@poll_router.get("/")
async def retrieve_polls(session: Session = Depends(get_db)):
    """Retrieve all polls."""
    polls = session.query(Poll).all()
    if polls:
        return polls
    return {"message": "No polls available"}


@poll_router.post("/create", response_model=PollSchema)
async def create_poll(
    poll: PollSchema, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new poll."""
    poll.created_by = current_user.username
    new_poll = Poll(**poll.dict())
    session.add(new_poll)
    session.commit()
    session.refresh(new_poll)
    return new_poll


@poll_router.get("/{id_}", response_model=PollSchema)
async def retrieve_poll_by_id(id_: int, session: Session = Depends(get_db)):
    """Retrieve a poll by the given id."""
    get_poll = session.query(Poll).filter(Poll.id == id_).first()

    if not get_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )

    return get_poll


@poll_router.put("/update/{id_}", response_model=PollSchema)
async def update_poll(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a poll."""
    get_poll = session.query(Poll).filter(Poll.id == id_).first()

    if not get_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )

    if get_poll.created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    get_poll.updated_at = datetime.utcnow()


@poll_router.delete("/delete/{id_}")
async def delete_poll(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a poll."""
    get_poll = session.query(Poll).filter(Poll.id == id_)

    if not get_poll.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )

    if get_poll.first().created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    get_poll.delete()
    session.commit()
    return
