#!/usr/bin/python3
"""Users routes."""
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.v1.database_config import get_db
from api.v1.models import User
from api.v1.users.oauth import get_current_user
from api.v1.schema import User as UserSchema, AccessToken
from .oauth import create_token
from .utils import verify_pwd

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
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


@user_router.get("/{uuid_pk}")
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


@user_router.post("/create", response_model=UserSchema)
async def create(
    user: UserSchema, response: Response,
    session: Session = Depends(get_db)
):
    """Create a new user."""
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
