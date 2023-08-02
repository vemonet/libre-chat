import os
import shutil

import pytest

from libre_chat.chat_conf import parse_conf
from libre_chat.llm import Llm

llm = Llm(conf=parse_conf("config/chat-vectorstore-qa.yml"))


def test_query_vectorstore_capital() -> None:
    """Test capital query with vectorstore for PDF"""
    resp = llm.query("What is the capital of the Netherlands?")
    assert len(resp["source_documents"]) >= 1
    assert "amsterdam" in resp["result"].lower()


def test_query_vectorstore_gdp() -> None:
    """Test GDP query with vectorstore for CSV"""
    resp = llm.query("What was the GDP of France in 1998?")
    assert len(resp["source_documents"]) >= 1


def test_query_vectorstore_drug() -> None:
    """Test capital query with vectorstore for PDF"""
    resp = llm.query("Which drugs can be used to mitigate Alzheimer symptoms??")
    assert len(resp["source_documents"]) >= 1


def test_failed_query() -> None:
    """Test failed query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"


def test_build_vectorstore() -> None:
    """Test building the vectorstore"""
    shutil.rmtree(llm.conf.vector.vector_path)
    llm.build_vectorstore()
    assert os.path.exists(llm.conf.vector.vector_path)


def test_build_failed_no_docs() -> None:
    """Test fail building the vectorstore when no documents"""
    llm_empt = Llm(
        conf=parse_conf("config/chat-vectorstore-qa.yml"), documents_path="tests/tmp/nothinghere"
    )
    shutil.rmtree(llm.conf.vector.vector_path)
    llm_empt.build_vectorstore()
    assert not os.path.exists(llm_empt.conf.vector.vector_path)
