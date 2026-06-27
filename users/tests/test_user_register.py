import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_create_user():

    client = APIClient()

    response = client.post(
        "/users/register",
        {"username": "testuser", "password": "12345678"},
        format="json",
    )

    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_register_user_duplicate_username():

    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    response = client.post(
        "/users/register",
        {"username": "testuser", "password": "12345678"},
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_without_username():

    client = APIClient()

    response = client.post("/users/register", {"password": "12345678"}, format="json")

    assert response.status_code == 400
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_user_without_password():

    client = APIClient()

    response = client.post(
        "/users/register",
        {
            "username": "testuser",
        },
        format="json",
    )

    assert response.status_code == 400
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_returns():

    client = APIClient()

    response = client.post(
        "/users/register",
        {"username": "testuser", "password": "12345678"},
        format="json",
    )
    assert response.status_code == 201
    assert response.data["data"]["user"]["username"] == "testuser"


@pytest.mark.django_db
def test_register_password_is_hashed():

    client = APIClient()

    response = client.post(
        "/users/register",
        {"username": "testuser", "password": "12345678"},
        format="json",
    )

    user = User.objects.get(username="testuser")

    assert response.status_code == 201
    assert user.password != "12345678"
    assert user.check_password("12345678")


@pytest.mark.django_db
def test_register_user_invalid_data():

    client = APIClient()

    response = client.post(
        "/users/register", {"username": "", "password": ""}, format="json"
    )

    assert response.status_code == 400
    assert not User.objects.filter(username="").exists()
