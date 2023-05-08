#!/usr/bin/python3
"""Test cases for the user models."""
import pytest


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("frank", "frank@example.com", "frank123"),
        ("me", "me@example.com", "me123Qw"),
        ("your", "your@example.com", "your123Lov"),
        ("Welcome", "Welcome@example.com", "@welcome@example.com"),
        ("whatever", "whatever@example.com", "whatever123"),
    ]
)
def test_create_users_success(client, username, email, password):
    """Test creating users success."""
    new_users = {
        "username": username,
        "email": email,
        "password": password
    }
    create = client.post("/users/create", json=new_users)

    assert create.status_code == 201
    assert isinstance(create.json(), dict)


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("frank", True, "frank123"),
        ("me", 1, "me123Qw"),
        ("your", "your@example.com", None),
        (0, None, "@welcome@example.com"),
        (True, "whatever@example.com", None)
    ]
)
def test_create_users_fail(client, test_user, username, email, password):
    """Test creating users fail."""
    new_users = {
        "username": username,
        "email": email,
        "password": password
    }
    create = client.post("/users/create", json=new_users)

    assert create.status_code == 422
    print(create.json())
    assert isinstance(create.json(), dict)


@pytest.mark.parametrize(
    "username, password",
    [
        ("testuser1", "testpassword1"),
        ("frank", "frank123"),
        ("me", "me123Qw"),
        ("your", "your123Lov"),
        ("Welcome", "@welcome@example.com"),
        ("whatever", "whatever123"),
    ]
)
def test_login_token_success(client, username, password):
    """Test login token users success."""
    login_users = {
        "username": username,
        "password": password
    }
    login = client.post("/users/login_token", data=login_users)

    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert isinstance(login.json(), dict)


@pytest.mark.parametrize(
    "username, password",
    [
        (1234, ""),
        (None, True),
        ("your", False),
        (True, "@welcome@example.com"),
        ("whatever", None),
    ]
)
def test_login_token_fail(client, username, password):
    """Test login token users fail."""
    login_users = {
        "username": username,
        "password": password
    }
    login = client.post("/users/login_token", data=login_users)

    assert login.status_code == 401 or\
        login.status_code == 422


@pytest.mark.parametrize(
    "username, password",
    [
        (1234, ""),
        (None, True),
        ("your", False),
        (True, "@welcome@example.com"),
        ("whatever", None),
    ]
)
def test_login_basic_fail(client, username, password):
    """Test login basic users fail."""
    login_users = {
        "username": username,
        "password": password
    }
    login = client.post("/users/login_basic", data=login_users)

    assert login.status_code == 401 or\
        login.status_code == 400


def test_retrieve_users_fail(authorized_client):
    """Test retrieve_users_success."""
    users = authorized_client.get("users/")
    assert users.status_code == 403
