import { createSignal, For } from 'solid-js';
import {marked} from 'marked';

export default function Home() {
  const [messages, setMessages] = createSignal([
		{message: "How can I help you today?", type: "bot", sources: []}
	]);
  const [prompt, setPrompt] = createSignal("");
  const [selectedSource, setSelectedSource]: any = createSignal(null);
  const [warningMsg, setWarningMsg] = createSignal("");
  const [loading, setLoading] = createSignal(false);
  let socket: WebSocket;
  let chatContainer: any;

  // TODO: Retrieve from API
  const conf = {
		title: "Libre Chat",
		description: "Hey `there`",
		repo_url: "https://github.com/vemonet/libre-chat",
		favicon: "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png",
		examples: [
			"What is the capital of the Netherlands?"
		]
	}

  const appendMessage = (message: string, type = "bot") => {
    setMessages(messages => [...messages, { message, type, sources: [] }]);
    setLoading(false);
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
		console.log("submitInput")
		if (loading()) {
			setWarningMsg("⏳ Thinking...");
			return
		}
		if (prompt().trim() !== "") {
			appendMessage(prompt(), "user");
			// userInput.innerText = "";
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
			appendMessage("Sorry, an error happened, please retry.")
			// Attempt to reconnect after a delay
			setTimeout(() => {
				console.log("♻️ Attempting to reconnect...");
				createWebSocket(baseUrl);
			}, 2000); // 2s delay before attempting to reconnect
		};
		socket.onerror = (error) => {
			console.error("WebSocket error:", error);
			appendMessage("An error happened, please retry.")
		};

		// Receive response from the websocket
		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.type === "start") {
				appendMessage("", "bot");
			} else if (data.type === "stream") {
				console.log("STREAM", data.message)
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
        console.log(messages())
        setLoading(false);
        setWarningMsg("");
			}
		};
	};
  // https://chat.semanticscience.org/chat
  const chatUrl = new URL("https://chat.semanticscience.org/chat")
  // const chatUrl = new URL("http://127.0.0.1:8000/chat")
  // const currentLocation = window.location;
  // const protocol = currentLocation.protocol === "https:" ? "wss:" : "ws:";
  // const websocketUrl = `${protocol}//${currentLocation.host}/chat`;
  createWebSocket(chatUrl)

  // <main class="text-center mx-auto text-gray-700 p-4">
  return (
    <main class="flex flex-col bg-gray-100 dark:bg-gray-800 text-black dark:text-white" style={{"flex-grow": 1, "overflow-y": "auto"}}>

      <div ref={chatContainer} id="chat-container" class="flex-grow overflow-y-auto">

          {/* Website description */}
          <div class="container mx-auto px-2 max-w-5xl">
              <div class="py-4 text-center" innerHTML={marked.parse(conf.description).toString()}>
              </div>
          </div>

          {/* Chat messages */}
          <div id="chat-thread" class="w-full border-t border-slate-400">
              <For each={messages()}>{(msg, i) =>
                  // messageElement.className = `border-b border-slate-400 ${sender === "user" ? "bg-gray-100 dark:bg-gray-700" : "bg-gray-200 dark:bg-gray-600 hidden"}`;
                  <div class={`border-b border-slate-400 ${msg.type === "user" ? "bg-gray-100 dark:bg-gray-700" : "bg-gray-200 dark:bg-gray-600"}`}>
                    <div class="px-2 py-8 mx-auto max-w-5xl">
                      <div class="container flex items-center">
                        {msg.type === "user" ? (
                          <i class="fas fa-user-astronaut text-xl mr-4"></i>
                        ) : (
                          <i class="fas fa-robot text-xl mr-4"></i>
                        )}
                        <div>
                          <article class="prose dark:prose-invert max-w-full" innerHTML={marked.parse(msg.message).toString()}>
                          </article>
                          {/* TODO: add sources */}
                          { msg.sources.length > 0 &&
                            <>
                              <For each={msg.sources}>{(source: any, i) =>
                                  <button class="m-2 px-3 py-1 text-sm bg-gray-300 hover:bg-gray-400 dark:bg-gray-700 dark:hover:bg-gray-800 rounded-lg"
                                    onClick={() => setSelectedSource(selectedSource() === source ? null : source)}
                                  >
                                    {source.metadata.filename}
                                  </button>
                              }</For>
                              {selectedSource() &&
                                <article class="prose dark:prose-invert bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 mx-3">
                                  📖 {selectedSource().metadata.filename} [p. {selectedSource().metadata.page}]<br/>
                                  {selectedSource().page_content}
                                </article>
                              }
                            </>
                          }
                        </div>
                      </div>
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
            <div id="warning-card" class="bg-orange-300 p-2 text-orange-900 text-sm rounded-lg font-semibold mb-2 hidden inline-block"></div>
          </div>
        }

        {/* List of examples */}
        <div class="py-2 px-4 justify-center items-center text-xs flex space-x-2" id="example-buttons">
          <For each={conf.examples}>{(example, i) =>
            <button onClick={() => {setPrompt(example) ; submitInput()}} class="px-4 py-1 bg-slate-300 text-slate-600 rounded-lg hover:bg-gray-400">
              {example}
            </button>
          }</For>
        </div>

        {/* User input border-t border-slate-400 dark:border-slate-500 */}
        <form class="p-2 flex" id="chat-form" onSubmit={(e) => handleSubmit(e)}>
          <div class="container flex mx-auto max-w-5xl">
              <div id="user-input" contenteditable={true} style="height: max-content;"
                  class="flex-grow px-4 py-2 border border-slate-400 dark:border-slate-500 rounded-lg focus:outline-none focus:ring focus:ring-blue-200 dark:focus:ring-blue-400"
                  // placeholder="Send a message..."
                  onInput={(e) => handleInput(e)}
                  onKeyDown={(e) => handleKeyPress(e)}
              ></div>
              <button type="submit" id="submit-btn" class="ml-2 px-4 py-2 rounded-lg text-slate-500 bg-slate-200 hover:bg-slate-300 dark:text-slate-400 dark:bg-slate-700 dark:hover:bg-slate-600">
                { loading() ? (
                  <i id="loading-spinner" class="hidden fas fa-spinner fa-spin"></i>
                ) : (
                  <i id="send-icon" class="fas fa-paper-plane"></i>
                )}
              </button>
          </div>
        </form>
      </div>

      {/* <h1 class="max-6-xs text-6xl text-sky-700 font-thin uppercase my-16">
        Hello world!
      </h1>
      <Counter />
      <p class="mt-8">
        Visit{" "}
        <a
          href="https://solidjs.com"
          target="_blank"
          class="text-sky-600 hover:underline"
        >
          solidjs.com
        </a>{" "}
        to learn how to build Solid apps.
      </p>
      <p class="my-4">
        <span>Home</span>
        {" - "}
        <A href="/about" class="text-sky-600 hover:underline">
          About Page
        </A>{" "}
      </p> */}
    </main>
  );
}
