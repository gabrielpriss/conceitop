/* Formulário próprio das páginas /b2b e /industrial (embutido na página; não usa o formulário global).
   Envia para /api/lead-b2b (worker.js) e redireciona: faturamento a partir de R$ 100 mil vai para
   /obrigado-qualificado/, o resto para /obrigado/. Nada de WhatsApp aqui. */
(function () {
  var QUALIFICADAS = ['100k-500k', '500k-1m', '1m-5m', 'acima-5m'];
  var GRATUITOS = /@(gmail|hotmail|outlook|live|yahoo|icloud|bol|uol|terra|ig)\./i;
  var CHAVES = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  window.dataLayer = window.dataLayer || [];

  /* gclid e UTMs: lidos da URL e guardados na sessão, para não se perderem se a pessoa navegar antes de enviar */
  var rastreio = {};
  try { rastreio = JSON.parse(sessionStorage.getItem('cp_campanha_rastreio') || '{}'); } catch (e) { rastreio = {}; }
  var params = new URLSearchParams(location.search);
  CHAVES.forEach(function (k) { var v = params.get(k); if (v) rastreio[k] = v.slice(0, 200); });
  try { sessionStorage.setItem('cp_campanha_rastreio', JSON.stringify(rastreio)); } catch (e) { /* sessão indisponível */ }

  var form = document.getElementById('cb-form');
  if (!form) return;
  CHAVES.forEach(function (k) { var el = form.querySelector('[name="' + k + '"]'); if (el && rastreio[k]) el.value = rastreio[k]; });

  var tel = form.querySelector('[name="telefone"]');
  tel.addEventListener('input', function () {
    var d = tel.value.replace(/\D/g, '').slice(0, 11);
    tel.value = d.length > 6 ? '(' + d.slice(0, 2) + ') ' + d.slice(2, d.length - 4) + '-' + d.slice(-4) : d.length > 2 ? '(' + d.slice(0, 2) + ') ' + d.slice(2) : d;
  });

  var iniciou = false;
  form.addEventListener('input', function () {
    if (!iniciou) { iniciou = true; window.dataLayer.push({ event: 'form_start', formulario: 'lp-' + form.dataset.pagina }); }
  });

  function campo(el) { return el.closest('.cb-campo'); }
  function validar() {
    var erros = [];
    form.querySelectorAll('[required]').forEach(function (el) {
      var ok = String(el.value || '').trim() !== '';
      if (ok && el.type === 'email') ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
      if (ok && el.name === 'telefone') ok = el.value.replace(/\D/g, '').length >= 10;
      campo(el).classList.toggle('cb-invalido', !ok);
      el.setAttribute('aria-invalid', String(!ok));
      if (!ok) erros.push(el);
    });
    var grupo = form.querySelector('[data-obrigatorio-grupo]');
    var marcado = grupo.querySelectorAll('input:checked').length > 0;
    campo(grupo).classList.toggle('cb-invalido', !marcado);
    if (!marcado) erros.push(grupo.querySelector('input'));
    return erros;
  }

  var erroBox = form.querySelector('.cb-erro');
  var botao = form.querySelector('.cb-enviar');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var erros = validar();
    if (erros.length) { erroBox.textContent = 'Confira os campos destacados. Só o site da empresa é opcional.'; erros[0].focus(); return; }
    erroBox.textContent = '';

    var dados = {};
    new FormData(form).forEach(function (v, k) {
      v = String(v).trim();
      if (!v) return;
      dados[k] = dados[k] ? dados[k] + ', ' + v : v;
    });
    var qualificado = QUALIFICADAS.indexOf(dados.faturamento) !== -1;
    dados.lead_qualificado = qualificado ? 'sim' : 'nao';
    dados.email_gratuito = GRATUITOS.test(dados.email || '') ? 'sim' : 'nao';
    dados.origem = 'campanha-google-ads';

    botao.disabled = true;
    botao.textContent = 'Enviando...';
    var controle = window.AbortController ? new AbortController() : null;
    var limite = setTimeout(function () { if (controle) controle.abort(); }, 8000);

    fetch('/api/lead-b2b', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados),
      signal: controle ? controle.signal : undefined
    }).then(function (r) {
      clearTimeout(limite);
      if (!r.ok) throw new Error('status ' + r.status);
      window.dataLayer.push({ event: 'lead_b2b', lead_qualificado: qualificado, faturamento: dados.faturamento, segmento: dados.segmento, pagina: dados.pagina });
      try {
        sessionStorage.setItem('cp_lead_b2b', JSON.stringify({ nome: dados.nome, empresa: dados.empresa, faturamento: dados.faturamento, qualificado: qualificado, pagina: dados.pagina, t: Date.now() }));
      } catch (err) { /* segue sem personalizar a página de obrigado */ }
      setTimeout(function () { location.href = qualificado ? '/obrigado-qualificado/' : '/obrigado/'; }, 250);
    }).catch(function () {
      clearTimeout(limite);
      botao.disabled = false;
      botao.innerHTML = '<i class="fas fa-paper-plane" aria-hidden="true"></i> Solicitar diagnóstico';
      erroBox.textContent = 'Não conseguimos enviar agora. Tente de novo em alguns instantes ou escreva para contato@conceitop.com.br.';
    });
  });

  /* Botões "Solicitar diagnóstico": rolam até o formulário e põem o foco no primeiro campo */
  document.querySelectorAll('a[href="#orcamento"]').forEach(function (a) {
    a.addEventListener('click', function () {
      window.dataLayer.push({ event: 'cta_click', posicao: a.dataset.cta || 'lp', texto: 'Solicitar diagnóstico' });
      setTimeout(function () { var f = form.querySelector('input:not([type=hidden])'); if (f) f.focus({ preventScroll: true }); }, 600);
    });
  });
})();
