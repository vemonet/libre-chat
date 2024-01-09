import {atom} from 'nanostores';

interface ChatConfig {
  info: any;
  llm: any;
  vector: any;
}

// api: process.env.PUBLIC_API_URL ? process.env.PUBLIC_API_URL : 'https://chat.semanticscience.org'
export const $chatConfig = atom<ChatConfig>({
  info: {
    title: "Libre Chat",
    description: "Open source chatbot",
    repository_url: "https://github.com/vemonet/libre-chat",
    favicon: "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png",
    examples: [
      "What is the capital of the Netherlands?"
    ]
  },
  llm: {},
  vector: {},
});

export function setConfig(chatConfig: ChatConfig) {
  $chatConfig.set(chatConfig);
}

export const apiUrl = import.meta.env.PUBLIC_API_URL || window.origin;
