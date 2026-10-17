/* Conceito Prime: scripts compartilhados */

/* ========== CONTATO: número único do WhatsApp ==========
   PENDENTE: confirmar o número. O site antigo usa (41) 99990-4764; aqui está o fixo (41) 3057-4764,
   definido no briefing de junho. Trocar só esta constante. */
const WA_NUMERO = '554130574764';

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

function leadFormHeaderHTML() {
  return `
      <div class="lead-card-header">
        <span class="lead-eyebrow">Orçamento rápido</span>
        <h2 class="lead-card-title" id="lead-title">Vamos conversar?</h2>
        <p class="lead-card-desc">Preencha os dados e seguimos a conversa pelo WhatsApp.</p>
      </div>`;
}

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
    track('form_submit', { formulario: form.id || 'inline', faturamento: msg.dados.faturamento || '', segmento: msg.dados.segmento || '' });
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

  window.openLeadModal = function () {
    ultimoFoco = document.activeElement;
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

/* Botão flutuante WhatsApp: Comercial / Administrativo */
(function initWhatsAppFloat() {
  const WA = {
    comercial: waLink('Olá! Gostaria de falar com o Comercial.'),
    administrativo: waLink('Olá! Gostaria de falar com o Administrativo.')
  };

  const widget = document.createElement('div');
  widget.id = 'wa-float';
  widget.className = 'wa-float';
  widget.innerHTML = `
    <div class="wa-float-menu hidden" id="wa-float-menu" aria-label="Opções de WhatsApp">
      <a href="${WA.comercial}" target="_blank" rel="noopener" class="wa-float-option" data-cta="flutuante-comercial">
        <i class="fab fa-whatsapp" aria-hidden="true"></i> Comercial
      </a>
      <a href="${WA.administrativo}" target="_blank" rel="noopener" class="wa-float-option" data-cta="flutuante-administrativo">
        <i class="fab fa-whatsapp" aria-hidden="true"></i> Administrativo
      </a>
    </div>
    <button type="button" class="wa-float-btn" id="wa-float-btn" aria-label="Falar no WhatsApp" aria-expanded="false" aria-controls="wa-float-menu">
      <i class="fab fa-whatsapp" aria-hidden="true"></i>
    </button>
  `;
  document.body.appendChild(widget);

  const btn = document.getElementById('wa-float-btn');
  const menu = document.getElementById('wa-float-menu');
  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { track('whatsapp_open', { posicao: a.dataset.cta }); });
  });
  btn.addEventListener('click', function () {
    const fechado = menu.classList.toggle('hidden');
    btn.setAttribute('aria-expanded', String(!fechado));
  });
  document.addEventListener('click', function (e) {
    if (!widget.contains(e.target)) {
      menu.classList.add('hidden');
      btn.setAttribute('aria-expanded', 'false');
    }
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

  const slideWidth = () => viewport.clientWidth;

  const go = (n) => {
    const total = track.children.length;
    if (!total) return;
    idx = (n + total) % total;
    track.style.transform = `translateX(-${idx * slideWidth()}px)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
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

/* Carrossel depoimentos em texto */
(function initQuotesCarousel() {
  const track = document.getElementById('quotes-track');
  const viewport = track?.parentElement;
  const dots = document.querySelectorAll('.quotes-dots .quotes-dot');
  if (!track || !viewport || !dots.length) return;

  let idx = 0;
  let timer;
  const slideWidth = () => viewport.clientWidth;

  const go = (n) => {
    const total = track.children.length;
    if (!total) return;
    idx = (n + total) % total;
    track.style.transform = `translateX(-${idx * slideWidth()}px)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
  };

  const start = () => { timer = setInterval(() => go(idx + 1), 7000); };
  const stop = () => clearInterval(timer);

  dots.forEach((d, i) => d.addEventListener('click', () => { stop(); go(i); start(); }));
  const wrap = track.closest('.quotes-carousel');
  wrap?.addEventListener('mouseenter', stop);
  wrap?.addEventListener('mouseleave', start);
  window.addEventListener('resize', () => go(idx));
  go(0);
  start();
})();
