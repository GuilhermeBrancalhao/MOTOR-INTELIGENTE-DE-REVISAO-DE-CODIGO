---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — carregamento e conclusão normal

Uma requisição de IA é iniciada, recebe três fragmentos em sequência, e conclui. Em cada etapa,
`texto_parcial()` reflete o que já chegou — a interface poderia renderizar isso incrementalmente
sem esperar a conclusão.

## Caso 2 — falha sem cache, nenhum fallback enganoso

Uma requisição falha e não há cache anterior disponível. `resolver_exibicao` retorna `None` — a
interface mostra estado de erro explícito, nunca inventa um resultado.

## Caso 3 — falha com cache, fallback marcado

A mesma falha, mas com cache anterior disponível. `resolver_exibicao` retorna um
`ResultadoExibido` com `e_fallback=True` — a interface pode exibir o dado anterior, mas sempre
sinalizando que não é fresco.

## Caso 4 — cancelamento descarta fragmento tardio

Uma requisição é cancelada no meio do recebimento de fragmentos. Um fragmento que chega depois do
cancelamento é silenciosamente descartado — `texto_parcial()` não reflete esse fragmento tardio,
e o estado permanece CANCELADO, nunca reverte para CARREGANDO ou avança para CONCLUIDO.

## Caso 5 — promoção a estado global negada e depois autorizada

Uma tentativa de promover a resposta de uma requisição concluída ao estado global, sem
autorização, é rejeitada. A mesma promoção, com `autorizado=True`, funciona — a diferença entre
os dois casos é sempre uma decisão explícita, nunca implícita.


Os cinco casos, em conjunto, cobrem o ciclo de vida completo de uma requisição de IA do ponto de
vista da interface — desde o carregamento normal até os três desvios que mais frequentemente
diferenciam uma interface bem construída de uma que só funciona no caminho feliz: falha sem
fallback, falha com fallback, e cancelamento no meio de um stream em andamento.