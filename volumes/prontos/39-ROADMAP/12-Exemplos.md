---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — item priorizado corretamente

Um item com critério de priorização completo e horizonte comprometido de curto prazo, com data
real, é aceito sem ressalva.

## Caso 2 — item direcional com data comprometida é rejeitado

O mesmo item, mas classificado como `DIRECIONAL_LONGO_PRAZO` e ainda assim carregando uma data
comprometida, é rejeitado — a combinação contradiz a própria classificação.

## Caso 3 — item fora de escopo registrado com motivo

Um item explicitamente descartado deste ciclo, com motivo declarado, é registrado na seção
correspondente do roadmap, preservando o rastro da decisão.

## Caso 4 — decisão sinalizada como exigindo autoridade externa

Uma decisão que o processo de manutenção do roadmap não pode tomar sozinho é sinalizada com a
autoridade específica necessária, nunca decidida por quem só deveria registrar a pendência.

## Caso 5 — revisão com atraso exige motivo declarado

Uma revisão periódica que encontra item atrasado sem motivo é rejeitada — a revisão só é aceita
completa quando o motivo do atraso está registrado junto dela.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 2 é o mais direto em mostrar a
contradição lógica que AA5 existe para prevenir: um item que ainda não tem certeza suficiente
para ser considerado comprometido, mas que ainda assim carrega uma data específica prometida.

Os demais casos cobrem as rejeições específicas de cada regra individual, complementando a cobertura conjunta que os testes da seção seguinte confirmam de forma exaustiva e completa.

Essa progressão de casos, do sucesso normal até cada rejeição específica, é o padrão de cobertura que este acervo já aplica de forma consistente a praticamente todo volume promovido até este ponto da produção completa.