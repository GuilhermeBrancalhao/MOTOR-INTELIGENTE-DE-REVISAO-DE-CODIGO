---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] O roteador nunca aceita candidato fora da lista aprovada pelo 26.
- [ ] Fallback é acionado automaticamente sob degradação sustentada, sem bloquear a chamada.
- [ ] Degradação é julgada por amostra mínima, nunca por falha isolada.
- [ ] Recuperação ao principal exige janela de estabilidade, nunca é imediata.
- [ ] Toda decisão de roteamento está registrada com candidato e motivo.
- [ ] O estado de roteamento atual por tarefa é consultável diretamente, sem inferência por log.


- [ ] O caminho de recuperação (janela de estabilidade) tem teste dedicado, não apenas o caminho
  de degradação.
- [ ] O sinal de saúde que motivou cada decisão é registrado junto da decisão, não apenas o
  motivo categorizado.
