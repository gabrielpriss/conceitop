#!/usr/bin/env node
/* Instala o Google Tag Manager em todas as páginas de dist/ quando conteudo/rastreamento.json tiver o ID.
   Roda no build (scripts/build.sh), então os HTMLs da pasta de trabalho continuam limpos. */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const { gtm } = JSON.parse(fs.readFileSync(path.join(ROOT, 'conteudo/rastreamento.json'), 'utf8'));

if (!gtm) { console.log('GTM: sem ID em conteudo/rastreamento.json, nada instalado'); process.exit(0); }
if (!/^GTM-[A-Z0-9]{4,10}$/.test(gtm)) { console.error('GTM: ID inválido: ' + gtm); process.exit(1); }

const head = `<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','${gtm}');</script>
<!-- End Google Tag Manager -->`;
const body = `<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=${gtm}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->`;

let n = 0;
(function andar(dir) {
  for (const nome of fs.readdirSync(dir)) {
    const p = path.join(dir, nome);
    if (fs.statSync(p).isDirectory()) { andar(p); continue; }
    if (!p.endsWith('.html')) continue;
    let html = fs.readFileSync(p, 'utf8');
    if (html.includes('googletagmanager.com/gtm.js')) continue;
    html = html.replace(/<head>/i, '<head>\n' + head).replace(/(<body[^>]*>)/i, '$1\n' + body);
    fs.writeFileSync(p, html);
    n++;
  }
})(DIST);
console.log(`GTM ${gtm} instalado em ${n} páginas`);
