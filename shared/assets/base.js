/* Base das LPs Black Novembro da Conceito Prime. Sem dependências. */
(function () {
  var C = window.LP || {};
  var dl = (window.dataLayer = window.dataLayer || []);
  var reduz = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Destino dos CTAs: link do grupo; enquanto ele não existir, WhatsApp do comercial com a mensagem pronta
  var temGrupo = /^https?:\/\//.test(C.grupo || "");
  var destino = temGrupo
    ? C.grupo
    : "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(C.mensagem || "");
  document.querySelectorAll("[data-cta]").forEach(function (a) {
    a.href = a.hasAttribute("data-wa") ? "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(C.mensagem || "") : destino;
    a.target = "_blank";
    a.rel = "noopener";
    a.addEventListener("click", function () {
      dl.push({ event: "grupo_click", pagina: C.pagina, posicao: a.getAttribute("data-cta"), destino: temGrupo ? "grupo" : "whatsapp" });
      if (window.fbq) window.fbq("track", "Lead", { content_name: C.pagina });
    });
  });

  // Revelação ao rolar (uma vez por elemento)
  var rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && !reduz) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add("on"); });

  // Mapas só carregam no clique (o embed do Google pesa mais que a página inteira)
  document.querySelectorAll("[data-mapa]").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = b.getAttribute("data-mapa");
      f.title = b.getAttribute("aria-label");
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      b.replaceWith(f);
    });
  });

  // Contagem regressiva: só aparece quando a data e o horário do evento estiverem definidos (LP.evento em ISO)
  var alvo = C.evento ? new Date(C.evento) : null;
  var relogios = document.querySelectorAll("[data-contagem]");
  if (alvo && !isNaN(alvo) && relogios.length) {
    var dois = function (n) { return (n < 10 ? "0" : "") + n; };
    var tick = function () {
      var s = Math.max(0, Math.floor((alvo - Date.now()) / 1000));
      var d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
      relogios.forEach(function (r) {
        r.hidden = false;
        r.querySelector("[data-d]").textContent = dois(d);
        r.querySelector("[data-h]").textContent = dois(h);
        r.querySelector("[data-m]").textContent = dois(m);
        r.querySelector("[data-s]").textContent = dois(x);
        if (s === 0) r.classList.add("fim");
      });
    };
    tick();
    setInterval(tick, 1000);
  }

  // Rolagem: 75% da página
  var marcou = false;
  window.addEventListener("scroll", function () {
    if (marcou) return;
    var h = document.documentElement;
    if ((h.scrollTop + innerHeight) / h.scrollHeight > 0.75) { marcou = true; dl.push({ event: "scroll_75", pagina: C.pagina }); }
  }, { passive: true });
})();
