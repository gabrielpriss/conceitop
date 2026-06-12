#!/usr/bin/env python3
import os, shutil, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_form_snippet import render_lead_form_block, render_lead_header
from social_links_snippet import render_footer_social

# Config padrão (ver scripts/prompt-geracao-sites.md)
BUSINESS_NAME = "Conceito Prime"
BUSINESS_LOCATION = "Curitiba, PR"
MAP_EMBED = f"https://maps.google.com/maps?q={BUSINESS_NAME.replace(' ', '+')},+{BUSINESS_LOCATION.replace(' ', '+').replace(',', '%2C')}&hl=pt-BR&z=14&output=embed"
WA_URL = "https://wa.me/554130574764?text=Ol%C3%A1!%20Gostaria%20de%20falar%20com%20um%20atendente."
WA_CTA_HEADER = f'''<a href="{WA_URL}" target="_blank" rel="noopener" class="btn-wa text-xs px-6 py-3 uppercase tracking-[0.15em]">Falar com atendente</a>'''
WA_CTA_MOBILE = f'''<a href="{WA_URL}" target="_blank" rel="noopener" class="btn-wa inline-flex justify-center text-xs px-6 py-4 mt-2 uppercase tracking-[0.2em]">Falar com atendente</a>'''

FAVICON = '''  <link rel="icon" href="/assets/images/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">'''

