# Fontes públicas de defesa comercial (SECEX/DECOM e GECEX)

Pesquisa da issue #2. Data da verificação: 29/10/2026. Todas as datas de atualização citadas foram lidas nas próprias páginas nessa data.

## Resposta curta

Os atos de defesa comercial têm uma única fonte oficial com valor jurídico, o **Diário Oficial da União (DOU), Seção 1**, onde saem as circulares SECEX (abertura, prorrogação, cronograma, determinação preliminar, encerramento sem medida) e as resoluções GECEX (aplicação, prorrogação, suspensão ou extinção de direitos). O MDIC reproduz essa informação em três camadas secundárias no portal gov.br: (i) páginas HTML de **investigações em curso** e **medidas em vigor**; (ii) arquivos **CSV de dados abertos** do DECOM, entre eles uma base histórica de investigações com 21 colunas que já traz NCM, atos e direito aplicado; (iii) a listagem de **resoluções GECEX** com feed RSS. Os pareceres DECOM ficam nos autos do SEI; ao público chegam como Anexo das resoluções e circulares publicadas no DOU. Para coleta automatizada confiável, a combinação recomendada é **DOU via INLABS (XML diário)** como gatilho de novos atos e **CSV do DECOM** como carga inicial e conferência periódica.

## 1. Onde cada ato é publicado

| Ato | Quem edita | Onde sai com valor oficial | Onde aparece no portal do MDIC |
|---|---|---|---|
| Circular de abertura de investigação ou revisão | SECEX | DOU Seção 1 | Página do caso em "Investigações em curso"; coluna "Circular de Inicio da investigacao" do CSV |
| Circular de prorrogação de prazo / novo cronograma | SECEX | DOU Seção 1 | CSV, coluna "Circular de prorrogacao da investigacao" |
| Circular de determinação preliminar | SECEX | DOU Seção 1 | CSV, colunas "Data/Circular de determinacao preliminar" |
| Resolução de direito provisório | GECEX | DOU Seção 1 | Listagem de resoluções GECEX; CSV |
| Resolução de aplicação ou prorrogação de direito definitivo (com Anexo que torna públicos os fatos da determinação final) | GECEX | DOU Seção 1 | Listagem de resoluções GECEX; "Medidas em vigor"; CSV |
| Circular ou resolução de encerramento | SECEX ou GECEX | DOU Seção 1 | CSV, coluna "Resolucao ou Circular de encerramento" |
| Parecer DECOM (determinação preliminar ou final), notas técnicas de fatos essenciais | DECOM | Autos SEI (públicos/restritos/confidenciais); resumo no Anexo do ato no DOU | Não há repositório público sistemático |
| Avaliação de interesse público (suspensão/alteração de medida) | SECEX/GECEX | DOU Seção 1 | "Suspensões e alterações por Interesse Público em vigor"; CSV próprio |

Exemplos verificados da estrutura dos atos:

