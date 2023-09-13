import os
import zipfile
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Body, File, HTTPException, Request, UploadFile, WebSocket
from fastapi.responses import JSONResponse
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.schema.document import Document

from libre_chat.conf import ChatConf, default_conf
from libre_chat.utils import ChatResponse, Prompt, log

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

        @self.post(
            "/documents",
            description="""Upload documents to be added to the vectorstore, you can provide a zip file that will be automatically unzipped.""",
            response_description="Operation result",
            response_model={},
            tags=["vectorstore"],
        )
        def upload_documents(
            files: List[UploadFile] = File(...),
            admin_pass: Optional[str] = None,
            # current_user: User = Depends(get_current_user),
        ) -> JSONResponse:
            os.makedirs(self.conf.vector.documents_path, exist_ok=True)
            if self.conf.auth.admin_pass and admin_pass != self.conf.auth.admin_pass:
                raise HTTPException(
                    status_code=403,
                    detail="The admin pass key provided was wrong",
                )
            for uploaded in files:
                if uploaded.filename:  # no cov
                    file_path = os.path.join(self.conf.vector.documents_path, uploaded.filename)
                    with open(file_path, "wb") as file:
                        file.write(uploaded.file.read())
                    # Check if the uploaded file is a zip file
                    if uploaded.filename.endswith(".zip"):
                        log.info(f"🤐 Unzipping {file_path}")
                        with zipfile.ZipFile(file_path, "r") as zip_ref:
                            zip_ref.extractall(self.conf.vector.documents_path)
                        os.remove(file_path)
            self.llm.build_vectorstore()
            self.llm.setup_dbqa()
            return JSONResponse(
                {
                    "message": f"Documents uploaded in {self.conf.vector.documents_path}, vectorstore rebuilt."
                }
            )

        @self.get(
            "/documents",
            description="""List documents uploaded to the server.""",
            response_description="List of files",
            response_model={},
            tags=["vectorstore"],
        )
        def list_documents(
            admin_pass: Optional[str] = None,
        ) -> JSONResponse:
            """List all documents in the documents folder."""
            if self.conf.auth.admin_pass and admin_pass != self.conf.auth.admin_pass:
                raise HTTPException(
                    status_code=403,
                    detail="The admin pass key provided was wrong",
                )
            file_list = os.listdir(self.conf.vector.documents_path)
            return JSONResponse({"count": len(file_list), "files": file_list})

        @self.get(
            "/config",
            name="Get Chat configuration",
            description="""Get the Chat web service configuration.""",
            response_description="Chat configuration",
            response_model=ChatConf,
            tags=["configuration"],
        )
        def get_config(
            admin_pass: Optional[str] = None,
        ) -> JSONResponse:
            """Get the Chat web service configuration."""
            if self.conf.auth.admin_pass and admin_pass != self.conf.auth.admin_pass:
                raise HTTPException(
                    status_code=403,
                    detail="The admin pass key provided was wrong",
                )
            return JSONResponse(self.conf.dict())

        @self.post(
            "/config",
            name="Edit Chat configuration",
            description="""Edit the Chat web service configuration.""",
            response_description="Chat configuration",
            response_model=ChatConf,
            tags=["configuration"],
        )
        def post_config(
            request: Request,
            config: ChatConf = Body(..., example=self.conf),
            admin_pass: Optional[str] = None,
        ) -> JSONResponse:
            """Edit the Chat web service configuration."""
            if self.conf.auth.admin_pass and admin_pass != self.conf.auth.admin_pass:
                raise HTTPException(
                    status_code=403,
                    detail="The admin pass key provided was wrong",
                )
            self.conf = config
            # TODO: save new config to disk, and make sure all workers reload the new config
            return JSONResponse(self.conf.dict())

        @self.websocket("/chat")
        async def websocket_endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            self.connected_clients.append(websocket)
            log.info(
                f"🔌 New websocket connection: {len(self.connected_clients)} clients are connected"
            )
            memory = ConversationBufferMemory(ai_prefix="AI Assistant")
            try:
                # Loop to receive messages from the WebSocket client
                while True:
                    data = await websocket.receive_json()

                    start_resp = ChatResponse(sender="bot", message="", type="start")
                    await websocket.send_json(start_resp.dict())

                    resp = await self.llm.aquery(
                        data["prompt"],
                        memory=memory,
                        callbacks=[StreamWebsocketCallback(websocket)],
                    )
                    # chat_history.append((question, resp["result"]))
                    # log.warning("RESULTS!")
                    # log.warning(resp["result"])

                    end_resp = ChatResponse(
                        sender="bot",
                        message=resp["result"],
                        type="end",
                        sources=resp["source_documents"] if "source_documents" in resp else None,
                    )
                    await websocket.send_json(end_resp.model_dump())
            except Exception as e:
                log.error(f"WebSocket error: {e}")
            finally:
                self.connected_clients.remove(websocket)


# https://github.com/langchain-ai/chat-langchain/blob/master/main.py
# class StreamingWebsocketCallbackHandler(AsyncCallbackHandler):
class StreamWebsocketCallback(AsyncCallbackHandler):
    """Callback handler for streaming to websocket.
    Only works with LLMs that support streaming."""

    def __init__(
        self,
        websocket: WebSocket,
    ) -> None:
        """Initialize callback handler."""
        super().__init__()
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        resp = ChatResponse(message=token, sender="bot", type="stream")
        await self.websocket.send_json(resp.model_dump())
