import os
import shutil

import pytest

from libre_chat.llm import Llm
from libre_chat.utils import parse_config

llm = Llm(conf=parse_config("tests/llm-with-vectorstore.yml"))


def test_query_vectorstore():
    """Test capital query to a model with vectorstore"""
    resp = llm.query("What is the capital of the Netherlands?")
    assert len(resp["source_documents"]) >= 1
    assert "amsterdam" in resp["result"].lower()


def test_failed_query():
    """Test failed query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"


def test_build_vectorstore():
    """Test building the vectorstore"""
    shutil.rmtree(llm.conf.vector.vector_path)
    llm.build_vectorstore()
    assert os.path.exists(llm.conf.vector.vector_path)
