# Acesso automatizado ao Diário Oficial da União

Pesquisa do ticket #4. Data de referência: 29/10/2026.

Pergunta: quais são os meios oficiais de acesso automatizado ao DOU (INLABS com XML, APIs, busca da Imprensa Nacional, dados abertos), com cadastro, formato, seções, horário, filtros por órgão, limites e termos de uso, e qual é o caminho mais confiável para capturar diariamente os **atos** da SECEX, do GECEX/CAMEX e do MDIC.

## Resposta curta

O único canal oficial pensado para coleta automatizada é o **INLABS** (`inlabs.in.gov.br`), mantido pela Imprensa Nacional. Ele exige cadastro gratuito com e-mail e senha e entrega, por dia e por seção, um arquivo ZIP com um XML por matéria (e também o PDF das edições). O XML traz o órgão emissor em um campo hierárquico (`artCategory`), o que permite filtrar SECEX, GECEX/CAMEX e MDIC sem raspar HTML. A busca do portal `in.gov.br/consulta` é usada por ferramentas abertas, mas é uma interface web sem contrato público de API. O projeto aberto mais maduro é o **Ro-DOU**, do Ministério da Gestão e da Inovação, que usa exatamente o INLABS como fonte de texto integral e serve de implementação de referência.

## 1. INLABS (canal recomendado)

**O que é.** Segundo o repositório oficial da Imprensa Nacional, "o objetivo do INLABS é permitir o acesso aos arquivos das edições completas do Diário Oficial da União, em formato PDF e XML, que é livre e gratuito desde o dia 1º de janeiro de 2020" [1].

**Janela temporal.** "Os dados estão disponíveis na ferramenta INLabs para os últimos 4 meses da data corrente. Para períodos anteriores, se faz necessário recorrer às coleções disponíveis na página de Dados Abertos" [1]. Para o sistema, isso significa que a captura diária precisa ser contínua, pois um atraso de mais de quatro meses obriga a recorrer a outra fonte.

**Cadastro.** O acesso exige conta criada em `https://inlabs.in.gov.br/acessar.php`. A documentação do Ro-DOU registra que "é comum o portal exibir uma mensagem de erro logo após o cadastro", e que a conta costuma ser criada mesmo assim [3]. O cadastro é por e-mail, gratuito, e não há indicação de chave de API, OAuth ou contrato [1][3].

**Mecanismo de acesso (não há API REST documentada).** Os scripts oficiais em Python e Bash mostram o fluxo [2]:

1. `POST https://inlabs.in.gov.br/logar.php` com `email` e `password` em `application/x-www-form-urlencoded`. O login bem-sucedido devolve o cookie `inlabs_session_cookie`. Credencial errada também responde HTTP 200, então o teste de sucesso é a presença do cookie [2][4].
2. `GET https://inlabs.in.gov.br/index.php?p=AAAA-MM-DD` lista os arquivos do dia (links com `title="Baixar Arquivo"`) [5].
3. `GET https://inlabs.in.gov.br/index.php?p=AAAA-MM-DD&dl=AAAA-MM-DD-DO1.zip` baixa o ZIP de uma seção, com o cabeçalho `origem: 736372697074` (hex de "script") e o cookie da sessão. HTTP 404 significa que o arquivo ainda não existe [2].

O README oficial sugere agendar o script via `crontab` "de acordo com sua necessidade" [2].

**Seções e nomes de arquivo.** XML: `DO1`, `DO2`, `DO3` (edições ordinárias) e `DO1E`, `DO2E`, `DO3E` (edições extras). PDF: `do1`, `do2`, `do3` [2]. O Ro-DOU mapeia todas as variantes de edição extra (1A, 1B, 1D etc.) e a edição suplementar para `DO1E`/`DO2E`/`DO3E` no INLABS [6].

**Estrutura do XML.** A Imprensa Nacional não publica um schema (XSD) no repositório oficial. A estrutura abaixo é a que o Ro-DOU extrai de cada XML (elemento `article` com atributos e um bloco `body`), conforme o esquema da tabela de carga [7] e o leitor `pd.read_xml(...)` + `xpath="//body"` [5]:

