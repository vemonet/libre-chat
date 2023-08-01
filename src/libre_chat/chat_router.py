from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Body, Request, WebSocket
from fastapi.responses import JSONResponse
from langchain.schema.document import Document

from libre_chat.chat_conf import ChatConf, default_conf
from libre_chat.utils import Prompt, log

__all__ = [
    "ChatRouter",
]

api_responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = {
    200: {
        "description": "Chat response",
        "content": {
            "application/json": {
                "result": "",
                "source_docs": [],
            },
        },
    },
    400: {"description": "Bad Request"},
    422: {"description": "Unprocessable Entity"},
}


@dataclass
class PromptResponse:
    result: str
    source_documents: Optional[List[Document]] = None


class ChatRouter(APIRouter):
    """
    Class to deploy a LLM router with FastAPI.
    """

    def __init__(
        self,
        *args: Any,
        llm: Any,
        path: str = "/prompt",
        conf: Optional[ChatConf] = None,
        examples: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the LLM API router with the actual calls
        """
        self.path = path
        self.llm = llm
        self.conf = conf if conf else default_conf
        self.title = self.conf.info.title
        self.description = self.conf.info.description
        self.version = self.conf.info.version
        self.examples = examples if examples else self.conf.info.examples
        example_post = {"prompt": self.examples[0]}

        # Instantiate APIRouter
        super().__init__(
            *args,
            responses=api_responses,
            **kwargs,
        )
        # Create a list to store all connected WebSocket clients
        self.connected_clients: List[WebSocket] = []

        @self.get(
            self.path,
            name="Prompt the LLM",
            description=self.description,
            response_model=PromptResponse,
        )
        def get_prompt(request: Request, prompt: str = self.examples[0]) -> JSONResponse:
            """Send a prompt to the chatbot through HTTP GET operation.

            :param request: The HTTP GET request with a .body()
            :param prompt: Prompt to send to the LLM
            """
            return JSONResponse(self.llm.query(prompt))

        @self.post(
            self.path,
            name="Prompt the LLM",
            description=self.description,
            response_description="Prompt response",
            response_model=PromptResponse,
        )
        def post_prompt(
            request: Request,
            prompt: Prompt = Body(..., example=example_post),
        ) -> JSONResponse:
            """Send a prompt to the chatbot through HTTP POST operation.

            :param request: The HTTP POST request with a .body()
            :param prompt: Prompt to send to the LLM.
            """
            return JSONResponse(self.llm.query(prompt.prompt))

        @self.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            self.connected_clients.append(websocket)
            log.info(
                f"🔌 New websocket connection: {len(self.connected_clients)} clients are connected"
            )
            try:
                # Loop to receive messages from the WebSocket client
                while True:
                    data = await websocket.receive_json()
                    await websocket.send_json(self.llm.query(data["prompt"]))
            except Exception as e:
                log.error(f"WebSocket error: {e}")
            finally:
                self.connected_clients.remove(websocket)
