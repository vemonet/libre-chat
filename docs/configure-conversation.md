Create a `chat.yml` file with your configuration before starting the web service.

Below is an example of configuration using the llama-2 7B GGML model, without vectorstore, to deploy a **generic conversational agent**

```yaml title="chat.yml"
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
  title: "🦙 Libre Chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [Llama 2](https://ai.meta.com/llama).

    See: [💻 UI](/) | [📡 API](/docs) | [📚 Source code](https://github.com/vemonet/libre-chat)
  examples:
  - "What is the capital of the Netherlands?"
  - "How can I create a logger with timestamp using python logging?"
  contact:
    name: "Vincent Emonet"
    email: "vincent.emonet@gmail.com"
  license_info:
    name: "MIT license"
    url: "https://raw.github.com/vemonet/libre-chat/main/LICENSE.txt"
```
