"""Module: Gradio web UI for LangChain chatbot"""
from collections.abc import Iterator
from queue import Empty, Queue
from threading import Thread
from typing import Any, List, Tuple

import gradio as gr
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationBufferMemory

from libre_chat.llm import Llm

RETRY_COMMAND = "/retry"
USER_NAME = "User"
BOT_NAME = "Assistant"
CSS = """.contain { display: flex; flex-direction: column; }
#component-0 { height: 100%; flex-grow: 1; }
#chatbot { flex-grow: 1; }
"""


# https://www.gradio.app/guides/creating-a-custom-chatbot-with-blocks
# https://github.com/hwchase17/conversation-qa-gradio
# https://github.com/gradio-app/gradio/issues/5345
# https://huggingface.co/spaces/HuggingFaceH4/falcon-chat-demo-for-blog/blob/main/app.py
# https://huggingface.co/spaces/HuggingFaceH4/falcon-chat-demo-for-blog
def gradio_app(llm: Llm) -> Any:
    def chat_accordion() -> Tuple[float, int]:
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

    sources_list = []

    def stream(
        input_text: str, memory: Any, instructions: str, temperature: float, max_new_tokens: int
    ) -> "Iterator[Tuple[Any, str]]":
        # Create a Queue
        q: "Queue[Any]" = Queue()
        job_done = object()

        # Create a function to call - this will run in a thread
        def task() -> None:
            config = {
                "temperature": temperature,
                "max_new_tokens": max_new_tokens,
            }
            res = llm.query(
                input_text,
                memory,
                callbacks=[StreamGradioCallback(q)],
                config=config,
                instructions=instructions,
            )
            if "source_documents" in res:
                sources_list.append(res["source_documents"])
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
                content += str(next_token)
                yield next_token, content
            except Empty:
                continue

    def vote(data: gr.LikeData) -> None:
        # TODO: save votes somewhere
        if data.liked:
            print("You upvoted this response: " + data.value)
        else:
            print("You downvoted this response: " + data.value)

    def on_select(evt: gr.SelectData) -> str:
        msg_index = evt.index[0]
        if msg_index < len(sources_list):
            sources_str = f"## 🗃️ Sources\nFor message n°{msg_index}\n"
            for source in sources_list[msg_index]:
                sources_str += (
                    f'### 📄 {source["metadata"]["filename"]}\n{source["page_content"]}\n\n'
                )
            return sources_str
        return ""
        # return f"You selected 【{evt.value}】 at 【{evt.index}】 from 【{evt.target}】"

    # gray https://www.gradio.app/guides/theming-guide#core-colors
    theme = gr.themes.Soft(primary_hue="cyan")
    # theme = 'ParityError/LimeFace',
    # theme = 'bethecloud/storj_theme'
    # .set(slider_color="#FF0000")

    with gr.Blocks(
        theme=theme, css=CSS, analytics_enabled=False, title=llm.conf.info.title
    ) as chat:
        gr.Markdown(f"# {llm.conf.info.title}\n\n{llm.conf.info.description}")
        chatbot = gr.Chatbot(elem_id="chatbot", show_copy_button=True, show_label=False)
        inputs = gr.Textbox(
            placeholder="Ask me anything",
            label="Type a question and press Enter",
            max_lines=5,
        )

        with gr.Row():
            submit_button = gr.Button("📩 Submit question", variant="primary")
            retry_button = gr.Button("♻️ Retry last question")
            delete_turn_button = gr.Button("🧽 Delete last question")
            clear_chat_button = gr.Button("🧹 Delete history", variant="stop")
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
                    lines=6,
                    interactive=True,
                    label="Instructions",
                    max_lines=16,
                    show_label=False,
                )

        sources = gr.Markdown("")

        memory = ConversationBufferMemory(ai_prefix="AI Assistant")

        def run_chat(
            message: str,
            chat_history: List[List[str]],
            instructions: str,
            temperature: float,
            max_new_tokens: int,
        ) -> "Iterator[List[List[str]]]":
            if not message or (message == RETRY_COMMAND and len(chat_history) == 0):
                yield chat_history
                return

            if message == RETRY_COMMAND and chat_history:
                prev_turn = chat_history.pop(-1)
                user_message, _ = prev_turn
                message = user_message
                # TODO: the chat history in the gradio app is properly cleaned, but the LLM built-in memory is not cleaned

            # prompt = format_chat_prompt(message, chat_history, instructions)
            chat_history = [*chat_history, [message, "⏳ Processing your question"]]
            # memory.chat_memory.add_user_message(message)
            yield chat_history
            for next_token, content in stream(
                message, memory, instructions, temperature, max_new_tokens
            ):
                chat_history[-1][1] = content
                yield chat_history
            # memory.chat_memory.add_ai_message(chat_history[-1][1])
            # print(memory.chat_memory.messages)

        def delete_last_turn(chat_history: List[List[str]]) -> Any:
            if chat_history:
                chat_history.pop(-1)
            return {chatbot: gr.update(value=chat_history)}

        def run_retry(
            message: str,
            chat_history: List[List[str]],
            instructions: str,
            temperature: float,
            max_new_tokens: int,
        ) -> "Iterator[List[List[str]]]":
            yield from run_chat(
                RETRY_COMMAND, chat_history, instructions, temperature, max_new_tokens
            )

        def clear_chat() -> List[str]:
            ConversationBufferMemory(ai_prefix="AI Assistant")
            return []

        inputs.submit(
            run_chat,
            [inputs, chatbot, instructions, temperature, max_new_tokens],
            outputs=[chatbot],
            queue=True,
            show_progress="hidden",
        )
        inputs.submit(
            lambda: "", inputs=None, outputs=inputs, queue=False, show_progress="hidden"
        )  # Clear inputs on submit
        submit_button.click(
            run_chat,
            [inputs, chatbot, instructions, temperature, max_new_tokens],
            outputs=[chatbot],
            queue=True,
            show_progress="hidden",
        )
        submit_button.click(
            lambda: "", inputs=None, outputs=inputs, queue=False, show_progress="hidden"
        )
        delete_turn_button.click(delete_last_turn, inputs=[chatbot], outputs=[chatbot], queue=False)
        retry_button.click(
            run_retry,
            [inputs, chatbot, instructions, temperature, max_new_tokens],
            outputs=[chatbot],
            queue=False,
        )
        clear_chat_button.click(clear_chat, [], chatbot, queue=False)

        chatbot.like(vote, None, None, queue=False)
        chatbot.select(on_select, None, sources, queue=False, show_progress="hidden")

    return chat.queue()


class StreamGradioCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q: "Queue[Any]"):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.q.put(token)

    def on_llm_end(self, *args: Any, **kwargs: Any) -> bool:
        return self.q.empty()
