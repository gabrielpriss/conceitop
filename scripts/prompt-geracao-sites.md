# Prompt padrão: geração de sites e landing pages

Use este documento como base em **todo** projeto novo. Cole no início do prompt da IA junto com o briefing do cliente.

---

## Briefing obrigatório (preencher antes de gerar)

| Campo | Exemplo |
|-------|---------|
| Nome da empresa | Conceito Prime |
| Segmento | Agência de marketing digital |
| Cidade/UF | Curitiba, PR |
| WhatsApp (somente números) | 554130574764 |
| Domínio | conceitop.com.br |
| Fonte principal | Cairo (ou definir conforme segmento) |
| Google Meu Negócio | Nome exato do perfil no Google |

---

## 1. Google Maps (vincular ao Google Meu Negócio)

**Sempre** usar o **nome da empresa** na query do mapa, não apenas o endereço. Isso vincula ao perfil do Google Meu Negócio.

```html
<!-- Embed (iframe) -->
<iframe
  src="https://maps.google.com/maps?q=NOME+DA+EMPRESA,+Cidade,+UF&hl=pt-BR&z=14&output=embed"
  title="Localização NOME DA EMPRESA"
  loading="lazy"
  referrerpolicy="no-referrer-when-downgrade"
  allowfullscreen>
</iframe>

<!-- Link externo -->
<a href="https://www.google.com/maps/search/?api=1&query=NOME+DA+EMPRESA+Cidade+UF" target="_blank" rel="noopener">
  Ver no Google Maps
</a>
```

**Zoom padrão: `z=14`** (mostra o endereço + bairros próximos). Evitar `z=16` ou superior (muito próximo, usuário se perde). Evitar `z=11` ou inferior (cidade inteira, pouco útil).

**Layout da seção contato (referência visual):**
- Fundo amarelo da marca
- Barra vertical escura à esquerda com ícones de redes sociais
- Card branco do formulário **sobreposto** ao mapa (z-index maior, margem negativa)
- Mapa em escala de cinza (`filter: grayscale`) ocupando o lado direito
- O embed do Google exibe automaticamente o card do GMB (nome, endereço, estrelas)
- Campos: Nome, Telefone, E-mail, select de área, Mensagem
- Botão full-width escuro: `ENVIAR SOLICITAÇÃO →`
- Classes CSS: `.contact-section`, `.contact-layered`, `.contact-social-rail`, `.contact-form-card`, `.contact-map-wrap`

---

## 2. CTAs (padrão de conversão)

Evitar textos criativos ou “viajados” (`Quero me surpreender`, `#PartiuCafé` como CTA principal, etc.).

**Textos permitidos (escolher o mais adequado ao contexto):**
- Falar com atendente
- Entrar em contato
- Falar no WhatsApp
- Solicitar orçamento

**Regra obrigatória:** todo CTA de conversão (botão principal, flutuante, banner) deve incluir o ícone `<i class="fab fa-whatsapp" aria-hidden="true"></i>` **antes** do texto, para o usuário identificar que abrirá o WhatsApp e não fechar a janela antes da conversão.

```html
<a href="https://wa.me/5541999999999?text=Olá!%20Gostaria%20de%20falar%20com%20um%20atendente."
   target="_blank" rel="noopener" class="btn-wa">
  <i class="fab fa-whatsapp" aria-hidden="true"></i> Falar com atendente
</a>
```

**Links WhatsApp:** usar **sempre** `https://wa.me/NUMERO` (nunca `api.whatsapp.com`).

Botão flutuante: redondo, canto inferior direito, ícone WhatsApp. Pode ter submenu (Comercial / Administrativo) se o cliente tiver mais de um número ou setor.

Formulários de e-mail: botão pode ser `Enviar mensagem` (sem ícone WhatsApp), pois não abre o app.

---

## 3. Bloco de diferenciais (3 itens abaixo do hero)

O bloco padrão de 3 diferenciais/números **não** fica logo abaixo do hero.

**Posição:** próximo ao rodapé (após depoimentos/contato), para reduzir rolagem até serviços e imagens.

Ordem sugerida na home:
1. Hero
2. Sobre / estrutura (se houver)
3. Serviços
4. Portfólio / galeria
5. Clientes / logos
6. Depoimentos
7. Contato / formulário
8. Diferenciais (3 itens)
9. Avaliações Google (carrossel)
10. Footer

---

## 4. Tipografia

