"""Test a generic conversational chatbot without vectorstore"""
import json

from fastapi.testclient import TestClient

from libre_chat.conf import parse_conf
from libre_chat.endpoint import ChatEndpoint
from libre_chat.llm import Llm

prompt = {"prompt": "What is the capital of the Netherlands?"}
conf = parse_conf("tests/config/additional-prop.yml")
conf.auth.admin_pass = "testpass"
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf, examples=[prompt["prompt"]])
client = TestClient(app)


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
    with client.websocket_connect("/chat") as websocket:
        websocket.send_json(prompt)
        while True:
            resp = websocket.receive_json()
            if resp["type"] == "end":
                assert resp["sender"] == "bot"
                assert "amsterdam" in resp["message"].lower()
                break
            else:
                pass  # wait for the end


def test_get_ui() -> None:
    """Test get UI"""
    response = client.get("/")
    assert response.status_code == 200
