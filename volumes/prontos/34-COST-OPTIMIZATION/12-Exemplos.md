---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — custo registrado corretamente, com tarefa e escopo

Um custo associado a uma tarefa concluída e a um escopo específico é aceito sem ressalva pelo
registro de custo.

## Caso 2 — custo sem tarefa é rejeitado

Uma tentativa de registrar custo sem identificar a tarefa que o gerou falha antes de contaminar
qualquer total agregado.

## Caso 3 — orçamento em três estados: OK, ALERTA, ESTOURADO

Um mesmo orçamento avaliado contra três níveis crescentes de gasto acumulado produz os três
estados distintos — a transição de ALERTA para ESTOURADO é visível antes de o limite ser
efetivamente ultrapassado.

## Caso 4 — tendência de custo detectada entre dois períodos

Um histórico com dois períodos consecutivos, o segundo com gasto maior que o primeiro, produz uma
tendência explícita com os dois valores específicos.

## Caso 5 — otimização de custo validada e rejeitada

Uma mudança que reduz o gasto medido é validada como economia real; a mesma estrutura de teste,
mas sem redução de gasto medido, é rejeitada como otimização não comprovada.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 3 sozinho ilustra os três
estados de orçamento numa única sequência, o exemplo mais didático deste volume para entender a
diferença entre alerta antecipado e estouro efetivo do limite declarado.

Essa progressão de casos, do registro básico até a otimização validada, cobre o ciclo de vida completo de uma decisão de custo dentro do escopo deste volume específico.

Cada caso foi escolhido para corresponder a exatamente uma regra ou a um par de regras relacionadas, evitando redundância entre exemplos que provariam essencialmente a mesma coisa.