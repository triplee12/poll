#!/usr/bin/python3
"""Choice routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from api.v1.database_config import get_db
from api.v1.users.oauth import get_current_user
from .schemas import ChoiceSchema, ChoiceRes
from api.v1.models import Choice

choice_router = APIRouter(prefix="/choices", tags=["choices"])


@choice_router.get("/", response_model=ChoiceRes)
async def get_choices(
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve choices."""
    if current_user:
        choices = session.query(Choice).all()
        if choices:
            return choices
        return {"message": "no choices available"}


@choice_router.get("/{id_}", response_model=ChoiceRes)
async def get_choice_by_id(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve a choice by its id."""
    if current_user:
        choice = session.query(
            Choice
        ).filter(Choice.id == id_).one_or_none()
        if choice:
            return choice
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="choice not found"
        )


@choice_router.put("/{id_}/update", response_model=ChoiceRes)
async def update_choice(
    id_: int, to_update: ChoiceSchema,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a choice."""
    choice = session.query(Choice).filter(Choice.id == id_)
    if not choice.first() and choice.first(
    ).created_by == current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="choice not found"
        )

    if choice.first() and choice.first().created_by != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    if choice.first() and choice.first().created_by == current_user.uuid_pk:
        choice.first().updated_at = datetime.utcnow()
        update_c = choice.update(**to_update.dict())
        session.commit()
        session.refresh(update_c)
        return update_c
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )


@choice_router.delete("/{id_}/delete")
async def delete_choice(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a choice."""
    choice = session.query(Choice).filter(Choice.id == id_)
    if not choice.first() and choice.first(
    ).created_by == current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="choice not found"
        )

    if choice.first() and choice.first().created_by != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    if choice.first() and choice.first().created_by == current_user.uuid_pk:
        choice.delete()
        session.commit()
        return
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )


@choice_router.post("/create", response_model=ChoiceRes)
async def create_choice(
    choice: ChoiceSchema, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new choice."""
    if current_user:
        choice.created_by = current_user.uuid_pk
        new_choice = Choice(**choice.dict())
        session.add(new_choice)
        session.commit()
        session.refresh(new_choice)
        if new_choice:
            response.status_code = status.HTTP_201_CREATED
            return new_choice
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="choice not created. Error occurred"
        )
