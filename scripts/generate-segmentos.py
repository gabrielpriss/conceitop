#!/usr/bin/env python3
"""Páginas de destino da campanha de Google Ads: /industrial/ e /b2b/.

Uso: python3 scripts/generate-segmentos.py

Cabeçalho vem de partials/header.html e o rodapé é copiado da página de serviço
(servicos/branding/index.html), para as páginas seguirem o resto do site.
O formulário é o mesmo das páginas internas, com faturamento obrigatório: o
evento lead_qualificado (brand.js) só dispara a partir de R$ 100 mil por mês.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_form_snippet import render_lead_form_block, render_lead_header
from PIL import Image

SITE = 'https://conceitop.com.br'
HEADER = open(os.path.join(ROOT, 'partials/header.html'), encoding='utf-8').read().strip()
ESTRUTURA = open(os.path.join(ROOT, 'partials/estrutura.html'), encoding='utf-8').read().rstrip()
_base = open(os.path.join(ROOT, 'servicos/branding/index.html'), encoding='utf-8').read()
FOOTER = _base[_base.index('  </main>'):]
CLIENTES = {c['slug']: c for faixa in ('faixa1', 'faixa2')
            for c in json.load(open(os.path.join(ROOT, 'conteudo/clientes.json'), encoding='utf-8'))[faixa]}

VIDEOS = {
    'kuzma': ('W2THQatKpyQ', 'depoimento-rafael.webp', 'Depoimento de Rafael Kuzma, Diretor da Molas Kuzma'),
    'german': ('iaNFzlWoXDo', 'depoimento-philipe.webp', 'Depoimento de Philippe Enke, CEO da German Financial'),
    'ruan': ('hCFMWFbYoZc', 'depoimento-ruan.webp', 'Depoimento de Ruan Ançay, Diretor da Nova Direção Negócios'),
    'heloise': ('UDBxL5vSQcI', 'depoimento-heloise.webp', 'Depoimento de Heloise Biscaia, Diretora do Grupo Nuele'),
}

# Serviços da página de indústria: foco no que a campanha vende (a home continua com todos)
SERVICOS_INDUSTRIA = [
    ('fab fa-google', 'Google Ads de intenção', 'Campanhas de pesquisa com termos de quem procura fornecedor, negativas de varejo e consumidor final e região definida pela praça comercial.'),
    ('fas fa-laptop-code', 'Página de captação', 'Página rápida, com o portfólio que importa e formulário que pergunta o que o comercial precisa saber antes de responder.'),
    ('fas fa-chart-line', 'Medição e CRM', 'Conversão contada só quando chega pedido de verdade, com cada contato registrado na planilha ou no CRM e a origem de cada um.'),
]

# Página B2B: mostra a agência completa, não só anúncios
SERVICOS_B2B = [
    ('fas fa-chess-knight', 'Posicionamento e marca', 'Proposta de valor clara para o decisor, identidade visual e discurso alinhados entre site, proposta e time comercial.'),
    ('fas fa-laptop-code', 'Site e páginas de captação', 'Site institucional que passa confiança para quem compra de empresa e páginas de campanha com formulário que qualifica o contato.'),
    ('fas fa-bullseye', 'Mídia paga', 'Google Ads para quem já procura fornecedor e Meta Ads para quem ainda não conhece a sua marca, com verba e região definidas pelo comercial.'),
    ('fas fa-share-nodes', 'Conteúdo e redes sociais', 'LinkedIn e Instagram com conteúdo técnico e de autoridade, para o decisor reconhecer a sua empresa quando chega a hora de comprar.'),
    ('fas fa-comments', 'Atendimento e CRM', 'WhatsApp organizado, leads registrados com origem e funil visível, para nenhum contato se perder entre o marketing e o vendedor.'),
    ('fas fa-chalkboard-user', 'Treinamento e materiais de venda', 'Capacitação do time comercial e apresentações e materiais impressos que sustentam a negociação depois do primeiro contato.'),
]

PAGINAS = [
    {
        'slug': 'industrial',
        'title': 'Marketing para Indústrias com Google Ads | Conceito Prime',
        'description': 'Marketing para indústrias: Google Ads com termos de compra B2B, página de captação e medição para receber pedidos de orçamento de empresas, não de curiosos.',
        'eyebrow': 'Marketing para indústrias',
        'h1': 'Pedidos de orçamento de quem <span class="text-gold-400">compra em volume</span>',
        'sub': 'Estruturamos Google Ads, página de captação e medição para a sua indústria receber contatos de empresas compradoras, e não de consumidor final atrás de peça avulsa.',
        'logos_titulo': 'Algumas indústrias e distribuidores que <span class="text-gold-400">trabalham com a gente</span>',
        'logos': ['plasfix', 'naciopetro', 'rolpro', 'ladaniuski', 'atlas-eletromotores', 'cactos',
                  'tech-composites', 'rgm-service', 'serquip', 'mais-madeiras', 'pontual', 'm8-pneus',
                  'luzago', 'ivankio', 'pinhapel', '2a', 'aiss', 'ice-cargo', 'ana-mariana', 'dracos',
                  'molas-kuzma', 'wyllis', 'bw-printer'],
        'servicos_titulo': 'O que <span class="text-gold-400">entregamos</span>',
        'servicos': SERVICOS_INDUSTRIA,
        'problema_titulo': 'Por que o tráfego da indústria costuma trazer <span class="text-gold-400">contato errado</span>',
        'problemas': [
            ('fas fa-user-slash', 'Busca de consumidor final', 'Termos abertos trazem quem quer uma unidade, um conserto caseiro ou o preço do varejo. O comercial perde tempo e a verba vai embora.'),
            ('fas fa-filter', 'Conversão que não é venda', 'Clique no WhatsApp, rede de display e parceiros de pesquisa contam como resultado no painel e não aparecem no pedido.'),
            ('fas fa-eye-slash', 'Comercial sem contexto', 'O vendedor recebe um "oi, quero informação" sem saber empresa, volume ou produto, e o lead esfria antes da primeira resposta.'),
        ],
        'passos': [
            ('Diagnóstico do que é lead bom', 'Entendemos portfólio, ticket, praças e o que o seu comercial considera pedido qualificado. Isso vira a regra da campanha.'),
            ('Campanha só com intenção de compra', 'Termos de fornecedor, distribuidor e especificação técnica, em frase e exata, com negativas de varejo, consumidor final e itens que vocês não vendem.'),
            ('Página que qualifica', 'Formulário no lugar do WhatsApp aberto, com empresa, volume e produto. O contato chega pronto para o orçamento.'),
            ('Medição pelo comercial', 'Conversão só de pedido enviado, leads na planilha ou no CRM e leitura mensal cruzada com o que virou venda.'),
        ],
        'videos': ['kuzma', 'german', 'ruan', 'heloise'],
        'faq': [
            ('Atendem indústrias fora de Curitiba?', 'Sim. Temos campanhas rodando para o Brasil inteiro e também fora do país. A região de cada campanha segue as praças onde vocês querem vender.'),
            ('Vocês só fazem os anúncios?', 'Não. Cuidamos da campanha, da página de captação e da medição. Sem as três juntas, o painel mostra resultado que o comercial não enxerga.'),
            ('Como sabemos se a campanha está dando resultado?', 'Cada contato chega com a origem registrada e conferimos com vocês quais viraram orçamento e venda. O relatório parte desse dado, não só do que o Google mostra.'),
            ('Qual o investimento em mídia?', 'Definimos no diagnóstico, a partir do volume de busca do seu mercado, das praças e do ticket. A proposta mostra a verba sugerida antes de qualquer contratação.'),
        ],
        'servico_hidden': 'Campanha para indústria',
        'segmento': 'industria',
        'form_titulo': 'Solicite um diagnóstico',
        'form_desc': 'Respondemos com uma leitura do seu mercado no Google e o próximo passo.',
    },
    {
        'slug': 'b2b',
        'title': 'Marketing B2B e Geração de Leads Qualificados | Conceito Prime',
        'description': 'Marketing B2B completo: marca, site, mídia paga, conteúdo, CRM e treinamento comercial para quem vende para empresas gerar e fechar mais negócios.',
        'eyebrow': 'Marketing B2B',
        'h1': 'Marketing B2B do posicionamento ao <span class="text-gold-400">contrato fechado</span>',
        'sub': 'Marca, site, mídia, conteúdo e processo comercial trabalhando juntos para a sua empresa atrair decisores com perfil de compra e transformar esses contatos em contratos.',
        'logos_titulo': 'Algumas empresas B2B que <span class="text-gold-400">trabalham com a gente</span>',
        'logos': ['reda', 'german-financial', 'rgm-service', 'naciopetro', 'cactos', 'ice-cargo',
                  'tech-composites', 'aiss', 'pontual', 'serquip', 'dracos', 'rolpro', 'ladaniuski',
                  'atlas-eletromotores', 'plasfix', 'bw-printer', 'luzago', 'm8-pneus', 'mais-madeiras',
                  'pinhapel', 'ivankio', '2a', 'giga', 'molas-kuzma'],
        'servicos_titulo': 'Uma agência para <span class="text-gold-400">toda a jornada</span>',
        'servicos': SERVICOS_B2B,
        'problema_titulo': 'Onde a geração de leads B2B <span class="text-gold-400">costuma travar</span>',
        'problemas': [
            ('fas fa-user-xmark', 'Lead sem perfil', 'Pessoa física, estudante e concorrente entram no mesmo funil que o decisor. O volume parece bom e a agenda do comercial não enche.'),
            ('fas fa-hourglass-half', 'Ciclo longo sem dado', 'A venda leva semanas e ninguém liga o contrato fechado ao anúncio que trouxe o contato. A verba é cortada justamente no que funciona.'),
            ('fas fa-comment-slash', 'Primeiro contato frio', 'Sem saber porte, segmento e necessidade, o time abre a conversa do zero e perde para quem responde com proposta.'),
        ],
        'passos': [
            ('Diagnóstico e cliente ideal', 'Porte, segmento, cargo de quem decide e ticket mínimo que vale a pena atender. Olhamos também marca, site e processo comercial de hoje.'),
            ('Presença que gera confiança', 'Posicionamento, site e conteúdo ajustados para o decisor entender rápido o que vocês fazem e por que vale a reunião.'),
            ('Geração de demanda', 'Google Ads para quem já procura, Meta Ads e conteúdo para quem ainda não conhece, e formulário que filtra por faturamento, segmento e empresa.'),
            ('Conversão e leitura', 'Leads no CRM com origem, atendimento organizado, time treinado e conferência mensal de reuniões, propostas e contratos.'),
        ],
        'videos': ['german', 'kuzma', 'ruan', 'heloise'],
        'faq': [
            ('Vocês fazem só anúncios?', 'Não. Trabalhamos marca, site, mídia paga, conteúdo, atendimento e CRM, treinamento comercial e materiais de venda. O diagnóstico mostra por onde começar no caso de vocês.'),
            ('Funciona para venda consultiva com ciclo longo?', 'Sim. Medimos o lead qualificado na entrada e acompanhamos com vocês o que vira reunião e contrato, para o trabalho não ser julgado só pelo volume.'),
            ('Precisamos contratar tudo de uma vez?', 'Não. Montamos a entrega pelo que mais trava as vendas hoje e ampliamos conforme o resultado aparece.'),
            ('Atendem empresas fora do Paraná?', 'Sim. Temos clientes e campanhas no Brasil inteiro e também fora do país.'),
            ('Qual o investimento?', 'Definimos no diagnóstico, a partir do que vocês já têm, do mercado e do ticket. A proposta mostra escopo e verba sugerida antes de qualquer contratação.'),
        ],
        'servico_hidden': 'Campanha B2B',
        'segmento': '',
        'form_titulo': 'Solicite um diagnóstico',
        'form_desc': 'Respondemos com uma leitura do seu marketing e comercial hoje e o próximo passo.',
    },
]


def logos_html(slugs):
    itens = []
    for slug in slugs:
        c = CLIENTES[slug]
        w, h = Image.open(os.path.join(ROOT, 'assets/images/clientes', slug + '.webp')).size
        classe = 'carousel-item carousel-item--escuro' if c.get('fundo') == 'escuro' else 'carousel-item'
        itens.append(f'<li class="{classe}"><img src="/assets/images/clientes/{slug}.webp" alt="{c["nome"]}" width="{w // 2}" height="{h // 2}" loading="lazy" decoding="async"></li>')
    return '\n          '.join(itens)


def cards_html(lista):
    return '\n'.join(f'''        <article class="seg-card">
          <span class="seg-card-icon" aria-hidden="true"><i class="{icone}"></i></span>
          <h3 class="font-serif text-lg text-prime-900 uppercase mb-3">{titulo}</h3>
          <p class="text-prime-600 font-light text-[15px] leading-[1.8]">{texto}</p>
        </article>''' for icone, titulo, texto in lista)


def passos_html(lista):
    return '\n'.join(f'''        <li class="seg-step">
          <span class="seg-step-num" aria-hidden="true">{i:02d}</span>
          <h3 class="font-serif text-lg text-white uppercase mb-3">{titulo}</h3>
          <p class="text-prime-300 font-light text-[15px] leading-[1.8]">{texto}</p>
        </li>''' for i, (titulo, texto) in enumerate(lista, 1))


def videos_html(chaves):
    slides, dots = [], []
    for i, k in enumerate(chaves):
        yt, img, alt = VIDEOS[k]
        titulo = alt.replace(', Diretora do ', ', ').replace(', Diretor da ', ', ').replace(', CEO da ', ', ')
        slides.append(f'''          <div class="video-carousel-slide">
            <button type="button" class="video-thumb" data-youtube-id="{yt}" data-video-title="{titulo}">
              <img src="/assets/images/depoimentos/{img}" alt="{alt}" width="997" height="534" loading="lazy" decoding="async">
              <span class="video-play" aria-hidden="true"><i class="fas fa-play"></i></span>
            </button>
          </div>''')
        nome = alt.split(', ')[0].replace('Depoimento de ', '')
        dots.append(f'<button type="button" class="video-dot{" active" if i == 0 else ""}" aria-label="Depoimento {i + 1}, {nome}"></button>')
    return '\n'.join(slides), '\n        '.join(dots)


def faq_html(lista):
    return '\n'.join(f'''        <details class="seg-faq"{" open" if i == 0 else ""}>
          <summary>{p}<i class="fas fa-chevron-down" aria-hidden="true"></i></summary>
          <p>{r}</p>
        </details>''' for i, (p, r) in enumerate(lista))


def formulario(pg):
    form_id = f'form-{pg["slug"]}'
    bloco = render_lead_form_block(hidden_servico=pg['servico_hidden'], form_id=form_id,
                                   aria_label=f'Formulário de diagnóstico {pg["eyebrow"].lower()}')
    if pg['segmento']:
        bloco = bloco.replace('<option value="" disabled selected>Qual o seu segmento?</option>',
                              '<option value="" disabled>Qual o seu segmento?</option>')
        bloco = bloco.replace(f'<option value="{pg["segmento"]}">', f'<option value="{pg["segmento"]}" selected>')
    cab = render_lead_header(title=pg['form_titulo'], subtitle=pg['form_desc'], title_id=f'{form_id}-title')
    return form_id, cab, bloco


def pagina(pg):
    url = f'{SITE}/{pg["slug"]}/'
    schema = json.dumps([
        {'@context': 'https://schema.org', '@type': 'Service', 'name': pg['eyebrow'], 'description': pg['description'],
         'provider': {'@type': 'Organization', 'name': 'Conceito Prime', 'url': SITE}, 'areaServed': 'BR', 'url': url},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': p, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for p, r in pg['faq']]},
    ], ensure_ascii=False)
    slides, dots = videos_html(pg['videos'])
    form_id, form_cab, form_bloco = formulario(pg)
    return f'''<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{pg['title']}</title>
  <link rel="canonical" href="{url}">
  <meta name="description" content="{pg['description']}">
  <meta name="robots" content="index, follow">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{pg['title']}">
  <meta property="og:description" content="{pg['description']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
  <link rel="icon" href="/assets/images/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/cairo.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">{schema}</script>
</head>
<body class="font-sans text-prime-800 antialiased" data-contato="formulario">

  {HEADER}

  <main>
  <section class="hero-bg seg-hero pt-36 pb-24 lg:pt-44 lg:pb-32" aria-labelledby="seg-titulo">
    <div class="hero-content max-w-4xl mx-auto px-6 lg:px-8 text-center">
      <p class="text-gold-400 font-semibold uppercase tracking-[0.3em] text-[11px] mb-6">{pg['eyebrow']}</p>
      <h1 id="seg-titulo" class="font-serif text-4xl sm:text-5xl lg:text-6xl text-white leading-[1.1] mb-8 uppercase">{pg['h1']}</h1>
      <p class="text-white/75 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto mb-10">{pg['sub']}</p>
      <a href="#orcamento" class="btn-wa px-10 py-5 uppercase tracking-[0.2em] text-[12px] font-bold" data-cta="hero-{pg['slug']}" style="background:var(--brand-yellow);color:var(--brand-dark);box-shadow:0 8px 32px rgba(247,204,25,.45);">
        <i class="fas fa-magnifying-glass" aria-hidden="true"></i> Solicitar diagnóstico
      </a>
    </div>
  </section>

  <section class="py-20 bg-white" aria-labelledby="seg-logos">
    <div class="max-w-6xl mx-auto px-6 lg:px-8">
      <h2 id="seg-logos" class="font-serif text-2xl sm:text-3xl text-prime-900 uppercase text-center mb-12">{pg['logos_titulo']}</h2>
      <ul class="seg-logos" role="list">
          {logos_html(pg['logos'])}
      </ul>
    </div>
  </section>

  <section class="bg-prime-900 py-16" aria-label="Números da Conceito Prime">
    <div class="max-w-5xl mx-auto px-6 lg:px-8 grid grid-cols-3 gap-6 text-center">
      <div>
        <p class="font-serif text-4xl sm:text-5xl text-white mb-2 stat-num"><span class="sr-only">9 anos</span><span aria-hidden="true" data-count="9">9</span></p>
        <p class="text-gold-400 font-medium uppercase tracking-[0.2em] text-[11px]">Anos de mercado</p>
      </div>
      <div>
        <p class="font-serif text-4xl sm:text-5xl text-white mb-2 stat-num"><span class="sr-only">Mais de 1.000</span><span aria-hidden="true" data-count="1000" data-prefix="+">+1.000</span></p>
        <p class="text-gold-400 font-medium uppercase tracking-[0.2em] text-[11px]">Clientes atendidos</p>
      </div>
      <div>
        <p class="font-serif text-4xl sm:text-5xl text-white mb-2 stat-num"><span class="sr-only">Mais de 10.000</span><span aria-hidden="true" data-count="10000" data-prefix="+">+10.000</span></p>
        <p class="text-gold-400 font-medium uppercase tracking-[0.2em] text-[11px]">Serviços realizados</p>
      </div>
    </div>
  </section>

  <section class="py-24 bg-prime-50" aria-labelledby="seg-problema">
    <div class="max-w-6xl mx-auto px-6 lg:px-8">
      <div class="w-12 h-[1px] bg-gold-400 mb-8 mx-auto" aria-hidden="true"></div>
      <h2 id="seg-problema" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight max-w-3xl mx-auto mb-14">{pg['problema_titulo']}</h2>
      <div class="grid md:grid-cols-3 gap-6">
{cards_html(pg['problemas'])}
      </div>
    </div>
  </section>

  <section class="py-24 bg-prime-950" aria-labelledby="seg-metodo">
    <div class="max-w-6xl mx-auto px-6 lg:px-8">
      <h2 id="seg-metodo" class="font-serif text-3xl sm:text-4xl text-white uppercase text-center leading-tight mb-14">Como <span class="text-gold-400">trabalhamos</span></h2>
      <ol class="seg-steps" role="list">
{passos_html(pg['passos'])}
      </ol>
    </div>
  </section>

  <section class="py-24 bg-white" aria-labelledby="seg-servicos">
    <div class="max-w-6xl mx-auto px-6 lg:px-8">
      <h2 id="seg-servicos" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight mb-14">{pg['servicos_titulo']}</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards_html(pg['servicos'])}
      </div>
    </div>
  </section>

  <section id="depoimentos" class="py-24 bg-prime-950 border-b border-prime-800" aria-labelledby="video-depoimentos-title">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 id="video-depoimentos-title" class="font-serif text-2xl sm:text-3xl text-white uppercase">Quem trabalha com a gente <span class="text-gold-400">conta</span></h2>
      </div>
      <div class="video-carousel-wrap">
        <button type="button" class="video-arrow video-arrow-prev" id="video-prev" aria-label="Depoimento anterior">
          <i class="fas fa-chevron-left" aria-hidden="true"></i>
        </button>
        <div class="video-carousel">
        <div id="video-carousel-track" class="video-carousel-track">
{slides}
        </div>
        </div>
        <button type="button" class="video-arrow video-arrow-next" id="video-next" aria-label="Próximo depoimento">
          <i class="fas fa-chevron-right" aria-hidden="true"></i>
        </button>
      </div>
      <div class="video-dots" role="tablist" aria-label="Navegar depoimentos em vídeo">
        {dots}
      </div>
    </div>
  </section>

{ESTRUTURA}

  <section class="py-24 bg-prime-50" aria-labelledby="seg-faq">
    <div class="max-w-3xl mx-auto px-6 lg:px-8">
      <h2 id="seg-faq" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight mb-12">Perguntas <span class="text-gold-400">frequentes</span></h2>
      <div class="seg-faqs">
{faq_html(pg['faq'])}
      </div>
    </div>
  </section>

  <section id="orcamento" class="lead-form-section py-24" aria-labelledby="{form_id}-title">
    <div class="max-w-md mx-auto px-6 lg:px-8">
      <div class="lead-card lead-card-inline">
        {form_cab}
        {form_bloco}
      </div>
      <p class="seg-form-nota">Nosso trabalho é pensado para empresas que já faturam a partir de R$ 100 mil por mês.</p>
    </div>
  </section>
''' + FOOTER


def main():
    for pg in PAGINAS:
        destino = os.path.join(ROOT, pg['slug'])
        os.makedirs(destino, exist_ok=True)
        with open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina(pg))
        print(f'Criada /{pg["slug"]}/')


if __name__ == '__main__':
    main()