| Campo | Conteúdo |
|---|---|
| `id`, `idMateria`, `idOficio` | identificadores da matéria e do ofício de envio |
| `name` | nome técnico da matéria |
| `pubName` | seção (`DO1`, `DO2`, `DO3`, `DO1E`...) |
| `artType` | espécie do ato (Portaria, Resolução, Circular, Aviso...) |
| `artCategory` | hierarquia do órgão emissor, separada por `/` |
| `pubDate` | data de publicação, `DD/MM/AAAA` |
| `numberPage`, `pdfPage`, `editionNumber` | página, link para o PDF da página e número da edição |
| `artClass`, `artSize`, `artNotes`, `highlight*`, `midias` | metadados editoriais |
| `body/Identifica` | título do ato (ex.: "CIRCULAR Nº ...") |
| `body/Ementa`, `body/Titulo`, `body/SubTitulo`, `body/Data` | ementa e demais partes |
| `body/Texto` | texto integral em HTML; a assinatura aparece em `<p class="assina">` |

Os nomes de campo vêm de código de terceiros (Ro-DOU) e não de documentação da Imprensa Nacional; convém validá-los no primeiro download real.

**Filtro por órgão.** O INLABS não filtra no servidor, ele entrega a seção inteira. O filtro é feito localmente sobre `artCategory`. O Ro-DOU implementa o parâmetro `department` exatamente assim, por expressão regular sobre `artcategory` (com `unaccent`) [8], e exige que "o nome deve ser idêntico ao da publicação" [9]. Para o sistema, os prefixos relevantes provavelmente serão do tipo `Ministério do Desenvolvimento, Indústria, Comércio e Serviços/Secretaria de Comércio Exterior` e `.../Câmara de Comércio Exterior/Comitê-Executivo de Gestão`, mas as strings exatas não foram verificadas nesta pesquisa e devem ser lidas do primeiro XML baixado.

**Horário.** Nenhuma fonte oficial consultada informa a hora de disponibilização no INLABS. O que há de evidência indireta é o agendamento do Ro-DOU, que baixa o INLABS às `59 6,23 * * *` (06h59 e 23h59, horário de Brasília) [5]: a primeira execução captura a edição ordinária do dia, e a segunda captura edições extras publicadas ao longo do dia, tratadas como um evento separado (`inlabs_edicao_extra`) [5]. Os testes automatizados do Ro-DOU também procuram a edição mais recente recuando até 7 dias úteis, sinal de que a disponibilização pode atrasar [4].

**Limites e termos de uso.** Não foram encontrados limites de requisição nem termos de uso publicados para o INLABS. O README oficial apenas orienta que indisponibilidades do serviço sejam reportadas à Central de Atendimento da Imprensa Nacional, e não como issue do repositório [1]. A FAQ do Ro-DOU afirma que "os acessos são ilimitados", mas isso se refere à ferramenta, não a uma garantia da Imprensa Nacional [10]. O conteúdo do portal da Imprensa Nacional está sob licença Creative Commons Atribuição-SemDerivações 3.0 [11].

## 2. Busca do portal (`in.gov.br/consulta`)

O buscador oficial do DOU em `https://www.in.gov.br/consulta/` é a base da fonte padrão do Ro-DOU [12]. O Ro-DOU faz `GET https://www.in.gov.br/consulta/-/buscar/dou` com parâmetros `q`, `s` (seções `do1`, `do2`, `do3`, `doe`, `do1a`...), `exactDate=personalizado`, `publishFrom`/`publishTo` e `sortType`, e extrai o JSON embutido na página no `<script id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_params">`, campo `jsonArray` [13]. Cada resultado traz `pubName`, `title`, `urlTitle`, `content` (excerto), `pubDate`, `hierarchyStr`, `artType` [13].

Limitações: é uma página HTML de portal (Liferay), sem contrato de API; a paginação é limitada a 20 itens por página; o próprio código do Ro-DOU registra erro "The DOU API may have changed its structure" quando o script some [13]; o retorno é só excerto, sem texto integral [9]; e o `robots.txt` de `www.in.gov.br` bloqueia robôs de busca em páginas institucionais (verificado nesta pesquisa ao tentar ler páginas do domínio). Serve como fonte de redundância, não como fonte primária.

