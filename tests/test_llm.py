import pytest

from libre_llm.llm import Llm
from libre_llm.utils import parse_config

settings = parse_config("tests/llm-with-vectorstore.yml")
llm = Llm(
    model_path=settings.llm.model_path,
    model_type=settings.llm.model_type,
    model_download=settings.llm.model_download,
    embeddings_path=settings.vector.embeddings_path,
    embeddings_download=settings.vector.embeddings_download,
    vector_path=settings.vector.vector_path,
    vector_download=settings.vector.vector_download,
    documents_path=settings.vector.documents_path,
    max_new_tokens=settings.llm.max_new_tokens,
    temperature=settings.llm.temperature,
    return_source_documents=settings.vector.return_source_documents,
    vector_count=settings.vector.vector_count,
    chunk_size=settings.vector.chunk_size,
    chunk_overlap=settings.vector.chunk_overlap,
    template_variables=settings.template.variables,
    template_prompt=settings.template.prompt,
)


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
