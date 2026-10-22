/* Conceito Prime: scripts compartilhados */

/* ========== CONTATO: número único do WhatsApp ==========
   Comercial (José), o mesmo número do botão do site anterior. Trocar só aqui. */
const WA_NUMERO = '5541999904764';
const WA_ADMINISTRATIVO = '5541998863226';

window.dataLayer = window.dataLayer || [];
function track(event, data) { window.dataLayer.push(Object.assign({ event: event }, data || {})); }

/* Preserva gclid, gbraid, wbraid e utm_* da chegada para anexar ao lead */
const RASTREIO = (function () {
  const chaves = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  let salvo = {};
  try { salvo = JSON.parse(sessionStorage.getItem('cp_rastreio') || '{}'); } catch (e) { salvo = {}; }
  const qs = new URLSearchParams(location.search);
  chaves.forEach(function (k) { if (qs.get(k)) salvo[k] = qs.get(k).slice(0, 200); });
  try { sessionStorage.setItem('cp_rastreio', JSON.stringify(salvo)); } catch (e) { /* sem storage */ }
  return salvo;
})();

function waLink(msg) { return 'https://wa.me/' + WA_NUMERO + '?text=' + encodeURIComponent(msg); }

function abrirWhatsApp(url, posicao) {
  track('whatsapp_open', { posicao: posicao || 'desconhecida' });
  const w = window.open(url, '_blank');
  if (w) { try { w.opener = null; } catch (e) { /* ignora */ } } else { location.href = url; }
}

/* ========== FORMULÁRIO "SOLICITE UM DIAGNÓSTICO" ==========
   O mesmo em todas as páginas (inline, popup do site e popup de WhatsApp das LPs).
   Em etapas: primeiro o que se responde com um clique (segmento e faturamento), por último o que precisa digitar.
   Envio:
   - no site: grava o lead (/api/lead) e abre o WhatsApp com a mensagem pronta;
   - nas LPs da campanha (body data-contato="formulario"): envia para /api/lead-b2b e redireciona para
     /obrigado-qualificado/ (a partir de R$ 100 mil/mês) ou /obrigado/.
   Marcação na página: <form data-diagnostico data-pagina="b2b" data-segmento="industria" data-servico="Branding"
   data-desc="..." data-titulo-id="..."></form>. O conteúdo é montado aqui. */
const DIAG_SEGMENTOS = [
  ['industria', 'Indústria', 'fa-industry'],
  ['distribuidor', 'Distribuidor ou atacado', 'fa-truck'],
  ['servicos', 'Serviços', 'fa-briefcase'],
  ['tecnologia', 'Tecnologia', 'fa-microchip'],
  ['saude', 'Saúde e bem-estar', 'fa-heart-pulse'],
  ['imobiliario', 'Imobiliário e construção', 'fa-building'],
  ['alimentacao', 'Alimentação', 'fa-utensils'],
  ['ecommerce', 'E-commerce', 'fa-cart-shopping'],
  ['varejo', 'Varejo', 'fa-store'],
  ['educacao', 'Educação', 'fa-graduation-cap'],
  ['outros', 'Outro segmento', 'fa-ellipsis']
];
const DIAG_FATURAMENTO = [
  ['ate-10k', 'Até R$ 10 mil'],
  ['10k-50k', 'R$ 10 mil a R$ 50 mil'],
  ['50k-100k', 'R$ 50 mil a R$ 100 mil'],
  ['100k-500k', 'R$ 100 mil a R$ 500 mil'],
  ['500k-1m', 'R$ 500 mil a R$ 1 milhão'],
  ['1m-5m', 'R$ 1 milhão a R$ 5 milhões'],
  ['acima-5m', 'Acima de R$ 5 milhões'],
  ['nao-faturou', 'Ainda não faturamos']
];
const DIAG_TOTAL = 4;
const DIAG_DICAS = ['Leva menos de 1 minuto', 'Boa! Só mais um clique', 'Já passou da metade', 'Último passo'];
const FAIXAS_QUALIFICADAS = ['100k-500k', '500k-1m', '1m-5m', 'acima-5m'];

function diagEsc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

function diagHTML(o) {
  const segs = DIAG_SEGMENTOS.map(function (s) {
    return `<label class="diag-opcao"><input type="radio" name="segmento" value="${s[0]}"${o.segmento === s[0] ? ' checked' : ''}><span><i class="fas ${s[2]}" aria-hidden="true"></i>${s[1]}</span></label>`;
  }).join('');
  const fats = DIAG_FATURAMENTO.map(function (f) {
    return `<label class="diag-opcao diag-opcao--linha"><input type="radio" name="faturamento" value="${f[0]}"><span>${f[1]}</span></label>`;
  }).join('');
  const b2b = o.envio === 'lead-b2b';
  const botaoFinal = b2b
    ? '<i class="fas fa-paper-plane" aria-hidden="true"></i> Solicitar diagnóstico'
    : '<i class="fab fa-whatsapp" aria-hidden="true"></i> Enviar e abrir o WhatsApp';
  const desc = o.desc || (o.servico ? 'Interesse em <strong>' + diagEsc(o.servico) + '</strong>. São 4 perguntas rápidas.' : 'São 4 perguntas rápidas e seguimos a conversa com você.');
  return `
    <div class="diag-topo">
      <p class="diag-eyebrow"><i class="fas fa-bolt" aria-hidden="true"></i> <span data-diag-dica>${DIAG_DICAS[0]}</span></p>
      <h2 class="diag-titulo" id="${o.tituloId}">Solicite um diagnóstico</h2>
      <p class="diag-desc">${desc}</p>
      <div class="diag-barra" aria-hidden="true"><span data-diag-barra></span></div>
      <p class="diag-contador" data-diag-contador>Etapa 1 de ${DIAG_TOTAL}</p>
    </div>
    <div class="diag-hist" data-diag-hist aria-live="polite">
      <p class="diag-msg diag-msg--in">Olá! 👋 Para preparar o seu diagnóstico, são só 4 perguntas rápidas.</p>
    </div>
    <fieldset class="diag-etapa" data-etapa="1">
      <legend class="diag-pergunta">Qual o segmento da sua empresa?</legend>
      <div class="diag-opcoes">${segs}</div>
      <button type="button" class="diag-avancar diag-avancar--opcao" data-diag-avancar hidden>Continuar <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
    </fieldset>
    <fieldset class="diag-etapa" data-etapa="2" hidden>
      <legend class="diag-pergunta">Quanto a empresa fatura por mês, em média?</legend>
      <div class="diag-opcoes diag-opcoes--lista">${fats}</div>
      <button type="button" class="diag-avancar diag-avancar--opcao" data-diag-avancar hidden>Continuar <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
    </fieldset>
    <fieldset class="diag-etapa" data-etapa="3" hidden>
      <legend class="diag-pergunta">Como podemos te chamar?</legend>
      <div class="diag-campos">
        <label class="diag-campo"><span>Seu nome</span><input type="text" name="nome" autocomplete="given-name" placeholder="Primeiro nome" maxlength="80" enterkeyhint="next"></label>
        <label class="diag-campo"><span>Nome da empresa</span><input type="text" name="empresa" autocomplete="organization" placeholder="Empresa" maxlength="120" enterkeyhint="next"></label>
      </div>
      <button type="button" class="diag-avancar" data-diag-avancar>Continuar <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
    </fieldset>
    <fieldset class="diag-etapa" data-etapa="4" hidden>
      <legend class="diag-pergunta" data-diag-pergunta-tel>Qual o seu WhatsApp?</legend>
      <div class="diag-campos">
        <label class="diag-campo"><span>WhatsApp com DDD</span><span class="diag-tel"><span class="diag-ddi" aria-hidden="true">🇧🇷 +55</span><input type="tel" name="telefone" inputmode="tel" autocomplete="tel-national" placeholder="(41) 99999-9999" data-phone-mask enterkeyhint="send"></span></label>
      </div>
      <button type="submit" class="diag-enviar">${botaoFinal}</button>
      <p class="diag-aviso"><i class="fas fa-lock" aria-hidden="true"></i> Usamos seus dados só para falar com você sobre este pedido.</p>
    </fieldset>
    <p class="diag-erro" data-diag-erro role="alert" aria-live="assertive"></p>
    <button type="button" class="diag-voltar" data-diag-voltar hidden><i class="fas fa-arrow-left" aria-hidden="true"></i> Voltar</button>
    <input type="hidden" name="pagina" value="${diagEsc(o.pagina)}">
    ${o.servico ? `<input type="hidden" name="servico" value="${diagEsc(o.servico)}">` : ''}
    <div class="diag-hp" aria-hidden="true"><label>Não preencha<input type="text" name="hp" tabindex="-1" autocomplete="off"></label></div>
    <div class="diag-ok" data-diag-ok hidden>
      <i class="fas fa-circle-check" aria-hidden="true"></i>
      <p class="diag-ok-titulo" data-diag-ok-titulo>Pronto!</p>
      <p class="diag-ok-texto">Abrimos o WhatsApp com a sua mensagem. É só enviar por lá.</p>
      <a href="#" class="diag-ok-link" data-diag-wa target="_blank" rel="noopener"><i class="fab fa-whatsapp" aria-hidden="true"></i> Abrir o WhatsApp de novo</a>
    </div>`;
}

