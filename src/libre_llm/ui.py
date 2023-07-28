"""Module: web UI for LLM"""
from typing import List, Optional, Tuple

import gradio as gr

from libre_llm.utils import log, settings


def gradio_app(
    llm,
    title: str = settings.info.title,
    description: str = settings.info.description,
    examples: Optional[List[str]] = None,
):
    # TODO: title, description, examples
    def get_chatbot_resp(message: str, history: List[Tuple[str, str]]) -> str:
        log.debug(f"Running inference for: {message}, with message history: {history}")
        res = llm.query(message, history)
        # gradio auto add the response at the top of the list instead of the bottom
        # history.append((res, None))
        # history.insert(0, (None, res))
        return res["result"]

    if not examples:
        examples = settings.info.examples
    # https://www.gradio.app/guides/creating-a-chatbot-fast
    # https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
    chat = gr.ChatInterface(
        get_chatbot_resp,
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(placeholder="Ask me anything", container=False, scale=7),
        title=title,
        description=description,
        theme="soft",
        examples=examples,
        cache_examples=False,  # Error in GitHub action when enabled
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear",
    )
    return gr.routes.App.create_app(chat)
