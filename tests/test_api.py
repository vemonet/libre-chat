import json

from fastapi.testclient import TestClient

from tests.main import app

client = TestClient(app)


def test_post_prompt_conversational():
    """Test POST prompt using model with a generic LLM"""
    prompt = {"prompt": "What is the capital of the Netherlands?"}
    response = client.post(
        "/prompt",
        data=json.dumps(prompt),
        headers={"Content-Type": "application/json"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert "amsterdam" in resp["result"].lower()


def test_get_prompt_conversational():
    """Test GET prompt using model with a generic LLM"""
    prompt = {"prompt": "What is the capital of the Netherlands?"}
    response = client.get("/prompt", params={"prompt": prompt})
    resp = response.json()
    assert response.status_code == 200
    assert "amsterdam" in resp["result"].lower()


def test_get_ui():
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
