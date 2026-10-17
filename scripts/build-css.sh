#!/usr/bin/env bash
# Gera assets/css/site.css (versionado): fontes + ícones + Tailwind compilado + brand.css.
# Rodar sempre que mudar classe Tailwind em HTML/JS ou o brand.css.
#   TAILWIND_BIN=/caminho/tailwindcss bash scripts/build-css.sh
# Sem TAILWIND_BIN, usa "npx tailwindcss@3".
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
TMP="$(mktemp)"
printf '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' > "$TMP.in.css"
if [ -n "${TAILWIND_BIN:-}" ]; then
  "$TAILWIND_BIN" -c tailwind.config.js -i "$TMP.in.css" -o "$TMP" --minify
else
  npx -y tailwindcss@3 -c tailwind.config.js -i "$TMP.in.css" -o "$TMP" --minify
fi
{
  cat assets/css/src/fonts-icons.css
  cat "$TMP"
  printf '\n'
  cat assets/css/src/brand.css
} > assets/css/site.css
rm -f "$TMP" "$TMP.in.css"
echo "✓ assets/css/site.css ($(wc -c < assets/css/site.css) bytes)"
