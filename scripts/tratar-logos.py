#!/usr/bin/env python3
"""Trata os logos dos clientes mantendo as cores reais.

Uso: python3 scripts/tratar-logos.py <pasta-com-os-originais>

Para cada logo: recorta a área útil (fundo transparente ou fundo sólido),
normaliza o peso visual pela área (logos largos e logos quadrados ficam com
presença parecida) e exporta WebP 2x em assets/images/clientes/<slug>.webp.
Logos brancos vão para o cartão escuro (campo "fundo": "escuro" em conteudo/clientes.json).
"""
import json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_logos-originais')
SAIDA = os.path.join(ROOT, 'assets/images/clientes')

# Área útil do logo dentro do cartão (px CSS). O cartão tem 184x88.
CAIXA_W, CAIXA_H = 148, 56
AREA_ALVO = CAIXA_W * CAIXA_H * 0.5
ESCALA = 2  # exporta em 2x para telas retina


def recortar(im):
    """Devolve o logo em RGBA, sem margem, com o fundo removido."""
    im = im.convert('RGBA')
    a = im.getchannel('A')
    transparente = sum(a.histogram()[:250]) / (im.width * im.height)
    if transparente < 0.05:
        # Fundo sólido: usa a cor dos cantos como chave e gera alfa pela distância
        rgb = im.convert('RGB')
        cantos = [rgb.getpixel(p) for p in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]]
        fundo = max(set(cantos), key=cantos.count)
        px = rgb.load()
        alfa = Image.new('L', im.size)
        ap = alfa.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b = px[x, y]
                d = max(abs(r - fundo[0]), abs(g - fundo[1]), abs(b - fundo[2]))
                ap[x, y] = 0 if d < 18 else (255 if d > 60 else int((d - 18) / 42 * 255))
        im.putalpha(alfa)
        a = alfa
    caixa = a.point(lambda v: 255 if v > 100 else 0).getbbox()
    return im.crop(caixa) if caixa else None


def tratar(slug, origem):
    im = recortar(Image.open(origem))
    if im is None:
        raise ValueError('imagem vazia')
    w, h = im.size
    s = (AREA_ALVO / (w * h)) ** 0.5
    s = min(s, CAIXA_W / w, CAIXA_H / h)
    css_w, css_h = max(1, round(w * s)), max(1, round(h * s))
    final = im.resize((css_w * ESCALA, css_h * ESCALA), Image.LANCZOS)
    destino = os.path.join(SAIDA, slug + '.webp')
    final.save(destino, 'WEBP', quality=90, method=6)
    return css_w, css_h, os.path.getsize(destino)


def main():
    dados = json.load(open(os.path.join(ROOT, 'conteudo/clientes.json'), encoding='utf-8'))
    os.makedirs(SAIDA, exist_ok=True)
    faltando = []
    for faixa in ('faixa1', 'faixa2'):
        for c in dados[faixa]:
            origem = c.get('origem')
            caminho = os.path.join(ORIG, origem) if origem and not origem.startswith('assets/') else os.path.join(ROOT, origem or '')
            if not origem or not os.path.exists(caminho):
                faltando.append(c['nome'])
                continue
            w, h, kb = tratar(c['slug'], caminho)
            print(f"{c['slug']:<24} {w}x{h} css  {kb // 1024} KB  fundo {c.get('fundo', 'claro')}")
    print('sem arquivo de origem:', ', '.join(faltando) or 'nenhum')


if __name__ == '__main__':
    main()
