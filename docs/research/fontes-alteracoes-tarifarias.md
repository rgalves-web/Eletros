# Fontes públicas de alterações tarifárias

Pesquisa do ticket #3. Data da pesquisa: 29/10/2026.

Pergunta: onde e como são publicados no Brasil os atos e listas de alteração tarifária (resoluções Gecex/Camex, LETEC, ex-tarifários de BK/BIT, Lista DCC, reduções temporárias por desabastecimento, alterações da TEC no Mercosul e pleitos em análise), com formatos, estrutura, periodicidade, caminhos de coleta automatizada e listas vigentes utilizáveis na carga inicial.

Nota de método: as páginas HTML de navegação de `gov.br/mdic/.../camex` não puderam ser lidas diretamente nesta sessão (bloqueio de acesso da ferramenta), de modo que a estrutura dessas páginas foi reconstruída a partir dos PDFs oficiais hospedados no próprio domínio, das cartas de serviço em `gov.br/pt-br/servicos`, da base normativa do Mercosul e, quando indicado, de notícias especializadas que reproduzem comunicados do MDIC. Afirmações apoiadas apenas em fonte secundária estão marcadas com **(secundária)**.

## 1. Visão geral: um único ato jurídico concentra as listas

Quase todas as alíquotas do Imposto de Importação fora da TEC estão consolidadas em anexos da **Resolução Gecex nº 272, de 19/11/2021**, que é alterada continuamente por novas resoluções Gecex. Cada nova resolução de alteração tarifária diz qual anexo altera, e é esse vínculo que permite classificar o ato por instrumento.

| Anexo da Res. Gecex 272/2021 | Conteúdo | Base Mercosul |
|---|---|---|
| I | NCM e TEC (alíquotas comuns) | Decisões CMC que aprovam a TEC |
| II | Alíquotas brasileiras próprias (TEB), inclusive códigos a 28%/35% e recomposições de BK/BIT | Waivers do Mercosul |
| III | Regime tributário de produtos aeronáuticos | |
| IV | Reduções por razões de abastecimento (desabastecimento) | Res. GMC 49/19 |
| V | LETEC | Dec. CMC 11/21 e 1/25 |
| VI | LEBIT/BK (exceções de informática, telecomunicações e bens de capital) | Dec. CMC 08/21 |
| VII | Reduções temporárias Covid-19 | |
| VIII | Concessões decorrentes de compromissos na OMC (incluído pela Res. Gecex 332/2022) | |
| IX | Lista DCC (Desequilíbrios Comerciais Conjunturais) | Dec. CMC 27/15 |
| X | Lista de exceções temporárias para produtos automotivos (ACE-14) | |

