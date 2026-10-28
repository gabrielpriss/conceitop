#!/usr/bin/env python3
"""Gera as páginas dos artigos (/blog/<slug>/) e a listagem do blog a partir de conteudo/blog/.

Uso: python3 scripts/generate-blog.py
Entradas:
  conteudo/blog/posts.json       metadados de cada artigo (campos em conteudo/blog/REGRAS.md)
  conteudo/blog/<slug>.html      corpo dos artigos novos (HTML limpo: h2, h3, p, ul, ol, table, a, strong)
  conteudo/blog/<slug>.raw.html  corpo dos 16 artigos migrados do WordPress antigo
Saídas:
  blog/<slug>/index.html, blog/index.html e blog/pagina/<n>/ (12 artigos por página),
  blog/feed.xml (RSS) e a seção do blog no sitemap.xml
"""
import html as H
import json, math, os, re
from datetime import date
from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = 'https://conceitop.com.br'
POSTS = json.load(open(os.path.join(ROOT, 'conteudo/blog/posts.json'), encoding='utf-8'))
SLUGS = {p['slug'] for p in POSTS}
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
CAT_COR = {
    'Vendas': 'bg-orange-100 text-orange-800',
    'Marketing Digital': 'bg-blue-100 text-blue-800',
    'Estratégias de Marketing': 'bg-amber-100 text-amber-900',
    'Gestão': 'bg-emerald-100 text-emerald-800',
}
LINK_CORRIGIDO = {'/icas-para-fazer-um-feedback-de-sucesso/': '/blog/dicas-para-fazer-um-feedback-de-sucesso/'}


def data_extenso(iso):
    d = date.fromisoformat(iso)
    return f'{d.day} de {MESES[d.month - 1]} de {d.year}'


def sem_travessao(t):
    """Padrão da casa: nenhum travessão no texto publicado."""
    t = re.sub(r'(?<=\d) ?[–—] ?(?=\S)', '. ', t)                        # "1 – Texto" -> "1. Texto"
    t = re.sub(r'\b(SEO|CRM) [–—] ([^<.;]+)', r'\1 (\2)', t)              # "SEO – Search..." -> "SEO (Search...)"
    t = t.replace('outbound – ou seja, a prospecção comercial ativa, quando VOCÊ vai em busca do cliente – a hashtag',
                  'outbound (ou seja, a prospecção comercial ativa, quando VOCÊ vai em busca do cliente), a hashtag')
    t = re.sub(r'^([^<]{1,40}?) [–—] ', r'\1: ', t)                        # "Uber – quando..." -> "Uber: quando..."
    t = re.sub(r' ?[–—] ?', ', ', t)
    return t


