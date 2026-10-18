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

function leadFormFieldsHTML() {
  return `
        <div class="lead-error" data-lead-error role="alert" aria-live="assertive"></div>
        <label class="sr-only" for="lf-nome">Primeiro nome</label>
        <input id="lf-nome" type="text" name="nome" placeholder="Primeiro nome" required autocomplete="given-name">
        <label class="sr-only" for="lf-email">E-mail</label>
        <input id="lf-email" type="email" name="email" placeholder="Qual seu e-mail?" required autocomplete="email">
        <label class="sr-only" for="lf-empresa">Nome da empresa</label>
        <input id="lf-empresa" type="text" name="empresa" placeholder="Qual o nome da sua empresa?" required autocomplete="organization">
        <div class="lead-phone-row">
          <span class="lead-flag" aria-hidden="true">🇧🇷</span>
          <label class="sr-only" for="lf-telefone">Telefone com DDD</label>
          <input id="lf-telefone" type="tel" name="telefone" placeholder="Qual seu telefone?" required data-phone-mask autocomplete="tel" inputmode="tel">
        </div>
        <label class="sr-only" for="lf-faturamento">Faturamento mensal</label>
        <select id="lf-faturamento" name="faturamento" required>
          <option value="" disabled selected>Qual o faturamento mensal da sua empresa?</option>
          <option value="ate-10k">Até R$ 10.000</option>
          <option value="10k-50k">De R$ 10.000 a R$ 50.000</option>
          <option value="50k-100k">De R$ 50.000 a R$ 100.000</option>
          <option value="100k-500k">De R$ 100.000 a R$ 500.000</option>
          <option value="500k-1m">De R$ 500.000 a R$ 1.000.000</option>
          <option value="1m-5m">De R$ 1.000.000 a R$ 5.000.000</option>
          <option value="acima-5m">Acima de R$ 5.000.000</option>
          <option value="nao-faturou">Ainda não faturou</option>
        </select>
        <label class="sr-only" for="lf-segmento">Segmento</label>
        <select id="lf-segmento" name="segmento" required>
          <option value="" disabled selected>Qual o seu segmento?</option>
          <option value="ecommerce">E-commerce</option>
          <option value="servicos">Serviços</option>
          <option value="industria">Indústria</option>
          <option value="varejo">Varejo</option>
          <option value="saude">Saúde e Bem-estar</option>
          <option value="educacao">Educação</option>
          <option value="imobiliario">Imobiliário</option>
          <option value="tecnologia">Tecnologia</option>
          <option value="alimentacao">Alimentação</option>
          <option value="outros">Outros</option>
        </select>
        <button type="submit" class="lead-submit"><i class="fab fa-whatsapp" aria-hidden="true"></i> Enviar pelo WhatsApp</button>`;
}

function leadFormHeaderWaHTML() {
  return `
      <div class="lead-card-header lead-wa-head">
        <i class="fab fa-whatsapp" aria-hidden="true"></i>
        <div>
          <h2 class="lead-card-title" id="lead-title">Fale com a gente no WhatsApp</h2>
          <p class="lead-card-desc">Preencha os dados e abrimos o WhatsApp com a sua mensagem pronta.</p>
        </div>
      </div>`;
}

function leadFormHeaderHTML() {
  return `
      <div class="lead-card-header">
        <span class="lead-eyebrow">Orçamento rápido</span>
        <h2 class="lead-card-title" id="lead-title">Vamos conversar?</h2>
        <p class="lead-card-desc">Preencha os dados e seguimos a conversa pelo WhatsApp.</p>
      </div>`;
}

const FAIXAS_QUALIFICADAS = ['100k-500k', '500k-1m', '1m-5m', 'acima-5m'];
const ROTULOS = { nome: 'Nome', empresa: 'Empresa', email: 'E-mail', telefone: 'Telefone', faturamento: 'Faturamento mensal', segmento: 'Segmento', servico: 'Interesse', area: 'Interesse', mensagem: 'Mensagem' };

function validarLead(form) {
  const erros = [];
  form.querySelectorAll('[required]').forEach(function (el) {
    let ok = !!String(el.value || '').trim();
    if (ok && el.type === 'email') ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
    if (ok && el.name === 'telefone') ok = el.value.replace(/\D/g, '').length >= 10;
    el.classList.toggle('is-invalid', !ok);
    el.setAttribute('aria-invalid', String(!ok));
    if (!ok) erros.push(el);
  });
  return erros;
}

