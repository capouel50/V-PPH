if(!self.define){let e,i={};const s=(s,l)=>(s=new URL(s+".js",l).href,i[s]||new Promise((i=>{if("document"in self){const e=document.createElement("script");e.src=s,e.onload=i,document.head.appendChild(e)}else e=s,importScripts(s),i()})).then((()=>{let e=i[s];if(!e)throw new Error(`Module ${s} didn’t register its module`);return e})));self.define=(l,r)=>{const n=e||("document"in self?document.currentScript.src:"")||location.href;if(i[n])return;let c={};const o=e=>s(e,n),u={module:{uri:n},exports:c,require:o};i[n]=Promise.all(l.map((e=>u[e]||o(e)))).then((e=>(r(...e),c)))}}define(["./workbox-d169e1d7"],(function(e){"use strict";e.setCacheNameDetails({prefix:"PPH"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.f2f5eb75.css",revision:null},{url:"/css/chunk-vendors.b30114d5.css",revision:null},{url:"/fonts/Bellota-Light.0277ce35.ttf",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNa.4ad034d2.woff",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.13749f83.woff2",revision:null},{url:"/guest-particlesjs-config.json",revision:"aab449b324c5a17b76401ad39f50090b"},{url:"/img/blanc.2f72339c.jpg",revision:null},{url:"/img/capsule2.efa435a4.png",revision:null},{url:"/img/controle2.ee12c8bc.jpg",revision:null},{url:"/img/demande3.593b0d7f.jpg",revision:null},{url:"/img/gelules.e6c37735.png",revision:null},{url:"/img/health_hazard.61e5836e.png",revision:null},{url:"/img/molecule.f42c6dc4.jpg",revision:null},{url:"/index.html",revision:"602799faa07252477b4d1c8dd552fe53"},{url:"/js/app.9c291167.js",revision:null},{url:"/js/chunk-vendors.e46602c8.js",revision:null},{url:"/js/scichart2d.wasm",revision:"c877aae470fed25dc7ad4c1f553c19bc"},{url:"/js/scichart3d.wasm",revision:"5073d246b3d59b315823ab0b30441f43"},{url:"/manifest.json",revision:"db757eeca087be67892aa54e776c72e9"},{url:"/particlesjs-config.json",revision:"5a44728a5d93b079d7375160c4ac15d2"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"},{url:"/scichart2d.data",revision:"711c69b91556d7faa5746029de92fa86"},{url:"/scichart3d.data",revision:"4e048a7d74ce9f15578cfae36b98e2ad"}],{})}));
//# sourceMappingURL=service-worker.js.map
