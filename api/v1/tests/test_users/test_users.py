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
    """Test retrieve users fail."""
    users = authorized_client.get("users/")
    assert users.status_code == 403


def test_retrieve_one_user_fail(client):
    """Test retrieve one user fail."""
    user = client.get("users/12345-567f35-2cd3wrhgb")
    assert user.status_code == 403


def test_update_user_fail(client):
    """Test update user fail."""
    data = {
        "email": "user@example.com"
    }
    user = client.put("users/12345-567f35-2cd3wrhgb/update", data=data)
    assert user.status_code == 403


def test_delete_user_fail(client):
    """Test delete user fail."""
    user = client.delete("users/12345-567f35-2cd3wrhgb/delete")
    assert user.status_code == 403


def test_retrieve_moderators_fail(client):
    """Test retrieve moderators fail."""
    moderators = client.get("users/moderators")
    assert moderators.status_code == 403


def test_retrieve_one_moderator_fail(client):
    """Retrieve one moderator fail."""
    moderator = client.get("users/moderators/12345-567f35-2cd3wrhgb")
    assert moderator.status_code == 403


def test_update_moderator_fail(client):
    """Test update moderator fail."""
    data = {
        "email": "user@example.com"
    }
    moderator = client.put(
        "users/moderator/12345-567f35-2cd3wrhgb/update",
        data=data
    )
    assert moderator.status_code == 404


def test_delete_moderator_fail(client):
    """Test delete moderator fail."""
    user = client.delete("users/moderator/12345-567f35-2cd3wrhgb/delete")
    assert user.status_code == 404


@pytest.mark.parametrize(
    "mod_for, mod_user",
    [
        (1, "12345-567f35-2cd3wrhgb"),
        (2, "12345-567f35-2cd3wrhgb"),
        (3, "12345-567f35-2cd3wrhgb"),
        (4, "12345-567f35-2cd3wrhgb"),
        (5, "12345-567f35-2cd3wrhgb")
    ]
)
def test_create_moderators_fail(client, mod_for, mod_user):
    """Test creating moderators fail."""
    new_moderators = {
        "mod_for": mod_for,
        "mod_user": mod_user
    }
    create = client.post(
        "/users/moderators/create",
        json=new_moderators
    )

    assert create.status_code == 403
    print(create.json())
    assert isinstance(create.json(), dict)


def test_logout_fail(client):
    """Test logout user fail."""
    user = client.get("users/logout")
    assert user.status_code == 403
