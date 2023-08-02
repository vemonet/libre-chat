import json
import os

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


def test_documents_upload() -> None:
    files = [
        ("files", ("test.txt", b"content")),
    ]
    with open("tests/config/amsterdam.zip", "rb") as zip_file:
        files.append(("files", ("amsterdam.zip", zip_file.read())))

    response = client.post(
        "/documents",
        files=files,
        data={"admin_pass": ""},
    )
    assert response.status_code == 200
    assert "Documents uploaded" in response.json()["message"]


def test_documents_list() -> None:
    response = client.get("/documents", params={"admin_pass": ""})
    resp = response.json()
    assert response.status_code == 200
    assert resp["count"] > 0
    assert "test.txt" in resp["files"]
    os.remove("documents/test.txt")
    os.remove("documents/amsterdam.txt")


def test_get_ui() -> None:
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
