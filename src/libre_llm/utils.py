import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

log = logging.getLogger("uvicorn")
# log.propagate = False
# log.setLevel(logging.getLevelName("INFO"))
# console_handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s")
# console_handler.setFormatter(formatter)
# log.addHandler(console_handler)


@dataclass
class Defaults:
    model_path = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    vector_db_path = "vectorstore/db_faiss"
    data_path = "data/"
    example_prompt = "What is the capital of the Netherlands?"
    title = "🦙 Llama2 chat"
    version = "0.1.0"
    favicon = "https://rdflib.readthedocs.io/en/stable/_static/RDFlib.png"
    description = """API for a chatbot powered by llama2.

[Source code on GitHub](https://github.com/vemonet/libre-llm)
"""


defaults = Defaults()


@dataclass
class Prompt:
    prompt: str
    history_with_input: List[Tuple[str, str]] = field(default_factory=lambda: [])
    system_prompt: Optional[str] = None
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
