from fastapi.testclient import TestClient
from src.gateway.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_protected_route_unauthorized():
    response = client.get("/api/v1/protected")
    assert response.status_code == 401

def test_protected_route_authorized():
    response = client.get("/api/v1/protected", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200
    assert response.json()["message"] == "You are authenticated"
