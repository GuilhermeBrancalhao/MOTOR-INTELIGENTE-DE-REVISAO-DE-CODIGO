---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — caso de uso registrado corretamente

Um caso de uso de classificação de crédito é registrado com dono responsável, nível de risco
ALTO. O registro é aceito sem ressalva.

## Caso 2 — decisão de alto risco sem revisão humana é rejeitada

Uma `DecisaoAutomatizada` de um caso de uso ALTO chega sem `revisada_por_humano=True` —
`registrar_decisao` rejeita antes de a decisão entrar na trilha de auditoria.

## Caso 3 — decisão de baixo risco não exige revisão humana

A mesma estrutura de decisão, mas associada a um caso de uso classificado como BAIXO risco, é
aceita sem exigir revisão humana — o rigor é proporcional à classificação, não uniforme.

## Caso 4 — produção bloqueada sem aprovação explícita

Um caso de uso classificado e com dono responsável, mas ainda sem aprovação explícita para
produção, é bloqueado por `verificar_pronto_para_producao` até que a aprovação seja registrada.

## Caso 5 — revisão periódica acumula histórico sem substituir

Duas revisões periódicas sucessivas do mesmo caso de uso, em datas diferentes, ficam ambas
registradas no histórico de revisão — a segunda não apaga nem substitui a primeira.


Os cinco casos cobrem, juntos, os dois portões distintos do fluxo principal (registro de caso de
uso com dono e classificação, aprovação para produção) mais o portão por decisão individual
(revisão humana proporcional ao risco) e o ciclo de revisão periódica — a mesma cobertura que os
testes da seção seguinte verificam individualmente.

Essa progressão, do registro inicial até a revisão periódica anos depois, é o que dá a este conjunto de exemplos uma dimensão temporal que os exemplos de outros volumes deste grupo não precisam necessariamente ter.