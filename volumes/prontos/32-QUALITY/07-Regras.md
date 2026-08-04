---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**H1 — Cobertura é medida pela taxa de prova por mutação, nunca apenas por cobertura de linha
executada.** *Consequência:* o indicador reflete verificação real de regra, não apenas
passagem de código por um caminho de execução.

**H2 — Release é bloqueado quando o indicador cai abaixo de um piso declarado, exceto com
exceção explicitamente registrada.** *Consequência:* nenhum release "só desta vez" ignora
silenciosamente uma queda de qualidade — toda exceção é uma decisão rastreável.

**H3 — Dívida técnica é registrada como item explícito e datado — o quê, por que foi adiado,
custo estimado.** *Consequência:* dívida técnica nunca existe apenas como julgamento implícito na
memória de quem decidiu adiar algo.

**H4 — Tendência de qualidade é acompanhada por múltiplas medições ao longo do tempo, nunca
julgada por uma única medição isolada.** *Consequência:* uma queda pontual não é confundida com
regressão real sem o contexto de mais de um ponto de dado.

**H5 — Toda regressão do indicador entre duas medições é investigada antes de ser aceita como
novo normal.** *Consequência:* uma queda de qualidade nunca se normaliza silenciosamente sem que
alguém entenda a causa.

**H6 — O indicador agregado é composto por submétricas nomeadas e individualmente inspecionáveis,
nunca um único número opaco.** *Consequência:* quando a qualidade cai, é sempre possível decompor
qual dimensão específica degradou, não apenas que "a qualidade caiu".