function diagRotulo(lista, valor) {
  for (let i = 0; i < lista.length; i++) if (lista[i][0] === valor) return lista[i][1];
  return valor || '';
}

function diagMensagem(d) {
  const linhas = ['Olá! Vim pelo site da Conceito Prime e quero solicitar um diagnóstico.', ''];
  linhas.push('Nome: ' + d.nome);
  linhas.push('Empresa: ' + d.empresa);
  linhas.push('WhatsApp: ' + d.telefone);
  linhas.push('Segmento: ' + diagRotulo(DIAG_SEGMENTOS, d.segmento));
  linhas.push('Faturamento mensal: ' + diagRotulo(DIAG_FATURAMENTO, d.faturamento));
  if (d.servico) linhas.push('Interesse: ' + d.servico);
  linhas.push('', 'Origem: site (' + location.pathname + ')');
  const ref = Object.keys(RASTREIO).map(function (k) { return k + '=' + RASTREIO[k]; }).join(' ');
  if (ref) linhas.push('Ref: ' + ref);
  return linhas.join('\n');
}

function enviarParaPlanilha(dados) {
  /* Endpoint do Worker (worker.js). Fica inerte enquanto LEAD_WEBHOOK não estiver configurado. */
  try {
    const corpo = JSON.stringify(Object.assign({ pagina: location.pathname, origem: 'site' }, RASTREIO, dados));
    if (navigator.sendBeacon) navigator.sendBeacon('/api/lead', new Blob([corpo], { type: 'application/json' }));
  } catch (e) { /* o lead segue pelo WhatsApp mesmo assim */ }
}

