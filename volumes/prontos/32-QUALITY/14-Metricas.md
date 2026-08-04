---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Taxa de prova por mutação ao longo do tempo, por área do sistema.** É a métrica central deste
volume — decompor por área permite localizar onde a qualidade está caindo, não apenas que caiu em
algum lugar.

**Número de exceções de gate concedidas por período, e frequência de repetição para o mesmo
motivo.** Um número crescente ou motivo repetido é sinal de que o limiar ou o processo precisa de
revisão, não apenas de mais exceções.

**Idade média de item de dívida técnica registrado e não resolvido.** Dívida muito antiga sem
resolução nem revisão é sinal de que o "adiamento" original se tornou permanente sem decisão
consciente disso.

**Frequência de regressão detectada e investigada versus regressão detectada e ignorada.**
Complementa H5 — mede se a investigação de fato acontece na prática, não apenas se o mecanismo de
detecção existe.


Nenhuma dessas quatro métricas deveria ser lida isoladamente do contexto de negócio — um número
de exceções de gate crescente pode ser aceitável durante uma migração planejada e teria
significado completamente diferente em um período de operação estável sem justificativa
correspondente.

A leitura sempre exige o contexto operacional do momento específico, nunca apenas o valor numérico isolado de uma métrica sem nenhuma explicação correspondente ao lado.