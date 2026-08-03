---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar a instrumentação de um sistema com IA madura para produção. Nenhum item vem
marcado: quem verifica marca cada um com evidência à mão — um painel aberto, um alerta que de
fato chegou — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] Sucesso técnico de chamada e correção de resultado são sinais estruturalmente separados,
      nunca colapsados num único indicador.
- [ ] Todo sinal que cruza limiar de alerta dispara notificação confirmada, não só registro
      passivo.
- [ ] Limiar de cada categoria de sinal foi calibrado a partir de distribuição real observada,
      com a proveniência registrada.
- [ ] Canal de notificação tem heartbeat periódico, com alerta reverso se o heartbeat falhar.
- [ ] Todo painel de custo/latência agregado decompõe por tipo de etapa (IA versus
      determinística).
- [ ] Existe teste que força um sinal a cruzar o limiar e verifica disparo real de notificação,
      não apenas registro.
- [ ] Existe teste que simula indisponibilidade do canal de notificação e verifica o alerta
      reverso correspondente.
- [ ] Integração real com `08-AGENT-ENGINE`, `09-ORCHESTRATOR` e `10-WORKFLOW` (emissão de sinal
      na ponta de origem) exercitada de ponta a ponta — os quatro volumes já têm exemplo próprio,
      mas a emissão de sinal de um motor para o coletor deste ainda não tem teste (ver
      `16-Roadmap.md`).

O último item é o único que este volume ainda não consegue marcar: `exemplos/21-observability`
prova o avaliador de limiar isoladamente, não a emissão na ponta de origem.
