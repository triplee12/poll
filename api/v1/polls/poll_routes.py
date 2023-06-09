#!/usr/bin/python3
"""Poll routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from api.v1.users.oauth import get_current_user
from api.v1.database_config import get_db
from api.v1.models import Poll
from .schemas import PollSchema, PollRes

poll_router = APIRouter(prefix="/polls", tags=["poll"])


@poll_router.get("/", response_model=PollRes)
async def retrieve_polls(session: Session = Depends(get_db)):
    """Retrieve all polls."""
    polls = session.query(Poll).all()
    if polls:
        return polls
    return {"message": "No polls available"}


@poll_router.post("/create", response_model=PollRes)
async def create_poll(
    poll: PollSchema, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new poll."""
    poll.created_by = current_user.username
    new_poll = Poll(**poll.dict())
    session.add(new_poll)
    session.commit()
    session.refresh(new_poll)
    if new_poll:
        response.status_code = status.HTTP_201_CREATED
        return new_poll
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Error occurred while creating poll"
    )


@poll_router.get("/{id_}", response_model=PollRes)
async def retrieve_poll_by_id(id_: int, session: Session = Depends(get_db)):
    """Retrieve a poll by the given id."""
    get_poll = session.query(Poll).filter(Poll.id == id_).first()

    if not get_poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found"
        )

    return get_poll


@poll_router.put("/update/{id_}", response_model=PollRes)
async def update_poll(
    id_: int, poll: PollSchema, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a poll."""
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

    get_poll.first().updated_at = datetime.utcnow()
    updated = get_poll.update(**poll.dict(), synchronize_session=False)
    session.commit()
    session.refresh(updated)
    return updated


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
