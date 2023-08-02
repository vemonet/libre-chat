"""Module: Open-source LLM setup"""
import os
from typing import Any, Dict, List, Optional, Tuple

import torch
from langchain import PromptTemplate
from langchain.chains import ConversationChain, RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.memory import ConversationBufferMemory
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from libre_chat.chat_conf import ChatConf, default_conf
from libre_chat.utils import BOLD, CYAN, END, log, parallel_download

__all__ = [
    "Llm",
]


class Llm:
    """
    Class for LLMs
    """

    def __init__(
        self,
        conf: Optional[ChatConf] = None,
        model_path: Optional[str] = None,
        model_type: Optional[str] = None,
        model_download: Optional[str] = None,
        embeddings_path: Optional[str] = None,
        embeddings_download: Optional[str] = None,
        vector_path: Optional[str] = None,
        vector_download: Optional[str] = None,
        documents_path: Optional[str] = None,
        document_loaders: Optional[List[Dict[str, str]]] = None,
        prompt_variables: Optional[List[str]] = None,
        prompt_template: Optional[str] = None,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        chain_type: Optional[str] = None,
        search_type: Optional[str] = None,
        return_sources_count: Optional[int] = None,
        score_threshold: Optional[float] = None,
    ) -> None:
        """
        Constructor for the LLM
        """
        self.conf = conf if conf else default_conf
        self.model_path = model_path if model_path else self.conf.llm.model_path
        self.model_type = model_type if model_type else self.conf.llm.model_type
        self.model_download = model_download if model_download else self.conf.llm.model_download
        self.embeddings_path = (
            embeddings_path if embeddings_path else self.conf.vector.embeddings_path
        )
        self.embeddings_download = (
            embeddings_download if embeddings_download else self.conf.vector.embeddings_download
        )
        self.vector_path = vector_path if vector_path else self.conf.vector.vector_path
        self.vector_download = (
            vector_download if vector_download else self.conf.vector.vector_download
        )
        self.documents_path = documents_path if documents_path else self.conf.vector.documents_path
        self.document_loaders = (
            document_loaders if document_loaders else self.conf.vector.document_loaders
        )
        self.return_sources_count = (
            return_sources_count if return_sources_count else self.conf.vector.return_sources_count
        )
        self.chain_type = chain_type if chain_type else self.conf.vector.chain_type
        self.search_type = search_type if search_type else self.conf.vector.search_type
        self.score_threshold = (
            score_threshold if score_threshold else self.conf.vector.score_threshold
        )
        self.chunk_size = chunk_size if chunk_size else self.conf.vector.chunk_size
        self.chunk_overlap = chunk_overlap if chunk_overlap else self.conf.vector.chunk_overlap
        self.max_new_tokens = max_new_tokens if max_new_tokens else self.conf.llm.max_new_tokens
        self.temperature = temperature if temperature else self.conf.llm.temperature
        self.prompt_variables: List[str] = (
            prompt_variables if prompt_variables else self.conf.prompt.variables
        )
        self.prompt_template = prompt_template if prompt_template else self.conf.prompt.template

        if torch.cuda.is_available():
            self.device = torch.device(0)
            log.info(f"⚡ Using GPU: {self.device}")
        else:
            log.info("💽 No GPU detected, using CPU")
            self.device = torch.device("cpu")
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)

        os.environ["NUMEXPR_MAX_THREADS"] = str(self.conf.info.workers)

        if not self.prompt_template:
            if self.vector_path:
                self.prompt_template = DEFAULT_QA_PROMPT
                self.prompt_variables = ["question", "context"]
            else:
                self.prompt_template = DEFAULT_CONVERSATION_PROMPT
                self.prompt_variables = ["input", "history"]
        if len(self.prompt_variables) < 1:
            raise ValueError("You should provide at least 1 template variable")

        self.prompt = PromptTemplate(
            template=self.prompt_template, input_variables=self.prompt_variables
        )
        self.download_data()
        if self.vector_path:
            self.build_vectorstore()
        self.setup_dbqa()

    def download_data(self) -> None:
        """Download data"""
        ddl_list = []
        ddl_list.append({"url": self.model_download, "path": self.model_path})
        ddl_list.append({"url": self.embeddings_download, "path": self.embeddings_path})
        ddl_list.append({"url": self.vector_download, "path": self.vector_path})
        parallel_download(ddl_list, self.conf.info.workers)

    def setup_dbqa(self) -> None:
        """Setup the model and vector db for QA"""
        log.info(f"🤖 Loading CTransformers model from {BOLD}{self.model_path}{END}")
        # Instantiate local CTransformers model https://github.com/marella/ctransformers#config
        # NOTE: streaming not implemented yet on the LLM class (only available for OpenAI API)
        llm = CTransformers(  # type: ignore
            model=self.model_path,
            # model_file=self.model_path,
            model_type=self.model_type,
            config={"max_new_tokens": self.max_new_tokens, "temperature": self.temperature},
        )
        if self.vector_path:
            log.info(
                f"💫 Loading vector database at {BOLD}{self.vector_path}{END}, with embeddings from {BOLD}{self.embeddings_path}{END}"
            )
            embeddings = HuggingFaceEmbeddings(
                model_name=self.embeddings_path, model_kwargs={"device": self.device}
            )
            vectordb = FAISS.load_local(self.vector_path, embeddings)

            search_args: Dict[str, Any] = {"k": self.return_sources_count}
            if self.score_threshold is not None:
                search_args["score_threshold"] = self.score_threshold
            self.dbqa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type=self.chain_type,
                retriever=vectordb.as_retriever(
                    search_type=self.search_type, search_kwargs=search_args
                ),
                return_source_documents=self.return_sources_count > 0,
                chain_type_kwargs={"prompt": self.prompt},
            )
        else:
            log.info("🦜 No vector database provided, using a generic LLM")
            self.conversation = ConversationChain(
                llm=llm, prompt=self.prompt, verbose=True, memory=ConversationBufferMemory()
            )

    def build_vectorstore(self, documents_path: Optional[str] = None) -> Optional[str]:
        """Build vectorstore from PDF documents with FAISS."""
        if self.vector_path and os.path.exists(self.vector_path):
            log.info(
                f"♻️  Reusing existing vectorstore at {BOLD}{self.vector_path}{END}, skip building the vectorstore"
            )
            return self.vector_path
        if not documents_path:
            documents_path = self.documents_path
        docs_count = len(os.listdir(documents_path))
        if docs_count > 0:
            log.info(
                f"🏗️  No vectorstore found at {self.vector_path}. Building the vectorstore from the {BOLD}{CYAN}{docs_count}{END} documents found in {BOLD}{documents_path}{END}"
            )
            documents: List[Document] = []
            # Loading all file types provided in the document_loaders object
            for doc_load in self.document_loaders:
                loader = DirectoryLoader(
                    documents_path, glob=doc_load["glob"], loader_cls=doc_load["loader_cls"]  # type: ignore
                )
                loaded_docs = loader.load()
                log.info(f"🗃️  Loaded {len(loaded_docs)} items from {doc_load['glob']} files")
                documents.extend(loaded_docs)

            # Split the text up into small, semantically meaningful chunks (often sentences) https://js.langchain.com/docs/modules/data_connection/document_transformers/
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            splitted_texts = text_splitter.split_documents(documents)
            embeddings = HuggingFaceEmbeddings(
                model_name=self.embeddings_path, model_kwargs={"device": self.device}
            )
            vectorstore = FAISS.from_documents(splitted_texts, embeddings)
            if self.vector_path:
                vectorstore.save_local(self.vector_path)
        else:
            log.warning(
                f"⚠️ No documents found in {documents_path}, could not build the vectorstore"
            )
        return self.vector_path

    def query(self, prompt: str, history: Optional[List[Tuple[str, str]]] = None) -> Dict[str, str]:
        """Query the built LLM"""
        log.info(f"💬 Querying the LLM with prompt: {prompt}")
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")

        if self.vector_path:
            # TODO: handle history
            res = self.dbqa({"query": prompt})
            log.info(f"💭 Complete response from the LLM: {res}")
            for i, doc in enumerate(res["source_documents"]):
                # doc.to_json() not implemented yet
                res["source_documents"][i] = {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata,
                }
            if "result" not in res:
                raise Exception(f"No result was returned by the LLM: {res}")
        else:
            resp = self.conversation.predict(input=prompt)
            res = {"result": resp}
        return res


DEFAULT_CONVERSATION_PROMPT = """Assistant is a large language model trained by everyone.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {input}
Assistant:"""

DEFAULT_QA_PROMPT = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
