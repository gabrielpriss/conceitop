#!/usr/bin/env python3
"""Monta a grade "Nossos Serviços" da home (formato dos cards do site antigo, com ícones de linha).
Uso: python3 scripts/generate-servicos-home.py
Ícones em partials/icones-servicos.py. Os cards de serviço são só informativos (sem clique).
Também monta o Portfólio da home (conteudo/portfolio.json): cada projeto abre um popup (brand.js,
initServicosPopup) com a imagem, a legenda e o detalhe do serviço ligado a ele (conteudo/servicos.json),
e o botão do popup troca o conteúdo pelo formulário "Solicite um diagnóstico"."""
import html, json, os, re
from importlib import util

# Negrito nos diferenciais: mesma função das LPs (scripts/generate-segmentos.py)
_spec = util.spec_from_file_location('segmentos', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generate-segmentos.py'))
_seg = util.module_from_spec(_spec)
_spec.loader.exec_module(_seg)
negritar = _seg.negritar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = util.spec_from_file_location('icones', os.path.join(ROOT, 'partials/icones-servicos.py'))
icones = util.module_from_spec(_spec); _spec.loader.exec_module(icones)

SERVICOS = [
    ('redes-sociais', 'Redes Sociais', 'Planejamento, conteúdo e gestão das redes, com calendário mensal e artes alinhadas à marca para gerar autoridade e demanda.'),
    ('google-meta-ads', 'Google e Meta Ads', 'Anúncios no Google para quem já procura e no Instagram e Facebook para quem ainda não conhece, medidos por contato qualificado e venda.'),
    ('plataformas-web', 'Sites', 'Sites institucionais, lojas e páginas de captação rápidos, com SEO e formulário que transforma visita em pedido de orçamento.'),
    ('branding', 'Branding', 'Planejamento e criação de marca: identidade visual e posicionamento para a empresa ser percebida pelo valor que entrega.'),
    ('treinamentos', 'Treinamentos para clientes', 'Treinamentos e curso de vendas feitos para os nossos clientes, para o time de atendimento e comercial aproveitar cada contato.'),
    ('automacao-vip', 'CRM e Automações', 'CRM com cada lead registrado do primeiro contato ao fechamento e automações no WhatsApp que respondem na hora e lembram o vendedor do próximo passo.'),
]


DETALHES = json.load(open(os.path.join(ROOT, 'conteudo/servicos.json'), encoding='utf-8'))


PORTFOLIO = json.load(open(os.path.join(ROOT, 'conteudo/portfolio.json'), encoding='utf-8'))


def detalhe(chave):
    d = DETALHES[chave]
    e = html.escape
    itens = ''.join(f'<li>{e(i)}</li>' for i in d['inclui'])
    return (f'<div class="servico-detalhe" hidden>'
            f'<p class="sd-tag">{e(d["tagline"])}</p><p class="sd-intro">{negritar(e(d["intro"]))}</p><ul class="sd-inclui">{itens}</ul></div>')


def portfolio():
    e = html.escape
    itens = '\n'.join(f'''        <figure class="port-item group" data-popup-servico data-servico="{e(p['servico'])}" data-titulo="{e(p['titulo'])}" data-eyebrow="{e(p['cat'])}" data-img="/assets/images/portfolio/{p['img']}.webp" data-alt="{e(p['alt'])}">
          <img src="/assets/images/portfolio/{p['img']}.webp" alt="{e(p['alt'])}" width="800" height="800" loading="lazy" decoding="async">
          <figcaption class="port-legenda">
            <span class="port-cat">{e(p['cat'])}</span>
            <h3 class="port-titulo">{e(p['titulo'])}</h3>
            <p class="port-desc">{e(p['desc'])}</p>
            <span class="port-ver">Ver projeto <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
          </figcaption>
          <button type="button" class="servico-abrir port-abrir" aria-haspopup="dialog" aria-label="Ver o projeto {e(p['titulo'])}"></button>
          {detalhe(p['detalhe'])}
        </figure>''' for p in PORTFOLIO)
    return f'''      <!-- PORTFOLIO HOME: gerado por scripts/generate-servicos-home.py -->
      <div class="port-grade">
{itens}
      </div>
      <!-- /PORTFOLIO HOME -->'''


def main():
    cards = '\n'.join(f'''        <article class="servico-card">
          {icones.svg(slug)}
          <h3 class="servico-titulo">{titulo}</h3>
          <p class="servico-texto">{texto}</p>
        </article>''' for slug, titulo, texto in SERVICOS)
    bloco = f'''      <!-- SERVICOS HOME: gerado por scripts/generate-servicos-home.py -->
      <div class="servicos-grade">
{cards}
      </div>
      <!-- /SERVICOS HOME -->'''
    p = os.path.join(ROOT, 'index.html')
    s = open(p, encoding='utf-8').read()
    if '<!-- SERVICOS HOME' in s:
        s = re.sub(r'      <!-- SERVICOS HOME.*?<!-- /SERVICOS HOME -->', lambda m: bloco, s, flags=re.S)
    else:
        sec = s.index('<section id="servicos"')
        a = s.index('      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">', sec)
        b = s.index('  </section>', a)
        b = s.rindex('    </div>\n', a, b)  # fecha o container max-w-7xl
        s = s[:a] + bloco + '\n' + s[b:]
    port = portfolio()
    if '<!-- PORTFOLIO HOME' in s:
        s = re.sub(r'      <!-- PORTFOLIO HOME.*?<!-- /PORTFOLIO HOME -->', lambda m: port, s, flags=re.S)
    else:
        a = s.index('      <div class="port-grade">')
        b = s.index('      <div class="text-center mt-16">', a)
        s = s[:a] + port + '\n\n' + s[b:]
    open(p, 'w', encoding='utf-8').write(s)
    print('Grade de serviços e portfólio da home atualizados')


if __name__ == '__main__':
    main()
