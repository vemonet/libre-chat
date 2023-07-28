<div align="center">

# 🦙 Libre LLM

[![Publish package](https://github.com/vemonet/libre-llm/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-llm/actions/workflows/publish.yml) [![Test package](https://github.com/vemonet/libre-llm/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-llm/actions/workflows/test.yml) [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-llm/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-llm?branch=main)

[![PyPI - Version](https://img.shields.io/pypi/v/libre-llm.svg?logo=pypi&label=PyPI&logoColor=silver)](https://pypi.org/project/libre-llm/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/libre-llm.svg?logo=python&label=Python&logoColor=silver)](https://pypi.org/project/libre-llm/)
[![license](https://img.shields.io/pypi/l/libre-llm.svg?color=%2334D058)](https://github.com/vemonet/libre-llm/blob/main/LICENSE.txt)
[![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

> ⚠️ Development on this project has just started, use it with caution

Easily deploy a Large Language Model (LLM) chatbot web service locally with a web UI and API.

- 🌐 Free and Open Source LLM with web UI and API.
- 🏡 Fully self-hosted, offline capable, and easy to setup. No need for any API key to any service.
- ⚡ No need for GPU, this will work even on your laptop CPU (but takes about 1min to answer on recent laptops)
- 🦜 Use [`LangChain`](https://python.langchain.com) to support performant open source models inference:
  - all [Llama-2-GGML](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML) ([7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)/[13B](https://huggingface.co/llamaste/Llama-2-13b-chat-hf)/[70B](https://huggingface.co/llamaste/Llama-2-70b-chat-hf))
  - all [Llama-2-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ)


![UI screenshot](https://raw.github.com/vemonet/libre-llm/main/docs/screenshot.png)

## 🐳 Deploy with docker

If you just want to quickly deploy it using the pre-trained model `Llama-2-7B-Chat-GGML`, you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-llm:main
```

You can configure the deployment using environment variables. For this using a `docker compose` and a `.env` file is easier, first create the `docker-compose.yml` file:

```yaml
version: "3"
services:
  libre-llm:
    image: ghcr.io/vemonet/libre-llm:main
    volumes:
    - ./llm.yml:/app/llm.yml
    ports:
      - 8000:8000
```

And create a `llm.yml` file with your configuration in the same folder as the `docker-compose.yml`:

```yaml
llm:
  model_type: llama
  model_path: ./models/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  # We recommend to predownload the files, but you can provide download URLs that will be used if the files are not present
  model_download: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  temperature: 0.01
  max_new_tokens: 256
template:
  # Always use input for the human input variable with a generic agent
  variables: [input, history]
  prompt: |
    Your are an assistant, please help me

    {history}
    Human: {input}
    Assistant:
vector:
  vector_path: null # Path to the vectorstore to do QA retrieval, e.g. ./vectorstore/db_faiss
  # Set to null to deploy a generic conversational agent
  vector_download: null
  embeddings_path: ./embeddings/all-MiniLM-L6-v2 # Embeddings used to generate the vectors
  # You can also directly use embeddings model from HuggingFace:
  # embeddings_path: sentence-transformers/all-MiniLM-L6-v2
  embeddings_download: https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
  documents_path: ./documents # For documents to vectorize
  return_source_documents: true
  vector_count: 2
  chunk_size: 500
  chunk_overlap: 50
info:
  title: "🦙 Libre LLM chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by langchain and llama2.

    See: [UI](/) | [API documentation](/docs) | [Source code](https://github.com/vemonet/libre-llm)
  examples:
  - "What is the capital of the Netherlands?"
  - "How can I create a logger with timestamp using python logging?"
  contact:
    name: "Vincent Emonet"
    email: "vincent.emonet@gmail.com"
  license_info:
    name: "MIT license"
    url: "https://raw.github.com/vemonet/libre-llm/main/LICENSE.txt"
```

Finally start your chat service with:

```bash
docker compose up
```

## 📦️ Usage with pip

This package requires Python >=3.7, simply install it with `pipx` or `pip`:

```bash
pip install libre-llm
```

### ⌨️ Use as a command-line interface

You can easily start a new chat web service including UI and API using your terminal:

```bash
libre-llm start
```

Provide a specific config file:

```bash
libre-llm start tests/llm-with-vectorstore.yml
```

Get a full rundown of the available options with:

```bash
libre-llm --help
```

### 🐍 Use with python

Or you can use this package in python scripts:

 ```python
from libre_llm.llm import Llm
from libre_llm.llm_endpoint import LlmEndpoint

llm = Llm(
    model_path="models/llama-2-7b-chat.ggmlv3.q3_K_L.bin",
    vector_path=None
)
print(llm.query("What is the capital of the Netherlands?"))

# Create and deploy a FastAPI app based on your LLM
app = LlmEndpoint(llm=llm)
uvicorn.run(app)
 ```

## 🧑‍💻 Development setup

The final section of the README is for if you want to run the package in development. Feel free to contribute!


### 📥️ Clone

Clone the repository:

```bash
git clone https://github.com/vemonet/libre-llm
cd libre-llm
```
### 🐣 Install dependencies

Install [Hatch](https://hatch.pypa.io), this will automatically handle virtual environments and make sure all dependencies are installed when you run a script in the project:

```bash
pipx install hatch
```

Download pre-trained model and embeddings for local development:

```bash
./download.sh
```

### 🛩️ Run dev API

```bash
hatch run dev
```

### ☑️ Run tests

Make sure the existing tests still work by running the test suite and linting checks. Note that any pull requests to the fairworkflows repository on github will automatically trigger running of the test suite;

```bash
hatch run test
```

To display all logs when debugging:

```bash
hatch run test -s
```

You can also run the tests on multiple python versions:

```bash
hatch run all:test
```


### 📖 Generate documentation

The documentation is automatically generated from the markdown files in the `docs` folder and python docstring comments, and published by a GitHub Actions workflow.

Start the docs on [http://localhost:8001](http://localhost:8001)

```bash
hatch run docs
```

### ♻️ Reset the environment

In case you are facing issues with dependencies not updating properly you can easily reset the virtual environment with:

```bash
hatch env prune
```

Manually trigger installing the dependencies in a local virtual environment:

```bash
hatch -v env create
```

### 🏷️ New release process

The deployment of new releases is done automatically by a GitHub Action workflow when a new release is created on GitHub. To release a new version:

1. Make sure the `PYPI_TOKEN` secret has been defined in the GitHub repository (in Settings > Secrets > Actions). You can get an API token from PyPI at [pypi.org/manage/account](https://pypi.org/manage/account).
2. Increment the `version` number in the `pyproject.toml` file in the root folder of the repository.
3. Create a new release on GitHub, which will automatically trigger the publish workflow, and publish the new release to PyPI.

You can also manually trigger the workflow from the Actions tab in your GitHub repository webpage.

## 🤝 Credits

Inspired by:

- https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference
- https://github.com/liltom-eth/llama2-webui

## 📋 To do

- [ ] Try with 70B model
- [ ] Try building a vectorstore from new data
- [ ] Speed up inference
- [ ] Create better UI with Svelte, served by FastAPI
