<div align="center">

# <span><img height="30" src="https://raw.github.com/vemonet/libre-chat/main/docs/assets/logo.png"></span> Libre Chat

[![Publish package](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml) [![Test package](https://github.com/vemonet/libre-chat/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/test.yml) [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-chat/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-chat?branch=main)

[![PyPI - Version](https://img.shields.io/pypi/v/libre-chat.svg?logo=pypi&label=PyPI&logoColor=silver)](https://pypi.org/project/libre-chat/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/libre-chat.svg?logo=python&label=Python&logoColor=silver)](https://pypi.org/project/libre-chat/)
[![License](https://img.shields.io/pypi/l/libre-chat)](https://github.com/vemonet/libre-chat/blob/main/LICENSE.txt)

Easily configure and deploy a **fully self-hosted chatbot web service** based on open source Large Language Models (LLMs), such as [Llama 2](https://ai.meta.com/llama/), without the need for knowledge in machine learning or programmation.

</div>

- 🌐 Free and Open Source chatbot web service with UI and API
- 🏡 Fully self-hosted, not tied to any service, and offline capable. Forget about API keys! Models and embeddings can be pre-downloaded, and the training and inference processes can run off-line if necessary.
- 🚀 Easy to setup, no need to program, just configure the service with a [YAML](https://yaml.org/) file, and start it with 1 command
- 📦 Available as a `pip` package 🐍, or `docker` image 🐳
- ⚡ No need for GPU, this will work even on your laptop CPU (but can take up to 1min to answer on recent laptops, works better on a server)
- 🦜 Powered by [`LangChain`](https://python.langchain.com) to support performant open source models inference: **Llama 2 GGML** ([7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML) | [13B](https://huggingface.co/llamaste/Llama-2-13b-chat-hf) | [70B](https://huggingface.co/llamaste/Llama-2-70b-chat-hf)), **Llama 2 GPTQ** ([7B](https://huggingface.co/TheBloke/Llama-2-7B-chat-GPTQ) | [13B](https://huggingface.co/TheBloke/Llama-2-13B-chat-GPTQ) | [70B](https://huggingface.co/TheBloke/Llama-2-70B-chat-GPTQ))
- 🤖 Various types of agents can be deployed:
  - **💬 Generic conversation**: do not need any additional training, just configure settings such as the template prompt
  - **📚 Documents-based question answering**: automatically build similarity vectors from locally provided PDF documents, the chatbot will use them to answer your question, and return which documents were used to generate the answer.
- 🪶 Modern and lightweight chat web interface, working well on desktop and mobile, with support for light/dark theme

Checkout the demo at [**chat.semanticscience.org**](https://chat.semanticscience.org)


![UI screenshot](https://raw.github.com/vemonet/libre-chat/main/docs/assets/screenshot.png)

![UI screenshot](https://raw.github.com/vemonet/libre-chat/main/docs/assets/screenshot-light.png)

> ⚠️ Development on this project has just started, use it with caution

## 📖 Documentation

For more details on how to use Libre Chat check the documentation at **[vemonet.github.io/libre-chat](http://vemonet.github.io/libre-chat)**

## 🐳 Deploy with docker

If you just want to quickly deploy it using the pre-trained model `Llama-2-7B-Chat-GGML`, you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-chat:main
```

You can configure the deployment using environment variables. For this using a `docker compose` and a `.env` file is easier, first create the `docker-compose.yml` file:

```yaml
version: "3"
services:
  libre-chat:
    image: ghcr.io/vemonet/libre-chat:main
    volumes:
    - ./:/data # Share the whole directory with your chat.yml, models, vectorstore
    ports:
      - 8000:8000
```

And create a `chat.yml` file with your configuration in the same folder as the `docker-compose.yml`:

```yaml
llm:
  model_type: llama
  model_path: ./models/llama-2-7b-chat.ggmlv3.q3_K_L.bin # We recommend to predownload the files, but you can provide download URLs that will be used if the files are not present:
  model_download: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  temperature: 0.01    # Config how creative, but also potentially wrong, the model can be. 0 is safe, 1 is adventurous
  max_new_tokens: 1024 # Max number of words the LLM can generate

prompt:
  # Always use input for the human input variable with a generic agent
  variables: [input, history]
  template: |
    Your are an assistant, please help me

    {history}
    Human: {input}
    Assistant:

vector:
  vector_path: null # Path to the vectorstore to do QA retrieval, e.g. ./vectorstore/db_faiss
  # Set to null to deploy a generic conversational agent
  vector_download: null
  embeddings_path: ./embeddings/all-MiniLM-L6-v2 # Path to embeddings used to generate the vectors, or use directly from HuggingFace: sentence-transformers/all-MiniLM-L6-v2
  embeddings_download: https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
  documents_path: ./documents # Path to documents to vectorize
  chunk_size: 500             # Maximum size of chunks, in terms of number of characters
  chunk_overlap: 50           # Overlap in characters between chunks
  chain_type: stuff           # Or: map_reduce, reduce, map_rerank. More details: https://docs.langchain.com/docs/components/chains/index_related_chains
  search_type: similarity     # Or: similarity_score_threshold, mmr. More details: https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore
  return_sources_count: 2     # Number of sources to return when generating an answer
  score_threshold: null       # If using the similarity_score_threshold search type. Between 0 and 1

info:
  title: "Libre Chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama) [7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)
  examples:
  - What is the capital of the Netherlands?
  - Which drugs are approved by the FDA to mitigate Alzheimer symptoms?
  - How can I create a logger with timestamp using python logging?
  favicon: https://raw.github.com/vemonet/libre-chat/main/docs/assets/logo.png
  repository_url: https://github.com/vemonet/libre-chat
  public_url: https://chat.semanticscience.org
  contact:
    name: Vincent Emonet
    email: vincent.emonet@gmail.com
  license_info:
    name: MIT license
    url: https://raw.github.com/vemonet/libre-chat/main/LICENSE.txt
```

Finally start your chat service with:

```bash
docker compose up
```

## 📦️ Usage with pip

This package requires Python >=3.8, simply install it with `pipx` or `pip`:

```bash
pip install libre-chat
```

### ⌨️ Use as a command-line interface

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

### 🐍 Use with python

Or you can use this package in python scripts:

```python
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

## 🤝 Credits

Inspired by:

- https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference
- https://github.com/liltom-eth/llama2-webui

<a href="https://www.flaticon.com/free-icons/llama" title="llama icons">Llama icons created by Freepik - Flaticon</a>

## 📋 To do

- [X] Add support for returning sources in UI when using documents-based QA
- [X] Stream response for the websocket to show words one by one: LangChain only implemented it for OpenAI at the moment
- [ ] Improve config parsing error handling
- [ ] Kubernetes deployment
- [ ] Try with 70B model
- [ ] Speed up inference, better use of GPUs
- [ ] Add authentication mechanisms (OAuth/OpenID Connect)
