#!/usr/bin/env python3
"""Monta o carrossel de clientes da home a partir de conteudo/clientes.json.
Só entram os logos que já existem em assets/images/clientes/<slug>.webp (silhueta 2x gerada pelo tratar.py)."""
import json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = json.load(open(os.path.join(ROOT, 'conteudo/clientes.json'), encoding='utf-8'))


def itens(lista):
    out, faltando = [], []
    for slug, nome in lista:
        arq = os.path.join(ROOT, 'assets/images/clientes', slug + '.webp')
        if not os.path.exists(arq):
            faltando.append(nome)
            continue
        w, h = Image.open(arq).size
        out.append(f'<li class="carousel-item"><img src="/assets/images/clientes/{slug}.webp" alt="{nome}" width="{w // 2}" height="{h // 2}" loading="lazy" decoding="async"></li>')
    return out, faltando


def faixa(lista, reversa):
    li, faltando = itens(lista)
    if not li:
        return '', faltando
    grupo = '\n            '.join(li)
    clone = grupo.replace('<li class="carousel-item">', '<li class="carousel-item" aria-hidden="true">')
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
