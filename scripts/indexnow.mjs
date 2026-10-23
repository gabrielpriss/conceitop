#!/usr/bin/env node
// Avisa o Bing (e os outros buscadores do protocolo IndexNow) sobre páginas novas ou alteradas.
// Uso: node scripts/indexnow.mjs /blog/<slug>/ /blog/ [mais caminhos]
// Sem argumentos: lê a lista de caminhos da variável INDEXNOW_PATHS (separados por espaço).
// A chave é o arquivo <hex>.txt na raiz do repositório, publicado em https://conceitop.com.br/<hex>.txt
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const HOST = 'conceitop.com.br';
const arquivo = readdirSync(ROOT).find((f) => /^[0-9a-f]{32}\.txt$/.test(f));
if (!arquivo) { console.error('IndexNow: arquivo de chave não encontrado na raiz'); process.exit(1); }
const key = readFileSync(join(ROOT, arquivo), 'utf8').trim();

let caminhos = process.argv.slice(2);
if (!caminhos.length && process.env.INDEXNOW_PATHS) caminhos = process.env.INDEXNOW_PATHS.split(/\s+/).filter(Boolean);
if (!caminhos.length) { console.log('IndexNow: nada para enviar'); process.exit(0); }
const urlList = [...new Set(caminhos.map((c) => `https://${HOST}${c.startsWith('/') ? c : '/' + c}`))];

const r = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key, keyLocation: `https://${HOST}/${key}.txt`, urlList }),
});
console.log(`IndexNow: Enviadas ${urlList.length} URLs (HTTP ${r.status})`);
urlList.forEach((u) => console.log('  ' + u));
if (![200, 202].includes(r.status)) process.exit(1);
