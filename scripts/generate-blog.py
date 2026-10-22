#!/usr/bin/env python3
"""Gera as páginas dos artigos (/blog/<slug>/) e a listagem do blog a partir de conteudo/blog/.

Uso: python3 scripts/generate-blog.py
Entradas:
  conteudo/blog/posts.json       metadados (título, data, categoria, descrição)
  conteudo/blog/<slug>.raw.html  texto original do artigo, extraído do WordPress antigo
Saídas:
  blog/<slug>/index.html, blog/index.html (grade de artigos), sitemap.xml (seção do blog)
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
            <img src="/blog/assets/capas/{p['slug']}-600.webp" srcset="/blog/assets/capas/{p['slug']}-600.webp 600w, /blog/assets/capas/{p['slug']}.webp 1200w" sizes="(min-width: 1024px) 400px, (min-width: 640px) 50vw, 100vw" alt="" width="600" height="315" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" {'' if eager else 'loading="lazy" '}decoding="async">
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


def main():
    base = open(os.path.join(ROOT, 'blog/index.html'), encoding='utf-8').read()
    header = bloco(base, '  <!-- ========== HEADER ========== -->', '</header>')
    footer = bloco(base, '  <!-- ========== FOOTER ========== -->', '</footer>')
    scripts = bloco(base, '  <!-- ========== JS ========== -->', '</body>', incluir_fim=False)
    favicons = '\n'.join(l for l in base.split('\n') if 'rel="icon"' in l or 'apple-touch-icon' in l)

    ordenados = sorted(POSTS, key=lambda p: p['data'], reverse=True)

    for p in POSTS:
        raw = open(os.path.join(ROOT, f"conteudo/blog/{p['slug']}.raw.html"), encoding='utf-8').read()
        lead, corpo = limpar(raw, p['slug'])
        palavras = len(re.sub(r'<[^>]+>', ' ', corpo).split())
        minutos = max(1, math.ceil(palavras / 200))
        url = f"{DOM}/blog/{p['slug']}/"
        relacionados = [x for x in ordenados if x['categoria'] == p['categoria'] and x['slug'] != p['slug']][:3]
        if len(relacionados) < 3:
            relacionados += [x for x in ordenados if x['slug'] != p['slug'] and x not in relacionados][:3 - len(relacionados)]
        ld = {
            '@context': 'https://schema.org',
            '@graph': [
                {
                    '@type': 'BlogPosting',
                    'headline': p['titulo'],
                    'description': p['descricao'],
                    'datePublished': p['data'],
                    'inLanguage': 'pt-BR',
                    'image': f"{DOM}/assets/images/og/{p['slug']}.jpg",
                    'mainEntityOfPage': url,
                    'wordCount': palavras,
                    'articleSection': p['categoria'],
                    'author': {'@type': 'Organization', 'name': 'Conceito Prime', 'url': DOM},
                    'publisher': {'@type': 'Organization', 'name': 'Conceito Prime', 'logo': {'@type': 'ImageObject', 'url': f'{DOM}/assets/images/logo.webp'}},
                },
                {
                    '@type': 'BreadcrumbList',
                    'itemListElement': [
                        {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': f'{DOM}/'},
                        {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': f'{DOM}/blog/'},
                        {'@type': 'ListItem', 'position': 3, 'name': p['titulo'], 'item': url},
                    ],
                },
            ],
        }
        titulo_pag = f"{p['titulo']} | Conceito Prime"
        lead_html = f'<p class="text-white/75 text-lg sm:text-xl leading-relaxed max-w-3xl mx-auto mb-8">{lead}</p>' if lead else ''
        rel_html = '\n'.join(card(x, h='h3') for x in relacionados)
        pagina = f'''<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{H.escape(titulo_pag)}</title>
  <meta name="description" content="{H.escape(p['descricao'])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Conceito Prime">
  <meta property="og:title" content="{H.escape(p['titulo'])}">
  <meta property="og:description" content="{H.escape(p['descricao'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOM}/assets/images/og/{p['slug']}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{H.escape(p['titulo'])}">
  <meta property="article:published_time" content="{p['data']}">
  <meta property="article:section" content="{p['categoria']}">
  <meta name="twitter:card" content="summary_large_image">
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
        <p class="text-white/70 text-sm"><time datetime="{p['data']}">{data_extenso(p['data'])}</time> <span aria-hidden="true">·</span> {minutos} min de leitura</p>
      </div>
    </header>

    <div class="bg-white">
      <figure class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-2 pt-12">
        <img src="/blog/assets/capas/{p['slug']}.webp" srcset="/blog/assets/capas/{p['slug']}-600.webp 600w, /blog/assets/capas/{p['slug']}.webp 1200w" sizes="(min-width: 960px) 896px, 100vw" alt="" width="1200" height="630" class="w-full h-auto rounded-2xl" decoding="async">
      </figure>

      <div class="post-content max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
{corpo}
      </div>

      <aside class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 lg:pb-16" aria-labelledby="cta-artigo">
        <div class="bg-prime-950 text-white p-8 sm:p-10 rounded-2xl">
          <h2 id="cta-artigo" class="font-serif text-2xl sm:text-3xl mb-3">Quer aplicar isso no seu negócio?</h2>
          <p class="text-white/75 mb-6">Conte o seu momento e montamos com você a estratégia de marketing digital certa para vender mais.</p>
          <a href="/contato/" class="btn-wa inline-flex items-center gap-2 px-8 py-4 uppercase tracking-[0.15em] text-xs font-bold" data-cta="artigo-{p['slug']}"><i class="fab fa-whatsapp" aria-hidden="true"></i> Solicitar orçamento</a>
        </div>
      </aside>
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

{footer}

{scripts}</body>
</html>
'''
        destino = os.path.join(ROOT, 'blog', p['slug'])
        os.makedirs(destino, exist_ok=True)
        open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8').write(pagina)

    # listagem
    grade = '\n\n'.join(card(p, eager=i < 3) for i, p in enumerate(ordenados))
    novo = f'''  <!-- ========== BLOG POSTS ========== -->
  <section class="py-20 bg-slate-50" aria-label="Artigos">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8" id="posts-grid">

{grade}

      </div>
      <p class="text-center text-gray-600 mt-10 hidden" data-sem-resultado>Nenhum artigo nesta categoria.</p>

    </div>
  </section>

'''
    a = base.index('  <!-- ========== BLOG POSTS ========== -->')
    b = base.index('  <!-- ========== NEWSLETTER BANNER ========== -->')
    base = base[:a] + novo + base[b:]
    open(os.path.join(ROOT, 'blog/index.html'), 'w', encoding='utf-8').write(base)

    # sitemap: substitui as entradas de artigos
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    sm = re.sub(r'\s*<url><loc>https://conceitop\.com\.br/blog/[^<]+/</loc>.*?</url>', '', sm, flags=re.S)
    entradas = ''.join(
        f'\n  <url><loc>{DOM}/blog/{p["slug"]}/</loc><lastmod>{p["data"]}</lastmod><changefreq>yearly</changefreq><priority>0.6</priority>'
        f'<image:image><image:loc>{DOM}/assets/images/og/{p["slug"]}.jpg</image:loc></image:image></url>'
        for p in ordenados)
    sm = sm.replace('</urlset>', entradas + '\n</urlset>')
    if 'xmlns:image' not in sm:
        sm = sm.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    print(f'✓ {len(POSTS)} artigos e listagem gerados')


if __name__ == '__main__':
    main()