function initDiagnostico(form) {
  if (form._diag) return form._diag;
  const envio = form.dataset.envio || (document.body.dataset.contato === 'formulario' ? 'lead-b2b' : 'whatsapp');
  const tituloId = form.dataset.tituloId || ('diag-' + Math.random().toString(36).slice(2, 8));
  const segPadrao = form.dataset.segmento || '';
  form.classList.add('diag');
  form.setAttribute('novalidate', '');
  form.setAttribute('aria-labelledby', tituloId);
  form.innerHTML = diagHTML({
    envio: envio, tituloId: tituloId, segmento: segPadrao, servico: form.dataset.servico || '',
    desc: form.dataset.desc || '', pagina: form.dataset.pagina || location.pathname
  });

  const etapas = Array.prototype.slice.call(form.querySelectorAll('.diag-etapa'));
  etapas.forEach(function (e) { e.setAttribute('tabindex', '-1'); });
  const hist = form.querySelector('[data-diag-hist]');
  const erroBox = form.querySelector('[data-diag-erro]');
  const voltar = form.querySelector('[data-diag-voltar]');
  const barra = form.querySelector('[data-diag-barra]');
  const contador = form.querySelector('[data-diag-contador]');
  const dica = form.querySelector('[data-diag-dica]');
  const ok = form.querySelector('[data-diag-ok]');
  const tel = form.querySelector('[name="telefone"]');
  const enviar = form.querySelector('.diag-enviar');
  const enviarHTML = enviar.innerHTML;
  maskPhone(tel);
  let atual = 1;
  let iniciou = false;
  let ocupado = false;

  function valor(nome) {
    const el = form.querySelector('[name="' + nome + '"]:checked') || form.querySelector('[name="' + nome + '"]:not([type=radio])');
    return el ? String(el.value || '').trim() : '';
  }
  function marcar(el, valido) { el.classList.toggle('is-invalid', !valido); el.setAttribute('aria-invalid', String(!valido)); }
  function erro(msg) { erroBox.textContent = msg || ''; }
  function comecar() { if (!iniciou) { iniciou = true; track('form_start', { formulario: form.id || 'diagnostico', pagina: location.pathname }); } }

  function atualizarOpcao(n) {
    const etapa = etapas[n - 1];
    const btn = etapa.querySelector('.diag-avancar--opcao');
    if (btn) btn.hidden = !etapa.querySelector('input:checked');
  }

  function ir(n, focar) {
    atual = n;
    etapas.forEach(function (e, i) { e.hidden = i !== n - 1; });
    voltar.hidden = n === 1;
    barra.style.width = Math.max(6, (n - 1) / DIAG_TOTAL * 100) + '%';
    contador.textContent = 'Etapa ' + n + ' de ' + DIAG_TOTAL;
    dica.textContent = DIAG_DICAS[n - 1];
    if (n === 4) {
      const nome = valor('nome').split(' ')[0];
      form.querySelector('[data-diag-pergunta-tel]').textContent = nome ? 'Prazer, ' + nome + '! Qual o seu WhatsApp?' : 'Qual o seu WhatsApp?';
    }
    if (n <= 2) atualizarOpcao(n);
    erro('');
    form.dispatchEvent(new CustomEvent('diag:etapa', { detail: { etapa: n, total: DIAG_TOTAL } }));
    if (focar) {
      setTimeout(function () {
        const etapa = etapas[n - 1];
        /* etapa de clique sem opção marcada: foco no grupo (sem destacar nenhuma opção como se estivesse escolhida) */
        const alvo = etapa.querySelector('input:checked') || etapa.querySelector('input:not([type=hidden]):not([type=radio])') || etapa;
        alvo.focus({ preventScroll: true });
      }, 60);
    }
  }

  function validar(n) {
    if (n === 1 && !valor('segmento')) { erro('Escolha o segmento da empresa para continuar.'); return false; }
    if (n === 2 && !valor('faturamento')) { erro('Escolha uma faixa de faturamento para continuar.'); return false; }
    if (n === 3) {
      const nome = form.querySelector('[name="nome"]');
      const emp = form.querySelector('[name="empresa"]');
      const okNome = nome.value.trim().length >= 2;
      const okEmp = emp.value.trim().length >= 2;
      marcar(nome, okNome); marcar(emp, okEmp);
      if (!okNome || !okEmp) { erro('Preencha o seu nome e o nome da empresa.'); (okNome ? emp : nome).focus(); return false; }
    }
    if (n === 4) {
      const okTel = tel.value.replace(/\D/g, '').length >= 10;
      marcar(tel, okTel);
      if (!okTel) { erro('Confira o WhatsApp: precisa ter DDD e o número completo.'); tel.focus(); return false; }
    }
    return true;
  }

  function resposta(n) {
    if (n === 1) return diagRotulo(DIAG_SEGMENTOS, valor('segmento'));
    if (n === 2) return diagRotulo(DIAG_FATURAMENTO, valor('faturamento'));
    if (n === 3) return valor('nome') + ', da ' + valor('empresa');
    return valor('telefone');
  }

  function registrar(n) {
    const pergunta = etapas[n - 1].querySelector('legend').textContent;
    hist.insertAdjacentHTML('beforeend',
      '<p class="diag-msg diag-msg--in" data-hist="' + n + '">' + diagEsc(pergunta) + '</p>' +
      '<p class="diag-msg diag-msg--out" data-hist="' + n + '">' + diagEsc(resposta(n)) + ' <i class="fas fa-check-double" aria-hidden="true"></i></p>');
    hist.scrollTop = hist.scrollHeight;
  }

  function avancar() {
    if (!validar(atual)) return;
    comecar();
    registrar(atual);
    track('form_etapa', { formulario: form.id || 'diagnostico', etapa: atual + 1 });
    if (atual < DIAG_TOTAL) ir(atual + 1, true);
  }

  etapas.slice(0, 2).forEach(function (etapa, i) {
    etapa.querySelectorAll('input[type=radio]').forEach(function (r) {
      r.addEventListener('change', function () {
        comecar();
        atualizarOpcao(i + 1);
        /* um clique já avança: dá tempo de ver a opção marcada */
        setTimeout(function () { if (atual === i + 1) avancar(); }, 260);
      });
    });
  });
  form.querySelectorAll('[data-diag-avancar]').forEach(function (b) { b.addEventListener('click', avancar); });
  voltar.addEventListener('click', function () {
    if (atual <= 1) return;
    hist.querySelectorAll('[data-hist="' + (atual - 1) + '"]').forEach(function (m) { m.remove(); });
    ir(atual - 1, true);
  });
  form.querySelector('[name="nome"]').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); form.querySelector('[name="empresa"]').focus(); }
  });
  form.querySelector('[name="empresa"]').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); avancar(); }
  });
  form.addEventListener('input', function (e) { comecar(); if (e.target.classList.contains('is-invalid')) marcar(e.target, true); });

  function coletar() {
    const d = {};
    ['segmento', 'faturamento', 'nome', 'empresa', 'telefone', 'pagina', 'servico', 'hp'].forEach(function (k) { const v = valor(k); if (v) d[k] = v; });
    return d;
  }

  function concluirWhatsApp(d, qualificado) {
    const evento = { formulario: form.id || 'diagnostico', pagina: location.pathname, faturamento: d.faturamento, segmento: d.segmento, lead_qualificado: qualificado };
    track('form_submit', evento);
    /* Conversão principal "Formulário comercial" (GTM: evento lead_comercial). Só os formulários de diagnóstico
       disparam este evento; o formulário de vagas e fornecedores nunca dispara. */
    track('lead_comercial', { origem: 'site', canal: form.dataset.canal || form.id || 'diagnostico', pagina: location.pathname, lead_id: String(Date.now()), lead_qualificado: qualificado });
    try { sessionStorage.setItem('cp_lead_enviado', '1'); } catch (e) { /* segue */ }
    /* Conversão principal do Google Ads: só empresa a partir de R$ 100 mil/mês (gatilho no GTM pelo evento lead_qualificado) */
    if (qualificado) track('lead_qualificado', evento);
    const url = waLink(diagMensagem(d));
    enviarParaPlanilha(d);
    abrirWhatsApp(url, form.dataset.canal || 'formulario');
    etapas.forEach(function (e) { e.hidden = true; });
    voltar.hidden = true;
    barra.style.width = '100%';
    contador.textContent = 'Concluído';
    dica.textContent = 'Tudo certo';
    form.querySelector('[data-diag-ok-titulo]').textContent = 'Pronto, ' + d.nome.split(' ')[0] + '!';
    form.querySelector('[data-diag-wa]').href = url;
    ok.hidden = false;
    form.dispatchEvent(new CustomEvent('diag:enviado', { detail: { qualificado: qualificado } }));
  }

  function concluirB2B(d, qualificado) {
    d.lead_qualificado = qualificado ? 'sim' : 'nao';
    d.origem = 'campanha-google-ads';
    d.canal = form.dataset.canal || 'formulario';
    Object.keys(RASTREIO).forEach(function (k) { d[k] = RASTREIO[k]; });
    ocupado = true;
    enviar.disabled = true;
    enviar.innerHTML = '<i class="fas fa-spinner fa-spin" aria-hidden="true"></i> Enviando...';
    const controle = window.AbortController ? new AbortController() : null;
    const limite = setTimeout(function () { if (controle) controle.abort(); }, 8000);
    fetch('/api/lead-b2b', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(d),
      signal: controle ? controle.signal : undefined
    }).then(function (r) {
      clearTimeout(limite);
      if (!r.ok) throw new Error('status ' + r.status);
      track('lead_b2b', { lead_qualificado: qualificado, faturamento: d.faturamento, segmento: d.segmento, pagina: d.pagina, canal: d.canal });
      try { sessionStorage.setItem('cp_lead_enviado', '1'); } catch (e) { /* segue */ }
      try {
        sessionStorage.setItem('cp_lead_b2b', JSON.stringify({ nome: d.nome, empresa: d.empresa, faturamento: d.faturamento, qualificado: qualificado, pagina: d.pagina, t: Date.now() }));
      } catch (err) { /* segue sem personalizar a página de obrigado */ }
      setTimeout(function () { location.href = qualificado ? '/obrigado-qualificado/' : '/obrigado/'; }, 250);
    }).catch(function () {
      clearTimeout(limite);
      ocupado = false;
      enviar.disabled = false;
      enviar.innerHTML = enviarHTML;
      erro('Não conseguimos enviar agora. Tente de novo em alguns instantes ou escreva para contato@conceitop.com.br.');
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (ocupado) return;
    if (atual < DIAG_TOTAL) { avancar(); return; }
    if (!validar(DIAG_TOTAL)) return;
    const d = coletar();
    if (d.hp) return; /* robô */
    registrar(DIAG_TOTAL);
    const qualificado = FAIXAS_QUALIFICADAS.indexOf(d.faturamento) !== -1;
    if (envio === 'lead-b2b') concluirB2B(d, qualificado);
    else concluirWhatsApp(d, qualificado);
  });

  function reset() {
    form.reset();
    if (segPadrao) { const r = form.querySelector('[name="segmento"][value="' + segPadrao + '"]'); if (r) r.checked = true; }
    form.querySelectorAll('.is-invalid').forEach(function (el) { marcar(el, true); });
    hist.querySelectorAll('[data-hist]').forEach(function (m) { m.remove(); });
    ok.hidden = true;
    ocupado = false;
    enviar.disabled = false;
    enviar.innerHTML = enviarHTML;
    ir(1, false);
  }

  ir(1, false);
  form._diag = { reset: reset, ir: ir, focar: function () { ir(atual, true); } };
  return form._diag;
}

