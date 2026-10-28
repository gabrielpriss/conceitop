#!/usr/bin/env python3
"""Trata os logos dos clientes mantendo as cores reais.

Uso: python3 scripts/tratar-logos.py <pasta-com-os-originais>

Para cada logo: recorta a área útil (fundo transparente ou fundo sólido),
normaliza o peso visual pela área (logos largos e logos quadrados ficam com
presença parecida) e exporta WebP 2x em assets/images/clientes/<slug>.webp.
Logos que a empresa só publica em branco recebem as cores oficiais da marca
pelo campo "cores" em conteudo/clientes.json (ver colorir()), para todos os
cartões ficarem claros. "fundo": "escuro" continua disponível, mas não é usado.
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


def _hex(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def colorir(im, spec):
    """Pinta as partes brancas de um logo com as cores oficiais da marca.

    Usado quando a empresa só publica o logo em branco (para fundo escuro) e
    as cores oficiais vêm do site dela. Pixels já coloridos (dourado, azul,
    degradê) ficam como estão; só o branco neutro é trocado.
    spec: {"base": "#hex",
           "regioes": [{"caixa": [x0, y0, x1, y1], "cor": "#hex"}],   (frações da área recortada)
           "componentes": {"caixa": [...], "cores": ["#hex", ...], "ordem": "x" | "raio" | "area"}}
    """
    import numpy as np
    from scipy import ndimage
    a = np.array(im.convert('RGBA')).astype(np.int16)
    h, w = a.shape[:2]
    rgb, alfa = a[..., :3], a[..., 3]
    branco = (rgb.min(axis=2) > 150) & ((rgb.max(axis=2) - rgb.min(axis=2)) < 40) & (alfa > 0)
    alvo = np.zeros((h, w, 3), np.int16)
    pintar = np.zeros((h, w), bool)

    def mascara(caixa):
        x0, y0, x1, y1 = caixa
        m = np.zeros((h, w), bool)
        m[int(y0 * h):int(round(y1 * h)), int(x0 * w):int(round(x1 * w))] = True
        return m

    if spec.get('base'):
        alvo[:] = _hex(spec['base'])
        pintar |= branco
    for r in spec.get('regioes', []):
        m = mascara(r['caixa']) & branco
        alvo[m] = _hex(r['cor'])
        pintar |= m
    comp = spec.get('componentes')
    if comp:
        area = mascara(comp.get('caixa', [0, 0, 1, 1]))
        rotulos, n = ndimage.label((alfa > 100) & area)
        centros = ndimage.center_of_mass(np.ones((h, w)), rotulos, range(1, n + 1))
        tamanhos = ndimage.sum(np.ones((h, w)), rotulos, range(1, n + 1))
        ids = [i + 1 for i in range(n) if tamanhos[i] > 0.002 * area.sum()]
        if comp.get('ordem') == 'raio':
            ys, xs = np.nonzero(area & (alfa > 100))
            cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
            ids.sort(key=lambda i: -((centros[i - 1][0] - cy) ** 2 + (centros[i - 1][1] - cx) ** 2))
        elif comp.get('ordem') == 'area':
            ids.sort(key=lambda i: -tamanhos[i - 1])
        else:
            ids.sort(key=lambda i: centros[i - 1][1])
        cores = comp['cores']
        # a borda suavizada (alfa baixo) fica fora dos rótulos: expande cada componente 2 px
        for k, i in enumerate(ids):
            m = ndimage.binary_dilation(rotulos == i, iterations=2) & branco & area
            alvo[m] = _hex(cores[min(k, len(cores) - 1)])
            pintar |= m
    rgb[pintar] = alvo[pintar]
    a[..., :3] = rgb
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def tratar(slug, origem, cores=None):
    im = recortar(Image.open(origem))
    if im is None:
        raise ValueError('imagem vazia')
    if cores:
        im = colorir(im, cores)
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
    for faixa in ('faixa1', 'faixa2', 'faixa3'):
        for c in dados[faixa]:
            origem = c.get('origem')
            caminho = os.path.join(ORIG, origem) if origem and not origem.startswith('assets/') else os.path.join(ROOT, origem or '')
            if not origem or not os.path.exists(caminho):
                faltando.append(c['nome'])
                continue
            w, h, kb = tratar(c['slug'], caminho, c.get('cores'))
            print(f"{c['slug']:<24} {w}x{h} css  {kb // 1024} KB  fundo {c.get('fundo', 'claro')}")
    print('sem arquivo de origem:', ', '.join(faltando) or 'nenhum')


if __name__ == '__main__':
    main()
