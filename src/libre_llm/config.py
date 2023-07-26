import logging
from dataclasses import dataclass


@dataclass
class LlmConfig:
    MODEL_PATH: str = "models/llama-2-7b-chat.ggmlv3.q3_K_L.bin"
    MODEL_TYPE: str = "llama"
    RETURN_SOURCE_DOCUMENTS: bool = True
    VECTOR_COUNT: float = 2
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    DATA_PATH: str = "data/"
    DB_FAISS_PATH: str = "vectorstore/db_faiss"
    MAX_NEW_TOKENS: int = 256
    TEMPERATURE: float = 0.01
    QA_TEMPLATE = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
    # MODEL_TYPE: 'mpt'
    # MODEL_BIN_PATH: 'models/mpt-7b-instruct.ggmlv3.q8_0.bin'
    # MODEL_BIN_PATH: str = 'models/llama-2-7b-chat.ggmlv3.q8_0.bin'


log = logging.getLogger("uvicorn")
# log.propagate = False
# log.setLevel(logging.getLevelName("INFO"))
# console_handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s %(levelname)s: [%(module)s:%(funcName)s] %(message)s")
# console_handler.setFormatter(formatter)
# log.addHandler(console_handler)
