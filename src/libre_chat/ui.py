"""Module: Gradio web UI for LangChain chatbot"""
from collections.abc import Generator
from queue import Empty, Queue
from threading import Thread
from typing import Any

import gradio as gr
from langchain.callbacks.base import BaseCallbackHandler

from libre_chat.llm import Llm

RETRY_COMMAND = "/retry"
USER_NAME = "User"
BOT_NAME = "Assistant"


# https://github.com/gradio-app/gradio/issues/5345
# https://huggingface.co/spaces/HuggingFaceH4/falcon-chat-demo-for-blog/blob/main/app.py
# https://huggingface.co/spaces/HuggingFaceH4/falcon-chat-demo-for-blog
def gradio_app(llm: Llm) -> Any:
    def chat_accordion():
        with gr.Accordion("Parameters", open=False):
            temperature = gr.Slider(
                minimum=0,
                maximum=2.0,
                value=0.1,
                step=0.1,
                interactive=True,
                label="Temperature",
            )
            max_new_tokens = gr.Slider(
                minimum=10,
                maximum=llm.conf.llm.max_new_tokens,
                value=llm.conf.llm.max_new_tokens,
                step=1,
                interactive=True,
                label="Max new tokens",
            )
        return temperature, max_new_tokens

    def stream(input_text, history, instructions, temperature, max_new_tokens) -> Generator:
        # Create a Queue
        q = Queue()
        job_done = object()

        # Create a function to call - this will run in a thread
        def task() -> None:
            config = {
                "temperature": temperature,
                "max_new_tokens": max_new_tokens,
            }
            llm.query(
                input_text,
                history,
                callbacks=[StreamGradioCallback(q)],
                config=config,
                instructions=instructions,
            )
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

    with gr.Blocks() as chat:
        chatbot = gr.Chatbot(elem_id="chatbot", show_copy_button=True)
        inputs = gr.Textbox(
            placeholder="Ask me anything",
            label="Type a question and press Enter",
            max_lines=5,
        )

        with gr.Row():
            retry_button = gr.Button("♻️ Retry last turn")
            delete_turn_button = gr.Button("🧽 Delete last turn")
            clear_chat_button = gr.Button("🧹 Delete all history")
            # clear = gr.ClearButton([msg, chatbot])

        gr.Examples(
            llm.conf.info.examples,
            inputs=inputs,
            label="Click on any example and press Enter in the input textbox!",
        )

        with gr.Row(elem_id="param_container"):
            with gr.Column():
                temperature, max_new_tokens = chat_accordion()
            with gr.Column(), gr.Accordion("Instructions", open=False):
                instructions = gr.Textbox(
                    placeholder="LLM instructions",
                    value=llm.conf.prompt.template,
                    lines=10,
                    interactive=True,
                    label="Instructions",
                    max_lines=16,
                    show_label=False,
                )

        def run_chat(
            message: str, chat_history, instructions: str, temperature: float, max_new_tokens: float
        ):
            if not message or (message == RETRY_COMMAND and len(chat_history) == 0):
                yield chat_history
                return

            if message == RETRY_COMMAND and chat_history:
                prev_turn = chat_history.pop(-1)
                user_message, _ = prev_turn
                message = user_message
                # TODO: the chat history in the gradio app is properly cleaned, but the LLM built-in memory is not cleaned

            # prompt = format_chat_prompt(message, chat_history, instructions)
            chat_history = [*chat_history, [message, "Processing your question ⏳"]]
            yield chat_history
            for next_token, content in stream(
                message, chat_history, instructions, temperature, max_new_tokens
            ):
                chat_history[-1][1] = content
                yield chat_history

        def delete_last_turn(chat_history):
            if chat_history:
                chat_history.pop(-1)
            return {chatbot: gr.update(value=chat_history)}

        def run_retry(
            message: str, chat_history, instructions: str, temperature: float, max_new_tokens: float
        ):
            yield from run_chat(
                RETRY_COMMAND, chat_history, instructions, temperature, max_new_tokens
            )

        def clear_chat():
            return []

        inputs.submit(
            run_chat,
            [inputs, chatbot, instructions, temperature, max_new_tokens],
            outputs=[chatbot],
            show_progress=False,
        )
        # inputs.submit(lambda: "", inputs=None, outputs=inputs)
        delete_turn_button.click(delete_last_turn, inputs=[chatbot], outputs=[chatbot])
        retry_button.click(
            run_retry,
            [inputs, chatbot, instructions, temperature, max_new_tokens],
            outputs=[chatbot],
            show_progress=False,
        )
        clear_chat_button.click(clear_chat, [], chatbot)

        chatbot.like(vote, None, None)

        # def user(user_message, history):
        #     return "", [*history, [user_message, None]]

        # def bot(history):
        #     print("history!!", history)
        #     history[-1][1] = ""
        #     for next_token, content in stream(history[-1][0], history):
        #         history[-1][1] = content
        #         yield history

        # inputs.submit(user, [inputs, chatbot], [inputs, chatbot], queue=False).then(bot, chatbot, chatbot)
        # chatbot.like(vote, None, None)

        # # def clear_interaction():
        # #     # Reset the chat history and input text when retry is clicked
        # #     chatbot.history = []
        # #     msg.update("")

        # def retry_interaction():
        #     history = inputs.history
        #     print(history)
        #     print(chat.history)
        #     # Reset the chat history and input text when retry is clicked
        #     history[-1][1] = ""
        #     inputs.submit(user, [history[-1][0], chatbot], [chatbot.history[-1][0], chatbot], queue=False).then(bot, chatbot, chatbot)
        #     # msg.update("")

        # # clear.click(clear_interaction, None, chatbot, queue=False)
        # # retry.click(retry_interaction, None, chatbot, queue=False)

    return chat.queue()


class StreamGradioCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.q.put(token)

    def on_llm_end(self, *args, **kwargs: Any) -> None:
        return self.q.empty()

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


# def format_chat_prompt(message: str, chat_history, instructions: str) -> str:
#     instructions = instructions.strip(" ").strip("\n")
#     prompt = instructions
#     for turn in chat_history:
#         user_message, bot_message = turn
#         prompt = f"{prompt}\n{USER_NAME}: {user_message}\n{BOT_NAME}: {bot_message}"
#     prompt = f"{prompt}\n{USER_NAME}: {message}\n{BOT_NAME}:"
#     return prompt
