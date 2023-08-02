import os
import shutil
from unittest.mock import MagicMock, patch

import pytest

from libre_chat.chat_conf import parse_conf
from libre_chat.llm import Llm

llm = Llm(conf=parse_conf("config/chat-vectorstore-qa.yml"))
capital_query = "What is the capital of the Netherlands?"


def test_query_vectorstore_capital() -> None:
    """Test capital query with vectorstore for PDF"""
    resp = llm.query(capital_query)
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


def test_failed_empty_query() -> None:
    """Test failed empty query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"


@patch("libre_chat.llm.Llm.dbqa")
def test_failed_query_no_result(mock_run: MagicMock) -> None:
    """Test failed query to LLM return no result"""
    mock_run.return_value = {"source_documents": []}
    with pytest.raises(ValueError) as exc_info:
        llm.query("Nothing")
    assert "No result was returned by the LLM" in str(exc_info.value)


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


# TODO: add test similarity_search
def test_similarity_score_threshold() -> None:
    """Test similarity_score_threshold with vectorstore"""
    Llm(
        conf=parse_conf("config/chat-vectorstore-qa.yml"),
        search_type="similarity_score_threshold",
        score_threshold=0.4,
    )
    resp = llm.query(capital_query)
    assert len(resp["source_documents"]) >= 1


def test_no_conf_file() -> None:
    """Test no conf file found"""
    conf = parse_conf("nothinghere.yml")
    assert len(conf.llm.model_path) > 2


def test_documents_dir_dont_exist() -> None:
    """Test documents dir created if doesn't exist"""
    tmp_docs = "tests/tmp/docs"
    Llm(conf=parse_conf("config/chat-conversation.yml"), documents_path=tmp_docs)
    assert os.path.exists(tmp_docs)
