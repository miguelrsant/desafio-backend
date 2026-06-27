import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_login_user():

    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    response = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_wrong_password():

    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    response = client.post(
        "/users/login",
        {"username": "testuser", "password": "wrongpassword"},
        format="json",
    )

    assert response.status_code == 401
    assert response.data["message"] == "Invalid username or password."


@pytest.mark.django_db
def test_login_user_not_found():

    client = APIClient()

    response = client.post(
        "/users/login",
        {"username": "nonexistentuser", "password": "12345678"},
        format="json",
    )

    assert response.status_code == 401
    assert response.data["message"] == "Invalid username or password."


def test_login_without_username():
    client = APIClient()

    response = client.post("/users/login", {"password": "12345678"}, format="json")

    assert response.status_code == 400
    assert response.data["message"] == "Validation failed."


def test_login_without_password():
    client = APIClient()

    response = client.post("/users/login", {"username": "testuser"}, format="json")

    assert response.status_code == 400
    assert response.data["message"] == "Validation failed."


def test_login_invalid_data():
    client = APIClient()

    response = client.post("/users/login", {}, format="json")

    assert response.status_code == 400
    assert response.data["message"] == "Validation failed."


@pytest.mark.django_db
def test_login_returns():
    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    response = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert response.status_code == 200
    assert "refresh" in response.data["data"]
    assert "access" in response.data["data"]
    assert "user" in response.data["data"]


@pytest.mark.django_db
def test_login_last_login_updated():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    user.refresh_from_db()
    assert user.last_login is not None
