---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Garantir que todo elemento de interface dependente de resultado de IA declare um estado de
carregamento distinto do carregamento genérico, porque a latência variável e frequentemente
longa de uma chamada de IA é informação que o usuário precisa perceber, não esconder atrás de um
spinner indistinguível de qualquer outra espera.

Renderizar saída incremental de IA conforme ela chega, nunca armazenada em buffer para parecer
uma resposta instantânea — a vantagem de latência percebida que o streaming oferece só existe se
a interface de fato a expõe.

Tornar toda falha de uma ação dirigida por IA visível como estado distinto, nunca substituída
silenciosamente por dado obsoleto sem indicar que uma substituição aconteceu.

Manter resposta de IA no escopo do componente que a solicitou por padrão, promovendo a estado
global apenas por decisão explícita, nunca implicitamente.

Cancelar requisição de IA pendente quando a ação que a originou é abandonada, para que uma
resposta que já não importa mais para ninguém não continue consumindo recurso nem, pior, chegue
tarde e afete um estado que já mudou de contexto.

Os cinco objetivos se agrupam em dois eixos: o que o usuário percebe (F1, F2, F3 — carregamento
distinto, streaming, falha visível) e o que a arquitetura interna garante sem que o usuário
precise notar (F4, F5 — escopo de estado, cancelamento). O primeiro eixo falha de forma visível e
imediata quando ignorado; o segundo falha de forma sutil, geralmente só sob condição de corrida
específica, o que o torna mais fácil de negligenciar durante o desenvolvimento e mais caro de
diagnosticar depois que já está em produção.