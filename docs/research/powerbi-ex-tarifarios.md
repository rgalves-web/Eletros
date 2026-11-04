# Extração automatizada do painel Power BI de ex-tarifários (SDIC)

Pesquisa do ticket #15. Data: 04/11/2026.

Pergunta: qual é o painel Power BI em que o SDIC/MDIC publica as consultas públicas de ex-tarifários de BK e BIT, se ele é público ou autenticado, quais campos traz, e qual é o caminho confiável para extrair seus dados de forma automatizada. Pedia-se também testar a extração a partir do ambiente do agente.

## Resumo

1. O painel é um relatório **"Publicar na web" público**, sem login: `https://app.powerbi.com/view?r=eyJrIjoiMzM3ZmNhOTAtZDZmOC00OGYzLWJjZmYtNzNlNWU5NWFiYzZmIiwidCI6IjQ1NjIxM2NmLTcwNzMtNDdjNi1iZjQ5LTQxYjY1NGFkNDQ5YiJ9`, publicado na página [Consulta Pública do SDIC](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/consulta-publica) com o título "Painel Consultas Públicas — Plataforma completa com informações relacionadas às consultas públicas do Ex-Tarifário". O parâmetro `r` decodificado em base64 é `{"k":"337fca90-d6f8-48f3-bcff-73e5e95abc6f","t":"456213cf-7073-47c6-bf49-41b654ad449b"}`, em que `k` é a chave de recurso pública do relatório e `t` o locatário (tenant) Azure AD do MDIC.
2. Um único painel cobre os pleitos de **BK e BIT**, tanto os protocolados no SEI (identificados pelo **código SDIC**) quanto os protocolados no Portal de Serviços gov.br a partir de 01/10/2026 (identificados pelo **número de protocolo**, que é também a referência para a contestação). Não foi localizado painel separado para autopeças.
3. Relatórios "Publicar na web" **não oferecem "Exportar dados"** ao visitante. A extração confiável passa pela API interna que o próprio visualizador usa: `POST https://wabi-<região>-api.analysis.windows.net/public/reports/querydata?synchronous=true`, com o cabeçalho `X-PowerBI-ResourceKey: <k>` e um corpo `SemanticQueryDataShapeCommand` com paginação por `RestartTokens`.
4. O caminho recomendado tem duas etapas: (a) um navegador sem interface (Playwright) abre o painel e **captura** as consultas `querydata` que os visuais disparam, e (b) um cliente HTTP **reenvia** essas consultas paginando até o fim e decodifica a resposta (formato DSR) em linhas. Há uma ferramenta de código aberto que faz exatamente isso ([cameronaaron/powerbi-extract](https://github.com/cameronaaron/powerbi-extract), Python, AGPL-3.0, commit de 11/10/2026).
5. **A extração não pôde ser testada daqui.** O proxy de saída deste ambiente recusa `app.powerbi.com`, `*.analysis.windows.net` e `www.gov.br` (`CONNECT tunnel failed, response 403`; no Chromium, `net::ERR_TUNNEL_CONNECTION_FAILED`). O script do spike está pronto em [`spike/pbi_ex_tarifarios.py`](../../spike/pbi_ex_tarifarios.py) e precisa rodar uma vez na máquina do usuário (passos na seção 5).
6. Os campos efetivamente expostos pelo painel (NCM, descrição do Ex, pleiteante, datas, prazo de contestação, situação) e o volume de linhas **não foram verificados**, porque o painel não pôde ser aberto. O script grava o esquema do modelo e uma captura de tela, o que resolve essa lacuna no primeiro teste.

## 1. O painel

| Item | Valor | Fonte |
|---|---|---|
| Página que publica o painel | `gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/consulta-publica` | [SDIC, Consulta Pública](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/consulta-publica) |
| URL do painel | `app.powerbi.com/view?r=eyJrIjoiMzM3ZmNh…` (completa no Resumo) | idem |
| Tipo | "Publicar na web" (formato `view?r=`), público, sem autenticação | formato da URL; [README do powerbi-extract](https://github.com/cameronaaron/powerbi-extract) |
| Escopo | Pleitos de concessão, alteração, renovação e revogação de Ex de BK e BIT | página do SDIC |
| Identificadores | Código SDIC (pleitos via SEI) e nº de protocolo do Portal gov.br (pleitos a partir de 01/10/2026) | página do SDIC |
| Contestação | Serviço "[Apresentar manifestação de produção nacional (contestação)](https://www.gov.br/pt-br/servicos/apresentar-manifestacao-de-producao-nacional-contestacao/view)", obrigatório para pleitos do Portal | página do SDIC |
| Material associado | [Notas Referenciais](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/consulta-publica/notas-referenciais-3) (PDF por produto, como a de inversores fotovoltaicos de maio/2026, segundo o [Canal Solar](https://canalsolar.com.br/mdic-consulta-producao-nacionak-ex-tarifarios-inversores/), secundária) | página do SDIC |
| Prazo de contestação | Não informado na página nem no [Manual de pleitos de 14/09/2026](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/ManualApresentaodepleitosdeExs_Gov.br_14.09.2026.pdf), que remete à Resolução Gecex nº 512 e ao e-mail extarifario@mdic.gov.br | manual |
| Frequência de atualização | Não declarada. Em "Publicar na web" o cache leva cerca de uma hora para refletir uma atualização do conjunto de dados, e a própria Microsoft desaconselha o recurso para dados de atualização frequente | [Fabric Community, resposta aceita citando a documentação](https://community.fabric.microsoft.com/t5/Service/How-often-does-a-report-refresh-its-data-when-using-the-publish/td-p/2493049) |

**Autopeças.** Os Ex de autopeças correm em regime próprio (Regime de Autopeças Não Produzidas, Resolução Gecex nº 284/2021, com serviço "[Obter redução em tarifas de importação de autopeças](https://www.gov.br/pt-br/servicos/obter-reducao-em-tarifas-de-importacao-de-autopecas)"). Não se encontrou painel Power BI para eles, e o tema tem baixa aderência ao setor da Eletros.

## 2. Como o visualizador público conversa com o serviço

O fluxo abaixo é o que um relatório `view?r=` executa no navegador. Os pontos marcados como verificados vêm do código-fonte do powerbi-extract (lido, não executado); os demais são o comportamento conhecido do visualizador e serão confirmados pela captura do spike.

1. O navegador decodifica `r` e obtém a chave `k`. A partir dela, o serviço resolve o cluster regional do locatário, um host `wabi-<região>-…analysis.windows.net` (para o MDIC, provavelmente Brazil South; a ferramenta usa `wabi-west-us-c-primary-api` só como padrão). *Não verificado.*
2. `GET …/public/reports/<k>/modelsAndExploration?preferReadOnlySession=true` devolve o modelo (id do conjunto de dados, `modelId`) e a definição do relatório: páginas, visuais e, em cada visual, o `prototypeQuery` que ele consulta. `POST …/public/reports/conceptualschema` devolve tabelas e colunas do modelo. *Não verificado; o script grava ambas as respostas.*
3. Cada visual dispara `POST …/public/reports/querydata?synchronous=true` com os cabeçalhos `X-PowerBI-ResourceKey: <k>`, `Origin`/`Referer: https://app.powerbi.com`, e um corpo `{"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{…}}]},"ApplicationContext":{"DatasetId":…,"Sources":[{"ReportId":…,"VisualId":…}]}}],"cancelQueries":[],"modelId":…}`. *Verificado em [`client.py`](https://github.com/cameronaaron/powerbi-extract/blob/main/powerbi_extract/client.py).*
4. Visuais de tabela pedem linhas em janelas: `Binding.DataReduction.Primary.Window.Count`. A resposta traz `RT` (restart tokens), que se devolve em `Window.RestartTokens` para obter a janela seguinte; páginas consecutivas repetem uma linha na emenda. *Verificado em `client.py`.*
5. A resposta vem no formato compacto DSR: `results[0].result.data.dsr.DS[0].PH[0].DM0` é a lista de linhas; `S` define o esquema, `C` traz os valores na ordem, o bit *i* de `R` repete o campo *i* da linha anterior, o bit *i* de `Ø` torna-o nulo, e inteiros de campos com `DN` indexam `ValueDicts`. Os nomes das colunas estão em `data.descriptor.Select`. *Verificado em [`dsr_parser.py`](https://github.com/cameronaaron/powerbi-extract/blob/main/powerbi_extract/dsr_parser.py).*

Duas observações do mesmo código importam para a robustez. A consulta capturada deve ser **reenviada literalmente**, alterando só a janela de paginação, porque consultas reconstruídas ou com `modelId` errado recebem 401 mesmo com chave válida. E sessões anônimas também respondem 401/403 sob rajadas de requisições, de modo que só uma nova tentativa com espera distingue limitação de taxa de chave revogada.

## 3. Alternativas de extração

| Abordagem | Como funciona | Prós | Contras |
|---|---|---|---|
| **Captura + reenvio (recomendada)** | Playwright abre o painel uma vez, grava as consultas `querydata`; um cliente HTTP repete-as paginando por `RestartTokens` | Linhas completas, sem depender do que está visível na tela; reenvio barato e diário; descoberta refeita automaticamente se o relatório mudar | Usa API não documentada; a consulta só existe para colunas que algum visual exibe |
| Só navegador (raspar o DOM) | Playwright rola a tabela e lê as células renderizadas | Simples de entender | Frágil: tabelas virtualizadas, textos truncados, dependência de layout e idioma |
| Só HTTP, montando a consulta a partir de `modelsAndExploration` | Lê o `prototypeQuery` de cada visual e envia sem navegador | Dispensa Chromium no servidor | Mais código, e consultas reconstruídas podem receber 401 (ver seção 2) |
| "Exportar dados" | Botão do visual | Oficial | **Indisponível** em "Publicar na web" ([Fabric Community](https://community.fabric.microsoft.com/t5/Service/Publish-to-Web-Export-to-Pdf-button-Download-Data-link/td-p/3422078)) |
| API REST oficial do Power BI | `executeQueries` etc. | Documentada | Exige credencial do workspace do MDIC; inaplicável |
| Pedido formal ao SDIC (LAI / dados abertos) | Solicitar a base em CSV/XLSX | Fonte estável | Prazo e resposta incertos; complementar, não substituto |

**Ferramenta pronta.** O [powerbi-extract](https://github.com/cameronaaron/powerbi-extract) implementa a abordagem recomendada (`powerbi-extract-auto --url "<view url>"`), com repetição em 429/5xx, falha explícita em chave morta e escrita só de tabelas completas. Por ser **AGPL-3.0**, usá-lo como serviço modificado obriga a publicar o código. O spike deste ticket foi escrito do zero, só com a biblioteca padrão e o Playwright, para não herdar essa obrigação.

## 4. Fontes equivalentes ou complementares

- **Ex-tarifários vigentes (XLSX, ~4 MB)** em [PDA de ex-tarifários](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/pda-de-ex-tarifarios/ex-tarifarios-vigentes.xlsx/view): retrato dos Ex em vigor, não dos pleitos em consulta. Já registrado em `fontes-documentos-acompanhamento.md` como defasado (atualizado em 03/07/2025).
- **Pleitos indeferidos de BK e BIT**: planilha oficial do MDIC com atualização mensal, segundo o [Buscador Ex-Tarifário](https://buscadorextarifario.com.br/fontes) (secundária; URL oficial não localizada).
- **DOU**: as Resoluções Gecex que concedem, alteram ou revogam Ex encerram o processo, mas a consulta pública em si não é publicada no DOU. Servem para fechar o histórico do processo, não para o prazo de contestação.
- **Antes de 01/10/2026**, a consulta pública era publicada em planilhas XLSX semanais com "Data de publicação" e "Prazo para Contestação" por linha ([ABIMO](https://abimo.org.br/servicos/consulta-publica-mdic/consulta-publica-ex-tarifario/), secundária). Não há indício de que continuem sendo publicadas.
- **Agregadores privados** (Buscador Ex-Tarifário sincroniza duas vezes por dia) cobrem vigentes e resoluções, e não mencionam a consulta pública.

Nenhuma delas substitui o painel para o que a Eletros precisa, que é ver os pleitos **em consulta** com o prazo de contestação aberto.

## 5. Teste na máquina do usuário (pendente)

O teste exige um computador com acesso normal à internet e Python 3.9+.

1. Copiar `spike/pbi_ex_tarifarios.py` do branch `research/powerbi-ex-tarifarios`.
2. `pip install playwright` e `python -m playwright install chromium`.
3. `python pbi_ex_tarifarios.py all --out saida_pbi --wait 12`.
4. Conferir: `saida_pbi/painel.png` (captura de tela do painel), `saida_pbi/raw/` (pedidos e respostas de `modelsAndExploration`, `conceptualschema` e `querydata`) e `saida_pbi/tables/*.csv` (uma tabela por visual de tabela, com todas as páginas).
5. Devolver ao repositório (ou anexar ao #15) a pasta `saida_pbi`. Ela contém só dados públicos do painel.

Alternativa sem instalar nada: abrir o painel no Chrome, F12 → aba Rede, filtrar por `querydata`, navegar por todas as páginas do painel e rolar as tabelas, e salvar com "Save all as HAR". O HAR permite montar o reenvio sem o passo de captura.

Se o teste falhar no passo 3 com 401/403 persistente, o painel deixou de ser público ou trocou de chave; se `tables/` vier vazio, o painel usa visuais de matriz (formato DSR com `X`), que o spike ainda não decodifica.

Outra via é liberar `app.powerbi.com` e `*.analysis.windows.net` (e `www.gov.br`) na lista de domínios permitidos do ambiente de agentes (claude.ai → Settings → Capabilities, ou o administrador da organização). Com isso o teste roda aqui mesmo.

## 6. Volumes e riscos de quebra

- **Volume**: não verificado. Como ordem de grandeza, o governo trabalhava em 2025 com cerca de 9 mil Ex vigentes ([Autodata, abr/2025](https://www.autodata.com.br/noticias/2025/04/22/governo-buscara-reduzir-pela-metade-os-atuais-9-mil-ex-tarifarios/87048/), secundária); os pleitos em consulta a cada momento devem ser uma fração disso, o que cabe com folga em poucas janelas de 500 linhas.
- **Republicação do relatório**: se o SDIC apagar e recriar o código de inserção, `k` muda e a URL na página do gov.br também. Mitigação: ler a URL do painel na página do SDIC a cada execução, em vez de fixá-la.
- **Mudança de layout ou de modelo**: novos visuais, colunas renomeadas ou `modelId` diferente invalidam as consultas gravadas. Mitigação: refazer a captura com o navegador quando o reenvio falhar ou o esquema mudar, e comparar o `conceptualschema` com o da execução anterior.
- **API não documentada**: a Microsoft pode alterar `querydata` ou o formato DSR. O risco é real, mas o formato está estável há anos e é o mesmo usado por todos os relatórios públicos.
- **Limitação de taxa**: respostas 401/403/429 em rajadas. Mitigação: uma execução por dia, espera exponencial, sem paralelismo.
- **Defasagem**: o cache de "Publicar na web" pode atrasar até cerca de uma hora em relação ao conjunto de dados; irrelevante para prazos contados em dias.
- **Política de uso**: o painel é público e oficial; a extração lê o mesmo que o visitante vê, uma vez por dia. Convém registrar no sistema a data e a hora de cada captura como prova do que estava publicado.

## Implicações para o sistema

1. O conector de ex-tarifários deve ser um **coletor em duas etapas**: descoberta com navegador sem interface (Playwright, quando necessário) e coleta diária por HTTP reenviando as consultas `querydata` gravadas. O navegador só volta a rodar quando o reenvio falhar ou o esquema mudar.
2. Cada captura gera um **documento de acompanhamento** do tipo "consulta pública SDIC", com data de captura, hash e arquivo bruto (respostas JSON e CSV), como previsto em `fontes-documentos-acompanhamento.md`.
3. Cada linha do painel vira ou atualiza um **processo** do tipo pleito de ex-tarifário, identificado pelo **código SDIC** ou pelo **número de protocolo** gov.br, conforme a origem. A **correspondência** com os itens de interesse se faz pela NCM e pela descrição do Ex, e o **prazo** de contestação alimenta o calendário da equipe.
4. A detecção de mudança compara o conjunto de chaves (código SDIC/protocolo) e os campos de situação e prazo entre capturas: entradas novas geram alerta; mudanças de situação entram no histórico do processo.
5. A URL do painel não deve ser fixada no código: o coletor lê a página do SDIC e extrai o link `app.powerbi.com/view?r=`, alertando a equipe se ele mudar ou desaparecer.
6. O ambiente onde o coletor rodar precisa de saída liberada para `www.gov.br`, `app.powerbi.com` e `*.analysis.windows.net`, além do Chromium do Playwright para a etapa de descoberta.
7. Enquanto o teste na máquina do usuário não for feito, a prioridade 2 de ex-tarifários continua **bloqueada pela verificação de campos e volume**, não mais pela viabilidade técnica, que está documentada.

## Fontes

- Primárias: [SDIC, Consulta Pública de ex-tarifários](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/consulta-publica); [Manual de pleitos SDIC, 14/09/2026](https://www.gov.br/mdic/pt-br/assuntos/sdic/ex-tarifario/ManualApresentaodepleitosdeExs_Gov.br_14.09.2026.pdf); [Serviço de contestação](https://www.gov.br/pt-br/servicos/apresentar-manifestacao-de-producao-nacional-contestacao/view); código-fonte de [cameronaaron/powerbi-extract](https://github.com/cameronaaron/powerbi-extract) (`client.py`, `discover.py`, `browser.py`, `dsr_parser.py`, commit `ae7431e`, 11/10/2026).
- Comunidade Microsoft (Fabric Community, citando a documentação "Publish to web"): [atualização e cache](https://community.fabric.microsoft.com/t5/Service/How-often-does-a-report-refresh-its-data-when-using-the-publish/td-p/2493049); [ausência de exportação de dados](https://community.fabric.microsoft.com/t5/Service/Publish-to-Web-Export-to-Pdf-button-Download-Data-link/td-p/3422078). A página oficial do Microsoft Learn não pôde ser aberta deste ambiente.
- Secundárias: [ABIMO](https://abimo.org.br/servicos/consulta-publica-mdic/consulta-publica-ex-tarifario/); [Buscador Ex-Tarifário, fontes](https://buscadorextarifario.com.br/fontes); [Canal Solar, 06/05/2026](https://canalsolar.com.br/mdic-consulta-producao-nacionak-ex-tarifarios-inversores/); [Autodata, 22/04/2025](https://www.autodata.com.br/noticias/2025/04/22/governo-buscara-reduzir-pela-metade-os-atuais-9-mil-ex-tarifarios/87048/).
- Teste de rede deste ambiente (04/11/2026): `curl` a `app.powerbi.com`, `wabi-brazil-south-b-primary-redirect.analysis.windows.net` e `www.gov.br` → `CONNECT tunnel failed, response 403`; Playwright → `net::ERR_TUNNEL_CONNECTION_FAILED`.
