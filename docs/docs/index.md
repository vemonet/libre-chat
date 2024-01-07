<div align="center" markdown="span">

[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat) [![Image size](https://ghcr-badge.egpl.dev/vemonet/libre-chat/size)](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat) [![MIT license](https://img.shields.io/pypi/l/libre-chat)](https://github.com/vemonet/libre-chat/blob/main/LICENSE.txt)
<br />

[![Test package](https://github.com/vemonet/libre-chat/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/test.yml) [![Coverage](https://coverage-badge.samuelcolvin.workers.dev/vemonet/libre-chat.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/vemonet/libre-chat)
<br /><br />

Easily configure and deploy a **fully self-hosted chatbot web service** based on open source Large Language Models (LLMs), such as [Mixtral](https://mistral.ai/news/mixtral-of-experts) or [Llama 2](https://ai.meta.com/llama/), without the need for knowledge in machine learning.

</div>

- 🌐 Free and Open Source chatbot web service with UI and API
- 🏡 Fully self-hosted, not tied to any service, and offline capable. Forget about API keys! Models and embeddings can be pre-downloaded, and the training and inference processes can run off-line if necessary.
- 🚀 Easy to setup, no need to program, just configure the service with a [YAML](https://yaml.org/) file, and start it with 1 command
- 🪶 Chat web interface (Gradio-based, or custom HTML), working well on desktop and mobile, with streaming response, and markdown rendering.
- 📦 Available as a `pip` package 🐍, or `docker` image 🐳
- 🐌 No need for GPU, this will work even on your laptop CPU! That said, just running on CPUs can be quite slow (up to 1min to answer a documents-base question on recent laptops).
- 🦜 Powered by [`LangChain`](https://python.langchain.com) and [`llama.cpp`](https://github.com/ggerganov/llama.cpp) to perform inference locally.
- 🤖 Various types of agents can be deployed:
  - **💬 Generic conversation**: do not need any additional training, just configure settings such as the template prompt
  - **📚 Documents-based question answering** (experimental): automatically build similarity vectors from documents uploaded through the API UI, the chatbot will use them to answer your question, and return which documents were used to generate the answer (PDF, CSV, HTML, JSON, markdown, and more supported).
- 🔍 Readable logs to understand what is going on.

![UI screenshot](/libre-chat/assets/screenshot.png)

![UI screenshot](/libre-chat/assets/screenshot-light.png)

!!! warning "Early stage"
	Development on this project has just started, use it with caution. If you are looking for more mature projects check out the bottom of this page.

## ℹ️ How it works

No need to program! The whole deployment can be configured from a YAML file: paths to the model/documents/vectorstore, model settings, web services infos, etc. Create a `chat.yml` file with your configuration then starts the web service.

1. Install it as a `pip` package 🐍, or create a `docker-compose.yml` file to use the `docker` image 🐳

2. Configure the service in a `chat.yml` file

3. Start the chat web service from the terminal with `libre-chat start` or `docker compose up`

Seasoned developers can also manipulate LLM models, and deploy the API in python scripts using the `libre_chat` module.

!!! help "Report issues"

    Feel free to create [issues on GitHub](https://github.com/vemonet/libre-chat/issues), if you are facing problems, have a question, or would like to see a feature implemented. Pull requests are welcome!

## 📥 Download supported models

All models supported in GGUF format by [`llama.cpp`](https://github.com/ggerganov/llama.cpp) should work. Preferably search for the `Instruct` version of a model (fine-tuned to better follow instructions), e.g.:

* [Mixtral](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF)
* [Llama 2](https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGUF)


!!! Question "Supporting other models"

    Let us know if you managed to run other models with Libre Chat, or if you would like to see a specific model supported.

## 🔎 Technical overview

The web service is deployed using a [**⚡ FastAPI**](https://fastapi.tiangolo.com) endpoint. It has 4 routes, plus its [OpenAPI](https://www.openapis.org/) documentation available on `/docs`:

- 📮 `GET` and `POST` on `/prompt` to query the model
- 🔌 Websocket on `/chat` to open a connection with the API, and query the model
- 🖥️ Chatbot web UI served on the root URL `/`
    - The web UI is contained within a single HTML file templated using [Jinja2](https://jinja.palletsprojects.com), written in vanilla JS, using [Tailwind](https://tailwindcss.com) CSS for styling, and [marked](https://marked.js.org/) for markdown rendering

All files required for querying the model are stored and accessed locally using [**🦜🔗 LangChain**](https://python.langchain.com): the main model binary, the embeddings and documents to create the vectors, and the [vectorstore](https://python.langchain.com/docs/modules/data_connection/vectorstores/).

## 🗺️ More mature projects

If you are looking for more mature tools to play with LLMs locally we recommend to look into those really good projects:

* [chat-langchain](https://github.com/langchain-ai/chat-langchain): chat UI for LangChain
* [ollama](https://github.com/jmorganca/ollama): Get up and running with Llama 2 and other large language models locally
* [GPT4All](https://gpt4all.io): open-source LLM chatbots that you can run anywhere
* [llm](https://github.com/simonw/llm): Python library for interacting with Large Language Models, both via remote APIs and models that can be installed and run on your own machine, by Simon Willison (checkout their blog [simonwillison.net](https://simonwillison.net), for a lot of really well written articles about LLMs)
* [vLLM](https://github.com/vllm-project/vllm): A high-throughput and memory-efficient inference and serving engine for LLMs (includes OpenAI-compatible server, requires GPU)
* [ChatDocs](https://github.com/marella/chatdocs): UI to Chat with your documents offline, by the developer of [ctransformers](https://github.com/marella/ctransformers)
* [localGPT](https://github.com/PromtEngineer/localGPT): Chat with your documents on your local device using GPT models
* [text-generation-webui](https://github.com/oobabooga/text-generation-webui): A Gradio web UI for Large Language Models
