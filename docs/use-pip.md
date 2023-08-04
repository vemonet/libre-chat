[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat)

`libre-chat` is tested on Linux.

??? Note "Using it on Mac or Windows"

    Just use Docker.

    Tests fails on MacOS, please let us know if you had any chances running it on your Mac.

    Tests were passing fine on Windows, until I added the UnstructuredEmailLoader. Since then the tests are going crazy, throwing `Windows fatal exception: access violation` without reason (the whole CTransformers thing was working fine on win, but a loader for text file smakes everything go down, with no logs, classic Windows).

    This was to be expected since Mac and Windows are not computers anymore, they are just a user interface to access the computing power hosted on Linux.

    If anyone have the time to fix those silly threads throwing error, please let me know! But I will personnally not lose time fixing problems of badly built paid proprietary softwares commercialized by the 2 biggest companies in the world. They can do it themselves. Or just switch their bad OS to be based on Linux, and contribute more to the open source community.


!!! Tip "Production deployment"

    When deploying in production it is recommended to use [docker](https://www.docker.com), or directly [gunicorn](https://gunicorn.org), to handle many requests. The CLI is mainly used for local testing and building vectorstores.


## 📦 Install

Install from [PyPI](https://pypi.org/project/libre-chat/) with `pipx` or `pip`:

```bash
pip install libre-chat
```

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
	model_path="models/llama-2-7b-chat.ggmlv3.q3_K_L.bin",
    vector_path=None
)
llm = Llm(conf=conf)
print(llm.query("What is the capital of the Netherlands?"))

# Create and deploy a FastAPI app based on your LLM
app = ChatEndpoint(llm=llm, conf=conf)
uvicorn.run(app)
```

Checkout the [Code reference](/libre-chat/Llm) for more details on the available classes.
