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

/* Desempenho: o evento gtm.js entra no dataLayer na hora (a ordem dos eventos fica igual),
   mas o download do gtm.js (cerca de 340 KiB com as tags do Google) espera a primeira interação
   (toque, clique, tecla, rolagem) ou 2,5 s depois do load, o que vier primeiro. Eventos empurrados
   antes disso ficam na fila e o GTM processa todos quando carrega.
   Nas páginas de obrigado o carregamento é imediato, para nunca perder a conversão. */
const head = `<!-- Google Tag Manager (carregamento adiado) -->
<script>(function(w,d,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var ok=0;function go(){if(ok)return;ok=1;var j=d.createElement('script');j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;d.head.appendChild(j);}if(/^\\/obrigado/.test(location.pathname)){go();return;}['pointerdown','touchstart','keydown','scroll','mousemove'].forEach(function(e){w.addEventListener(e,go,{once:true,passive:true});});if(d.readyState==='complete'){setTimeout(go,2500);}else{w.addEventListener('load',function(){setTimeout(go,2500);});}})(window,document,'dataLayer','${gtm}');</script>
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
