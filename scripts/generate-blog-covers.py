#!/usr/bin/env python3
"""Gera as capas dos artigos do blog na identidade da Conceito Prime (dev only).

Uso: python3 scripts/generate-blog-covers.py [--fonts DIR] [--todas]
  Por padrão usa as fontes de scripts/fontes/ e só gera a capa dos artigos que ainda não têm capa.
Saídas:
  blog/assets/capas/<slug>.webp      1200x630 (página do artigo)
  blog/assets/capas/<slug>-600.webp  600x315  (cards da listagem)
  assets/images/og/<slug>.jpg        1200x630 (compartilhamento em redes sociais)
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
ESCURO = (22, 22, 22)
AMARELO = (247, 204, 25)
BRANCO = (255, 255, 255)


def fonte_cairo(fonts, tamanho, peso):
    f = ImageFont.truetype(os.path.join(fonts, 'ofl/cairo/Cairo[slnt,wght].ttf'), tamanho)
    eixos = [a['name'] for a in f.get_variation_axes()]
    f.set_variation_by_axes([peso if n in (b'Weight', 'Weight') else 0 for n in eixos])
    return f


def quebrar(draw, texto, fonte, largura):
    linhas, atual = [], ''
    for palavra in texto.split():
        teste = (atual + ' ' + palavra).strip()
        if draw.textlength(teste, font=fonte) <= largura:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return linhas


def capa(post, fonts, logo):
    im = Image.new('RGB', (W, H), ESCURO)
    d = ImageDraw.Draw(im, 'RGBA')

    # textura: grade de pixels da marca, bem sutil, no canto direito
    for i in range(14):
        for j in range(9):
            if (i * 7 + j * 3) % 5 in (0, 2):
                a = max(0, 34 - i * 2)
                x, y = W - 40 - i * 34, 40 + j * 34
                d.rectangle([x, y, x + 22, y + 22], fill=(247, 204, 25, a))
    # brilho amarelo difuso
    halo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(halo).ellipse([760, -260, 1500, 420], fill=60)
    halo = halo.filter(ImageFilter.GaussianBlur(120))
    im.paste(Image.new('RGB', (W, H), AMARELO), (0, 0), halo.point(lambda v: int(v * 0.35)))

    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 0, 14, H], fill=AMARELO)

    cat = ImageFont.truetype(os.path.join(fonts, 'ofl/sharetech/ShareTech-Regular.ttf'), 30)
    d.text((90, 92), post['categoria'].upper(), font=cat, fill=AMARELO)
    d.rectangle([90, 140, 150, 143], fill=AMARELO)

    tamanho = 66
    while True:
        f = fonte_cairo(fonts, tamanho, 800)
        linhas = quebrar(d, post['titulo'], f, 900)
        if len(linhas) * tamanho * 1.18 <= 290 or tamanho <= 40:
            break
        tamanho -= 4
    y = 180
    for ln in linhas:
        d.text((88, y), ln, font=f, fill=BRANCO)
        y += int(tamanho * 1.18)

    lw = 230
    lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.paste(lg, (90, H - 70 - lg.height), lg)
    d.text((W - 90, H - 82), post.get('rodape', 'conceitop.com.br/blog'), font=cat, fill=(255, 255, 255, 150), anchor='rs')
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fonts', default=os.path.join(ROOT, 'scripts', 'fontes'))
    ap.add_argument('--todas', action='store_true', help='refaz todas as capas e a og-image.jpg')
    a = ap.parse_args()
    posts = json.load(open(os.path.join(ROOT, 'conteudo/blog/posts.json'), encoding='utf-8'))
    logo = Image.open(os.path.join(ROOT, 'assets/images/logo-footer.webp')).convert('RGBA')
    dir_capas = os.path.join(ROOT, 'blog/assets/capas')
    dir_og = os.path.join(ROOT, 'assets/images/og')
    os.makedirs(dir_capas, exist_ok=True)
    os.makedirs(dir_og, exist_ok=True)
    feitas = 0
    for p in posts:
        if not a.todas and os.path.exists(os.path.join(dir_capas, p['slug'] + '.webp')):
            continue
        feitas += 1
        im = capa(p, a.fonts, logo)
        im.save(os.path.join(dir_capas, p['slug'] + '.webp'), 'WEBP', quality=82, method=6)
        im.resize((600, 315), Image.LANCZOS).save(os.path.join(dir_capas, p['slug'] + '-600.webp'), 'WEBP', quality=80, method=6)
        im.save(os.path.join(dir_og, p['slug'] + '.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
    if not a.todas:
        print(f'✓ {feitas} capa(s) nova(s)')
        return
    # imagem padrão de compartilhamento do site
    geral = capa({'titulo': 'Estratégia ideal para impulsionar seu resultado', 'categoria': 'Marketing digital em Curitiba', 'rodape': 'conceitop.com.br'}, a.fonts, logo)
    geral.save(os.path.join(ROOT, 'assets/images/og-image.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
    print(f'✓ {len(posts)} capas geradas + og-image.jpg')


if __name__ == '__main__':
    main()
