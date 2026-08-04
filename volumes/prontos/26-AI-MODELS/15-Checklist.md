---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Toda seleção de modelo declara requisito de capacidade explícito antes de considerar
  candidatos.
- [ ] Nenhum modelo é usado numa tarefa sem avaliação contra casos de ouro registrada.
- [ ] Toda tarefa crítica tem fallback declarado e testado, não apenas declarado.
- [ ] Comparação de custo considera a tarefa completa, nunca só o preço por token.
- [ ] Nenhum preço, limite ou nome de modelo aparece como fato permanente sem data e fonte.
- [ ] Toda troca de modelo em produção está registrada com motivo e avaliação.


- [ ] Nenhuma constante de preço ou nome de modelo está hardcoded em código de produção sem
  origem dinâmica.
- [ ] A lista de candidatos aprovados é revisada com frequência maior que a configuração de
  qual é o principal.
