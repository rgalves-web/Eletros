# Captura semântica em atos oficiais: abordagens comparadas

Pesquisa do ticket #6. Pergunta: quais abordagens permitem reconhecer, em atos publicados no DOU (circulares SECEX, resoluções GECEX, portarias e avisos), correspondências com itens de interesse que vão além da NCM e da palavra-chave literal, e como elas se comparam em precisão esperada, custo diário, latência, facilidade de revisão humana e explicabilidade.

Data da pesquisa: 29/10/2026. Preços e modelos mudam com frequência e devem ser reconferidos antes de qualquer decisão de contratação.

## 1. O problema em termos do domínio

Uma correspondência é o vínculo entre um ato e um item de interesse. No universo da Eletros, esse vínculo aparece de três formas no texto do ato.

1. **NCM citada expressamente.** Circulares de abertura de investigação antidumping e resoluções GECEX costumam listar os subitens da NCM no corpo ou em anexo. A dificuldade aqui é de formato ("8418.10.00", "8418.10.00 Ex 001", "84181000", "posição 84.18") e de nível de agregação, já que o item de interesse pode ser cadastrado como capítulo, posição ou subitem. Essa camada é resolvida por expressões regulares com normalização de dígitos e comparação por prefixo, sem necessidade de semântica.
2. **Produto descrito sem NCM ou com NCM residual.** Avisos, consultas públicas, pleitos de ex-tarifário e partes narrativas das circulares descrevem o produto em linguagem técnica ("compressores herméticos para refrigeração", "copolímeros de propileno", "aço laminado a frio") ou o enquadram em NCM do tipo "Outros", cuja descrição sozinha nada diz. É nessa camada que entram sinônimos, termos técnicos próximos e a relação entre descrição da NCM e texto do ato.
3. **Relação indireta entre insumo e produto acabado.** Uma medida sobre um insumo (resina, aço, motor) afeta produtos acabados das associadas sem que o ato mencione o produto acabado. Essa relação depende do cadastro do item de interesse (categoria, insumo ou produto acabado) e de conhecimento setorial, e é o ponto em que um classificador por LLM agrega mais que qualquer busca.

A camada 1 é determinística e barata. As abordagens comparadas abaixo tratam das camadas 2 e 3.

## 2. Recurso disponível: a Nomenclatura Comum do Mercosul e as Notas Explicativas

