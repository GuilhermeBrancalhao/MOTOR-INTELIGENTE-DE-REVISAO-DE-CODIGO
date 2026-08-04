---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Toda avaliação de candidato usa exatamente a mesma amostra de casos de ouro do baseline.
- [ ] Nenhuma variante é considerada proposta com melhoria dentro da margem de ruído.
- [ ] O otimizador não expõe nenhum caminho de promoção direta, sem passar pelo 07.
- [ ] Toda busca tem orçamento de tentativas declarado e respeitado.
- [ ] Toda tentativa avaliada está registrada no histórico, aprovada ou não.
- [ ] Os casos de ouro usados como função objetivo nunca são alterados pelo processo de busca.


- [ ] Nenhum limiar de melhoria foi ajustado depois de já ver o resultado de um candidato
  específico.
- [ ] A estratégia de geração de candidato usada está documentada junto do histórico da busca.
