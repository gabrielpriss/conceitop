# Relatório: migração do conceitop.com.br (out/2026)

## Ponto de partida

- **Site no ar (conceitop.com.br):** WordPress com Elementor 4.3.5, jQuery, MetForm com reCAPTCHA, plugin de WhatsApp e GTranslate. Sem GTM, sem meta description, sem Open Graph, sem dados estruturados; o único H1 da home era "Nossos Serviços". Contadores da home exibindo 0.
- **Projeto no GitHub (gabrielpriss/conceitop, jun/2026):** redesign estático já avançado, mas com bloqueios para publicar:
  - formulário de orçamento não enviava o lead para lugar nenhum (só mostrava "Obrigado");
  - todos os CTAs e até o link "Contato" do menu abriam esse formulário;
  - Tailwind, Google Fonts e Font Awesome carregados por CDN em runtime;
  - botões com `href="#"`;
  - os 16 artigos do blog não existiam (as URLs indexadas virariam 404).

## O que foi feito

- Tailwind compilado; fontes e ícones autohospedados com subconjunto (zero requisição externa no carregamento).
- Formulário de orçamento valida, abre o WhatsApp com as respostas e envia cópia para `/api/lead`.
- Painel de WhatsApp igual ao do site antigo (Comercial e Administrativo), sem RH, com aviso para currículos e fornecedores.
- Página **Trabalhe Conosco** com anexo e endpoint próprio.
- 16 artigos migrados para `/blog/<slug>/` com 301 das URLs antigas, capas na identidade, JSON-LD BlogPosting, OG e sitemap com imagens.
- Números animados (+1.000 clientes atendidos, +10.000 serviços realizados, objetivo: 1, vender mais) com valores informados pelo Gabriel em 17/10/2026.
- Rodapé "Desenvolvido por Conceito Prime".
- Headers de segurança (HSTS, CSP compatível com GTM e Google Ads, Permissions-Policy) e cache com hash.
- Favicon igual ao do site atual (símbolo amarelo no quadrado escuro), com `/favicon.ico` na raiz.
- Depoimentos em vídeo: dois por vez no desktop.
- Remoção dos links `tel:`. O evento `click_to_call` deixa de existir.

## Pendências (dependem de informação ou ação)

1. **Logos do carrossel:** 40 logos com as cores reais. Faltam **Espaço Pirâmide** (site fora do ar), **Emunah** (só ícone de 64px) e **Easy Lipo** (sem site; só Instagram). Conferir: o logo da **2A** veio de 2a.com.br (2A Soluções Elétricas) e o da **Pontual** de pontualpetroleo.com.br; confirmar se são as mesmas empresas da carteira.
2. **GTM:** sem contêiner no site atual. Precisamos do ID GTM-XXXX da Conceito Prime.
3. **Endereço:** divergência entre fontes. Rodapé: R. Antônio Rodrigues, 76, Campina do Siqueira. Link do Maps: Seminário. Mapa incorporado: Av. Visconde de Guarapuava, Centro. Falta confirmar qual vale.
4. **Planilha de leads e de currículos:** criar os Apps Scripts (código em `worker.js`) e cadastrar os segredos `LEAD_WEBHOOK` e `TRABALHE_WEBHOOK` no Worker.
5. **Fontes Tachyon e Cosild** do manual de marca: arquivos não estão no projeto; títulos usam Share Tech e Michroma.
6. **Textos das páginas de serviço** (listas "o que inclui") foram escritos em jun/2026 e não vieram do cliente. Vale revisar se refletem a entrega real.
7. **Botão flutuante do WhatsApp:** ícone branco sobre o verde oficial tem contraste 1,98 (o mínimo para elemento gráfico é 3:1). Mantido assim a pedido, igual ao site anterior; a borda verde escura ajuda a destacar o botão do fundo.
8. **Repositório público:** o padrão da agência é repositório privado. A troca é feita em Settings do GitHub.

## Achados fora do escopo, para conferir

- **centroemunah.com.br** exibe publicamente o instalador de backup do Joomla (Akeeba Backup Installer). Qualquer pessoa pode rodar a restauração e sobrescrever o site. Convém remover a pasta `installation` do servidor.
- **espacopiramideeventos.com.br** não abriu (nem com nem sem https) em 17/10/2026, e o site recebe tráfego das campanhas de Google Ads do cliente.

## Virada de domínio (quando aprovado)

1. No Worker conceitop, adicionar o domínio personalizado conceitop.com.br e www.
2. Conferir que a zona DNS do domínio está na conta CONCEITO PRIME (hoje o WordPress responde pelo domínio).
3. Depois da virada, enviar o sitemap no Search Console e acompanhar os 301 dos artigos.