/* ========== POPUP DO DIAGNÓSTICO ==========
   Site: CTAs de orçamento abrem o formulário no visual da marca.
   LPs da campanha: o botão flutuante do WhatsApp abre o mesmo formulário com a cara do WhatsApp. */
(function initLeadModal() {
  const overlay = document.createElement('div');
  overlay.id = 'lead-overlay';
  overlay.className = 'lead-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'lead-title');
  overlay.innerHTML = `
    <div class="lead-card">
      <div class="wa-chat-head">
        <span class="wa-chat-avatar"><img src="/assets/images/apple-touch-icon.png" alt="" width="40" height="40"></span>
        <div class="wa-chat-id">
          <p class="wa-chat-nome">Conceito Prime <i class="fas fa-circle-check" aria-hidden="true"></i></p>
          <p class="wa-chat-status" data-wa-status>online</p>
        </div>
      </div>
      <button type="button" class="lead-close" id="lead-close" aria-label="Fechar">&times;</button>
      <form id="lead-form" data-diagnostico data-titulo-id="lead-title"></form>
    </div>`;
  document.body.appendChild(overlay);

  const form = document.getElementById('lead-form');
  /* Nas LPs, o popup herda a página e o segmento do formulário da própria página (ex.: /industrial já vem com Indústria) */
  const daPagina = document.querySelector('form[data-diagnostico][data-pagina]');
  if (daPagina) {
    form.dataset.pagina = daPagina.dataset.pagina;
    if (daPagina.dataset.segmento) form.dataset.segmento = daPagina.dataset.segmento;
  }
  const diag = initDiagnostico(form);
  const status = overlay.querySelector('[data-wa-status]');
  form.addEventListener('diag:etapa', function (e) { status.textContent = 'online · etapa ' + e.detail.etapa + ' de ' + e.detail.total; });

  let ultimoFoco = null;
  let fechar = null;
  const closeModal = function () {
    if (!overlay.classList.contains('open')) return;
    clearTimeout(fechar);
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
  };
  form.addEventListener('diag:enviado', function () { fechar = setTimeout(closeModal, 7000); });

  window.openLeadModal = function (modo) {
    ultimoFoco = document.activeElement;
    const wa = modo === 'whatsapp';
    overlay.classList.toggle('lead-overlay--wa', wa);
    form.classList.toggle('diag--wa', wa);
    form.dataset.canal = wa ? 'popup-whatsapp' : 'popup';
    diag.reset();
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    diag.focar();
  };

  document.getElementById('lead-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  /* CTAs de orçamento abrem o formulário */
  document.addEventListener('click', function (e) {
    const a = e.target.closest('a, button');
    if (!a) return;
    if (a.closest('#wa-float') || a.closest('#lead-overlay') || a.closest('.diag')) return;
    const ehCta = a.classList.contains('btn-wa') || a.classList.contains('btn-luxury') ||
      a.classList.contains('btn-brand') || a.classList.contains('contact-submit');
    if (!ehCta) return;
    if (a.tagName === 'BUTTON' && a.type === 'submit' && a.form) return;
    e.preventDefault();
    track('cta_click', { posicao: a.dataset.cta || (a.closest('section, header, footer') || {}).id || 'cta', texto: a.textContent.trim().slice(0, 60) });
    openLeadModal();
  });
})();

/* Formulários na página */
document.querySelectorAll('form[data-diagnostico]').forEach(function (form) {
  if (form.id === 'lead-form') return;
  initDiagnostico(form);
});

/* Botões que levam ao formulário da página (#orcamento): põem o foco na etapa atual depois da rolagem */
document.querySelectorAll('a[href="#orcamento"]').forEach(function (a) {
  a.addEventListener('click', function () {
    track('cta_click', { posicao: a.dataset.cta || 'ancora', texto: a.textContent.trim().slice(0, 60) });
    const f = document.querySelector('#orcamento form[data-diagnostico]');
    if (f && f._diag) setTimeout(f._diag.focar, 600);
  });
});

function maskPhone(input) {
  if (input.dataset.masked) return;
  input.dataset.masked = '1';
  input.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '').slice(0, 11);
    if (v.length > 10) v = v.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
    else if (v.length > 6) v = v.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
    else if (v.length > 2) v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    else if (v.length > 0) v = v.replace(/^(\d*)/, '($1');
    e.target.value = v.trim();
  });
}

document.querySelectorAll('[data-phone-mask]').forEach(maskPhone);

/* Links de WhatsApp escritos no HTML passam a usar o número único */
document.querySelectorAll('a[href*="wa.me/"]').forEach(function (a) {
  if (a.closest('#lead-overlay')) return;
  a.href = a.href.replace(/wa\.me\/\d+/, 'wa.me/' + WA_NUMERO);
  a.addEventListener('click', function () { track('whatsapp_open', { posicao: a.dataset.cta || 'link' }); });
});

