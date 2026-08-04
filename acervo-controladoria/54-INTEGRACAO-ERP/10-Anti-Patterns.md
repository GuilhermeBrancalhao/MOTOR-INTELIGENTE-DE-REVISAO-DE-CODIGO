---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Filtrar coluna candidata por `is_numeric_dtype` sem converter primeiro.** É o bug real
corrigido neste volume: toda coluna monetária de banco brasileiro chega como texto com vírgula
decimal, então esse filtro exclui a coluna certa e deixa sobrar só coluna vazia — que passa no
mesmo filtro por ter dtype numérico, mesmo sem conter nenhum valor real. `_para_numerico()`
existe para nunca mais reintroduzir esse padrão; ver `07-Regras.md`.

**Escolher a primeira coluna que casa com o padrão de nome, sem desempate.** Era o comportamento
original de `detectar_colunas()` antes da correção: quando duas colunas casam com o mesmo padrão
(`% da Comissão` e `Valor Comiss`, ambas contêm `comiss`), a ordem das colunas no CSV — que não
tem relação nenhuma com qual é a certa — decidia o resultado.

**Comparar a soma de uma coluna com ela mesma e chamar isso de validação.** O bug acima produzia
exatamente esse cenário: a mesma coluna vazia entrava nos dois lados da comparação de
`validar()`, e `0,00 == 0,00` "validava" uma comissão que não existia. Uma validação de soma só
tem valor se os dois lados vierem de fontes independentes — aqui, o CSV original e o resultado
mapeado, nunca a mesma referência de coluna repetida.

**Confundir citação de teste com citação de módulo de exemplo.** O marcador HTML que declara um
exemplo citável deve apontar para o módulo real (`normalizar.py`), nunca para o arquivo de
teste — citar o teste como se fosse o exemplo faz o gate de qualidade cobrar um teste *do
teste*, um caminho que não deveria existir. Erro real cometido e corrigido na primeira versão
deste volume, registrado em `acervo-controladoria/ESTADO.md`.

**Tratar toda coluna não encontrada como um único erro genérico.** `detectar_colunas()` nomeia
explicitamente qual campo faltou (`ValueError` distinto para comissão, data ou proposta) — um
erro genérico "não consegui detectar colunas" obrigaria quem for depurar a reabrir o CSV inteiro
em vez de ir direto ao campo que falhou.
