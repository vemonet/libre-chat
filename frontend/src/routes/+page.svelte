<script lang='ts'>
	// import Counter from './Counter.svelte';
	// import welcome from '$lib/images/svelte-welcome.webp';
	// import welcome_fallback from '$lib/images/svelte-welcome.png';
	import {onMount} from 'svelte';
	import {marked} from 'marked';

	const conf = {
		title: "Libre Chat",
		description: "Hey `there`",
		repo_url: "https://github.com/vemonet/libre-chat",
		favicon: "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png",
		examples: [
			"What is the capital of the Netherlands?"
		]
	}

	let warningMsg = ""
	let loading = false
	const messages = [
		{message: "How can I help you today?", type: "bot"}
	]
	let prompt = '';
	let socket: WebSocket;

	// Submit user input
	function handleSubmit(event: Event) {
		event.preventDefault();
		submitInput()
	}

	function handleInput(event: any) {
		prompt = event.target.innerText;
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
		if (loading) {
			warningMsg = "⏳ Thinking...";
			return
		}
		// const prompt = userInput.innerText;
		if (prompt.trim() !== "") {
			appendMessage(prompt, "user");
			// userInput.innerText = "";
			loading = true
			prompt = '';
			// TODO: next line needed to reset placeholder
			// if (userInput) userInput.innerText = '';
			const params = {
				prompt: prompt,
			};
			socket.send(JSON.stringify(params));
		}
	}

	let msgCount = 0
	function appendMessage(message: string, sender = "bot") {
		msgCount += 1
		messages.push({message: message, type: sender})
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
			loading = false
			// Attempt to reconnect after a delay
			setTimeout(() => {
				console.log("♻️ Attempting to reconnect...");
				createWebSocket(baseUrl);
			}, 2000); // 2s delay before attempting to reconnect
		};
		socket.onerror = (error) => {
			console.error("WebSocket error:", error);
			appendMessage("An error happened, please retry.")
			loading = false
		};

		// Receive response from the websocket
		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.type === "start") {
				appendMessage("", "bot");
			} else if (data.type === "stream") {
				console.log("STREAM", data.message)
				// const lastMsg = chatThread.lastElementChild
				// if (lastMsg.classList.contains("hidden")) chatThread.lastElementChild.classList.remove("hidden")
				// const p = lastMsg.lastElementChild.lastElementChild.lastElementChild;
				// p.innerHTML += data.message;
			} else if (data.type === "end") {
				// TODO: if (data.sources) appendSources(data.sources)
				loading = false
				warningMsg = ""
				// chatContainer.scrollTop = chatContainer.scrollHeight
			}
		};
	}

	onMount(() => {
		// TODO: for prod use: createWebSocket(window.location)
		const baseUrl = new URL("http://127.0.0.1:8000/chat")
		createWebSocket(baseUrl)
		// const protocol = baseUrl.protocol === "https:" ? "wss:" : "ws:";
		// const websocketUrl = `${protocol}//${baseUrl.host}/chat`;
		// console.log(`🔌 Connecting to ${websocketUrl}!!`);
		// socket = new WebSocket(websocketUrl);
		// socket.onopen = () => {
		// 	console.log("🔌 Connected to the API websocket!!");
		// };

		// const welcomeMsg = "Hello! How can I help you today?";
		const description = document.getElementById("description");
		const userInput = document.getElementById("user-input");
		const submitBtn = document.getElementById("submit-btn");
		const sendIcon = document.getElementById("send-icon");
		const loadingSpinner = document.getElementById("loading-spinner");
		// description.innerHTML = marked.parse(description.innerHTML.trim());


		// Warning card to send users messages
		// const warningCard = document.getElementById("warning-card");
		// function showWarning(message) {
		// 	warningCard.textContent = message;
		// 	warningCard.style.display = "inline-block";
		// }
		// function hideWarning() {
		// 	warningCard.style.display = "none";
		// }


		// Generate example buttons dynamically
		// const exampleButtons = document.getElementById("example-buttons");
		// const exampleStrings = conf.examples;
		// exampleStrings.forEach(example => {
		// 	const button = document.createElement("button");
		// 	button.textContent = example;
		// 	button.className = "px-4 py-1 bg-slate-300 text-slate-600 rounded-lg hover:bg-gray-400";
		// 	button.dataset.example = example;
		// 	button.addEventListener("click", function() {
		// 		userInput.textContent = example;
		// 		submitInput(userInput);
		// 	});
		// 	exampleButtons.appendChild(button);
		// });

		// Append a message to the chat
		const chatContainer = document.getElementById("chat-container");
		const chatThread = document.getElementById("chat-thread");
		const chatForm = document.getElementById("chat-form");
		// let msgCount = 0
		// function appendMessage(message: string, sender = "bot") {
		// 	msgCount += 1
		// 	messages.push({message: message, type: sender})
		// 	const messageElement = document.createElement("div");
		// 	const iconHtml = sender === "user" ?
		// 		'<i class="fas fa-user-astronaut text-xl mr-4"></i>' : // fa-comment fa-user-secret fa-user-astronaut
		// 		'<i class="fas fa-robot text-xl mr-4"></i>';
		// 	messageElement.className = `border-b border-slate-400 ${sender === "user" ? "bg-gray-100 dark:bg-gray-700" : "bg-gray-200 dark:bg-gray-600 hidden"}`;
		// 	messageElement.innerHTML = `<div class="px-2 py-8 mx-auto max-w-5xl">
		// 		<div class="container flex items-center">
		// 			${iconHtml}
		// 			<div>
		// 				<article class="prose dark:prose-invert max-w-full">
		// 					${marked(message)}
		// 				</article>
		// 			</div>
		// 		</div>
		// 	</div>`;
		// 	chatThread.appendChild(messageElement);
		// 	return messageElement
		// }
		// appendMessage(welcomeMsg, "bot")

		// Append sources documents in QA
		// function appendSources(source_documents) {
		// 	const messageElement = chatThread.lastElementChild;
		// 	let sourcesBtnHtml = ""
		// 	let sourcesCardHtml = ""
		// 	let sourcesHtml = ""
		// 	const encounteredFilenames = new Set();
		// 	if (source_documents && source_documents.length > 0) {
		// 		for (const [i, doc] of source_documents.entries()) {
		// 			const sourceId = doc.metadata.filename ? doc.metadata.filename : (i+1).toString()
		// 			const pageBit = doc.metadata.hasOwnProperty("page") ? ` [p. ${doc.metadata.page.toString()}]` : ""
		// 			sourcesCardHtml += `
		// 				<article class="prose dark:prose-invert bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 mx-3">
		// 					📖 ${sourceId}${pageBit}<br/>
		// 					${doc.page_content}
		// 				</article>`;
		// 			// Add button only if different file
		// 			if (!encounteredFilenames.has(sourceId)) {
		// 				encounteredFilenames.add(sourceId);
		// 				// Add sources button once per filename
		// 				sourcesBtnHtml += `<button id="source-btn-${msgCount}-${i}" class="my-3 px-3 py-1 text-sm bg-gray-300 hover:bg-gray-400 dark:bg-gray-700 dark:hover:bg-gray-800 rounded-lg">${sourceId}</button>&nbsp;&nbsp;`
		// 			}
		// 		}
		// 		// Combine all display cards for this message sources
		// 		sourcesHtml += `<div id="source-card-${msgCount}" class="hidden flex">${sourcesCardHtml}</div>`
		// 	}
		// 	messageElement.lastElementChild.innerHTML += sourcesBtnHtml;
		// 	messageElement.lastElementChild.innerHTML += sourcesHtml;
		// 	// Add click event on each source document
		// 	if (source_documents && source_documents.length > 0) {
		// 		const card = document.getElementById(`source-card-${msgCount}`);
		// 		const sourceButtons = document.querySelectorAll(`[id^='source-btn-${msgCount}-']`);
		// 		sourceButtons.forEach(button => {
		// 			button.addEventListener("click", function() {
		// 				if (card.classList.contains("hidden")) {
		// 					card.classList.remove("hidden")
		// 					sourceButtons.forEach(btn => {
		// 						btn.classList.add("dark:bg-gray-800", "bg-gray-400");
		// 						btn.classList.remove("dark:bg-gray-700", "bg-gray-300");
		// 					});
		// 				} else {
		// 					card.classList.add("hidden")
		// 					sourceButtons.forEach(btn => {
		// 						btn.classList.remove("dark:bg-gray-800", "bg-gray-400");
		// 						btn.classList.add("dark:bg-gray-700", "bg-gray-300");
		// 					});
		// 				}
		// 			});
		// 		})
		// 	}
		// }

		// Function to show the tooltip content on click
		function showTooltipContent(event) {
			const tooltip = event.target.getAttribute("data-tooltip");
			if (tooltip) {
				window.alert(tooltip);
			}
		}
		// Attach click event to all <code> elements
		const codeElements = document.getElementsByTagName("code");
		for (const codeElement of codeElements) {
			codeElement.addEventListener("click", showTooltipContent);
		}

		// function enableLoading() {
		// 	loadingSpinner.classList.remove("hidden");
		// 	sendIcon.classList.add("hidden");
		// 	submitBtn.disabled = true;
		// }
		// function disableLoading() {
		// 	chatContainer.scrollTop = chatContainer.scrollHeight
		// 	loadingSpinner.classList.add("hidden");
		// 	sendIcon.classList.remove("hidden");
		// 	submitBtn.disabled = false;
		// }


		// Submit form when hit enter, or click submit button
		// userInput.addEventListener("keydown", function(event) {
		// 	chatContainer.scrollTop = chatContainer.scrollHeight;
		// 	if (event.key === "Enter" && !event.shiftKey) {
		// 		event.preventDefault();
		// 		submitInput(userInput);
		// 	}
		// });
		// chatForm.addEventListener("submit", function(event) {
		// 	event.preventDefault();
		// 	submitInput(userInput)
		// });
		// Add a placeholder when empty
		function togglePlaceholder() {
			if (userInput.textContent.trim() === "") userInput.innerHTML = "";
		}
		userInput.addEventListener("input", togglePlaceholder);
		togglePlaceholder();


		// Light/dark theme setup, default to dark if nothing found
		const sunIcon = document.getElementById("sun-icon");
		const moonIcon = document.getElementById("moon-icon");
		function toggleIcons() {
			const isDarkMode = document.documentElement.classList.contains("dark");
			if (isDarkMode) {
				sunIcon.classList.remove("hidden");
				moonIcon.classList.add("hidden");
			} else {
				sunIcon.classList.add("hidden");
				moonIcon.classList.remove("hidden");
			}
		}
		let prefersDark = true
		if (window.matchMedia) prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		document.documentElement.classList.toggle('dark', prefersDark);
		toggleIcons();
		const themeSwitchBtn = document.getElementById("theme-switch-btn");
		function toggleDarkMode() {
			const doc = document.documentElement;
			doc.classList.toggle("dark");
			toggleIcons();
		}
		themeSwitchBtn.addEventListener("click", toggleDarkMode);


		// Toggle mobile navigation menu
		const mobileNavBtn = document.getElementById("mobile-nav-btn");
		const navBtnsMobile = document.getElementById("nav-btns-mobile");
		mobileNavBtn.addEventListener("click", () => {
			navBtnsMobile.classList.toggle("hidden");
		});
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section class="bg-gray-100 dark:bg-gray-800 text-black dark:text-white">
	<div class="flex flex-col h-screen w-full">

        <!-- Main chat container -->
        <div id="chat-container" class="flex-grow overflow-y-auto">

            <!-- Title, top nav, and description -->
            <div class="container mx-auto px-2 max-w-5xl">
                <div class="container mx-auto max-w-5xl p-4 border-b border-slate-300 dark:border-slate-600 flex justify-center items-center">
                    <h2 class="text-xl font-semibold flex">
                        <img class="h-8 mr-3" src={conf.favicon}>
                        {conf.title}
                    </h2>
                    <!-- Top nav buttons -->
                    <div class="nav-btns-desktop flex space-x-1 absolute top-2 right-8">
                        <button data-tooltip="Switch theme" id="theme-switch-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                            <i id="sun-icon" class="fas fa-sun"></i>
                            <i id="moon-icon" class="fas fa-moon hidden"></i>
                        </button>
                        <a href="/docs" target="_blank" rel="noopener noreferrer" data-tooltip="OpenAPI documentation"
                            class="text-black hover:text-black dark:text-white">
                            <button class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                                <img class="h-5" src="https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg">
                            </button>
                        </a>
                        <a href={conf.repo_url} target="_blank" rel="noopener noreferrer"
                            class="text-black hover:text-black dark:text-white">
                            <button data-tooltip="Source code" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                                <i class="fab fa-github text-xl"></i>
                            </button>
                        </a>
                    </div>
                    <!-- Nav on mobile -->
                    <div class="nav-btns-mobile flex gap-1 absolute top-2 right-3">
                        <button data-tooltip="Menu" id="mobile-nav-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                            <i class="fas fa-bars"></i>
                        </button>
                        <div id="nav-btns-mobile" class="hidden">
                            <!-- <button data-tooltip="Switch theme" id="theme-switch-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                                <i id="sun-icon" class="fas fa-sun"></i>
                                <i id="moon-icon" class="fas fa-moon hidden"></i>
                            </button> -->
                            <a href="/docs" target="_blank" rel="noopener noreferrer" class="text-black hover:text-black dark:text-white">
                                <button data-tooltip-target="tooltip-api" class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                                    <img class="h-5" src="https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg">
                                </button>
                            </a>
                            <a href={conf.repo_url} target="_blank" rel="noopener noreferrer" class="text-black hover:text-black dark:text-white">
                                <button data-tooltip="Source code" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                                    <i class="fab fa-github text-xl"></i>
                                </button>
                            </a>
                        </div>
                    </div>
					<!-- End nav -->
                </div>
				<!-- Website description -->
                <div class="py-4 text-center">
					{@html marked.parse(conf.description)}
                </div>
            </div>

            <div id="chat-thread" class="w-full border-t border-slate-400">
                <!-- Chat messages will be appended here -->
				{#each messages as msg, index}
					<!-- messageElement.className = `border-b border-slate-400 ${sender === "user" ? "bg-gray-100 dark:bg-gray-700" : "bg-gray-200 dark:bg-gray-600 hidden"}`; -->
					<div class="border-b border-slate-400">
						<div class="px-2 py-8 mx-auto max-w-5xl">
							<div class="container flex items-center">
								{#if msg.type == "user"}
									<!-- fa-comment fa-user-secret fa-user-astronaut -->
									<i class="fas fa-user-astronaut text-xl mr-4"></i>
								{:else}
									<i class="fas fa-robot text-xl mr-4"></i>
								{/if}
								<div>
									<article class="prose dark:prose-invert max-w-full">
										${marked(msg.message)}
									</article>
								</div>
							</div>
						</div>
					</div>
				{/each}
            </div>
        </div>

        <!-- Warning message -->
		{#if warningMsg.length > 0}
			<div class="text-center">
				<div id="warning-card" class="bg-orange-300 p-2 text-orange-900 text-sm rounded-lg font-semibold mb-2 hidden inline-block"></div>
			</div>
		{/if}

        <!-- List of examples -->
        <div class="py-2 px-4 justify-center items-center text-xs flex space-x-2" id="example-buttons">
			{#each conf.examples as example, index}
				<button on:click={() => {
						prompt = example
						submitInput()
					}} class="px-4 py-1 bg-slate-300 text-slate-600 rounded-lg hover:bg-gray-400">
					{example}
				</button>
			{/each}
		</div>

        <!-- User input border-t border-slate-400 dark:border-slate-500 -->
        <form class="p-2 flex" id="chat-form" on:submit={handleSubmit}>
            <div class="container flex mx-auto max-w-5xl">
                <div id="user-input" contenteditable="true" style="height: max-content;"
                    class="flex-grow px-4 py-2 border border-slate-400 dark:border-slate-500 rounded-lg focus:outline-none focus:ring focus:ring-blue-200 dark:focus:ring-blue-400"
                    placeholder="Send a message..."
					on:input={handleInput} on:keydown={handleKeyPress}
                ></div>
                <button type="submit" id="submit-btn" class="ml-2 px-4 py-2 rounded-lg text-slate-500 bg-slate-200 hover:bg-slate-300 dark:text-slate-400 dark:bg-slate-700 dark:hover:bg-slate-600">
					{#if loading}
						<i id="loading-spinner" class="hidden fas fa-spinner fa-spin"></i>
					{:else}
						<i id="send-icon" class="fas fa-paper-plane"></i>
					{/if}
                </button>
            </div>
        </form>
    </div>
</section>

<style>
	/* section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	} */
</style>
