#!/usr/bin/python3
"""Database configuration."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from api.v1.app import app
from api.v1.users.oauth import create_token
from api.v1.models import Base, Poll
from api.v1.database_config import get_db
from api.v1.settings import settings

PASSW = settings.DB_USER_PASSW
DB_NAME = settings.DB_NAME
SQLALCHEMY_DATABASE_URL = f"postgresql://{PASSW}@localhost/{DB_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


@pytest.fixture(scope="session")
def session():
    """Fixture: Database session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client(session):
    """Fixture: Return TestClient."""
    def get_test_db():
        """Get the database."""
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture(scope="session")
def test_user(client):
    """Create a generic test user."""
    user_data1 = {
        "username": "testuser1",
        "password": "testpassword1",
        "email": "testemail1@testuser.com"
    }
    res = client.post("/users/create", json=user_data1)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data1["password"]
    return new_user


@pytest.fixture(scope="session")
def test_user1(client):
    """Create a generic test user."""
    user_data1 = {
        "username": "testuser2",
        "password": "testpassword1",
        "email": "testemail2@testuser.com"
    }
    res = client.post("/users/create", json=user_data1)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data1["password"]
    return new_user


@pytest.fixture(scope="session")
def token(test_user):
    """Fixture: Create token for testuser."""
    access_token = create_token(
        data={
            "uuid_pk": test_user["uuid_pk"],
            "username": test_user["username"]
        }
    )
    return access_token


@pytest.fixture(scope="session")
def authorized_client(client, token):
    """Fixture: Authorize client fixture."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer: {token}"
    }
    return client


def convert_poll(data):
    """Convert data to poll model object."""
    return Poll(**data)


@pytest.fixture(scope="session")
def test_create_poll(test_user, session, test_user1):
    """Test creating poll."""
    res = [
        {
            "title": "Testing poll creation",
            "poll_type": "text",
            "created_by": test_user.uuid_pk,
            "is_add_choices_active": True,
            "is_voting_active": True
        },
        {
            "title": "Testing poll creation",
            "poll_type": "text",
            "created_by": test_user1.uuid_pk,
            "is_add_choices_active": False,
            "is_voting_active": False
        },
        {
            "title": "Testing poll creation",
            "poll_type": "text",
            "created_by": test_user.uuid_pk,
            "is_add_choices_active": True,
            "is_voting_active": False
        },
        {
            "title": "Testing poll creation",
            "poll_type": "text",
            "created_by": test_user1.uuid_pk,
            "is_add_choices_active": False,
            "is_voting_active": True
        }
    ]
    poll_data = list(map(convert_poll, res))
    session.add_all(poll_data)
    session.commit()
    data = session.query(Poll).all()
    return data