SERVICES = [
    {
        "slug": "redes-sociais",
        "title": "Redes Sociais",
        "icon": "fa-share-nodes",
        "icon_lib": "fas",
        "tagline": "Presença digital com curadoria e estratégia",
        "summary": "Curadoria, posicionamento e gestão de redes para conexões profundas e autênticas.",
        "intro": "Transformamos suas redes sociais em um canal estratégico de relacionamento e conversão. Criamos conteúdo com identidade visual alinhada à sua marca, planejamos calendários editoriais e monitoramos métricas para evolução contínua.",
        "includes": [
            "Diagnóstico de perfil e concorrência",
            "Calendário editorial mensal",
            "Criação de artes e copy",
            "Gestão de Instagram, Facebook e LinkedIn",
            "Relatório de métricas e insights",
        ],
        "image_src": "assets/images/portfolio/portfolio-01.webp",
        "image_alt": "Projeto de social media da Conceito Prime",
    },
    {
        "slug": "google-meta-ads",
        "title": "Google e Meta Ads",
        "icon": "fa-google",
        "icon_lib": "fab",
        "tagline": "Tráfego pago com inteligência e ROI",
        "summary": "Inteligência de tráfego pago focado na atração de público qualificado de alto valor.",
        "intro": "Campanhas de mídia paga estruturadas para atrair leads e vendas com previsibilidade. Trabalhamos com Google Ads, Meta Ads e remarketing, otimizando investimento e ampliando o alcance da sua marca junto ao público certo.",
        "includes": [
            "Auditoria de contas e estrutura de campanhas",
            "Criação e gestão de anúncios Google e Meta",
            "Configuração de conversões e pixels",
            "Relatórios semanais de performance",
            "Reuniões de alinhamento estratégico",
        ],
        "image_src": "assets/images/portfolio/portfolio-02.webp",
        "image_alt": "Campanha de mídia paga gerenciada pela Conceito Prime",
    },
    {
        "slug": "plataformas-web",
        "title": "Plataformas Web",
        "icon": "fa-laptop-code",
        "icon_lib": "fas",
        "tagline": "Sites que convertem visitantes em clientes",
        "summary": "Desenvolvimento de sites institucionais com design minimalista e altíssima conversão.",
        "intro": "Desenvolvemos sites institucionais e landing pages com foco em performance, SEO e experiência do usuário. Cada projeto é pensado para representar sua marca com elegância e gerar resultados mensuráveis.",
        "includes": [
            "Briefing e wireframe estratégico",
            "Design UI/UX responsivo",
            "Desenvolvimento HTML/CSS/JS otimizado",
            "Integração com formulários e analytics",
            "SEO técnico on-page",
        ],
        "image_src": "assets/images/portfolio/portfolio-02.webp",
        "image_alt": "Projeto de web design da Conceito Prime",
    },
    {
        "slug": "papelaria-fina",
        "title": "Papelaria Fina",
        "icon": "fa-file-invoice",
        "icon_lib": "fas",
        "tagline": "Materiais impressos com requinte e credibilidade",
        "summary": "Design de materiais impressos que transmitem credibilidade e requinte absoluto.",
        "intro": "Cartões de visita, folders, apresentações e materiais corporativos que reforçam a percepção de valor da sua marca. Cada peça é desenvolvida com atenção à tipografia, cores e acabamentos premium.",
        "includes": [
            "Cartões de visita e papel timbrado",
            "Folders e apresentações institucionais",
            "Envelopes e materiais de escritório",
            "Arquivos CMYK para impressão",
            "Acompanhamento na produção gráfica",
        ],
        "image_src": "assets/images/portfolio/portfolio-04.webp",
        "image_alt": "Projeto de papelaria corporativa da Conceito Prime",
    },
    {
        "slug": "branding",
        "title": "Branding",
        "icon": "fa-lightbulb",
        "icon_lib": "fas",
        "tagline": "Marcas memoráveis com propósito claro",
        "summary": "Construção e reposicionamento de marcas voltadas para o segmento de luxo.",
        "intro": "Criamos e reposicionamos marcas com estratégia, narrativa e identidade visual completa. Do naming à aplicação em todos os pontos de contato, garantimos que sua marca se destaque com personalidade e consistência.",
        "includes": [
            "Pesquisa de mercado e benchmarking",
            "Desenvolvimento de logotipo e variações",
            "Paleta de cores e tipografia",
            "Manual de identidade visual",
            "Aplicações em mockups e materiais",
        ],
        "image_src": "assets/images/portfolio/portfolio-06.webp",
        "image_alt": "Projeto de branding corporativo da Conceito Prime",
    },
    {
        "slug": "treinamentos",
        "title": "Treinamentos",
        "icon": "fa-chalkboard-user",
        "icon_lib": "fas",
        "tagline": "Capacitação que eleva o padrão do time",
        "summary": "Capacitação in-company focada em atendimento primoroso e excelência relacional.",
        "intro": "Programas de treinamento personalizados para equipes comerciais, de atendimento e liderança. Conteúdo prático, dinâmico e alinhado aos desafios reais do seu negócio.",
        "includes": [
            "Diagnóstico de necessidades da equipe",
            "Material didático exclusivo",
            "Workshops presenciais ou online",
            "Avaliação de desempenho pós-treinamento",
            "Suporte pós-entrega por 30 dias",
        ],
        "image_src": "assets/images/estrutura.webp",
        "image_alt": "Equipe em treinamento na Conceito Prime",
    },
    {
        "slug": "pesquisa-dados",
        "title": "Pesquisa & Dados",
        "icon": "fa-chart-line",
        "icon_lib": "fas",
        "tagline": "Decisões baseadas em evidências reais",
        "summary": "Levantamento de percepção de valor e satisfação para refinamento contínuo.",
        "intro": "Pesquisas de satisfação, NPS, percepção de marca e análise de dados para embasar decisões estratégicas. Transformamos feedback em planos de ação concretos.",
        "includes": [
            "Desenho de questionários e metodologia",
            "Coleta online ou presencial",
            "Análise estatística dos resultados",
            "Relatório executivo com insights",
            "Plano de ação recomendado",
        ],
        "image_src": "assets/images/portfolio/portfolio-03.webp",
        "image_alt": "Análise de dados e pesquisa de mercado",
    },
    {
        "slug": "automacao-vip",
        "title": "Automação VIP",
        "icon": "fa-whatsapp",
        "icon_lib": "fab",
        "tagline": "Atendimento inteligente com toque humano",
        "summary": "Arquitetura de atendimento otimizado no WhatsApp mantendo o toque humano.",
        "intro": "Fluxos automatizados no WhatsApp Business que qualificam leads, respondem dúvidas frequentes e encaminham oportunidades para sua equipe, sem perder a personalização que seu cliente espera.",
        "includes": [
            "Mapeamento de jornada do cliente",
            "Configuração do WhatsApp Business API",
            "Criação de fluxos e respostas automáticas",
            "Integração com ferramentas de gestão",
            "Treinamento da equipe de atendimento",
        ],
        "image_src": "assets/images/portfolio/portfolio-05.webp",
        "image_alt": "Automação de atendimento via WhatsApp",
    },
]


def render_form_section(title):
    form_id = f"form-{title.lower().replace(' ', '-').replace('&', '')}"
    return f'''
  <section id="orcamento" class="lead-form-section py-24" aria-labelledby="{form_id}-title">
    <div class="max-w-md mx-auto px-6 lg:px-8">
      <div class="lead-card lead-card-inline">
        {render_lead_header(title="Solicite uma proposta", servico=title, title_id=f"{form_id}-title")}
        {render_lead_form_block(hidden_servico=title, aria_label=f"Formulário de orçamento para {title}")}
      </div>
    </div>
  </section>
'''


