#!/usr/bin/env python3
"""Gera fontes e ícones autohospedados (dev only, roda só quando mudar fonte ou ícone).

Uso:
  python3 scripts/build-assets.py --fonts DIR_GOOGLE_FONTS --fa DIR_FONTAWESOME_WEB

  DIR_GOOGLE_FONTS: checkout de github.com/google/fonts com ofl/cairo, ofl/michroma, ofl/sharetech
  DIR_FONTAWESOME_WEB: fontawesome-free-6.x-web (release do GitHub)

Saídas versionadas no repositório:
  assets/fonts/*.woff2            (subconjunto latino, font-display swap)
  assets/css/src/fonts-icons.css  (@font-face + só as classes de ícone usadas no site)
"""
import argparse, glob, os, re, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_OUT = os.path.join(ROOT, 'assets', 'fonts')
CSS_OUT = os.path.join(ROOT, 'assets', 'css', 'src', 'fonts-icons.css')

LATIN = ('U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,'
         'U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215')

SOURCES = [
    '*.html', '404.html', 'quem-somos/*.html', 'contato/*.html', 'blog/**/*.html',
    'servicos/**/*.html', 'assets/js/*.js', 'scripts/*.py', 'scripts/*.mjs', 'templates/*.html',
]


def subset_font(src, dst, unicodes, variable_limits=None):
    font = TTFont(src, lazy=False)
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['*']
    opts.name_IDs = ['*']
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes(unicodes))
    sub.subset(font)
    if variable_limits:
        font = instancer.instantiateVariableFont(font, variable_limits)
    font.flavor = 'woff2'
    font.save(dst)
    return os.path.getsize(dst)


def used_icons():
    names = set()
    for pat in SOURCES:
        for f in glob.glob(os.path.join(ROOT, pat), recursive=True):
            if os.path.basename(f) == 'build-assets.py':
                continue
            with open(f, encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
            names.update(re.findall(r'\bfa-([a-z0-9]+(?:-[a-z0-9]+)*)', txt))
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fonts', required=True)
    ap.add_argument('--fa', required=True)
    a = ap.parse_args()
    os.makedirs(FONTS_OUT, exist_ok=True)
    os.makedirs(os.path.dirname(CSS_OUT), exist_ok=True)

    sizes = {}
    sizes['cairo.woff2'] = subset_font(
        os.path.join(a.fonts, 'ofl/cairo/Cairo[slnt,wght].ttf'), os.path.join(FONTS_OUT, 'cairo.woff2'),
        LATIN, {'slnt': 0, 'wght': (300, 800)})
    sizes['share-tech.woff2'] = subset_font(
        os.path.join(a.fonts, 'ofl/sharetech/ShareTech-Regular.ttf'), os.path.join(FONTS_OUT, 'share-tech.woff2'), LATIN)
    sizes['michroma.woff2'] = subset_font(
        os.path.join(a.fonts, 'ofl/michroma/Michroma-Regular.ttf'), os.path.join(FONTS_OUT, 'michroma.woff2'), LATIN)

    # Ícones: mapeia nome -> codepoint e família a partir do CSS oficial
    css = open(os.path.join(a.fa, 'css', 'all.css'), encoding='utf-8').read()
    mapping = {}
    for sel, cp in re.findall(r'([^{}]+)\{\s*content:\s*"\\(f[0-9a-f]+)"\s*;?\s*\}', css):
        for s in sel.split(','):
            m = re.match(r'\s*\.fa-([a-z0-9-]+)::?before\s*$', s)
            if m:
                mapping[m.group(1)] = cp
    solid = TTFont(os.path.join(a.fa, 'webfonts', 'fa-solid-900.ttf')).getBestCmap()
    brands = TTFont(os.path.join(a.fa, 'webfonts', 'fa-brands-400.ttf')).getBestCmap()

    wanted = sorted(n for n in used_icons() if n in mapping)
    solid_cps, brand_cps = set(), set()
    for n in wanted:
        cp = int(mapping[n], 16)
        if cp in solid:
            solid_cps.add(cp)
        if cp in brands:
            brand_cps.add(cp)

    def cps(s):
        return ','.join('U+%04X' % c for c in sorted(s))

    if solid_cps:
        sizes['fa-solid.woff2'] = subset_font(os.path.join(a.fa, 'webfonts', 'fa-solid-900.ttf'),
                                              os.path.join(FONTS_OUT, 'fa-solid.woff2'), cps(solid_cps))
    if brand_cps:
        sizes['fa-brands.woff2'] = subset_font(os.path.join(a.fa, 'webfonts', 'fa-brands-400.ttf'),
                                               os.path.join(FONTS_OUT, 'fa-brands.woff2'), cps(brand_cps))

    out = ['/* Gerado por scripts/build-assets.py: não editar à mão */']
    for fam, file, weight in [('Cairo', 'cairo', '300 800'), ('Share Tech', 'share-tech', '400'), ('Michroma', 'michroma', '400')]:
        out.append("@font-face{font-family:'%s';src:url('/assets/fonts/%s.woff2') format('woff2');"
                   "font-weight:%s;font-style:normal;font-display:swap}" % (fam, file, weight))
    out.append("@font-face{font-family:'Font Awesome 6 Free';src:url('/assets/fonts/fa-solid.woff2') format('woff2');font-weight:900;font-style:normal;font-display:block}")
    out.append("@font-face{font-family:'Font Awesome 6 Brands';src:url('/assets/fonts/fa-brands.woff2') format('woff2');font-weight:400;font-style:normal;font-display:block}")
    out.append('.fa,.fas,.fa-solid,.fab,.fa-brands{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;'
               'display:inline-block;font-style:normal;font-variant:normal;line-height:1;text-rendering:auto}')
    out.append(".fa,.fas,.fa-solid{font-family:'Font Awesome 6 Free';font-weight:900}")
    out.append(".fab,.fa-brands{font-family:'Font Awesome 6 Brands';font-weight:400}")
    out.append('.fa-spin{animation:fa-spin 1s linear infinite}@keyframes fa-spin{to{transform:rotate(360deg)}}')
    for n in wanted:
        out.append('.fa-%s:before{content:"\\%s"}' % (n, mapping[n]))
    with open(CSS_OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')

    missing = sorted(n for n in used_icons() if n not in mapping and n not in {
        'solid', 'brands', 'spin', 'fw', 'lg', 'xs', 'sm', 'xl', '2x', '3x', 'ul', 'li', 'whatsapp-float'})
    for k, v in sizes.items():
        print(f'  {k:20s} {v/1024:6.1f} KB')
    print(f'  ícones: {len(wanted)} ({len(solid_cps)} solid, {len(brand_cps)} brands)')
    if missing:
        print('  aviso, classes fa-* sem ícone correspondente:', ', '.join(missing))


if __name__ == '__main__':
    sys.exit(main())
