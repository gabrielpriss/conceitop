#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"

echo "→ Build produção Conceito Prime para Cloudflare Pages"

rm -rf "$DIST"
mkdir -p "$DIST"

cp "$ROOT/index.html" "$ROOT/404.html" "$ROOT/robots.txt" "$ROOT/sitemap.xml" "$DIST/"
cp "$ROOT/_headers" "$ROOT/_redirects" "$DIST/"

for dir in blog contato quem-somos; do
  mkdir -p "$DIST/$dir"
  cp "$ROOT/$dir/index.html" "$DIST/$dir/"
done

mkdir -p "$DIST/servicos"
for svc in "$ROOT/servicos"/*/; do
  name=$(basename "$svc")
  mkdir -p "$DIST/servicos/$name/assets"
  cp "$svc/index.html" "$DIST/servicos/$name/"
  if compgen -G "$svc/assets/*.webp" > /dev/null; then
    cp "$svc/assets/"*.webp "$DIST/servicos/$name/assets/"
  fi
done

mkdir -p "$DIST/assets/css" "$DIST/assets/js"
cp "$ROOT/assets/css/"* "$DIST/assets/css/"
cp "$ROOT/assets/js/"* "$DIST/assets/js/"

if command -v rsync >/dev/null 2>&1; then
  rsync -a "$ROOT/assets/images/" "$DIST/assets/images/"
else
  mkdir -p "$DIST/assets/images"
  cp -r "$ROOT/assets/images/." "$DIST/assets/images/"
fi

if [ -d "$ROOT/assets/fonts" ]; then
  mkdir -p "$DIST/assets/fonts"
  cp -r "$ROOT/assets/fonts/." "$DIST/assets/fonts/"
fi

mkdir -p "$DIST/blog/assets"
cp "$ROOT/blog/assets/"*.webp "$DIST/blog/assets/"

BYTES=$(du -sh "$DIST" | cut -f1)
FILES=$(find "$DIST" -type f | wc -l)
echo "✓ Build concluído: $DIST ($BYTES, $FILES arquivos)"