def limpar(raw, slug):
    s = BeautifulSoup(raw, 'html.parser')
    # título duplicado solto no começo (último artigo)
    primeiro = next((n for n in s.contents if not (isinstance(n, NavigableString) and not n.strip())), None)
    if getattr(primeiro, 'name', None) == 'strong':
        primeiro.decompose()
    # embeds do Instagram que viraram só texto e frases que apontam para mídia que não existe mais
    for bq in s.find_all('blockquote'):
        if 'instagram' in bq.get_text().lower() or bq.find('a', href=re.compile('instagram.com')):
            bq.decompose()
    for no in list(s.find_all(string=re.compile(r'Confira no vídeo mais dicas|Como no exemplo da imagem abaixo'))):
        novo = re.sub(r'\s*(Confira no vídeo mais dicas de um especialista em atendimento\.|Como no exemplo da imagem abaixo:)', '', str(no))
        no.replace_with(novo)
    # subtítulo perdido virou parágrafo
    for p in s.find_all('p'):
        if p.get_text(strip=True) == 'Identifique-se':
            p.name = 'h2'
    # títulos: sem negrito interno, h4/h5 viram h3
    for h in s.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        texto = re.sub(r'\s+', ' ', h.get_text()).strip()
        if h.name in ('h4', 'h5', 'h6'):
            h.name = 'h3'
        h.clear()
        h.append(texto)
    # links: internos para /blog/, externos em nova aba
    for a in s.find_all('a'):
        href = (a.get('href') or '').strip()
        href = LINK_CORRIGIDO.get(href, href)
        m = re.fullmatch(r'/([a-z0-9-]+)/', href)
        if m and m.group(1) in SLUGS:
            href = f'/blog/{m.group(1)}/'
        if href.startswith('http'):
            a['target'] = '_blank'
            a['rel'] = 'noopener'
        a['href'] = href
        if not a.get_text(strip=True):
            a.unwrap()
    for tag in s.find_all(['strong', 'em', 'p', 'li']):
        if not tag.get_text(strip=True) and not tag.find('br'):
            tag.decompose()
    out = str(s)
    out = re.sub(r'(<(strong|em)>)\s+', r' \1', out)
    out = re.sub(r'\s+(</(strong|em)>)', r'\1 ', out)
    out = re.sub(r' +', ' ', out)
    out = re.sub(r' ([.,;:!?])', r'\1', out)
    out = re.sub(r'(?<=[a-zà-ú.])(?=<a )', ' ', out)        # "do<a" -> "do <a"
    out = re.sub(r'([.!?])(?=[A-ZÀ-Ú])', r'\1 ', out)        # "comprador.É" -> "comprador. É"
    out = sem_travessao(out)
    # primeiro parágrafo em itálico é a linha fina do artigo
    lead = ''
    m = re.match(r'\s*<p><em>(.*?)</em></p>\s*', out, re.S)
    if m:
        lead = m.group(1).strip()
        out = out[m.end():]
    return lead, out.strip()


def bloco(src, inicio, fim, incluir_fim=True):
    a = src.index(inicio)
    b = src.index(fim, a) + (len(fim) if incluir_fim else 0)
    return src[a:b]


def card(p, eager=False, h='h2'):
    cor = CAT_COR.get(p['categoria'], 'bg-gray-100 text-gray-800')
    d = date.fromisoformat(p['data']).strftime('%d/%m/%Y')
    return f'''        <article class="post-card group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden relative" data-cat="{p['categoria']}">
          <div class="aspect-video overflow-hidden relative">
            <img src="/blog/assets/capas/{p['slug']}-600.webp" srcset="/blog/assets/capas/{p['slug']}-600.webp 600w, /blog/assets/capas/{p['slug']}.webp 1200w" sizes="(min-width: 1024px) 400px, (min-width: 640px) 50vw, 100vw" alt="{H.escape(p['titulo'])}" width="600" height="315" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {'' if eager else 'loading="lazy" '}decoding="async">
          </div>
          <div class="p-6">
            <div class="flex items-center gap-2 mb-4">
              <span class="{cor} font-semibold text-xs px-3 py-1 rounded-full">{p['categoria']}</span>
              <time class="text-gray-600 text-xs" datetime="{p['data']}">{d}</time>
            </div>
            <{h} class="font-bold font-serif text-prime-900 text-lg leading-snug mb-3">
              <a href="/blog/{p['slug']}/" class="post-card-link">{H.escape(p['titulo'])}</a>
            </{h}>
            <p class="text-gray-600 text-sm leading-relaxed line-clamp-3">{H.escape(p['descricao'])}</p>
            <span class="inline-flex items-center gap-1 text-prime-900 font-semibold text-sm mt-4 uppercase tracking-widest" aria-hidden="true">
              Ler artigo <i class="fas fa-arrow-right text-xs"></i>
            </span>
          </div>
        </article>'''


POR_PAGINA = 12
CATEGORIAS = ['Vendas', 'Marketing Digital', 'Estratégias de Marketing', 'Gestão']


def slug_ancora(texto, usados):
    import unicodedata
    t = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60] or 'secao'
    base, n = t, 2
    while t in usados:
        t = f'{base}-{n}'
        n += 1
    usados.add(t)
    return t


