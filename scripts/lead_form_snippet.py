"""HTML do formulário de lead (mesmo do popup). Usado nas páginas internas."""

LEAD_FORM_FIELDS = """
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

        <button type="submit" class="lead-submit">Receber mais informações <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
"""


def render_lead_header(title="Vamos conversar?", subtitle="Preencha os dados e nossa equipe retorna em breve.", servico="", title_id=""):
    servico_line = f'<p class="lead-card-desc">Interesse em <strong>{servico}</strong></p>' if servico else f'<p class="lead-card-desc">{subtitle}</p>'
    id_attr = f' id="{title_id}"' if title_id else ""
    return f"""
      <div class="lead-card-header">
        <span class="lead-eyebrow">Orçamento rápido</span>
        <h2 class="lead-card-title"{id_attr}>{title}</h2>
        {servico_line}
      </div>"""


def render_lead_form_block(hidden_servico="", form_id="", aria_label="Formulário de contato"):
    hidden = f'<input type="hidden" name="servico" value="{hidden_servico}">' if hidden_servico else ""
    id_attr = f' id="{form_id}"' if form_id else ""
    return f"""
      <div class="lead-success" data-lead-success aria-live="polite">
        <i class="fas fa-check-circle" aria-hidden="true"></i>
        <p>Obrigado! Recebemos seu contato.</p>
        <span>Em breve nossa equipe entrará em contato.</span>
      </div>
      <form class="lead-form" data-lead-form{id_attr} novalidate aria-label="{aria_label}">
        {hidden}
{LEAD_FORM_FIELDS}
      </form>"""
