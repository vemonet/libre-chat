"""Module: Open-source LLM setup"""
import os
from typing import List, Optional, Tuple

import torch
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from libre_llm.utils import log, settings


class Llm:
    """
    Class for LLMs
    """

    def __init__(
        self,
        model_path: str = settings.MODEL_PATH,
        model_type: str = settings.MODEL_TYPE,
        vector_db_path: str = settings.VECTOR_DB_PATH,
        data_path: str = settings.DATA_PATH,
        return_source_documents: bool = True,
        vector_count: float = 2,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        max_new_tokens: int = 256,
        temperature: float = 0.01,
        device: str = "cpu",
        qa_template: str = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
""",
    ) -> None:
        """
        Constructor for the LLM
        """
        self.model_path = model_path
        self.model_type = model_type
        self.vector_db_path = vector_db_path
        self.data_path = data_path
        self.return_source_documents = return_source_documents
        self.vector_count = vector_count
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.qa_template = qa_template
        if torch.cuda.is_available():
            log.info(f"Using GPU: {device}")
            self.device = torch.device(0)
        else:
            log.info("No GPU detected, using CPU")
            self.device = torch.device("cpu")
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        self.setup_dbqa()

    def setup_dbqa(self):
        """Setup the model and vector db for QA"""
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": self.device}
        )
        vectordb = FAISS.load_local(self.vector_db_path, embeddings)
        # Build local CTransformers model
        llm = CTransformers(
            model=self.model_path,
            model_type=self.model_type,
            config={"max_new_tokens": self.max_new_tokens, "temperature": self.temperature},
        )
        # Prompt template for QA retrieval for each vectorstore
        qa_prompt = PromptTemplate(template=self.qa_template, input_variables=["context", "question"])

        self.dbqa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(search_kwargs={"k": self.vector_count}),
            return_source_documents=self.return_source_documents,
            chain_type_kwargs={"prompt": qa_prompt},
        )

    def build_vector_db(self, data_path: Optional[str] = None):
        """Build vector database with FAISS from PDF documents"""
        if not data_path:
            data_path = self.data_path
            log.info(f"Building vector db from {data_path}")
        loader = DirectoryLoader(self.data_path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
        )
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(self.vector_db_path)
        return self.vector_db_path

    def query(self, prompt: str, history: Optional[List[Tuple[str, str]]] = None):
        """Query the built LLM"""
        # TODO: handle history
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")
        res = self.dbqa({"query": prompt})
        log.debug(f"Complete response from the LLM: {res}")
        if "result" not in res:
            raise Exception(f"No result was returned by the LLM: {res}")
        return res
