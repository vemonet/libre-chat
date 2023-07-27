import pytest

from libre_llm.llm import Llm

llm = Llm()


def test_query():
    """Test failed query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"
