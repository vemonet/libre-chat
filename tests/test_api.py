import json

from fastapi.testclient import TestClient

from tests.main import app

client = TestClient(app)
prompt = {"prompt": "What is the capital of the Netherlands?"}


def test_post_prompt_conversation() -> None:
    """Test POST prompt using model with a generic LLM"""
    response = client.post(
        "/prompt",
        data=json.dumps(prompt),
        headers={"Content-Type": "application/json"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert "amsterdam" in resp["result"].lower()


def test_get_prompt_conversation() -> None:
    """Test GET prompt using model with a generic LLM"""
    response = client.get("/prompt", params={"prompt": prompt})
    resp = response.json()
    assert response.status_code == 200
    assert "amsterdam" in resp["result"].lower()


def test_websocket_prompt_conversation() -> None:
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json(prompt)
        resp = websocket.receive_json()
        assert "amsterdam" in resp["result"].lower()


def test_get_ui() -> None:
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
