import logging
import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import requests


@dataclass
class Prompt:
    prompt: str
    history_with_input: List[Tuple[str, str]] = field(default_factory=lambda: [])
    system_prompt: Optional[str] = None
    max_new_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None


class ColoredFormatter(logging.Formatter):
    COLORS: Dict[str, str] = {
        "DEBUG": "\033[92m",  # Grey
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m",  # Red
    }

    def format(self, record):  # noqa: A003
        log_level = record.levelname
        color_prefix = self.COLORS.get(log_level, END)
        log_msg = super().format(record)
        colored_log_level = f"{color_prefix}{log_level}{END}"
        return log_msg.replace(log_level, colored_log_level, 1)


log = logging.getLogger("uvicorn.access")
if len(log.handlers) > 0:
    log.handlers[0].setFormatter(
        ColoredFormatter("%(levelname)s:     [%(asctime)s] [%(module)s:%(funcName)s] %(message)s")
    )
BOLD = "\033[1m"
END = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def download_file(url, path):
    ddl_path = f"{path}-ddl" if not url.endswith(".zip") else f"{path}.zip"
    log.info(f"📥 Downloading {url} to {ddl_path}")
    with requests.get(url, stream=True, timeout=10800) as response:  # 3h timeout
        response.raise_for_status()
        with open(ddl_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Adjust the chunk size as needed
                file.write(chunk)
    if ddl_path.endswith(".zip"):
        log.info(f"🤐 Unzipping {ddl_path} to {path}")
        with zipfile.ZipFile(ddl_path, "r") as zip_ref:
            zip_ref.extractall(path)
    else:
        shutil.move(ddl_path, path)

    log.info(f"✅ Downloaded: {url} in {path}")


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
                future = executor.submit(download_file, f["url"], f["path"])
                futures.append(future)
        for future in futures:
            future.result()
