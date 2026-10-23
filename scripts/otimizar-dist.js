#!/usr/bin/env node
/* Ajustes de desempenho aplicados em dist/ no build (os HTMLs da pasta de trabalho não mudam).
   1. Logo do cabeçalho: o arquivo original tem 1250x356, mas aparece com no máximo 40 px de altura.
      Ganha srcset com versões de 300 e 450 px (mesma proporção, sem perda visível).
   2. Fundo do hero (.hero-bg): é imagem de fundo em CSS, que o navegador só descobre depois de baixar
      o CSS. Cada página com hero ganha preload da versão certa para a largura da tela, com os mesmos
      cortes de brand.css (800 px até 767, 1200 px até 1279, 1600 px acima), e prioridade alta.
   Rodar depois de inject-gtm.js. */
const fs = require('fs');
const path = require('path');
const DIST = path.join(__dirname, '..', 'dist');

const LOGO_SRCSET = 'srcset="/assets/images/logo-300.webp 300w, /assets/images/logo-450.webp 450w, /assets/images/logo.webp 1250w" sizes="141px"';
const PRELOAD_HERO = [
  '<link rel="preload" as="image" href="/assets/images/hero-bg-800.webp" type="image/webp" media="(max-width: 767px)" fetchpriority="high">',
  '<link rel="preload" as="image" href="/assets/images/hero-bg-1200.webp" type="image/webp" media="(min-width: 768px) and (max-width: 1279px)" fetchpriority="high">',
  '<link rel="preload" as="image" href="/assets/images/hero-bg.webp" type="image/webp" media="(min-width: 1280px)" fetchpriority="high">',
].join('\n  ');

let paginas = 0, logos = 0, heros = 0;
(function andar(dir) {
  for (const nome of fs.readdirSync(dir)) {
    const p = path.join(dir, nome);
    if (fs.statSync(p).isDirectory()) { andar(p); continue; }
    if (!p.endsWith('.html')) continue;
    let html = fs.readFileSync(p, 'utf8');
    const antes = html;

    // 1. logo do cabeçalho (o do rodapé já é pequeno e carrega com lazy)
    html = html.replace(/<img src="\/assets\/images\/logo\.webp"(?![^>]*srcset)/g, () => { logos++; return `<img src="/assets/images/logo-300.webp" ${LOGO_SRCSET}`; });

    // 2. hero: tira o preload antigo da imagem grande e põe os três cortes
    const temHero = /<(section|header)[^>]*class="[^"]*\bhero-bg\b/.test(html);
    if (temHero && !html.includes('hero-bg-800.webp')) {
      html = html.replace(/\s*<link rel="preload" as="image" href="\/assets\/images\/hero-bg\.webp"[^>]*>/g, '');
      html = html.replace(/(<link rel="stylesheet" href="\/assets\/css\/site[^"]*\.css">)/, `${PRELOAD_HERO}\n  $1`);
      if (html.includes('hero-bg-800.webp')) heros++;
    }

    if (html !== antes) { fs.writeFileSync(p, html); paginas++; }
  }
})(DIST);
console.log(`Otimização: ${paginas} páginas ajustadas (logo responsivo em ${logos}, preload do hero em ${heros})`);
