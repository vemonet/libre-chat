"""
===========================================
        Module: Open-source LLM Setup
===========================================
"""
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.vectorstores import FAISS

from libre_llm.config import LlmConfig


def build_llm(cfg: LlmConfig):
    # Local CTransformers model
    return CTransformers(
        model=cfg.MODEL_PATH,
        model_type=cfg.MODEL_TYPE,
        config={"max_new_tokens": cfg.MAX_NEW_TOKENS, "temperature": cfg.TEMPERATURE},
    )


def set_qa_prompt(qa_prompt: str):
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=qa_prompt, input_variables=["context", "question"])
    return prompt


def build_retrieval_qa(cfg: LlmConfig, llm, prompt, vectordb):
    dbqa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": cfg.VECTOR_COUNT}),
        return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
        chain_type_kwargs={"prompt": prompt},
    )
    return dbqa


def setup_dbqa(cfg: LlmConfig = LlmConfig()):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    )
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    llm = build_llm(cfg)
    qa_prompt = set_qa_prompt(cfg.QA_TEMPLATE)
    dbqa = build_retrieval_qa(cfg, llm, qa_prompt, vectordb)

    return dbqa
