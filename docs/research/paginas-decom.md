# Páginas de processos em curso e de medidas em vigor do DECOM

Pesquisa da issue #16. Data da verificação: 04/11/2026. As datas "Publicado em" e "Atualizado em" citadas foram lidas nas próprias páginas nessa data.

Pergunta: o site do DECOM no gov.br mostra, para cada **processo** em curso e cada **medida** em vigor, o andamento e os **atos**. Quais são essas páginas, como estão estruturadas, que campos trazem, com que frequência mudam, que histórico guardam e como coletá-las automaticamente com detecção de mudança? Servem para a carga inicial e para alimentar o **histórico do processo** junto com o DOU?

Complementa, sem repetir, [fontes de defesa comercial](https://github.com/rgalves-web/eletros/blob/research/fontes-defesa-comercial/docs/research/fontes-defesa-comercial.md) (#2, que descreveu as duas tabelas-índice e os CSV de dados abertos) e [fontes de documentos de acompanhamento](https://github.com/rgalves-web/eletros/blob/research/fontes-documentos-acompanhamento/docs/research/fontes-documentos-acompanhamento.md) (#14).

**Nota de método.** O shell desta sessão não alcança `gov.br`, `web.archive.org`, `in.gov.br` nem `legisweb.com.br` (o proxy responde 403 ao CONNECT; Playwright, que usa o mesmo proxy, não muda isso). A ferramenta de leitura web só abre URLs que tenham aparecido em resultado de busca, e o buscador indexa poucas páginas de caso. Foram lidas integralmente **sete páginas**: as duas listas, a página "Suspensões e alterações por Interesse Público", o índice e a página 2026 de "Publicações do DECOM no D.O.U." e **três páginas de caso** (uma investigação em curso, uma encerrada e uma medida em vigor). A estrutura do HTML abaixo é a descrita pela ferramenta de leitura, que converte a página em texto; nomes de classes CSS e IDs não puderam ser vistos. O que ficou sem verificação está na seção 6.

## Resposta curta

1. O DECOM mantém, no Plone do gov.br, **dois índices em tabela HTML** ("Investigações de Defesa Comercial em curso", 45 linhas; "Medidas de defesa comercial em vigor", 94 linhas) e **uma página por caso**, ligada a partir de cada linha. Há ainda a tabela de "Suspensões e alterações por Interesse Público em vigor" (8 linhas) e a lista anual "Publicações do DECOM no D.O.U." (2019 a 2026).
2. A **página de caso de investigação** traz, em listas com rótulos em negrito: tipo de investigação, **NCM**, países de origem, peticionárias, data de início, e-mail do caso, **processos SEI** (restrito e confidencial), **documentos públicos** (cada ato com link para o DOU, data do DOU e resumo de uma linha), cronograma em tabela (arts. 59 a 63 do Decreto 8.058/2013) quando já publicado, resumo do parecer em PDF, questionários em ZIP, **prazos de resposta aos questionários** e, ao final, "Situação Atual da investigação".
3. A **página de caso de medida** traz: tipo de medida, NCM, país de origem, "Publicações no Diário Oficial da União" (toda a cadeia de atos desde a aplicação original, com links para o DOU), resumo do parecer, "Direito Aplicado", "Prazo de Vigência" e "Processos relacionados".
4. Para a Eletros, o valor dessas páginas está em **dois campos que nenhuma outra fonte estruturada dá**: a lista de atos já ligada ao caso (o DOU publica atos soltos, e o CSV traz só o nome do ato em texto) e os **prazos de questionário e de habilitação**, que saem da circular de início mas aparecem prontos na página. Também é a única fonte pública que liga o caso ao par de **processos SEI**.
5. As páginas são **mantidas à mão e atrasam**: a página de compressores recíprocos foi atualizada em 18/05/2026 e não mostra nenhum ato depois da circular de início; a página de cadeados exibe "Prazo de Vigência: 24/10/2025" enquanto o índice e a resolução de prorrogação já indicam 24/10/2030; a lista "Publicações do DECOM em 2026" estava atualizada em 01/10/2026, mas o trecho legível terminava em junho. Os campos não seguem um rótulo único ("Países de Origem", "País investigado", "País de Origem"; "Peticionárias"/"Peticionária").
6. **Conclusão**: as páginas servem como **fonte complementar** da carga inicial (para NCM, processos SEI e cadeia de atos dos casos que interessam à Eletros) e como **conferência** do histórico do processo, mas não como gatilho. O gatilho continua sendo o DOU (INLABS), e o ato do DOU é sempre a fonte de verdade; a página entra como evidência secundária, com detecção de mudança por "Atualizado em" e hash do bloco de conteúdo.

## 1. Mapa das páginas

Raiz: `https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/` (abaixo, `<raiz>`).

| Página | URL | Formato | "Atualizado em" (lido em 04/11/2026) | Conteúdo |
|---|---|---|---|---|
| Investigações em curso (índice) | [`<raiz>investigacoes/investigacoes-de-defesa-comercial`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/investigacoes/investigacoes-de-defesa-comercial) | Tabela HTML | 01/10/2026 09h23 (publicada em 26/06/2020) | 45 linhas: PRODUTO, INVESTIGAÇÃO, ORIGEM, COORDENAÇÃO RESPONSÁVEL; tabela "Outros procedimentos" (PRODUTO, TIPO), 3 linhas |
| Página de caso (investigação) | `<raiz>investigacoes/investigacoes-de-defesa-comercial/<slug>` | Listas com rótulos em negrito; uma tabela de cronograma quando houver | Varia por caso | Seção 2 |
| Medidas em vigor (índice) | [`<raiz>medidas-em-vigor/medidas-em-vigor`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/medidas-em-vigor/medidas-em-vigor) | Tabela HTML | 09/10/2026 15h28 (publicada em 26/06/2020) | 94 linhas: PRODUTO, MEDIDA (DAD, DAP, MCD, compromisso de preço), ORIGEM, PRAZO DE VIGÊNCIA |
| Página de caso (medida) | `<raiz>medidas-em-vigor/medidas-em-vigor/<slug>` | Listas com rótulos; sem tabela | Varia por caso | Seção 3 |
| Suspensões e alterações por interesse público | [`<raiz>medidas-em-vigor/suspensoes-por-interesse-publico-em-vigor`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/medidas-em-vigor/suspensoes-por-interesse-publico-em-vigor) | Tabela HTML | 18/09/2026 16h00 | 8 linhas: MEDIDA, PRODUTO, PAÍS DE ORIGEM, TIPO (medida alterada / medida suspensa), FIM DA SUSPENSÃO/ALTERAÇÃO (link para a resolução no DOU) |
| Publicações do DECOM no D.O.U. (índice anual) | [`<raiz>publicacoes-do-decom-no-diario-oficial-da-uniao`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/publicacoes-do-decom-no-diario-oficial-da-uniao) | Lista de links | Sem carimbo | Um link por ano, de 2019 a 2026 |
| Publicações do DECOM em 2026 | [`.../publicacoes-do-decom-em-2026`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/publicacoes-do-decom-no-diario-oficial-da-uniao/publicacoes-do-decom-em-2026) | Lista com marcadores | 01/10/2026 09h16 | Um item por ato: título com link para o DOU, data do DOU e resumo (seção 4) |

**Padrão dos slugs.** O slug é livre, escolhido por quem cadastra a página, com sufixos informais que indicam o tipo: `-dp` (dumping, investigação original), `-rvd`/`-rev`/`-rfp` (revisão), `-rdt` (redeterminação), `-acv` (anticircunvenção), `-mdc` (alteração de circunstâncias), `-cvd` (subsídios), `-id`, `-md`. Não há regra: a investigação de compressores é `compressores-reciprocos`, sem sufixo. Há slugs herdados de cópia (`copy_of_acrilato-de-butila-dp` para Resina PP, `copy11_of_modelo-pagina` para tubos de borracha elastomérica), erros de grafia (`clinindros-gnv-rev`, `cilindos-gnv`) e um link fora da pasta (`.../defesa-comercial/medidas-de-defesa-comercial-e-interesse-publico-em-vigor/copy_of_medidas-em-vigor/tubos-com-costura-de-aco-inoxidavel-austenitico`). **O slug não serve como chave**; a chave do caso tem de ser o par de processos SEI ou, na falta, produto + origem + tipo.

**Investigação e medida são páginas distintas.** A revisão de final de período de ventiladores de mesa tem página em `investigacoes/.../ventiladores-de-mesa-rvd` e a medida resultante tem página em `medidas-em-vigor/medidas-em-vigor/ventiladores-de-mesa`. Não há link explícito entre as duas no conteúdo lido. A ligação no sistema tem de ser feita por produto + origem + NCM ou pelo ato (a resolução que encerra a revisão aparece nas duas).

**Casos encerrados não saem da pasta.** A página de ventiladores de mesa continua publicada com o sufixo "(encerrada)" no título e no H1 e com "Situação Atual da investigação: Encerrada". Ela sai do índice, mas continua acessível pela URL. Na tabela de investigações em curso aparecem, como texto dentro de algumas células, URLs de casos que já não estão na lista (`acos-pre-pintados-rvd`, `fibras-opticas`, `fios-de-nailon`, `laminados-planos-a-frio`, `pvcs-rvd`, `vidros-de-seguranca-rvd`), resto de edição manual que indica a existência de páginas de casos encerrados ainda publicadas.

## 2. Página de caso de investigação

### 2.1 Compressores recíprocos para refrigeração (investigação em curso)

[`.../investigacoes-de-defesa-comercial/compressores-reciprocos`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/investigacoes/investigacoes-de-defesa-comercial/compressores-reciprocos). "Publicado em 01/12/2025 07h22", "Atualizado em 18/05/2026 08h09". Coordenação no índice: CGAC.

Ordem dos blocos, cada um com rótulo em negrito seguido de lista com marcadores (sem tabela):

1. **Informações gerais sobre a investigação de defesa comercial**: Tipo de Investigação: Antidumping · NCM: 8414.30.11 · Países de Origem: China · Peticionárias: Nidec Global Appliance Brasil Ltda · Início da Investigação: 30/04/2026 · Esclarecimentos adicionais: compressores@mdic.gov.br.
2. **Processos**: 19972.002380/2025-14 (restrito) · 19972.002405/2025-80 (confidencial).
3. **Documentos públicos da investigação**: um link sem texto para `http://www.in.gov.br/web/dou/-/circular-n-17-de-9-de-marco-de-2026-691503204` e o link "CIRCULAR Nº 34, DE 29 DE ABRIL DE 2026" para `https://www.in.gov.br/web/dou/-/circular-n-34-de-29-de-abril-de-2026-702424365`, seguido de "DOU de 30/04/2026" e de um resumo (inicia a investigação; cita os dois processos SEI).
4. **Questionários (RETIFICADOS)**: Exportador, Importador, Terceiro País, Produtor Nacional, em ZIP sob `.../investigacoes-de-defesa-comercial/arquivos/questionarios/` (ex.: `061Q.EXP.ANXQuestionriodoExportador.zip`).
5. **Prazo para resposta aos questionários**: Habilitação de outras partes 25/05/2026 · Exportador selecionado sem prorrogação 17/06/2026, com prorrogação 17/07/2026 · Produtor de terceiro país 17/07/2026 (recomendável) · Resposta voluntária de exportador 17/06/2026 · Importador 15/06/2026, com prorrogação 13/07/2026 · Produtor nacional 15/06/2026, com prorrogação 13/07/2026.

Não há campo de fase, de cronograma nem de situação. Em seis meses de página publicada, só aparecem a circular de início e uma circular anterior (nº 17, de 09/03/2026, cujo objeto a página não descreve). Qualquer ato posterior a maio de 2026 (cronograma, prorrogação, determinação preliminar) **não estava na página** em 04/11/2026.

### 2.2 Ventiladores de mesa (revisão encerrada)

[`.../investigacoes-de-defesa-comercial/ventiladores-de-mesa-rvd`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/investigacoes/investigacoes-de-defesa-comercial/ventiladores-de-mesa-rvd). "Publicado em 01/03/2024 10h03", "Atualizado em 30/05/2025 12h59". Título "Ventiladores de mesa (encerrada)".

Mesma estrutura, com três blocos a mais, o que mostra o modelo completo da página:

1. **Informações gerais**: Tipo de Investigação: Dumping Revisão · NCM: 8414.51.10 · País investigado: China · Peticionária: SEB do Brasil Produtos Domésticos Ltda., SEB Comercial de Produtos Domésticos Ltda. e MK Eletrodomésticos Mondial S.A. · Início da investigação: 01/07/2024 · ventiladores@mdic.gov.br.
2. **Cronograma** (a única tabela, três colunas: "Disposição legal (Decreto nº 8.058/2013)", "Prazo", "Data prevista"): art. 59 encerramento da fase probatória 20/12/2024 · art. 60 manifestação sobre os dados 13/01/2025 · art. 61 nota técnica de fatos essenciais 12/02/2025 · art. 62 manifestações finais e encerramento da instrução 06/03/2025 · art. 63 parecer de determinação final 26/03/2025.
3. **Processos**: 19972.000218/2024-81 (restrito) · 19972.000217/2024-36 (confidencial).
4. **Documentos públicos da investigação**, em ordem cronológica, cada item com link, "DOU de dd/mm/aaaa" e resumo: Circular nº 28/2024 (início, DOU 01/07/2024) · Circular nº 66/2024 (prazos, DOU 21/11/2024) · Circular nº 20/2025 (prorroga para doze meses, DOU 19/03/2025) · Resolução GECEX nº 725/2025 (prorroga o direito por até cinco anos, DOU 21/05/2025).
5. **Resumos do caso**: "Resumo do parecer de início" em PDF sob `.../investigacoes-de-defesa-comercial/arquivos/resumos/`.
6. **Questionários** e 7. **Prazo para resposta aos questionários**, como em 2.1.
8. **Situação Atual da investigação**: Encerrada.

O cronograma da página reproduz a tabela da circular de prazos (Circular nº 66/2024) e não é atualizado quando a circular seguinte prorroga a investigação: os rótulos continuam "Data prevista".

### 2.3 Campos de uma página de investigação

| Campo pedido na issue | Presente? | Onde e como |
|---|---|---|
| Produto | Sim | Só no título/H1 (não há rótulo "Produto") |
| NCM | Sim | "NCM:" em Informações gerais; uma ou mais NCMs em texto |
| Origens | Sim | "Países de Origem" ou "País investigado"; texto livre |
| Peticionária | Sim | "Peticionária(s)"; texto livre |
| Tipo | Sim | "Tipo de Investigação" (texto livre: "Antidumping", "Dumping Revisão"); o índice traz outra grafia ("Dumping (revisão)") |
| Número SEI | Sim | Bloco "Processos": restrito e confidencial |
| Fase | Não | Só "Situação Atual da investigação" (visto apenas como "Encerrada") e, indiretamente, o último ato da lista |
| Atos | Sim | "Documentos públicos": título do ato, link para `in.gov.br/web/dou/-/<slug>-<id>`, data do DOU, resumo; ordem cronológica |
| Cronograma | Às vezes | Tabela arts. 59–63 depois da circular de prazos; sem atualização em prorrogações |
| Prazos | Sim | "Prazo para resposta aos questionários" e habilitação de partes |
| Coordenação | Não na página | Só no índice (CGAC, CGAR, CGMC, CGSA) |
| Contato | Sim | E-mail do caso |
| Pareceres / notas técnicas | Parcial | Só o resumo do parecer de início (press release) em PDF; nota técnica de fatos essenciais e pareceres finais não aparecem |

## 3. Página de caso de medida

### 3.1 Cadeados (medida em vigor)

[`.../medidas-em-vigor/medidas-em-vigor/cadeados`](https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial-e-interesse-publico/medidas-em-vigor/medidas-em-vigor/cadeados). "Publicado em 11/05/2016 17h39", "Atualizado em 28/10/2025 09h53".

1. **Informações gerais**: Tipo de Medida: Direito Antidumping Definitivo · NCM: 8301.10.00 · País de Origem: China.
2. **Publicações no Diário Oficial da União** (lista, cada item com link, data do DOU e resumo de uma linha), cobrindo toda a vida da medida: Resolução CAMEX nº 95 (DOU 13/11/2013, prorrogação) · Resolução GECEX nº 9 (DOU 13/11/2019, prorrogação com suspensão imediata) · Resolução GECEX nº 7 (DOU 03/02/2020, indefere reconsideração) · Circular SECEX nº 67/2020 (DOU 08/10/2020, avaliação para retomar a cobrança) · Resolução GECEX nº 142/2020 (reaplicação) · Resolução GECEX nº 803/2025 (DOU 24/10/2025, prorrogação por até cinco anos). Os links usam três formatos: `pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?data=...&jornal=1&pagina=17` (até 2013), `in.gov.br/web/dou/-/<slug>-<id>` e `in.gov.br/en/web/dou/-/<slug>-<id>`.
3. **Resumos do caso**: "Resumo do parecer de determinação final", PDF em `/mdic/pt-br/images/REPOSITORIO/secex/decom/Resumos_pareceres/...`.
4. **Direito Aplicado**: US$10,11/kg (valor único, sem tabela por produtor/exportador).
5. **Prazo de Vigência**: 24/10/2025.
6. **Processos relacionados**: três Portarias SECEX de 2013–2014 sobre origem não preferencial, em PDF.

Não há processos SEI. O "Prazo de Vigência" da página (24/10/2025) **contradiz** o índice (24/10/2030) e o último ato da própria lista (prorrogação de 24/10/2025): a página recebeu o ato novo, mas o campo de vigência ficou com o valor antigo. Isso confirma que os campos derivados são editados à mão e podem divergir dos atos listados.

### 3.2 Campos de uma página de medida

Tipo de medida, NCM, país de origem, cadeia de atos com links para o DOU, resumo do parecer, direito aplicado, prazo de vigência, processos relacionados. Não verificado se as medidas com vários produtores trazem tabela de alíquotas por empresa; a de cadeados tem alíquota única.

### 3.3 Índice de medidas: sinais que só existem nele

- Asterisco no prazo: "medida em vigor por força de revisão de final de período em curso, nos termos do art. 105, § 2º do Decreto 8.058/2013" (15 linhas em 04/11/2026, entre elas tubos de borracha elastomérica e seringas descartáveis).
- Notas entre parênteses: "cobrança suspensa para <origem>" ou "cobrança suspensa por interesse público".
- Vigência por linha, já atualizada (cadeados: 24/10/2030).
- Linha malformada: "Porcelanato técnico" aparece só como link, sem medida, origem ou prazo, colado à linha de aço inoxidável laminado a frio.

Medidas do setor eletroeletrônico presentes em 04/11/2026: ventiladores de mesa (China, 20/05/2030), vidros para eletrodomésticos da linha fria (China, 24/06/2031), alto-falantes (China, 28/11/2030), polióis poliéteres (China e EUA, 04/07/2030), aço GNO (alterado por interesse público). Investigações em curso do setor: compressores recíprocos (China) e vidros temperados para eletrodomésticos da linha quente e molhada (China).

## 4. Lista anual "Publicações do DECOM no D.O.U."

- Índice com um link por ano, de 2019 a 2026, sem carimbo de data. Slug: `publicacoes-do-decom-em-<ano>`.
- A página de 2026 é uma **lista** (não tabela). Cada item: título do ato em caixa alta com link para o DOU, "DOU de dd/mm/aaaa" e um resumo copiado da ementa. Abrange circulares SECEX e resoluções GECEX de defesa comercial e interesse público, inclusive republicações (marcadas "(*)") e retificações (link `pesquisa.in.gov.br/...&jornal=515&pagina=40`).
- O resumo **nem sempre nomeia produto e origem** (ex.: Circular nº 10, Circular nº 29, as resoluções de reconsideração nº 859, 877–880 e 889 citam empresas, mas não produto). Para ligar o item ao caso é preciso abrir o ato.
- A leitura alcançou 65 itens, de janeiro a 22/06/2026 (Circular nº 44), e foi **cortada pela ferramenta** no meio do último resumo. Não foi possível confirmar se a página contém os atos de julho a outubro (a numeração das circulares chegou à nº 104 em 20/10/2026, segundo #2), embora o carimbo seja de 01/10/2026.
- Erros de cadastro: o item 1 tem título "CIRCULAR Nº 1, DE 5 DE JANEIRO DE 2025" para um ato publicado em 06/01/2026.

Uso: é uma lista curada de atos do DECOM por ano, útil para **conferir a cobertura do filtro do DOU** (todo ato da lista deve ter sido capturado pelo coletor INLABS) e para carga histórica de 2019 em diante. Não é gatilho, porque é atualizada em lote.

## 5. Frequência de atualização e confiabilidade

| Página | Evidência de atualização | Avaliação |
|---|---|---|
| Índice de investigações | 01/10/2026; abertura de compressores (30/04/2026) já está na lista | Atualizado em lotes, semanas depois dos atos |
| Índice de medidas | 09/10/2026; vigência de cadeados já ajustada a 2030 | Mais atual que o CSV de medidas (de 05/2025, ver #2) |
| Página de caso, investigação | Compressores: última edição 18/05/2026, nenhum ato posterior listado | Atualização irregular, por caso; atos intermediários podem faltar |
| Página de caso, medida | Cadeados: ato de 24/10/2025 incluído em 28/10/2025, mas o campo de vigência não foi corrigido | Atualização rápida da lista de atos, campos derivados pouco confiáveis |
| Publicações do DECOM 2026 | Carimbo 01/10/2026; trecho lido termina em junho | Atualização em lote; cobertura a confirmar |

Nenhuma página declara periodicidade. O carimbo "Atualizado em" do Plone muda a cada edição, mesmo pequena, e é o melhor indicador de mudança disponível sem baixar a página inteira. Não foi encontrado feed RSS que funcione para essas pastas (a URL `.../investigacoes-de-defesa-comercial/RSS` não pôde ser testada); em #2 o RSS do GECEX se mostrou defasado.

## 6. Coleta automatizada com detecção de mudança

Proposta, condicionada aos testes da seção 7:

1. **Varredura dos índices** (diária ou a cada dois dias): baixar as duas tabelas e a de interesse público, guardar o HTML bruto e o carimbo "Atualizado em". Extrair as linhas (produto, tipo/medida, origem, coordenação/vigência, href). Diff linha a linha com a captura anterior: linha nova = **proposta** de processo ou medida; linha que sumiu = indício de encerramento ou de extinção a confirmar no DOU; mudança de vigência ou de asterisco = **proposta** de evento da medida.
2. **Varredura das páginas de caso** dos itens de interesse (e de todas as linhas, na carga inicial): baixar a página, isolar o bloco de conteúdo principal (descartar menus, rodapé e barra de compartilhamento, que mudam sem relação com o caso), normalizar espaços e calcular hash. Reprocessar só quando o carimbo ou o hash mudar.
3. **Parser por rótulo, não por posição**: localizar os blocos pelos rótulos em negrito ("Informações gerais", "Processos", "Documentos públicos da investigação", "Publicações no Diário Oficial da União", "Cronograma", "Prazo para resposta aos questionários", "Situação Atual da investigação", "Direito Aplicado", "Prazo de Vigência"), com tabela de sinônimos para variações ("País investigado" / "Países de Origem" / "País de Origem"). Campo não reconhecido gera alerta, não erro silencioso.
4. **Extração dos atos**: de cada link para `in.gov.br`, tirar tipo, número e data do título e o identificador numérico final do slug (ex.: `702424365`). Ligar esse ato ao ato já capturado do INLABS por tipo + número + ano (e pelo identificador, se o XML do INLABS o trouxer, a confirmar). Ato listado na página que não existe na base = alerta de falha do coletor do DOU.
5. **Chave do caso**: par de processos SEI quando existir; senão, produto + origem + tipo. Nunca o slug.
6. **Anexos**: guardar o resumo do parecer (PDF) e registrar os questionários (ZIP) apenas como link, para não versionar arquivos grandes.

A página de caso é evidência secundária: tudo que ela traz e que mude o estado de um processo (novo ato, novo prazo, situação "Encerrada") entra como **proposta** e só é confirmado quando o ato correspondente do DOU estiver na base ou quando a equipe aprovar.

## 7. O que não foi verificado

- **Acesso a partir do servidor do sistema.** Esta sessão não alcançou `gov.br` pelo shell. É preciso testar, do ambiente de produção, `curl` simples, cabeçalho `User-Agent` de navegador e Playwright, e verificar se o gov.br aplica limitação de taxa ou desafio anti-robô às páginas do DECOM (em #2, as páginas individuais de resolução GECEX tinham `robots_disallowed`).
- **API do Plone** (`++api++` / plone.restapi) e feed RSS das pastas `investigacoes-de-defesa-comercial` e `medidas-em-vigor`: se disponíveis, dariam JSON com `modified` por página e listagem da pasta, inclusive de casos encerrados. Não testado.
- **HTML real** (classes, IDs, se os rótulos são `<strong>` dentro de `<p>` ou `<li>`): a ferramenta de leitura entrega texto convertido. Conferir no primeiro protótipo do parser.
- **Página de caso de investigação com determinação preliminar, direito provisório ou nota técnica**, e página de medida com **alíquotas por produtor/exportador**: não localizadas pela busca. Em particular, não foi possível abrir a página de vidros temperados para eletrodomésticos (`.../vidros-temperados-eletrodomesticos`), nem as de medida de vidros da linha fria e de ventiladores de mesa.
- **Objeto da Circular SECEX nº 17/2026**, listada sem título na página de compressores.
- **Cobertura da página "Publicações do DECOM em 2026"** depois de junho (leitura truncada) e conteúdo das páginas de 2019 a 2025.
- **Listagem dos casos encerrados**: não há índice público verificado; as páginas encerradas só são achadas pela URL.
- **"Estatísticas e Histórico"**: não localizada pela busca.

## Implicações para o sistema

1. **Fonte de verdade continua sendo o DOU.** As páginas do DECOM entram como **documento de acompanhamento** de natureza secundária: alimentam propostas e conferências, nunca alteram sozinhas o estado de um processo ou de uma medida.
2. **Carga inicial em três camadas**: (a) CSV "Base de investigações" (#2) para o universo de processos e medidas desde 1990; (b) **índices HTML** para o retrato atual (o índice de medidas é mais novo que o CSV de medidas e traz o asterisco do art. 105, § 2º); (c) **páginas de caso** dos itens de interesse da Eletros, para buscar NCM, processos SEI, peticionárias e a cadeia de atos com links, o que reduz a necessidade de procurar cada ato antigo no DOU. Tudo entra como **proposta**.
3. **Histórico do processo**: a lista "Documentos públicos" / "Publicações no DOU" de cada página é a reconstituição oficial da cadeia de atos do caso. O sistema deve usá-la para **conferir** o histórico montado a partir do DOU (ato faltando de um lado ou de outro gera alerta) e para preencher o histórico anterior a 2020, que o INLABS não cobre.
4. **Prazos**: a página dá prontos os prazos de questionário e de habilitação de partes e, depois da circular de prazos, o cronograma dos arts. 59 a 63. O sistema deve extrair esses valores como **prazos** propostos, mas o cálculo a partir da circular no DOU tem precedência, porque a página não acompanha prorrogações.
5. **Modelo de dados**: um processo precisa aceitar **dois ou mais números SEI** (restrito e confidencial), um e-mail de contato do caso e a coordenação do DECOM; a medida precisa guardar o indicador "em vigor por força de revisão" e a "cobrança suspensa" por origem, que hoje só existem no índice HTML. Investigação e medida são entidades distintas, ligadas pelo ato que encerra uma e aplica ou prorroga a outra.
6. **Coletor HTML com parser tolerante**: rótulos com sinônimos, chave por SEI e não por slug, detecção de mudança por "Atualizado em" mais hash do bloco de conteúdo, alerta quando um bloco esperado sumir ou um rótulo novo aparecer. Frequência diária para os índices e para as páginas dos casos acompanhados; semanal para o restante.
7. **Divergência como sinal**: diferença entre página e DOU (ex.: vigência de cadeados) não deve ser corrigida automaticamente; vira alerta para a equipe e, se for erro do MDIC, pode ser objeto de contato com o e-mail do caso.
8. **Antes de implementar**: testar o acesso do servidor ao gov.br, a API do Plone e o RSS das pastas, e ler uma página de caso em fase avançada e uma de medida com alíquotas por empresa (seção 7).
