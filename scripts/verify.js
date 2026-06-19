#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');

function walk(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

if (!fs.existsSync(path.join(DIST, 'index.html'))) {
  console.error('[verify] ERRO: dist/index.html ausente — execute npm run build');
  process.exit(1);
}

const htmlFiles = walk(DIST).filter(function (f) {
  return f.endsWith('.html');
});

const badRefs = [];
htmlFiles.forEach(function (file) {
  const html = fs.readFileSync(file, 'utf8');
  const matches = html.match(/(?:src|href|url\()\s*['"]?[^'")\s]*\.(?:jpe?g|png)(?!\.webp)/gi) || [];
  matches.forEach(function (m) {
    if (!/favicon|apple-touch|data:image/i.test(m)) {
      badRefs.push(path.relative(DIST, file) + ': ' + m);
    }
  });
});

const raster = walk(path.join(DIST, 'assets')).filter(function (f) {
  return /\.(jpe?g|png)$/i.test(f) && !/favicon|apple-touch/i.test(f);
});

const blogRaster = walk(path.join(DIST, 'blog', 'assets')).filter(function (f) {
  return /\.(jpe?g|png)$/i.test(f);
});

if (badRefs.length || raster.length || blogRaster.length) {
  console.error('[verify] ERRO: arquivos ou referências raster na saída de produção');
  badRefs.forEach(function (r) { console.error('  ref: ' + r); });
  raster.concat(blogRaster).forEach(function (f) {
    console.error('  file: ' + path.relative(DIST, f));
  });
  process.exit(1);
}

console.log('[verify] Site pronto para deploy em dist/ (' + htmlFiles.length + ' páginas)');
