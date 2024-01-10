"""Module: Open-source LLM setup"""
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import torch
from langchain.chains import ConversationChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import Qdrant

from libre_chat.conf import ChatConf, default_conf
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
        model_download: Optional[str] = None,
        vector_path: Optional[str] = None,
        document_loaders: Optional[List[Dict[str, Any]]] = None,
        prompt_variables: Optional[List[str]] = None,
        prompt_template: Optional[str] = None,
    ) -> None:
        """
        Constructor for the LLM
        """
        # NOTE: if we need to share infos between workers import redis
        # self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.conf = conf if conf else default_conf
        self.model_path = model_path if model_path else self.conf.llm.model_path
        self.model_download = model_download if model_download else self.conf.llm.model_download
        self.vector_path = vector_path if vector_path else self.conf.vector.vector_path
        self.document_loaders = document_loaders if document_loaders else DEFAULT_DOCUMENT_LOADERS
        self.prompt_variables: List[str] = (
            prompt_variables if prompt_variables is not None else self.conf.llm.prompt_variables
        )
        self.prompt_template = prompt_template if prompt_template else self.conf.llm.prompt_template

        # Check if GPU available
        if torch.cuda.is_available():
            self.device = torch.device(0)
            log.info(f"⚡ Using GPU: {self.device}")
        else:
            log.info("💽 No GPU detected, using CPU")
            self.device = torch.device("cpu")
        os.makedirs(self.conf.vector.documents_path, exist_ok=True)

        # Set max worker threads. Not sure it's the best place to do this
        os.environ["NUMEXPR_MAX_THREADS"] = str(self.conf.info.workers)

        if len(self.prompt_variables) < 1:
            raise ValueError("You should provide at least 1 template variable")

        # TODO: remove? There is always a default from ChatConf
        if not self.prompt_template or len(self.prompt_template) < 1:
            if self.vector_path:
                self.prompt_template = DEFAULT_QA_PROMPT
                self.prompt_variables = ["question", "context"]
            else:
                self.prompt_template = DEFAULT_CONVERSATION_PROMPT
                self.prompt_variables = ["input", "history"]
        self.prompt = PromptTemplate(
            template=self.prompt_template, input_variables=self.prompt_variables
        )

        self.download_data()
        if self.vector_path and not self.has_vectorstore():
            self.build_vectorstore()
        else:
            log.info(
                f"♻️  Reusing existing vectorstore at {BOLD}{self.vector_path}{END}, skip building the vectorstore"
            )

        log.info(f"🤖 Loading model from {BOLD}{self.model_path}{END}")
        self.llm = self.get_llm()
        if self.has_vectorstore():
            log.info(f"💫 Loading vectorstore from {BOLD}{self.vector_path}{END}")
            self.setup_dbqa()
        if not self.vector_path:
            log.info("🦜 No vectorstore provided, using a generic LLM")

    def download_data(self) -> None:
        """Download data"""
        ddl_list = []
        ddl_list.append({"url": self.model_download, "path": self.model_path})
        ddl_list.append(
            {"url": self.conf.vector.embeddings_download, "path": self.conf.vector.embeddings_path}
        )
        ddl_list.append(
            {"url": self.conf.vector.vector_download, "path": self.conf.vector.vector_path}
        )
        ddl_list.append(
            {"url": self.conf.vector.documents_download, "path": self.conf.vector.documents_path}
        )
        parallel_download(ddl_list, self.conf.info.workers)

    def has_vectorstore(self) -> bool:
        """Check if vectorstore present"""
        return bool(self.vector_path and os.path.exists(self.vector_path))

    def get_vectorstore(self) -> str:
        """Get the vectorstore path"""
        return self.vector_path if self.vector_path and os.path.exists(self.vector_path) else ""

    def get_llm(self, config: Optional[Dict[str, Any]] = None) -> LlamaCpp:
        if not config:
            config = {}
        if "temperature" not in config:
            config["temperature"] = self.conf.llm.temperature
        if "max_new_tokens" not in config:
            config["max_new_tokens"] = self.conf.llm.max_new_tokens
        if "stream" not in config:
            config["stream"] = True
        # if "gpu_layers" not in config:
        #     config["gpu_layers"] = self.conf.llm.gpu_layers if self.device.type != "cpu" else 0
        # if self.device.type != "cpu":
        #     config["n_gpu_layers"] = 40
        #     config["n_batch"] = 512
        return LlamaCpp(
            model_path=self.model_path,
            top_p=1,
            **config
            # model_type=self.conf.llm.model_type,
            # n_gpu_layers=40,  # Change this value based on your model and your GPU VRAM pool.
            # n_batch=512,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
            # temperature=0.01,
            # max_tokens=2000,
            # callback_manager=callback_manager,
            # verbose=True,  # Verbose is required to pass to the callback manager
        )

    def setup_dbqa(self) -> None:
        """Setup the vectorstore for QA"""
        if self.has_vectorstore():
            from qdrant_client import QdrantClient

            embeddings = HuggingFaceEmbeddings(
                model_name=self.conf.vector.embeddings_path, model_kwargs={"device": self.device}
            )
            # FAISS should automatically use GPU?
            # vectorstore = FAISS.load_local(self.get_vectorstore(), embeddings)
            vectorstore = Qdrant(
                QdrantClient(url=self.conf.vector.vector_path),
                collection_name="libre_chat_rag",
                embeddings=embeddings,
            )

            search_args: Dict[str, Any] = {"k": self.conf.vector.return_sources_count}
            if self.conf.vector.score_threshold is not None:
                search_args["score_threshold"] = self.conf.vector.score_threshold
            self.dbqa = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type=self.conf.vector.chain_type,
                retriever=vectorstore.as_retriever(
                    # search_type=self.conf.vector.search_type, search_kwargs=search_args
                ),
                return_source_documents=self.conf.vector.return_sources_count > 0,
                chain_type_kwargs={"prompt": self.prompt},
            )

    def build_vectorstore(self, documents_path: Optional[str] = None) -> Optional[Qdrant]:
        """Build vectorstore from documents."""
        # https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/vectorstores/qdrant.py
        time_start = datetime.now()
        documents_path = documents_path if documents_path else self.conf.vector.documents_path
        docs_count = len(os.listdir(documents_path))
        if docs_count < 1:
            log.warning(
                f"⚠️ No documents found in {documents_path}, vectorstore will not be built, and a generic chatbot will be used until documents are added"
            )
        else:
            log.info(
                f"🏗️ Building the vectorstore from the {BOLD}{CYAN}{docs_count}{END} documents found in {BOLD}{documents_path}{END}, using embeddings from {BOLD}{self.conf.vector.embeddings_path}{END}"
            )
            documents: List[Document] = []
            # Loading all file types provided in the document_loaders object
            for doc_load in self.document_loaders:
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
                chunk_size=self.conf.vector.chunk_size, chunk_overlap=self.conf.vector.chunk_overlap
            )
            splitted_texts = text_splitter.split_documents(documents)
            # TODO: use fastembed?
            embeddings = HuggingFaceEmbeddings(
                model_name=self.conf.vector.embeddings_path, model_kwargs={"device": self.device}
            )
            os.makedirs(str(self.conf.vector.vector_path), exist_ok=True)
            vectorstore = Qdrant.from_documents(
                splitted_texts,
                embeddings,
                # path=self.conf.vector.vector_path,
                url=self.conf.vector.vector_path,
                # prefer_grpc=True,
                collection_name="libre_chat_rag",
                force_recreate=True,
            )
            # vectorstore = FAISS.from_documents(splitted_texts, embeddings)
            # if self.vector_path:
            #     vectorstore.save_local(self.vector_path)
            log.info(f"✅ Vectorstore built in {datetime.now() - time_start}")
            return vectorstore
        return None

    def query(
        self,
        prompt: str,
        memory: Any = None,
        config: Optional[Dict[str, Any]] = None,
        instructions: Optional[str] = None,
        callbacks: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """Query the built LLM"""
        log.info(f"💬 Querying the LLM with prompt: {prompt}")
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")
        if self.vector_path:
            if not self.has_vectorstore():
                return {
                    "result": "The vectorstore has not been built, please go to the [API web UI](/docs) (the green icon at the top right of the page), and upload documents to vectorize."
                }
            # self.setup_dbqa()  # we need to reload the dbqa each time to make sure all workers are up-to-date
            res: Dict[str, Any] = self.dbqa({"query": prompt}, callbacks=callbacks)
            log.debug(f"💭 Complete response from the LLM: {res}")
            for i, doc in enumerate(res["source_documents"]):
                res["source_documents"][i] = {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata,
                }
                if "source" in res["source_documents"][i]["metadata"]:
                    res["source_documents"][i]["metadata"]["filename"] = os.path.basename(
                        res["source_documents"][i]["metadata"]["source"]
                    )
        else:
            # Not using vectostore, generic conversation
            # NOTE: initializing the LLM and conversation at every call to prevent the conversation to take up lot of memory after some time
            # And enable to customize the instructions prompt and temperature for each query
            # Memory is handled at the gradio level
            if not memory:
                memory = ConversationBufferMemory(ai_prefix="AI Assistant", memory_key="history")
            template = instructions if instructions else self.prompt_template
            prompt_template = PromptTemplate(
                template=template, input_variables=self.prompt_variables
            )
            conversation = ConversationChain(
                llm=self.llm,
                prompt=prompt_template,
                verbose=True,
                memory=memory
                # llm=self.get_llm(config), prompt=prompt_template, verbose=True, memory=memory
            )
            resp = conversation.predict(input=prompt, callbacks=callbacks)

            # NOTE: LCEL does not support callbacks handler yet https://github.com/langchain-ai/langchain/issues/14241
            # chat_prompt = ChatPromptTemplate.from_template(template)
            # chat_prompt = ChatPromptTemplate.from_messages(
            #     [
            #         ("system", "You're an assistant who's good at {ability}"),
            #         MessagesPlaceholder(variable_name="history"),
            #         ("human", "{question}"),
            #     ]
            # )
            # output_parser = StrOutputParser()
            # chain = chat_prompt | self.llm | output_parser
            # resp = chain.invoke({"input": prompt}, callbacks=callbacks)

            res = {"result": resp}
        return res

    async def aquery(
        self,
        prompt: str,
        memory: Any = None,
        config: Optional[Dict[str, Any]] = None,
        instructions: Optional[str] = None,
        callbacks: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """Async query the built LLM"""
        log.info(f"💬 Querying the LLM with prompt: {prompt}")
        if len(prompt) < 1:
            raise ValueError("Provide a prompt")
        # TODO: we might need to check if the vectorstore has changed since the last time it was queried,
        # And rerun self.setup_dbqa() if it has changed. Otherwise uploading file will not be applied to all workers
        if self.vector_path:
            if not self.has_vectorstore():
                return {
                    "result": "The vectorstore has not been built, please go to the [API web UI](/docs) (the green icon at the top right of the page), and upload documents to vectorize."
                }
            # TODO: handle history
            # self.setup_dbqa()  # we need to reload the dbqa each time to make sure all workers are up-to-date
            res: Dict[str, Any] = await self.dbqa.acall({"query": prompt}, callbacks=callbacks)
            log.debug(f"💭 Complete response from the LLM: {res}")
            for i, doc in enumerate(res["source_documents"]):
                # doc.to_json() not implemented yet
                res["source_documents"][i] = {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata,
                }
                if "source" in res["source_documents"][i]["metadata"]:
                    res["source_documents"][i]["metadata"]["filename"] = os.path.basename(
                        res["source_documents"][i]["metadata"]["source"]
                    )
        else:
            # Not using vectostore, generic conversation
            if not memory:
                memory = ConversationBufferMemory(ai_prefix="AI Assistant")
            template = instructions if instructions else self.prompt_template
            PromptTemplate(template=template, input_variables=self.prompt_variables)
            conversation = ConversationChain(
                llm=self.llm,
                prompt=self.prompt,
                verbose=True,
                memory=memory,
            )
            resp = await conversation.apredict(input=prompt, callbacks=callbacks)
            res = {"result": resp}
        return res


# "page_content": "Drug repositioning and repurposing for Alzheimer disease\nClive Ballard1",
# "metadata": { "source": "documents/drug_repositioning_for_alzheimer_disease.pdf",
#     "page": 0, "filename": "drug_repositioning_for_alzheimer_disease.pdf" }


DEFAULT_CONVERSATION_PROMPT = """Assistant is a large language model trained by everyone.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
User: {input}
Assistant:"""

DEFAULT_QA_PROMPT = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

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
