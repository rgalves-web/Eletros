# ADR-0001: Cérebro em Markdown versionado como fonte única da verdade

**Data**: 2026-11-04
**Status**: aceito
**Decidido em**: [Entrevista: estrutura do cérebro](https://github.com/rgalves-web/eletros/issues/17)

## Contexto

A entrevista de regras de correspondência (#9) fixou que todo julgamento é do agente, apoiado num cérebro no modelo LLM wiki (Karpathy), e que o banco relacional guarda só o índice operacional. Faltava decidir onde vivem os campos estruturados (prazos, status, NCMs, vigência): no banco, com a página só em prosa, ou na própria página.

## Decisão

O cérebro é um repositório git próprio (`eletros-cerebro`), só Markdown com frontmatter YAML e wikilinks, com `index.md`, `log.md` e `schema.md` na raiz. Os campos estruturados ficam no frontmatter de cada página. O banco relacional é derivado: um indexador o reconstrói a partir do frontmatter a cada mudança de página, e ninguém o edita diretamente. Um validador rejeita escritas que violem `schema.md`.

A equipe edita pelo editor da aplicação web (frontmatter como formulário, corpo como texto, trava otimista por versão, commit em nome do usuário). O agente escreve direto só em `propostas/`, na camada de fontes brutas e nas páginas de síntese; nas demais páginas só aplica o conteúdo de propostas confirmadas, em commit atômico.

## Alternativas rejeitadas

- **Banco como fonte dos campos, página só para texto**: obriga a equipe a editar em dois lugares e cria divergência entre ficha e página, justamente o que o cérebro existe para evitar.
- **Agente escrevendo direto nas páginas definitivas**: viola a regra de não auto-confirmação de #9.
- **Edição pela equipe via Obsidian ou GitHub**: exige git de uma equipe de comércio exterior e deixa o frontmatter sem validação.

## Consequências

- O sistema precisa de indexador, validador de esquema e lint periódico do cérebro.
- O banco pode ser recriado do zero a qualquer momento a partir do repositório.
- Custo de leitura por ato fica previsível: ato, índice, esquema e as páginas que o índice indicar.
