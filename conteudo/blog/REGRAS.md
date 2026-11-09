# Regras do blog da Conceito Prime

Estas regras valem para todo artigo novo ou revisado em conceitop.com.br/blog. A tarefa automática diária publica 2 artigos por dia (frente A e frente B, ver seção 3) e segue este arquivo à risca. Se algo aqui conflitar com o prompt da tarefa, vale este arquivo.

## 1. Objetivo

O blog existe para trazer **empresários e gestores** do Google para o site e transformar parte deles em pedido de diagnóstico. Medimos sucesso em cliques orgânicos de quem tem perfil de cliente e em formulários enviados, nunca em visita de estudante, candidato a vaga ou concorrente.

**Foco atual (desde 2026-11-09, pedido do Gabriel): empresas que querem vender mais.** Os temas são o que donos, sócios, diretores e gestores comerciais ou de marketing pesquisam quando querem aumentar vendas: conseguir mais clientes, gerar leads, prospectar, montar e cobrar a equipe comercial, funil de vendas, CRM, atendimento e tempo de resposta, ticket médio, recompra, investimento em anúncios, escolha de agência e medição de retorno. Vale para qualquer setor, B2B ou B2C, de preferência empresas com faturamento acima de R$ 100 mil por mês (indústria, distribuidora, serviços B2B, clínica, imobiliária, construtora, varejo de porte, agronegócio). O setor pode entrar como recorte de um artigo (ex.: "como aumentar as vendas de uma distribuidora"), mas nenhum setor é foco exclusivo. (De 2026-10-30 a 2026-11-08 o foco foi o mercado imobiliário, e antes disso indústrias e empresas B2B; os artigos desses focos ficam no ar e podem ser revisados.)

Público que não queremos atrair: quem procura curso, aula, estágio, vaga, freelancer, "grátis", "barato", MEI, "como fazer sozinho" de nível iniciante, outras agências, vendedor individual procurando frases ou técnicas para bater a própria meta (só entra com ângulo de gestão da equipe), quem quer vender como pessoa física (marketplace, revenda, renda extra) e consumidor final.

## 2. Como escolher o tema (pesquisa real, nunca chute)

Todo tema precisa de **sinal de busca real** em pelo menos uma fonte abaixo, anotado em `conteudo/blog/pauta.md` com a fonte e o número.

Fontes, em ordem de peso:

1. **Planejador de palavras-chave do Google Ads** (conta Cprime 2026, 404-812-7952), pelo Chrome: volume médio mensal no Brasil e, quando der, no Paraná e em Santa Catarina. É a fonte principal de volume.
2. **Search Console** de https://conceitop.com.br/ (pelo Chrome; o Windsor não tem essa propriedade): consultas com impressões em posição 8 a 40 mostram assunto em que já aparecemos e falta página forte. Ignore consultas de spam (cassino, slot, apostas, domínios .online e .site) que sobraram da invasão de 2025.
3. **Termos de pesquisa do Google Ads** da conta 404-812-7952 pelo Windsor.ai (conector google_ads, últimos 90 dias): mostram as palavras de quem está pronto para contratar.
4. **Resultados do Google** pelo WebSearch: perguntas relacionadas, buscas relacionadas e o que os concorrentes ranqueados já publicaram. Serve para confirmar a intenção e achar o ângulo que falta, não para substituir volume.
5. **Pesquisas do setor** com metodologia declarada (IBGE, CNI, FIEP, FIESC, Sebrae, Google, Think with Google, RD Station, HubSpot, Meta, associações setoriais): para dar dado de apoio dentro do texto.

Filtros obrigatórios na escolha:

- O termo precisa ter intenção de empresário ou gestor. Exemplo bom: "como aumentar as vendas da empresa", "como montar uma equipe comercial", "funil de vendas b2b", "quanto investir em marketing". Exemplo ruim: "curso de vendas grátis", "como vender no mercado livre", "frases para vender mais", "renda extra vendendo".
- Nunca repetir a palavra-chave principal nem a pergunta de um artigo existente (`conteudo/blog/posts.json`). Se o tema já existe, melhoramos o artigo antigo e atualizamos o campo `atualizado` em vez de criar outro.
- Alternar a camada geográfica e a categoria em relação aos últimos 3 artigos da mesma frente (seção 3).
- Os 2 artigos do mesmo dia nunca têm a mesma palavra-chave principal, a mesma pergunta nem a mesma cidade, e de preferência ficam em categorias diferentes.

Sinal mínimo para publicar (volume real e qualificado):

