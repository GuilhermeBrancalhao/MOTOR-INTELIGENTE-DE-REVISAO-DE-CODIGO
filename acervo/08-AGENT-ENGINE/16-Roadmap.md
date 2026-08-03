---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Código executável de referência — este ciclo (2026-08-03) priorizou fechar contrato, regras e
diagramas para os 10 volumes essenciais antes de investir em implementação citável, decisão
registrada em `ENTREGA.md`. Sem código, os critérios 2 (testes dos exemplos) da Definição de
PRONTO não se aplicam ainda a este volume — ele pode passar no gate 1 sem nunca ter passado no
gate 2, porque não há exemplo citado.

Paralelismo controlado dentro de uma única execução (múltiplas ferramentas no mesmo passo) —
deliberadamente fora do contrato atual (ver `07-Regras.md`, invariante "um passo produz
exatamente uma ação"), mas pode ser revisitado se um caso de uso real justificar a complexidade
adicional na trilha de auditoria.

Mecanismo de checkpoint/retomada de uma execução interrompida por falha de infraestrutura (não
por orçamento nem erro do agente) — hoje o contrato assume que uma execução interrompida
externamente simplesmente não tem resultado; retomar do último passo registrado na trilha é
possível em teoria, mas não está especificado.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (executor de passo + guardião de orçamento) com testes que
provem as invariantes de `07-Regras.md` por mutação. Depois, a integração real com
`09-ORCHESTRATOR` — hoje a fronteira está descrita em prosa (`03-Escopo.md`), mas nunca foi
exercitada com os dois volumes tendo código simultaneamente.

## O que este volume assume que pode mudar

O número de dimensões de orçamento (três: passos, tokens, tempo) pode crescer se um caso de uso
real expuser uma quarta dimensão relevante (custo monetário direto, por exemplo, se diferente de
tokens por variar por provedor) — mas qualquer dimensão nova precisa da mesma independência de
verificação que as três atuais têm, não pode ser derivada implicitamente de outra.
