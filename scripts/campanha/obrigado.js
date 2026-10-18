/* Páginas de obrigado da campanha: personaliza com o lead enviado e dispara as conversões do Google Ads
   uma única vez por envio (recarregar a página não conta de novo; visita direta sem envio não conta). */
(function () {
  var lead = null;
  try { lead = JSON.parse(sessionStorage.getItem('cp_lead_b2b') || 'null'); } catch (e) { lead = null; }
  var nome = document.querySelector('[data-lead-nome]');
  if (lead && lead.nome && nome) nome.textContent = ', ' + lead.nome.split(' ')[0];

  var wa = document.querySelectorAll('[data-wa-msg]');
  wa.forEach(function (a) {
    var msg = a.getAttribute('data-wa-msg');
    if (lead) msg += ' Sou ' + (lead.nome || '') + (lead.empresa ? ', da ' + lead.empresa : '') + '.';
    a.href = 'https://wa.me/' + a.getAttribute('data-wa-numero') + '?text=' + encodeURIComponent(msg);
    a.addEventListener('click', function () { (window.dataLayer = window.dataLayer || []).push({ event: 'whatsapp_open', posicao: a.dataset.cta || 'obrigado' }); });
  });

  if (!lead) return;
  var chave = 'cp_conv_' + lead.t + '_' + location.pathname;
  try { if (sessionStorage.getItem(chave)) return; sessionStorage.setItem(chave, '1'); } catch (e) { /* segue */ }

  /* GTM: gatilho "Evento personalizado" conversao_lead_b2b. tipo = qualificado (Lead Qualificado B2B) ou todos (Lead B2B Todos).
     Na página qualificada saem os dois eventos, porque "Lead B2B Todos" conta todo lead enviado. */
  var tipos = (document.body.getAttribute('data-tipos-conversao') || '').split(',').filter(Boolean);
  window.dataLayer = window.dataLayer || [];
  tipos.forEach(function (tipo) {
    window.dataLayer.push({ event: 'conversao_lead_b2b', tipo: tipo, lead_id: String(lead.t), faturamento: lead.faturamento, pagina_origem: lead.pagina });
  });

  /* Tag do Google direta (só se GOOGLE_TAG_ID estiver preenchido no gerador, sem GTM) */
  var conversoes = (document.body.getAttribute('data-conversoes') || '').split(',').filter(Boolean);
  if (!conversoes.length || typeof window.gtag !== 'function') return;
  conversoes.forEach(function (envio) { window.gtag('event', 'conversion', { send_to: envio, transaction_id: String(lead.t) }); });
})();
