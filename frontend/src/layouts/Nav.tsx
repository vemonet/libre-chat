import { createEffect } from "solid-js";

import {useStore} from '@nanostores/solid'
import {$chatConfig, setConfig, apiUrl} from '../components/nanostores'


export default function Nav() {
  const chatConfig = useStore($chatConfig)

  createEffect(async () => {
    const response = await fetch(`${apiUrl}/config`);
    const data = await response.json();
    setConfig({api: apiUrl as string, ...data})
    console.log("CONF", chatConfig())
  });

  // const location = useLocation();
  // const active = (path: string) =>
  //   path == location.pathname
  //     ? "border-sky-600"
  //     : "border-transparent hover:border-sky-600";

  // const [theme, setTheme] = createSignal("dark");
  // const toggleTheme = () => {
  //   const newTheme = theme() === "light" ? "dark" : "light";
  //   setTheme(newTheme);
  //   document.documentElement.setAttribute("data-theme", newTheme);
  // };

  return (
    <nav class="bg-gray-200 dark:bg-gray-900 text-black dark:text-white">
      <div class="nav-btns-desktop flex justify-between items-center">
        {/* Left-side menu */}
        <div></div>
        {/* <ul class="flex p-3 text-gray-200">
          <li class={`border-b-2 ${active("/")} mx-1.5 sm:mx-6`}>
            <a href="/">Home</a>
          </li>
          <li class={`border-b-2 ${active("/about")} mx-1.5 sm:mx-6`}>
            <a href="/about">About</a>
          </li>
        </ul> */}

        <div class="text-xl font-thin">
          {chatConfig().info.title}
        </div>

        <div class="flex">
          {/* Add light/dark theme switch */}
          {/* <label class="cursor-pointer grid place-items-center">
            <input type="checkbox" onClick={toggleTheme} value="dark" class="toggle theme-controller bg-base-content row-start-1 col-start-1 col-span-2"/>
            <svg class="col-start-1 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
            <svg class="col-start-2 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          </label> */}
          {/* <a href="/gradio" target="_blank" rel="noopener noreferrer" data-tooltip="Gradio UI"
              class="text-black hover:text-black dark:text-white">
              <button class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                  <img class="h-5" src="https://gradio-theme-soft.hf.space/assets/logo-3707f936.svg" />
              </button>
          </a> */}
          <a href="/docs" target="_blank" rel="noopener noreferrer" data-tooltip="OpenAPI documentation"
              class="text-black hover:text-black dark:text-white">
              <button class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                  <img class="h-5" src="https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg" />
              </button>
          </a>
          <a href={chatConfig().info.repository_url} target="_blank" rel="noopener noreferrer"
              class="text-black hover:text-black dark:text-white">
              <button data-tooltip="Source code" class="px-4 py-2 mr-6 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                  <i class="fab fa-github text-xl"></i>
              </button>
          </a>
        </div>
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
              <a href={chatConfig().info.repository_url} target="_blank" rel="noopener noreferrer" class="text-black hover:text-black dark:text-white">
                  <button data-tooltip="Source code" class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500">
                      <i class="fab fa-github text-xl"></i>
                  </button>
              </a>
          </div>
      </div>
    </nav>
  );
}
