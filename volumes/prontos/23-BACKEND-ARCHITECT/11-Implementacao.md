---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/23-backend-architect/fila_de_trabalhos.py -->

`fila_de_trabalhos.py`, citado acima, formaliza S1-S6: `Trabalho` e `EstadoDoTrabalho` modelam o
ciclo de vida assíncrono com estado consultável a qualquer momento via `consultar_estado`, nunca
bloqueando (S1); `retirar_proximo` não recebe identificador de worker, garantindo ausência de
afinidade (S2); a checagem de `limite_concorrente` em `retirar_proximo` aplica backpressure
explícita, levantando `CapacidadeInsuficiente` (S3); `enfileirar` busca por chave de idempotência
antes de criar um trabalho novo (S4); toda transição de estado passa por um método nomeado da
fila, nunca por atribuição direta (S5); `marcar_falha` transiciona para o estado terminal
`FALHOU_PERMANENTEMENTE` apenas após esgotar `max_tentativas`, mantendo o trabalho consultável
(S6).


`_buscar_ativo_por_chave` ignora explicitamente trabalhos em `FALHOU_PERMANENTEMENTE` — um
trabalho que já esgotou suas tentativas e falhou definitivamente não deveria bloquear uma nova
tentativa de processar a mesma operação de negócio sob uma solicitação nova; a idempotência (S4)
protege contra duplicação de trabalho *ativo*, não contra uma segunda tentativa legítima depois
de uma primeira ter falhado de vez.

`marcar_falha` e `marcar_concluido` têm a mesma pré-condição (`estado == EXECUTANDO`) verificada
de forma idêntica — essa duplicação pequena e deliberada, em vez de extraída para um método
auxiliar comum, mantém cada operação legível isoladamente sem exigir que quem lê uma delas precise
também entender a outra para confirmar a pré-condição que está sendo aplicada.