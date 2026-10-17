#!/usr/bin/env python3
"""Monta o carrossel de clientes da home a partir de conteudo/clientes.json.
Só entram os logos que já existem em assets/images/clientes/<slug>.webp (WebP 2x colorido gerado por scripts/tratar-logos.py)."""
import json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = json.load(open(os.path.join(ROOT, 'conteudo/clientes.json'), encoding='utf-8'))


def itens(lista):
    out, faltando = [], []
    for c in lista:
        slug, nome = c['slug'], c['nome']
        classe = 'carousel-item carousel-item--escuro' if c.get('fundo') == 'escuro' else 'carousel-item'
        arq = os.path.join(ROOT, 'assets/images/clientes', slug + '.webp')
        if not os.path.exists(arq):
            faltando.append(nome)
            continue
        w, h = Image.open(arq).size
        out.append(f'<li class="{classe}"><img src="/assets/images/clientes/{slug}.webp" alt="{nome}" width="{w // 2}" height="{h // 2}" loading="lazy" decoding="async"></li>')
    return out, faltando


def faixa(lista, reversa):
    li, faltando = itens(lista)
    if not li:
        return '', faltando
    grupo = '\n            '.join(li)
    clone = grupo  # a segunda lista já é aria-hidden; só existe para o loop sem emenda
    classe = 'carousel-track carousel-reverse' if reversa else 'carousel-track'
    return f'''      <div class="carousel-container">
        <div class="{classe}">
          <ul class="carousel-group" role="list">
            {grupo}
          </ul>
          <ul class="carousel-group" aria-hidden="true">
            {clone}
          </ul>
        </div>
      </div>''', faltando


f1, x1 = faixa(DADOS['faixa1'], False)
f2, x2 = faixa(DADOS['faixa2'], True)
bloco = f'''    <!-- CARROSSEL CLIENTES: gerado por scripts/generate-clientes.py -->
    <div class="carousel-faixas">
{f1}
{f2}
    </div>
    <!-- /CARROSSEL CLIENTES -->'''

p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()
if '<!-- CARROSSEL CLIENTES' in s:
    s = re.sub(r'    <!-- CARROSSEL CLIENTES.*?<!-- /CARROSSEL CLIENTES -->', lambda m: bloco, s, flags=re.S)
else:
    a = s.index('    <div class="carousel-container">')
    b = s.index('  </section>', a)
    s = s[:a] + bloco + '\n' + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('faltando logo:', ', '.join(x1 + x2) or 'nenhum')
