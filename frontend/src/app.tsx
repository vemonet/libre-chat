// @refresh reload
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start";
import { createContext, createEffect, createSignal, Suspense } from "solid-js";
import Nav from "~/components/Nav";
import "./app.css";

const default_conf = {
  apiUrl: window.origin,
  info: {
    title: "Libre Chat",
    description: "Open source chatbot",
    repository_url: "https://github.com/vemonet/libre-chat",
    favicon: "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png",
    examples: [
      "What is the capital of the Netherlands?"
    ]
  }
}

export const ChatContext = createContext([default_conf, () => {}]);

export default function App() {
  const [conf, setConf]: any = createSignal(default_conf);

  createEffect(async () => {
    const apiUrl = import.meta.env.VITE_API_URL || window.origin;
    const response = await fetch(`${apiUrl}/config`);
    const data = await response.json();
    setConf({apiUrl, ...data});
  });

  return (
    <ChatContext.Provider value={[conf, setConf]}>
      <Router
        root={(props) => (
          <div class="flex flex-col h-screen">
            <Nav />
            <Suspense>{props.children}</Suspense>
          </div>
        )}
      >
        <FileRoutes />
      </Router>
    </ChatContext.Provider>
  );
}
