// Conceito Prime: Worker que serve o site estático (dist/) e recebe POST /api/lead.
//
// Leads para planilha do Google (opcional):
//   1. Na planilha: Extensões > Apps Script, cole a função abaixo e publique como
//      "App da Web" (executar como você, acesso: qualquer pessoa). Copie a URL /exec.
//
//      function doPost(e) {
//        const d = JSON.parse(e.postData.contents);
//        const aba = SpreadsheetApp.getActive().getSheetByName('Leads') || SpreadsheetApp.getActive().insertSheet('Leads');
//        if (aba.getLastRow() === 0) aba.appendRow(['data', 'nome', 'empresa', 'email', 'telefone', 'faturamento', 'segmento', 'servico', 'mensagem', 'pagina', 'gclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']);
//        aba.appendRow([new Date(), d.nome, d.empresa, d.email, d.telefone, d.faturamento, d.segmento, d.servico, d.mensagem, d.pagina, d.gclid, d.utm_source, d.utm_medium, d.utm_campaign, d.utm_term, d.utm_content]);
//        return ContentService.createTextOutput('ok');
//      }
//
//   2. No Cloudflare (Worker conceitop > Configurações > Variáveis): crie o segredo LEAD_WEBHOOK com a URL /exec.
//   Sem essa variável o endpoint responde 204 e não guarda nada; o lead segue normalmente pelo WhatsApp.

const CAMPOS = ['nome', 'empresa', 'email', 'telefone', 'faturamento', 'segmento', 'servico', 'area', 'mensagem', 'pagina', 'origem',
  'gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/lead') {
      if (request.method !== 'POST') return new Response(null, { status: 405, headers: { Allow: 'POST' } });
      return receberLead(request, env, ctx);
    }
    return env.ASSETS.fetch(request);
  },
};

async function receberLead(request, env, ctx) {
  let corpo;
  try {
    const txt = await request.text();
    if (txt.length > 8000) return new Response(null, { status: 413 });
    corpo = JSON.parse(txt);
  } catch {
    return new Response(null, { status: 400 });
  }
  if (corpo.company || corpo.website) return new Response(null, { status: 204 }); // honeypot
  if (!env.LEAD_WEBHOOK) return new Response(null, { status: 204 });

  const lead = {};
  for (const k of CAMPOS) if (corpo[k] != null) lead[k] = String(corpo[k]).slice(0, k === 'mensagem' ? 2000 : 200);

  ctx.waitUntil(
    fetch(env.LEAD_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lead),
      redirect: 'follow',
    }).catch(() => {})
  );
  return new Response(null, { status: 204 });
}