- **Circular SECEX nº 58/2026** (DOU 21/07/2026), papel decorativo da China, NCM 4805.91.00: item único que torna público novo cronograma, com tabela de prazos (arts. 59 a 63 do Decreto 8.058/2013), e cita os processos SEI 19972.002430/2024-82 (restrito) e 19972.002429/2024-58 (confidencial). Fonte: [LegisWeb, reprodução do DOU](https://www.legisweb.com.br/legislacao/?id=498343).
- **Resolução GECEX nº 920/2026** (238ª reunião, DOU 24/06/2026), filtros cerâmicos da China, NCM 6903.90.91 e 6903.90.99: art. 1º prorroga o direito por até cinco anos com tabela origem / produtor-exportador / alíquota em US$/kg; parágrafo único declara a NCM "meramente indicativa"; art. 2º remete ao **Anexo Único**, que expõe a determinação final (histórico, produto, indústria doméstica, dumping, dano); cita o Parecer SEI nº 564/2026/MDIC e os processos SEI. Fonte: [LegisWeb, reprodução do DOU](https://www.legisweb.com.br/legislacao/?id=497135).

Observação de método: os textos integrais acima foram lidos em reproduções do DOU (LegisWeb), porque o `in.gov.br` bloqueia leitura automatizada pela ferramenta usada nesta pesquisa. A estrutura descrita deve ser conferida contra o XML do INLABS na implementação.

Base normativa: o rito e os prazos estão no [Decreto nº 8.058/2013](https://planalto.gov.br/ccivil_03/_Ato2011-2014/2013/Decreto/D8058.htm): investigação concluída em 10 meses, prorrogável até 18 (art. 72); direito definitivo extinto em 5 anos (art. 93); durante revisão de final de período o direito permanece em vigor (art. 105, § 2º). A tramitação eletrônica no SEI e o regime de autos confidenciais, restritos e públicos estão na [Portaria SECEX nº 162/2022](https://www.legisweb.com.br/legislacao/?id=425945) (arts. 4º, 6º, 7º e 43); o antigo Sistema DECOM Digital ficou apenas para consulta.

## 2. Portal do DECOM no gov.br

Página-raiz: [Defesa Comercial e Interesse Público](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico). Destaques: "Investigações em curso", "Medidas em vigor", "Publicações do DECOM no D.O.U.", "Estatísticas e Histórico", "Legislação".

### 2.1 Investigações em curso (HTML)

- URL: [investigacoes-de-defesa-comercial](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/investigacoes/investigacoes-de-defesa-comercial). "Atualizado em 01/10/2026 09h23".
- Tabela HTML com colunas **PRODUTO, INVESTIGAÇÃO, ORIGEM, COORDENAÇÃO RESPONSÁVEL** (cerca de 45 linhas) e tabela "Outros procedimentos" (PRODUTO, TIPO).
- Cada produto leva a uma página do caso (`.../investigacoes-de-defesa-comercial/<slug>`, ex.: `acido-acrilico-dp`, `acido-citrico-rdt`). Há links trocados (ex.: "Pneus de carga" aponta para `aco-inox-lam-id`) e slugs `copy_of_...`, sinal de manutenção manual.
- **Não tem NCM nem número do ato.** Atualização manual, sem periodicidade declarada.

### 2.2 Medidas em vigor (HTML)

- URL: [medidas-em-vigor/medidas-em-vigor](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/medidas-em-vigor/medidas-em-vigor). "Atualizado em 09/10/2026 15h28".
- Colunas **PRODUTO, MEDIDA, ORIGEM, PRAZO DE VIGÊNCIA**, cerca de 95 linhas. Tipos presentes: direito antidumping definitivo e provisório, medida compensatória definitiva, compromisso de preço. Nenhuma salvaguarda vigente na data.
- Asterisco na data: "Medida em vigor por força de revisão de final de período em curso, nos termos do art. 105, § 2º do Decreto 8.058, de 2013". Notas entre parênteses indicam cobrança suspensa para certas origens.
- **Não tem NCM, alíquota nem número do ato** na tabela; o detalhe fica em páginas por produto.
- Página irmã: [Suspensões e alterações por Interesse Público em vigor](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/medidas-em-vigor/suspensoes-por-interesse-publico-em-vigor).

### 2.3 Dados abertos do DECOM (CSV) — base para carga inicial

Os arquivos ficam em `https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/arquivos/dados-abertos/<arquivo>`, com download por `<arquivo>/@@download/file`. Não há índice estável verificado; os arquivos foram localizados por busca e o nome muda a cada versão.

| Arquivo | Publicado | Tamanho | Conteúdo |
|---|---|---|---|
| [base-de-investigacoes-de-defesa-comercial-julho-2026.csv](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/arquivos/dados-abertos/base-de-investigacoes-de-defesa-comercial-julho-2026.csv/view) | 05/08/2026 | 406 KB | Histórico de investigações, uma linha por produto × origem |
| [medidasemvigor07052025.csv](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/arquivos/dados-abertos/medidasemvigor07052025.csv/view) | 08/10/2026 (cabeçalho interno "ATUALIZADO EM 07/05/2025") | 49 KB | Medidas em vigor |
| [base_interesse_publico_out_26.csv](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/arquivos/dados-abertos/base_interesse_publico_out_26.csv/view) | 08/10/2026 | 104 KB | Avaliações de interesse público desde 1998 |

**Base de investigações** (separador `;`, com BOM UTF-8), 21 colunas: Produto; Origem; Tipo da investigacao; Subtipo da investigacao; NCM; Setor; Peticionaria; Status da investigacao; Data de entrada da peticao; Data da abertura; Circular de Inicio da investigacao; Data da determinacao preliminar; Circular de determinacao preliminar; Data de aplicacao do direito provisorio; Resolução de aplicação de direito provisorio; Circular de prorrogacao da investigacao; Data do encerramento da investigacao; Resolucao ou Circular de encerramento; Direito aplicado; Status da medida; Vigencia da medida aplicada.

- Valores vistos: Subtipo = investigação original, revisão de final de período, revisão por alteração de circunstâncias, redeterminação, revisão de anticircunvenção, habilitação de indústria fragmentada. Status da investigação = em curso, encerrada com/sem aplicação de direito, procedimento encerrado, medida estendida. Status da medida = em vigor, estendida, suspensa pelo art. 109, encerrada.
- Exemplo: Filtros cerâmicos refratários / China / 6903.90.91, 6903.90.99 / Circular SECEX nº 46/2025 / Resolução Gecex nº 920/2026 / "Demais = US$3,88/kg" / Em vigor / 24/06/2031.
- Problemas de qualidade: NCMs múltiplas escritas de quatro formas ("a, b", "a; b", "a e b", quebra de linha dentro da célula); "Direito aplicado" é texto livre com empresas e alíquotas; o nome do ato é texto ("Circular SECEX nº 60/2026"), sem link nem data do DOU.

**Medidas em vigor CSV**: colunas Produto; Origem; NCM; Direito aplicado; Vigencia da medida aplicada; Status da medida; Data do encerramento da investigacao. A data interna (07/05/2025) indica que **o arquivo está defasado** em relação à página HTML (09/10/2026); ex.: "Alho / China / vigência 03/10/2024 / Em vigor por força de revisão".

**Portal Brasileiro de Dados Abertos**: há o conjunto [Base de dados de Defesa Comercial](https://dados.gov.br/dados/conjuntos-dados/base-de-dados-de-defesa-comercial) e, em espelho, [Investigações de Defesa Comercial em Curso no Brasil](https://data.amerigeoss.org/dataset/investigacoes-de-defesa-comercial-em-curso-no-brasil), cujo recurso aponta para um CSV antigo de 2019 em `mdic.gov.br/images/REPOSITORIO/...`. O dados.gov.br não pôde ser lido diretamente (página dinâmica); periodicidade declarada não foi confirmada.

### 2.4 Outras páginas

- "Publicações do DECOM no D.O.U." e "Estatísticas e Histórico" existem na página-raiz, mas não puderam ser lidas nesta pesquisa (bloqueio de acesso). Devem ser conferidas manualmente.
- O [Painel de Defesa Comercial da FIESP](https://inteligencia-dados.fiesp.com.br/defesa-comercial/notas-metodologicas.html) declara usar DOU, SEI e a página do DECOM como fontes; é secundário e não deve alimentar o sistema.

## 3. Resoluções GECEX

- Listagem: [gov.br/mdic/.../camex/resolucoes/gecex](https://www.gov.br/mdic/pt-br/assuntos/camex/resolucoes/gecex). Lista plana, cerca de 30 itens por página (`?b_start:int=0, 30, 60...`), **sem ordem cronológica**, sem filtro por tema; antidumping e tarifas aparecem misturados. Cada item tem título, ementa (às vezes ausente) e carimbo "publicado DD/MM/AAAA HHhMM". Link do item: `.../resolucoes/gecex/resolucoes/resolucao-gecex-no-<n>-de-<dia>-de-<mes>-de-<ano>` (às vezes com sufixo `-1`).
- Feed RSS 1.0: [.../resolucoes/gecex/resolucoes/RSS](https://www.gov.br/mdic/pt-br/assuntos/camex/resolucoes/gecex/resolucoes/RSS). Apenas 15 itens, e o mais recente era a Resolução 899 (maio/2026), embora a listagem já mostre a 954 (set/2026). **O RSS não acompanha as publicações** e não serve como gatilho.
- As páginas individuais de resolução bloqueiam robôs (`robots_disallowed`).
- Ritmo: o GECEX delibera em reuniões ordinárias mensais (238ª em 23/06/2026) e extraordinárias; atas em PDF em [camex/atas/gecex/<ano>](https://www.gov.br/mdic/pt-br/assuntos/camex/atas/gecex/2025/ata-da-228a-reuniao-ordinaria-do-gecex-de-2025.pdf). As resoluções de defesa comercial saem em lote no DOU nos dias seguintes à reunião (ex.: Resoluções 900 a 910 de 03/06/2026).

## 4. DOU: caminhos de coleta automatizada

**INLABS (Imprensa Nacional)** — caminho preferencial.
- Acesso livre e gratuito, com cadastro (e-mail e senha), às edições completas em **XML e PDF** desde 01/01/2020; janela dos **últimos 4 meses**. Fonte: [README oficial](https://github.com/Imprensa-Nacional/inlabs).
- Script oficial: POST de login em `https://inlabs.in.gov.br/logar.php`, cookie `inlabs_session_cookie`, download diário de `https://inlabs.in.gov.br/index.php?p=AAAA-MM-DD&dl=AAAA-MM-DD-<SEÇÃO>.zip`, com seções `DO1 DO2 DO3 DO1E DO2E DO3E` (extras incluídas). Resposta 404 quando a edição ainda não existe. O próprio README sugere agendamento em `crontab`. (Arquivo `public/python/inlabs-auto-download-xml.py` do mesmo repositório.)
- Cada ZIP contém um XML por matéria (`<article>`), com metadados de órgão, tipo do ato, seção, página e texto em HTML. Os nomes exatos dos campos não foram confirmados em fonte primária nesta pesquisa.
- Relato de terceiro: o login automatizado do INLABS já retornou 502 para clientes não-navegador ([issue #42 de conselhos-vivos](https://github.com/Luidooo/conselhos-vivos/issues/42)). Risco a testar.

**Base mensal de dados abertos do DOU** — para histórico.
- [Base de Dados de Publicações do DOU](https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados): um ZIP por mês e por seção (ex.: `S01082026.zip`), mesmo formato `<article>` do INLABS, sem login, com cerca de duas semanas de atraso (segundo a mesma issue de terceiro; página oficial não pôde ser lida).

**Busca web do DOU** (`in.gov.br/consulta`, `in.gov.br/web/dou/-/<slug>`): bloqueia robôs e não é caminho confiável.

**Filtro dos atos de interesse no XML**: órgão "Ministério do Desenvolvimento, Indústria, Comércio e Serviços / Secretaria de Comércio Exterior" (circulares) e "... / Câmara de Comércio Exterior / Comitê Executivo de Gestão" (resoluções), mais termos como "dumping", "subsídio", "salvaguarda", "Decreto nº 8.058", "Decreto nº 10.839" e NCM no padrão `\d{4}\.\d{2}\.\d{2}`.

## 5. Periodicidade observada

| Fonte | Periodicidade | Evidência |
|---|---|---|
| DOU Seção 1 | Diária (dias úteis), mais edições extras | INLABS lista DO1E |
| Circulares SECEX | Contínua; ~100 por ano (nº 104 em 20/10/2026) | numeração das circulares |
| Resoluções GECEX | Em lote após reuniões mensais | Resoluções 900–910 em 03/06/2026 |
| HTML "Investigações em curso" / "Medidas em vigor" | Manual, irregular | atualizadas em 01/10 e 09/10/2026 |
| CSV de investigações | Aparentemente mensal ou bimestral, com nome datado | "julho-2026" publicado em 05/08/2026 |
| CSV de medidas em vigor | Irregular, defasado | conteúdo de 05/2025 republicado em 10/2026 |

## Implicações para o sistema

1. **Gatilho de novos atos = DOU via INLABS**, coleta diária de DO1 e DO1E, filtrando órgão SECEX e GECEX. É a única fonte oficial e completa; o portal do MDIC chega depois e com lacunas. Precisamos de uma conta INLABS institucional da Eletros e de um teste de login automatizado.
2. **Carga inicial de processos e medidas = CSV "Base de investigações de defesa comercial"**, porque é a única fonte estruturada que liga produto, origem, NCM, peticionária, atos e direito aplicado. Exige normalização de NCMs múltiplas, separação de origens e parsing do "Direito aplicado" em texto livre; cada medida carregada deve entrar como **proposta** a confirmar pela equipe.
3. **Conferência periódica** com a página HTML "Medidas em vigor" (mais atualizada que o CSV de medidas) e com "Investigações em curso", para detectar divergências, inclusive medidas mantidas por revisão de final de período (asterisco).
4. **Correspondência por NCM** deve tratar a NCM do ato como indicativa (parágrafo único das resoluções) e cruzar também com a descrição do produto, por palavra-chave.
5. **Prazos** podem ser extraídos das tabelas de cronograma das circulares (arts. 59 a 63 do Decreto 8.058/2013), além dos prazos legais (10/18 meses de investigação, 5 anos de vigência).
6. **Pareceres DECOM** não têm fonte pública automatizável; o sistema deve guardar o Anexo do ato no DOU e o número do processo SEI, e tratar os autos restritos como upload manual da equipe quando a Eletros estiver habilitada.
7. **Não usar** o RSS do GECEX nem a busca web do DOU como gatilho, e tratar páginas e links do gov.br como instáveis (slugs `copy_of_`, nomes de CSV datados).
