# Regras do blog da Conceito Prime

Estas regras valem para todo artigo novo ou revisado em conceitop.com.br/blog. A tarefa automática diária publica 2 artigos por dia (frente A e frente B, ver seção 3) e segue este arquivo à risca. Se algo aqui conflitar com o prompt da tarefa, vale este arquivo.

## 1. Objetivo

O blog existe para trazer **empresários e gestores** do Google para o site e transformar parte deles em pedido de diagnóstico. Medimos sucesso em cliques orgânicos de quem tem perfil de cliente e em formulários enviados, nunca em visita de estudante, candidato a vaga ou concorrente.

**Foco atual (desde 2026-10-30, pedido do Gabriel): mercado imobiliário.** Público que queremos: sócios, diretores e gestores comerciais ou de marketing de **imobiliárias, construtoras, incorporadoras e loteadoras**, de preferência com faturamento acima de R$ 100 mil por mês (imobiliária com equipe de corretores e carteira própria, construtora ou incorporadora com lançamentos). Corretor autônomo e imobiliária de uma pessoa só não são público. (Antes de 2026-10-30 o foco era indústrias e empresas B2B; os artigos antigos desse foco ficam no ar e podem ser revisados, mas não entram tema novo de indústria.)

Público que não queremos atrair: quem procura curso, aula, estágio, vaga, freelancer, "grátis", "barato", MEI, "como fazer sozinho" de nível iniciante, outras agências, corretor autônomo procurando captar sozinho, e **quem quer comprar, alugar ou vender um imóvel** (consumidor final, que é a busca dominante nesse mercado: "apartamento à venda curitiba", "aluguel", "financiamento" etc.).

## 2. Como escolher o tema (pesquisa real, nunca chute)

Todo tema precisa de **sinal de busca real** em pelo menos uma fonte abaixo, anotado em `conteudo/blog/pauta.md` com a fonte e o número.

Fontes, em ordem de peso:

1. **Planejador de palavras-chave do Google Ads** (conta Cprime 2026, 404-812-7952), pelo Chrome: volume médio mensal no Brasil e, quando der, no Paraná e em Santa Catarina. É a fonte principal de volume.
2. **Search Console** de https://conceitop.com.br/ (pelo Chrome; o Windsor não tem essa propriedade): consultas com impressões em posição 8 a 40 mostram assunto em que já aparecemos e falta página forte. Ignore consultas de spam (cassino, slot, apostas, domínios .online e .site) que sobraram da invasão de 2025.
3. **Termos de pesquisa do Google Ads** da conta 404-812-7952 pelo Windsor.ai (conector google_ads, últimos 90 dias): mostram as palavras de quem está pronto para contratar.
4. **Resultados do Google** pelo WebSearch: perguntas relacionadas, buscas relacionadas e o que os concorrentes ranqueados já publicaram. Serve para confirmar a intenção e achar o ângulo que falta, não para substituir volume.
5. **Pesquisas do setor** com metodologia declarada (IBGE, CNI, FIEP, FIESC, Sebrae, Google, Think with Google, RD Station, HubSpot, Meta, associações setoriais): para dar dado de apoio dentro do texto.

Filtros obrigatórios na escolha:

- O termo precisa ter intenção de empresário. Exemplo bom: "marketing para imobiliária", "google ads para construtora", "como vender lançamento imobiliário". Exemplo ruim: "curso de corretor de imóveis", "apartamento à venda curitiba".
- Nunca repetir a palavra-chave principal nem a pergunta de um artigo existente (`conteudo/blog/posts.json`). Se o tema já existe, melhoramos o artigo antigo e atualizamos o campo `atualizado` em vez de criar outro.
- Alternar a camada geográfica e a categoria em relação aos últimos 3 artigos da mesma frente (seção 3).
- Os 2 artigos do mesmo dia nunca têm a mesma palavra-chave principal, a mesma pergunta nem a mesma cidade, e de preferência ficam em categorias diferentes.

Sinal mínimo para publicar (volume real e qualificado):

- Com o Planejador disponível: a palavra-chave principal (ou a soma das variações próximas) precisa ter volume médio mensal registrado. Preferência: 50 ou mais buscas por mês em tema nacional e 10 ou mais em tema local, somando as variações. Abaixo disso, só se o termo for de contratação direta (serviço mais cidade) e tiver sinal em outra fonte.
- Sem o Planejador na execução: só publicar tema do estoque do `pauta.md` que já tenha volume do Planejador registrado, ou tema com sinal em pelo menos 2 fontes de dados reais (Search Console, termos do Ads). Perguntas relacionadas do Google sozinhas não bastam.
- Qualidade antes de cota: se uma frente não tiver tema que passe nestes critérios, melhoramos um artigo existente daquela frente (e atualizamos o campo `atualizado`) em vez de publicar texto fraco, e registramos o motivo no `pauta.md`.