def render_footer():
    social = render_footer_social()
    return '''
  </main>

  <footer class="site-footer bg-prime-950 pt-24 pb-12 border-t border-white/10">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="grid lg:grid-cols-12 gap-12 lg:gap-8 mb-20 items-start border-b border-white/10 pb-20">
        <div class="lg:col-span-5">
          <img src="../../assets/images/logo-footer.webp" alt="Conceito Prime - Marketing Digital" width="400" height="114" class="footer-logo mb-8">
          <p class="text-prime-400 font-light text-[15px] leading-[1.8] max-w-sm">Especialistas em posicionamento, branding e tráfego para marcas que buscam autoridade e resultados de altíssimo padrão.</p>
        </div>
        <div class="lg:col-span-3 lg:col-start-7">
          <h2 class="text-white font-serif text-lg mb-6">Menu</h2>
          <ul class="space-y-4">
            <li><a href="/" class="text-prime-400 hover:text-gold-400 transition text-[15px] font-light">Início</a></li>
            <li><a href="/quem-somos/" class="text-prime-400 hover:text-gold-400 transition text-[15px] font-light">A Agência</a></li>
            <li><a href="/blog/" class="text-prime-400 hover:text-gold-400 transition text-[15px] font-light">Journal</a></li>
            <li><a href="/contato/" class="text-prime-400 hover:text-gold-400 transition text-[15px] font-light">Contato</a></li>
          </ul>
        </div>
        <div class="lg:col-span-3">
          <h2 class="text-white font-serif text-lg mb-6">Social</h2>
''' + social + '''
        </div>
      </div>
      <div class="flex flex-col md:flex-row justify-between items-center gap-6 text-[11px] text-prime-500 uppercase tracking-widest font-light">
        <p>© 2026 Conceito Prime.</p>
        <p>Design & Code por Conceito Prime</p>
      </div>
    </div>
  </footer>
  <script>
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    menuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      const icon = menuBtn.querySelector('i');
      icon.classList.toggle('fa-bars');
      icon.classList.toggle('fa-times');
    });
    const header = document.getElementById('header');
    window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 20));
  </script>
  <script src="../../assets/js/brand.js" defer></script>
</body>
</html>'''


def render_head(svc, schema):
    s = svc
    return f'''<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{s['title']} | Conceito Prime</title>
  <link rel="canonical" href="https://conceitop.com.br/servicos/{s['slug']}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{s['title']} | Conceito Prime">
  <meta property="og:description" content="{s['summary']}">
  <meta property="og:url" content="https://conceitop.com.br/servicos/{s['slug']}/">
  <meta name="robots" content="index, follow">
  <meta name="description" content="{s['summary']}">
{FAVICON}
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&family=Share+Tech&family=Michroma&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="../../assets/css/brand.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Cairo', 'sans-serif'],
            serif: ['Tachyon', 'Share Tech', 'sans-serif'],
            display: ['Cosild', 'Michroma', 'sans-serif']
          }},
          colors: {{
            prime: {{ 50:'#fafafa', 100:'#f0f0f0', 200:'#d9d9d9', 300:'#a3a3a3', 400:'#6b6b6b', 500:'#4a4a4a', 600:'#353535', 700:'#2a2a2a', 800:'#1f1f1f', 900:'#161616', 950:'#0d0d0d' }},
            gold:  {{ 300:'#fce88a', 400:'#f7cc19', 500:'#e5b800', 600:'#c9a000' }},
            accent: {{ DEFAULT:'#ff4c01', light:'#ff7a3d', pale:'#ffd4b8' }}
          }}
        }}
      }}
    }}
  </script>
  <script type="application/ld+json">{schema}</script>
</head>
<body class="font-sans text-prime-800 antialiased">

  <header id="header" class="fixed inset-x-0 top-0 z-50 py-4">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <nav class="flex items-center justify-between gap-4" aria-label="Navegação principal">
        <a href="/" class="site-logo-link">
          <img src="../../assets/images/logo.webp" alt="Conceito Prime - Marketing Digital" width="1250" height="356" class="site-logo">
        </a>
        <div class="header-nav-right hidden md:flex">
          <div class="header-nav-links">
            <a href="/" class="nav-link text-prime-900 text-[15px] uppercase tracking-widest font-medium transition">Início</a>
            <a href="/quem-somos/" class="nav-link text-prime-900 text-[15px] uppercase tracking-widest font-medium transition">Quem somos</a>
            <a href="/blog/" class="nav-link text-prime-900 text-[15px] uppercase tracking-widest font-medium transition">Blog</a>
            <a href="/contato/" class="nav-link text-prime-900 text-[15px] uppercase tracking-widest font-medium transition">Contato</a>
          </div>
          {WA_CTA_HEADER}
        </div>
        <button id="menu-btn" type="button" aria-label="Abrir menu" aria-expanded="false" class="md:hidden text-prime-900 focus:outline-none"><i class="fas fa-bars text-xl"></i></button>
      </nav>
      <div id="mobile-menu" class="hidden md:hidden mt-4 pb-4 border-t border-gray-100 pt-4 flex flex-col gap-4 bg-white">
        <a href="/" class="text-prime-900 text-sm uppercase tracking-widest font-medium transition px-2">Início</a>
        <a href="/quem-somos/" class="text-prime-900 text-sm uppercase tracking-widest font-medium transition px-2">Quem somos</a>
        <a href="/blog/" class="text-prime-900 text-sm uppercase tracking-widest font-medium transition px-2">Blog</a>
        <a href="/contato/" class="text-prime-900 text-sm uppercase tracking-widest font-medium transition px-2">Contato</a>
        {WA_CTA_MOBILE}
      </div>
    </div>
  </header>

  <main>
  <nav aria-label="Breadcrumb" class="pt-28 pb-4 bg-prime-50">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <ol class="flex flex-wrap items-center gap-2 text-xs uppercase tracking-widest text-prime-500">
        <li><a href="/" class="hover:text-gold-500 transition">Início</a></li>
        <li aria-hidden="true">/</li>
        <li><a href="/#servicos" class="hover:text-gold-500 transition">Serviços</a></li>
        <li aria-hidden="true">/</li>
        <li class="text-prime-900 font-semibold" aria-current="page">{s['title']}</li>
      </ol>
    </div>
  </nav>

  <section class="hero-bg pt-16 pb-32">
    <div class="hero-content max-w-4xl mx-auto px-6 lg:px-8 text-center">
      <span class="inline-block border border-gold-400/30 text-gold-400 font-bold tracking-widest uppercase text-xs px-5 py-2 rounded-full mb-6">Serviço</span>
      <div class="w-20 h-20 rounded-full border border-gold-400/30 flex items-center justify-center mx-auto mb-8 text-gold-400 text-3xl" aria-hidden="true">
        <i class="{s['icon_lib']} {s['icon']}"></i>
      </div>
      <h1 class="font-serif text-4xl sm:text-5xl lg:text-6xl text-white mb-6 leading-tight uppercase">{s['title']}</h1>
      <p class="text-white/70 text-lg leading-relaxed max-w-2xl mx-auto">{s['tagline']}</p>
    </div>
  </section>
'''


