"""Module: Gradio web UI for LangChain chatbot"""
from collections.abc import Generator
from queue import Empty, Queue
from threading import Thread
from typing import Any

import gradio as gr
from langchain.callbacks.base import BaseCallbackHandler

from libre_chat.llm import Llm


# https://github.com/gradio-app/gradio/issues/5345
def gradio_app(llm: Llm) -> Any:
    def stream(input_text, history) -> Generator:
        # Create a Queue
        q = Queue()
        job_done = object()

        print(input_text)

        # Create a function to call - this will run in a thread
        def task() -> None:
            llm.query(input_text, history, callbacks=[StreamGradioCallback(q)])
            q.put(job_done)

        # Create a thread and start the function
        t = Thread(target=task)
        t.start()
        content = ""
        # Get each new token from the queue and yield for our generator
        while True:
            try:
                next_token = q.get(True, timeout=1)
                if next_token is job_done:
                    break
                content += next_token
                yield next_token, content
            except Empty:
                continue

    def vote(data: gr.LikeData):
        # TODO: save vote in a db
        if data.liked:
            print("You upvoted this response: " + data.value)
        else:
            print("You downvoted this response: " + data.value)

    # async def get_chatbot_resp(message: str, history: List[Tuple[str, str]]) -> Any:
    #     log.debug(f"Running inference for: {message}, with message history: {history}")
    #     for next_token, content in stream(message):
    #         yield (content)

    # https://www.gradio.app/guides/creating-a-chatbot-fast
    # https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
    # chat = gr.ChatInterface(
    #     get_chatbot_resp,
    #     chatbot=gr.Chatbot(height=600),
    #     textbox=gr.Textbox(placeholder="Ask me anything", container=False, scale=7),
    #     title=llm.conf.info.title,
    #     description=llm.conf.info.description,
    #     theme="soft",
    #     examples=llm.conf.info.examples,
    #     cache_examples=False,  # Error in GitHub action tests when enabled
    # )

    with gr.Blocks() as chat:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def user(user_message, history):
            return "", [*history, [user_message, None]]

        def bot(history):
            print("history!!", history)
            history[-1][1] = ""
            for next_token, content in stream(history[-1][0], history):
                history[-1][1] = content
                yield history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
        chatbot.like(vote, None, None)
        clear.click(lambda: None, None, chatbot, queue=False)

    return chat.queue()


class StreamGradioCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.q.put(token)

    def on_llm_end(self, *args, **kwargs: Any) -> None:
        return self.q.empty()
