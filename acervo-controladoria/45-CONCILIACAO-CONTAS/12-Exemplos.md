---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — fechamento correto com lançamento tardio

Um saldo inicial de 1000 é conhecido em 1º de janeiro. O único saldo de banco disponível é o do
dia 5, em 1050. Sem nenhum movimento registrado, `achar_ancora` não encontra fechamento — o
resíduo de 50 não bate com nada. Assim que um movimento de +50 com data de registro igual ao dia
5 é incluído (mesmo que esse movimento só tenha chegado à base dias depois), a âncora fecha
exatamente no dia 5. O caso está reproduzido em
[`../exemplos/45-conciliacao-contas/tests/test_ancora.py`](../exemplos/45-conciliacao-contas/tests/test_ancora.py),
no teste `test_lancamento_com_data_retroativa_fecha_o_dia_correto_quando_chega`, e ilustra a regra
central de `07-Regras.md`: o que importa é a data do fato, não a data em que o dado chegou.

## Caso 2 — boilerplate quase engana o casamento

Dois títulos abertos têm a mesma descrição de origem, "COMPRA NACIONAL DEBIT", seguida de nomes
de fornecedor diferentes — um posto de padaria, uma farmácia. Um movimento bancário chega com a
descrição da farmácia. Comparando o texto bruto, as duas descrições de título parecem quase
igualmente próximas do movimento, porque o prefixo comum domina a métrica de similaridade.
Descontando o vocabulário genérico antes de comparar — o que `casar()` faz por padrão — o
casamento correto (farmácia) fica evidente, porque só os tokens que identificam de fato o
fornecedor entram na conta. Ver
[`test_boilerplate_nao_derruba_a_identificacao_de_fornecedores_diferentes`](../exemplos/45-conciliacao-contas/tests/test_casamento.py).

## Caso 3 — dois valores redondos iguais, uma é duplicata e a outra não

Duas transferências de exatamente 1000, mesmo valor com sinal, para a mesma contraparte, no
mesmo dia: a segunda é bloqueada pela guarda, porque a chave completa (data + valor + contraparte)
já foi vista. Duas transferências de 1000 para a mesma contraparte em dias diferentes: nenhuma é
bloqueada, porque a chave é composta e a data diverge. O caso existe porque decidir por valor
isolado — um erro real de implementação em motores mais simples — bloquearia a segunda situação
por engano, negando uma transação legítima. Ver `test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata`
e `test_mesma_chave_completa_e_bloqueada` em
[`../exemplos/45-conciliacao-contas/tests/test_guarda.py`](../exemplos/45-conciliacao-contas/tests/test_guarda.py).

Os três casos, e a composição completa dos cinco módulos numa única passagem, estão narrados de
ponta a ponta em `test_fluxo_completo.py`, citado em `13-Testes.md`.
