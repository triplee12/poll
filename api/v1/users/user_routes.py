#!/usr/bin/python3
"""Users routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.v1.database_config import get_db
from api.v1.models import Moderator, User
from .schemas import (
    ModeratorRes, UserSchema, AccessToken,
    ModeratorSchema, UserRes
)
from .oauth import create_token, get_current_user
from .utils import verify_pwd, hash_pwd

user_router = APIRouter(prefix="/users", tags=["users"])

# [User]


@user_router.get("/", response_model=UserRes)
async def retrieve_users(
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve users."""
    if current_user:
        users = session.query(User).all()

        if not users:
            return {"message": "No users"}
        return users


@user_router.get("/{uuid_pk}", response_model=UserRes)
async def get_user_by_id(
    uuid_pk: str, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve user by id."""
    user = session.query(
        User
    ).filter(User.uuid_pk == uuid_pk).one_or_none()

    if current_user:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return user


@user_router.put("/{uuid_pk}/update", response_model=UserRes)
async def update_user(
    uuid_pk: str, updated_user: UserSchema,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update user."""
    user = session.query(
        User
    ).filter(User.uuid_pk == uuid_pk)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if user.first() and user.first().uuid_pk != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )
    user.first().updated_at = datetime.utcnow()
    user.update(**updated_user.dict())
    session.commit()
    session.refresh(user)
    return user


@user_router.delete("/{uuid_pk}/delete")
async def delete_user(
    uuid_pk: str,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete user."""
    user = session.query(
        User
    ).filter(User.uuid_pk == uuid_pk)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    if user.first() and user.first().uuid_pk != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )
    user.delete()
    session.commit()
    return


@user_router.post("/create", response_model=UserRes)
async def create(
    user: UserSchema, response: Response,
    session: Session = Depends(get_db)
):
    """Create a new user."""
    user.password = hash_pwd(user.password)
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    if new_user:
        response.status_code = status.HTTP_201_CREATED
        return new_user
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="User not created. User with username or email already exists"
    )


@user_router.post("/login", response_model=AccessToken)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    """User authentication method."""
    q_username = session.query(User).filter(
        User.username == credentials.username
    ).first()

    if not q_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_pwd(credentials.password, q_username.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_token(
        data={"id": q_username.uuid_pk, "username": q_username.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# [Moderator]


@user_router.get("/moderators", response_model=ModeratorRes)
async def get_moderators(
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve all moderators."""
    if current_user:
        moderators = session.query(Moderator).all()
        if not moderators:
            return {"message": "No moderators"}
        return moderators


@user_router.get("/moderators/{id_}", response_model=ModeratorRes)
async def get_moderator(
    id_: str, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Retrieve a moderator."""
    if current_user:
        moderator = session.query(
            Moderator
        ).filter(Moderator.id == id_).first()

        if not moderator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="moderator does not exist"
            )
        return moderator


@user_router.put("/moderators/{id_}/update", response_model=ModeratorRes)
async def update_moderator(
    id_: str, moderator: ModeratorSchema,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a moderator."""
    get_mod = session.query(Moderator).filter(Moderator.id == id_)

    if not get_mod.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="moderator does not exist"
        )

    if get_mod.first() and get_mod.first().created_by != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    get_mod.first().updated_at = datetime.utcnow()
    updated = get_mod.update(**moderator.dict())
    session.commit()
    session.refresh(updated)
    return updated


@user_router.delete("/moderators/{id_}/delete")
async def delete_moderator(
    id_: int, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Delete a moderator."""
    moderator = session.query(Moderator).filter(Moderator.id == id_)
    if not moderator.first() and moderator.first(
    ).created_by == current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="moderator does not exist"
        )

    if moderator.first() and moderator.first(
    ).created_by != current_user.uuid_pk:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access denied"
        )

    if moderator.first() and moderator.first(
    ).created_by == current_user.uuid_pk:
        moderator.delete()
        session.commit()
        return

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="moderator does not exist"
        )


@user_router.post("/moderators/create", response_model=ModeratorRes)
async def create_moderator(
    moderator: ModeratorSchema, response: Response,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Create a new moderator."""
    if current_user:
        get_user = session.query(
            User
        ).filter(User.username == moderator.mod_user).first()

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )

        moderator.created_by = current_user.uuid_pk
        new_moderator = Moderator(**moderator.dict())
        session.add(new_moderator)
        session.commit()
        session.refresh(new_moderator)
        if new_moderator:
            response.status_code = status.HTTP_201_CREATED
            return new_moderator

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="moderator already exists"
        )