- Com o Planejador disponível: a palavra-chave principal (ou a soma das variações próximas) precisa ter volume médio mensal registrado. Preferência: 50 ou mais buscas por mês em tema nacional e 10 ou mais em tema local, somando as variações. Abaixo disso, só se o termo for de contratação direta (serviço mais cidade) e tiver sinal em outra fonte.
- Sem o Planejador na execução: só publicar tema do estoque do `pauta.md` que já tenha volume do Planejador registrado, ou tema com sinal em pelo menos 2 fontes de dados reais (Search Console, termos do Ads). Perguntas relacionadas do Google sozinhas não bastam.
- Qualidade antes de cota: se uma frente não tiver tema que passe nestes critérios, melhoramos um artigo existente daquela frente (e atualizamos o campo `atualizado`) em vez de publicar texto fraco, e registramos o motivo no `pauta.md`.

Escada de prioridade (desça um degrau só quando o de cima não tiver tema novo com sinal real):

1. **Contratação local**: serviço de marketing ou vendas mais cidade com volume (ex.: "agência de marketing curitiba", "consultoria de vendas curitiba", "agência de marketing joinville", "marketing digital cascavel").
2. **Decisão de compra**: preço, comparação, escolha, ROI, prazo (ex.: "quanto custa uma agência de marketing", "quanto investir em marketing", "google ads ou meta ads", "terceirizar o comercial vale a pena", "qual crm escolher").
3. **Dor do empresário com volume nacional**: vender mais, conseguir clientes, gerar leads, prospecção, equipe comercial (metas, comissão, rotina, indicadores), funil de vendas, CRM, atendimento e tempo de resposta, ticket médio, recompra e pós-venda, vendas pelo WhatsApp (ex.: "como aumentar as vendas", "como conseguir mais clientes", "como montar uma equipe de vendas", "indicadores de vendas").
4. **Recorte por setor ou modelo**: a mesma dor aplicada a um setor de porte (indústria, distribuidora, serviços B2B, clínica, imobiliária, construtora, varejo, agronegócio) ou a um modelo de venda (venda consultiva, venda recorrente, venda por representantes).

## 3. Camada geográfica: duas frentes por dia

Toda execução da tarefa diária publica 2 artigos, um de cada frente. A frente sai do campo `local`: cidade do Paraná ou "Paraná" é frente A; "Brasil", outro estado ou cidade fora do Paraná é frente B.

**Frente A: Curitiba, região metropolitana e Paraná.** Termo de busca com a cidade ou a região, ou tema de vendas com recorte paranaense (setor forte no estado, polo econômico, dado do estado). Distribuição alvo por semana (7 artigos): 3 de Curitiba ou região metropolitana, 1 de Cascavel ou oeste do Paraná, 2 de outros polos do Paraná e 1 com recorte do estado inteiro. Recorte do estado é tema do artigo, nunca promessa de "atendimento em todo o Paraná".

**Frente B: contexto amplo.** Tema nacional (Brasil) ou de polo econômico forte fora do Paraná. Distribuição alvo por semana (7 artigos): 4 nacionais, 2 de Santa Catarina e 1 de São Paulo ou de outro polo forte. Empresa fora do Paraná é zona cinzenta na definição de lead qualificado, então o tema local fora do estado precisa ter intenção clara de empresa de porte contratando.

Ajuste as duas distribuições conforme o volume real encontrado.

Cidades e polos estratégicos:

- Curitiba e região metropolitana (frente A): Curitiba, São José dos Pinhais, Araucária, Pinhais, Colombo, Campo Largo, Fazenda Rio Grande, Almirante Tamandaré, Quatro Barras, Campina Grande do Sul, Piraquara, Mandirituba.
- Outros polos do Paraná (frente A): Cascavel, Toledo, Foz do Iguaçu, Marechal Cândido Rondon, Londrina, Maringá, Ponta Grossa, Guarapuava, Pato Branco, Francisco Beltrão, Apucarana, Arapongas.
- Santa Catarina (frente B): Joinville, Blumenau, Jaraguá do Sul, Itajaí, Brusque, Chapecó, Criciúma, Florianópolis, São Bento do Sul, Rio do Sul.
- São Paulo (frente B): São Paulo capital, ABC Paulista (Santo André, São Bernardo do Campo, São Caetano do Sul, Diadema), Guarulhos, Campinas, Jundiaí, Sorocaba, São José dos Campos, Ribeirão Preto, Piracicaba.
- Outros polos (frente B, só com volume real e intenção B2B): Caxias do Sul, Porto Alegre e região metropolitana, Belo Horizonte, Contagem e Betim.