**Antes de codar**, definir ou pedir à IA que escolha fonte coerente com o segmento:

| Segmento | Sugestão |
|----------|----------|
| Saúde / clínica | Nunito, Lato |
| Advocacia / corporativo | Libre Baskerville, Source Sans |
| Beleza / estética | Poppins, Playfair Display |
| Infantil / educação | Quicksand, Fredoka |
| Marketing / agência | Cairo, DM Sans |
| Luxo / premium | Cormorant, Montserrat |

Registrar a escolha no `brand.css` com `@import` ou `@font-face` no início do projeto. Não deixar a IA escolher no meio do desenvolvimento.

---

## 5. Widget de avaliações Google

Incluir seção com carrossel de avaliações (estilo TrustIndex), antes do footer.

- Estrelas, nome do avaliador, texto resumido, link “Ver todas no Google”
- Carrossel automático com pausa no hover
- Dados: informar Place ID ou colar avaliações manualmente até integrar API
- Link sempre para o perfil do Google Meu Negócio

```html
<section id="avaliacoes-google" aria-labelledby="reviews-title">
  <h2 id="reviews-title">O que dizem no Google</h2>
  <div class="reviews-carousel">...</div>
  <a href="LINK_GMB">Ver todas as avaliações no Google</a>
</section>
```

---

## 6. SEO básico (checklist obrigatório)

A IA deve entregar **todos** os itens abaixo antes de considerar o site pronto:

- [ ] `title` único e descritivo por página
- [ ] `meta description` única por página
- [ ] `charset` UTF-8
- [ ] `viewport` responsivo
- [ ] `link rel="canonical"` em cada página
- [ ] Hierarquia correta: um `h1`, `h2`/`h3` em ordem lógica
- [ ] HTML semântico (`header`, `main`, `section`, `article`, `footer`, `nav`, `address`)
- [ ] Imagens com `alt` descritivo
- [ ] Links internos entre páginas (sites multipágina)
- [ ] URLs amigáveis (pastas com `index.html`, sem `.html` na URL)
- [ ] `sitemap.xml` na raiz
- [ ] `robots.txt` na raiz
- [ ] `schema.org` (Organization, LocalBusiness ou Service quando aplicável)
- [ ] `label` ou `sr-only` em todos os campos de formulário
- [ ] Contraste e `:focus-visible` acessíveis
- [ ] Imagens em WebP (ou AVIF) otimizadas
- [ ] `loading="lazy"` em imagens abaixo da dobra
- [ ] `width` e `height` em imagens (evitar CLS)
- [ ] Performance mobile (Lighthouse > 85 quando possível)
- [ ] CTA claro e visível
- [ ] Conteúdo escaneável (parágrafos curtos, listas, subtítulos)

---

## 7. WhatsApp

| Correto | Incorreto |
|---------|-----------|
| `https://wa.me/5541999999999` | `https://api.whatsapp.com/send?phone=...` |
| `https://wa.me/5541999999999?text=...` | Links `whatsapp://` em CTAs web |

---

## 8. Texto: sem travessões de IA

**Nunca** usar travessão longo (`—`) ou hífen decorativo (`–`) em textos do site, mesmo que venham do briefing ou sejam gerados pela IA.

Substituir por:
- vírgula
- ponto
- dois pontos
- parênteses

| Errado | Correto |
|--------|---------|
| `Curitiba — PR` | `Curitiba, PR` |
| `equipe — sem perder` | `equipe, sem perder` |
| `08h00 – 18h00` | `08h00 às 18h00` |

Revisar todo HTML antes de entregar.

---

## 9. Estrutura de arquivos recomendada

```
/
├── index.html
├── robots.txt
├── sitemap.xml
├── 404.html
├── assets/
│   ├── css/brand.css
│   ├── js/brand.js
│   └── images/
├── contato/index.html
├── quem-somos/index.html
└── servicos/{slug}/index.html
```

---

## Snippet: variáveis do projeto (copiar e preencher)

```
EMPRESA=Nome da Empresa
SEGMENTO=
CIDADE=Curitiba
UF=PR
DOMINIO=exemplo.com.br
WA_NUMERO=5541999999999
MAPA_QUERY=Nome+da+Empresa,+Curitiba,+PR
MAPA_ZOOM=14
FONTE_PRINCIPAL=Cairo
GMB_URL=https://www.google.com/maps/search/?api=1&query=...
```
