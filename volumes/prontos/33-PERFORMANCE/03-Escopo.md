---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o processo de definir, medir e proteger orçamento de desempenho: SLO declarado,
medição sob carga realista, regressão investigada, degradação graciosa, e otimização validada por
medição.

**Fronteira com `25-API-ARCHITECT`.** O orçamento de latência por endpoint síncrono, exigido
naquele volume (T6), é uma das entradas deste volume — este volume trata do processo mais amplo
de como esse orçamento é definido, medido sob carga, e o que acontece quando é violado, incluindo
para operações assíncronas que aquele volume não cobre diretamente.

**Fronteira com `32-QUALITY`.** O indicador agregado de qualidade daquele volume trata de
correção verificada por prova de regra; este volume trata de uma dimensão independente
(desempenho). Um sistema pode ter alta taxa de prova por mutação e ainda violar todo SLO de
latência — as duas dimensões merecem verificação separada.

**Fronteira com `23-BACKEND-ARCHITECT`.** Backpressure explícita para trabalho assíncrono (S3
daquele volume) e degradação graciosa sob sobrecarga (aqui) tratam de aspectos relacionados —
este volume formaliza o critério de quando a degradação é aceitável do ponto de vista de SLO,
não a mecânica de fila que a implementa.

Não cobre técnica específica de otimização (cache, paralelização, índice) — os princípios deste
volume (SLO declarado, medição sob carga, regressão investigada) valem independentemente de qual
técnica é usada para melhorar desempenho.
