import logging
import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import requests
from pydantic import BaseModel, validator
from uvicorn.logging import ColourizedFormatter

__all__ = ["Prompt", "parallel_download", "log"]


log_format = "%(levelprefix)s [%(asctime)s] %(message)s [%(module)s:%(funcName)s]"
log = logging.getLogger(__name__)
log.propagate = False
handler = logging.StreamHandler()
handler.setFormatter(ColourizedFormatter(log_format))
log.addHandler(handler)

BOLD = "\033[1m"
END = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


class ChatResponse(BaseModel):
    """Chat response schema."""

    message: str
    type: str = "stream"  # noqa
    sender: str = "bot"
    sources: Optional[List[Dict[str, Any]]] = None

    @validator("sender", allow_reuse=True)
    def sender_must_be_bot_or_you(cls, v: str) -> str:  # noqa
        if v not in ["bot", "user"]:
            raise ValueError("sender must be bot or user")
        return v

    @validator("type", allow_reuse=True)
    def validate_message_type(cls, v: str) -> str:  # noqa
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v


# https://github.com/lm-sys/FastChat/blob/main/docs/openai_api.md
# https://github.com/lm-sys/FastChat/blob/main/fastchat/protocol/openai_api_protocol.py
@dataclass
class Prompt:
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    history_with_input: List[Tuple[str, str]] = field(default_factory=lambda: [])
    # model: str


def download_file(url: str, path: str) -> None:
    ddl_path = f"{path}-ddl" if not url.endswith(".zip") else f"{path}.zip"
    log.info(f"📥 Downloading {url} to {ddl_path}")
    try:
        with requests.get(url, stream=True, timeout=10800) as response:  # 3h timeout
            response.raise_for_status()
            with open(ddl_path, "wb") as file:
                for chunk in response.iter_content(
                    chunk_size=8192
                ):  # Adjust the chunk size as needed
                    file.write(chunk)
        if ddl_path.endswith(".zip"):
            log.info(f"🤐 Unzipping {ddl_path} to {path}")
            with zipfile.ZipFile(ddl_path, "r") as zip_ref:
                zip_ref.extractall(path)
        else:
            shutil.move(ddl_path, path)
    except Exception as e:
        log.warning(f"⚠️ Failed to download {url}: {e}")
    log.info(f"✅ Downloaded: {url} in {path}")


def parallel_download(files_list: List[Dict[str, Optional[str]]], workers: int = 4) -> None:
    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:  # Adjust the number of workers as needed
        futures = []
        for f in files_list:
            if not f["path"]:
                continue
            parent_folder = os.path.dirname(f["path"])
            if parent_folder:
                os.makedirs(parent_folder, exist_ok=True)
            if f["path"] and not os.path.exists(f["path"]) and f["url"]:
                future = executor.submit(download_file, f["url"], f["path"])
                futures.append(future)
        for future in futures:
            future.result()
