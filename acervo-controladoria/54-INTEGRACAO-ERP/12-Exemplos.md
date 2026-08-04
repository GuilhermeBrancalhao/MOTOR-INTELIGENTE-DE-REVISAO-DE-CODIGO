---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Exemplos Práticos

## Caso real — DIGIO, janeiro/2026 (`110075 02.01.csv`)

O CSV tem 29 colunas, duas delas casando com o padrão `comiss`: "% da
Comissão" (percentual) e "Valor Comiss" (o valor pago, como texto
`'886,39'`). A versão original de `normalizar.py` escolhia a primeira que
aparecesse na ordem das colunas do CSV — nesse arquivo, o percentual — e a
validação de soma "batia" mesmo assim: como `is_numeric_dtype` excluía
texto com vírgula, só sobravam colunas numéricas vazias como candidatas, e
a soma de uma coluna 100% vazia dá `0,00` por padrão do pandas.

Corrigido, o script escolhe "Valor Comiss", converte `'886,39'` → `886.39`,
e a soma das 14 linhas do arquivo bate em `6.762,97` — conferida à mão
contra o CSV original. Reproduzido em
[`test_escolhe_valor_comissao_e_nao_o_percentual`](../exemplos/54-integracao-erp/tests/test_normalizar.py)
e
[`test_mapeamento_grava_valor_correto_nao_o_percentual`](../exemplos/54-integracao-erp/tests/test_normalizar.py).

## Pendência conhecida, ainda sem correção

O mesmo banco, arquivo de julho (`DIGIO - 110075 01.07.csv`), tem BOM UTF-8
(`\xef\xbb\xbf`) no início. A detecção de separador de `ler_csv` falha
nesse arquivo — lê como 2 colunas em vez de ~29 — e ainda não foi
corrigida. É um bug diferente deste (está em `ler_csv`, não na detecção de
comissão), registrado aqui para não se perder.

## Por que este caso específico, e não um sintético inventado

O caso do DIGIO entrou neste volume porque foi reproduzido rodando o script contra o arquivo de
produção real, não porque foi montado para ilustrar o ponto. A diferença importa: um cenário
sintético provaria só que a lógica de desempate funciona no papel; o CSV real provou, além
disso, que a causa raiz era mais profunda do que parecia — o problema não era só a ordem das
colunas, era o parsing numérico brasileiro escondendo a coluna certa antes mesmo do desempate
entrar em jogo.
