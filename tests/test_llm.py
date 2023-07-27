import pytest

from libre_llm.llm import Llm

llm = Llm(vector_path=None)


def test_query_generic_llm():
    """Test capital query to a generic LLM"""
    resp = llm.query("What is the capital of the Netherlands?")
    assert "amsterdam" in resp["result"].lower()


def test_failed_query():
    """Test failed query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"
