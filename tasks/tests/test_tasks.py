import pytest
from rest_framework.test import APIClient
from tasks.models import Task
from users.models import User


@pytest.mark.django_db
def test_create_task_authenticated_user():
    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    responseTask = client.post(
        "/tasks/",
        {"title": "Test Task", "description": "This is a test task."},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTask.status_code == 201

    task = Task.objects.first()
    assert task.title == "Test Task"
    assert task.description == "This is a test task."


@pytest.mark.django_db
def test_create_task_without_authentication():
    client = APIClient()

    responseTask = client.post(
        "/tasks/",
        {"title": "Test Task", "description": "This is a test task."},
        format="json",
    )

    assert responseTask.status_code == 401


@pytest.mark.django_db
def test_create_task_invalid_data():
    client = APIClient()

    User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    responseTask = client.post(
        "/tasks/",
        {"title": "", "description": "This is a test task."},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTask.status_code == 400


@pytest.mark.django_db
def test_get_user_tasks():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    Task.objects.create(title="Task 1", description="Description 1", user=user)
    Task.objects.create(title="Task 2", description="Description 2", user=user)

    responseTasks = client.get(
        "/tasks/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTasks.status_code == 200
    assert len(responseTasks.data) == 2


@pytest.mark.django_db
def test_get_tasks_without_authentication():
    client = APIClient()

    responseTasks = client.get(
        "/tasks/",
        format="json",
    )

    assert responseTasks.status_code == 401


@pytest.mark.django_db
def test_get_task_detail():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user)

    responseTaskDetail = client.get(
        f"/tasks/{task.id}/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTaskDetail.status_code == 200
    assert responseTaskDetail.data["data"]["title"] == "Task 1"
    assert responseTaskDetail.data["data"]["description"] == "Description 1"


@pytest.mark.django_db
def test_get_other_user_task_detail():
    client = APIClient()

    User.objects.create_user(username="testuser1", password="12345678")
    user2 = User.objects.create_user(username="testuser2", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser1", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user2)

    responseTaskDetail = client.get(
        f"/tasks/{task.id}/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTaskDetail.status_code == 404


@pytest.mark.django_db
def test_update_task():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user)

    responseUpdateTask = client.patch(
        f"/tasks/{task.id}/",
        {"title": "Updated Task 1"},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseUpdateTask.status_code == 200
    assert responseUpdateTask.data["data"]["title"] == "Updated Task 1"


@pytest.mark.django_db
def test_update_other_user_task():
    client = APIClient()

    User.objects.create_user(username="testuser1", password="12345678")
    user2 = User.objects.create_user(username="testuser2", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser1", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user2)

    responseUpdateTask = client.patch(
        f"/tasks/{task.id}/",
        {"title": "Updated Task 1"},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseUpdateTask.status_code == 404


@pytest.mark.django_db
def test_delete_task_soft_delete():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user)

    responseDeleteTask = client.delete(
        f"/tasks/{task.id}/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseDeleteTask.status_code == 200

    # Check if the task is soft deleted
    task.refresh_from_db()
    assert task.deleted_at is not None


@pytest.mark.django_db
def test_deleted_task_not_returned():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user)

    client.delete(
        f"/tasks/{task.id}/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    task.refresh_from_db()

    responseTasks = client.get(
        "/tasks/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTasks.status_code == 200
    assert len(responseTasks.data["data"]) == 0


@pytest.mark.django_db
def test_delete_other_user_task():
    client = APIClient()

    User.objects.create_user(username="testuser1", password="12345678")
    user2 = User.objects.create_user(username="testuser2", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser1", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    task = Task.objects.create(
        title="Task 1", description="Description 1", user=user2)

    responseDeleteTask = client.delete(
        f"/tasks/{task.id}/",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseDeleteTask.status_code == 404


@pytest.mark.django_db
def test_filter_tasks_by_title():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    Task.objects.create(title="Task 1", description="Description 1", user=user)
    Task.objects.create(title="Task 2", description="Description 2", user=user)

    responseTasks = client.get(
        "/tasks/?title=Task 1",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTasks.status_code == 200
    assert len(responseTasks.data["data"]) == 1
    assert responseTasks.data["data"][0]["title"] == "Task 1"


@pytest.mark.django_db
def test_filter_tasks_by_status():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    Task.objects.create(
        title="Task 1", description="Description 1", user=user, status="COMPLETED"
    )
    Task.objects.create(
        title="Task 2", description="Description 2", user=user, status="PENDING"
    )

    responseTasks = client.get(
        "/tasks/?status=COMPLETED",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTasks.status_code == 200
    assert len(responseTasks.data["data"]) == 1
    assert responseTasks.data["data"][0]["status"] == "COMPLETED"


@pytest.mark.django_db
def test_filter_tasks_by_multiple_filters():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="12345678")

    responseLogin = client.post(
        "/users/login", {"username": "testuser", "password": "12345678"}, format="json"
    )

    assert responseLogin.status_code == 200
    acess_token = responseLogin.data["data"]["access"]

    Task.objects.create(
        title="Task 1", description="Description 1", user=user, status="COMPLETED"
    )
    Task.objects.create(
        title="Task 2", description="Description 2", user=user, status="PENDING"
    )
    Task.objects.create(
        title="Task 3", description="Description 3", user=user, status="COMPLETED"
    )

    responseTasks = client.get(
        "/tasks/?status=COMPLETED&title=Task 3",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {acess_token}",
    )

    assert responseTasks.status_code == 200
    assert len(responseTasks.data["data"]) == 1
    assert responseTasks.data["data"][0]["title"] == "Task 3"
    assert responseTasks.data["data"][0]["status"] == "COMPLETED"