/* Botão flutuante WhatsApp: painel Fale Conosco (mesmo formato do site anterior, sem RH) */
(function initWhatsAppFloat() {
  /* Páginas da campanha (body data-contato="formulario"): o botão do WhatsApp não abre conversa direta.
     Ele abre o formulário de diagnóstico em popup com a cara do WhatsApp; o envio segue o fluxo da campanha
     (/api/lead-b2b e página de obrigado, onde o lead qualificado encontra o WhatsApp com a mensagem pronta). */
  if (document.body.dataset.contato === 'formulario') {
    const botao = document.createElement('div');
    botao.id = 'wa-float';
    botao.className = 'wa-float';
    botao.innerHTML = '<button type="button" class="wa-float-btn" id="wa-float-btn" aria-label="Falar no WhatsApp"><i class="fab fa-whatsapp" aria-hidden="true"></i></button>';
    document.body.appendChild(botao);
    document.getElementById('wa-float-btn').addEventListener('click', function () {
      track('cta_click', { posicao: 'whatsapp-flutuante', texto: 'WhatsApp' });
      if (window.openLeadModal) window.openLeadModal('whatsapp');
    });
    return;
  }
  const contatos = [
    { setor: 'Comercial', nome: 'José', fone: '(41) 99990-4764', numero: WA_NUMERO, msg: 'Olá! Vim pelo site da Conceito Prime e gostaria de falar com o Comercial.' },
    { setor: 'Administrativo', nome: 'Vitor', fone: '(41) 99886-3226', numero: WA_ADMINISTRATIVO, msg: 'Olá! Vim pelo site da Conceito Prime e gostaria de falar com o Administrativo.' }
  ];
  const itens = contatos.map(function (c) {
    const url = 'https://wa.me/' + c.numero + '?text=' + encodeURIComponent(c.msg);
    return `
        <a href="${url}" target="_blank" rel="noopener" class="wa-contact" data-cta="flutuante-${c.setor.toLowerCase()}">
          <span class="wa-contact-avatar" aria-hidden="true"><i class="fab fa-whatsapp"></i></span>
          <span class="wa-contact-text">
            <span class="wa-contact-name">${c.setor} - ${c.nome}</span>
            <span class="wa-contact-phone">${c.fone}</span>
          </span>
          <i class="fab fa-whatsapp" aria-hidden="true"></i>
        </a>`;
  }).join('');

  const widget = document.createElement('div');
  widget.id = 'wa-float';
  widget.className = 'wa-float';
  widget.innerHTML = `
    <div class="wa-panel hidden" id="wa-float-menu" role="dialog" aria-labelledby="wa-panel-title">
      <div class="wa-panel-head">
        <i class="fab fa-whatsapp" aria-hidden="true"></i>
        <div>
          <p class="wa-panel-title" id="wa-panel-title">Fale Conosco</p>
          <p class="wa-panel-sub">Entre em contato pelo número oficial da Conceito Prime.</p>
        </div>
      </div>
      <div class="wa-panel-body">
        <p class="wa-panel-note">Nosso time costuma responder em poucos minutos.</p>
        ${itens}
      </div>
      <div class="wa-panel-foot">
        <strong>Currículos e propostas de fornecedores</strong> não são atendidos pelo WhatsApp: envie pelo formulário <a href="/trabalhe-conosco/">Vagas e fornecedores</a>.
      </div>
    </div>
    <button type="button" class="wa-float-btn" id="wa-float-btn" aria-label="Falar no WhatsApp" aria-expanded="false" aria-controls="wa-float-menu">
      <i class="fab fa-whatsapp" aria-hidden="true"></i>
    </button>
  `;
  document.body.appendChild(widget);

  const btn = document.getElementById('wa-float-btn');
  const menu = document.getElementById('wa-float-menu');
  const icone = btn.querySelector('i');
  const definir = function (aberto) {
    menu.classList.toggle('hidden', !aberto);
    btn.setAttribute('aria-expanded', String(aberto));
    btn.setAttribute('aria-label', aberto ? 'Fechar contatos do WhatsApp' : 'Falar no WhatsApp');
    icone.className = aberto ? 'fas fa-times' : 'fab fa-whatsapp';
  };
  menu.querySelectorAll('a.wa-contact').forEach(function (a) {
    a.addEventListener('click', function () {
      track('whatsapp_open', { posicao: a.dataset.cta });
      /* Conversão principal "Clique WhatsApp comercial" (GTM: evento whatsapp_comercial). O Administrativo não conta. */
      if (a.dataset.cta === 'flutuante-comercial') track('whatsapp_comercial', { pagina: location.pathname });
    });
  });
  btn.addEventListener('click', function () {
    const abrir = menu.classList.contains('hidden');
    definir(abrir);
    if (abrir) track('cta_click', { posicao: 'flutuante', texto: 'Fale Conosco' });
  });
  document.addEventListener('click', function (e) { if (!widget.contains(e.target)) definir(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.classList.contains('hidden')) { definir(false); btn.focus(); } });
})();

/* ========== POPUP DE SAÍDA (exit intent) ==========
   Mesmo comportamento do site anterior: aparece toda vez que a pessoa leva o mouse para fora da janela
   pela parte de cima (indo fechar a aba, trocar de aba ou digitar outro endereço), em qualquer página.
   - Uma vez por página aberta: fechou, só volta ao abrir outra página ou recarregar.
   - Só em computador com mouse: no celular não existe esse gesto (e o Google penaliza intersticiais no mobile).
   - Não aparece nas páginas de obrigado, com o formulário de diagnóstico aberto, nem depois que o lead já foi enviado.
   - O botão abre o formulário "Solicite um diagnóstico". */
