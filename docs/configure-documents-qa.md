The whole deployment can be configured from a YAML file: paths to the model and vectorstore, model settings, web services infos. Create a `chat.yml` file with your configuration before starting the web service.

Libre Chat can be used to train and deploy a **documents-based question answering agent**

When starting the service Libre Chat will automatically check if the `vectorstore` is already available, if not, it will build it from the provided `documents`. It currently only supports PDF, but more options could be easily added, let us know if you need something in the issues.

Below is an example of configuration using the Llama 2 7B GGML model, with a FAISS vectorstore, to deploy a question answering agent that will source its answers from the documents provided in the `./documents` folder:

```yaml title="chat.yml"
llm:
  model_type: llama
  model_path: ./models/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  # We recommend to predownload the files, but you can provide download URLs that will be used if the files are not present
  model_download: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  temperature: 0.01
  max_new_tokens: 256

template:
  variables: ["question", "context"]
  prompt: |
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:

vector:
  vector_path: ./vectorstore/db_faiss # Path to the vectorstore to do QA retrieval
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
  title: "🦙 Libre Chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama).

    See: [💻 UI](/) | [📡 API](/docs) | [📚 Source code](https://github.com/vemonet/libre-chat)
  examples:
  - What is the capital of the Netherlands?
  - How can I create a logger with timestamp using python logging?
  contact:
    name: "Vincent Emonet"
    email: "vincent.emonet@gmail.com"
  license_info:
    name: "MIT license"
    url: "https://raw.github.com/vemonet/libre-chat/main/LICENSE.txt"
  max_workers: 4
```

If no files are found at the path provided, e.g. `model_path`, and a download URL has been defined, e.g. `model_download`, Libre Chat will automatically download the file from the provided URL, and unzip it if it is a `.zip` file.
