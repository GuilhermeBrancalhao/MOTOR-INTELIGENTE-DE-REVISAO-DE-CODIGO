---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma implementação deste motor pronta para uso. Nenhum item vem marcado:
quem verifica marca cada um com evidência à mão — um teste que roda, uma linha de código
apontada — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] Todo grafo é validado (ciclo, referência a nó inexistente) antes de qualquer nó executar.
- [ ] Um nó só transita para `Pronto` quando todas as suas dependências estão em `Sucesso`, sem
      exceção de maioria.
- [ ] A política de falha (`AbortarDependentes`, `PularDependentes`, `RetryComBackoff`) é
      configurável por nó, não fixa para o grafo inteiro.
- [ ] Retry de nó nunca reexecuta dependências já resolvidas.
- [ ] O resultado final do grafo lista o status de cada nó individualmente, sem campo agregado
      de sucesso/falha binário.
- [ ] Existe teste que prova, por grafo cíclico construído de propósito, que a validação rejeita
      antes de qualquer execução.
- [ ] Existe teste que prova que fan-in com uma dependência falha nunca libera o nó de agregação.
- [ ] Integração real com `08-AGENT-ENGINE` (tradução de `MotivoEncerramento` para
      `Sucesso`/`Falha`) exercitada de ponta a ponta — os dois volumes já têm exemplo próprio, mas
      a ponte entre eles ainda não tem teste (ver `16-Roadmap.md`).

O último item é o único que este volume ainda não consegue marcar: `exemplos/09-orchestrator`
prova o grafo isoladamente, não a tradução na fronteira com o motor de agente.
