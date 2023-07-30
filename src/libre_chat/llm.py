"""Module: Open-source LLM setup"""
import os
from typing import List, Optional, Tuple

import torch
from langchain import PromptTemplate
from langchain.chains import ConversationChain, RetrievalQA
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.memory import ConversationBufferMemory
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
        template_variables: Optional[List[str]] = None,
        template_prompt: Optional[str] = None,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        return_source_documents: Optional[bool] = None,
        vector_count: Optional[int] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> None:
        """
        Constructor for the LLM
        """
        self.conf = conf if conf else default_conf
        self.model_path = model_path if model_path else self.conf.llm.model_path
        self.model_type = model_type if model_type else self.conf.llm.model_type
        self.model_download = model_download if model_download else self.conf.llm.model_download
        self.embeddings_path = embeddings_path if embeddings_path else self.conf.vector.embeddings_path
        self.embeddings_download = embeddings_download if embeddings_download else self.conf.vector.embeddings_download
        self.vector_path = vector_path if vector_path else self.conf.vector.vector_path
        self.vector_download = vector_download if vector_download else self.conf.vector.vector_download
        self.documents_path = documents_path if documents_path else self.conf.vector.documents_path
        self.return_source_documents = (
            return_source_documents if return_source_documents else self.conf.vector.return_source_documents
        )
        self.vector_count = vector_count if vector_count else self.conf.vector.vector_count
        self.chunk_size = chunk_size if chunk_size else self.conf.vector.chunk_size
        self.chunk_overlap = chunk_overlap if chunk_overlap else self.conf.vector.chunk_overlap
        self.max_new_tokens = max_new_tokens if max_new_tokens else self.conf.llm.max_new_tokens
        self.temperature = temperature if temperature else self.conf.llm.temperature
        self.template_variables = template_variables if template_variables else self.conf.template.variables
        self.template_prompt = template_prompt if template_prompt else self.conf.template.prompt

        if torch.cuda.is_available():
            self.device = torch.device(0)
            log.info(f"⚡ Using GPU: {self.device}")
        else:
            log.info("💽 No GPU detected, using CPU")
            self.device = torch.device("cpu")
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)

        os.environ["NUMEXPR_MAX_THREADS"] = str(self.conf.info.max_workers)

        if not self.template_prompt:
            if self.vector_path:
                self.template_prompt = DEFAULT_QA_TEMPLATE
                self.template_variables = ["question", "context"]
            else:
                self.template_prompt = DEFAULT_GENERIC_TEMPLATE
                self.template_variables = ["input", "history"]
        if len(self.template_variables) < 1:
            raise ValueError("You should provide at least 1 template variable")

        self.template = PromptTemplate(template=self.template_prompt, input_variables=self.template_variables)
        self.download_data()
        if self.vector_path:
            self.build_vectorstore()
        self.setup_dbqa()

    def download_data(self):
        """Download data"""
        ddl_list = []
        ddl_list.append({"url": self.model_download, "path": self.model_path})
        ddl_list.append({"url": self.embeddings_download, "path": self.embeddings_path})
        ddl_list.append({"url": self.vector_download, "path": self.vector_path})
        parallel_download(ddl_list, self.conf.info.max_workers)

    def setup_dbqa(self):
        """Setup the model and vector db for QA"""
        log.info(f"🤖 Loading CTransformers model from {BOLD}{self.model_path}{END}")
        # Instantiate local CTransformers model
        llm = CTransformers(
            model=self.model_path,
            model_type=self.model_type,
            config={"max_new_tokens": self.max_new_tokens, "temperature": self.temperature},
        )
        if self.vector_path:
            log.info(
                f"💫 Loading vector database at {BOLD}{self.vector_path}{END}, with embeddings from {BOLD}{self.embeddings_path}{END}"
            )
            embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_path, model_kwargs={"device": self.device})
            vectordb = FAISS.load_local(self.vector_path, embeddings)

            self.dbqa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectordb.as_retriever(search_kwargs={"k": self.vector_count}),
                return_source_documents=self.return_source_documents,
                chain_type_kwargs={"prompt": self.template},
            )
        else:
            log.info("🦜 No vector database provided, using a generic LLM")
            self.conversation = ConversationChain(
                llm=llm, prompt=self.template, verbose=True, memory=ConversationBufferMemory()
            )

    def build_vectorstore(self, documents_path: Optional[str] = None):
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
            loader = DirectoryLoader(documents_path, glob="*.pdf", loader_cls=PyPDFLoader)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            texts = text_splitter.split_documents(documents)
            embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_path, model_kwargs={"device": self.device})
            vectorstore = FAISS.from_documents(texts, embeddings)
            vectorstore.save_local(self.vector_path)
        else:
            log.warn(f"⚠️ No documents found in {documents_path}, could not build the vectorstore")
        return self.vector_path

    def query(self, prompt: str, history: Optional[List[Tuple[str, str]]] = None):
        """Query the built LLM"""
        log.info(f"💬 Querying the LLM with prompt: {prompt}")
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")

        if self.vector_path:
            # TODO: handle history
            res = self.dbqa({"query": prompt})
            log.debug(f"💭 Complete response from the LLM: {res}")
            if "result" not in res:
                raise Exception(f"No result was returned by the LLM: {res}")
        else:
            resp = self.conversation.predict(input=prompt)
            res = {"result": resp}
        return res


DEFAULT_GENERIC_TEMPLATE = """Assistant is a large language model trained by everyone.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {input}
Assistant:"""

DEFAULT_QA_TEMPLATE = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
