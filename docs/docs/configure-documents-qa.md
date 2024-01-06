The whole deployment can be configured from a YAML file: paths to the model and vectorstore, model settings, web services infos. Create a `chat.yml` file with your configuration before starting the web service.

Libre Chat can be used to train and deploy a **documents-based question answering chatbot**

When starting the service Libre Chat will automatically check if the `vectorstore` is already available, if not, it will build it from the documents provided in the directory available at the given `documents_path`.

Once the web service is up you can easily upload more documents through the API UI (green icon at the top right of the chatbot web UI). Zip files will be automatically unzipped, and the vectorstore will be automatically rebuilt with all the files uploaded to the server. You will also find a call to get the list of all the documents uploaded to the server. You can prevent unwanted users to add files by adding a pass key using the environment variable `LIBRECHAT_ADMIN_KEY`

??? abstract "File types supported"

    Libre Chat will automatically vectorize the file types below. Let us know if you need anything else in the [issues](https://github.com/vemonet/libre-chat/issues).

    | File type                  | Pattern                 |
    | -------------------------- | ----------------------- |
    | PDF                        | `*.pdf`                 |
    | CSV/TSV/PSV                | `*.csv`/`*.tsv`/`*.psv` |
    | JSON                       | `*.json*`               |
    | HTML                       | `.?xhtm?l`              |
    | Markdown                   | `*.md*`                 |
    | Text                       | `*.txt`                 |
    | Open Document Format (ODT) | `*.odt`                 |
    | Word documents             | `*.doc?x`               |
    | Excel                      | `*.xls?x`               |
    | PowerPoint                 | `*.ppt?x`               |
    | ePub                       | `*.epub`                |
    | Email                      | `*.eml`                 |
    | EverNote                   | `*.enex`                |

??? example "Use custom document loaders"

    Custom document loaders can be defined when instantiating the `Llm` class:

    ```python
    from langchain.document_loaders import (
        CSVLoader,
        EverNoteLoader,
        JSONLoader,
        PyPDFLoader,
        TextLoader,
        UnstructuredEmailLoader,
        UnstructuredEPubLoader,
        UnstructuredHTMLLoader,
        UnstructuredMarkdownLoader,
        UnstructuredODTLoader,
        UnstructuredPowerPointLoader,
        UnstructuredWordDocumentLoader,
        UnstructuredExcelLoader,
    )
    from libre_chat import Llm, parse_conf

    loaders = [
        {"glob": "*.pdf", "loader_cls": PyPDFLoader},
        {"glob": "*.csv", "loader_cls": CSVLoader, "loader_kwargs": {"encoding": "utf8"}},
        {"glob": "*.tsv", "loader_cls": CSVLoader, "loader_kwargs": {"encoding": "utf8", "delimiter": "\t"}},
        {"glob": "*.psv", "loader_cls": CSVLoader, "loader_kwargs": {"encoding": "utf8", "delimiter": "\\p"}},
        {"glob": "*.xls?x", "loader_cls": UnstructuredExcelLoader},
        {"glob": "*.?xhtm?l", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "*.xml", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "*.json*", "loader_cls": JSONLoader},
        {"glob": "*.md*", "loader_cls": UnstructuredMarkdownLoader},
        {"glob": "*.txt", "loader_cls": TextLoader, "loader_kwargs": {"encoding": "utf8"}},
        {"glob": "*.doc?x", "loader_cls": UnstructuredWordDocumentLoader},
        {"glob": "*.odt", "loader_cls": UnstructuredODTLoader},
        {"glob": "*.ppt?x", "loader_cls": UnstructuredPowerPointLoader},
        {"glob": "*.epub", "loader_cls": UnstructuredEPubLoader},
        {"glob": "*.eml", "loader_cls": UnstructuredEmailLoader},
        {"glob": "*.enex", "loader_cls": EverNoteLoader},
    ]

    llm = Llm(
        conf=parse_conf("config/chat-vectorstore-qa.yml"),
        document_loaders=loaders
    )
    ```



Below is an example of configuration using the Llama 2 7B GGML model, with a Faiss vectorstore, to deploy a question answering agent that will source its answers from the documents provided in the `./documents` folder:

```yaml title="chat.yml"
llm:
  model_type: llama
  model_path: ./models/llama-2-7b-chat.ggmlv3.q3_K_L.bin # (1)
  model_download: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
  temperature: 0.01    # Config how creative (but also potentially wrong) the model can be. 0 is safe, 1 is adventurous
  max_new_tokens: 1024 # Max number of words the LLM can generate

prompt:
  variables: ["question", "context"]
  template: |
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:

vector:
  vector_path: ./vectorstore/db_faiss # Path to the vectorstore to do QA retrieval
  vector_download: null
  embeddings_path: ./embeddings/all-MiniLM-L6-v2 # (2)
  embeddings_download: https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
  documents_path: ./documents # Path to documents to vectorize (3)
  chunk_size: 500             # Maximum size of chunks, in terms of number of characters
  chunk_overlap: 50           # Overlap in characters between chunks
  chain_type: stuff           # (4)
  search_type: similarity     # (5)
  return_sources_count: 2     # Number of sources to return when generating an answer
  score_threshold: null       # If using the similarity_score_threshold search_type. Between 0 and 1

info:
  title: "Libre Chat"
  version: "0.1.0"
  description: |
    Open source and free chatbot powered by [LangChain](https://python.langchain.com) and [llama.cpp](https://github.com/ggerganov/llama.cpp)

    See also: [📡 API](/docs) | [🖥️ Alternative UI](/ui)
  examples:
  - What is the capital of the Netherlands?
  - Which drugs are approved by the FDA to mitigate Alzheimer symptoms?
  - What was the GDP of France in 1998?
  favicon: https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png
  repository_url: https://github.com/vemonet/libre-chat
  public_url: https://chat.semanticscience.org
  contact:
    name: "Vincent Emonet"
    email: "vincent.emonet@gmail.com"
  license_info:
    name: "MIT license"
    url: "https://raw.github.com/vemonet/libre-chat/main/LICENSE.txt"
  workers: 4
```

1. We recommend to predownload the files, but you can provide download URLs that will be used if the files are not present
2. Embeddings used to generate the vectorstore.<br/>You can also directly use embeddings model from HuggingFace:
    ```yaml
    embeddings_path: sentence-transformers/all-MiniLM-L6-v2
    ```
3. When vectorizing we split the text up into small, semantically meaningful chunks (often sentences)
4. Also available: `map_reduce`, `reduce`, `map_rerank`.<br/>More details at [https://docs.langchain.com/docs/components/chains/index_related_chains](https://docs.langchain.com/docs/components/chains/index_related_chains)
5. Also available: `similarity_score_threshold`, `mmr`.<br/>More details: [https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore](https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore)


If no files are found at the path provided, e.g. `model_path`, and a download URL has been defined, e.g. `model_download`, Libre Chat will automatically download the file from the provided URL, and unzip it if it is a `.zip` file.
