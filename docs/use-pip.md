[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat)

## 📦 Install

Install from [PyPI](https://pypi.org/project/libre-chat/){:target="_blank"} with `pipx` or `pip`:

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
