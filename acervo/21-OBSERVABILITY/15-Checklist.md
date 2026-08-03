---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar a instrumentação de um sistema com IA madura para produção:

- [x] Sucesso técnico de chamada e correção de resultado são sinais estruturalmente separados,
      nunca colapsados num único indicador.
- [x] Todo sinal que cruza limiar de alerta dispara notificação confirmada, não só registro
      passivo.
- [x] Limiar de cada categoria de sinal foi calibrado a partir de distribuição real observada,
      com a proveniência registrada.
- [x] Canal de notificação tem heartbeat periódico, com alerta reverso se o heartbeat falhar.
- [x] Todo painel de custo/latência agregado decompõe por tipo de etapa (IA versus
      determinística).
- [x] Existe teste que força um sinal a cruzar o limiar e verifica disparo real de notificação,
      não apenas registro.
- [x] Existe teste que simula indisponibilidade do canal de notificação e verifica o alerta
      reverso correspondente.
- [ ] Integração real com `08-AGENT-ENGINE`, `09-ORCHESTRATOR` e `10-WORKFLOW` (emissão de sinal
      na ponta de origem) testada de ponta a ponta — este volume descreve o contrato; a
      integração testada é trabalho do ciclo em que os volumes tiverem código citável (ver
      `16-Roadmap.md`).

O último item permanece aberto porque este volume, no ciclo atual, não cita código executável.
