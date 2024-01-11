"""Module: Open-source LLM setup"""
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    EverNoteLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from libre_chat.conf import ChatConf
from libre_chat.utils import BOLD, CYAN, END, log


def build_vectorstore(
    conf: ChatConf, document_loaders: Any, device: Any, vector_path: Optional[str] = None
) -> Optional[FAISS]:
    """Build vectorstore from documents."""
    # NOTE: Using Qdrant blocked by UM proxy...
    # https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/vectorstores/qdrant.py
    time_start = datetime.now()
    documents_path = conf.vector.documents_path
    docs_count = len(os.listdir(documents_path))
    if docs_count < 1:
        log.warning(
            f"⚠️ No documents found in {documents_path}, vectorstore will not be built, and a generic chatbot will be used until documents are added"
        )
    else:
        log.info(
            f"🏗️ Building the vectorstore from the {BOLD}{CYAN}{docs_count}{END} documents found in {BOLD}{documents_path}{END}, using embeddings from {BOLD}{conf.vector.embeddings_path}{END}"
        )
        documents: List[Document] = []
        # Loading all file types provided in the document_loaders object
        for doc_load in document_loaders:
            loader = DirectoryLoader(
                documents_path,
                glob=doc_load["glob"],
                loader_cls=doc_load["loader_cls"],
                loader_kwargs=doc_load["loader_kwargs"] if "loader_kwargs" in doc_load else {},
            )
            loaded_docs = loader.load()
            if len(loaded_docs) > 0:
                log.info(f"🗃️  Loaded {len(loaded_docs)} items from {doc_load['glob']} files")
            documents.extend(loaded_docs)

        # Split the text up into small, semantically meaningful chunks (often sentences) https://js.langchain.com/docs/modules/data_connection/document_transformers/
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=conf.vector.chunk_size, chunk_overlap=conf.vector.chunk_overlap
        )
        splitted_texts = text_splitter.split_documents(documents)
        # TODO: use fastembed?
        embeddings = HuggingFaceEmbeddings(
            model_name=conf.vector.embeddings_path, model_kwargs={"device": device}
        )
        # TODO: use Qdrant vectorstore
        # os.makedirs(str(conf.vector.vector_path), exist_ok=True)
        # vectorstore = Qdrant.from_documents(
        #     splitted_texts,
        #     embeddings,
        #     # path=conf.vector.vector_path,
        #     url=conf.vector.vector_path,
        #     collection_name="libre_chat_rag",
        #     prefer_grpc=True,
        #     # force_recreate=True,
        # )
        vectorstore = FAISS.from_documents(splitted_texts, embeddings)
        if vector_path:
            vectorstore.save_local(vector_path)
        log.info(f"✅ Vectorstore built in {datetime.now() - time_start}")
        return vectorstore
    return None


DEFAULT_DOCUMENT_LOADERS: List[Dict[str, Union[str, Any]]] = [
    {"glob": "*.pdf", "loader_cls": PyPDFLoader},
    {"glob": "*.csv", "loader_cls": CSVLoader, "loader_kwargs": {"encoding": "utf8"}},
    {
        "glob": "*.tsv",
        "loader_cls": CSVLoader,
        "loader_kwargs": {"encoding": "utf8", "delimiter": "\t"},
    },
    {
        "glob": "*.psv",
        "loader_cls": CSVLoader,
        "loader_kwargs": {"encoding": "utf8", "delimiter": "\\p"},
    },
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