Regras para artigo local:

- Só escrever sobre a cidade o que for verdade e verificável (polos industriais, setores fortes), com fonte quando citar dado.
- Sempre citar que temos **escritórios em Curitiba e Cascavel**. Cidade do Paraná: atendemos empresas da cidade com reunião presencial ou online. Cidade fora do Paraná: atendemos com reunião online, sem sugerir escritório ou equipe local. Nunca escrever "atendimento em todo o Paraná".
- Nunca inventar endereço, telefone, cliente ou case na cidade.
- Preencher o campo `local` com o nome da cidade, "Paraná", "Santa Catarina", "São Paulo" (estado) ou "Brasil".

## 4. Formato do artigo

Metadados em `conteudo/blog/posts.json` (um objeto por artigo):

| Campo | Regra |
|---|---|
| `slug` | curto, com a palavra-chave principal, sem acento, sem data |
| `titulo` | H1 do artigo, com a palavra-chave e o gancho do artigo (ver seção 4.1) |
| `titulo_seo` | o título que aparece no Google, até 60 caracteres, palavra-chave no começo e gancho de clique (ver seção 4.1); "\| Conceito Prime" só se couber sem cortar o gancho |
| `descricao` | 140 a 155 caracteres, com a palavra-chave e um motivo para clicar |
| `linha_fina` | 1 frase abaixo do título, dor ou promessa concreta |
| `data` e `atualizado` | AAAA-MM-DD de hoje |
| `categoria` | uma de: Vendas, Marketing Digital, Estratégias de Marketing, Gestão |
| `palavras_chave` | lista com a principal primeiro e 3 a 6 secundárias reais da pesquisa |
| `local` | cidade, Paraná, Santa Catarina, São Paulo ou Brasil (define a frente, seção 3) |
| `faq` | 3 a 5 `{pergunta, resposta}` com perguntas reais (perguntas relacionadas do Google, Search Console, termos do Ads); resposta de 1 a 3 frases |
| `fontes` | lista `{nome, url}` de toda fonte de dado citada, sempre a página original |

### 4.1 Título com alto CTR

O `titulo_seo` é o que o empresário vê no Google e decide o clique. Ele não é só a palavra-chave com a marca: precisa ter a palavra-chave no começo **e** um motivo concreto para clicar. Queremos o título com mais chance de clique, mas no tom de quem fala com dono ou diretor de empresa: direto, provocativo quando o artigo sustenta, nunca alarmista nem de manchete policial.

Ganchos que funcionam para esse público (usar um por título):

- **Dor de negócio concreta:** vendas paradas, lead que ninguém atende, vendedor que não bate meta, cliente que não volta a comprar, verba de anúncio sem retorno. Ex.: "Como aumentar as vendas: por que o lead esfria antes do contato".
- **Número real do artigo:** quantidade de erros, etapas, critérios ou indicadores que o texto entrega de fato. Ex.: "Indicadores de vendas: 9 números para cobrar da equipe".
- **Decisão ou comparação:** "X ou Y?", "vale a pena?", "quando contratar". Ex.: "Equipe de vendas própria ou terceirizada: quando vale cada uma".
- **Custo e investimento**, só quando o artigo traz faixa de mercado com fonte. Ex.: "Quanto investir em marketing: o cálculo a partir da meta".
- **Recorte local** na frente A (Curitiba, Paraná) e no polo da frente B, junto com a dor.
- **Ano** só quando o artigo traz dado ou regra daquele ano.

Regras:

- Palavra-chave principal nos primeiros 30 caracteres do `titulo_seo`; o gancho logo em seguida, dentro dos 60.
- "| Conceito Prime" no fim só se couber sem cortar o gancho. Na dúvida, fica o gancho: o Google já mostra o nome do site acima do título na maioria dos resultados.
- O `titulo` (H1) pode ser mais longo e completar o `titulo_seo`, sem repetir as mesmas palavras na mesma ordem. A `linha_fina` entrega a promessa concreta e a `descricao` dá o motivo do clique com a palavra-chave.
- Escrever três opções de `titulo_seo`, escolher a mais forte que passe nos testes abaixo e registrar as três no `pauta.md` junto da linha em Publicados.

Proibido no título, na linha fina e na descrição:

