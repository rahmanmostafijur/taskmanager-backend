from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_app():
    response = client.get("/")
    assert response.status_code == 200

def test_tasks_requires_auth():
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_invalid_token_rejected():
    response = client.get("/tasks/", headers={"Authorization": "Bearer abcd1234"})
    assert response.status_code == 401