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
    if (url.pathname === '/api/trabalhe-conosco') {
      if (request.method !== 'POST') return new Response(null, { status: 405, headers: { Allow: 'POST' } });
      return receberTrabalheConosco(request, env);
    }
    if (url.pathname === '/api/lead-b2b') {
      if (request.method !== 'POST') return new Response(null, { status: 405, headers: { Allow: 'POST' } });
      return receberLeadB2B(request, env);
    }
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

// Trabalhe Conosco: currículos e fornecedores, com anexo em base64 (até 5 MB).
// Segredo TRABALHE_WEBHOOK = URL /exec de um Apps Script como este, que salva o anexo no Drive e registra na planilha:
//
//   const PASTA_ID = 'ID_DA_PASTA_NO_DRIVE';
//   function doPost(e) {
//     const d = JSON.parse(e.postData.contents);
//     let link = '';
//     if (d.anexo && d.anexo.base64) {
//       const blob = Utilities.newBlob(Utilities.base64Decode(d.anexo.base64), d.anexo.tipo, d.anexo.nome);
//       link = DriveApp.getFolderById(PASTA_ID).createFile(blob).getUrl();
//     }
//     const aba = SpreadsheetApp.getActive().getSheetByName('Trabalhe Conosco') || SpreadsheetApp.getActive().insertSheet('Trabalhe Conosco');
//     if (aba.getLastRow() === 0) aba.appendRow(['data', 'tipo', 'nome', 'email', 'telefone', 'cidade', 'area', 'link', 'empresa', 'oferta', 'site', 'mensagem', 'anexo']);
//     aba.appendRow([new Date(), d.tipo, d.nome, d.email, d.telefone, d.cidade, d.area, d.link, d.empresa, d.oferta, d.site, d.mensagem, link]);
//     return ContentService.createTextOutput('ok');
//   }
//
// Sem o segredo, responde 503 e a página orienta a pessoa a enviar por e-mail (nada se perde em silêncio).
const CAMPOS_TC = ['tipo', 'nome', 'email', 'telefone', 'cidade', 'area', 'link', 'empresa', 'oferta', 'site', 'mensagem', 'pagina'];
const ANEXO_OK = /\.(pdf|docx?|jpe?g|png)$/i;

async function receberTrabalheConosco(request, env) {
  if (!env.TRABALHE_WEBHOOK) return new Response(null, { status: 503 });
  const tamanho = Number(request.headers.get('content-length') || 0);
  if (tamanho > 7.5 * 1024 * 1024) return new Response(null, { status: 413 });
  let d;
  try { d = JSON.parse(await request.text()); } catch { return new Response(null, { status: 400 }); }
  if (d.website || d.company) return new Response(null, { status: 204 });
  if (!d.nome || !d.email || !d.telefone || !['curriculo', 'fornecedor'].includes(d.tipo)) return new Response(null, { status: 422 });

  const envio = {};
  for (const k of CAMPOS_TC) if (d[k] != null) envio[k] = String(d[k]).slice(0, k === 'mensagem' ? 3000 : 300);
  if (d.anexo && d.anexo.base64) {
    if (!ANEXO_OK.test(d.anexo.nome || '') || d.anexo.base64.length > 7 * 1024 * 1024) return new Response(null, { status: 415 });
    envio.anexo = { nome: String(d.anexo.nome).slice(0, 150), tipo: String(d.anexo.tipo || '').slice(0, 100), base64: d.anexo.base64 };
  }
  try {
    const r = await fetch(env.TRABALHE_WEBHOOK, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(envio), redirect: 'follow',
    });
    if (!r.ok) return new Response(null, { status: 502 });
  } catch {
    return new Response(null, { status: 502 });
  }
  return new Response(null, { status: 204 });
}

/* Leads das páginas da campanha (/b2b e /industrial). Rota própria: não muda o /api/lead das outras páginas.
   Envia para o segredo LEAD_B2B_WEBHOOK (ou LEAD_WEBHOOK, se o B2B não existir) e só responde 204 quando o
   webhook aceitou o lead. Sem webhook configurado responde 503 e a página mostra erro, para nenhum lead se perder
   em silêncio. O Apps Script de leads (topo deste arquivo) grava as colunas novas sem mudança: cada chave vira coluna. */
const CAMPOS_B2B = ['nome', 'empresa', 'telefone', 'segmento', 'faturamento', 'servico', 'canal',
  'pagina', 'lead_qualificado', 'origem', 'gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign',
  'utm_term', 'utm_content'];

async function receberLeadB2B(request, env) {
  let corpo;
  try {
    const txt = await request.text();
    if (txt.length > 8000) return new Response(null, { status: 413 });
    corpo = JSON.parse(txt);
  } catch {
    return new Response(null, { status: 400 });
  }
  if (corpo.hp) return new Response(null, { status: 204 }); // honeypot
  if (!corpo.nome || !corpo.telefone || !corpo.faturamento) return new Response(null, { status: 422 });
  const destino = env.LEAD_B2B_WEBHOOK || env.LEAD_WEBHOOK;
  if (!destino) return new Response(null, { status: 503 });

  const lead = { recebido_em: new Date().toISOString() };
  for (const k of CAMPOS_B2B) if (corpo[k] != null) lead[k] = String(corpo[k]).slice(0, 300);
  try {
    const r = await fetch(destino, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lead),
      redirect: 'follow',
      signal: AbortSignal.timeout(7000),
    });
    if (!r.ok) return new Response(null, { status: 502 });
  } catch {
    return new Response(null, { status: 502 });
  }
  return new Response(null, { status: 204 });
}
