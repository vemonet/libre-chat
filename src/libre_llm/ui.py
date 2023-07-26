from typing import List

import gradio as gr

from libre_llm.config import log
from libre_llm.llm import query_llm

DESCRIPTION = """Chat with llama2, hosted at Maastrich University

See the API documentation at [/docs](/docs)
"""


def gradio_app(dbqa):
    def get_chatbot_resp(message: str, history: List[tuple[str, str]]) -> str:
        log.debug(f"Running inference for: {message}")
        res = query_llm(dbqa, message, history)
        history.append((message, res))
        return message

    # https://www.gradio.app/guides/creating-a-chatbot-fast
    # https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
    chat = gr.ChatInterface(
        get_chatbot_resp,
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Ask me anything", container=False, scale=7),
        title="🦙 llama2 chat",
        description=DESCRIPTION,
        theme="soft",
        examples=["What is the capital of the Netherlands?", "Are tomatoes vegetables?"],
        cache_examples=False,  # Error in GitHub action when enabled
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear",
    )
    return gr.routes.App.create_app(chat)
