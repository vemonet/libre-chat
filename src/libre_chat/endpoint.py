import time
from typing import Any, List, Optional

import gradio as gr
import pkg_resources
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from libre_chat.conf import ChatConf, default_conf
from libre_chat.router import ChatRouter
from libre_chat.ui import gradio_app

__all__ = [
    "ChatEndpoint",
]


class ChatEndpoint(FastAPI):
    """
    Class to deploy a LLM endpoint with API and web UI.
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
        Constructor of the SPARQL endpoint, everything happens here.
        FastAPI calls are defined in this constructor
        """
        self.path = path
        self.llm = llm
        self.conf = conf if conf else default_conf
        self.examples = examples
        if not self.examples:
            self.examples = self.conf.info.examples

        # Instantiate FastAPI
        super().__init__(
            *args,
            title=self.conf.info.title,
            description=self.conf.info.description,
            version=self.conf.info.version,
            license_info=self.conf.info.license_info,
            contact=self.conf.info.contact,
            **kwargs,
        )

        router = ChatRouter(
            llm=self.llm,
            path=self.path,
            conf=self.conf,
            examples=self.examples,
        )
        self.include_router(router)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.middleware("http")
        async def add_process_time_header(request: Request, call_next: Any) -> Response:
            start_time = time.time()
            response: Response = await call_next(request)
            response.headers["X-Process-Time"] = str(time.time() - start_time)
            return response

        # Mount web wroker asset:
        self.mount(
            "/static",
            StaticFiles(directory=pkg_resources.resource_filename("libre_chat", "static")),
            name="static",
        )

        # TODO: not found when used after installing from pip, cf. https://github.com/vemonet/libre-chat/issues/2
        templates = Jinja2Templates(
            directory=pkg_resources.resource_filename("libre_chat", "templates")
            # directory="templates"
        )

        # Serve UI from index.html directly
        @self.get("/ui", response_class=HTMLResponse, include_in_schema=False)
        def chat_ui(request: Request) -> Any:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "title": self.conf.info.title,
                    "description": self.conf.info.description,
                    "short_description": self.conf.info.description.split("\n")[0].replace('"', ""),
                    "repository_url": self.conf.info.repository_url,
                    "examples": self.conf.info.examples,
                    "favicon": self.conf.info.favicon,
                },
            )

        @self.get("/admin", response_class=HTMLResponse, include_in_schema=False)
        def admin_ui(request: Request) -> Any:
            return templates.TemplateResponse(
                "admin.html",
                {
                    "request": request,
                    "title": self.conf.info.title,
                    "description": self.conf.info.description,
                    "short_description": self.conf.info.description.split("\n")[0].replace('"', ""),
                    "repository_url": self.conf.info.repository_url,
                    "examples": self.conf.info.examples,
                    "favicon": self.conf.info.favicon,
                },
            )

        self = gr.mount_gradio_app(self, gradio_app(self.llm), path="/")

        # TODO: Try with svelte https://github.com/OriginalStefikO/fastapi-svelte-starter/blob/main/main.py
        # self.mount(
        #     "/",
        #     StaticFiles(
        #         directory=pkg_resources.resource_filename("libre_chat", "webapp"), html=True
        #     ),
        #     name="static",
        # )
