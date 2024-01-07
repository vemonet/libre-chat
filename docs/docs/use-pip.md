[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat)

`libre-chat` is tested on Linux, and MacOS, should work on Windows WSL.

!!! Tip "Production deployment"

    When deploying in production it is recommended to use [docker](https://www.docker.com), or directly [gunicorn](https://gunicorn.org), to handle many requests. The CLI is mainly used for local testing and building vectorstores.


## 📦 Install

Install from [PyPI](https://pypi.org/project/libre-chat/) with `pipx` or `pip`:

```bash
pip install libre-chat
```

??? Note "Installing on Windows"

    We recommend to use WSL or Docker. Otherwise you can install with an extra dependency:

    ```bash
    pip install "libre-chat[windows]"
    ```

    Note there are some issues with the `UnstructuredEmailLoader` on Windows. It uses `unstructured`, which uses [`python-magic`](https://pydigger.com/pypi/python-magic) which fails due to a `ctypes` import.


## ⌨️ Use as a command-line interface

You can easily **start a new chat web service** including UI and API from your terminal. If no arguments are provided it will try to parse a `chat.yml` file in the current directory, or use the default configuration:

```bash
libre-chat start
```

Provide a specific **config file**:

```bash
libre-chat start config/chat-vectorstore-qa.yml
```

Re-build the **vectorstore**:

```bash
libre-chat build --vector vectorstore/db_faiss --documents documents
```

Get a full rundown of the available options with the usual:

```bash
libre-chat --help
```

## 🐍 Use in python scripts

Alternatively, you can use this package in python scripts:

```python title="main.py"
import logging

import uvicorn
from libre_chat import ChatConf, ChatEndpoint, Llm

logging.basicConfig(level=logging.getLevelName("INFO"))
conf = ChatConf(
    model_path="./models/mixtral-8x7b-instruct-v0.1.Q2_K.gguf",
    vector_path=None
)
llm = Llm(conf=conf)
print(llm.query("What is the capital of the Netherlands?"))

# Create and deploy a FastAPI app based on your LLM
app = ChatEndpoint(llm=llm, conf=conf)
uvicorn.run(app)
```

Checkout the [Code reference](/libre-chat/Llm) for more details on the available classes.
