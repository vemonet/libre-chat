import time
from typing import Any, List, Optional

import gradio as gr
import pkg_resources
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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

        # TODO: Add OAuth
        # Move get_current_user to conf.py
        # async def get_current_user(token: str = Depends(oauth2_scheme)):
        #     if not self.conf.auth.client_id:
        #         return {"sub": "anonymous"}  # Bypass auth and use a default user
        #     # Else, proceed with the usual token verification process
        #     async with httpx.AsyncClient() as client:
        #         response = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {token}"})
        #         user_info = response.json()
        #         return user_info

        # if self.conf.auth.client_id:
        #     from fastapi import Depends, status
        #     from fastapi.security import OAuth2AuthorizationCodeBearer
        #     import httpx
        #     from starlette.responses import RedirectResponse

        #     oauth2_scheme = OAuth2AuthorizationCodeBearer(
        #         authorizationUrl=f"{self.conf.auth.authorization_url}?response_type=code&client_id={self.conf.auth.client_id}&redirect_uri={self.conf.auth.redirect_uri}&scope={self.conf.auth.scope}",
        #         tokenUrl=self.conf.auth.token_url,
        #     )
        #     @self.get("/login")
        #     def login():
        #         return RedirectResponse(url=oauth2_scheme.authorizationUrl)

        #     @self.get("/auth/callback")
        #     async def auth_callback(code: str = Depends(oauth2_scheme)):
        #         token_payload = {
        #             "client_id": self.conf.auth.client_id,
        #             "client_secret": self.conf.auth.client_secret,
        #             "code": code,
        #             "grant_type": "authorization_code",
        #             "redirect_uri": self.conf.auth.redirect_uri,
        #         }
        #         async with httpx.AsyncClient() as client:
        #             response = await client.post(self.conf.auth.token_url, data=token_payload)
        #             response.raise_for_status()
        #             token = response.json()
        #             return token

        # Mount web wroker asset:
        # self.mount(
        #     "/static",
        #     StaticFiles(directory=pkg_resources.resource_filename("libre_chat", "static")),
        #     name="static",
        # )

        gr.mount_gradio_app(self, gradio_app(self.llm), path="/gradio")

        # UI with SolidJS
        self.mount(
            "/",
            StaticFiles(
                directory=pkg_resources.resource_filename("libre_chat", "webapp"), html=True
            ),
            name="static",
        )
