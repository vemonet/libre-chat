import time
from typing import Any, List, Optional

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from libre_llm.llm_router import LlmRouter
from libre_llm.ui import gradio_app
from libre_llm.utils import Settings, settings

__all__ = [
    "LlmEndpoint",
]


class LlmEndpoint(FastAPI):
    """
    Class to deploy a LLM endpoint with API and web UI.
    """

    def __init__(
        self,
        *args: Any,
        llm: Any,
        settings: Settings = settings,
        path: str = "/prompt",
        examples: Optional[List[str]] = None,
        cors_enabled: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the SPARQL endpoint, everything happens here.
        FastAPI calls are defined in this constructor
        """
        self.path = path
        self.llm = llm
        self.settings = settings
        self.examples = examples
        if not self.examples:
            self.examples = settings.info.examples

        # Instantiate FastAPI
        super().__init__(
            *args,
            title=self.settings.info.title,
            description=self.settings.info.description,
            version=self.settings.info.version,
            license_info=self.settings.info.license_info,
            contact=self.settings.info.contact,
            **kwargs,
        )

        llm_router = LlmRouter(
            llm=self.llm,
            path=self.path,
            settings=self.settings,
            examples=self.examples,
        )
        self.include_router(llm_router)

        if cors_enabled:
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

        self.mount(
            "/",
            gradio_app(self.llm, self.settings.info.title, self.settings.info.description, self.settings.info.examples),
        )
