"""Test a question-answering chatbot with a vectorstore"""
import os

from fastapi.testclient import TestClient

from libre_chat.conf import parse_conf
from libre_chat.endpoint import ChatEndpoint
from libre_chat.llm import Llm

prompt = {"prompt": "What is the capital of the Netherlands?"}
conf = parse_conf("config/chat-vectorstore-qa.yml")
conf.auth.admin_pass = "adminpass"
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
client = TestClient(app)


def test_websocket_prompt_vectorstore_qa() -> None:
    with client.websocket_connect("/chat") as websocket:
        websocket.send_json(prompt)
        while True:
            resp = websocket.receive_json()
            if resp["type"] == "end":
                assert resp["sender"] == "bot"
                assert "amsterdam" in resp["message"].lower()
                assert len(resp["sources"]) > 0
                break
            else:
                pass  # wait for the end


def test_documents_success_upload() -> None:
    files = [
        ("files", ("test.txt", b"content")),
    ]
    with open("tests/config/amsterdam.zip", "rb") as zip_file:
        files.append(("files", ("amsterdam.zip", zip_file.read())))

    response = client.post(
        "/documents",
        files=files,
        params={"admin_pass": conf.auth.admin_pass},
    )
    assert response.status_code == 200
    assert "Documents uploaded" in response.json()["message"]


def test_documents_success_list() -> None:
    response = client.get("/documents", params={"admin_pass": conf.auth.admin_pass})
    resp = response.json()
    assert response.status_code == 200
    assert resp["count"] > 0
    assert "test.txt" in resp["files"]
    os.remove("documents/test.txt")
    os.remove("documents/amsterdam.txt")


def test_wrong_pass() -> None:
    files = [
        ("files", ("test.txt", b"content")),
    ]
    resp = client.post(
        "/documents",
        files=files,
        params={"admin_pass": ""},
    )
    assert resp.status_code == 403
    resp = client.get("/documents", params={"admin_pass": ""})
    assert resp.status_code == 403
    resp = client.get("/config", params={"admin_pass": ""})
    assert resp.status_code == 403
    resp = client.post("/config", json=conf.dict(), params={"admin_pass": ""})
    assert resp.status_code == 403


def test_documents_empty_files() -> None:
    resp = client.post(
        "/documents",
        files=[],
        params={"admin_pass": conf.auth.admin_pass},
    )
    assert resp.status_code == 422


def test_get_config() -> None:
    response = client.get("/config", params={"admin_pass": conf.auth.admin_pass})
    resp = response.json()
    assert response.status_code == 200
    assert resp["llm"]["model_path"] == conf.llm.model_path


def test_post_config() -> None:
    conf_test = conf
    conf_test.llm.model_path = "changedmodel"
    response = client.post(
        "/config", json=conf_test.dict(), params={"admin_pass": conf.auth.admin_pass}
    )
    resp = response.json()
    assert response.status_code == 200
    assert resp["llm"]["model_path"] == "changedmodel"
