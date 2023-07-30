[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat) [![MIT license](https://img.shields.io/pypi/l/libre-chat)](https://github.com/vemonet/libre-chat/blob/main/LICENSE)

!!! warning "Early stage"
	Development on this project has just started, use it with caution

Easily configure and deploy a **fully self-hosted chat web service** based on open source Large Language Models (LLMs), such as [Llama 2](https://ai.meta.com/llama/).

Available as a `pip` package 🐍, or `docker` image 🐳

- 🌐 Free and Open Source chatbot web service with UI and API
- 🏡 Fully self-hosted, not tied to any service, and offline capable. Forget about API keys! Models and embeddings can be pre-downloaded, and the training and inference processes can run off-line if necessary.
- 🧞 Easy to setup, no need to program, just configure the service with a [YAML](https://yaml.org/) file, and start the chat web service in 1 command
- ⚡ No need for GPU, this will work even on your laptop CPU (but takes about 1min to answer on recent laptops)
- 🦜 Use [`LangChain`](https://python.langchain.com) to support performant open source models inference:
    - all [Llama-2-GGML](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML) ([7B](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)/[13B](https://huggingface.co/llamaste/Llama-2-13b-chat-hf)/[70B](https://huggingface.co/llamaste/Llama-2-70b-chat-hf))
    - all [Llama-2-GPTQ](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ)
- 📚 Possibility to automatically build similarity vectors from PDF documents, and use them to have the chatbot search documents for you.
- 🪶 Modern and lightweight chat web interface, working as well on desktop as on mobile, with support for light/dark theme


![UI screenshot](https://raw.github.com/vemonet/libre-chat/main/docs/assets/screenshot.png)

![UI screenshot](https://raw.github.com/vemonet/libre-chat/main/docs/assets/screenshot-light.png)

## ℹ️ How it works

No need to program! The whole deployment can be configured from a YAML file: paths to the model/documents/vectorstore, model settings, web services infos, etc. Create a `chat.yml` file with your configuration then starts the web service.

1. Install it as a `pip` package 🐍, or create a `docker-compose.yml` file to use the `docker` image 🐳

2. Configure the service in a `chat.yml` file

3. Start the chat web service from the terminal with `libre-chat start` or `docker compose up`

Seasoned developers can also use the models, and deploy the API in python scripts sing the `libre_chat` module.

!!! help "Report issues"

    Feel free to create [issues on GitHub](https://github.com/vemonet/libre-chat/issues){:target="_blank"}, if you are facing problems, have a question, or would like to see a feature implemented. Pull requests are welcome!

<!--

## 🗃️ Projects using libre-chat

Here are some projects using `libre-chat`:

* TODO
-->