def corpo_do_post(p):
    """Lê o corpo (novo .html ou migrado .raw.html), põe âncoras nos h2 e devolve (lead, corpo, sumário)."""
    novo = os.path.join(ROOT, f"conteudo/blog/{p['slug']}.html")
    antigo = os.path.join(ROOT, f"conteudo/blog/{p['slug']}.raw.html")
    raw = open(novo if os.path.exists(novo) else antigo, encoding='utf-8').read()
    lead, corpo = limpar(raw, p['slug'])
    s = BeautifulSoup(corpo, 'html.parser')
    usados, sumario = set(), []
    for h in s.find_all('h2'):
        texto = h.get_text(' ', strip=True)
        if texto.lower().startswith('perguntas frequentes'):
            continue
        h['id'] = slug_ancora(texto, usados)
        sumario.append((h['id'], texto))
    for t in s.find_all('table'):
        if not (t.parent and t.parent.name == 'div' and 'post-tabela' in (t.parent.get('class') or [])):
            t.wrap(s.new_tag('div', attrs={'class': 'post-tabela'}))
    return lead, str(s), sumario


def cta_meio(p):
    return (
        '\n<aside class="blog-cta-meio" aria-label="Diagnóstico gratuito">\n'
        '  <p class="blog-cta-meio-selo">Para empresas a partir de R$ 100 mil por mês</p>\n'
        '  <p class="blog-cta-meio-titulo">Quer esse resultado na sua empresa?</p>\n'
        '  <p class="blog-cta-meio-texto">Em 3 perguntas rápidas entendemos o seu momento e mostramos o próximo passo para vender mais.</p>\n'
        f'  <a href="#diagnostico" class="btn-wa inline-flex items-center gap-2 px-6 py-3 uppercase tracking-[0.15em] text-xs font-bold" data-cta="artigo-meio-{p["slug"]}">Solicitar diagnóstico <i class="fas fa-arrow-right" aria-hidden="true"></i></a>\n'
        '</aside>\n'
    )


