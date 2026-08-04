---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`EstadoDoTrabalho` é um enum de quatro valores (ENFILEIRADO, EXECUTANDO, CONCLUIDO,
FALHOU_PERMANENTEMENTE) — a ausência de um quinto estado "cancelado" ou "pausado" é proposital
neste modelo mínimo, deixado como extensão futura registrada no roadmap, não uma omissão por
descuido.

`Trabalho` carrega `chave_idempotencia` separada de `id` — o `id` identifica a instância
específica do trabalho na fila; a chave de idempotência é o que permite reconhecer que duas
solicitações diferentes (dois `id` potenciais) representam, na verdade, a mesma operação de
negócio que não deveria ser executada duas vezes.

`FilaDeTrabalhos` mantém `limite_concorrente` como parâmetro explícito de configuração, não como
valor implícito de infraestrutura descoberto em tempo de execução — a decisão de quanta
capacidade concorrente o sistema aceita processar é uma decisão de arquitetura declarada, não uma
consequência acidental de quantos workers por acaso estão rodando no momento.


A ausência de um campo que registre "qual worker processou este trabalho" em `Trabalho` também é
proposital, pela mesma razão que `retirar_proximo` não recebe identificador de worker — registrar
essa informação criaria a tentação de usá-la para decisões de roteamento, reintroduzindo por uma
porta lateral a afinidade que S2 existe para eliminar.

`resultado`, em `Trabalho`, é tipado como `object` genérico em vez de um formato específico — o
exemplo não assume nenhuma estrutura particular de retorno de IA, deixando essa definição para o
tipo de trabalho concreto que uma implementação real declararia, sem acoplar o modelo central de
fila a nenhum formato de resposta específico de provedor ou modelo.