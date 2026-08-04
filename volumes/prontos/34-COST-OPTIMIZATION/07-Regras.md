---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**U1 — Custo é medido e atribuído pela tarefa completa, nunca por token ou chamada isolada sem
contexto.** *Consequência:* o registro de custo sempre responde "qual trabalho de negócio isso
serviu", nunca apenas "quantos tokens foram consumidos".

**U2 — Todo custo é atribuído a um escopo explícito.** *Consequência:* nenhum gasto fica num
balde não atribuído que ninguém é responsável por explicar ou justificar.

**U3 — Orçamento por escopo tem limiar de alerta antes do limite rígido.**
*Consequência:* quem acompanha o orçamento tem uma janela de reação, nunca descobrindo o estouro
só depois que ele já aconteceu.

**U4 — Tendência de custo é acompanhada por múltiplos períodos, nunca julgada por um único
período isolado.** *Consequência:* um pico pontual de gasto não é confundido com tendência real
de crescimento sem o contexto de mais de um ponto de dado.

**U5 — Toda mudança proposta como redução de custo é validada por medição real antes e depois.**
*Consequência:* uma mudança "obviamente mais barata" que não reduz o gasto medido não é aceita
como otimização real.

**U6 — Nenhum preço ou valor de custo específico entra como fato duradouro; todo número é
ilustração datada de método.** *Consequência:* o volume não envelhece mal — o método continua
válido mesmo quando os valores específicos de hoje deixarem de ser verdade.
