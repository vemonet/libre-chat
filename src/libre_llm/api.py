"""Module: API for LLM"""
import time
from typing import Any, List, Tuple

from fastapi import Body, FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from libre_llm.llm import Llm
from libre_llm.ui import gradio_app
from libre_llm.utils import Prompt

DESCRIPTION = """API for a chatbot powered by llama2, hosted at Maastricht University.

Checkout the [UI at /](/)

[Source code on GitHub](https://github.com/vemonet/libre-llm)
"""

app = FastAPI(
    title="Llama2 API",
    description=DESCRIPTION,
    license_info={"name": "MIT license", "url": "https://raw.github.com/vemonet/libre-llm/main/LICENSE"},
    contact={
        "name": "Vincent Emonet",
        "email": "vincent.emonet@gmail.com",
    },
    # terms_of_service = "https://raw.github.com/vemonet/libre-llm/main/LICENSE",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Response:
    start_time = time.time()
    response: Response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


example_prompt = {"prompt": "What is the capital of the Netherlands?"}
llm = Llm()


@app.post("/prompt", description=DESCRIPTION, response_description="Prompt response", response_model={})
def send_prompt(
    prompt: Prompt = Body(..., example=example_prompt),
) -> List[Tuple[str, str]]:
    return llm.query(prompt.prompt)


# https://github.com/gradio-app/gradio/issues/1608
app.mount("/", gradio_app(llm))
