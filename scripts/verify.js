#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

function walk(dir, skip) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const rel = path.relative(ROOT, full);
    if (entry.isDirectory()) {
      if (skip.some(function (s) { return rel.startsWith(s); })) continue;
      out.push(...walk(full, skip));
    } else {
      out.push(full);
    }
  }
  return out;
}

const skipDirs = ['node_modules', 'scripts', 'assets/marcas', 'assets/portfolio'];
const htmlFiles = walk(ROOT, skipDirs).filter(function (f) {
  return f.endsWith('.html') && !f.includes(path.sep + 'scripts' + path.sep);
}).filter(function (f) {
  const rel = path.relative(ROOT, f);
  return !/^(blog|contato|quem-somos)\.html$/.test(rel);
});

const badRefs = [];
htmlFiles.forEach(function (file) {
  const html = fs.readFileSync(file, 'utf8');
  const matches = html.match(/(?:src|href|url\()\s*['"]?[^'")\s]*\.(?:jpe?g|png)(?!\.webp)/gi) || [];
  matches.forEach(function (m) {
    if (!/favicon|apple-touch|data:image/i.test(m)) {
      badRefs.push(path.relative(ROOT, file) + ': ' + m);
    }
  });
});

if (badRefs.length) {
  console.error('[verify] ERRO: referências raster (exceto favicons):');
  badRefs.forEach(function (r) {
    console.error('  ' + r);
  });
  process.exit(1);
}

console.log('[verify] Site estático pronto para deploy (' + htmlFiles.length + ' páginas)');
