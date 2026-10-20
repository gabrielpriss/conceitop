#!/usr/bin/env python3
"""Monta a grade "Nossos Serviços" da home (formato dos cards do site antigo, com ícones de linha).
Uso: python3 scripts/generate-servicos-home.py
Ícones em partials/icones-servicos.py. Não há mais páginas de serviço: cada card abre um popup
(brand.js, initServicosPopup) com imagem, descrição e o que está incluso, lidos de conteudo/servicos.json,
e o botão do popup troca o conteúdo pelo formulário "Solicite um diagnóstico"."""
import html, json, os, re
from importlib import util

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


def detalhe(slug, titulo):
    d = DETALHES[slug]
    e = html.escape
    itens = ''.join(f'<li>{e(i)}</li>' for i in d['inclui'])
    return (f'<div class="servico-detalhe" hidden data-img="{e(d["img"])}" data-alt="{e(d["alt"])}">'
            f'<p class="sd-tag">{e(d["tagline"])}</p><p class="sd-intro">{e(d["intro"])}</p><ul class="sd-inclui">{itens}</ul></div>')


def main():
    cards = '\n'.join(f'''        <article class="servico-card" data-servico="{titulo}">
          <button type="button" class="servico-abrir absolute inset-0 z-10" aria-haspopup="dialog" aria-label="Ver detalhes do serviço {titulo}"></button>
          {icones.svg(slug)}
          <h3 class="servico-titulo">{titulo}</h3>
          <p class="servico-texto">{texto}</p>
          <span class="servico-link">Ver detalhes <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
          {detalhe(slug, titulo)}
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
    open(p, 'w', encoding='utf-8').write(s)
    print('Grade de serviços da home atualizada')


if __name__ == '__main__':
    main()
