---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma implementação deste motor pronta para uso. Nenhum item vem marcado:
quem verifica marca cada um com evidência à mão — um teste que roda, uma linha de código
apontada — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] As três dimensões de orçamento (passos, tokens, tempo) são verificadas independentemente,
      antes de cada chamada ao modelo.
- [ ] Erro de ferramenta é capturado e devolvido como observação, nunca sobe como exceção não
      tratada até fora do loop.
- [ ] Erro marcado como não recuperável encerra imediatamente, sem tentativa de retry pelo
      modelo.
- [ ] Todo passo é registrado na trilha antes da próxima decisão do modelo ser solicitada.
- [ ] O resultado devolvido ao chamador sempre carrega o motivo de encerramento explícito, nunca
      um booleano genérico de sucesso/falha.
- [ ] `saida` é `None` em todo resultado cujo motivo não seja `OBJETIVO_ATINGIDO`.
- [ ] Existe teste que prova, por contagem de chamadas ao modelo fake, que orçamento zerado
      impede a próxima chamada ao modelo.
- [ ] Integração real com `27-LLM-ROUTER` e `09-ORCHESTRATOR` testada de ponta a ponta — este
      volume descreve o contrato; a integração testada é trabalho do ciclo em que os três
      volumes tiverem código citável (ver `16-Roadmap.md`).

O último item é o que este volume já sabe não poder marcar hoje: no ciclo atual ele não cita
código executável, então não existe integração a exercitar. Registro honesto do que falta, não
lacuna escondida.
