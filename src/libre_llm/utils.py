import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pydantic import BaseSettings
from pydantic_yaml import parse_yaml_raw_as

log = logging.getLogger("uvicorn")
# log.setLevel(logging.getLevelName("INFO"))
# formatter = logging.Formatter("%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s")
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# log.addHandler(console_handler)


@dataclass
class Prompt:
    prompt: str
    history_with_input: List[Tuple[str, str]] = field(default_factory=lambda: [])
    system_prompt: Optional[str] = None
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None


class SettingsTemplate(BaseSettings):
    prompt: Optional[str] = None
    variables: Optional[List[str]] = None

    class Config:
        env_prefix = "librellm_"


class SettingsInfo(BaseSettings):
    example_prompt: str = "What is the capital of the Netherlands?"
    title: str = "🦙 Libre LLM chat"
    version: str = "0.1.0"
    description: str = """Open source and free chatbot powered by langchain and llama2.

See: [UI](/) | [API documentation](/docs) | [Source code](https://github.com/vemonet/libre-llm)"""
    favicon: str = "https://rdflib.readthedocs.io/en/stable/_static/RDFlib.png"

    class Config:
        env_prefix = "librellm_"


class Settings(BaseSettings):
    config_path: str = "llm.yml"
    model_path: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    model_type: str = "llama"
    vector_path: Optional[str] = "vectorstore/db_faiss"
    data_path: str = "data/"
    info: SettingsInfo = SettingsInfo()
    template: SettingsTemplate = SettingsTemplate()

    class Config:
        env_prefix = "librellm_"


settings = Settings()

if os.path.exists(settings.config_path):
    with open(settings.config_path) as file:
        settings = parse_yaml_raw_as(Settings, file.read())
        log.info(f"Loaded config from {settings.config_path}")
