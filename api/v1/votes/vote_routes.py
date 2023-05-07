#!/usr/bin/python3
"""Vote routes."""
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from api.v1.database_config import get_db
from api.v1.users.oauth import get_current_user
from api.v1.models import Vote
from api.v1.schema import VoteRes, VoteSchema

vote_router = APIRouter(prefix="/votes", tags=["votes"])


@vote_router.get("/", response_model=VoteRes)
async def get_votes(
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve a list of votes."""
    if current_user:
        votes = session.query(Vote).all()
        if votes:
            return votes
        return {"message": "No votes were found"}


@vote_router.get("/{id_}", response_model=VoteRes)
async def get_vote(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve a vote from the database."""
    if current_user:
        vote = session.query(Vote).filter(Vote.id == id_).first()
        if vote:
            return vote
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="vote not found"
        )


@vote_router.delete("/{id_}/update", response_model=VoteRes)
async def delete_vote(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a vote."""
    vote = session.query(Vote).filter(Vote.id == id_)
    if not vote.first() and vote.first().user == current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="vote not found"
        )

    if vote.first() and vote.first().user != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    if vote.first() and vote.first().user == current_user.uuid_pk:
        vote.delete()
        session.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="access denied"
    )


@vote_router.post("/create", response_model=VoteRes)
async def create_vote(
    vote: VoteSchema, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new vote."""
    if current_user:
        vote.user = current_user.uuid_pk
        new_vote = Vote(**vote.dict())
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        if new_vote:
            response.status_code = status.HTTP_201_CREATED
            return new_vote
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="vote already exists"
        )