(function initPopupSaida() {
  if (document.body.hasAttribute('data-tipos-conversao')) return;
  if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1024px)').matches) return;

  const IMG = '/assets/images/popup-consultor-v2.webp';
  let armado = false;
  let mostrado = false;
  /* 1,5 s de carência: evita disparar com o mouse que ainda está na barra do navegador quando a página abre */
  setTimeout(function () {
    armado = true;
    const pre = new Image(); pre.src = IMG; /* carrega a foto só agora, sem pesar na abertura da página */
  }, 1500);

  function bloqueado() {
    let enviado = false;
    try { enviado = !!sessionStorage.getItem('cp_lead_enviado'); } catch (e) { enviado = false; }
    return enviado || !!document.querySelector('#lead-overlay.open, .saida-overlay, .serv-overlay') ||
      (window.dataLayer || []).some(function (e) { return e && /^(form_submit|lead_b2b|lead_qualificado)$/.test(e.event); });
  }

  function mostrar() {
    mostrado = true;
    const overlay = document.createElement('div');
    overlay.className = 'saida-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'saida-titulo');
    overlay.innerHTML = `
      <div class="saida-card">
        <button type="button" class="saida-fechar" aria-label="Fechar">&times;</button>
        <div class="saida-foto"><img src="${IMG}" alt="Consultor da Conceito Prime à mesa de reunião, com café e notebook" width="560" height="840"></div>
        <div class="saida-texto">
          <p class="saida-eyebrow"><i class="fas fa-mug-hot" aria-hidden="true"></i> Antes de sair</p>
          <h2 id="saida-titulo">Uma reunião com nosso consultor <span>não tem preço</span></h2>
          <p class="saida-desc">Em poucos minutos entendemos o momento da sua empresa e mostramos o próximo passo para vender mais.</p>
          <button type="button" class="saida-cta">Quero falar com um consultor <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
          <button type="button" class="saida-depois">Agora não</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    const anterior = document.activeElement;
    const fechar = function (motivo) {
      overlay.classList.remove('open');
      document.removeEventListener('keydown', teclado);
      setTimeout(function () { overlay.remove(); }, 300);
      if (motivo) track('exit_popup_fechar', { motivo: motivo });
      if (anterior && anterior.focus && motivo !== 'cta') anterior.focus();
    };
    const teclado = function (e) { if (e.key === 'Escape') fechar('esc'); };
    document.addEventListener('keydown', teclado);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) fechar('fora'); });
    overlay.querySelector('.saida-fechar').addEventListener('click', function () { fechar('x'); });
    overlay.querySelector('.saida-depois').addEventListener('click', function () { fechar('agora-nao'); });
    overlay.querySelector('.saida-cta').addEventListener('click', function () {
      track('exit_popup_clique', { pagina: location.pathname });
      fechar('cta');
      if (window.openLeadModal) window.openLeadModal();
    });
    requestAnimationFrame(function () { overlay.classList.add('open'); overlay.querySelector('.saida-cta').focus({ preventScroll: true }); });
    track('exit_popup_view', { pagina: location.pathname });
  }

  /* Saída pela parte de cima da janela (abas, barra de endereço, botão de fechar). Com o mouse rápido o
     último evento chega com y um pouco abaixo de 0, por isso a margem de 40 px. */
  document.addEventListener('mouseout', function (e) {
    if (mostrado || !armado || e.relatedTarget || e.toElement) return;
    if (e.clientY > 40) return;
    if (bloqueado()) return;
    mostrar();
  });
})();

/* ========== POPUP DO PORTFÓLIO (home) ==========
   Cada projeto do portfólio ([data-popup-servico]) abre um popup com a imagem, a descrição e o que está
   incluso no serviço (lidos do próprio item, .servico-detalhe). O botão troca o conteúdo do popup pelo
   formulário "Solicite um diagnóstico", já com o serviço preenchido, sem sair da página. */
(function initServicosPopup() {
  const cards = document.querySelectorAll('[data-popup-servico]');
  if (!cards.length) return;
  let overlay = null;
  let anterior = null;

  function fechar() {
    if (!overlay) return;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    const o = overlay;
    overlay = null;
    setTimeout(function () { o.remove(); }, 300);
    document.removeEventListener('keydown', teclado);
    if (anterior && anterior.focus) anterior.focus();
  }
  function teclado(e) { if (e.key === 'Escape') fechar(); }

  function abrir(card) {
    const servico = card.dataset.servico;
    const titulo = card.dataset.titulo || servico;
    const det = card.querySelector('.servico-detalhe');
    anterior = document.activeElement;
    overlay = document.createElement('div');
    overlay.className = 'serv-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'serv-titulo');
    overlay.innerHTML = `
      <div class="serv-card">
        <button type="button" class="serv-fechar" aria-label="Fechar">&times;</button>
        <div class="serv-foto"><img src="${card.dataset.img}" alt="${diagEsc(card.dataset.alt || '')}" width="800" height="800"></div>
        <div class="serv-painel">
          <div class="serv-view" data-view="detalhe">
            <p class="serv-eyebrow">${diagEsc(card.dataset.eyebrow || 'Serviço')}</p>
            <h2 class="serv-titulo" id="serv-titulo">${diagEsc(titulo)}</h2>
            ${det.innerHTML}
            <button type="button" class="serv-cta">Quero um projeto assim <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
          </div>
          <div class="serv-view" data-view="form" hidden>
            <button type="button" class="serv-voltar"><i class="fas fa-arrow-left" aria-hidden="true"></i> Voltar para o projeto</button>
            <form data-diagnostico data-servico="${diagEsc(servico)}" data-titulo-id="serv-form-titulo" data-canal="popup-portfolio"></form>
          </div>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
    const o = overlay;
    const vDet = o.querySelector('[data-view="detalhe"]');
    const vForm = o.querySelector('[data-view="form"]');
    let diag = null;
    o.querySelector('.serv-fechar').addEventListener('click', fechar);
    o.addEventListener('click', function (e) { if (e.target === o) fechar(); });
    document.addEventListener('keydown', teclado);
    o.querySelector('.serv-cta').addEventListener('click', function () {
      track('portfolio_popup_cta', { servico: servico, projeto: titulo });
      vDet.hidden = true;
      vForm.hidden = false;
      o.querySelector('.serv-painel').scrollTop = 0;
      if (!diag) diag = initDiagnostico(vForm.querySelector('form'));
      diag.focar();
    });
    o.querySelector('.serv-voltar').addEventListener('click', function () {
      vForm.hidden = true;
      vDet.hidden = false;
      o.querySelector('.serv-cta').focus({ preventScroll: true });
    });
    requestAnimationFrame(function () { o.classList.add('open'); o.querySelector('.serv-cta').focus({ preventScroll: true }); });
    track('portfolio_popup_view', { servico: servico, projeto: titulo });
  }

  cards.forEach(function (card) {
    card.querySelector('.servico-abrir').addEventListener('click', function () { abrir(card); });
  });
})();

/* Eventos de engajamento */
(function initEngajamento() {
  let rolou = false;
  window.addEventListener('scroll', function () {
    if (rolou) return;
    const h = document.documentElement;
    if ((h.scrollTop + innerHeight) / h.scrollHeight >= 0.75) { rolou = true; track('scroll_75'); }
  }, { passive: true });
  setTimeout(function () { track('time_on_page_60s'); }, 60000);
})();

/* Carrossel de depoimentos em vídeo + modal YouTube */
(function initVideoCarousel() {
  const track = document.getElementById('video-carousel-track');
  const viewport = track?.parentElement;
  const dots = document.querySelectorAll('.video-dots .video-dot');
  if (!track || !viewport) return;

  let idx = 0;
  let timer;

  /* 2 depoimentos por vez no desktop, 1 no celular e tablet */
  const desktop = window.matchMedia('(min-width: 1024px)');
  const porVez = () => (desktop.matches ? 2 : 1);
  const posicoes = () => Math.max(1, track.children.length - porVez() + 1);

  const go = (n) => {
    const total = posicoes();
    idx = ((n % total) + total) % total;
    track.style.transform = `translateX(-${idx * (viewport.clientWidth / porVez())}px)`;
    dots.forEach((d, i) => {
      d.hidden = i >= total;
      d.classList.toggle('active', i === idx);
    });
  };

  const start = () => { timer = setInterval(() => go(idx + 1), 6000); };
  const stop = () => clearInterval(timer);

  const reset = () => { stop(); start(); };

  dots.forEach((d, i) => d.addEventListener('click', () => { stop(); go(i); start(); }));
  document.getElementById('video-prev')?.addEventListener('click', () => { stop(); go(idx - 1); reset(); });
  document.getElementById('video-next')?.addEventListener('click', () => { stop(); go(idx + 1); reset(); });

  const wrap = track.closest('.video-carousel-wrap')?.parentElement;
  wrap?.addEventListener('mouseenter', stop);
  wrap?.addEventListener('mouseleave', start);
  window.addEventListener('resize', () => go(idx));
  go(0);
  start();

  let modal = document.getElementById('video-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'video-modal';
    modal.className = 'video-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Reproduzir depoimento em vídeo');
    modal.innerHTML = `
      <div class="video-modal-inner">
        <button type="button" class="video-modal-close" aria-label="Fechar vídeo">&times;</button>
        <div id="video-modal-player"></div>
      </div>`;
    document.body.appendChild(modal);
  }

  const player = document.getElementById('video-modal-player');
  const close = () => {
    modal.classList.remove('open');
    player.innerHTML = '';
    document.body.style.overflow = '';
  };

  modal.querySelector('.video-modal-close').addEventListener('click', close);
  modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });

  document.querySelectorAll('[data-youtube-id]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const id = btn.getAttribute('data-youtube-id');
      const title = btn.getAttribute('data-video-title') || 'Depoimento em vídeo';
      player.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0" title="${title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });
})();

