#!/usr/bin/env python3
"""Aplica o cabeçalho único (partials/header.html) em todas as páginas do site.

Uso: python3 scripts/sync-header.py         # reescreve as páginas
     python3 scripts/sync-header.py --check # só confere (o QA usa este modo)
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER = open(os.path.join(ROOT, 'partials/header.html'), encoding='utf-8').read().strip()
PASTAS = ['index.html', 'quem-somos', 'contato', 'trabalhe-conosco', 'blog', 'servicos', 'industrial', 'b2b']
PADRAO = re.compile(r'<header id="header".*?</header>', re.S)


def paginas():
    for item in PASTAS:
        caminho = os.path.join(ROOT, item)
        if os.path.isfile(caminho):
            yield caminho
        for raiz, _, arquivos in os.walk(caminho):
            for a in arquivos:
                if a.endswith('.html'):
                    yield os.path.join(raiz, a)


def main():
    conferir = '--check' in sys.argv
    diferentes, sem_header = [], []
    for p in paginas():
        s = open(p, encoding='utf-8').read()
        if not PADRAO.search(s):
            sem_header.append(os.path.relpath(p, ROOT))
            continue
        novo = PADRAO.sub(lambda m: HEADER, s, count=1)
        if novo != s:
            diferentes.append(os.path.relpath(p, ROOT))
            if not conferir:
                open(p, 'w', encoding='utf-8').write(novo)
    acao = 'diferentes do parcial' if conferir else 'atualizadas'
    print(f'{len(diferentes)} páginas {acao}' + (': ' + ', '.join(diferentes) if diferentes else ''))
    if sem_header:
        print('sem cabeçalho:', ', '.join(sem_header))
    if conferir and diferentes:
        sys.exit(1)


if __name__ == '__main__':
    main()
