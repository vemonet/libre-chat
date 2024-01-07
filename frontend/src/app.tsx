// @refresh reload
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start";
import { createContext, Suspense } from "solid-js";
import Nav from "~/components/Nav";
import "./app.css";

const ChatContext = createContext("default value");

export default function App() {
  return (
    <ChatContext.Provider value="new value">
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
