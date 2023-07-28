"""Module: web UI for LLM"""
from typing import List, Tuple

import gradio as gr

from libre_llm.utils import log


def gradio_app(llm):
    def get_chatbot_resp(message: str, history: List[Tuple[str, str]]) -> str:
        log.debug(f"Running inference for: {message}, with message history: {history}")
        res = llm.query(message, history)
        # gradio auto add the response at the top of the list instead of the bottom
        # history.append((res, None))
        # history.insert(0, (None, res))
        return res["result"]

    # https://www.gradio.app/guides/creating-a-chatbot-fast
    # https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
    chat = gr.ChatInterface(
        get_chatbot_resp,
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(placeholder="Ask me anything", container=False, scale=7),
        title=llm.conf.info.title,
        description=llm.conf.info.description,
        theme="soft",
        examples=llm.conf.info.examples,
        cache_examples=False,  # Error in GitHub action when enabled
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear",
    )
    return gr.routes.App.create_app(chat)
