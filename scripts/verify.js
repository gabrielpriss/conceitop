#!/usr/bin/env node
'use strict';
// QA da saída de produção (dist/). Sai com código 1 se houver ERRO.

const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');
const erros = [];
const HEADER_PADRAO = fs.readFileSync(path.join(__dirname, '..', 'partials', 'header.html'), 'utf8').trim();
const avisos = [];

function walk(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

if (!fs.existsSync(path.join(DIST, 'index.html'))) {
  console.error('[verify] ERRO: dist/index.html ausente, execute npm run build');
  process.exit(1);
}

const arquivos = walk(DIST);
const htmls = arquivos.filter((f) => f.endsWith('.html'));
const redirects = fs.readFileSync(path.join(DIST, '_redirects'), 'utf8')
  .split('\n').map((l) => l.trim().split(/\s+/)[0]).filter((l) => l && !l.startsWith('#'));

function existe(ref, base) {
  let p = ref.split('#')[0].split('?')[0];
  if (!p) return true;
  p = decodeURIComponent(p);
  const abs = p.startsWith('/') ? path.join(DIST, p) : path.join(path.dirname(base), p);
  if (fs.existsSync(abs) && fs.statSync(abs).isFile()) return true;
  if (fs.existsSync(path.join(abs, 'index.html'))) return true;
  if (fs.existsSync(abs + '.html')) return true;
  const rel = '/' + path.relative(DIST, abs).split(path.sep).join('/');
  return redirects.some((r) => r === rel || r === rel + '/' || (r.endsWith('*') && rel.startsWith(r.slice(0, -1))));
}

for (const file of htmls) {
  const rel = path.relative(DIST, file);
  const html = fs.readFileSync(file, 'utf8');

  // referências locais quebradas
  const refs = [...html.matchAll(/\b(src|href|srcset)="([^"]+)"/g)];
  for (const [, attr, r] of refs) {
    const lista = attr === 'srcset' ? r.split(',').map((x) => x.trim().split(/\s+/)[0]) : [r];
    for (const ref of lista) {
      if (/^(https?:|mailto:|data:|#|javascript:)/.test(ref) || !ref) continue;
      if (/^tel:/.test(ref)) { erros.push(`${rel}: link tel: (padrão: só WhatsApp)`); continue; }
      if (!existe(ref, file)) erros.push(`${rel}: referência quebrada ${ref}`);
    }
  }

  // dependências externas em runtime
  if (/cdn\.tailwindcss|fonts\.googleapis|cdnjs\.cloudflare\.com\/ajax\/libs\/font-awesome/.test(html)) {
    erros.push(`${rel}: dependência de CDN em runtime`);
  }
  if (/api\.whatsapp\.com/.test(html)) erros.push(`${rel}: link api.whatsapp.com (usar wa.me)`);
  if (/<a[^>]+href="#"[^>]*class="[^"]*btn-wa/.test(html)) erros.push(`${rel}: CTA com href="#"`);

  // raster fora do padrão
  const raster = (html.match(/(?:src|href|url\()\s*['"]?[^'")\s]*\.(?:jpe?g|png)(?=['")\s])/gi) || [])
    .filter((m) => !/favicon|apple-touch|og-image|\/og\//i.test(m));
  raster.forEach((m) => erros.push(`${rel}: imagem raster ${m}`));

  // travessões no texto visível (fora de scripts, estilos e comentários)
  const visivel = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '').replace(/<!--[\s\S]*?-->/g, '');
  if (/[–—]/.test(visivel)) erros.push(`${rel}: travessão no conteúdo`);

  // SEO básico
  const title = (html.match(/<title>([^<]*)<\/title>/) || [])[1];
  const desc = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1];
  const h1 = (html.match(/<h1[\s>]/g) || []).length;
  const is404 = rel === '404.html';
  if (!title) erros.push(`${rel}: sem <title>`);
  if (!is404 && !desc) erros.push(`${rel}: sem meta description`);
  if (!is404 && !/<link rel="canonical"/.test(html)) erros.push(`${rel}: sem canonical`);
  if (h1 !== 1) avisos.push(`${rel}: ${h1} h1`);
  if (title && (title.length < 30 || title.length > 65)) avisos.push(`${rel}: title com ${title.length} caracteres`);
  if (desc && (desc.length < 110 || desc.length > 165)) avisos.push(`${rel}: description com ${desc.length} caracteres`);
  const semAlt = (html.match(/<img(?![^>]*\balt=)[^>]*>/g) || []).length;
  if (semAlt) erros.push(`${rel}: ${semAlt} <img> sem alt`);
  const semDim = (html.match(/<img(?![^>]*\bwidth=)[^>]*>/g) || []).length;
  if (semDim) avisos.push(`${rel}: ${semDim} <img> sem width/height`);

  // cabeçalho único: todas as páginas iguais ao partials/header.html (scripts/sync-header.py)
  if (!is404 && !/<body[^>]*data-lp=/.test(html)) {
    const header = (html.match(/<header id="header"[\s\S]*?<\/header>/) || [])[0];
    if (!header) erros.push(`${rel}: sem o cabeçalho padrão`);
    else if (header.replace(/\/assets\/(css|js)\/[^"]+/g, '') !== HEADER_PADRAO) erros.push(`${rel}: cabeçalho diferente de partials/header.html (rodar scripts/sync-header.py)`);
  }
}

// .md, rascunhos e originais não podem ir ao ar
arquivos.filter((f) => /\.(md|py|sh|psd|ai)$|\.(jpe?g|png)$/i.test(f) && !/favicon|apple-touch|og-image|[\\/]og[\\/]/i.test(f))
  .forEach((f) => erros.push(`arquivo que não deveria publicar: ${path.relative(DIST, f)}`));

avisos.forEach((a) => console.warn('[verify] aviso: ' + a));
if (erros.length) {
  erros.forEach((e) => console.error('[verify] ERRO: ' + e));
  console.error(`[verify] ${erros.length} erro(s)`);
  process.exit(1);
}
console.log(`[verify] Site pronto para deploy em dist/ (${htmls.length} páginas, ${avisos.length} avisos)`);