Fontes: texto da Res. Gecex 272/2021 consolidado em [normasbrasil.com.br](https://www.normasbrasil.com.br/norma/resolucao-272-2021_423483.html) (secundária, reproduz o texto oficial, cobre os anexos I a VIII); Anexo IX como DCC confirmado pela Res. Gecex 941/2026 noticiada pela [CBIC](https://cbic.org.br/gecex-amplia-lista-de-produtos-com-elevacao-temporaria-das-aliquotas-de-importacao/) (secundária) e pelo [Thomson Reuters](https://www.thomsonreuters.com.br/pt/tax-accounting/comercio-exterior/blog/mecanismo-desequilibrio-comercial-mercosul.html) (secundária); Anexo X pela [Res. Gecex 927/2026](https://www.gov.br/siscomex/pt-br/informacoes/importacaoo/ResoluoGecexn.927_2026.pdf); Anexo IV pela [Res. Gecex 827/2025](https://www.normasbrasil.com.br/norma/resolucao-827-2025_487104.html) (secundária); Anexos I e II pela nota técnica oficial [SEI 1384/2026](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/240a-reuniao-ordinaria-do-comite-executivo-de-gestao-gecex/extrato-publico-da-nota-tecnica-sei-no-1384_2026-mdic.pdf).

Os ex-tarifários de BK e BIT ficam fora da Res. 272/2021. Eles são concedidos em resoluções próprias (por exemplo, Res. Gecex 322/2022 para BK, 323/2022 para BIT e 311/2022 para BK autopropulsado), que depois são alteradas por novas resoluções a cada reunião ([ata da 225ª reunião do Gecex](https://www.gov.br/mdic/pt-br/assuntos/camex/atas/gecex/2025/ata-da-225a-reuniao-ordinaria-do-gecex-de-2025.pdf)).

## 2. Ciclo de um pleito e onde cada etapa aparece

O fluxo segue o Decreto nº 10.242/2020 ([texto na Câmara](https://www2.camara.leg.br/legin/fed/decret/2020/decreto-10242-13-fevereiro-2020-789765-normaatualizada-pe.html)) e o manual da SE-Camex ([Manual de pleitos, 2ª ed.](https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/manual-pleitos-de-alteracao-tarifaria-2a-edicao-1.pdf)).

1. **Protocolo do pleito.** Empresa (e-CNPJ), associação ou órgão público preenche formulário no portal gov.br, serviço nº 1505 ([carta de serviço](https://www.gov.br/pt-br/servicos/apresentar-pleitos-de-alteracao-do-imposto-de-importacao), [formulário](http://solicitacao.servicos.gov.br/processos/iniciar?codServico=1505)). Cobre alteração definitiva da TEC (CT-1), desabastecimento, LETEC e LEBIT. Cada pleito gera um processo SEI.
2. **Publicação do pleito para manifestações.** A SE-Camex publica o pleito no site da Camex, e interessados têm **até 45 dias** para se manifestar via SEI. A página de referência é `https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/pleitos-emanalise` ([manual](https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/manual-pleitos-de-alteracao-tarifaria-2a-edicao-1.pdf)). Essa publicação **não sai no DOU**. Na prática a janela observada é de cerca de 30 dias: o pleito DCC da nota SEI 1384/2026 ficou em consulta de 19/01/2026 a 19/02/2026 ([nota técnica](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/240a-reuniao-ordinaria-do-comite-executivo-de-gestao-gecex/extrato-publico-da-nota-tecnica-sei-no-1384_2026-mdic.pdf)).
3. **Nota técnica da SE-Camex e parecer do CAT.** O Comitê de Alterações Tarifárias se reúne mensalmente (art. 4º do Decreto 10.242/2020) e tem 90 dias para recomendar ao Gecex ([manual](https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/manual-pleitos-de-alteracao-tarifaria-2a-edicao-1.pdf)). As atas do CAT são publicadas em PDF em `gov.br/mdic/pt-br/assuntos/camex/atas/cat/<ano>/` (ex.: [47ª reunião, 2024](https://www.gov.br/mdic/pt-br/assuntos/camex/atas/cat/2024/ata-da-47a-reuniao-ordinaria-do-comite-de-alteracoes-tarifarias-cat.pdf)).
4. **Deliberação do Gecex.** Reuniões ordinárias aproximadamente mensais (numeradas: 225ª em 19/05/2025, 238ª em julho/2026, 240ª em setembro/2026), mais extraordinárias. A ata é publicada em PDF em `gov.br/mdic/pt-br/assuntos/camex/atas/gecex/<ano>/ata-da-<n>a-reuniao-ordinaria-do-gecex-de-<ano>.pdf`. A pauta é organizada por instrumento (LETEC, desabastecimento, DCC, LEBIT/BK, CT-1, ex-tarifários, defesa comercial) e cada item traz processo SEI, pleiteante, NCM, Ex, descrição, alíquota antes/depois, quota e prazo ([ata da 225ª](https://www.gov.br/mdic/pt-br/assuntos/camex/atas/gecex/2025/ata-da-225a-reuniao-ordinaria-do-gecex-de-2025.pdf)).
5. **Notas técnicas públicas.** Após a reunião, a SE-Camex publica extratos públicos das notas técnicas em `gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/<reunião>/` e `.../notas/indeferimentos/<reunião>/`, em PDF, com seções fixas (I Do Pleito, II Do Produto, III Da Publicidade e das Manifestações, IV Da Análise, V Da Conclusão) ([exemplo SEI 1384/2026](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/240a-reuniao-ordinaria-do-comite-executivo-de-gestao-gecex/extrato-publico-da-nota-tecnica-sei-no-1384_2026-mdic.pdf), [exemplo de indeferimento](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/indeferimentos/232a-reuniao-ordinaria-do-comite-executivo-de-gestao-gecex/ncm-9021-90-12_implantes-vp.pdf)). Às vezes um PDF agrupa todos os deferimentos de uma resolução (ex.: [234ª reunião, Res. 864/26](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/234a-reuniao-gecex-resolucao-864-26.pdf)).
6. **Resolução Gecex no DOU.** O ato com efeito jurídico é a resolução Gecex publicada no **DOU, Seção 1**, sob o órgão Ministério do Desenvolvimento, Indústria, Comércio e Serviços / Câmara de Comércio Exterior / Comitê-Executivo de Gestão. A numeração é sequencial e contínua (941/2026 em 24/07/2026, 957/2026 em 03/09/2026). Entra em vigor geralmente na publicação ou em data fixada. O anexo traz tabela com colunas NCM, Nº Ex, Alíquota (%), Descrição, Quota, Unidade da quota, Início e Término de vigência ([Res. Gecex 927/2026](https://www.gov.br/siscomex/pt-br/informacoes/importacaoo/ResoluoGecexn.927_2026.pdf)).

Prazo para novo pleito após indeferimento: seis meses, salvo fato novo (art. 11 do Decreto 10.242/2020).

## 3. Instrumento por instrumento

### 3.1 LETEC (Anexo V)
- Base: Dec. CMC 11/21 prorrogou as listas nacionais de exceção até 31/12/2028; Dec. CMC 1/25 autorizou ampliação temporária de 50 códigos além dos 100 originais, internalizada pela Res. Gecex 752/2025 ([Machado Meyer](https://www.machadomeyer.com.br/pt/inteligencia-juridica/publicacoes-ij/tributario-ij/mercosul-autoriza-ampliacao-temporaria-da-letec), secundária; [LegisWeb sobre CMC 11/21](https://www.legisweb.com.br/noticia/?id=26319), secundária).
- Por ser lista de tamanho fixo, inclusões costumam vir acompanhadas de exclusões. A página oficial da lista é `https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/lista-de-excecoes-a-tarifa-externa-comum` ([carta de serviço](https://www.gov.br/pt-br/servicos/apresentar-pleitos-de-alteracao-do-imposto-de-importacao)).

### 3.2 LEBIT/BK (Anexo VI) e recomposição da TEC de BK/BIT (Anexo II)
- Base: Dec. CMC 08/21, waiver para BK e BIT até 31/12/2028 ([LegisWeb](https://www.legisweb.com.br/noticia/?id=26319), secundária). Pleitos pelo mesmo serviço 1505.

### 3.3 Ex-tarifários de BK e BIT (resoluções próprias)
- Regras: **Res. Gecex nº 512/2023** ([PDF oficial](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/legislacao/resolucao_gecex_n__512__2023.pdf)) e Portaria MDIC nº 265/2025, que criou o Comitê Técnico de Análise de Ex-Tarifários (CTEx) ([Teletime](https://teletime.com.br/23/10/2025/governo-cria-novos-procedimentos-para-pleitos-de-ex-tarifario/), secundária).
- Gestão pela **SDIC/MDIC** (não pela SE-Camex). Desde 2026 o pleito é apresentado no portal gov.br ([manual SDIC de 14/09/2026](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/ManualApresentaodepleitosdeExs_Gov.br_14.09.2026.pdf); [serviço de pleito](https://www.gov.br/pt-br/servicos/apresentar-pedido-referente-a-reducao-temporaria-do-imposto-de-importacao-para-bens-de-capital-bk-ou-bens-de-informatica-e-telecomunicacoes-bit); [serviço de renovação](https://www.gov.br/pt-br/servicos/renovar-ex-tarifario-para-bens-de-capital-e-bens-de-informatica-e-telecomunicacoes-bk-e-bit)).
- **Consulta pública no site do MDIC**: 30 dias corridos para concessão e alteração de redação, 20 dias para renovação. É a janela em que fabricante nacional ou associação apresenta contestação por existência de produção nacional (arts. 5º, 6º e 9º da Res. 512/2023). Para a Eletros, este é o ponto de atuação mais frequente em ex-tarifários.
- A SDIC mantém no site **lista de pleitos aprovados e indeferidos**, com número SEI, descrição, NCM, número da resolução e término de vigência (art. 24 da Res. 512/2023). Essa lista é candidata natural à carga inicial de ex-tarifários vigentes. Páginas de referência: `https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/` (ex.: [encerramento de processos](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/encerramento-de-processos-de-pleitos)).
- Volume: cada reunião do Gecex aprova dezenas a centenas de Ex (a 225ª alterou anexos com 256 BK e 20 BIT) ([ata](https://www.gov.br/mdic/pt-br/assuntos/camex/atas/gecex/2025/ata-da-225a-reuniao-ordinaria-do-gecex-de-2025.pdf)).

### 3.4 Lista DCC (Anexo IX)
- Base: **Dec. CMC 27/15** (internalizada pelo Decreto 11.895/2024) e Dec. CMC 09/21, citadas na nota técnica oficial SEI 1384/2026 ([PDF](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/240a-reuniao-ordinaria-do-comite-executivo-de-gestao-gecex/extrato-publico-da-nota-tecnica-sei-no-1384_2026-mdic.pdf)).
- Até 100 códigos NCM por Estado Parte, elevação por até 12 meses renovável, teto na alíquota consolidada na OMC ([Thomson Reuters](https://www.thomsonreuters.com.br/pt/tax-accounting/comercio-exterior/blog/mecanismo-desequilibrio-comercial-mercosul.html), secundária). A nota SEI 1384/2026 usa como critério de análise crescimento de importações acima de 30% em 48 meses.
- Exemplo recente: Res. Gecex 941/2026 (DOU 24/07/2026) elevou a 25% sete NCM de aço, vigência 27/07/2026 a 26/07/2027 ([CBIC](https://cbic.org.br/gecex-amplia-lista-de-produtos-com-elevacao-temporaria-das-aliquotas-de-importacao/), secundária).
- O pleito DCC não aparece na carta de serviço 1505, mas segue o mesmo rito de publicidade e nota técnica da SE-Camex.

### 3.5 Desabastecimento (Anexo IV)
- Base vigente: **Res. GMC 49/19** (internalizada pelo Decreto 10.291/2020; em vigor desde 05/07/2020), até 100 NCM por país, alíquota 0% ou 2%, 12 meses renováveis, sempre com quota ([ficha na base normativa do Mercosul](https://documentos.mercosur.int/public/normativas/3812); [Demarest](https://www.demarest.com.br/mercosul-adota-novas-regras-para-reducao-tarifaria-decorrente-de-desabastecimento/), secundária).
- **Mudança em curso**: a **Res. GMC 26/26** (aprovada em julho/2026) substitui a 49/19, amplia a vigência das medidas para 24 meses, encurta prazos e leva a tramitação para sistema eletrônico do Mercosul. Ainda depende de internalização ([LegisWeb/MDIC via Ideal](https://www.idealsoftwares.com.br/idealnews/noticia.php?id=33848), secundária).
- Cada redução brasileira é também uma **Diretriz CCM** registrada na base do Mercosul (ex.: [Dir. CCM 211/2025](https://normas.mercosur.int/simfiles/normativas/110786_DIR_211-2025_ES_Acciones%20Puntuales%20Ambito%20Arancelario_NCM%203909.40.91%20AR_BR-AR-PY-UY.pdf), título padrão "Acciones puntuales en el ámbito arancelario por razones de abastecimiento"). Os pleitos de outros países do bloco também aparecem ali e na pauta do Gecex.
- As quotas são distribuídas por norma complementar da Secex (art. 2º da Res. Gecex 827/2025).

### 3.6 Alterações permanentes da TEC/NCM no Mercosul (Anexo I)
- Discutidas no **Comitê Técnico nº 1 (CT-1)** do Mercosul e aprovadas por Decisão CMC ou Resolução GMC, depois incorporadas ao Anexo I da Res. 272/2021 por resolução Gecex.
- Antes de levar posição ao CT-1, a **Secex abre consulta pública por Circular Secex no DOU**, com 45 dias para contribuições, formulário próprio e e-mail `deintcgnr@mdic.gov.br`. A tabela tem colunas Situação Atual e Situação Proposta (NCM, Descrição, TEC %). As circulares e PDFs ficam em `https://www.gov.br/siscomex/pt-br/servicos/consultas-publicas/` ([Circular Secex 81/2025](https://www.gov.br/siscomex/pt-br/servicos/consultas-publicas/circular-no-81-de-20-de-outubro-de-2025); [Circular Secex 31/2026](https://www.gov.br/siscomex/pt-br/servicos/consultas-publicas/ConsultaPblicaSecexSite_versocompletaabr_2026.pdf); [versão fev/2026](https://www.gov.br/siscomex/pt-br/servicos/consultas-publicas/ConsultaPblicaSecexSite_versocompletafev_2026.pdf)). A cadência observada é de rodadas a cada poucos meses (out/2025, fev/2026, abr/2026).
- Base normativa do Mercosul: `https://normas.mercosur.int` e `https://documentos.mercosur.int/public/normativas/<id>`, com ficha estruturada (número/ano, órgão, data, arquivos, incorporação por país, vigência, concordância) ([exemplo Res. GMC 49/19](https://documentos.mercosur.int/public/normativas/3812)).

## 4. Fontes agregadas e listas vigentes para a carga inicial

| Fonte | O que entrega | Formato | Observação |
|---|---|---|---|
| **Camex360** `https://www.gov.br/mdic/pt-br/assuntos/camex/360` | Painel tarifário; painel de Mecanismos de Alteração Tarifária (NCMs em cada instrumento: LETEC, Desabastecimento, DCC etc.); painel de Pleitos (status, tempo médio); painel de Deliberações do Gecex com notas técnicas; painel com as 2.582 resoluções Camex/Gecex desde 2001, filtráveis por NCM e tema; Rastreador NCM | Painéis interativos (provável Power BI); exportação não documentada | Lançado/ampliado em jun–jul/2026 ([LegisWeb](https://www.legisweb.com.br/noticia/?id=33699), [TAGD](https://tagdlaw.com.br/novo-painel-reune-25-anos-de-decisoes-da-camex-e-facilita-busca-por-temas-e-codigos-tarifarios/), secundárias). Melhor fonte única para a carga inicial se permitir exportação. |
| Página de pleitos em análise `.../camex/estrategia-comercial/pleitos-emanalise` | Tabelas de controle de pleitos por instrumento, com prazos de manifestação | Tabelas no site (formato a confirmar) | Fonte primária do monitoramento de pleitos ([manual](https://www.gov.br/mdic/pt-br/assuntos/camex/estrategia-comercial/manual-pleitos-de-alteracao-tarifaria-2a-edicao-1.pdf)) |
| Página da LETEC `.../camex/estrategia-comercial/lista-de-excecoes-a-tarifa-externa-comum` | Lista vigente | A confirmar | |
| Lista SDIC de ex-tarifários `.../sdic/ex-tarifario/` | Ex aprovados/indeferidos com SEI, NCM, resolução, término | A confirmar (art. 24 Res. 512/2023) | |
| **Classif / Portal Único Siscomex** | Tabela NCM completa; consulta de tratamento tributário (II, Ex, antidumping) | JSON público sem captcha: `https://portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json`; XLSX no portal | ([Notícia Siscomex 20/2024](https://www.gov.br/siscomex/pt-br/noticias/noticias-siscomex-importacao/Comunicados/importacao-no-2024-020)). Base de referência para validar NCM dos itens de interesse; o download não traz alíquotas. |
| Texto consolidado da Res. Gecex 272/2021 | Todos os anexos com alíquotas | PDF/HTML | Consolidações oficiais não foram localizadas; agregadores privados mantêm versões. |

## 5. Caminhos para coleta automatizada

1. **DOU via INLABS** (`https://inlabs.in.gov.br`), da Imprensa Nacional: edições completas em XML e PDF, gratuitas desde 01/01/2020, com scripts oficiais de download automatizado em Bash e Python no repositório [Imprensa-Nacional/inlabs](https://github.com/Imprensa-Nacional/inlabs). A necessidade de cadastro/login não foi confirmada nas fontes lidas. É a via principal para capturar resoluções Gecex e circulares Secex no dia da publicação, filtrando por órgão (Câmara de Comércio Exterior / Secretaria de Comércio Exterior) e tipo de ato. O mesmo canal serve às circulares de defesa comercial.
2. **Raspagem de PDFs no gov.br/mdic**: atas do Gecex e do CAT e extratos de notas técnicas seguem padrões de URL estáveis por ano e por reunião (seção 2). São PDFs de texto (não digitalizados), adequados à extração. Atenção: a URL das atas mudou de `atas-e-resolucoes/gecex/atas/` (até ~2023) para `atas/gecex/<ano>/`.
3. **Páginas de pleitos e de consultas** (Camex, SDIC, Siscomex): HTML do Plone do gov.br, com anexos PDF. Coleta por varredura periódica e detecção de mudança. Não há API documentada nem RSS identificado.
4. **Base normativa do Mercosul** (`normas.mercosur.int`, `documentos.mercosur.int`): fichas estruturadas por norma, com PDFs. Útil para Decisões CMC, Resoluções GMC e Diretrizes CCM.
5. **Camex360**: se o painel for Power BI público, a exportação de dados pode ser limitada. Verificar manualmente antes de projetar o conector.

Periodicidade: Gecex ordinário cerca de mensal, CAT mensal, consultas públicas de ex-tarifários contínuas, consultas da TEC (Circular Secex) em rodadas de alguns meses, DOU diário. Uma varredura diária do DOU combinada com varredura semanal das páginas de pleitos/consultas cobre os prazos de 20 a 45 dias com folga.

## 6. Lacunas não resolvidas

- Não foi possível ler o HTML das páginas `pleitos-emanalise`, `lista-de-excecoes-a-tarifa-externa-comum`, Camex360 e da lista SDIC de ex-tarifários. Formato exato (HTML, XLSX ou PDF), campos e frequência de atualização precisam de verificação manual.
- Não se confirmou se o Camex360 permite exportar dados.
- A cadência real de prazos de manifestação nos pleitos (45 dias no manual, ~30 dias observados) deve ser lida em cada publicação.
- A internalização da Res. GMC 26/26 no Brasil ainda não foi localizada.
- A Res. Gecex 512/2023 citada no manual SDIC de 2026 aparece com data "16 de agosto de 2026", o que sugere nova redação ou erro material. Conferir.

## Implicações para o sistema

- **Ato** deve ter como atributos o órgão emissor (Gecex, Secex, SDIC, CMC/GMC/CCM), o tipo (resolução, circular, ata, nota técnica, diretriz) e, para resoluções Gecex, o **anexo da Res. 272/2021 alterado**, que identifica o instrumento (LETEC, DCC, desabastecimento, LEBIT/BK, TEC, automotivo). Ex-tarifários precisam de um vínculo à resolução-base (322, 323, 311 etc.).
- Cada pleito tarifário é um **Processo** com número SEI como chave natural, porque o SEI aparece no pleito publicado, na ata do Gecex, na nota técnica e na lista da SDIC. A **Correspondência** deve operar em NCM com Ex (NCM + nº Ex), já que ex-tarifários e muitas exceções são definidos no nível do destaque.
- Os **Prazos** críticos para a **Participação** da Eletros são a janela de manifestação de pleitos (até 45 dias, no site da Camex, sem DOU), a consulta pública de ex-tarifários (20 a 30 dias, no site do MDIC/SDIC) e a consulta da TEC (45 dias, por Circular Secex no DOU). Os dois primeiros só são capturáveis por varredura de páginas gov.br, não pelo DOU.
- A **Medida** tarifária tem alíquota, quota com unidade e vigência com início e término, conforme o anexo padrão das resoluções. Vencimentos de DCC (12 meses), desabastecimento (12, futuramente 24 meses) e ex-tarifários geram alertas de renovação.
- Ordem sugerida de conectores: (1) INLABS/DOU, (2) páginas de pleitos em análise e de consultas de ex-tarifários, (3) atas e notas técnicas do Gecex, (4) Circulares Secex de TEC, (5) base Mercosul. Carga inicial: Camex360 ou, na falta de exportação, anexos IV, V, VI e IX da Res. 272/2021 reconstruídos a partir das resoluções de alteração, mais a lista SDIC de ex-tarifários e o JSON NCM do Classif.