## 3. Dados abertos da Imprensa Nacional

A Imprensa Nacional mantém um plano de dados abertos, baseado no Decreto nº 8.777/2016, em que o DOU é o conjunto prioritário [11], e uma página "Base de Dados de Publicações do DOU" em `in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados`, à qual o README do INLABS remete para períodos anteriores a quatro meses [1]. Essa página não pôde ser lida nesta pesquisa (bloqueio de robôs), portanto formato, periodicidade e cobertura das coleções não foram confirmados. Para o sistema ela importa apenas para carga histórica, não para captura diária.

## 4. Marco normativo relevante para a captura

- O DOU é exclusivamente eletrônico, publicado no sítio da Imprensa Nacional, com acesso gratuito (Decreto nº 9.215/2017, art. 3º) [14].
- É publicado de segunda a sexta, uma vez por dia, exceto feriados nacionais e pontos facultativos no DF (Decreto nº 9.215/2017, art. 10; Portaria IN/CC/PR nº 1/2024, art. 43) [14][15].
- Edições extras e publicação em dias não previstos dependem de autorização da Secretaria Especial para Assuntos Jurídicos da Casa Civil (Decreto nº 11.823/2023, que alterou o art. 10 do Decreto nº 9.215/2017) [16].
- Atos devem ser enviados até as 19h do dia útil anterior; o que chega depois vai para a edição seguinte (Portaria IN/CC/PR nº 1/2024, art. 37) [15].
- Seção 1: atos normativos; Seção 2: atos de pessoal; Seção 3: extratos de contratos, editais, avisos, comunicados e resultados de julgamento (arts. 28 a 31) [15].

Para a Eletros, as circulares SECEX que iniciam investigações e as resoluções GECEX que aplicam direitos ou alteram alíquotas são atos de conteúdo normativo e saem na Seção 1, eventualmente em edição extra. Avisos de audiência e prazos podem aparecer na Seção 3. A captura deve portanto cobrir `DO1`, `DO1E` e `DO3` (e `DO3E`), deixando `DO2` de fora.

## 5. Projetos abertos

**Ro-DOU** (`gestaogovbr/Ro-dou`) [3]. Desenvolvido pela Secretaria de Gestão e Inovação do Ministério da Gestão e da Inovação em Serviços Públicos; licença GPL-3.0; versão 0.13.5 de 23/10/2026, com releases quase semanais em out/2026 [17]. Roda sobre Apache Airflow, lê YAML com termos, órgãos (`department`), tipos de ato (`pubtype`) e seções, e notifica por e-mail, Slack, Discord, Teams e outros [3][9][17]. Suporta três fontes: busca do portal (padrão), INLABS (texto integral carregado em Postgres, com OpenSearch opcional e resumos por IA) e Querido Diário (municípios) [3][9]. Tem testes "live" contra INLABS e DOU [4][17]. A FAQ afirma que pode ser usado por empresa privada sem custo [10].

**Imprensa-Nacional/inlabs** [1][2]. Repositório oficial, apenas com scripts-exemplo de download em Python e Bash; não é uma biblioteca.

Não foi encontrada biblioteca Python oficial ou amplamente adotada além dessas duas.

## Implicações para o sistema

- O caminho mais confiável é um coletor próprio e enxuto sobre o INLABS: login, listagem do dia, download de `DO1`, `DO1E`, `DO3` e `DO3E`, descompactação e armazenamento do XML bruto, com execução de manhã cedo e novamente à noite para pegar edições extras. É pouco código e reproduz o fluxo dos scripts oficiais [2] e do Ro-DOU [5].
- Adotar o Ro-DOU inteiro traz Airflow, Postgres e eventualmente OpenSearch, o que é infraestrutura pesada para o volume da Eletros. Ele serve melhor como referência de código e de casos de borda (edição extra, data de referência, retentativas) do que como dependência.
- A identificação do **ato** e do órgão deve partir de `artCategory`, `artType` e `Identifica` do XML. A **correspondência** com os **itens de interesse** (NCM e palavras-chave) roda sobre `Texto`, que vem em HTML e precisa de limpeza; tabelas de NCM em anexos ficam dentro desse HTML.
- O `id` da matéria permite deduplicar reprocessamentos (o Ro-DOU faz upsert por `id`) [5].
- A busca do portal pode ser um segundo canal de verificação, aceitando que ela pode quebrar sem aviso.
- Como o INLABS guarda só quatro meses, falhas prolongadas exigem alerta; o histórico anterior depende de outra fonte (dados abertos), ainda não validada.
- É preciso uma conta INLABS para o sistema, de preferência com e-mail institucional da Eletros, guardada como segredo e não no repositório.

