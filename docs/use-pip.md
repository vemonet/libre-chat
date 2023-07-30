## 📦 Install

This package requires Python >=3.8, simply install it from [PyPI](https://pypi.org/project/libre-chat/){:target="_blank"} with `pipx` or `pip`:

```bash
pip install libre-chat
```

## ⌨️ Use as a command-line interface

You can easily start a new chat web service including UI and API using your terminal:

```bash
libre-chat start
```

Provide a specific config file:

```bash
libre-chat start config/chat-vectorstore-qa.yml
```

For re-build of the vectorstore:

```bash
libre-chat build --vector vectorstore/db_faiss --documents documents
```

Get a full rundown of the available options with:

```bash
libre-chat --help
```

## 🐍 Use in python scripts

Or you can use this package in python scripts:

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