/* Trabalhe Conosco: currículos e fornecedores com anexo (POST /api/trabalhe-conosco) */
(function initTrabalheConosco() {
  const form = document.getElementById('form-trabalhe');
  if (!form) return;
  const EMAIL_FALLBACK = 'contato@conceitop.com.br';
  const LIMITE = 5 * 1024 * 1024;
  const erroBox = form.querySelector('[data-lead-error]');
  const sucesso = document.querySelector('[data-tc-sucesso]');
  const arquivo = form.querySelector('#tc-arquivo');
  const rotuloArquivo = form.querySelector('[data-rotulo-arquivo]');
  const anexoOpcional = form.querySelector('[data-anexo-opcional]');
  const botao = form.querySelector('button[type="submit"]');
  maskPhone(form.querySelector('[data-phone-mask]'));

  const tipoAtual = function () { return form.querySelector('input[name="tipo"]:checked').value; };
  const aplicarTipo = function () {
    const t = tipoAtual();
    form.querySelectorAll('.tc-bloco').forEach(function (b) { b.classList.toggle('hidden', b.dataset.tipo !== t); });
    rotuloArquivo.textContent = t === 'curriculo' ? 'Currículo' : 'Apresentação ou catálogo';
    anexoOpcional.hidden = t === 'curriculo';
  };
  form.querySelectorAll('input[name="tipo"]').forEach(function (r) { r.addEventListener('change', aplicarTipo); });
  try { if (new URLSearchParams(location.search).get('tipo') === 'fornecedor') form.querySelector('input[value="fornecedor"]').checked = true; } catch (e) { /* ignora */ }
  aplicarTipo();

  let iniciou = false;
  form.addEventListener('input', function () { if (!iniciou) { iniciou = true; track('form_start', { formulario: 'trabalhe-conosco' }); } });

  function marcar(el, ok) { el.classList.toggle('is-invalid', !ok); el.setAttribute('aria-invalid', String(!ok)); return ok; }

  function validar() {
    const t = tipoAtual();
    const erros = [];
    form.querySelectorAll('[required], [data-obrigatorio-' + t + ']').forEach(function (el) {
      let ok = !!String(el.value || '').trim();
      if (ok && el.type === 'email') ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
      if (ok && el.name === 'telefone') ok = el.value.replace(/\D/g, '').length >= 10;
      if (!marcar(el, ok)) erros.push(el);
    });
    form.querySelectorAll('[data-obrigatorio-curriculo], [data-obrigatorio-fornecedor]').forEach(function (el) {
      if (!el.hasAttribute('data-obrigatorio-' + t)) marcar(el, true);
    });
    const f = arquivo.files[0];
    let msgArquivo = '';
    if (t === 'curriculo' && !f) msgArquivo = 'Anexe o seu currículo.';
    if (f && f.size > LIMITE) msgArquivo = 'O arquivo passa de 5 MB. Envie uma versão menor.';
    if (f && !/\.(pdf|docx?|jpe?g|png)$/i.test(f.name)) msgArquivo = 'Formato não aceito. Use PDF, Word, JPG ou PNG.';
    if (!marcar(arquivo, !msgArquivo)) erros.push(arquivo);
    return { erros: erros, msgArquivo: msgArquivo };
  }

  function lerArquivo(f) {
    return new Promise(function (ok, falha) {
      if (!f) return ok(null);
      const r = new FileReader();
      r.onload = function () { ok({ nome: f.name, tipo: f.type || 'application/octet-stream', base64: String(r.result).split(',')[1] }); };
      r.onerror = falha;
      r.readAsDataURL(f);
    });
  }

  function mostrarFalha(dados) {
    const assunto = encodeURIComponent((dados.tipo === 'curriculo' ? 'Currículo: ' : 'Fornecedor: ') + (dados.nome || ''));
    erroBox.innerHTML = 'Não conseguimos receber o envio agora. Envie o mesmo conteúdo, com o anexo, para ' +
      '<a href="mailto:' + EMAIL_FALLBACK + '?subject=' + assunto + '">' + EMAIL_FALLBACK + '</a>.';
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (form.website.value) return;
    const v = validar();
    if (v.erros.length) {
      erroBox.textContent = v.msgArquivo || 'Confira os campos destacados. O telefone precisa ter DDD.';
      v.erros[0].focus();
      return;
    }
    erroBox.textContent = '';
    const dados = {};
    new FormData(form).forEach(function (val, chave) { if (chave !== 'arquivo' && chave !== 'website' && String(val).trim()) dados[chave] = String(val).trim(); });
    dados.pagina = location.pathname;
    botao.disabled = true;
    botao.dataset.texto = botao.innerHTML;
    botao.textContent = 'Enviando...';
    try {
      dados.anexo = await lerArquivo(arquivo.files[0]);
      const r = await fetch('/api/trabalhe-conosco', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) });
      if (!r.ok) throw new Error('status ' + r.status);
      track('form_submit', { formulario: 'trabalhe-conosco', tipo: dados.tipo });
      form.classList.add('hidden');
      sucesso.classList.remove('hidden');
      sucesso.setAttribute('tabindex', '-1');
      sucesso.focus();
    } catch (err) {
      mostrarFalha(dados);
    } finally {
      botao.disabled = false;
      botao.innerHTML = botao.dataset.texto;
    }
  });
})();

/* Números que sobem gradualmente quando a seção entra na tela */
(function initContadores() {
  const alvos = document.querySelectorAll('[data-count]');
  if (!alvos.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const fmt = new Intl.NumberFormat('pt-BR');
  const render = function (el, v) { el.textContent = (el.dataset.prefix || '') + fmt.format(v); };
  const animar = function (el) {
    const fim = Number(el.dataset.count);
    const dur = fim > 1 ? 2000 : 900;
    const t0 = performance.now();
    const passo = function (t) {
      const p = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      render(el, Math.round(fim * e));
      if (p < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  };
  const obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (en) {
      if (en.isIntersecting) { animar(en.target); obs.unobserve(en.target); }
    });
  }, { threshold: 0.4 });
  alvos.forEach(function (el) { render(el, 0); obs.observe(el); });
})();

/* Blog: filtro por categoria */
(function initFiltroBlog() {
  const grade = document.getElementById('posts-grid');
  const botoes = document.querySelectorAll('.cat-btn');
  if (!grade || !botoes.length) return;
  const vazio = document.querySelector('[data-sem-resultado]');
  botoes.forEach(function (b) {
    b.setAttribute('aria-pressed', String(b.classList.contains('active')));
    b.addEventListener('click', function () {
      const cat = b.dataset.cat;
      botoes.forEach(function (x) {
        const ativo = x === b;
        x.classList.toggle('active', ativo);
        x.classList.toggle('bg-prime-900', ativo);
        x.classList.toggle('text-white', ativo);
        x.classList.toggle('bg-gray-100', !ativo);
        x.setAttribute('aria-pressed', String(ativo));
      });
      let visiveis = 0;
      grade.querySelectorAll('.post-card').forEach(function (c) {
        const mostra = cat === 'all' || c.dataset.cat === cat;
        c.hidden = !mostra;
        if (mostra) visiveis++;
      });
      if (vazio) vazio.classList.toggle('hidden', visiveis > 0);
    });
  });
})();

