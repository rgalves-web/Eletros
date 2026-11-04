# Sistema Comex Eletros

Monitoramento e gestão, pela equipe de comércio exterior da Eletros, dos processos brasileiros de alteração tarifária e de defesa comercial que afetam insumos e produtos acabados do setor eletroeletrônico.

## Itens monitorados

**Item de interesse**:
Uma NCM, em qualquer nível de agregação, ou uma palavra-chave que a Eletros quer acompanhar. Cada um é classificado como insumo ou produto acabado e pertence a uma categoria.
_Avoid_: produto monitorado, alvo, termo

**Insumo**:
Item de interesse usado como matéria-prima ou componente na fabricação de produtos do setor.
_Avoid_: matéria-prima, componente (como rótulo de classificação)

**Produto acabado**:
Item de interesse que é ele próprio um bem final fabricado ou comercializado pelas associadas.
_Avoid_: produto final, eletro

**Correspondência**:
Vínculo identificado pelo agente entre um ato e um item de interesse ou um processo já cadastrado, seja por NCM, por palavra-chave, por chave do processo ou por termo semanticamente próximo. Toda correspondência traz nível de confiança, trecho literal do ato e justificativa.
_Avoid_: match, hit, ocorrência

**Nível de confiança**:
Juízo do agente sobre uma correspondência, entre alta, média e baixa, que a equipe pode reclassificar ao confirmar. Determina se a proposta gera alerta imediato ou espera o resumo diário.
_Avoid_: escore, score, probabilidade

**Ex pertinente**:
Ex criado ou alterado numa NCM de interesse cuja descrição alcança um produto fabricado ou um insumo comprado pelas associadas, segundo o agente. Distingue-se do Ex na mesma NCM, que só compartilha a classificação.
_Avoid_: Ex relevante, Ex da Eletros

**Ex**:
Recorte de uma NCM por descrição específica de mercadoria, com alíquota diferenciada (menor ou maior) da prevista para a NCM, como um ex-tarifário de BK/BIT ou um Ex de LETEC. Um item de interesse pode ser a NCM raiz ou a NCM com um Ex.
_Avoid_: ex-tarifário (como termo genérico), subitem

**Destaque**:
Código que identifica um Ex no Siscomex para fins de tratamento administrativo e licenciamento de importação, condição para usufruir da alíquota diferenciada.
_Avoid_: Ex (quando se fala do código operacional)

## Processos e medidas

**Processo**:
Procedimento administrativo brasileiro de defesa comercial ou de alteração tarifária, com fases e prazos, como uma investigação antidumping, uma revisão ou um pleito de inclusão na LETEC.
_Avoid_: caso, investigação (como termo genérico), pleito (como termo genérico)

**Medida**:
Resultado em vigor de um processo, com prazo de vigência, como um direito antidumping aplicado ou uma alíquota alterada.
_Avoid_: medida vigente (redundante), direito, tarifa

**Ato**:
Publicação oficial que inicia, movimenta ou encerra um processo ou uma medida, como uma circular SECEX, uma resolução GECEX ou um aviso no DOU.
_Avoid_: publicação, norma, documento

**Prazo**:
Data-limite para um ato dentro de um processo. Por regra decorre do regulamento do tipo de processo (prazo regulamentar) e pode ser substituída por prazo impróprio ou convencional quando houver; a equipe também pode fixar prazos internos.
_Avoid_: deadline, vencimento, vigência

**Prazo regulamentar**:
Prazo previsto na norma que rege o tipo de processo, calculado a partir de um evento do próprio processo.
_Avoid_: prazo legal (quando a fonte é infralegal), prazo padrão

**Vigência**:
Período durante o qual uma medida produz efeitos, do início ao término ou à renovação. Distinta dos prazos do processo que a originou.
_Avoid_: prazo da medida, validade

**Tipo de processo**:
Procedimento previsto em regulamento para um instituto de defesa comercial ou de política tarifária, com fases e prazos regulamentares próprios, como a revisão de final de período de um direito antidumping ou o pleito de inclusão na LETEC.
_Avoid_: modalidade, categoria de processo

**Incidente**:
Procedimento com prazos próprios que corre dentro de um processo principal, como o compromisso de preços, o direito provisório, a habilitação de indústria fragmentada ou o recurso.
_Avoid_: subprocesso, procedimento acessório

**Evento da medida**:
Fato que altera a vigência ou as condições de uma medida existente, como prorrogação, suspensão por interesse público, reaplicação, redeterminação ou revogação.
_Avoid_: nova medida, alteração (como termo genérico)

**Documento de acompanhamento**:
Publicação oficial fora do DOU que registra a tramitação de um processo, como ata do CAT ou do Gecex, planilha de acompanhamento de pleitos ou nota técnica.
_Avoid_: sinal antecipado, anexo, documento auxiliar

**Histórico do processo**:
Registro cronológico de todos os atos, documentos de acompanhamento e eventos da participação de um processo, que permite reconstituir a sua tramitação.
_Avoid_: linha do tempo, log

## Atuação da Eletros

**Participação**:
O envolvimento da Eletros em um processo, abrangendo posição, habilitação como parte interessada, manifestações, associadas envolvidas e responsáveis internos.
_Avoid_: atuação, engajamento, acompanhamento (como termo genérico)

**Posição**:
O lado que a Eletros adota em um processo, entre apoio, oposição e acompanhamento.
_Avoid_: estratégia, interesse

**Manifestação**:
Peça protocolada pela Eletros em um processo, com seus documentos.
_Avoid_: petição, submissão, contribuição

**Cérebro**:
Base de conhecimento viva, em documentos editáveis, que o agente consulta e atualiza antes de propor: páginas por item de interesse, tipo de processo, processo e medida, mais o registro das decisões da equipe com motivo.
_Avoid_: base de conhecimento (como termo genérico), memória, wiki

**Proposta**:
Cadastro ou atualização de processo, medida ou correspondência sugerida pelo agente e ainda não confirmada pela equipe.
_Avoid_: sugestão, rascunho, pendência
