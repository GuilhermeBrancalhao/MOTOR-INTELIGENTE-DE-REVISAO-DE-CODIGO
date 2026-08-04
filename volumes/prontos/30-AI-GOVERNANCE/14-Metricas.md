---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de casos de uso com dono responsável e classificação de risco registrados.** Deveria
ser 100% por construção (G1/G2 impedem registro incompleto) — uma queda indica falha no processo
de registro, não apenas descuido pontual.

**Proporção de decisões de alto risco de fato revisadas por humano versus rejeitadas por falta de
revisão.** Mede se o portão de revisão humana (G3) está sendo respeitado na prática operacional,
não apenas disponível como controle teórico.

**Tempo médio entre proposta de caso de uso e aprovação explícita para produção.** Um tempo muito
longo pode indicar processo de aprovação sobrecarregado; um tempo muito curto para caso de alto
risco pode indicar revisão superficial.

**Frequência de reclassificação de risco por revisão periódica (G6).** Um número baixo constante
pode ser normal, ou pode indicar que a revisão periódica está acontecendo apenas como formalidade,
sem de fato reavaliar impacto real.


Estas quatro métricas, lidas em conjunto ao longo do tempo, revelam se a governança está
operando como controle real ou como formalidade — um caso de uso com métricas perfeitas mas
nenhuma decisão jamais rejeitada por falta de revisão humana pode simplesmente nunca ter
encontrado um caso de risco alto, ou pode estar contornando o controle silenciosamente.

A leitura combinada dessas quatro métricas é sempre mais informativa do que qualquer uma isolada, especialmente para distinguir um sistema realmente bem governado de um que apenas nunca foi posto à prova por um caso de risco alto de verdade.