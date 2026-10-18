# Ícones de linha dos serviços (inspirados nos do site antigo), viewBox 64x64.
# Traço na cor do texto e detalhe em amarelo (classe "ac").
ICONES = {
'redes-sociais': '''<path d="M8 30v-8l22-9v34L8 38z"/><path d="M12 38l3 12h6l-2-11"/><path d="M34 22c3 2 3 14 0 16"/><circle class="ac" cx="47" cy="12" r="6"/><path class="ac" d="M45.5 9.5v5l4-2.5z"/><rect x="41" y="25" width="13" height="13" rx="3.5"/><circle cx="47.5" cy="31.5" r="3"/><path class="ac" d="M42 46h14v8h-8l-4 3v-3h-2z"/>''',
'google-meta-ads': '''<rect x="-5" y="-19" width="10" height="38" rx="5" transform="translate(21 29) rotate(-28)"/><circle class="ac" cx="9.5" cy="44" r="6"/><path d="M13 40l9-17"/><path class="ac" d="M36 36c0-5 2.5-9 5.5-9 4 0 6 5 8 8s4 8 7 8c2 0 3.5-2.5 3.5-5.5S58.5 30 56 30c-3.5 0-5.5 4.5-7 7.5S45 44 41.5 44C38.5 44 36 41 36 36z"/>''',
'plataformas-web': '''<rect x="7" y="11" width="50" height="34" rx="3"/><path d="M32 45v8M22 53h20"/><path class="ac" d="M13 18h38"/><rect x="13" y="23" width="16" height="15" rx="1.5"/><path class="ac" d="M34 25h17M34 31h17M34 37h10"/>''',
'branding': '''<path d="M10 14h44"/><rect x="7" y="11" width="6" height="6" rx="1"/><rect x="51" y="11" width="6" height="6" rx="1"/><circle class="ac" cx="32" cy="14" r="3"/><path d="M32 22l7 13-7 17-7-17z"/><path d="M32 35v6"/><path d="M10 17c0 6 3 10 4 15"/><path d="M54 17c0 6-3 10-4 15"/><circle class="ac" cx="14" cy="40" r="6"/><path d="M11 49h6M12 46h4"/><circle class="ac" cx="50" cy="40" r="6"/><path d="M47 49h6M48 46h4"/>''',
'treinamentos': '''<rect x="25" y="7" width="33" height="23" rx="2"/><path class="ac" d="M30 24l7-7 5 4 10-9"/><path d="M41.5 30v5"/><circle cx="13" cy="15" r="4"/><path d="M13 19v14M7 24l6-2 9-6M9 44l4-11 4 11"/><circle cx="24" cy="44" r="3.5"/><circle cx="36" cy="44" r="3.5"/><circle cx="48" cy="44" r="3.5"/><path d="M18 56c0-5 3-7 6-7s6 2 6 7M30 56c0-5 3-7 6-7s6 2 6 7M42 56c0-5 3-7 6-7s6 2 6 7"/>''',
'pesquisa-dados': '''<circle cx="20" cy="15" r="8"/><path class="ac" d="M16.5 17c2 2.5 5 2.5 7 0"/><path d="M17.5 12.5h.01M22.5 12.5h.01"/><circle cx="44" cy="15" r="8"/><path d="M40.5 19.5c2-2.5 5-2.5 7 0"/><path d="M41.5 12.5h.01M46.5 12.5h.01"/><path d="M10 52a22 22 0 0 1 44 0"/><path class="ac" d="M32 52l9-12"/><circle cx="32" cy="52" r="3"/><path d="M15 44l3 2M49 44l-3 2M32 32v3"/>''',
'papelaria-fina': '''<rect x="6" y="18" width="36" height="26" rx="2"/><path d="M6 20l18 13 18-13"/><rect x="28" y="34" width="30" height="19" rx="2"/><path class="ac" d="M33 41h12M33 46h18"/><circle class="ac" cx="52" cy="41" r="2"/>''',
'automacao-vip': '''<path d="M12 10h32a4 4 0 0 1 4 4v18a4 4 0 0 1-4 4H26l-10 8v-8h-4a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z"/><path d="M18 23h.01M28 23h.01M38 23h.01"/><circle class="ac" cx="48" cy="46" r="5"/><path class="ac" d="M48 37v3M48 52v3M39 46h3M54 46h3M41.6 39.6l2.1 2.1M52.3 50.3l2.1 2.1M41.6 52.4l2.1-2.1M52.3 41.7l2.1-2.1"/>''',
}


def svg(slug):
    return ('<svg class="servico-icone" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONES[slug] + '</svg>')
