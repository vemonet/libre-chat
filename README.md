<div align="center">

# 🦙 Libre LLM

[![Publish package](https://github.com/vemonet/libre-llm/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-llm/actions/workflows/publish.yml) [![Test package](https://github.com/vemonet/libre-llm/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-llm/actions/workflows/test.yml) [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-llm/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-llm?branch=main)

[![PyPI - Version](https://img.shields.io/pypi/v/libre-llm.svg?logo=pypi&label=PyPI&logoColor=silver)](https://pypi.org/project/libre-llm/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/libre-llm.svg?logo=python&label=Python&logoColor=silver)](https://pypi.org/project/libre-llm/)
[![license](https://img.shields.io/pypi/l/libre-llm.svg?color=%2334D058)](https://github.com/vemonet/libre-llm/blob/main/LICENSE.txt)
[![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

> ⚠️ Development on this project has just started, use it with caution

Easily deploy a Chatbot locally with a web UI and API.

- Free and Open Source LLM chatbot web API and UI.
- Self-hosted, offline capable and easy to setup.
- No need for GPU, will work even on your laptop CPU (takes about 1min to answer though)
- Use `langchain` to support performant open source models inference: [Llama-2-7b](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)/[13b](https://huggingface.co/llamaste/Llama-2-13b-chat-hf)/[70b](https://huggingface.co/llamaste/Llama-2-70b-chat-hf), all [Llama-2-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ), all [Llama-2-GGML](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)

![UI screenshot](https://raw.github.com/vemonet/libre-llm/main/docs/screenshot.png)

Inspired by:

- https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference
- https://github.com/liltom-eth/llama2-webui

<!--

## 📦️ Installation

This package requires Python >=3.7, simply install it with:

```bash
pip install libre-llm
```

## 🪄 Usage

### ⌨️ Use as a command-line interface

You can easily use your package from your terminal after installing `libre-llm` with pip:

```bash
libre-llm
```

Get a full rundown of the available options with:

```bash
libre-llm --help
```

### 🐍 Use with python

 Use this package in python scripts:

 ```python
import libre_llm

# TODO: add example to use your package
 ```

-->

## 🐳 Deploy with docker

If you just want to quickly deploy it you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-llm:main
```

You can configure the deployment using environment variables.

For this using a `docker compose` and a `.env` file is easier. First create the `docker-compose.yml` file:

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

And the `llm.yml` file with your settings in the same folder as the `docker-compose.yml`:

```yaml
model_path: "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
vector_path: "vectorstore/db_faiss" # Path to the vectorstore, set to null to not use a vectostore
data_path: "data/" # For documents to vectorize if needed
info:
  title: "🦙 Libre LLM chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by langchain and llama2.

    See: [UI](/) | [API documentation](/docs) | [Source code](https://github.com/vemonet/libre-llm)"
  example_prompt: "What is the capital of the Netherlands?"
template:
  variables: [input, history]
  prompt: |
    Your are an assistant, please help me!

    {history}
    Human: {input}
    Assistant:
```

Finally start your chat service with:

```bash
docker compose up
```

## 🧑‍💻 Development setup

The final section of the README is for if you want to run the package in development, and get involved by making a code contribution.


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

### Run dev API

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

Start the docs on [http://localhost:8001](http://localhost:8001){:target="_blank"}

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

## To do

- [ ] Check if runs fine when no internet
- [ ] Try with 70B model
- [ ] Check without any vectorstore
- [ ] Try building a vectorstore from new data
- [ ] Create better UI with Svelte, served by FastAPI
