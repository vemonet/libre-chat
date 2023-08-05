import os
from typing import Any, Dict, List, Optional, Union

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from pydantic import BaseSettings, Extra
from pydantic_yaml import parse_yaml_raw_as

from libre_chat.utils import BOLD, END, YELLOW, log

__all__ = ["ChatConf", "parse_conf"]


class BaseConf(BaseSettings):
    class Config:
        env_prefix = "librechat_"
        extra = Extra.allow


class SettingsPrompt(BaseConf):
    variables: List[str] = ["input", "history"]
    template: str = ""


class SettingsInfo(BaseConf):
    examples: List[str] = [
        "What is the capital of the Netherlands?",
        "Which drugs are approved by the FDA to mitigate Alzheimer symptoms?",
    ]
    title: str = "Libre Chat"
    version: str = "0.1.0"
    description: str = """Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama) [7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)"""
    public_url: str = "https://your-endpoint-url"
    repository_url: str = "https://github.com/vemonet/libre-chat"
    favicon: str = "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png"
    license_info: Dict[str, str] = {
        "name": "MIT license",
        "url": "https://raw.github.com/vemonet/libre-chat/main/LICENSE",
    }
    contact: Dict[str, str] = {
        "name": "Vincent Emonet",
        "email": "vincent.emonet@gmail.com",
    }
    workers: int = 4


class SettingsVector(BaseConf):
    embeddings_path: str = "sentence-transformers/all-MiniLM-L6-v2"
    # or embeddings_path: str = "./embeddings/all-MiniLM-L6-v2"
    embeddings_download: Optional[str] = None
    vector_path: Optional[str] = None
    vector_download: Optional[str] = None
    documents_path: str = "documents/"
    documents_download: Optional[str] = None
    document_loaders: List[Dict[str, Union[Union[str, Any]]]] = [
        {"glob": "*.pdf", "loader_cls": PyPDFLoader},
        {"glob": "*.[c|t|p]sv", "loader_cls": CSVLoader, "loader_kwargs": {"encoding": "utf8"}},
        {"glob": "*.?xhtm?l", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "*.xml", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "*.json*", "loader_cls": JSONLoader},
        {"glob": "*.md*", "loader_cls": UnstructuredMarkdownLoader},
        {"glob": "*.txt", "loader_cls": TextLoader, "loader_kwargs": {"encoding": "utf8"}},
        {"glob": "*.doc?x", "loader_cls": UnstructuredWordDocumentLoader},
        {"glob": "*.odt", "loader_cls": UnstructuredODTLoader},
        {"glob": "*.ppt?x", "loader_cls": UnstructuredPowerPointLoader},
        {"glob": "*.epub", "loader_cls": UnstructuredEPubLoader},
        {"glob": "*.eml", "loader_cls": UnstructuredEmailLoader},
        {"glob": "*.enex", "loader_cls": EverNoteLoader},
    ]

    chunk_size: int = 500
    chunk_overlap: int = 50
    chain_type: str = "stuff"  # Or: map_reduce, reduce, map_rerank https://docs.langchain.com/docs/components/chains/index_related_chains
    search_type: str = "similarity"  # Or: similarity_score_threshold, mmr https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore
    return_sources_count: int = 4
    score_threshold: Optional[float] = None  # Between 0 and 1


class SettingsLlm(BaseConf):
    model_type: str = "llama"
    model_path: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    model_download: Optional[str] = None
    max_new_tokens: int = 256
    temperature: float = 0.01


class SettingsAuth(BaseConf):
    admin_pass: Optional[str] = None


class ChatConf(BaseConf):
    conf_path: str = "chat.yml"
    conf_url: Optional[str] = None
    llm: SettingsLlm = SettingsLlm()
    vector: SettingsVector = SettingsVector()
    info: SettingsInfo = SettingsInfo()
    prompt: SettingsPrompt = SettingsPrompt()
    auth: SettingsAuth = SettingsAuth()


default_conf = ChatConf()


def parse_conf(path: str = default_conf.conf_path) -> ChatConf:
    if os.path.exists(path):
        with open(path) as file:
            conf = parse_yaml_raw_as(ChatConf, file.read())
            log.info(f"📋 Loaded config from {BOLD}{YELLOW}{path}{END}")
            return conf
    else:
        return default_conf
