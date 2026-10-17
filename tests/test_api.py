from fastapi.testclient import TestClient

from api.main import app
from core.providers.gemini import GeminiProvider

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "NOVA",
    }


def test_chat_success(monkeypatch):
    def mock_ask(self, prompt):
        return "This is a mocked response."

    monkeypatch.setattr(GeminiProvider, "ask", mock_ask)

    response = client.post("/api/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "This is a mocked response."}


def test_empty_message():
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_missing_message():
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
