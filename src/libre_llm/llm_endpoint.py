import time
from typing import Any, List, Optional

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from libre_llm.llm_router import LlmRouter
from libre_llm.ui import gradio_app
from libre_llm.utils import settings

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
        path: str = "/",
        title: str = settings.info.title,
        description: str = settings.info.description,
        version: str = settings.info.version,
        examples: Optional[List[str]] = None,
        cors_enabled: bool = True,
        public_url: str = settings.info.public_url,
        favicon: str = settings.info.favicon,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the SPARQL endpoint, everything happens here.
        FastAPI calls are defined in this constructor
        """
        self.llm = llm
        self.title = title
        self.description = description
        self.version = version
        if not examples:
            examples = [settings.info.example_prompt]

        # Instantiate FastAPI
        super().__init__(
            *args,
            title=title,
            description=description,
            version=version,
            license_info=settings.info.license_info,
            contact=settings.info.contact,
            **kwargs,
        )

        llm_router = LlmRouter(
            llm=self.llm,
            path=path,
            title=title,
            description=description,
            version=version,
            examples=examples,
            public_url=public_url,
            favicon=favicon,
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

        self.mount("/", gradio_app(self.llm, self.title, self.description, examples))
