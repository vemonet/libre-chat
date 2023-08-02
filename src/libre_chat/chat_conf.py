import os
from typing import Any, Dict, List, Optional, Union

from langchain.document_loaders import (
    CSVLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)
from pydantic import BaseSettings
from pydantic_yaml import parse_yaml_raw_as

from libre_chat.utils import BOLD, END, YELLOW, log

__all__ = ["ChatConf", "parse_conf"]


class SettingsPrompt(BaseSettings):
    variables: List[str] = ["input", "history"]
    template: str = ""

    class Config:
        env_prefix = "librechat_"


class SettingsInfo(BaseSettings):
    examples: List[str] = [
        "What is the capital of the Netherlands?",
        "Which drugs are approved by the FDA to mitigate Alzheimer symptoms?",
    ]
    title: str = "Libre Chat"
    version: str = "0.1.0"
    description: str = """Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama) [7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)"""
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
    workers: int = 4

    class Config:
        env_prefix = "librechat_"


class SettingsVector(BaseSettings):
    embeddings_path: str = "sentence-transformers/all-MiniLM-L6-v2"
    # or embeddings_path: str = "./embeddings/all-MiniLM-L6-v2"
    embeddings_download: Optional[str] = None
    vector_path: Optional[str] = None
    vector_download: Optional[str] = None
    documents_path: str = "documents/"
    document_loaders: List[Dict[str, Union[Union[str, Any]]]] = [
        {"glob": "*.pdf", "loader_cls": PyPDFLoader},
        {"glob": "*.[c|t|p]sv", "loader_cls": CSVLoader},
        {"glob": "*.?xhtm?l", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "*.json*", "loader_cls": JSONLoader},
        {"glob": "*.md*", "loader_cls": UnstructuredMarkdownLoader},
        {"glob": "*.txt", "loader_cls": TextLoader},
    ]
    chunk_size: int = 500
    chunk_overlap: int = 50
    chain_type: str = "stuff"  # Or: map_reduce, reduce, map_rerank https://docs.langchain.com/docs/components/chains/index_related_chains
    search_type: str = "similarity"  # Or: similarity_score_threshold, mmr https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore
    return_sources_count: int = 4
    score_threshold: Optional[float] = None  # Between 0 and 1

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
    prompt: SettingsPrompt = SettingsPrompt()

    class Config:
        env_prefix = "librechat_"


default_conf = ChatConf()


def parse_conf(path: str = default_conf.config_path) -> ChatConf:
    if os.path.exists(path):
        with open(path) as file:
            cfg = parse_yaml_raw_as(ChatConf, file.read())
            log.info(f"📋 Loaded config from {BOLD}{YELLOW}{path}{END}")
            return cfg
    else:
        return default_conf
