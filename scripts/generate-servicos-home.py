#!/usr/bin/env python3
"""Monta a grade "Nossos Serviços" da home (formato dos cards do site antigo, com ícones de linha).
Uso: python3 scripts/generate-servicos-home.py
Ícones em partials/icones-servicos.py. Os links levam às páginas de serviço."""
import os, re
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
    ('pesquisa-dados', 'Pesquisa', 'Pesquisa de satisfação e de percepção de marca com os clientes de vocês, para decidir com dado e não com achismo.'),
    ('papelaria-fina', 'Papelaria Fina', 'Cartões, pastas, apresentações e materiais impressos que reforçam a credibilidade da marca em cada ponto de contato.'),
    ('automacao-vip', 'Automação VIP', 'Atendimento no WhatsApp organizado, com respostas rápidas e funil visível, sem perder o toque humano.'),
]


def main():
    cards = '\n'.join(f'''        <article class="servico-card">
          <a href="/servicos/{slug}/" class="absolute inset-0 z-10" aria-label="Conheça o serviço de {titulo}"></a>
          {icones.svg(slug)}
          <h3 class="servico-titulo">{titulo}</h3>
          <p class="servico-texto">{texto}</p>
          <span class="servico-link">Saiba mais <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
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
