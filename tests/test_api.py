import json

from fastapi.testclient import TestClient

from libre_llm.api import app

client = TestClient(app)


def test_post_prompt():
    """Test POST prompt"""
    prompt = {"prompt": "What is the capital of the Netherlands?"}
    response = client.post(
        "/prompt",
        data=json.dumps(prompt),
        headers={"Content-Type": "application/json"},
    )
    resp = response.json()
    assert response.status_code == 200
    assert len(resp) >= 1
    assert len(resp["result"]) >= 1
    assert len(resp["source_documents"]) >= 1
    assert "amsterdam" in resp["result"].lower()


def test_get_ui():
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
