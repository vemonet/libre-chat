import logging
import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import requests
from pydantic import BaseSettings
from pydantic_yaml import parse_yaml_raw_as


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
    public_url: str = "https://your-endpoint-url"
    favicon: str = "https://rdflib.readthedocs.io/en/stable/_static/RDFlib.png"
    license_info: Dict[str, str] = {
        "name": "MIT license",
        "url": "https://raw.github.com/vemonet/libre-llm/main/LICENSE",
    }
    contact: Dict[str, str] = {
        "name": "Vincent Emonet",
        "email": "vincent.emonet@gmail.com",
    }

    class Config:
        env_prefix = "librellm_"


class SettingsVector(BaseSettings):
    return_source_documents: bool = True
    vector_count: int = 2
    chunk_size: int = 500
    chunk_overlap: int = 50

    class Config:
        env_prefix = "librellm_"


class Settings(BaseSettings):
    config_path: str = "llm.yml"
    model_path: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    model_type: str = "llama"
    model_download: Optional[str] = None
    embeddings_path: str = "sentence-transformers/all-MiniLM-L6-v2"  # or "./embeddings/all-MiniLM-L6-v2"
    embeddings_download: Optional[str] = None
    vector_path: Optional[str] = "vectorstore/db_faiss"
    vector_download: Optional[str] = None
    documents_path: str = "documents/"
    max_new_tokens: int = 256
    temperature: float = 0.01
    info: SettingsInfo = SettingsInfo()
    template: SettingsTemplate = SettingsTemplate()
    vector: SettingsVector = SettingsVector()

    class Config:
        env_prefix = "librellm_"


settings = Settings()

log = logging.getLogger("uvicorn")
BOLD = "\033[1m"
END = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
# log.setLevel(logging.getLevelName("INFO"))
# formatter = logging.Formatter("%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s")
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# log.addHandler(console_handler)

if os.path.exists(settings.config_path):
    with open(settings.config_path) as file:
        settings = parse_yaml_raw_as(Settings, file.read())
        log.info(f"Loaded config from {YELLOW}{settings.config_path}")


def download_file(url, path):
    ddl_path = f"{path}-ddl" if not url.endswith(".zip") else f"{path}.zip"
    log.info(f"Downloading {url} to {ddl_path}")
    # 3h timeout
    with requests.get(url, stream=True, timeout=10800) as response:
        response.raise_for_status()
        with open(ddl_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Adjust the chunk size as needed
                file.write(chunk)
    if ddl_path.endswith(".zip"):
        log.ingo(f"Unzipping {ddl_path} to {path}")
        with zipfile.ZipFile(ddl_path, "r") as zip_ref:
            zip_ref.extractall(path)
    else:
        shutil.move(ddl_path, path)

    log.info(f"Downloaded: {url} in {path}")


def parallel_download(files_list: List[Dict[str, str]]):
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust the number of workers as needed
        futures = []
        for f in files_list:
            if not f["path"]:
                continue
            parent_folder = os.path.dirname(f["path"])
            if not os.path.exists(parent_folder):
                os.makedirs(parent_folder)
            if f["path"] and not os.path.exists(f["path"]) and f["url"]:
                # log.info(f"Downloading {f['url']} to {f['path']}")
                future = executor.submit(download_file, f["url"], f["path"])
                futures.append(future)
        for future in futures:
            future.result()
