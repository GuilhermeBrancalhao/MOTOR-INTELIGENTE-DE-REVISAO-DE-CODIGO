---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma implementação deste motor pronta para uso:

- [x] Checkpoint é gravado e confirmado antes de avançar para o próximo passo, sem excepção.
- [x] Toda saída de passo de IA passa por validação de formato antes de alimentar o próximo
      passo; passo determinístico não passa por essa validação.
- [x] Checkpoint contém todo estado necessário para retomada, sem dependência de memória do
      processo original.
- [x] `AguardandoSinal` e `Pausado` são estados distintos na observabilidade, não colapsados num
      único "workflow parado".
- [x] Correção automática de saída de IA malformada tem limite de tentativas, com queda
      controlada para pausa.
- [x] Existe teste que injeta falha entre conclusão de passo e confirmação de checkpoint, e
      verifica reexecução conservadora na retomada.
- [x] Existe teste que confirma que passo determinístico nunca passa por validação de formato de
      IA.
- [ ] Integração real com `08-AGENT-ENGINE` (tradução de motivo de encerramento) testada de
      ponta a ponta — este volume descreve o contrato; a integração testada é trabalho do ciclo
      em que ambos os volumes tiverem código citável (ver `16-Roadmap.md`).

O último item permanece aberto porque este volume, no ciclo atual, não cita código executável —
registro honesto do que falta.