def main():
    for svc in SERVICES:
        slug = svc['slug']
        dest_dir = os.path.join(ROOT, 'servicos', slug)
        assets_dir = os.path.join(dest_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)

        img_name = os.path.basename(svc['image_src'])
        shutil.copy2(os.path.join(ROOT, svc['image_src']), os.path.join(assets_dir, img_name))

        includes_html = ''.join(
            f'<li class="flex items-start gap-3"><i class="fas fa-check text-gold-400 mt-1 text-xs" aria-hidden="true"></i><span class="text-prime-600 font-light text-[15px]">{item}</span></li>'
            for item in svc['includes']
        )

        schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "Service",
            "name": svc['title'],
            "description": svc['summary'],
            "provider": {"@type": "Organization", "name": "Conceito Prime", "url": "https://conceitop.com.br"},
            "areaServed": "Curitiba, PR",
            "url": f"https://conceitop.com.br/servicos/{slug}/"
        }, ensure_ascii=False)

        body = f'''
  <section class="py-24 bg-white">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-16 items-start">
        <div>
          <div class="w-12 h-[1px] bg-gold-400 mb-8" aria-hidden="true"></div>
          <h2 class="font-serif text-3xl sm:text-4xl text-prime-900 mb-6 uppercase leading-tight">Sobre o <span class="text-gold-400">serviço</span></h2>
          <p class="text-prime-600 font-light text-[15px] leading-[1.8] mb-8">{svc['intro']}</p>
          <h3 class="font-serif text-lg text-prime-900 mb-4 uppercase">O que está incluso</h3>
          <ul class="space-y-3">{includes_html}</ul>
        </div>
        <figure class="m-0 lg:sticky lg:top-28">
          <img src="assets/{img_name}" alt="{svc['image_alt']}" width="800" height="800" class="w-full object-cover aspect-[4/3] border border-prime-100" loading="lazy" decoding="async">
        </figure>
      </div>
    </div>
  </section>
''' + render_form_section(svc['title'])

        html = render_head(svc, schema) + body + render_footer()
        with open(os.path.join(dest_dir, 'index.html'), 'w') as f:
            f.write(html)
        print(f'Created servicos/{slug}/')


if __name__ == '__main__':
    main()
