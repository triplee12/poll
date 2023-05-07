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
def test_create_users_fail(client, username, email, password):
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
        ("frank", "frank123"),
        ("me", "me123Qw"),
        ("your", "your123Lov"),
        ("Welcome", "@welcome@example.com"),
        ("whatever", "whatever123"),
    ]
)
def test_login_success(client, username, password):
    """Test creating users success."""
    login_users = {
        "username": username,
        "password": password
    }
    login = client.post("/users/login", data=login_users)

    assert login.status_code == 200
    assert isinstance(login.json(), dict)
