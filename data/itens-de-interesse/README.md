# Lista inicial de itens de interesse

Extraída do Censo da Eletros (`Censo_Resumo.xlsx`, arquivo do Project "Sistema Comex Eletros"), que Renato indicou como fonte inicial de NCMs e palavras-chave em 30/10/2026.

- `insumos.csv`: 203 NCMs distintas de insumos, consolidadas das abas *PROD-IM Insumos* (compra nacional, importação, produção própria) e *Insumos Utilizados*, com até quatro descrições do censo, categoria e número de associadas que citaram cada NCM. Nomes de fornecedores e de associadas foram omitidos.
- `produtos.csv`: 122 produtos acabados (sem NCM no censo), consolidados das abas *Fabricação*, *Importação* e *Exportação*, com segmento (linha branca, linha marrom, portáteis, ar-condicionado, TIC) quando informado.
- `ncms-a-corrigir.csv`: 51 NCMs do censo com número de dígitos inválido (truncadas ou com 10+ dígitos), a corrigir antes do cadastro.

As descrições do censo servem como palavras-chave iniciais. A consolidação é mecânica: há duplicatas de grafia entre produtos (por exemplo "Lava-Louça" e "Lava-Louças") e categorias variando entre abas.
