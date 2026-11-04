#!/usr/bin/env bash
# Copia a base compartilhada (fontes, CSS, JS, imagens, favicons) para cada LP.
# Cada pasta (salasecreta/, live/) é a raiz de um projeto do Cloudflare Pages, sem comando de build.
set -euo pipefail
cd "$(dirname "$0")"
for lp in salasecreta live; do
  mkdir -p "$lp/assets"
  cp -r shared/assets/. "$lp/assets/"
  cp shared/favicon.ico shared/favicon-32.png shared/apple-touch-icon.png shared/_headers shared/robots.txt "$lp/"
done
for lp in salasecreta live; do [ -d "$lp-extra" ] && cp -r "$lp-extra/." "$lp/"; done
echo "ok"
