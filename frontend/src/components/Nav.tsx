import { useLocation } from "@solidjs/router";

export default function Nav() {
  const location = useLocation();
  const active = (path: string) =>
    path == location.pathname
      ? "border-sky-600"
      : "border-transparent hover:border-sky-600";

  const conf = {
    title: "Libre Chat",
    description: "Hey `there`",
    repo_url: "https://github.com/vemonet/libre-chat",
    favicon: "https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/logo.png",
    examples: [
      "What is the capital of the Netherlands?"
    ]
  }

  return (
    <nav class="bg-gray-200 dark:bg-gray-900 text-black dark:text-white">
      <div class="nav-btns-desktop flex space-x-1 items-center">
        <ul class="flex p-3 text-gray-200">
          <li class={`border-b-2 ${active("/")} mx-1.5 sm:mx-6`}>
            <a href="/">Home</a>
          </li>
          <li class={`border-b-2 ${active("/about")} mx-1.5 sm:mx-6`}>
            <a href="/about">About</a>
          </li>
        </ul>
        <div style={{"flex-grow": 1}}></div>
        {/* <button data-tooltip="Switch theme" id="theme-switch-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
            <i id="sun-icon" class="fas fa-sun"></i>
            <i id="moon-icon" class="fas fa-moon hidden"></i>
        </button> */}
        <a href="/gradio" target="_blank" rel="noopener noreferrer" data-tooltip="Gradio UI"
            class="text-black hover:text-black dark:text-white">
            <button class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                <img class="h-5" src="https://gradio-theme-soft.hf.space/assets/logo-3707f936.svg" />
            </button>
        </a>
        <a href="/docs" target="_blank" rel="noopener noreferrer" data-tooltip="OpenAPI documentation"
            class="text-black hover:text-black dark:text-white">
            <button class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                <img class="h-5" src="https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg" />
            </button>
        </a>
        <a href={conf.repo_url} target="_blank" rel="noopener noreferrer"
            class="text-black hover:text-black dark:text-white">
            <button data-tooltip="Source code" class="px-4 py-2 mr-6 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                <i class="fab fa-github text-xl"></i>
            </button>
        </a>
    </div>
    {/* Nav on mobile */}
    <div class="nav-btns-mobile flex gap-1 absolute top-2 right-3">
        <button data-tooltip="Menu" id="mobile-nav-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
            <i class="fas fa-bars"></i>
        </button>
        <div id="nav-btns-mobile" class="hidden">
            {/* <!-- <button data-tooltip="Switch theme" id="theme-switch-btn" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                <i id="sun-icon" class="fas fa-sun"></i>
                <i id="moon-icon" class="fas fa-moon hidden"></i>
            </button> --> */}
            <a href="/docs" target="_blank" rel="noopener noreferrer" class="text-black hover:text-black dark:text-white">
                <button data-tooltip-target="tooltip-api" class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                    <img class="h-5" src="https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg" />
                </button>
            </a>
            <a href={conf.repo_url} target="_blank" rel="noopener noreferrer" class="text-black hover:text-black dark:text-white">
                <button data-tooltip="Source code" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                    <i class="fab fa-github text-xl"></i>
                </button>
            </a>
        </div>
    </div>
    </nav>
  );
}
