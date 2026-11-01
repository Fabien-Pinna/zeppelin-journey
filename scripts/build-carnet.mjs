import { writeFile } from "node:fs/promises";
import { islands, exhibits } from "../src/features/journey/world.js";
const escape = (text) =>
  text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll('"', "&quot;");
const links = islands
  .map((i) => `<a href="#${i.id}">${i.number} · ${escape(i.short)}</a>`)
  .join("");
const entries = islands
  .map((i) => {
    const e = exhibits[i.id];
    return `<article id="${i.id}"><p class="label">${i.number} / ${escape(e.label)}</p><h2>${escape(e.title)}</h2>${e.paragraphs.map((p) => `<p>${escape(p)}</p>`).join("")}<small>${escape(e.note)}</small></article>`;
  })
  .join("");
await writeFile(
  new URL("../public/projects.html", import.meta.url),
  `<!doctype html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Le carnet de Fabien — Zeppelin Journey</title><meta name="description" content="Neuf étapes du parcours de Fabien : entrepôt, maçonnerie, agriculture, trapèze au Club Med, cirque, Backroads, autodidacte, O’Clock et développement."><style>body{margin:0;background:#fff5e2;color:#263e42;font:16px/1.8 system-ui,sans-serif}main{max-width:780px;margin:auto;padding:40px 24px 80px}a{color:#346c6c}a:focus-visible{outline:3px solid #a4543c;outline-offset:5px}h1{font-size:clamp(36px,7vw,60px);line-height:1.1;letter-spacing:-.05em;margin:50px 0 24px}h2{line-height:1.3;font-size:28px}article{border-top:1px solid #263e4230;padding:30px 0;margin-top:25px;scroll-margin-top:25px}.label{font-size:11px;letter-spacing:.12em;text-transform:uppercase}small{color:#66756b}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin:30px 0}nav a{text-decoration:none;border-bottom:1px solid #263e4220;padding:8px 0;font-size:14px}</style></head><body><main><a href="./">← Revenir à l’archipel</a><p class="label">Zeppelin Journey · Le carnet de Fabien</p><h1>Chaque détour<br>a son histoire.</h1><p>Du geste au code, neuf escales entre savoir-faire et curiosité. Cette version se lit sans animation, sans WebGL et sans JavaScript.</p><nav aria-label="Les neuf escales">${links}</nav>${entries}<a href="./">Embarquer pour le voyage en 3D ↗</a></main></body></html>`,
);
