#!/usr/bin/env python3
"""Gera as capas dos depoimentos em vídeo na identidade atual da Conceito Prime.

Uso: python3 scripts/gerar-depoimentos.py <pasta-das-fontes-ttf>
  (pasta com ShareTech-Regular.ttf e Cairo[slnt,wght].ttf, as mesmas fontes do site)

Fonte das fotos e logos: conteudo/depoimentos-originais/ (capas antigas, fundo azul marinho).
De cada capa antiga aproveitamos a foto do cliente (faixa da esquerda) e o logo da empresa
(recortado do fundo e convertido para branco). O resto é desenhado aqui: fundo preto da marca
com grão, brilho amarelo, a escada de pixels do logo, nome, cargo e empresa.
Saída: assets/images/depoimentos/depoimento-<slug>-v2.webp (1600 x 857, mesma proporção de antes).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, 'conteudo/depoimentos-originais')
SAIDA = os.path.join(ROOT, 'assets/images/depoimentos')
FONTES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_fontes')

DEPOIMENTOS = [
    ('rafael', 'Rafael Kuzma', 'Diretor', 'Molas Kuzma'),
    ('philipe', 'Philippe Enke', 'CEO e Co-fundador', 'German Financial'),
    ('ruan', 'Ruan Ançay', 'Diretor', 'Nova Direção Negócios'),
    ('heloise', 'Heloise Biscaia', 'Diretora', 'Grupo Nuele'),
]

W, H = 1600, 857
PRETO = (22, 22, 22)
AMARELO = (247, 204, 25)
FOTO_W = 610          # largura da faixa da foto
X_TEXTO = 690         # início do bloco de texto
DEGRAU = [(0, [.22, .38, .58, .8, 1]), (1, [.22, .42, .66, .9]), (2, [.26, .5, .78]), (3, [.32, .64])]


def fonte(nome, tam, peso=None):
    f = ImageFont.truetype(os.path.join(FONTES, nome), tam)
    if peso is not None:
        try:
            f.set_variation_by_axes([peso, 0])  # Cairo variável: eixos [peso, inclinação]
        except Exception:
            pass
    return f


def escada(lado, opac=1.0):
    """Escada de pixels do logo: 5 x 4 quadrados que ganham opacidade da esquerda para a direita."""
    q = lado // 5
    im = Image.new('RGBA', (q * 5, q * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for r, ops in DEGRAU:
        ini = 5 - len(ops)
        for i, o in enumerate(ops):
            x = (ini + i) * q
            d.rectangle([x, r * q, x + q - 1, r * q + q - 1], fill=AMARELO + (int(255 * o * opac),))
    return im


def fundo():
    rng = np.random.default_rng(7)
    base = np.zeros((H, W, 3), np.float32) + np.array(PRETO, np.float32)
    # brilho amarelo no canto de cima à direita e um mais fraco embaixo
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for cx, cy, raio, forca in [(W * .95, 0, W * .42, .16), (W * .55, H * 1.05, W * .35, .06)]:
        g = np.clip(1 - np.hypot(xx - cx, yy - cy) / raio, 0, 1) ** 2 * forca
        base += g[..., None] * (np.array(AMARELO, np.float32) - base)
    # grão fino
    base += rng.normal(0, 4.5, (H, W, 1)).astype(np.float32)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB')


def extrair(arq):
    im = Image.open(arq).convert('RGB')
    w, h = im.size
    foto = im.crop((0, 0, 427, h))
    a = np.array(im).astype(np.int16)
    bg = a[h // 2, w - 20]
    # logo: faixa de baixo do painel azul, depois da linha amarela
    y0 = int(h * .64)
    reg = a[y0:h - 8, 432:w - 8]
    lum = reg.mean(2) - bg.mean()
    amarelo = (reg[..., 0] > 150) & (reg[..., 2] < 120)  # tira a linha amarela, se pegar
    alfa = np.clip((lum - 8) * 2.4, 0, 255)  # o -8 corta o ruído da compressão em volta do logo
    alfa[amarelo] = 0
    alfa = alfa.astype(np.uint8)
    logo = Image.new('RGBA', (reg.shape[1], reg.shape[0]), (255, 255, 255, 0))
    logo.putalpha(Image.fromarray(alfa))
    bbox = Image.fromarray((alfa > 40).astype(np.uint8) * 255).getbbox()
    return foto, logo.crop(bbox) if bbox else None


def capa(slug, nome, cargo, empresa):
    foto, logo = extrair(os.path.join(ORIG, f'depoimento-{slug}.webp'))
    img = fundo().convert('RGBA')

    # foto: preenche a faixa da esquerda e some em degradê para o preto
    escala = max(FOTO_W / foto.width, H / foto.height)
    f = foto.resize((round(foto.width * escala), round(foto.height * escala)), Image.LANCZOS)
    f = f.crop(((f.width - FOTO_W) // 2, 0, (f.width - FOTO_W) // 2 + FOTO_W, H)).convert('RGBA')
    mask = Image.new('L', (FOTO_W, H), 255)
    md = ImageDraw.Draw(mask)
    for i in range(160):
        md.line([(FOTO_W - 160 + i, 0), (FOTO_W - 160 + i, H)], fill=int(255 * (1 - i / 160) ** 1.4))
    img.paste(f, (0, 0), mask)
    # fio amarelo fino na base da foto (marca a faixa sem pesar)
    ImageDraw.Draw(img).rectangle([0, H - 8, FOTO_W - 160, H], fill=AMARELO + (255,))

    # escada de pixels no canto de cima à direita
    e = escada(170)
    img.alpha_composite(e, (W - e.width - 56, 56))

    d = ImageDraw.Draw(img)
    f_eye = fonte('ShareTech-Regular.ttf', 30)
    f_nome = fonte('ShareTech-Regular.ttf', 92)
    f_cargo = fonte('Cairo[slnt,wght].ttf', 36, 600)
    f_emp = fonte('Cairo[slnt,wght].ttf', 40, 800)

    y = 150
    eyebrow = 'CLIENTE PRIME'
    x = X_TEXTO
    for ch in eyebrow:  # espaçamento entre letras, como no site
        d.text((x, y), ch, font=f_eye, fill=AMARELO)
        x += d.textlength(ch, font=f_eye) + 7
    y += 62
    nome_up = nome.upper()
    tam = 92
    while d.textlength(nome_up, font=f_nome) > W - X_TEXTO - 70 and tam > 60:
        tam -= 4
        f_nome = fonte('ShareTech-Regular.ttf', tam)
    d.text((X_TEXTO, y), nome_up, font=f_nome, fill=(255, 255, 255))
    y += tam + 34
    d.text((X_TEXTO, y), cargo, font=f_cargo, fill=(255, 255, 255, 190))
    y += 50
    d.text((X_TEXTO, y), empresa, font=f_emp, fill=AMARELO)
    y += 86
    d.rectangle([X_TEXTO, y, X_TEXTO + 110, y + 4], fill=AMARELO)

    if logo is not None:
        caixa_w, caixa_h = 420, 130
        s = min(caixa_w / logo.width, caixa_h / logo.height)
        lg = logo.resize((max(1, round(logo.width * s)), max(1, round(logo.height * s))), Image.LANCZOS)
        img.alpha_composite(lg, (X_TEXTO, H - 90 - lg.height))

    destino = os.path.join(SAIDA, f'depoimento-{slug}-v2.webp')
    img.convert('RGB').save(destino, 'WEBP', quality=84, method=6)
    print(destino, os.path.getsize(destino) // 1024, 'KB')


if __name__ == '__main__':
    for dep in DEPOIMENTOS:
        capa(*dep)
