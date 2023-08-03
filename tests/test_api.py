import json
import os

from fastapi.testclient import TestClient

from libre_chat.chat_conf import parse_conf
from libre_chat.chat_endpoint import ChatEndpoint
from libre_chat.llm import Llm

conf = parse_conf("chat.yml")
conf.auth.admin_pass = "testpass"
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
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


def test_documents_upload_success() -> None:
    files = [
        ("files", ("test.txt", b"content")),
    ]
    with open("tests/config/amsterdam.zip", "rb") as zip_file:
        files.append(("files", ("amsterdam.zip", zip_file.read())))

    response = client.post(
        "/documents",
        files=files,
        data={"admin_pass": conf.auth.admin_pass},
    )
    assert response.status_code == 200
    assert "Documents uploaded" in response.json()["message"]


def test_documents_list_success() -> None:
    response = client.get("/documents", params={"admin_pass": conf.auth.admin_pass})
    resp = response.json()
    assert response.status_code == 200
    assert resp["count"] > 0
    assert "test.txt" in resp["files"]
    os.remove("documents/test.txt")
    os.remove("documents/amsterdam.txt")


def test_documents_wrong_pass() -> None:
    files = [
        ("files", ("test.txt", b"content")),
    ]
    resp_upload = client.post(
        "/documents",
        files=files,
        data={"admin_pass": ""},
    )
    assert resp_upload.status_code == 403
    resp_list = client.get("/documents", params={"admin_pass": ""})
    assert resp_list.status_code == 403


def test_documents_empty_files() -> None:
    resp = client.post(
        "/documents",
        files=[],
        data={"admin_pass": conf.auth.admin_pass},
    )
    assert resp.status_code == 422


def test_get_ui() -> None:
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
