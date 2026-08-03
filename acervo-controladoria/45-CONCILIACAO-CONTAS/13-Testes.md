---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Vinte e três testes em seis arquivos, todos determinísticos e sem I/O — nenhum teste depende de
rede, relógio do sistema ou arquivo externo, porque toda data usada é passada explicitamente
como parâmetro. Cinco arquivos testam um módulo cada de forma isolada; o sexto,
`test_fluxo_completo.py`, testa a composição dos cinco na ordem real de uso, incluindo o caminho
em que o motor decide não escrever.

<!-- exemplo: exemplos/45-conciliacao-contas/ancora.py -->

## Como rodar

```bash
cd acervo-controladoria
python -m pytest exemplos/45-conciliacao-contas -q
```

## O que cada arquivo cobre

`test_ancora.py` cobre fechamento correto, ausência de fechamento e o caso de lançamento com
data retroativa. `test_casamento.py` cobre casamento por valor e nome, ausência de candidato, o
efeito do desconto de boilerplate e a tolerância de consumo variável. `test_confianca.py` cobre
os dois caminhos para `ALTA`, a rejeição de ocorrência isolada e — o teste mais importante do
arquivo — a prova de que ausência de evidência só pode reduzir a classificação, nunca elevá-la.
`test_guarda.py` cobre bloqueio de chave idêntica e não bloqueio de valores redondos repetidos
em condições diferentes (data diferente, contraparte diferente, sinal diferente).
`test_trilha.py` cobre registro, rejeição de chave duplicada com exceção, ordem de inserção
preservada, e o cenário em que um índice externo simulado perde a referência mas a trilha local
continua correta.

## O que prova que o teste não é decorativo

Cada regra listada em `07-Regras.md` tem pelo menos um teste que falha se a regra for violada —
não um teste que só confirma o caminho feliz. `test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata`
falharia imediatamente se `guarda.py` fosse simplificado para comparar só `abs(valor)`; é esse
tipo de teste, escrito para capturar o erro específico que a regra existe para evitar, que
distingue suíte que trava comportamento de suíte que só documenta.
