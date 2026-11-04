# LPs Black Novembro | Conceito Prime

Duas landing pages estáticas, sem build, publicadas no Cloudflare Pages (conta CONCEITO PRIME):

| Pasta | Endereço | Projeto Pages |
|---|---|---|
| `salasecreta/` | https://salasecreta.conceitop.com.br | prime-salasecreta |
| `live/` | https://live.conceitop.com.br | prime-live |

Branch de produção dos dois projetos: `lps-black-novembro`. Comando de build: nenhum. Diretório raiz: a pasta da LP.

## Variáveis pendentes

Ficam visíveis na página entre colchetes e em caixa alta (classe `var`). Para trocar, editar o texto no `index.html` da LP.

- Link do grupo e data do evento: objeto `window.LP` no `<head>` de cada página. `grupo` recebe o link de convite; `evento` recebe a data e o horário em ISO (ex.: `2026-11-13T19:00:00-03:00`) e liga a contagem regressiva. Enquanto `grupo` não for um link, os botões abrem o WhatsApp do comercial com mensagem pronta.

## Base compartilhada

`shared/` tem fontes, CSS, JS, imagens e favicons comuns; `salasecreta-extra/` e `live-extra/` têm o que é só de cada uma. Depois de mexer nelas, rodar `./build.sh` para copiar para as pastas publicadas.

## Eventos no dataLayer

`grupo_click {pagina, posicao, destino}`, `calculadora_uso` (salasecreta), `autodiagnostico_uso` (live), `scroll_75`. Se houver pixel da Meta na página, o clique também dispara `Lead`.