def inserir_cta_meio(corpo, p):
    """Põe o CTA no meio do artigo: antes do h2 do meio, ou depois do parágrafo do meio."""
    posicoes = [m.start() for m in re.finditer(r'<h2[ >]', corpo)]
    if len(posicoes) >= 3:
        k = posicoes[len(posicoes) // 2]
    else:
        fins = [m.end() for m in re.finditer(r'</p>', corpo)]
        if len(fins) < 4:
            return corpo
        k = fins[len(fins) // 2]
    return corpo[:k] + cta_meio(p) + corpo[k:]


def faq_html(faq):
    if not faq:
        return ''
    itens = '\n'.join(
        f'      <details class="blog-faq-item"><summary>{H.escape(q["pergunta"])}</summary><p>{H.escape(q["resposta"])}</p></details>'
        for q in faq)
    return ('\n    <section class="blog-faq" aria-labelledby="faq-titulo">\n'
            '      <h2 id="faq-titulo">Perguntas frequentes</h2>\n'
            f'{itens}\n'
            '    </section>')


def bloco_fontes(fontes):
    if not fontes:
        return ''
    itens = '\n'.join(f'        <li><a href="{H.escape(f["url"])}" target="_blank" rel="noopener">{H.escape(f["nome"])}</a></li>' for f in fontes)
    return ('\n    <section class="blog-fontes" aria-labelledby="fontes-titulo">\n'
            '      <h2 id="fontes-titulo">Fontes consultadas</h2>\n'
            '      <ul>\n'
            f'{itens}\n'
            '      </ul>\n'
            '    </section>')


def grade_paginada(base, ordenados):
    """Listagem com 12 artigos por página: /blog/ e /blog/pagina/<n>/."""
    import shutil
    paginas = max(1, math.ceil(len(ordenados) / POR_PAGINA))
    a = base.index('  <!-- ========== BLOG POSTS ========== -->')
    b = base.index('  <!-- ========== NEWSLETTER BANNER ========== -->')
    for n in range(1, paginas + 1):
        fatia = ordenados[(n - 1) * POR_PAGINA:n * POR_PAGINA]
        grade = '\n\n'.join(card(p, eager=(n == 1 and i < 3)) for i, p in enumerate(fatia))
        nav = ''
        if paginas > 1:
            links = []
            if n > 1:
                ant = '/blog/' if n == 2 else f'/blog/pagina/{n - 1}/'
                links.append(f'<a href="{ant}" class="blog-pag-link" rel="prev">Artigos mais recentes</a>')
            links.append(f'<span class="blog-pag-atual">Página {n} de {paginas}</span>')
            if n < paginas:
                links.append(f'<a href="/blog/pagina/{n + 1}/" class="blog-pag-link" rel="next">Artigos anteriores</a>')
            nav = '\n      <nav class="blog-paginacao" aria-label="Páginas do blog">' + ' '.join(links) + '</nav>'
        bloco_html = (
            '  <!-- ========== BLOG POSTS ========== -->\n'
            '  <section class="py-20 bg-slate-50" aria-label="Artigos">\n'
            '    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">\n\n'
            '      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8" id="posts-grid">\n\n'
            f'{grade}\n\n'
            '      </div>\n'
            f'      <p class="text-center text-gray-600 mt-10 hidden" data-sem-resultado>Nenhum artigo nesta categoria.</p>{nav}\n\n'
            '    </div>\n'
            '  </section>\n\n')
        pagina = base[:a] + bloco_html + base[b:]
        url_pag = f'{DOM}/blog/' if n == 1 else f'{DOM}/blog/pagina/{n}/'
        ld_lista = {
            '@context': 'https://schema.org',
            '@graph': [
                {'@type': 'CollectionPage', '@id': url_pag, 'url': url_pag, 'name': 'Blog da Conceito Prime',
                 'inLanguage': 'pt-BR', 'isPartOf': {'@type': 'WebSite', 'url': DOM + '/', 'name': 'Conceito Prime'},
                 'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                     {'@type': 'ListItem', 'position': (n - 1) * POR_PAGINA + i + 1, 'url': f"{DOM}/blog/{q['slug']}/", 'name': q['titulo']}
                     for i, q in enumerate(fatia)]}},
                {'@type': 'BreadcrumbList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': DOM + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': DOM + '/blog/'}]},
            ]}
        pagina = re.sub(r'\s*<script type="application/ld\+json" data-lista>.*?</script>', '', pagina, flags=re.S)
        pagina = pagina.replace('</head>', f'  <script type="application/ld+json" data-lista>{json.dumps(ld_lista, ensure_ascii=False)}</script>\n</head>', 1)
        if n == 1:
            open(os.path.join(ROOT, 'blog/index.html'), 'w', encoding='utf-8').write(pagina)
            continue
        url = f'{DOM}/blog/pagina/{n}/'
        pagina = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', pagina)
        pagina = re.sub(r'<title>([^<]*)</title>', lambda m: f'<title>Blog da Conceito Prime, página {n}</title>', pagina, count=1)
        pagina = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', pagina)
        destino = os.path.join(ROOT, 'blog', 'pagina', str(n))
        os.makedirs(destino, exist_ok=True)
        open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8').write(pagina)
    pasta = os.path.join(ROOT, 'blog', 'pagina')
    if os.path.isdir(pasta):
        for nome in os.listdir(pasta):
            if nome.isdigit() and int(nome) > paginas:
                shutil.rmtree(os.path.join(pasta, nome))
    return paginas


def feed_rss(ordenados):
    from email.utils import format_datetime
    from datetime import datetime, timezone
    itens = []
    for p in ordenados[:30]:
        dt = datetime.fromisoformat(p['data']).replace(hour=9, tzinfo=timezone.utc)
        itens.append(
            '  <item>\n'
            f'    <title>{H.escape(p["titulo"])}</title>\n'
            f'    <link>{DOM}/blog/{p["slug"]}/</link>\n'
            f'    <guid isPermaLink="true">{DOM}/blog/{p["slug"]}/</guid>\n'
            f'    <pubDate>{format_datetime(dt)}</pubDate>\n'
            f'    <category>{H.escape(p["categoria"])}</category>\n'
            f'    <description>{H.escape(p["descricao"])}</description>\n'
            '  </item>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
           '  <title>Blog da Conceito Prime</title>\n'
           f'  <link>{DOM}/blog/</link>\n'
           f'  <atom:link href="{DOM}/blog/feed.xml" rel="self" type="application/rss+xml"/>\n'
           '  <description>Marketing, vendas e Google Ads para empresas que querem vender mais. Escritórios em Curitiba e Cascavel.</description>\n'
           '  <language>pt-BR</language>\n'
           + '\n'.join(itens) + '\n</channel>\n</rss>\n')
    open(os.path.join(ROOT, 'blog/feed.xml'), 'w', encoding='utf-8').write(xml)


BARRA_JS = ("<script>(function(){var b=document.querySelector('[data-blog-barra]'),d=document.getElementById('diagnostico');"
            "if(!b||!d||!('IntersectionObserver' in window))return;var vis=false,topo=false;"
            "function up(){b.classList.toggle('is-oculta',vis||!topo);}"
            "new IntersectionObserver(function(e){vis=e[0].isIntersecting;up();}).observe(d);"
            "window.addEventListener('scroll',function(){topo=window.scrollY>480;up();},{passive:true});up();})();</script>")


def pagina_post(p, ordenados, header, footer, scripts, favicons):
    lead, corpo, sumario = corpo_do_post(p)
    lead = lead or H.escape(p.get('linha_fina', ''))
    palavras = len(re.sub(r'<[^>]+>', ' ', corpo).split())
    minutos = max(1, math.ceil(palavras / 200))
    corpo = inserir_cta_meio(corpo, p)
    url = f"{DOM}/blog/{p['slug']}/"
    atualizado = p.get('atualizado') or p['data']
    imagem = f"{DOM}/assets/images/og/{p['slug']}.jpg"
    outros = [x for x in ordenados if x['slug'] != p['slug']]
    relacionados = [x for x in outros if p.get('local') and x.get('local') == p.get('local')]
    relacionados += [x for x in outros if x['categoria'] == p['categoria'] and x not in relacionados]
    relacionados += [x for x in outros if x not in relacionados]
    relacionados = relacionados[:3]
    posting = {
        '@type': 'BlogPosting',
        'headline': p['titulo'],
        'description': p['descricao'],
        'datePublished': p['data'],
        'dateModified': atualizado,
        'inLanguage': 'pt-BR',
        'image': {'@type': 'ImageObject', 'url': imagem, 'width': 1200, 'height': 630},
        'mainEntityOfPage': url,
        'wordCount': palavras,
        'articleSection': p['categoria'],
        'author': {'@type': 'Organization', 'name': 'Conceito Prime', 'url': DOM},
        'publisher': {'@type': 'Organization', 'name': 'Conceito Prime', 'url': DOM,
                      'logo': {'@type': 'ImageObject', 'url': f'{DOM}/assets/images/logo.webp'}},
    }
    if p.get('palavras_chave'):
        posting['keywords'] = ', '.join(p['palavras_chave'])
    if p.get('local') and p['local'] != 'Brasil':
        posting['contentLocation'] = {'@type': 'Place', 'name': p['local']}
    grafo = [posting, {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': f'{DOM}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': f'{DOM}/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': p['titulo'], 'item': url},
        ],
    }]
    if p.get('faq'):
        grafo.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q['pergunta'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['resposta']}}
            for q in p['faq']]})
    ld = {'@context': 'https://schema.org', '@graph': grafo}
    titulo_pag = p.get('titulo_seo') or f"{p['titulo']} | Conceito Prime"
    lead_html = f'<p class="text-white/75 text-lg sm:text-xl leading-relaxed max-w-3xl mx-auto mb-8">{lead}</p>' if lead else ''
    rel_html = '\n'.join(card(x, h='h3') for x in relacionados)
    sumario_html = ''
    if len(sumario) >= 3:
        itens = '\n'.join(f'            <li><a href="#{a}">{H.escape(t)}</a></li>' for a, t in sumario)
        sumario_html = ('\n          <nav class="blog-sumario" aria-labelledby="sumario-titulo">\n'
                        '            <p id="sumario-titulo" class="blog-aside-titulo">Neste artigo</p>\n'
                        f'            <ol>\n{itens}\n            </ol>\n'
                        '          </nav>')
    atualizado_txt = (f' <span aria-hidden="true">·</span> atualizado em <time datetime="{atualizado}">{data_extenso(atualizado)}</time>'
                      if atualizado != p['data'] else '')
    slug = p['slug']
    return f'''<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{H.escape(titulo_pag)}</title>
  <meta name="description" content="{H.escape(p['descricao'])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Conceito Prime">
  <meta property="og:title" content="{H.escape(p['titulo'])}">
  <meta property="og:description" content="{H.escape(p['descricao'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{imagem}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{H.escape(p['titulo'])}">
  <meta property="article:published_time" content="{p['data']}">
  <meta property="article:modified_time" content="{atualizado}">
  <meta property="article:section" content="{p['categoria']}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="Blog da Conceito Prime" href="/blog/feed.xml">
  <link rel="preload" href="/assets/fonts/cairo.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
{favicons}
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="font-sans text-gray-900 antialiased">

{header}

  <main>
  <article>
    <header class="hero-bg pt-40 pb-16">
      <div class="hero-content max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <nav aria-label="Trilha de navegação" class="text-white/70 text-xs uppercase tracking-widest mb-6">
          <a href="/" class="hover:text-gold-400">Início</a> <span aria-hidden="true">/</span>
          <a href="/blog/" class="hover:text-gold-400">Blog</a> <span aria-hidden="true">/</span>
          <span class="text-gold-400">{p['categoria']}</span>
        </nav>
        <h1 class="text-3xl sm:text-5xl font-serif font-normal text-white mb-6 leading-tight">{H.escape(p['titulo'])}</h1>
        {lead_html}
        <p class="text-white/70 text-sm">Por Equipe Conceito Prime <span aria-hidden="true">·</span> <time datetime="{p['data']}">{data_extenso(p['data'])}</time>{atualizado_txt} <span aria-hidden="true">·</span> {minutos} min de leitura</p>
      </div>
    </header>

    <div class="bg-white">
      <div class="blog-layout max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div class="blog-coluna">
          <figure class="blog-capa">
            <img src="/blog/assets/capas/{slug}.webp" srcset="/blog/assets/capas/{slug}-600.webp 600w, /blog/assets/capas/{slug}.webp 1200w" sizes="(min-width: 1024px) 740px, 100vw" alt="{H.escape(p['titulo'])}" width="1200" height="630" class="w-full h-auto rounded-2xl" fetchpriority="high" decoding="async">
          </figure>
          <div class="post-content">
{corpo}
          </div>
{faq_html(p.get('faq'))}
{bloco_fontes(p.get('fontes'))}
        </div>

        <aside class="blog-aside" aria-label="Atalhos do artigo">
          <div class="blog-aside-cartao">
            <p class="blog-aside-titulo">Diagnóstico gratuito</p>
            <p class="blog-aside-texto">Quer vender mais com o marketing da sua empresa? Entendemos o seu momento e respondemos com o próximo passo.</p>
            <a href="#diagnostico" class="btn-wa inline-flex items-center justify-center gap-2 w-full px-5 py-3 uppercase tracking-[0.12em] text-xs font-bold" data-cta="artigo-lateral-{slug}">Solicitar diagnóstico</a>
            <p class="blog-aside-local">Escritórios em Curitiba e Cascavel</p>
          </div>{sumario_html}
        </aside>
      </div>

      <section id="diagnostico" class="blog-diagnostico" aria-labelledby="diag-artigo-titulo">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 id="diag-artigo-titulo" class="font-serif text-2xl sm:text-3xl text-white mb-3 text-center">Quer aplicar isso no seu negócio?</h2>
          <p class="text-white/75 mb-8 text-center">Conte o seu momento em 3 perguntas rápidas e montamos com você a estratégia certa para vender mais. Escritórios em Curitiba e Cascavel.</p>
          <div class="contact-form-card lead-card lead-card-inline">
            <form class="diag" id="form-artigo" data-diagnostico data-pagina="blog/{slug}" data-titulo-id="diag-artigo-titulo" aria-label="Solicite um diagnóstico"></form>
          </div>
        </div>
      </section>
    </div>
  </article>

  <section class="pt-12 pb-20 lg:pt-16 bg-slate-50" aria-labelledby="relacionados">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 id="relacionados" class="font-serif text-3xl text-prime-900 mb-10 text-center">Continue lendo</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
{rel_html}
      </div>
    </div>
  </section>
  </main>

  <a href="#diagnostico" class="blog-barra is-oculta" data-blog-barra data-cta="artigo-barra-{slug}">Solicitar diagnóstico gratuito <i class="fas fa-arrow-right" aria-hidden="true"></i></a>

{footer}

{scripts}  {BARRA_JS}
</body>
</html>
'''


