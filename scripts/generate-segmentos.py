#!/usr/bin/env python3
"""Páginas da campanha de Google Ads B2B: /industrial/, /b2b/, /obrigado-qualificado/ e /obrigado/.

Uso: python3 scripts/generate-segmentos.py

Tudo o que é específico da campanha fica dentro destas páginas: cabeçalho e rodapé próprios (sem menu,
sem WhatsApp), CSS e JavaScript embutidos (scripts/campanha/), formulário próprio que envia para
/api/lead-b2b e redireciona para a página de obrigado certa. O CSS global, o brand.js, o cabeçalho e o
rodapé compartilhados não são alterados por este script.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image

SITE = 'https://conceitop.com.br'
HEADER = open(os.path.join(ROOT, 'partials/header.html'), encoding='utf-8').read().strip()
ESTRUTURA = open(os.path.join(ROOT, 'partials/estrutura.html'), encoding='utf-8').read().rstrip()
CSS_LOCAL = open(os.path.join(ROOT, 'scripts/campanha/campanha.css'), encoding='utf-8').read().strip()
JS_OBRIGADO = open(os.path.join(ROOT, 'scripts/campanha/obrigado.js'), encoding='utf-8').read().strip()

# Tag do Google da conta Cprime 2026 (404-812-7952), só nestas 4 páginas.
# Preencher com o ID da tag (AW-...) e com o "send_to" (AW-.../rótulo) de cada conversão. Vazio = sem tag.
GOOGLE_TAG_ID = ''
CONVERSAO_QUALIFICADO = ''   # "Lead Qualificado B2B" (primária)
CONVERSAO_TODOS = ''         # "Lead B2B Todos" (secundária)

WA_COMERCIAL = '5541999904764'
ENDERECO = 'R. Antônio Rodrigues, 76, Curitiba/PR'
CLIENTES = {c['slug']: c for faixa in ('faixa1', 'faixa2')
            for c in json.load(open(os.path.join(ROOT, 'conteudo/clientes.json'), encoding='utf-8'))[faixa]}

VIDEOS = {
    'kuzma': ('W2THQatKpyQ', 'depoimento-rafael-v2.webp', 'Depoimento de Rafael Kuzma, Diretor da Molas Kuzma'),
    'german': ('iaNFzlWoXDo', 'depoimento-philipe-v2.webp', 'Depoimento de Philippe Enke, CEO da German Financial'),
    'ruan': ('hCFMWFbYoZc', 'depoimento-ruan-v2.webp', 'Depoimento de Ruan Ançay, Diretor da Nova Direção Negócios'),
    'heloise': ('UDBxL5vSQcI', 'depoimento-heloise-v2.webp', 'Depoimento de Heloise Biscaia, Diretora do Grupo Nuele'),
}

# Serviços da página de indústria: foco no que a campanha vende (a home continua com todos)
SERVICOS_INDUSTRIA = [
    ('fab fa-google', 'Google Ads e Meta Ads', 'Google Ads para quem já procura fornecedor, com termos de compra B2B e negativas de varejo, e Meta Ads para alcançar compradores que ainda não conhecem a sua indústria.'),
    ('fas fa-laptop-code', 'Site e página de captação', 'Sites e páginas de alta conversão, rápidos e integrados ao Google Ads, com mensagem pensada para o comprador industrial e formulário que qualifica o contato.'),
    ('fas fa-chart-line', 'Medição e CRM', 'Conversão contada só quando chega pedido de verdade, com cada contato registrado na planilha ou no CRM e a origem de cada um.'),
]

# Página B2B: mostra a agência completa, não só anúncios
SERVICOS_B2B = [
    ('fas fa-chess-knight', 'Posicionamento e marca', 'Proposta de valor clara para o decisor, identidade visual e discurso alinhados entre site, proposta e time comercial.'),
    ('fas fa-laptop-code', 'Site e páginas de captação', 'Sites e páginas de alta conversão, integrados ao Google Ads, com mensagem pensada para o decisor e formulário que qualifica o contato.'),
    ('fas fa-bullseye', 'Google Ads e Meta Ads', 'Google Ads para quem já procura fornecedor e Meta Ads para quem ainda não conhece a sua marca, com verba e região definidas pelo comercial.'),
    ('fas fa-share-nodes', 'Conteúdo e redes sociais', 'LinkedIn e Instagram com conteúdo técnico e de autoridade, para o decisor reconhecer a sua empresa quando chega a hora de comprar.'),
    ('fas fa-comments', 'Atendimento e CRM', 'WhatsApp organizado, leads registrados com origem e funil visível, para nenhum contato se perder entre o marketing e o vendedor.'),
    ('fas fa-chalkboard-user', 'Treinamento e materiais de venda', 'Capacitação do time comercial e apresentações e materiais impressos que sustentam a negociação depois do primeiro contato.'),
]

# O que os anúncios prometem: cada item precisa aparecer na página de destino
PROMESSAS = [
    ('fas fa-check', '<strong>Para empresas com faturamento acima de R$ 100 mil/mês</strong>'),
    ('fas fa-location-dot', 'Escritórios em <strong>Curitiba e Cascavel</strong>'),
    ('fab fa-google', 'Gestão de <strong>Google Ads e Meta Ads</strong>'),
    ('fas fa-laptop-code', 'Sites e páginas de <strong>alta conversão</strong>, integrados ao Google Ads'),
    ('fas fa-filter', 'Foco em <strong>lead qualificado</strong>, não em volume'),
]

NAO_FAZ_SENTIDO = [
    'A empresa ainda não fatura ou está validando o produto.',
    'A expectativa é resultado garantido na primeira semana.',
    'O objetivo é só seguidor e curtida, sem ligação com vendas.',
    'Não há ninguém para responder os contatos que chegarem.',
]

PAGINAS = [
    {
        'slug': 'industrial',
        'title': 'Marketing Industrial e Google Ads | Conceito Prime',
        'description': 'Marketing industrial e geração de leads B2B: Google Ads, página de captação e medição para receber orçamentos de empresas, não de curiosos.',
        'eyebrow': 'Marketing industrial para indústrias e distribuidores',
        'logos_eyebrow': 'Já atendemos indústrias no Paraná',
        'faz_sentido': [
            'Vocês são indústria ou distribuidor e vendem para outras empresas.',
            'A empresa fatura acima de R$ 100 mil por mês.',
            'Existe um comercial para atender e orçar os pedidos que chegarem.',
            'O objetivo é pedido qualificado, mesmo com volume menor, num trabalho de 3 a 6 meses.',
        ],
        'h1': 'Estratégia e execução para sua indústria <span class="text-gold-400">vender mais</span>',
        'sub': 'Somos uma agência de marketing B2B que estrutura Google Ads, Meta Ads, site e medição para a sua indústria gerar leads de empresas compradoras, e não de consumidor final atrás de peça avulsa. Escritórios em Curitiba e Cascavel.',
        'logos_titulo': 'Algumas indústrias e distribuidores que <span class="text-gold-400">trabalham com a gente</span>',
        'logos': ['plasfix', 'naciopetro', 'rolpro', 'ladaniuski', 'atlas-eletromotores', 'do-valle', 'cactos',
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
            ('Para que tipo de empresa é esse trabalho?', 'Para indústrias e distribuidores com faturamento acima de R$ 100 mil por mês que vendem para outras empresas. Já atendemos indústrias no Paraná em segmentos como fitas adesivas, rolamentos, correias industriais, motores elétricos e usinagem.'),
            ('Em quanto tempo aparece resultado?', 'É um trabalho de médio prazo. As primeiras semanas servem para calibrar termos, negativas e página com o que o comercial de vocês considera pedido bom, e o resultado fica consistente entre 3 e 6 meses.'),
            ('Atendem indústrias fora de Curitiba?', 'Sim. Temos escritórios em Curitiba e em Cascavel, com reuniões presenciais ou online, e atendemos clientes em outros estados.'),
            ('Vocês só fazem os anúncios?', 'Não. Cuidamos de Google Ads e Meta Ads, do site e das páginas de alta conversão integrados ao Google Ads, e da medição. Sem essas peças juntas, o painel mostra resultado que o comercial não enxerga.'),
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
        'title': 'Agência de Marketing B2B e Tráfego Pago | Conceito Prime',
        'description': 'Agência de marketing digital B2B: tráfego pago no Google Ads e Meta Ads, site, CRM e treinamento comercial para gerar leads qualificados.',
        'eyebrow': 'Agência de marketing digital B2B',
        'logos_eyebrow': '',
        'faz_sentido': [
            'A empresa vende para outras empresas e fatura acima de R$ 100 mil por mês.',
            'Existe um comercial (ou alguém dedicado) para atender os contatos.',
            'O objetivo é lead qualificado e venda, mesmo com volume menor.',
            'Vocês topam um trabalho de médio prazo, de 3 a 6 meses, para o resultado ficar consistente.',
        ],
        'h1': 'Estratégia e execução para sua empresa <span class="text-gold-400">vender mais</span>',
        'sub': 'Somos uma agência de marketing digital focada em empresas B2B: tráfego pago no Google Ads e no Meta Ads, site, marca e processo comercial trabalhando juntos para atrair decisores com perfil de compra e transformar esses contatos em contratos. Escritórios em Curitiba e Cascavel.',
        'logos_titulo': 'Algumas empresas B2B que <span class="text-gold-400">trabalham com a gente</span>',
        'logos': ['adriano-cobuccio', 'auxiliadora-predial', 'reda', 'do-valle', 'brasilcard', 'german-financial', 'sinc-capital', 'rgm-service', 'naciopetro', 'cactos', 'ice-cargo',
                  'tech-composites', 'aiss', 'pontual', 'serquip', 'dracos', 'rolpro', 'ladaniuski',
                  'atlas-eletromotores', 'plasfix', 'bw-printer', 'luzago', 'm8-pneus', 'mais-madeiras',
                  'pinhapel', 'ivankio', '2a', 'giga', 'molas-kuzma', 'reviver-saude', 'geoazimute'],
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
            ('Vocês são uma agência de tráfego pago?', 'Sim, e não só isso. Fazemos a gestão de tráfego pago no Google Ads e no Meta Ads com foco em lead qualificado, e cuidamos do que faz esse tráfego virar venda: página de destino, medição pelo comercial e CRM.'),
            ('Vocês fazem só anúncios?', 'Não. Além da gestão de Google Ads e Meta Ads, trabalhamos sites e páginas de alta conversão integrados ao Google Ads, marca, conteúdo, atendimento e CRM, treinamento comercial e materiais de venda. O diagnóstico mostra por onde começar no caso de vocês.'),
            ('Para que tipo de empresa é esse trabalho?', 'Para empresas que vendem para outras empresas e faturam acima de R$ 100 mil por mês. O foco é lead qualificado, não volume: preferimos menos contatos com perfil de compra do que muitos contatos que o comercial descarta.'),
            ('Em quanto tempo aparece resultado?', 'É um trabalho de médio prazo. As primeiras semanas servem para calibrar campanhas, página e filtro de leads, e o resultado fica consistente entre 3 e 6 meses.'),
            ('Funciona para venda consultiva com ciclo longo?', 'Sim. Medimos o lead qualificado na entrada e acompanhamos com vocês o que vira reunião e contrato, para o trabalho não ser julgado só pelo volume.'),
            ('Precisamos contratar tudo de uma vez?', 'Não. Montamos a entrega pelo que mais trava as vendas hoje e ampliamos conforme o resultado aparece.'),
            ('Atendem empresas fora de Curitiba?', 'Sim. Temos escritórios em Curitiba e em Cascavel, com reuniões presenciais ou online, e atendemos clientes em outros estados.'),
            ('Qual o investimento?', 'Definimos no diagnóstico, a partir do que vocês já têm, do mercado e do ticket. A proposta mostra escopo e verba sugerida antes de qualquer contratação.'),
        ],
        'servico_hidden': 'Campanha B2B',
        'segmento': '',
        'form_titulo': 'Solicite um diagnóstico',
        'form_desc': 'Respondemos com uma leitura do seu marketing e comercial hoje e o próximo passo.',
    },
]


def logos_html(slugs):
    """Dois carrosseis iguais aos da home: a lista da frente é dividida ao meio, a segunda faixa anda ao contrário."""
    def itens(lista):
        out = []
        for slug in lista:
            c = CLIENTES[slug]
            w, h = Image.open(os.path.join(ROOT, 'assets/images/clientes', slug + '.webp')).size
            classe = 'carousel-item carousel-item--escuro' if c.get('fundo') == 'escuro' else 'carousel-item'
            out.append(f'<li class="{classe}"><img src="/assets/images/clientes/{slug}.webp" alt="{c["nome"]}" width="{w // 2}" height="{h // 2}" loading="lazy" decoding="async"></li>')
        return '\n            '.join(out)

    meio = (len(slugs) + 1) // 2
    faixas = []
    for lista, reversa in ((slugs[:meio], False), (slugs[meio:], True)):
        grupo = itens(lista)
        classe = 'carousel-track carousel-reverse' if reversa else 'carousel-track'
        faixas.append(f'''      <div class="carousel-container">
        <div class="{classe}">
          <ul class="carousel-group" role="list">
            {grupo}
          </ul>
          <ul class="carousel-group" aria-hidden="true">
            {grupo}
          </ul>
        </div>
      </div>''')
    return '    <div class="carousel-faixas">\n' + '\n'.join(faixas) + '\n    </div>'


def cards_html(lista):
    return '\n'.join(f'''        <article class="seg-card">
          <span class="seg-card-icon" aria-hidden="true"><i class="{icone}"></i></span>
          <h3 class="font-serif text-lg text-prime-900 uppercase mb-3">{titulo}</h3>
          <p class="text-prime-600 font-light text-[15px] leading-[1.8]">{texto}</p>
        </article>''' for icone, titulo, texto in lista)


# Imagem e categoria de cada serviço na galeria das LPs (mesmo visual do Portfólio da home)
GALERIA = {
    'Posicionamento e marca': ('portfolio-06.webp', 'Branding', 'Identidade visual de marca aplicada na parede de um escritório'),
    'Site e páginas de captação': ('portfolio-02.webp', 'Sites e landing pages', 'Site institucional responsivo exibido em um notebook'),
    'Site e página de captação': ('portfolio-02.webp', 'Sites e landing pages', 'Site institucional responsivo exibido em um notebook'),
    'Google Ads e Meta Ads': ('portfolio-03.webp', 'Mídia paga', 'Página de campanha integrada ao Google Ads e ao Meta Ads exibida em um tablet'),
    'Conteúdo e redes sociais': ('portfolio-01.webp', 'Conteúdo', 'Feed de Instagram com conteúdo criado pela Conceito Prime'),
    'Atendimento e CRM': ('/assets/images/popup-consultor-v2.webp', 'CRM', 'Consultor da Conceito Prime atendendo à mesa de reunião'),
    'Medição e CRM': ('/assets/images/popup-consultor-v2.webp', 'Medição e CRM', 'Consultor da Conceito Prime atendendo à mesa de reunião'),
    'Treinamento e materiais de venda': ('portfolio-05.webp', 'Time comercial', 'Catálogo e revista impressos usados como material de venda'),
}


def galeria_html(lista):
    itens = []
    for _icone, titulo, texto in lista:
        img, cat, alt = GALERIA[titulo]
        src = img if img.startswith('/') else f'/assets/images/portfolio/{img}'
        itens.append(f'''        <figure class="port-item group">
          <img src="{src}" alt="{alt}" width="800" height="800" loading="lazy" decoding="async">
          <figcaption class="port-legenda">
            <span class="port-cat">{cat}</span>
            <h3 class="port-titulo">{titulo}</h3>
            <p class="port-desc">{texto}</p>
          </figcaption>
        </figure>''')
    return '\n'.join(itens)


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
              <img src="/assets/images/depoimentos/{img}" alt="{alt}" width="1600" height="857" loading="lazy" decoding="async">
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


def opcoes(lista, placeholder):
    return f'<option value="" disabled selected>{placeholder}</option>' + ''.join(f'<option value="{v}">{t}</option>' for v, t in lista)


FATURAMENTO = [('ate-10k', 'Até R$ 10 mil'), ('10k-50k', 'De R$ 10 mil a R$ 50 mil'), ('50k-100k', 'De R$ 50 mil a R$ 100 mil'),
               ('100k-500k', 'De R$ 100 mil a R$ 500 mil'), ('500k-1m', 'De R$ 500 mil a R$ 1 milhão'),
               ('1m-5m', 'De R$ 1 milhão a R$ 5 milhões'), ('acima-5m', 'Acima de R$ 5 milhões'), ('nao-faturou', 'Ainda não faturou')]
SEGMENTOS = [('industria', 'Indústria'), ('distribuidor', 'Distribuidor ou atacado'), ('servicos', 'Serviços'), ('tecnologia', 'Tecnologia'),
             ('saude', 'Saúde e Bem-estar'), ('imobiliario', 'Imobiliário e construção'), ('alimentacao', 'Alimentação'),
             ('ecommerce', 'E-commerce'), ('varejo', 'Varejo'), ('educacao', 'Educação'), ('outros', 'Outros')]
CARGOS = [('socio-diretor', 'Sócio ou Diretor'), ('gerente-mkt-comercial', 'Gerente de Marketing ou Comercial'), ('analista', 'Analista'), ('outro', 'Outro')]
INVESTIMENTO = [('nao-investe', 'Ainda não investimos'), ('ate-2k', 'Até R$ 2 mil'), ('2k-5k', 'De R$ 2 mil a R$ 5 mil'),
                ('5k-15k', 'De R$ 5 mil a R$ 15 mil'), ('acima-15k', 'Acima de R$ 15 mil')]


def formulario(pg):
    """Formulário "Solicite um diagnóstico": o mesmo do site inteiro, montado em etapas pelo brand.js
    (initDiagnostico). Nas LPs (body data-contato="formulario") ele envia para /api/lead-b2b e
    redireciona para a página de obrigado. O botão do WhatsApp abre o mesmo formulário em popup."""
    desc = f"{pg['form_desc']} Nosso trabalho é pensado para empresas que já faturam a partir de R$ 100 mil por mês."
    seg = f' data-segmento="{pg["segmento"]}"' if pg['segmento'] else ''
    return f'''  <section id="orcamento" class="cb-form-sec" aria-labelledby="cb-form-titulo">
    <div class="cb-form-card">
      <form id="cb-form" class="diag" data-diagnostico data-pagina="{pg['slug']}"{seg} data-titulo-id="cb-form-titulo" data-desc="{desc}" aria-label="Solicite um diagnóstico"></form>
    </div>
  </section>'''


def tag_google():
    if not GOOGLE_TAG_ID:
        return ''
    return (f'\n  <script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_TAG_ID}"></script>\n'
            f"  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GOOGLE_TAG_ID}');</script>")


def cabeca(titulo, descricao, url, robots, schema=''):
    sch = f'\n  <script type="application/ld+json">{schema}</script>' if schema else ''
    return f'''<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo}</title>
  <link rel="canonical" href="{url}">
  <meta name="description" content="{descricao}">
  <meta name="robots" content="{robots}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descricao}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
  <link rel="icon" href="/assets/images/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/cairo.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
  <style>
{CSS_LOCAL}
  </style>{sch}{tag_google()}
</head>'''


def topo(link_logo, com_cta):
    logo = '<img src="/assets/images/logo.webp" alt="Conceito Prime" width="1250" height="356">'
    logo = f'<a href="{link_logo}" class="cb-topo-logo">{logo}</a>' if link_logo else f'<span class="cb-topo-logo">{logo}</span>'
    cta = '<a href="#orcamento" class="cb-topo-cta" data-cta="topo">Solicitar diagnóstico</a>' if com_cta else ''
    # Navegação só por âncoras da própria página: dá contexto sem tirar o visitante da LP
    nav = ('''<nav class="cb-topo-nav" aria-label="Seções da página">
        <a href="#seg-logos" data-cta="menu-clientes">Clientes</a>
        <a href="#seg-metodo" data-cta="menu-metodo">Como trabalhamos</a>
        <a href="#depoimentos" data-cta="menu-depoimentos">Depoimentos</a>
        <a href="#seg-faq" data-cta="menu-perguntas">Perguntas</a>
      </nav>''' if com_cta else '')
    return f'''  <header class="cb-topo">
    <div class="cb-topo-in">
      {logo}
      {nav}
      {cta}
    </div>
  </header>'''


def rodape(js):
    return f'''  <footer class="cb-rodape">
    <div class="cb-rodape-in">
      <img src="/assets/images/logo-footer.webp" alt="Conceito Prime" width="400" height="114" loading="lazy" decoding="async">
      <p><i class="fas fa-location-dot" aria-hidden="true"></i> {ENDERECO}</p>
      <p><a href="/quem-somos/" target="_blank" rel="noopener">Quem somos</a> <span aria-hidden="true">·</span> © 2026 Conceito Prime</p>
    </div>
  </footer>
  <script src="/assets/js/brand.js" defer></script>{script_local(js)}
</body>
</html>'''


def script_local(js):
    if not js:
        return ''
    return f'''
  <script>
document.addEventListener('DOMContentLoaded', function () {{
{js}
}});
  </script>'''


def promessas_html():
    itens = '\n'.join(f'      <li><i class="{i}" aria-hidden="true"></i><span>{t}</span></li>' for i, t in PROMESSAS)
    return f'''  <section class="cb-promessas" aria-label="Como trabalhamos">
    <ul role="list">
{itens}
    </ul>
  </section>'''


def numeros_html():
    return '''  <section class="bg-prime-900 py-16" aria-label="Números da Conceito Prime">
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
  </section>'''


def filtro_html(pg):
    sim = '\n'.join(f'          <li><i class="fas fa-check" aria-hidden="true"></i><span>{t}</span></li>' for t in pg['faz_sentido'])
    nao = '\n'.join(f'          <li><i class="fas fa-times" aria-hidden="true"></i><span>{t}</span></li>' for t in NAO_FAZ_SENTIDO)
    return f'''  <section class="cb-filtro-sec" aria-labelledby="cb-filtro-titulo">
    <h2 id="cb-filtro-titulo" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight mb-14">A conversa vale <span class="text-gold-400">para os dois lados</span></h2>
    <div class="cb-filtro">
      <div class="cb-filtro-col cb-sim">
        <h3>Faz sentido conversarmos se</h3>
        <ul role="list">
{sim}
        </ul>
      </div>
      <div class="cb-filtro-col cb-nao">
        <h3>Provavelmente não somos a melhor opção se</h3>
        <ul role="list">
{nao}
        </ul>
      </div>
    </div>
  </section>'''


def videos_secao(pg):
    slides, dots = videos_html(pg['videos'])
    return f'''  <section id="depoimentos" class="py-24 bg-prime-950 border-b border-prime-800" aria-labelledby="video-depoimentos-title">
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
      <div class="video-dots" role="group" aria-label="Navegar depoimentos em vídeo">
        {dots}
      </div>
    </div>
  </section>'''


def pagina(pg):
    url = f'{SITE}/{pg["slug"]}/'
    schema = json.dumps([
        {'@context': 'https://schema.org', '@type': 'Service', 'name': pg['eyebrow'], 'description': pg['description'],
         'provider': {'@type': 'Organization', 'name': 'Conceito Prime', 'url': SITE,
                      'address': {'@type': 'PostalAddress', 'streetAddress': 'R. Antônio Rodrigues, 76', 'addressLocality': 'Curitiba',
                                  'addressRegion': 'PR', 'addressCountry': 'BR'}},
         'areaServed': {'@type': 'Country', 'name': 'Brasil'}, 'url': url},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': p, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for p, r in pg['faq']]},
    ], ensure_ascii=False)
    eyebrow_logos = (f'\n      <p class="text-gold-500 font-semibold uppercase tracking-[0.3em] text-[11px] text-center mb-4">{pg["logos_eyebrow"]}</p>'
                     if pg['logos_eyebrow'] else '')
    return cabeca(pg['title'], pg['description'], url, 'index, follow', schema) + f'''
<body class="font-sans text-prime-800 antialiased" data-contato="formulario" data-lp="{pg['slug']}">

{topo(f"/{pg['slug']}/", True)}

  <main>
  <section class="hero-bg seg-hero pt-36 pb-24 lg:pt-44 lg:pb-28" aria-labelledby="seg-titulo">
    <div class="hero-content max-w-4xl mx-auto px-6 lg:px-8 text-center">
      <p class="cb-selo"><i class="fas fa-check" aria-hidden="true"></i> Para empresas com faturamento acima de R$ 100 mil/mês</p>
      <p class="text-gold-400 font-semibold uppercase tracking-[0.3em] text-[11px] mb-6">{pg['eyebrow']}</p>
      <h1 id="seg-titulo" class="font-serif text-4xl sm:text-5xl lg:text-6xl text-white leading-[1.1] mb-8 uppercase">{pg['h1']}</h1>
      <p class="text-white/75 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto mb-10">{pg['sub']}</p>
      <a href="#orcamento" class="cb-cta" data-cta="hero-{pg['slug']}"><i class="fas fa-magnifying-glass" aria-hidden="true"></i> Solicitar diagnóstico</a>
    </div>
  </section>

{promessas_html()}

  <section class="pt-20 pb-14 bg-white overflow-hidden" aria-labelledby="seg-logos">
    <div class="max-w-6xl mx-auto px-6 lg:px-8">{eyebrow_logos}
      <h2 id="seg-logos" class="font-serif text-2xl sm:text-3xl text-prime-900 uppercase text-center mb-12">{pg['logos_titulo']}</h2>
    </div>
{logos_html(pg['logos'])}
  </section>

{numeros_html()}

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

  <section class="py-24 bg-prime-50" aria-labelledby="seg-servicos">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <h2 id="seg-servicos" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight mb-14">{pg['servicos_titulo']}</h2>
      <div class="port-grade">
{galeria_html(pg['servicos'])}
      </div>
    </div>
  </section>

{videos_secao(pg)}

{filtro_html(pg)}

{ESTRUTURA}

{formulario(pg)}

  <section class="py-24 bg-prime-50" aria-labelledby="seg-faq">
    <div class="max-w-3xl mx-auto px-6 lg:px-8">
      <h2 id="seg-faq" class="font-serif text-3xl sm:text-4xl text-prime-900 uppercase text-center leading-tight mb-12">Perguntas <span class="text-gold-400">frequentes</span></h2>
      <div class="seg-faqs">
{faq_html(pg['faq'])}
      </div>
    </div>
  </section>
  </main>

''' + rodape('')


OBRIGADO = [
    {
        'slug': 'obrigado-qualificado',
        'title': 'Recebemos seu pedido de diagnóstico | Conceito Prime',
        'description': 'Recebemos seu pedido de diagnóstico. Fale agora com o comercial da Conceito Prime pelo WhatsApp ou deixe uma reunião agendada.',
        'conversoes': [CONVERSAO_QUALIFICADO, CONVERSAO_TODOS],
        'tipos': 'qualificado,todos',
        'corpo': f'''      <i class="fas fa-check-circle" aria-hidden="true"></i>
      <h1>Recebemos seu pedido<span data-lead-nome></span></h1>
      <p>Pelo que vocês contaram, o perfil da empresa tem tudo a ver com o nosso trabalho. Nosso time comercial já recebeu os dados e vai preparar a leitura do seu mercado.</p>
      <p>Se quiser adiantar, fale agora com a gente ou já deixe uma conversa agendada:</p>
      <div class="cb-acoes">
        <a class="cb-btn-wa" href="https://wa.me/{WA_COMERCIAL}" target="_blank" rel="noopener" data-cta="obrigado-whatsapp" data-wa-numero="{WA_COMERCIAL}" data-wa-msg="Olá! Acabei de pedir um diagnóstico pelo site da Conceito Prime e quero adiantar a conversa."><i class="fab fa-whatsapp" aria-hidden="true"></i> Falar no WhatsApp</a>
        <a class="cb-btn-agenda" href="https://wa.me/{WA_COMERCIAL}" target="_blank" rel="noopener" data-cta="obrigado-agendar" data-wa-numero="{WA_COMERCIAL}" data-wa-msg="Olá! Acabei de pedir um diagnóstico pelo site da Conceito Prime e quero agendar uma reunião."><i class="fas fa-clock" aria-hidden="true"></i> Agendar reunião</a>
      </div>''',
    },
    {
        'slug': 'obrigado',
        'title': 'Recebemos seus dados | Conceito Prime',
        'description': 'Recebemos seus dados. O time da Conceito Prime analisa cada pedido e retorna pelo WhatsApp informado no formulário.',
        'conversoes': [CONVERSAO_TODOS],
        'tipos': 'todos',
        'corpo': '''      <i class="fas fa-check-circle" aria-hidden="true"></i>
      <h1>Recebemos seus dados<span data-lead-nome></span></h1>
      <p>Obrigado pelo interesse. Nosso time analisa cada pedido e retorna pelo WhatsApp que você informou.</p>
      <p>Enquanto isso, separamos conteúdos do nosso blog sobre marketing e vendas para empresas.</p>
      <p><a class="cb-link" href="/blog/">Ver os artigos do blog</a></p>''',
    },
]


def pagina_obrigado(ob):
    url = f'{SITE}/{ob["slug"]}/'
    conv = ','.join(c for c in ob['conversoes'] if c)
    return cabeca(ob['title'], ob['description'], url, 'noindex, nofollow') + f'''
<body class="font-sans text-prime-800 antialiased" data-contato="formulario" data-lp="{ob['slug']}" data-conversoes="{conv}" data-tipos-conversao="{ob['tipos']}">

{topo('', False)}

  <main class="cb-obrigado">
    <div class="cb-obrigado-card">
{ob['corpo']}
    </div>
  </main>

''' + rodape(JS_OBRIGADO)


def main():
    for pg in PAGINAS:
        destino = os.path.join(ROOT, pg['slug'])
        os.makedirs(destino, exist_ok=True)
        with open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina(pg))
        print(f'Criada /{pg["slug"]}/')
    for ob in OBRIGADO:
        destino = os.path.join(ROOT, ob['slug'])
        os.makedirs(destino, exist_ok=True)
        with open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina_obrigado(ob))
        print(f'Criada /{ob["slug"]}/')
    if not GOOGLE_TAG_ID:
        print('Info: conversões saem como evento conversao_lead_b2b no dataLayer, para o GTM (conteudo/rastreamento.json).')


if __name__ == '__main__':
    main()
