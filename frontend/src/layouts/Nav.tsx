import { createEffect, createSignal } from "solid-js";
import {useStore} from '@nanostores/solid'
import {$chatConfig, setConfig, apiUrl} from '../components/nanostores'


export default function Nav() {
  const chatConfig = useStore($chatConfig)

  createEffect(async () => {
    const response = await fetch(`${apiUrl}/config`);
    const data = await response.json();
    setConfig(data)
  });

  // const location = useLocation();
  // const active = (path: string) =>
  //   path == location.pathname
  //     ? "border-sky-600"
  //     : "border-transparent hover:border-sky-600";

  const [theme, setTheme] = createSignal("dark");
  const toggleTheme = () => {
    const newTheme = theme() === "light" ? "dark" : "light";
    setTheme(newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  return (
    <div class="navbar bg-base-300 min-h-0 p-0">
      <div class="navbar-start">
        {/* <ul class="menu menu-horizontal px-1 hidden lg:flex">
          <li><a href="/">Home</a></li>
          <li><a href="/admin">Admin</a></li>
        </ul>
        <div class="dropdown lg:hidden">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
          </div>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
            <li><a href="/">Home</a></li>
            <li><a href="/admin">Admin</a></li>
          </ul>
        </div> */}
      </div>

      <div class="navbar-center">
        {/* <a class="btn btn-ghost text-xl">daisyUI</a> */}
        <div class="text-xl font-thin">
          {chatConfig().info.title}
        </div>
      </div>

      <div class="navbar-end">
        {/* Desktop */}
        <div class="space-x-3 hidden items-center lg:flex">
          {/* Add light/dark theme switch */}
          <label class="cursor-pointer grid place-items-center">
            <input type="checkbox" onClick={toggleTheme} value="dark" checked class="toggle theme-controller bg-base-content row-start-1 col-start-1 col-span-2"/>
            <svg class="col-start-1 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
            <svg class="col-start-2 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          </label>
          <a href="/gradio/" target="_blank" data-tooltip="Gradio UI">
              <button class="p-1 rounded-lg hover:bg-gray-500">
                  <img class="h-5" src="/gradio_logo.svg" />
              </button>
          </a>
          <a href="/docs" target="_blank" data-tooltip="OpenAPI documentation">
              <button class="p-1 rounded-lg hover:bg-gray-500">
                  <img class="h-5" src="/openapi_logo.svg" />
              </button>
          </a>
          <a href={chatConfig().info.repository_url} target="_blank" rel="noopener noreferrer">
              <button data-tooltip="Source code" class="px-2 py-1 mr-8 rounded-lg hover:bg-gray-500">
                  <i class="fab fa-github text-xl" />
              </button>
          </a>
        </div>

        {/* Mobile */}
        <div class="dropdown dropdown-end lg:hidden">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
          </div>
          <ul tabindex="0" class="menu menu-sm dropdown-content items-center mt-3 z-[1] p-2 shadow bg-base-100 rounded-box dropdown-left">
            {/* <li>
              <label class="cursor-pointer grid place-items-center">
                <input type="checkbox" onClick={toggleTheme} value="dark" checked class="toggle theme-controller bg-base-content row-start-1 col-start-1 col-span-2"/>
                <svg class="col-start-1 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
                <svg class="col-start-2 row-start-1 stroke-base-100 fill-base-100" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
              </label>
            </li> */}
            <li>
              <a href="/gradio/" target="_blank" data-tooltip="Gradio UI">
                <img class="h-5" src="/gradio_logo.svg" />
              </a>
            </li>
            <li>
              <a href="/docs" target="_blank" data-tooltip="OpenAPI documentation">
                <img class="h-5" src="/openapi_logo.svg" />
              </a>
            </li>
            <li>
              <a href={chatConfig().info.repository_url} target="_blank" rel="noopener noreferrer">
                <i class="fab fa-github text-xl" />
              </a>
            </li>
          </ul>
        </div>
      </div>

    </div>
  );
}