Escada de prioridade (desça um degrau só quando o de cima não tiver tema novo com sinal real):

1. **Contratação local**: serviço para o mercado imobiliário mais cidade com volume (ex.: "marketing imobiliário curitiba", "agência de marketing para imobiliária curitiba", "marketing para construtora joinville").
2. **Decisão de compra**: preço, comparação, escolha, ROI, prazo (ex.: "quanto investir em anúncios para imobiliária", "agência de marketing imobiliário vale a pena", "meta ads ou google ads para lançamento").
3. **Dor do empresário com volume nacional**: leads para imobiliária, captação de imóveis, vendas de lançamento, CRM imobiliário, atendimento de leads e tempo de resposta, portais imobiliários versus site próprio, estande e plantão (ex.: "como gerar leads para imobiliária", "como captar imóveis", "como vender lançamento imobiliário").
4. **Nicho do mercado imobiliário**: alto padrão, loteamentos, imóveis comerciais e corporativos, locação e administração de imóveis, condomínios logísticos e galpões, incorporação de médio porte, casas de campo e praia (litoral do Paraná e de SC).

## 3. Camada geográfica: duas frentes por dia

Toda execução da tarefa diária publica 2 artigos, um de cada frente. A frente sai do campo `local`: cidade do Paraná ou "Paraná" é frente A; "Brasil", outro estado ou cidade fora do Paraná é frente B.

**Frente A: Curitiba, região metropolitana e Paraná.** Termo de busca com a cidade ou a região, ou tema com recorte paranaense (setor forte no estado, polo industrial). Distribuição alvo por semana (7 artigos): 3 de Curitiba ou região metropolitana, 1 de Cascavel ou oeste do Paraná, 2 de outros polos do Paraná e 1 com recorte do estado inteiro. Recorte do estado é tema do artigo, nunca promessa de "atendimento em todo o Paraná".

**Frente B: contexto amplo.** Tema nacional (Brasil) ou de polo industrial e comercial forte fora do Paraná. Distribuição alvo por semana (7 artigos): 3 nacionais, 2 de Santa Catarina e 2 de São Paulo ou de outro polo forte. Empresa fora do Paraná é zona cinzenta na definição de lead qualificado, então o tema precisa ter intenção clara de imobiliária, construtora ou incorporadora de porte.

Ajuste as duas distribuições conforme o volume real encontrado.

Cidades e polos estratégicos (mercado imobiliário forte; a lista também vale para os polos de Santa Catarina com lançamentos de alto padrão, como Balneário Camboriú, Itapema e Florianópolis):

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
| `titulo` | H1 do artigo, claro, com a palavra-chave |
| `titulo_seo` | até cerca de 60 caracteres, termina em "\| Conceito Prime" se couber |
| `descricao` | 140 a 155 caracteres, com a palavra-chave e um motivo para clicar |
| `linha_fina` | 1 frase abaixo do título, dor ou promessa concreta |
| `data` e `atualizado` | AAAA-MM-DD de hoje |
| `categoria` | uma de: Vendas, Marketing Digital, Estratégias de Marketing, Gestão |
| `palavras_chave` | lista com a principal primeiro e 3 a 6 secundárias reais da pesquisa |
| `local` | cidade, Paraná, Santa Catarina, São Paulo ou Brasil (define a frente, seção 3) |
| `faq` | 3 a 5 `{pergunta, resposta}` com perguntas reais (perguntas relacionadas do Google, Search Console, termos do Ads); resposta de 1 a 3 frases |
| `fontes` | lista `{nome, url}` de toda fonte de dado citada, sempre a página original |

Corpo em `conteudo/blog/<slug>.html`, HTML limpo (só `h2`, `h3`, `p`, `ul`, `ol`, `li`, `table`, `thead`, `tbody`, `tr`, `th`, `td`, `a`, `strong`, `em`), sem `h1`, sem estilos e sem scripts. O gerador já coloca sozinho: índice "Neste artigo" (com 3 ou mais `h2`), CTA no meio, cartão lateral fixo, formulário de diagnóstico no fim, barra fixa no celular, FAQ com schema FAQPage, fontes, BlogPosting, Breadcrumb, artigos relacionados, sitemap e RSS.

Conteúdo:

- 1.200 a 2.000 palavras, português do Brasil, tom executivo e direto, primeira pessoa do plural ("na nossa experiência com indústrias...").
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