function montarMensagem(form) {
  const linhas = ['Olá! Vim pelo site da Conceito Prime e quero um orçamento.', ''];
  const dados = {};
  Array.prototype.forEach.call(form.elements, function (el) {
    if (!el.name || el.type === 'submit' || el.type === 'hidden' && !el.value) return;
    let valor = String(el.value || '').trim();
    if (!valor) return;
    dados[el.name] = valor;
    if (el.tagName === 'SELECT') valor = el.options[el.selectedIndex].text;
    linhas.push((ROTULOS[el.name] || el.name) + ': ' + valor);
  });
  linhas.push('', 'Origem: site (' + location.pathname + ')');
  const ref = Object.keys(RASTREIO).map(function (k) { return k + '=' + RASTREIO[k]; }).join(' ');
  if (ref) linhas.push('Ref: ' + ref);
  return { texto: linhas.join('\n'), dados: dados };
}

function enviarParaPlanilha(dados) {
  /* Endpoint do Worker (worker.js). Fica inerte enquanto LEAD_WEBHOOK não estiver configurado. */
  try {
    const corpo = JSON.stringify(Object.assign({ pagina: location.pathname, origem: 'site' }, RASTREIO, dados));
    if (navigator.sendBeacon) navigator.sendBeacon('/api/lead', new Blob([corpo], { type: 'application/json' }));
  } catch (e) { /* o lead segue pelo WhatsApp mesmo assim */ }
}

function setupLeadForm(form, onSuccess) {
  const wrap = form.parentElement;
  const success = wrap && wrap.querySelector('[data-lead-success]');
  const erroBox = form.querySelector('[data-lead-error]');
  const phone = form.querySelector('[data-phone-mask]');
  if (phone) maskPhone(phone);
  let iniciou = false;
  form.addEventListener('input', function () {
    if (!iniciou) { iniciou = true; track('form_start', { formulario: form.id || 'inline' }); }
  });
  form.querySelectorAll('select').forEach(function (sel) {
    sel.addEventListener('change', function () { sel.classList.toggle('has-value', !!sel.value); });
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const erros = validarLead(form);
    if (erros.length) {
      if (erroBox) erroBox.textContent = 'Confira os campos destacados: todos são obrigatórios e o telefone precisa ter DDD.';
      erros[0].focus();
      return;
    }
    if (erroBox) erroBox.textContent = '';
    const msg = montarMensagem(form);
    const url = waLink(msg.texto);
    const qualificado = FAIXAS_QUALIFICADAS.indexOf(msg.dados.faturamento) !== -1;
    const evento = { formulario: form.id || 'inline', pagina: location.pathname, faturamento: msg.dados.faturamento || '', segmento: msg.dados.segmento || '', lead_qualificado: qualificado };
    track('form_submit', evento);
    /* Conversão principal do Google Ads: só empresa a partir de R$ 100 mil/mês (gatilho no GTM pelo evento lead_qualificado) */
    if (qualificado) track('lead_qualificado', evento);
    enviarParaPlanilha(msg.dados);
    abrirWhatsApp(url, 'formulario');
    form.style.display = 'none';
    if (success) {
      const link = success.querySelector('[data-wa-fallback]');
      if (link) link.href = url;
      success.classList.add('show');
    }
    if (onSuccess) onSuccess();
  });
}

function sucessoHTML() {
  return `
      <div class="lead-success" data-lead-success aria-live="polite">
        <i class="fas fa-check-circle" aria-hidden="true"></i>
        <p>Pronto! Abrimos o WhatsApp com os seus dados.</p>
        <span>É só enviar a mensagem por lá. Se o WhatsApp não abriu, <a href="#" data-wa-fallback target="_blank" rel="noopener">toque aqui</a>.</span>
      </div>`;
}

function resetLeadForm(form) {
  const wrap = form.parentElement;
  const success = wrap && wrap.querySelector('[data-lead-success]');
  form.style.display = '';
  form.reset();
  if (success) success.classList.remove('show');
  form.querySelectorAll('select').forEach(function (s) { s.classList.remove('has-value'); });
  form.querySelectorAll('.is-invalid').forEach(function (el) { el.classList.remove('is-invalid'); el.removeAttribute('aria-invalid'); });
  const erroBox = form.querySelector('[data-lead-error]');
  if (erroBox) erroBox.textContent = '';
}

