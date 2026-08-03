---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma implementação deste motor pronta para uso. Nenhum item vem marcado:
quem verifica marca cada um com evidência à mão — um teste que roda, uma linha de código
apontada — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] Checkpoint é gravado e confirmado antes de avançar para o próximo passo, sem exceção.
- [ ] Toda saída de passo de IA passa por validação de formato antes de alimentar o próximo
      passo; passo determinístico não passa por essa validação.
- [ ] Checkpoint contém todo estado necessário para retomada, sem dependência de memória do
      processo original.
- [ ] `AguardandoSinal` e `Pausado` são estados distintos na observabilidade, não colapsados num
      único "workflow parado".
- [ ] Correção automática de saída de IA malformada tem limite de tentativas, com queda
      controlada para pausa.
- [ ] Existe teste que injeta falha entre conclusão de passo e confirmação de checkpoint, e
      verifica reexecução conservadora na retomada.
- [ ] Existe teste que confirma que passo determinístico nunca passa por validação de formato de
      IA.
- [ ] Integração real com `08-AGENT-ENGINE` (tradução de motivo de encerramento) exercitada de
      ponta a ponta — os dois volumes já têm exemplo próprio, mas a ponte entre eles ainda não tem
      teste (ver `16-Roadmap.md`).

O último item é o único que este volume ainda não consegue marcar: `exemplos/10-workflow` prova a
garantia de checkpoint isoladamente, não a integração com o motor de agente.
