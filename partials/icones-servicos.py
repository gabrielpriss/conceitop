# Ícones dos serviços da home: traço único, grade 24 x 24, pontas arredondadas (mesmo padrão em todos).
# Ficam dentro de um bloco preto da marca; o traço é branco e o detalhe de destaque é amarelo (classe "ac").
ICONES = {
    # celular com curtida: conteúdo e gestão das redes
    'redes-sociais': '''<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10.5 18.5h3"/><path class="ac" d="M12 14.2l-2.7-2.6a1.7 1.7 0 0 1 2.7-2.1 1.7 1.7 0 0 1 2.7 2.1z"/>''',
    # alvo com seta: anúncios que chegam em quem procura
    'google-meta-ads': '''<circle cx="11" cy="13" r="8.5"/><circle class="ac" cx="11" cy="13" r="4.5"/><circle class="ac" cx="11" cy="13" r=".9"/><path d="M11 13l9-9"/><path d="M16.5 4h3.5v3.5"/>''',
    # janela de navegador com código: sites e páginas
    'plataformas-web': '''<rect x="2" y="4" width="20" height="16" rx="2.2"/><path d="M2 8.5h20"/><path class="ac" d="M5 6.25h.01M7.5 6.25h.01"/><path class="ac" d="M9.5 12.5L7.5 14.5l2 2M14.5 12.5l2 2-2 2"/>''',
    # pena de caneta vetorial: criação de marca
    'branding': '''<path d="M12 2.5l6.5 8L12 21.5 5.5 10.5z"/><path class="ac" d="M12 10.5v6"/><circle class="ac" cx="12" cy="10.5" r="1.4"/><path d="M3 21.5h18"/>''',
    # quadro de apresentação com gráfico: treinamentos
    'treinamentos': '''<rect x="3" y="3" width="18" height="12.5" rx="1.8"/><path d="M12 15.5v3M8 21.5l4-3 4 3"/><path class="ac" d="M7 11.5l3-3 2.5 2L17 6.5"/>''',
    # fluxo de etapas ligadas: CRM e automações
    'automacao-vip': '''<rect x="3" y="2.5" width="8" height="5.5" rx="1.5"/><rect x="13" y="9.25" width="8" height="5.5" rx="1.5"/><rect x="3" y="16" width="8" height="5.5" rx="1.5"/><path class="ac" d="M11 5.25h4a2 2 0 0 1 2 2v2M17 14.75v2a2 2 0 0 1-2 2h-4"/>''',
}


def svg(slug):
    return ('<span class="servico-tile" aria-hidden="true"><svg class="servico-icone" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
            + ICONES[slug] + '</svg></span>')
