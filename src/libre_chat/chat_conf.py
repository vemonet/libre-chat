import os
from typing import Dict, List, Optional

from pydantic import BaseSettings
from pydantic_yaml import parse_yaml_raw_as

from libre_chat.utils import BOLD, END, YELLOW, log


class SettingsTemplate(BaseSettings):
    prompt: Optional[str] = None
    variables: Optional[List[str]] = None

    class Config:
        env_prefix = "librechat_"


class SettingsInfo(BaseSettings):
    examples: List[str] = ["What is the capital of the Netherlands?"]
    title: str = "🦙 Libre Chat"
    version: str = "0.1.0"
    description: str = """Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama).

See: [💻 UI](/) | [📡 API](/docs) | [📚 Source code](https://github.com/vemonet/libre-chat)"""
    public_url: str = "https://your-endpoint-url"
    repository_url: str = "https://github.com/vemonet/libre-chat"
    favicon: str = "https://raw.github.com/vemonet/libre-chat/main/docs/assets/logo.png"
    license_info: Dict[str, str] = {
        "name": "MIT license",
        "url": "https://raw.github.com/vemonet/libre-chat/main/LICENSE",
    }
    contact: Dict[str, str] = {
        "name": "Vincent Emonet",
        "email": "vincent.emonet@gmail.com",
    }
    max_workers: int = 4

    class Config:
        env_prefix = "librechat_"


class SettingsVector(BaseSettings):
    embeddings_path: str = "sentence-transformers/all-MiniLM-L6-v2"
    # or embeddings_path: str = "./embeddings/all-MiniLM-L6-v2"
    embeddings_download: Optional[str] = None
    vector_path: Optional[str] = None  # "vectorstore/db_faiss"
    vector_download: Optional[str] = None
    documents_path: str = "documents/"
    return_source_documents: bool = True
    vector_count: int = 2
    chunk_size: int = 500
    chunk_overlap: int = 50

    class Config:
        env_prefix = "librechat_"


class SettingsLlm(BaseSettings):
    model_type: str = "llama"
    model_path: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    model_download: Optional[str] = None
    max_new_tokens: int = 256
    temperature: float = 0.01

    class Config:
        env_prefix = "librechat_"


class ChatConf(BaseSettings):
    config_path: str = "chat.yml"
    llm: SettingsLlm = SettingsLlm()
    vector: SettingsVector = SettingsVector()
    info: SettingsInfo = SettingsInfo()
    template: SettingsTemplate = SettingsTemplate()

    class Config:
        env_prefix = "librechat_"


default_conf = ChatConf()


def parse_config(path: str = default_conf.config_path):
    if os.path.exists(path):
        with open(path) as file:
            cfg = parse_yaml_raw_as(ChatConf, file.read())
            log.info(f"📋 Loaded config from {BOLD}{YELLOW}{path}{END}")
            return cfg
    else:
        return default_conf
