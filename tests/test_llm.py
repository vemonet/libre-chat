import os
import shutil

import pytest

from libre_chat.conf import parse_conf
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


# def test_query_vectorstore_drug() -> None:
#     """Test capital query with vectorstore for PDF"""
#     resp = llm.query("Which drugs can be used to mitigate Alzheimer symptoms??")
#     assert len(resp["source_documents"]) >= 1


def test_failed_empty_query() -> None:
    """Test failed empty query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        llm.query("")
    assert str(exc_info.value) == "Provide a prompt"


@pytest.mark.asyncio
async def test_failed_empty_aquery() -> None:
    """Test failed empty query to LLM"""
    with pytest.raises(ValueError) as exc_info:
        await llm.aquery("")
    assert str(exc_info.value) == "Provide a prompt"


def test_build_vectorstore() -> None:
    """Test building the vectorstore"""
    shutil.rmtree(llm.conf.vector.vector_path)
    llm.build_vectorstore()
    assert os.path.exists(llm.conf.vector.vector_path)
    # And with providing a docs path
    shutil.rmtree(llm.conf.vector.vector_path)
    llm.build_vectorstore(documents_path="documents")
    assert os.path.exists(llm.conf.vector.vector_path)


def test_build_failed_no_docs() -> None:
    """Test fail building the vectorstore when no documents"""
    llm_empt = Llm(
        conf=parse_conf("config/chat-vectorstore-qa.yml"), documents_path="tests/tmp/nothinghere"
    )
    shutil.rmtree(llm.conf.vector.vector_path)
    # with pytest.raises(ValueError) as exc_info:
    llm_empt.build_vectorstore()
    res = llm.query("anything")
    assert "vectorstore has not been built" in res["result"]
    assert not os.path.exists(llm.conf.vector.vector_path)
    # assert "No documents found" in str(exc_info.value)


def test_similarity_score_threshold() -> None:
    """Test similarity_score_threshold with vectorstore"""
    Llm(
        conf=parse_conf("config/chat-vectorstore-qa.yml"),
        search_type="similarity_score_threshold",
        score_threshold=0.4,
    )
    resp = llm.query(capital_query)
    assert len(resp["source_documents"]) >= 1


def test_documents_dir_dont_exist() -> None:
    """Test documents dir created if doesn't exist"""
    tmp_docs = "tests/tmp/docs"
    Llm(conf=parse_conf("config/chat-conversation.yml"), documents_path=tmp_docs)
    assert os.path.exists(tmp_docs)


def test_llm_failed_no_prompt_variables() -> None:
    """Test fail building Llm when no prompt variable provided"""
    with pytest.raises(Exception) as exc_info:
        Llm(conf=parse_conf("config/chat-vectorstore-qa.yml"), prompt_variables=[])
    assert "You should provide at least 1 template variable" in str(exc_info.value)


def test_no_prompt_template() -> None:
    """Test no prompt templates provided"""
    conf_conv = parse_conf("config/chat-conversation.yml")
    conf_conv.prompt.template = ""
    llm_conv = Llm(conf=conf_conv)
    assert "{input}" in llm_conv.prompt_template
    conf_qa = parse_conf("config/chat-vectorstore-qa.yml")
    conf_qa.prompt.template = ""
    llm_qa = Llm(conf=conf_qa)
    assert "{question}" in llm_qa.prompt_template


# @patch("torch.cuda.is_available")
# @patch("torch.cuda.device")
# def test_cuda(mock_device: MagicMock, mock_is_available: MagicMock) -> None:
#     """Pretend we have GPU, but run on cpu anyway"""
#     mock_device.return_value = "cpu"
#     mock_is_available.return_value = True
#     llm = Llm(conf=parse_conf("tests/config/additional-prop.yml"))
#     assert llm is not None


# def test_failed_query_no_result() -> None:
#     """Test failed query to LLM return no result"""
#     with patch.object(llm, "dbqa") as mock_dbqa:
#         mock_dbqa.return_value = {"source_documents": []}
#         with pytest.raises(Exception) as exc_info:
#             llm.query("Nothing")
#         assert "No result was returned by the LLM" in str(exc_info.value)
