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

from libre_llm.utils import BOLD, END, log, parallel_download, settings

__all__ = [
    "Llm",
]


class Llm:
    """
    Class for LLMs
    """

    def __init__(
        self,  # cfg: Settings = settings,
        model_path: str = settings.llm.model_path,
        model_type: str = settings.llm.model_type,
        model_download: str = settings.llm.model_download,
        embeddings_path: str = settings.vector.embeddings_path,
        embeddings_download: str = settings.vector.embeddings_download,
        vector_path: str = settings.vector.vector_path,
        vector_download: str = settings.vector.vector_download,
        documents_path: str = settings.vector.documents_path,
        max_new_tokens: int = settings.llm.max_new_tokens,
        temperature: float = settings.llm.temperature,
        return_source_documents: bool = settings.vector.return_source_documents,
        vector_count: int = settings.vector.vector_count,
        chunk_size: int = settings.vector.chunk_size,
        chunk_overlap: int = settings.vector.chunk_overlap,
        template_variables: Optional[List[str]] = None,
        template_prompt: Optional[str] = None,
    ) -> None:
        """
        Constructor for the LLM
        """
        self.model_path = model_path
        self.model_type = model_type
        self.model_download = model_download
        self.embeddings_path = embeddings_path
        self.embeddings_download = embeddings_download
        self.vector_path = vector_path
        self.vector_download = vector_download
        self.documents_path = documents_path
        self.return_source_documents = return_source_documents
        self.vector_count = vector_count
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.template_variables = template_variables
        self.template_prompt = template_prompt
        if torch.cuda.is_available():
            self.device = torch.device(0)
            log.info(f"Using GPU: {self.device}")
        else:
            log.info("No GPU detected, using CPU")
            self.device = torch.device("cpu")
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)

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
        self.setup_dbqa()

    def download_data(self):
        """Download data"""
        ddl_list = []
        # if not os.path.exists(self.model_path) and self.model_download:
        ddl_list.append({"url": self.model_download, "path": self.model_path})
        ddl_list.append({"url": self.embeddings_download, "path": self.embeddings_path})
        ddl_list.append({"url": self.vector_download, "path": self.vector_path})
        parallel_download(ddl_list)
        # asyncio.run(parallel_download(ddl_list))
        # if not os.path.exists(self.model_path):
        #     raise ValueError(f"Could not find a model at the path provided: {self.model_path}")

    def setup_dbqa(self):
        """Setup the model and vector db for QA"""
        log.info(f"Loading CTransformers model from {BOLD}{self.model_path}{END}")
        # Instantiate local CTransformers model
        llm = CTransformers(
            model=self.model_path,
            model_type=self.model_type,
            config={"max_new_tokens": self.max_new_tokens, "temperature": self.temperature},
        )
        if self.vector_path:
            log.info(
                f"Loading vector database at {BOLD}{self.vector_path}{END}, with embeddings from {BOLD}{self.embeddings_path}{END}"
            )
            embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_path, model_kwargs={"device": self.device})
            # embeddings = HuggingFaceEmbeddings(
            #     model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": self.device}
            # )
            vectordb = FAISS.load_local(self.vector_path, embeddings)

            self.dbqa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectordb.as_retriever(search_kwargs={"k": self.vector_count}),
                return_source_documents=self.return_source_documents,
                chain_type_kwargs={"prompt": self.template},
            )
        else:
            log.info("No vector database provided, using a generic LLM")
            self.conversation = ConversationChain(
                llm=llm, prompt=self.template, verbose=True, memory=ConversationBufferMemory()
            )

    def build_vector_db(self, documents_path: Optional[str] = None):
        """Build vector database with FAISS from PDF documents"""
        if not documents_path:
            documents_path = self.documents_path
            log.info(f"Building vector db from {documents_path}")
        loader = DirectoryLoader(self.documents_path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_path, model_kwargs={"device": "cpu"})
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(self.vector_path)
        return self.vector_path

    def query(self, prompt: str, history: Optional[List[Tuple[str, str]]] = None):
        """Query the built LLM"""
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")

        if self.vector_path:
            # TODO: handle history
            res = self.dbqa({"query": prompt})
            log.debug(f"Complete response from the LLM: {res}")
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