- Promessa de resultado ("dobre suas vendas", "venda todo o estoque", "leads garantidos", "em 30 dias", "vendas explosivas"), número ou case que o artigo não comprova.
- Gatilho vazio: "segredo", "ninguém te conta", "o que ninguém fala", "chocante", "urgente", exclamação, reticências, emoji, palavra inteira em caixa alta (siglas como CRM, VGV, ROI, SEO são permitidas).
- Título que atrai o público errado: vendedor individual atrás de frases prontas, quem quer renda extra ou vender como pessoa física, iniciante, curso ou "grátis". Um título com CTR alto para quem não é cliente é pior que um título discreto.
- Ganho de alcance, curtida ou seguidor como benefício (seção 5).

Testes antes de publicar:

1. **Promessa cumprida no início:** o que o título promete aparece respondido no primeiro parágrafo ou no primeiro `h2`.
2. **Quem clica é cliente?** Ler o título como dono de empresa com equipe comercial e como vendedor iniciante ou pessoa física. Se o segundo clicaria mais que o dono, reescrever.
3. **Número conferido:** todo número do título existe no corpo (contagem de itens) ou tem fonte em `fontes`.

Títulos de artigos antigos: ao revisar um artigo que no Search Console tem 100 impressões ou mais nos últimos 28 dias, posição média até 15 e CTR abaixo de 2%, podemos reescrever o `titulo_seo` e a `descricao` por esta seção, sem trocar o `slug`, e registrar no `pauta.md` o título antigo, o novo, a data e os números de antes, para comparar depois.

Corpo em `conteudo/blog/<slug>.html`, HTML limpo (só `h2`, `h3`, `p`, `ul`, `ol`, `li`, `table`, `thead`, `tbody`, `tr`, `th`, `td`, `a`, `strong`, `em`), sem `h1`, sem estilos e sem scripts. O gerador já coloca sozinho: índice "Neste artigo" (com 3 ou mais `h2`), CTA no meio, cartão lateral fixo, formulário de diagnóstico no fim, barra fixa no celular, FAQ com schema FAQPage, fontes, BlogPosting, Breadcrumb, artigos relacionados, sitemap e RSS.

Conteúdo:

- 1.200 a 2.000 palavras, português do Brasil, tom executivo e direto, primeira pessoa do plural ("na nossa experiência com empresas de porte...").
- O primeiro parágrafo já responde a busca em 2 ou 3 frases.
- 4 a 7 seções `h2`; pelo menos uma tabela, checklist ou passo a passo quando o tema permitir.
- Pelo menos 2 links internos para páginas de serviço (`/b2b/`, `/contato/`, `/quem-somos/`; `/industrial/` só se o tema tocar galpão ou imóvel industrial) e 1 para outro artigo do blog com relação.
- Fechar com um parágrafo que liga o tema ao diagnóstico gratuito (o formulário já vem no template).
- Dados e estatísticas só depois de abrir a fonte original e confirmar número, ano e quem publicou. Sem fonte confirmada, sem número.
- Escrever com nossas palavras; nunca copiar trechos das fontes.

## 5. Abacaxis (proibido em qualquer artigo)

- Travessão (caracteres Unicode U+2014 e U+2013) em qualquer lugar do texto ou dos metadados.
- Primeira pessoa do singular.
- "Atendimento em todo o Paraná".
- Prometer curtida, seguidor, alcance ou "viralizar" como resultado. Nosso resultado é contato qualificado e venda.
- Inventar número, case, cliente, depoimento, preço ou prazo da Conceito Prime. Preço de mercado só com fonte.
- Reduzir a Conceito Prime a "agência de tráfego pago".
- Expressões como "assumimos a conta" ou "operação enxuta".
- Citar nome de cliente sem que ele esteja na lista de logos do site.
- Conteúdo para iniciante que quer fazer sozinho sem contratar (curso, tutorial de ferramenta passo a passo para leigo).

## 6. Publicação

1. `python3 scripts/generate-blog-covers.py` (gera só a capa do artigo novo).
2. `python3 scripts/generate-blog.py`.
3. `npm run build` (o verify precisa terminar com "Site pronto para deploy").
4. Conferir que `dist/blog/<slug>/index.html` existe, que não há travessão (rodar `python3 -c "import sys;t=open(sys.argv[1]).read();print(t.count(chr(8212))+t.count(chr(8211)))" <arquivo>` no corpo e no posts.json; precisa dar 0) e que o schema FAQPage foi gerado.
5. Acrescentar a linha em `conteudo/blog/pauta.md` (Publicados, com a frente) e registrar os temas avaliados e descartados.
6. Um commit por artigo, com autor "Gabriel Priss <feedxe321@gmail.com>", mensagem "Blog: <título curto>", push na main. O Cloudflare publica em 1 a 2 minutos e o workflow do GitHub avisa o Bing pelo IndexNow.
