/* eslint-disable solid/no-innerhtml */
import { createSignal, For } from 'solid-js';
import {useStore} from '@nanostores/solid'
import {$chatConfig, apiUrl} from '../components/nanostores'
import {marked} from 'marked';
import DOMPurify from 'dompurify';

export default function Chat() {
  const chatConfig = useStore($chatConfig)

  const [messages, setMessages] = createSignal([
		{message: "How can I help you today?", type: "bot", sources: []}
	]);
  const [prompt, setPrompt] = createSignal("");
  // const [selectedSource, setSelectedSource]: any = createSignal(null);
  const [warningMsg, setWarningMsg] = createSignal("");
  const [loading, setLoading] = createSignal(false);
  let socket: WebSocket;
  let chatContainer: any;

  const appendMessage = (message: string, type = "bot") => {
    setMessages(messages => [...messages, { message, type, sources: [] }]);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  };

  // Submit user input
	function handleSubmit(event: Event) {
		event.preventDefault();
		submitInput()
	}
	function handleInput(event: any) {
		setPrompt(event.target.innerText);
	}

	function handleKeyPress(event: any) {
		if (event.key === 'Enter' && !event.shiftKey) {
			// Submit the form when Enter is pressed without Shift
			event.preventDefault();
			submitInput();
		}
	}

	// Send the user input to the chat API
	function submitInput() {
		if (loading()) {
			setWarningMsg("⏳ Thinking...");
			return
		}
		if (prompt().trim() !== "") {
			appendMessage(prompt(), "user");
			// TODO: next line needed to reset placeholder
			// if (userInput) userInput.innerText = '';
			const params = {
				prompt: prompt(),
			};
			socket.send(JSON.stringify(params));
      setLoading(true);
			setPrompt('');
		}
	}

  // Create a new WebSocket connection
	function createWebSocket(baseUrl: Location | URL) {
		const protocol = baseUrl.protocol === "https:" ? "wss:" : "ws:";
		const websocketUrl = `${protocol}//${baseUrl.host}/chat`;
		console.log(`🔌 Connecting to ${websocketUrl}`);
		socket = new WebSocket(websocketUrl);
		socket.onopen = () => {
			console.log("🔌 Connected to the API websocket");
		};
		socket.onclose = (event) => {
			console.warn("WebSocket closed with code:", event.code, "reason:", event.reason);
      setLoading(false);
			// Attempt to reconnect after a delay
			setTimeout(() => {
				console.log("♻️ Attempting to reconnect...");
				createWebSocket(baseUrl);
			}, 2000); // 2s delay before attempting to reconnect
		};
		socket.onerror = (error) => {
			console.error("WebSocket error:", error);
			appendMessage("An error happened, please retry.")
      setLoading(false);
		};

		// Receive response from the websocket
		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.type === "start") {
				appendMessage("", "bot");
			} else if (data.type === "stream") {
				// console.log("STREAM", data.message)
        setMessages(messages => {
          const newMessages = [...messages];
          const lastIndex = newMessages.length - 1;
          if (lastIndex >= 0) {
            newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              message: newMessages[lastIndex].message + data.message
            };
          }
          return newMessages;
        });
			} else if (data.type === "end") {
				if (data.sources) {
          setMessages(messages => {
            const newMessages = [...messages];
            const lastIndex = newMessages.length - 1;
            if (lastIndex >= 0) {
              newMessages[lastIndex] = {
                ...newMessages[lastIndex],
                sources: data.sources
              };
            }
            return newMessages;
          });
        }
        console.log("Messages:", messages())
        setLoading(false);
        setWarningMsg("");
			}
		};
	};
  const chatUrl = new URL(`${apiUrl}/chat`)
  createWebSocket(chatUrl)

  return (
    <main class="flex flex-col overflow-y-auto flex-grow">
      <div ref={chatContainer} id="chat-container" class="flex-grow overflow-y-auto">

          {/* Website description */}
          <div class="container mx-auto px-2 max-w-5xl">
              <div class="py-4 text-center font-thin" innerHTML={DOMPurify.sanitize(marked.parse(chatConfig().info.description).toString())} />
          </div>

          {/* Chat messages */}
          <div id="chat-thread" class="w-full border-t border-slate-500">
              <For each={messages()}>{(msg, iMsg) =>
                  // messageElement.className = `border-b border-slate-500 ${sender === "user" ? "bg-gray-100 dark:bg-gray-700" : "bg-gray-200 dark:bg-gray-600 hidden"}`;
                  <div class={`border-b border-slate-500 ${msg.type === "user" ? "bg-accent" : "bg-secondary"}`}>
                    <div class="px-2 py-8 mx-auto max-w-5xl">
                      <article class="prose max-w-full" innerHTML={DOMPurify.sanitize(marked.parse(msg.message).toString())} />
                      {/* Add sources when RAG */}
                      { msg.sources.length > 0 &&
                        <For each={msg.sources}>{(source: any, iSource) =>
                          <>
                            <button class="m-2 px-3 py-1 text-sm bg-accent hover:bg-base-100 rounded-lg"
                              // @ts-ignore
                              onClick={()=>document.getElementById(`source_modal_${iMsg()}_${iSource()}`)?.showModal()}
                            >
                              {source.metadata.filename}
                            </button>
                            <dialog id={`source_modal_${iMsg()}_${iSource()}`} class="modal">
                              <div class="modal-box">
                                <h3 class="font-bold text-lg">📖 {source.metadata.filename} [p. {source.metadata.page}]</h3>
                                <p class="py-4">
                                  {source.page_content}
                                </p>
                              </div>
                              <form method="dialog" class="modal-backdrop">
                                <button>close</button>
                              </form>
                            </dialog>
                          </>
                        }</For>
                      }
                    </div>
                  </div>
                }
              </For>
          </div>
      </div>

      <div>
        {/* Warning message */}
        { warningMsg().length > 0 &&
          <div class="text-center">
            <div id="warning-card" class="bg-orange-300 p-2 text-orange-900 text-sm rounded-lg font-semibold mb-2 hidden inline-block" />
          </div>
        }

        {/* List of examples */}
        <div class="py-2 px-4 justify-center items-center text-xs flex space-x-2" id="example-buttons">
          <For each={chatConfig().info.examples}>{(example) =>
            <button onClick={() => {setPrompt(example) ; submitInput()}} class="px-4 py-1 bg-neutral-content text-slate-600 rounded-lg hover:bg-slate-400">
              {example}
            </button>
          }</For>
        </div>

        {/* User input */}
        <form class="p-2 flex" id="chat-form" onSubmit={(e) => handleSubmit(e)}>
          <div class="container flex mx-auto max-w-5xl">
              <div id="user-input" contenteditable={true} style="height: max-content;"
                  class="flex-grow px-4 py-2 border border-slate-500 rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
                  // @ts-ignore
                  placeholder="Ask something..."
                  onInput={(e) => handleInput(e)}
                  onKeyDown={(e) => handleKeyPress(e)}
              />
              <button type="submit" id="submit-btn" class="ml-2 px-4 py-2 rounded-lg text-slate-400 bg-slate-600 hover:bg-slate-700">
                { loading() ? (
                  <i id="loading-spinner" class="fas fa-spinner fa-spin"/>
                ) : (
                  <i id="send-icon" class="fas fa-paper-plane"/>
                )}
              </button>
          </div>
        </form>
      </div>
    </main>
  );
}