/* ========== MODAL DE LEAD ========== */
(function initLeadModal() {
  const overlay = document.createElement('div');
  overlay.id = 'lead-overlay';
  overlay.className = 'lead-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', 'lead-title');

  overlay.innerHTML = `
    <div class="lead-card">
      <button type="button" class="lead-close" id="lead-close" aria-label="Fechar">&times;</button>
      ${leadFormHeaderHTML()}
      ${sucessoHTML()}
      <form class="lead-form" id="lead-form" data-lead-form novalidate>
        ${leadFormFieldsHTML()}
      </form>
    </div>
  `;

  document.body.appendChild(overlay);

  const modalForm = document.getElementById('lead-form');
  let ultimoFoco = null;
  const closeModal = function () {
    if (!overlay.classList.contains('open')) return;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
  };
  setupLeadForm(modalForm, function () { setTimeout(closeModal, 6000); });

  const cabecalho = overlay.querySelector('.lead-card-header');
  const cabPadrao = cabecalho.outerHTML;
  window.openLeadModal = function (modo) {
    ultimoFoco = document.activeElement;
    const wa = modo === 'whatsapp';
    overlay.classList.toggle('lead-overlay--wa', wa);
    overlay.querySelector('.lead-card-header').outerHTML = wa ? leadFormHeaderWaHTML() : cabPadrao;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(function () { const f = modalForm.querySelector('input'); if (f) f.focus(); }, 50);
  };

  document.getElementById('lead-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  /* CTAs de orçamento abrem o formulário (o envio termina no WhatsApp) */
  document.addEventListener('click', function (e) {
    const a = e.target.closest('a, button');
    if (!a) return;
    if (a.closest('#wa-float') || a.closest('#lead-overlay')) return;
    const ehCta = a.classList.contains('btn-wa') || a.classList.contains('btn-luxury') ||
      a.classList.contains('btn-brand') || a.classList.contains('contact-submit');
    if (!ehCta) return;
    if (a.tagName === 'BUTTON' && a.type === 'submit' && a.form) return;
    e.preventDefault();
    track('cta_click', { posicao: a.dataset.cta || (a.closest('section, header, footer') || {}).id || 'cta', texto: a.textContent.trim().slice(0, 60) });
    resetLeadForm(modalForm);
    openLeadModal();
  });
})();

/* Formulários inline nas páginas internas */
(function initInlineLeadForms() {
  document.querySelectorAll('[data-lead-form]').forEach(function (form) {
    if (form.id === 'lead-form') return;
    if (!form.querySelector('[data-lead-error]')) {
      const box = document.createElement('div');
      box.className = 'lead-error'; box.setAttribute('data-lead-error', ''); box.setAttribute('role', 'alert');
      form.insertBefore(box, form.firstChild);
    }
    const wrap = form.parentElement;
    const oldSuccess = wrap && wrap.querySelector('[data-lead-success]');
    if (oldSuccess && !oldSuccess.querySelector('[data-wa-fallback]')) oldSuccess.outerHTML = sucessoHTML();
    if (!oldSuccess) form.insertAdjacentHTML('beforebegin', sucessoHTML());
    setupLeadForm(form);
  });
})();

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
  /* Páginas da campanha (body data-contato="formulario"): o formulário é o único ponto de contato.
     O botão continua com a cara do WhatsApp, mas abre o formulário e só depois redireciona com a mensagem pronta. */
  if (document.body.dataset.contato === 'formulario') {
    const botao = document.createElement('div');
    botao.id = 'wa-float';
    botao.className = 'wa-float';
    botao.innerHTML = '<button type="button" class="wa-float-btn" id="wa-float-btn" aria-label="Falar no WhatsApp"><i class="fab fa-whatsapp" aria-hidden="true"></i></button>';
    document.body.appendChild(botao);
    document.getElementById('wa-float-btn').addEventListener('click', function () {
      track('cta_click', { posicao: 'whatsapp-flutuante', texto: 'WhatsApp' });
      const f = document.getElementById('lead-form');
      if (f) resetLeadForm(f);
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
        <strong>Currículos e propostas de fornecedores</strong> não são atendidos pelo WhatsApp: envie pelo formulário <a href="/trabalhe-conosco/">Trabalhe Conosco</a>.
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
    a.addEventListener('click', function () { track('whatsapp_open', { posicao: a.dataset.cta }); });
  });
  btn.addEventListener('click', function () {
    const abrir = menu.classList.contains('hidden');
    definir(abrir);
    if (abrir) track('cta_click', { posicao: 'flutuante', texto: 'Fale Conosco' });
  });
  document.addEventListener('click', function (e) { if (!widget.contains(e.target)) definir(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.classList.contains('hidden')) { definir(false); btn.focus(); } });
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
    const duracao = reversa ? 45 : 55; // segundos para uma volta completa, como no CSS
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
        const auto = reduzMovimento.matches ? 0 : (largura / duracao) * (reversa ? 1 : -1);
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
