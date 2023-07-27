import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")
# log.propagate = False
# log.setLevel(logging.getLevelName("INFO"))
# console_handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s")
# console_handler.setFormatter(formatter)
# log.addHandler(console_handler)


class Settings(BaseSettings):
    MODEL_PATH: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    MODEL_TYPE: str = "llama"
    VECTOR_DB_PATH = "vectorstore/db_faiss"
    DATA_PATH = "data/"
    EXAMPLE_PROMPT = "What is the capital of the Netherlands?"
    TITLE = "🦙 Llama2 chat"
    VERSION = "0.1.0"
    FAVICON = "https://rdflib.readthedocs.io/en/stable/_static/RDFlib.png"
    DESCRIPTION = """Open source and free chatbot powered by langchain and llama2.

See: [UI](/) | [API documentation](/docs) | [Source code](https://github.com/vemonet/libre-llm)"""


settings = Settings()


@dataclass
class Prompt:
    prompt: str
    history_with_input: List[Tuple[str, str]] = field(default_factory=lambda: [])
    system_prompt: Optional[str] = None
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