## Lacunas desta pesquisa

Não foi possível ler diretamente `inlabs.in.gov.br` nem páginas de `www.in.gov.br` (bloqueio de robôs ou de rede). Ficaram sem confirmação em fonte oficial: horário exato de disponibilização no INLABS, eventuais termos de uso ou limites de requisição, schema oficial do XML, formato da base de dados abertos e as strings exatas de `artCategory` para SECEX e GECEX.

## Fontes

1. Imprensa Nacional, repositório `Imprensa-Nacional/inlabs`, README.md (commit de 30/09/2026). https://github.com/Imprensa-Nacional/inlabs
2. Idem, `public/python/README.md`, `public/python/inlabs-auto-download-xml.py` e `public/bash/inlabs-auto-download-xml.sh`. https://github.com/Imprensa-Nacional/inlabs/tree/master/public
3. Ro-DOU, README.md e `docs/docs/como_utilizar/instalacao.md` (seção "Usando o INLABS como fonte de dados"). https://github.com/gestaogovbr/Ro-dou
4. Ro-DOU, `tests/live/conftest.py`. https://github.com/gestaogovbr/Ro-dou/blob/main/tests/live/conftest.py
5. Ro-DOU, `dag_load_inlabs/ro_dou_inlabs_load_pg_dag.py`. https://github.com/gestaogovbr/Ro-dou/blob/main/dag_load_inlabs/ro_dou_inlabs_load_pg_dag.py
6. Ro-DOU, `src/utils/search_domains.py` (enums `Section` e `SectionINLABS`). https://github.com/gestaogovbr/Ro-dou/blob/main/src/utils/search_domains.py
7. Ro-DOU, `dag_load_inlabs/sql/init-db.sql`. https://github.com/gestaogovbr/Ro-dou/blob/main/dag_load_inlabs/sql/init-db.sql
8. Ro-DOU, `src/searchers.py` (l. 792) e `src/hooks/inlabs_hook_sql_mode.py`. https://github.com/gestaogovbr/Ro-dou/tree/main/src
9. Ro-DOU, `docs/docs/como_funciona/parametros.md`. https://gestaogovbr.github.io/Ro-dou/
10. Ro-DOU, `docs/docs/outros/faq.md`. https://gestaogovbr.github.io/Ro-dou/
11. Imprensa Nacional, "Dados abertos". https://www.gov.br/imprensanacional/pt-br/acesso-a-informacao/dados-abertos
12. Ro-DOU, `docs/docs/como_funciona/pesquisa_dou.md`. https://gestaogovbr.github.io/Ro-dou/
13. Ro-DOU, `src/hooks/dou_hook.py`. https://github.com/gestaogovbr/Ro-dou/blob/main/src/hooks/dou_hook.py
14. Decreto nº 9.215, de 29/11/2017 (texto atualizado). https://www2.camara.leg.br/legin/fed/decret/2017/decreto-9215-29-novembro-2017-785835-normaatualizada-pe.html
15. Portaria IN/CC/PR nº 1, de 2/1/2024 (DOU). https://abmes.org.br/arquivos/legislacoes/Portaria-in-cc-pr-001-2024-01-02.pdf
16. Decreto nº 11.823, de 12/12/2023. https://www2.camara.leg.br/legin/fed/decret/2023/decreto-11823-12-dezembro-2023-795059-publicacaooriginal-170416-pe.html
17. Ro-DOU, CHANGELOG.md (0.13.3 a 0.13.5, out/2026). https://github.com/gestaogovbr/Ro-dou/blob/main/CHANGELOG.md