def main():
    base = open(os.path.join(ROOT, 'blog/index.html'), encoding='utf-8').read()
    header = bloco(base, '  <!-- ========== HEADER ========== -->', '</header>')
    footer = bloco(base, '  <!-- ========== FOOTER ========== -->', '</footer>')
    scripts = bloco(base, '  <!-- ========== JS ========== -->', '</body>', incluir_fim=False)
    favicons = '\n'.join(l for l in base.split('\n') if 'rel="icon"' in l or 'apple-touch-icon' in l)

    for p in POSTS:
        if p['categoria'] not in CATEGORIAS:
            raise SystemExit(f"categoria inválida em {p['slug']}: {p['categoria']} (use uma de {CATEGORIAS})")
    ordenados = sorted(POSTS, key=lambda p: (p['data'], p['slug']), reverse=True)

    for p in POSTS:
        destino = os.path.join(ROOT, 'blog', p['slug'])
        os.makedirs(destino, exist_ok=True)
        html = pagina_post(p, ordenados, header, footer, scripts, favicons)
        open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8').write(html)

    paginas = grade_paginada(base, ordenados)
    feed_rss(ordenados)

    # sitemap: substitui as entradas do blog (artigos e páginas da listagem)
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    sm = re.sub(r'\s*<url><loc>https://conceitop\.com\.br/blog/[^<]+/</loc>.*?</url>', '', sm, flags=re.S)
    entradas = ''.join(
        f'\n  <url><loc>{DOM}/blog/{p["slug"]}/</loc><lastmod>{p.get("atualizado") or p["data"]}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>'
        f'<image:image><image:loc>{DOM}/assets/images/og/{p["slug"]}.jpg</image:loc></image:image></url>'
        for p in ordenados)
    entradas += ''.join(f'\n  <url><loc>{DOM}/blog/pagina/{n}/</loc><changefreq>weekly</changefreq><priority>0.3</priority></url>'
                        for n in range(2, paginas + 1))
    sm = sm.replace('</urlset>', entradas + '\n</urlset>')
    if 'xmlns:image' not in sm:
        sm = sm.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    print(f'✓ {len(POSTS)} artigos, {paginas} página(s) de listagem e feed RSS gerados')


if __name__ == '__main__':
    main()
