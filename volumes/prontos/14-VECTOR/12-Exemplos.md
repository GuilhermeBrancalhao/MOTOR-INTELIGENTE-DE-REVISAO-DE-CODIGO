---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — consulta bem formada, resultado correto

Um índice com partição "documentos-suporte" e métrica cosseno recebe uma consulta declarando os
três campos obrigatórios corretamente. A busca compara só vetores da mesma versão de modelo e
partição, devolvendo os cinco mais próximos por cosseno, nenhum deles excluído.

## Caso 2 — consulta rejeitada por métrica ausente

A mesma consulta chega sem o campo de métrica declarado — talvez por um bug de integração que
esqueceu de preencher o parâmetro. A consulta é rejeitada antes de qualquer comparação, com o
motivo explícito ("consulta incompleta: métrica ausente"), em vez de assumir cosseno por padrão
e devolver um resultado que pareceria válido mas se baseou numa suposição não confirmada.

## Caso 3 — reindexação após mudança de modelo

O sistema migra de um modelo de embedding para outro. Em vez de atualizar vetores incrementalmente
conforme documentos são reingeridos, o índice inteiro é reconstruído em paralelo (versão nova),
validado, e só então a consulta passa a apontar para a versão nova numa única troca atômica — a
versão antiga é mantida por um período de retenção antes de ser descartada, permitindo reverter
se um problema for descoberto depois da troca.

## Caso 4 — cruzamento de partição prevenido

Uma consulta declara corretamente a partição "documentos-suporte", mas o índice também contém
vetores da partição "documentos-financeiro" armazenados na mesma estrutura física subjacente
(uma escolha de implementação para eficiência de armazenamento). A busca nunca considera os
vetores da partição errada como candidatos — o filtro de partição acontece antes de qualquer
cálculo de similaridade, não depois, então o custo computacional da comparação nunca é gasto em
vetores que seriam descartados de qualquer forma.
