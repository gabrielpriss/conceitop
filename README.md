# conceitop.com.br

Site institucional da Conceito Prime em HTML estático, servido por um Cloudflare Worker (assets estáticos + `worker.js`).

## Deploy

- Worker **conceitop** na conta CONCEITO PRIME, conectado a este repositório (branch `main`).
- Cada push na `main` roda `npm run build` e `npx wrangler deploy`.
- Endereço de teste: https://conceitop.conceito-prime.workers.dev/
- O domínio conceitop.com.br continua no WordPress até a virada (ver RELATORIO.md, "Virada de domínio").

## Build

```
npm run build        # monta dist/ (scripts/build.sh) e roda o QA (scripts/verify.js)
```

O build só copia o que vai ao ar e coloca hash de conteúdo em `site.css` e `brand.js` (cache imutável de um ano). O QA falha se encontrar: referência quebrada, link `tel:`, CDN em runtime, `api.whatsapp.com`, CTA com `href="#"`, imagem raster fora do padrão, travessão no texto, página sem title, description ou canonical.

## Arquivos gerados (rodar quando mudar a fonte)

| O que mudou | Comando | Saída versionada |
|---|---|---|
| Classe Tailwind em HTML/JS ou `assets/css/src/brand.css` | `TAILWIND_BIN=/caminho/tailwindcss bash scripts/build-css.sh` | `assets/css/site.css` |
| Fonte ou ícone novo (`fa-*`) | `python3 scripts/build-assets.py --fonts <google/fonts> --fa <fontawesome-web>` | `assets/fonts/*.woff2`, `assets/css/src/fonts-icons.css` |
| Artigo do blog | editar `conteudo/blog/posts.json` e `<slug>.raw.html`, depois `python3 scripts/generate-blog-covers.py --fonts <google/fonts>` e `python3 scripts/generate-blog.py` | `blog/<slug>/`, `blog/index.html`, capas, `sitemap.xml` |
| Logo de cliente | tratar com `_logos/tratar.py` (Mac), salvar em `assets/images/clientes/<slug>.webp`, editar `conteudo/clientes.json`, `python3 scripts/generate-clientes.py` | carrossel da home |
| Página de serviço | `python3 scripts/generate-services.py` | `servicos/<slug>/` |

Depois de qualquer um deles, rodar `build-css.sh` de novo se surgiram classes novas.

## Contato e leads

- Número principal do WhatsApp: constante `WA_NUMERO` em `assets/js/brand.js` (Comercial, 41 99990-4764). Administrativo em `WA_ADMINISTRATIVO`.
- Formulário de orçamento: valida, abre o WhatsApp com as respostas e envia uma cópia para `/api/lead`.
- `/api/lead`: grava na planilha se o segredo **LEAD_WEBHOOK** existir (instruções do Apps Script no topo de `worker.js`). Sem ele, responde 204 e o lead segue só pelo WhatsApp.
- `/api/trabalhe-conosco`: currículos e fornecedores com anexo. Precisa do segredo **TRABALHE_WEBHOOK** (Apps Script que salva o anexo no Drive e registra na planilha, código em `worker.js`). Sem ele, a página orienta a enviar por e-mail para contato@conceitop.com.br.

## Eventos no dataLayer

`cta_click {posicao, texto}`, `form_start {formulario}`, `form_submit {formulario, faturamento, segmento | tipo}`, `whatsapp_open {posicao}`, `scroll_75`, `time_on_page_60s`. O GTM ainda não está instalado (pendente o ID do contêiner).

## Redirecionamentos

`_redirects` leva as URLs do WordPress antigo para as novas: artigos da raiz para `/blog/<slug>/`, categorias e tags para `/blog/`, `/criacao-de-sites/` para `/servicos/plataformas-web/` e páginas vazias para a home.
