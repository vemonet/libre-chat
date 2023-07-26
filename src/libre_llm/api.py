import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

from fastapi import Body, FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from libre_llm.config import LlmConfig
from libre_llm.llm import setup_dbqa
from libre_llm.ui import gradio_app

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
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@dataclass
class Prompt:
    prompt: str
    history_with_input: List[tuple[str, str]] = field(default_factory=lambda: [])
    system_prompt: Optional[str] = None
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None


example_prompt = {"prompt": "What is the capital of the Netherlands?"}

cfg = LlmConfig()
dbqa = setup_dbqa(cfg)


@app.post("/prompt", description=DESCRIPTION, response_description="Prompt response", response_model={})
def send_prompt(
    prompt: Prompt = Body(..., example=example_prompt),
) -> List[tuple[str, str]]:
    if len(prompt.prompt) < 1:
        raise ValueError("Provide a `prompt`")
    return dbqa({"query": prompt.prompt})


# https://github.com/gradio-app/gradio/issues/1608
app.mount("/", gradio_app(dbqa))
