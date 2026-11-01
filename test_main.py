import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_state():
    main.tasks.clear()
    main.next_id = 1


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_task():
    response = client.post("/tasks", json={"title": "Apprendre DevOps"})
    assert response.status_code == 201
    assert response.json()["title"] == "Apprendre DevOps"

    response = client.get("/tasks")
    assert len(response.json()) == 1


def test_delete_task():
    created = client.post("/tasks", json={"title": "A supprimer"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get("/tasks").json() == []


def test_delete_unknown_task():
    assert client.delete("/tasks/999").status_code == 404