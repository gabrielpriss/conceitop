#!/usr/bin/env bash
# Build de produção: monta dist/ só com o que vai ao ar e põe hash de conteúdo em CSS e JS.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"

echo "→ Build Conceito Prime (Cloudflare)"

rm -rf "$DIST"
mkdir -p "$DIST"

cp "$ROOT/index.html" "$ROOT/404.html" "$ROOT/robots.txt" "$ROOT/sitemap.xml" "$DIST/"
cp "$ROOT/_headers" "$ROOT/_redirects" "$DIST/"

# Páginas: copia só HTML e WebP de cada pasta publicada (rascunhos e originais ficam de fora)
for dir in quem-somos contato trabalhe-conosco blog servicos; do
  (cd "$ROOT" && find "$dir" -type f \( -name '*.html' -o -name '*.webp' -o -name '*.avif' \) -print0) |
    while IFS= read -r -d '' f; do
      mkdir -p "$DIST/$(dirname "$f")"
      cp "$ROOT/$f" "$DIST/$f"
    done
done

mkdir -p "$DIST/assets/css" "$DIST/assets/js" "$DIST/assets/fonts" "$DIST/assets/images"
cp -r "$ROOT/assets/images/." "$DIST/assets/images/"
cp "$ROOT/assets/fonts/"*.woff2 "$DIST/assets/fonts/"

# Hash de conteúdo: permite cache imutável de um ano sem servir versão antiga
hash() { md5sum "$1" | cut -c1-10; }
CSS_H=$(hash "$ROOT/assets/css/site.css")
JS_H=$(hash "$ROOT/assets/js/brand.js")
cp "$ROOT/assets/css/site.css" "$DIST/assets/css/site.$CSS_H.css"
cp "$ROOT/assets/js/brand.js" "$DIST/assets/js/brand.$JS_H.js"

find "$DIST" -name '*.html' -print0 | xargs -0 sed -i \
  -e "s#/assets/css/site\.css#/assets/css/site.$CSS_H.css#g" \
  -e "s#/assets/js/brand\.js#/assets/js/brand.$JS_H.js#g"

BYTES=$(du -sh "$DIST" | cut -f1)
FILES=$(find "$DIST" -type f | wc -l)
echo "✓ Build concluído: $DIST ($BYTES, $FILES arquivos)"