/* Carrossel de clientes: anda sozinho sem pausar no hover e pode ser arrastado (mouse e toque) */
(function initCarrosselClientes() {
  const faixas = document.querySelectorAll('.carousel-faixas .carousel-container');
  if (!faixas.length || !window.requestAnimationFrame) return;
  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)');

  faixas.forEach(function (faixa) {
    const trilho = faixa.querySelector('.carousel-track');
    const grupo = trilho && trilho.querySelector('.carousel-group');
    if (!grupo) return;
    faixa.classList.add('is-js');
    faixa.querySelectorAll('img').forEach(function (img) { img.draggable = false; });

    const reversa = trilho.classList.contains('carousel-reverse');
    const velocidade = reversa ? 90 : 75; // px por segundo: o ritmo não muda com a quantidade de logos
    let largura = grupo.offsetWidth;
    let x = reversa ? -largura : 0;
    let arrastando = false, inicioX = 0, inicioPos = 0, ultimoX = 0, ultimoT = 0, inercia = 0;
    let visivel = true, anterior = 0;

    function normaliza() {
      if (largura > 0) x = ((x % largura) - largura) % largura;
    }
    function aplica() { trilho.style.transform = 'translate3d(' + x + 'px,0,0)'; }

    function quadro(t) {
      const dt = anterior ? Math.min((t - anterior) / 1000, 0.05) : 0;
      anterior = t;
      if (!arrastando && visivel) {
        const auto = reduzMovimento.matches ? 0 : velocidade * (reversa ? 1 : -1);
        x += (auto + inercia) * dt;
        inercia *= Math.pow(0.04, dt); // a inércia do arraste some em cerca de 1 segundo
        if (Math.abs(inercia) < 1) inercia = 0;
        normaliza();
        aplica();
      }
      requestAnimationFrame(quadro);
    }

    faixa.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      arrastando = true;
      inercia = 0;
      inicioX = ultimoX = e.clientX;
      inicioPos = x;
      ultimoT = e.timeStamp;
      faixa.setPointerCapture(e.pointerId);
      faixa.classList.add('is-arrastando');
    });
    faixa.addEventListener('pointermove', function (e) {
      if (!arrastando) return;
      const dt = (e.timeStamp - ultimoT) / 1000;
      if (dt > 0) inercia = (e.clientX - ultimoX) / dt;
      ultimoX = e.clientX;
      ultimoT = e.timeStamp;
      x = inicioPos + (e.clientX - inicioX);
      normaliza();
      aplica();
    });
    function solta(e) {
      if (!arrastando) return;
      arrastando = false;
      if (e.timeStamp - ultimoT > 80) inercia = 0; // segurou parado antes de soltar
      inercia = Math.max(-2500, Math.min(2500, inercia));
      faixa.classList.remove('is-arrastando');
    }
    faixa.addEventListener('pointerup', solta);
    faixa.addEventListener('pointercancel', solta);
    faixa.addEventListener('lostpointercapture', solta);

    window.addEventListener('resize', function () {
      largura = grupo.offsetWidth;
      normaliza();
      aplica();
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visivel = es[0].isIntersecting; }).observe(faixa);
    }
    // As imagens são lazy: recalcula a largura quando terminarem de carregar
    faixa.querySelectorAll('img').forEach(function (img) {
      if (!img.complete) img.addEventListener('load', function () { largura = grupo.offsetWidth; }, { once: true });
    });

    aplica();
    requestAnimationFrame(quadro);
  });
})();

/* Fotos da estrutura: carrossel simples com setas e troca automática */
(function initSliders() {
  document.querySelectorAll('[data-slider]').forEach(function (box) {
    const trilho = box.querySelector('[data-slider-trilho]');
    if (!trilho) return;
    const total = trilho.children.length;
    let i = 0, timer = null;
    const ir = function (n) { i = (n + total) % total; trilho.style.transform = 'translateX(-' + (i * 100) + '%)'; };
    const auto = function () { clearInterval(timer); if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) timer = setInterval(function () { ir(i + 1); }, 5000); };
    const ant = box.querySelector('[data-slider-ant]'), prox = box.querySelector('[data-slider-prox]');
    if (ant) ant.addEventListener('click', function () { ir(i - 1); auto(); });
    if (prox) prox.addEventListener('click', function () { ir(i + 1); auto(); });
    auto();
  });
})();

/* Animações leves de entrada: os blocos abaixo da dobra surgem com fade e um leve deslize ao entrar na tela.
   Não mexe no hero nem em nada que já está visível ao carregar (sem piscar e sem atrasar o LCP).
   Sem JS, sem IntersectionObserver ou com "reduzir movimento" ligado, tudo aparece normalmente. */
(function initRevelar() {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const main = document.querySelector('main');
  if (!main) return;

  // blocos de grade primeiro (de fora para dentro), depois títulos e textos soltos
  const SELETORES = [
    '.grid > *', '.servicos-grade > *', '.port-grade > *', '.seg-steps > *', '.seg-faqs > *',
    '.cb-filtro > *', '.cb-promessas li', '.estrutura-grade > *', '.carousel-faixas', '.video-carousel-wrap',
    '.contact-form-card', '.cb-form-card', '.post-content > *', 'section figure', 'article > div > figure', 'aside > div',
    '.section-line', '[class*="h-[1px]"]', 'section h2', 'section h3', 'section h2 ~ p', '.estrutura-endereco'
  ];
  const FORA = '#header, footer, .hero-bg, .seg-hero, .sticky, [role="dialog"], .lead-overlay, .saida-overlay, .serv-overlay, .diag, .hidden';
  const alturaTela = window.innerHeight;
  const marcados = [];

  const marcar = function (el) {
    if (el.hasAttribute('data-revelar') || el.closest(FORA)) return;
    if (el.parentElement && el.parentElement.closest('[data-revelar]')) return;
    if (el.querySelector('[data-revelar]')) return;
    if (!el.getClientRects().length) return;                       // escondido
    if (el.getBoundingClientRect().top < alturaTela * 0.92) return;  // já visível ao carregar
    el.setAttribute('data-revelar', '');
    marcados.push(el);
  };

  SELETORES.forEach(function (sel) {
    try { main.querySelectorAll(sel).forEach(marcar); } catch (e) { /* seletor sem suporte */ }
  });
  // o que sobrou em cada seção (CTAs, parágrafos, cards soltos) entra como bloco inteiro
  main.querySelectorAll('section').forEach(function (sec) {
    let alvo = sec;
    while (alvo.children.length === 1 && alvo.firstElementChild.tagName === 'DIV') alvo = alvo.firstElementChild;
    Array.prototype.forEach.call(alvo.children, marcar);
  });
  if (!marcados.length) return;
  document.documentElement.classList.add('revelar-on');

  const liberar = function (el) {
    el.classList.remove('revelado');
    el.removeAttribute('data-revelar');
    el.style.transitionDelay = '';
  };
  const obs = new IntersectionObserver(function (entradas) {
    const visiveis = entradas.filter(function (en) { return en.isIntersecting; }).map(function (en) { return en.target; });
    visiveis.sort(function (a, b) {
      const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      return (ra.top - rb.top) || (ra.left - rb.left);
    });
    visiveis.forEach(function (el, i) {
      obs.unobserve(el);
      const atraso = Math.min(i, 5) * 80;
      el.style.transitionDelay = atraso + 'ms';
      el.classList.add('revelado');
      // depois da entrada, devolve o elemento ao estilo normal (hover e transições próprias voltam a valer)
      setTimeout(function () { liberar(el); }, atraso + 900);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });
  marcados.forEach(function (el) { obs.observe(el); });
  window.addEventListener('beforeprint', function () { marcados.forEach(liberar); });
})();