O sistema Classif do Portal Único Siscomex permite baixar a tabela da NCM em JSON e em XLSX, e o XLSX tem uma versão com **descrição concatenada**, montada automaticamente do texto do capítulo até o subitem, além de vigência e ato legal de origem de cada código. O mesmo sistema dá acesso às Notas Explicativas do Sistema Harmonizado (NESH) e às Notas Legais, por posição e capítulo ([Manual do Usuário do Classif v5.0](https://www.gov.br/siscomex/pt-br/arquivos-e-imagens/2021/07/ClassifManualdoUsuariov5.0.pdf)).

Esse material serve a quatro usos no sistema.

- **Expandir o item de interesse cadastrado como NCM.** A descrição concatenada converte "8414.30.11" em uma frase com os termos técnicos que um ato usaria para descrever o produto, o que resolve o problema dos subitens "Outros".
- **Gerar sinônimos para a busca lexical.** As NESH trazem exemplos e denominações comerciais de cada posição, que podem alimentar a lista de sinônimos revisada pela equipe.
- **Ancorar embeddings.** A descrição concatenada de cada NCM monitorada pode ser vetorizada e comparada com trechos dos atos.
- **Dar contexto ao LLM.** O prompt do classificador pode receber a descrição oficial da NCM de cada item de interesse candidato, o que reduz a dependência do conhecimento prévio do modelo.

A tabela deve ser atualizada a cada alteração da NCM (a vigência por código vem no próprio arquivo do Classif).

## 3. Volume diário a processar

Segundo a Imprensa Nacional, citada pela Agência Brasil em 2022, o DOU publica em média cerca de 500 páginas e 4.200 atos por dia, e em 2021 foram 894.879 atos em 247 edições normais e 450 extras ([Agência Brasil, 2022](https://agenciabrasil.ebc.com.br/geral/noticia/2022-09/diario-oficial-da-uniao-completa-160-anos-de-circulacao-ininterrupta)). Não encontrei estatística oficial por seção. Os atos de comércio exterior relevantes saem na Seção 1, e a Seção 3 (contratos e licitações), que é a mais volumosa, pode ser descartada antes de qualquer análise. A página de dados abertos da Imprensa Nacional, que teria a base por seção, não pôde ser lida nesta pesquisa (bloqueio de robôs).

As estimativas de custo abaixo usam dois cenários, ambos com hipóteses explícitas.

| Cenário | Atos/dia | Tokens médios por ato | Tokens de entrada/dia |
|---|---|---|---|
| Pessimista: todo o DOU vai ao classificador | 4.200 | 1.500 | 6,3 milhões |
| Realista: Seção 1 filtrada por órgão (MDIC, SECEX, CAMEX/GECEX, Receita, Inmetro) e por filtro barato | 50 a 200 candidatos | 3.000 | 0,15 a 0,6 milhão |

O número de tokens por ato é uma hipótese. Pela documentação da Anthropic, 1 milhão de tokens equivale a cerca de 2,5 milhões de caracteres no tokenizador atual ([visão geral do Claude Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/overview.md)), o que dá cerca de 3.750 caracteres para 1.500 tokens. Atos com anexos de NCM podem ser bem maiores, e o número real deve ser medido sobre uma amostra de edições assim que o acesso ao DOU (ticket #4) estiver resolvido.

## 4. Abordagens

### 4.1 Busca lexical com expansão de sinônimos

**Como funciona.** O texto do ato é indexado com analisador para português (minúsculas, remoção de acentos, radicalização), e cada palavra-chave do item de interesse é expandida por uma lista de sinônimos. O Elasticsearch, por exemplo, tem o filtro `synonym_graph`, que aceita regras de equivalência (`refrigerador, geladeira, frigorífico`) e de mapeamento explícito (`ar condicionado => condicionador de ar`), trata sinônimos de várias palavras e, com `updateable: true`, permite recarregar a lista sem reindexar ([Elastic, synonym graph token filter](https://www.elastic.co/docs/reference/text-analysis/analysis-synonym-graph-tokenfilter)). O PostgreSQL oferece dicionários de sinônimos e de tesauro com radicalizador Snowball para português, com resultado equivalente em escala pequena.

**Precisão esperada.** Alta para termos que a equipe já previu e baixa para formulações imprevistas. A literatura de recuperação de informação trata o BM25 como linha de base robusta: no benchmark BEIR, ele supera muitos modelos densos fora do domínio de treino ([Thakur et al., BEIR, 2021](https://arxiv.org/abs/2104.08663)). Em português jurídico, o JurisTCU mediu P@10 de 23,8 para BM25 puro em consultas por palavra-chave, 27,4 com expansão de sinônimos gerada por LLM e 35,4 combinando duas expansões de documento ([Fernandes et al., JurisTCU, 2025](https://arxiv.org/pdf/2503.08379)). A expansão de sinônimos melhora a cobertura de modo mensurável, mas não alcança descrições que usam vocabulário inteiramente diverso.

**Custo.** Praticamente nulo além da infraestrutura do banco de dados. O custo real é a manutenção da lista de sinônimos, que pode ser semeada uma vez por LLM a partir das descrições da NCM e das NESH e depois revisada pela equipe.

**Latência.** Milissegundos por consulta.

**Revisão humana e explicabilidade.** As melhores entre as quatro abordagens. Cada correspondência aponta o termo encontrado, a regra de sinônimo usada e o trecho do ato, o que permite destacar o trecho na tela da proposta.

### 4.2 Embeddings multilíngues ou em português

**Como funciona.** Trechos dos atos e as descrições dos itens de interesse (palavra-chave enriquecida com a descrição concatenada da NCM) são convertidos em vetores, e a correspondência é proposta quando a similaridade de cosseno passa de um limiar.

**Modelos disponíveis.** A Anthropic não oferece modelo próprio de embeddings, e seus guias usam a Voyage AI para essa etapa ([Classification with Claude](https://platform.claude.com/cookbook/capabilities-classification-guide)). A família voyage-4 tem contexto de 32 mil tokens, e os modelos `voyage-4-large` e `voyage-4` são descritos como otimizados para recuperação multilíngue; há ainda `voyage-4-nano`, de pesos abertos, e os rerankers `rerank-3` e `rerank-3-lite` ([MongoDB/Voyage, modelos](https://mongodb.com/docs/voyageai/models/)). Entre os abertos, a família multilingual-E5 (small, base, large e uma versão instruída) foi treinada em 1 bilhão de pares multilíngues e relatada como comparável aos melhores modelos só em inglês de mesmo porte ([Wang et al., 2024](https://arxiv.org/abs/2402.05672v1)), e pode rodar localmente sem custo de API.

**Precisão esperada.** Boa para paráfrases e termos técnicos próximos, com dois cuidados. Primeiro, a qualidade varia muito por modelo: no JurisTCU, os modelos BERT em português (inclusive um jurídico) ficaram abaixo do BM25, enquanto o `text-embedding-3-large` da OpenAI chegou a P@10 de 40,8, cerca de 70% acima da linha de base ([Fernandes et al., 2025](https://arxiv.org/pdf/2503.08379)). Segundo, embeddings são fracos para distinções finas que importam em defesa comercial, como a diferença entre "compressor para refrigeração" e "compressor de ar", ou entre um insumo e o produto que o contém, e tendem a errar com números de NCM. O BEIR também registra que modelos densos generalizam mal fora do domínio de treino ([Thakur et al., 2021](https://arxiv.org/abs/2104.08663)).

**Custo.** Preço de lista da Voyage por milhão de tokens: US$ 0,12 (`voyage-4-large`), US$ 0,06 (`voyage-4`), US$ 0,02 (`voyage-4-lite`), com 200 milhões de tokens gratuitos por modelo e desconto de 33% no modo batch ([Voyage AI, pricing](https://docs.voyageai.com/pricing)). No cenário pessimista (6,3 milhões de tokens/dia), o `voyage-4` custa cerca de US$ 0,38/dia, e a franquia gratuita cobre aproximadamente um mês. A vetorização da tabela NCM inteira é uma despesa única e irrisória.

**Latência.** Segundos para vetorizar a edição do dia por API, e milissegundos por consulta ao índice vetorial (por exemplo pgvector).

**Revisão humana e explicabilidade.** Fracas isoladamente. O sistema só consegue mostrar um escore de similaridade e o trecho mais próximo, sem dizer por que os dois se correspondem. O limiar precisa ser calibrado sobre exemplos rotulados, e a equipe tende a perder confiança quando um escore alto vem acompanhado de um trecho irrelevante.

### 4.3 Classificação por LLM

**Como funciona.** Cada ato (ou trecho) vai a um modelo de linguagem junto com a lista de itens de interesse, suas descrições NCM e sua classificação como insumo ou produto acabado, e o modelo devolve, em saída estruturada, os itens correspondentes, o trecho literal que fundamenta cada um, o tipo de vínculo (NCM expressa, descrição, relação insumo-produto) e um grau de confiança.

**Precisão esperada.** É a abordagem que melhor trata as camadas 2 e 3, porque lê o contexto e aplica conhecimento setorial. No guia de classificação da própria Anthropic, um classificador de 10 categorias com Claude Haiku 4.5 passou de cerca de 70% de acurácia com prompt simples para 94% com exemplos recuperados por similaridade e 97% com raciocínio explícito antes do rótulo ([Claude Cookbook, Classification with Claude](https://platform.claude.com/cookbook/capabilities-classification-guide)). Em textos jurídicos em português, Santos et al. compararam LLMs por prompt, modelos ajustados e modelos clássicos e observaram que o formato de entrada e a capacidade do modelo pesam no resultado, com resumos dando bom desempenho a menor custo de tokens ([Santos et al., ENIAC 2025](https://sol.sbc.org.br/index.php/eniac/article/view/38798)). Para referência do problema vizinho de classificar descrições em NCM, trabalhos brasileiros com aprendizado clássico chegaram a 84% de acurácia no nível de capítulo, com 50 classes e 340 mil descrições de NF-e ([Pinheiro e Amaris, 2021](https://sol.sbc.org.br/index.php/erad-eramia-no2/article/view/18671)), e de 83% a 98% com Naive Bayes conforme a dificuldade do conjunto ([iSys, 2018](https://journals-sol.sbc.org.br/index.php/isys/article/view/361)). Nenhum desses números mede a tarefa da Eletros, e a precisão real só será conhecida com um conjunto de avaliação próprio (seção 6).

Os riscos conhecidos são correspondências inventadas quando o prompt induz o modelo a sempre encontrar algo e variação entre execuções. Ambos são mitigados exigindo citação literal do trecho (verificável por comparação de texto) e permitindo a resposta "nenhuma correspondência".

**Modelos Claude e custo.** Preços de lista por milhão de tokens, entrada/saída ([Claude, pricing](https://platform.claude.com/docs/en/about-claude/pricing?m=1)):

| Modelo | Entrada | Saída | Leitura de cache | Latência comparativa |
|---|---|---|---|---|
| Claude Haiku 5.5 (prompts até 100 mil tokens) | US$ 0,10 | US$ 0,50 | US$ 0,01 | a mais rápida |
| Claude Sonnet 5.5 | US$ 2 | US$ 10 | US$ 0,10 | rápida |
| Claude Opus 5.5 | US$ 4 | US$ 20 | US$ 0,20 | moderada |
| Claude Haiku 4.5 | US$ 1 | US$ 5 | US$ 0,10 | (geração anterior) |

A API de lotes (Message Batches) dá 50% de desconto em entrada e saída, cumulativo com o cache. A maioria dos lotes termina em menos de uma hora, mas o limite é de 24 horas ([Claude, batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md)). O cache de prompt cobra a leitura a 10% do preço de entrada (5% no Sonnet 5.5 e no Opus 5.5), o que torna barato repetir em todas as chamadas a lista de itens de interesse com suas descrições NCM. Os modelos 5.5 têm contexto de 1 milhão de tokens e raciocínio adaptativo, que gera tokens de saída adicionais conforme o nível de esforço configurado ([visão geral do Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/overview.md)).

Estimativa para o cenário pessimista (4.200 atos/dia, 1.500 tokens por ato, prompt fixo de 5 mil tokens em cache, 100 tokens de saída por ato, sem contar raciocínio):

| Modelo | Custo/dia (síncrono) | Custo/dia (lote) | Custo/mês útil (22 dias, síncrono) |
|---|---|---|---|
| Haiku 5.5 | ≈ US$ 1,05 | ≈ US$ 0,53 | ≈ US$ 23 |
| Sonnet 5.5 | ≈ US$ 19 | ≈ US$ 9,50 | ≈ US$ 415 |
| Opus 5.5 | ≈ US$ 38 | ≈ US$ 19 | ≈ US$ 830 |

Cálculo para o Haiku 5.5: 6,3 M × 0,10 + 21 M (cache) × 0,01 + 0,42 M × 0,50 ≈ US$ 1,05. Os demais escalam pelos preços da tabela. Com raciocínio ativo, a saída pode crescer de 5 a 10 vezes, o que pesa no Sonnet e no Opus.

**Latência.** Alguns segundos por ato em chamada síncrona, com paralelismo limitado pelos limites de taxa da conta. A edição inteira da Seção 1 cabe em minutos. O modo lote é adequado ao resumo diário, mas o teto de 24 horas o torna inadequado ao alerta imediato.

**Revisão humana e explicabilidade.** Boas quando a saída é estruturada: a proposta mostra o item, o trecho citado e uma justificativa curta, e a equipe confirma ou rejeita. A justificativa é gerada pelo modelo e pode ser plausível sem estar correta, por isso a citação literal verificada é o elemento que sustenta a revisão.

### 4.4 Pipelines híbridos (filtro barato seguido de LLM)

**Como funciona.** Uma cascata em que cada etapa reduz o volume da seguinte.

1. **Recorte estrutural.** Apenas Seção 1 e edições extras, e apenas órgãos de interesse (MDIC/SECEX, CAMEX/GECEX, Receita Federal, Inmetro, MAPA), usando os metadados do ato. Se o XML do INLABS trouxer seção e hierarquia do órgão por ato, como se espera, esse recorte é trivial (a confirmar no ticket #4).
2. **Camada determinística.** Regex de NCM por prefixo e busca lexical com sinônimos. Correspondência por NCM expressa vira proposta direta, sem LLM.
3. **Camada semântica de recall.** Embeddings comparando os trechos restantes com as descrições enriquecidas dos itens de interesse, com limiar baixo para não perder candidatos.
4. **Julgamento por LLM.** Somente os candidatos das etapas 2 e 3 (e, opcionalmente, todo ato dos órgãos-chave, que são poucos) vão ao Claude, que confirma, descarta ou acrescenta correspondências e produz a justificativa com citação.

**Precisão esperada.** A melhor relação entre cobertura e precisão. O relato da Anthropic sobre recuperação contextual mostra o efeito da combinação: em busca top-20, embeddings sozinhos reduziram a taxa de falha em 35%, embeddings com BM25 em 49% e a adição de reranking em 67% (de 5,7% para 1,9%) ([Anthropic, Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)). O mesmo texto observa que bases de conhecimento menores que 200 mil tokens podem ir inteiras no prompt com cache, o que se aplica à lista de itens de interesse da Eletros, que dificilmente chegará a esse tamanho.

**Custo.** No cenário realista (50 a 200 candidatos/dia, 3.000 tokens cada, 500 tokens de saída), o Sonnet 5.5 custa entre US$ 0,55 e US$ 2,20 por dia, e o Haiku 5.5 alguns centavos. Somando embeddings, o custo total fica na casa de dezenas de dólares por mês mesmo com o Sonnet.

**Latência.** Dominada pela etapa de LLM sobre poucos candidatos, portanto da ordem de um a poucos minutos por edição em modo síncrono, compatível com alerta imediato.

**Revisão humana e explicabilidade.** Cada proposta pode registrar a etapa que a gerou (NCM expressa, sinônimo, similaridade, julgamento do LLM), o que ajuda a equipe a calibrar a confiança e a priorizar a revisão. O risco próprio do híbrido é a perda de recall no filtro: um ato descartado na etapa 1 ou 3 nunca chega ao LLM, e por isso o limiar das etapas iniciais deve ser frouxo.

## 5. Quadro comparativo

| Critério | Lexical + sinônimos | Embeddings | LLM sobre tudo | Híbrido |
|---|---|---|---|---|
| Precisão (camada 2) | média, depende da lista | média a boa, depende do modelo | boa | boa |
| Recall (camada 2) | baixo para termos imprevistos | bom | bom | bom, se o filtro for frouxo |
| Relação insumo-produto (camada 3) | só se cadastrada | fraca | boa | boa |
| Custo/dia, cenário pessimista | ≈ 0 | ≈ US$ 0,40 | US$ 1 (Haiku 5.5) a US$ 38 (Opus 5.5) | US$ 0,05 a 2,50 |
| Latência | ms | segundos | minutos (síncrono) ou até 24 h (lote) | minutos |
| Revisão humana | muito fácil | difícil | fácil, com citação | fácil, com origem da proposta |
| Explicabilidade | total | escore opaco | justificativa gerada | origem + justificativa |
| Manutenção | lista de sinônimos | limiar e reindexação | prompt e conjunto de avaliação | todas as anteriores, em menor grau |

## 6. Lacunas e como medir

- **Não há medida publicada para esta tarefa.** Os números citados vêm de tarefas vizinhas (recuperação jurídica, classificação de tickets, classificação em NCM). A forma de obter precisão e recall reais é montar um conjunto de avaliação com atos históricos da Seção 1 dos últimos 12 a 24 meses, anotados pela equipe com as correspondências corretas, e rodar as quatro abordagens sobre ele.
- **Volume por seção do DOU.** Só há o número agregado de 4.200 atos/dia. O volume real da Seção 1 e o tamanho médio dos atos devem ser medidos com o acesso automatizado do ticket #4.
- **Metadados do XML do INLABS.** A viabilidade do recorte por órgão depende de o XML trazer seção e hierarquia do órgão por ato, o que não foi possível confirmar no README nesta pesquisa.
- **Atos com anexos longos.** Resoluções GECEX com listas extensas de NCM podem exigir divisão em trechos, mas a camada determinística resolve a maior parte delas antes do LLM.

## 7. Recomendação preliminar e implicações

**Recomendação.** Adotar o pipeline híbrido, com a camada determinística de NCM como base, busca lexical com sinônimos semeados a partir das descrições concatenadas da NCM e das NESH, embeddings como rede de recall e Claude como juiz final dos candidatos, com saída estruturada contendo item, tipo de vínculo, trecho citado e confiança. O Haiku 5.5 é o candidato natural para o julgamento por custo e latência, e o Sonnet 5.5 pode ser reservado para atos dos órgãos-chave ou para casos em que o Haiku indique baixa confiança. Ambos devem ser comparados no conjunto de avaliação antes da escolha.

O custo de LLM deixa de ser fator decisivo. Mesmo o cenário pessimista com Haiku 5.5 sobre o DOU inteiro fica perto de US$ 25 por mês, e o híbrido com Sonnet 5.5 fica em dezenas de dólares. O fator decisivo passa a ser a qualidade do cadastro dos itens de interesse e a existência de um conjunto de avaliação.

**Implicações para o sistema.**

- O cadastro do item de interesse deve guardar, além do código ou da palavra-chave, a descrição oficial da NCM, sinônimos aprovados e, para insumos, os produtos acabados afetados, porque é esse material que alimenta todas as camadas.
- A tabela NCM do Classif, com descrições concatenadas e vigências, passa a ser uma fonte de dados do sistema, com rotina de atualização.
- Toda correspondência proposta por camada semântica entra como proposta, nunca como correspondência confirmada, e registra a etapa de origem e o trecho citado, o que se alinha à premissa de que o agente propõe e a equipe confirma.
- O alerta imediato exige chamadas síncronas ao LLM, e o modo lote fica restrito ao reprocessamento e ao resumo diário.
- A rejeição de propostas pela equipe é um dado valioso e deve ser guardada para recalibrar limiares, sinônimos e exemplos do prompt.

## Fontes

- Agência Brasil. [Diário Oficial da União completa 160 anos de circulação ininterrupta](https://agenciabrasil.ebc.com.br/geral/noticia/2022-09/diario-oficial-da-uniao-completa-160-anos-de-circulacao-ininterrupta), 2022.
- Anthropic. [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval).
- Anthropic. [Pricing](https://platform.claude.com/docs/en/about-claude/pricing?m=1), [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing.md), [Claude Sonnet 5.5 overview](https://platform.claude.com/docs/en/models/sonnet-5-5/overview.md), [Classification with Claude](https://platform.claude.com/cookbook/capabilities-classification-guide). Consultados em 29/10/2026.
- Elastic. [Synonym graph token filter](https://www.elastic.co/docs/reference/text-analysis/analysis-synonym-graph-tokenfilter).
- Fernandes, L. C. et al. [JurisTCU: A Brazilian Portuguese Information Retrieval Dataset with Query Relevance Judgments](https://arxiv.org/pdf/2503.08379), 2025.
- Imprensa Nacional. [Repositório inlabs](https://github.com/Imprensa-Nacional) (acesso gratuito às edições completas do DOU desde 01/01/2020).
- MongoDB / Voyage AI. [Modelos Voyage](https://mongodb.com/docs/voyageai/models/); Voyage AI. [Pricing](https://docs.voyageai.com/pricing).
- Pinheiro, P.; Amaris, M. [Classificação dos Códigos de NCM Usando Processamento de Linguagem Natural](https://sol.sbc.org.br/index.php/erad-eramia-no2/article/view/18671), ERAD/ERAMIA-NO 2021.
- [Automatic Classification of NCM Codes Using the Naïve Bayes Algorithm](https://journals-sol.sbc.org.br/index.php/isys/article/view/361), iSys, 2018.
- Portal Único Siscomex. [Manual do Usuário do Classif v5.0](https://www.gov.br/siscomex/pt-br/arquivos-e-imagens/2021/07/ClassifManualdoUsuariov5.0.pdf), 2021.
- Santos, W. F. et al. [Comparing Prompt-based LLMs, Fine-Tuning, and Classical Models for Legal Text Classification in Portuguese](https://sol.sbc.org.br/index.php/eniac/article/view/38798), ENIAC 2025.
- Thakur, N. et al. [BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- Wang, L. et al. [Multilingual E5 Text Embeddings: A Technical Report](https://arxiv.org/abs/2402.05672v1), 2024.
