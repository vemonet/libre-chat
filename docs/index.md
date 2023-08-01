[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat) [![Image size](https://ghcr-badge.egpl.dev/vemonet/libre-chat/size)](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat) [![MIT license](https://img.shields.io/pypi/l/libre-chat)](https://github.com/vemonet/libre-chat/blob/main/LICENSE.txt)

Easily configure and deploy a **fully self-hosted chatbot web service** based on open source Large Language Models (LLMs), such as [Llama 2](https://ai.meta.com/llama/), without the need for knowledge in machine learning or programmation.

- 🌐 Free and Open Source chatbot web service with UI and API
- 🏡 Fully self-hosted, not tied to any service, and offline capable. Forget about API keys! Models and embeddings can be pre-downloaded, and the training and inference processes can run off-line if necessary.
- 🚀 Easy to setup, no need to program, just configure the service with a [YAML](https://yaml.org/) file, and start the chat web service with 1 command
- 📦 Available as a `pip` package 🐍, or `docker` image 🐳
- ⚡ No need for GPU, this will work even on your laptop CPU (but can take up to 1min to answer on recent laptops, works better on a server)
- 🦜 Powered by [`LangChain`](https://python.langchain.com) to support performant open source models inference: **Llama 2 GGML** ([7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML) | [13B](https://huggingface.co/llamaste/Llama-2-13b-chat-hf) | [70B](https://huggingface.co/llamaste/Llama-2-70b-chat-hf)), **Llama 2 GPTQ** ([7B](https://huggingface.co/TheBloke/Llama-2-7B-chat-GPTQ) | [13B](https://huggingface.co/TheBloke/Llama-2-13B-chat-GPTQ) | [70B](https://huggingface.co/TheBloke/Llama-2-70B-chat-GPTQ))
- 🤖 Various types of agents can be deployed:
    - **💬 Generic conversation**: do not need any additional training, just configure settings such as the template prompt
    - **📚 Documents-based question answering**: automatically build similarity vectors from locally provided PDF documents, the chatbot will use them to answer your question, and return which documents were used to generate the answer.

- 🪶 Modern and lightweight chat web interface, working well on desktop and mobile, with support for light/dark theme

Checkout the demo at [**chat.semanticscience.org**](https://chat.semanticscience.org)


![UI screenshot](/libre-chat/assets/screenshot.png)

![UI screenshot](/libre-chat/assets/screenshot-light.png)

!!! warning "Early stage"
	Development on this project has just started, use it with caution.

## ℹ️ How it works

No need to program! The whole deployment can be configured from a YAML file: paths to the model/documents/vectorstore, model settings, web services infos, etc. Create a `chat.yml` file with your configuration then starts the web service.

1. Install it as a `pip` package 🐍, or create a `docker-compose.yml` file to use the `docker` image 🐳

2. Configure the service in a `chat.yml` file

3. Start the chat web service from the terminal with `libre-chat start` or `docker compose up`

Seasoned developers can also manipulate LLM models, and deploy the API in python scripts using the `libre_chat` module.

!!! help "Report issues"

    Feel free to create [issues on GitHub](https://github.com/vemonet/libre-chat/issues), if you are facing problems, have a question, or would like to see a feature implemented. Pull requests are welcome!

## 📥 Download supported models

* Llama 2 GGML: [7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML) | [13B](https://huggingface.co/llamaste/Llama-2-13b-chat-hf) | [70B](https://huggingface.co/llamaste/Llama-2-70b-chat-hf)

* Llama 2 GPTQ: [7B](https://huggingface.co/TheBloke/Llama-2-7B-chat-GPTQ) | [13B](https://huggingface.co/TheBloke/Llama-2-13B-chat-GPTQ) | [70B](https://huggingface.co/TheBloke/Llama-2-70B-chat-GPTQ)

!!! Question "Supporting other models"

    Let us know if you managed to run other models with Libre Chat, or if you would like to see a specific model supported.

## 🔎 Technical overview

The web service is deployed using a [**⚡ FastAPI**](https://fastapi.tiangolo.com) endpoint. It has 4 routes, plus its [OpenAPI](https://www.openapis.org/) documentation available on `/docs`:

- 📮 `GET` and `POST` on `/prompt` to query the model
- 🔌 Websocket on `/ws` to open a connection with the API, and query the model
- 🖥️ Chatbot web UI served on the root URL `/`
    - The web UI is contained within a single HTML file templated using [Jinja2](https://jinja.palletsprojects.com), written in vanilla JS, using [Tailwind](https://tailwindcss.com) CSS for styling, and [marked](https://marked.js.org/) for markdown rendering

All files required for querying the model are stored and accessed locally using [**🦜🔗 LangChain**](https://python.langchain.com): the main model binary, the embeddings and documents to create the vectors, and the [vectorstore](https://python.langchain.com/docs/modules/data_connection/vectorstores/).
