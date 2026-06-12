/* Conceito Prime: scripts compartilhados */

function leadFormFieldsHTML() {
  return `
        <input type="text"  name="nome"     placeholder="Primeiro nome"               required autocomplete="given-name">
        <input type="email" name="email"    placeholder="Qual seu e-mail?"            required autocomplete="email">
        <input type="text"  name="empresa"  placeholder="Qual o nome da sua empresa?" required autocomplete="organization">
        <div class="lead-phone-row">
          <span class="lead-flag" aria-hidden="true">🇧🇷</span>
          <input type="tel" name="telefone" placeholder="Qual seu telefone?" required data-phone-mask autocomplete="tel">
        </div>
        <select name="faturamento" required>
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
        <select name="segmento" required>
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
        <button type="submit" class="lead-submit">Receber mais informações <i class="fas fa-arrow-right" aria-hidden="true"></i></button>`;
}

function leadFormHeaderHTML() {
  return `
      <div class="lead-card-header">
        <span class="lead-eyebrow">Orçamento rápido</span>
        <h2 class="lead-card-title">Vamos conversar?</h2>
        <p class="lead-card-desc">Preencha os dados e nossa equipe retorna em breve.</p>
      </div>`;
}

function setupLeadForm(form, onSuccess) {
  const wrap = form.parentElement;
  const success = wrap?.querySelector('[data-lead-success]');
  const phone = form.querySelector('[data-phone-mask]');
  if (phone) maskPhone(phone);
  form.querySelectorAll('select').forEach((sel) => {
    sel.addEventListener('change', () => sel.classList.toggle('has-value', !!sel.value));
  });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    form.style.display = 'none';
    success?.classList.add('show');
    if (onSuccess) onSuccess();
  });
}

function resetLeadForm(form) {
  const wrap = form.parentElement;
  const success = wrap?.querySelector('[data-lead-success]');
  form.style.display = '';
  form.reset();
  success?.classList.remove('show');
  form.querySelectorAll('select').forEach((s) => s.classList.remove('has-value'));
}

/* ========== MODAL DE LEAD ========== */
(function initLeadModal() {
  const overlay = document.createElement('div');
  overlay.id = 'lead-overlay';
  overlay.className = 'lead-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Formulário de contato');

  overlay.innerHTML = `
    <div class="lead-card">
      <button class="lead-close" id="lead-close" aria-label="Fechar">&times;</button>
      ${leadFormHeaderHTML()}
      <div class="lead-success" data-lead-success aria-live="polite">
        <i class="fas fa-check-circle" aria-hidden="true"></i>
        <p>Obrigado! Recebemos seu contato.</p>
        <span>Em breve nossa equipe entrará em contato.</span>
      </div>
      <form class="lead-form" id="lead-form" data-lead-form novalidate>
        ${leadFormFieldsHTML()}
      </form>
    </div>
  `;

  document.body.appendChild(overlay);

  const modalForm = document.getElementById('lead-form');
  const closeModal = () => {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  };
  setupLeadForm(modalForm, () => setTimeout(closeModal, 3000));

  window.openLeadModal = () => {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  document.getElementById('lead-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  /* ─── intercepta todos os CTAs do site ─── */
  document.addEventListener('click', e => {
    const a = e.target.closest('a, button');
    if (!a) return;
    if (a.closest('#wa-float')) return; /* preserva float WA */

    const href = a.getAttribute('href') || '';
    const isWABtn  = a.classList.contains('btn-wa');
    const isLuxury = a.classList.contains('btn-luxury');
    const isBrand  = a.classList.contains('btn-brand');
    const isContato = href === '/contato/' || href.endsWith('/contato/');
    const isSubmit = a.classList.contains('contact-submit');

    if (isWABtn || isLuxury || isBrand || isContato || isSubmit) {
      e.preventDefault();
      resetLeadForm(modalForm);
      openLeadModal();
    }
  });
})();

/* Formulários inline nas páginas internas */
(function initInlineLeadForms() {
  document.querySelectorAll('[data-lead-form]').forEach((form) => {
    if (form.id === 'lead-form') return;
    setupLeadForm(form);
  });
})();

function maskPhone(input) {
  if (input.dataset.masked) return;
  input.dataset.masked = '1';
  input.addEventListener('input', (e) => {
    let v = e.target.value.replace(/\D/g, '').slice(0, 11);
    if (v.length > 6) {
      v = v.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
    } else if (v.length > 2) {
      v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else if (v.length > 0) {
      v = v.replace(/^(\d*)/, '($1');
    }
    e.target.value = v.trim();
  });
}

document.querySelectorAll('[data-phone-mask]').forEach(maskPhone);

/* Botão flutuante WhatsApp: Comercial / Administrativo */
(function initWhatsAppFloat() {
  const WA = {
    comercial: 'https://wa.me/554130574764?text=' + encodeURIComponent('Olá! Gostaria de falar com o Comercial.'),
    administrativo: 'https://wa.me/554130574764?text=' + encodeURIComponent('Olá! Gostaria de falar com o Administrativo.')
  };

  const widget = document.createElement('div');
  widget.id = 'wa-float';
  widget.className = 'wa-float';
  widget.innerHTML = `
    <div class="wa-float-menu hidden" id="wa-float-menu" role="menu" aria-label="Opções de WhatsApp">
      <a href="${WA.comercial}" target="_blank" rel="noopener" class="wa-float-option" role="menuitem">
        Comercial
      </a>
      <a href="${WA.administrativo}" target="_blank" rel="noopener" class="wa-float-option" role="menuitem">
        Administrativo
      </a>
    </div>
    <button type="button" class="wa-float-btn" id="wa-float-btn" aria-label="Abrir opções de WhatsApp" aria-expanded="false" aria-haspopup="true">
      <i class="fab fa-whatsapp" aria-hidden="true"></i>
    </button>
  `;
  document.body.appendChild(widget);

  const btn = document.getElementById('wa-float-btn');
  const menu = document.getElementById('wa-float-menu');
  btn.addEventListener('click', () => {
    const open = menu.classList.toggle('hidden');
    btn.setAttribute('aria-expanded', String(!open));
  });
  document.addEventListener('click', (e) => {
    if (!widget.contains(e.target)) {
      menu.classList.add('hidden');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
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
