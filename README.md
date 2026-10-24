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
| Artigo do blog | seguir `conteudo/blog/REGRAS.md`: metadados em `conteudo/blog/posts.json`, corpo em `conteudo/blog/<slug>.html` (os 16 antigos usam `<slug>.raw.html`), depois `python3 scripts/generate-blog-covers.py` e `python3 scripts/generate-blog.py`; registrar a pauta em `conteudo/blog/pauta.md` | `blog/<slug>/`, `blog/index.html`, capas, `sitemap.xml` |
| Logo de cliente | editar `conteudo/clientes.json` (origem e fundo claro ou escuro), `python3 scripts/tratar-logos.py <pasta dos originais>` e `python3 scripts/generate-clientes.py` | `assets/images/clientes/*.webp`, carrossel da home |
| Capas dos depoimentos em vídeo | `python3 scripts/gerar-depoimentos.py <pasta com ShareTech-Regular.ttf e Cairo[slnt,wght].ttf>` (fotos e logos saem de `conteudo/depoimentos-originais/`) | `assets/images/depoimentos/depoimento-<slug>-v2.webp` |
| Grade "Nossos Serviços" da home | editar `scripts/generate-servicos-home.py` e `conteudo/servicos.json` (texto e imagem do popup de cada serviço; ícones em `partials/icones-servicos.py`) e rodar o script | `index.html` |
| Páginas da campanha (indústria e B2B) | editar `scripts/generate-segmentos.py` e rodar o script | `industrial/`, `b2b/` |
| Cabeçalho (menu, logo, botão) | editar `partials/header.html` e rodar `python3 scripts/sync-header.py` | cabeçalho de todas as páginas (o QA falha se alguma ficar diferente) |

Depois de qualquer um deles, rodar `build-css.sh` de novo se surgiram classes novas.

## Contato e leads

- Número principal do WhatsApp: constante `WA_NUMERO` em `assets/js/brand.js` (Comercial, 41 99990-4764). Administrativo em `WA_ADMINISTRATIVO`.
- Formulário "Solicite um diagnóstico": o mesmo em todas as páginas (`initDiagnostico` em `assets/js/brand.js`; na página basta `<form data-diagnostico>`). Quatro etapas, das mais fáceis para as mais chatas: segmento e faturamento com um clique, depois nome e empresa, por último o WhatsApp. No site, abre o WhatsApp com a mensagem pronta e envia uma cópia para `/api/lead`.
- `/api/lead`: grava na planilha se o segredo **LEAD_WEBHOOK** existir (instruções do Apps Script no topo de `worker.js`). Sem ele, responde 204 e o lead segue só pelo WhatsApp.
- `/api/trabalhe-conosco`: currículos e fornecedores com anexo. Precisa do segredo **TRABALHE_WEBHOOK** (Apps Script que salva o anexo no Drive e registra na planilha, código em `worker.js`). Sem ele, a página orienta a enviar por e-mail para contato@conceitop.com.br.

## Eventos no dataLayer

`cta_click {posicao, texto}`, `form_start {formulario}`, `form_submit {formulario, pagina, faturamento, segmento, lead_qualificado | tipo}`, `lead_qualificado` (só faturamento a partir de R$ 100 mil/mês: é a conversão principal do Google Ads da campanha), `whatsapp_open {posicao}`, `scroll_75`, `time_on_page_60s`. O GTM ainda não está instalado (pendente o ID do contêiner).

## Redirecionamentos

`_redirects` leva as URLs do WordPress antigo para as novas: artigos da raiz para `/blog/<slug>/`, categorias e tags para `/blog/`, `/criacao-de-sites/` e as antigas páginas `/servicos/*` para a grade de serviços da home (`/#servicos`) e páginas vazias para a home.

## Campanha de Google Ads da agência

- Destinos: `/b2b/` e `/industrial/`. Páginas de obrigado: `/obrigado-qualificado/` (faturamento a partir de R$ 100 mil) e `/obrigado/` (demais). Todas geradas por `scripts/generate-segmentos.py`, com cabeçalho, rodapé, CSS e JS próprios (`scripts/campanha/`), sem tocar nos componentes globais.
- O mesmo formulário do site, em modo campanha (body `data-contato="formulario"`), envia para `/api/lead-b2b` (worker.js) e redireciona para a página de obrigado. O botão flutuante do WhatsApp abre esse formulário em popup com a cara do WhatsApp (canal `popup-whatsapp` no lead). A rota `/api/lead-b2b` repassa ao segredo **LEAD_B2B_WEBHOOK** (ou LEAD_WEBHOOK). Sem segredo configurado a rota responde 503 e a página mostra erro: a campanha não pode ir ao ar antes disso.
- dataLayer: `lead_b2b {lead_qualificado, faturamento, segmento, pagina}` no envio; `conversao_lead_b2b {tipo: qualificado | todos}` nas páginas de obrigado (uma vez por envio).
- GTM: preencher o ID em `conteudo/rastreamento.json`; o build instala em todas as páginas (`scripts/inject-gtm.js`).
