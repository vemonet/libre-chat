import{d as y,k as $,c as C,g as S,i as M,f as E,r as j,s as n,t as A}from"./web.zg9RI5L8.js";import{p as T,$ as B,a as I,s as N}from"./nanostores.RVhpkXze.js";var U=A('<nav class=bg-base-300><div class="nav-btns-desktop flex justify-between items-center"><div></div><div class="text-xl font-thin"></div><div class="flex space-x-2"><label class="cursor-pointer grid place-items-center"><input type=checkbox value=dark checked class="toggle theme-controller bg-base-content row-start-1 col-start-1 col-span-2"><svg class="col-start-1 row-start-1 stroke-base-100 fill-base-100"xmlns=http://www.w3.org/2000/svg width=14 height=14 viewBox="0 0 24 24"fill=none stroke=currentColor stroke-width=2 stroke-linecap=round stroke-linejoin=round><circle cx=12 cy=12 r=5></circle><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"></path></svg><svg class="col-start-2 row-start-1 stroke-base-100 fill-base-100"xmlns=http://www.w3.org/2000/svg width=14 height=14 viewBox="0 0 24 24"fill=none stroke=currentColor stroke-width=2 stroke-linecap=round stroke-linejoin=round><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></label><a href=/gradio/ target=_blank data-tooltip="Gradio UI"><button class="px-4 py-3 rounded-lg hover:bg-gray-300"><img class=h-5 src=/gradio_logo.svg></button></a><a href=/docs target=_blank data-tooltip="OpenAPI documentation"><button class="px-4 py-3 rounded-lg hover:bg-gray-500"><img class=h-5 src=/openapi_logo.svg></button></a><a target=_blank rel="noopener noreferrer"><button data-tooltip="Source code"class="px-4 py-2 mr-6 rounded-lg hover:bg-gray-500"><i class="fab fa-github text-xl"></i></button></a></div></div><div class="nav-btns-mobile flex gap-1 absolute top-2 right-3"><button data-tooltip=Menu id=mobile-nav-btn class="px-4 py-2 rounded-lg hover:bg-gray-500"><i class="fas fa-bars"></i></button><div id=nav-btns-mobile class=hidden><a href=/docs target=_blank rel="noopener noreferrer"class="text-black hover:text-black dark:text-white"><button data-tooltip-target=tooltip-api class="px-4 py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500"><img class=h-5 src=https://raw.github.com/vemonet/libre-chat/main/docs/docs/assets/openapi_logo.svg></button></a><a target=_blank rel="noopener noreferrer"class="text-black hover:text-black dark:text-white"><button data-tooltip="Source code"class="px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-slate-500"><i class="fab fa-github text-xl">');function H(){const o=T(B);$(async()=>{const a=await(await fetch(`${I}/config`)).json();N(a)});const[c,d]=C("dark"),g=()=>{const t=c()==="light"?"dark":"light";d(t),document.documentElement.setAttribute("data-theme",t)};return(()=>{var t=S(U),a=t.firstChild,b=a.firstChild,r=b.nextSibling,h=r.nextSibling,s=h.firstChild,p=s.firstChild,v=s.nextSibling,u=v.nextSibling,f=u.nextSibling,x=a.nextSibling,k=x.firstChild,m=k.nextSibling,w=m.firstChild,_=w.nextSibling;return M(r,()=>o().info.title),p.$$click=g,E(e=>{var l=o().info.repository_url,i=o().info.repository_url;return l!==e.e&&n(f,"href",e.e=l),i!==e.t&&n(_,"href",e.t=i),e},{e:void 0,t:void 0}),j(),t})()}y(["click"]);export{H as default};
