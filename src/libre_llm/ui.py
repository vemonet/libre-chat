"""Module: web UI for LLM"""
from typing import List, Tuple

import gradio as gr

from libre_llm.utils import defaults, log

DESCRIPTION = """Chat with llama2, hosted at Maastrich University

See the API documentation at [/docs](/docs)

[Source code on GitHub](https://github.com/vemonet/libre-llm)
"""


def gradio_app(
    llm,
    title: str = defaults.title,
    description: str = defaults.description,
    examples: List[str] = [defaults.example_prompt],
):
    # TODO: title, description, examples
    def get_chatbot_resp(message: str, history: List[Tuple[str, str]]) -> str:
        log.debug(f"Running inference for: {message}")
        log.debug(f"With message history: {history}")
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
