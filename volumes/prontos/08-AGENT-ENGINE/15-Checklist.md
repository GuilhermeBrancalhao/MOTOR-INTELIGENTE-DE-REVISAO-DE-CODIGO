---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
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
- [ ] Integração real com `27-LLM-ROUTER` e `09-ORCHESTRATOR` exercitada de ponta a ponta — o
      exemplo deste volume prova o motor isoladamente, com modelo fake; a integração entre os
      três motores reais continua sendo trabalho de um ciclo seguinte (ver `16-Roadmap.md`).

O último item é o único que este volume ainda não consegue marcar: `exemplos/08-agent-engine`
prova o contrato do motor sozinho, não a integração entre motores. Registro honesto do que falta.
