if(!self.define){let e,s={};const i=(i,l)=>(i=new URL(i+".js",l).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(l,n)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(s[r])return;let o={};const c=e=>i(e,r),u={module:{uri:r},exports:o,require:c};s[r]=Promise.all(l.map((e=>u[e]||c(e)))).then((e=>(n(...e),o)))}}define(["./workbox-5b385ed2"],(function(e){"use strict";e.setCacheNameDetails({prefix:"PPH"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.e63e37c9.css",revision:null},{url:"/css/chunk-vendors.d81ba0ba.css",revision:null},{url:"/fonts/Bellota-Light.0277ce35.ttf",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNa.4ad034d2.woff",revision:null},{url:"/fonts/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.13749f83.woff2",revision:null},{url:"/guest-particlesjs-config.json",revision:"aab449b324c5a17b76401ad39f50090b"},{url:"/img/capsule2.efa435a4.png",revision:null},{url:"/img/gelules.e6c37735.png",revision:null},{url:"/img/molecule.f42c6dc4.jpg",revision:null},{url:"/index.html",revision:"1e4bd3cd6f20b3454600604083162d4c"},{url:"/js/app.2d6788ca.js",revision:null},{url:"/js/chunk-vendors.c2acaf34.js",revision:null},{url:"/manifest.json",revision:"629c49e8179ec2ae20fb5c76f49dcc44"},{url:"/particlesjs-config.json",revision:"5a44728a5d93b079d7375160c4ac15d2"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map
