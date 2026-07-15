import os

os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-with-at-least-32-bytes",
)
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ["DATABASE_URL"] = "sqlite:///./test_task_manager.db"

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


def _register_and_login(
    client: TestClient,
    email: str,
    password: str = "StrongPassword@123",
) -> dict[str, str]:
    signup_response = client.post(
        "/auth/signup",
        json={
            "full_name": "Test User",
            "email": email,
            "password": password,
        },
    )
    assert signup_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_signup_login_and_me(client: TestClient):
    headers = _register_and_login(client, "me@example.com")

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_duplicate_email_is_rejected(client: TestClient):
    _register_and_login(client, "duplicate@example.com")

    response = client.post(
        "/auth/signup",
        json={
            "full_name": "Duplicate User",
            "email": "duplicate@example.com",
            "password": "StrongPassword@123",
        },
    )

    assert response.status_code == 409


def test_task_crud_for_logged_in_user(client: TestClient):
    headers = _register_and_login(client, "tasks@example.com")

    create_response = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Write API tests",
            "description": "Cover auth and task CRUD",
            "status": "Pending",
        },
    )
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    list_response = client.get("/tasks?status=Pending", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Write API tests",
            "description": "CRUD tests completed",
            "status": "Completed",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Completed"

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert missing_response.status_code == 404


def test_user_cannot_access_another_users_task(client: TestClient):
    alice_headers = _register_and_login(client, "alice@example.com")
    bob_headers = _register_and_login(client, "bob@example.com")

    create_response = client.post(
        "/tasks",
        headers=alice_headers,
        json={
            "title": "Private task",
            "description": "Only Alice can access this",
            "status": "Pending",
        },
    )
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    forbidden_response = client.get(f"/tasks/{task_id}", headers=bob_headers)
    assert forbidden_response.status_code == 403

    bob_tasks_response = client.get("/tasks", headers=bob_headers)
    assert bob_tasks_response.status_code == 200
    assert bob_tasks_response.json() == []


def test_tasks_require_authentication(client: TestClient):
    response = client.get("/tasks")

    assert response.status_code == 401