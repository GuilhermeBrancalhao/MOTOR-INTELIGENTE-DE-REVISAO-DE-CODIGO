---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma implementação deste motor pronta para uso:

- [x] Todo grafo é validado (ciclo, referência a nó inexistente) antes de qualquer nó executar.
- [x] Um nó só transita para `Pronto` quando todas as suas dependências estão em `Sucesso`, sem
      excepção de maioria.
- [x] A política de falha (`AbortarDependentes`, `PularDependentes`, `RetryComBackoff`) é
      configurável por nó, não fixa para o grafo inteiro.
- [x] Retry de nó nunca reexecuta dependências já resolvidas.
- [x] O resultado final do grafo lista o status de cada nó individualmente, sem campo agregado
      de sucesso/falha binário.
- [x] Existe teste que prova, por grafo cíclico construído de propósito, que a validação rejeita
      antes de qualquer execução.
- [x] Existe teste que prova que fan-in com uma dependência falha nunca libera o nó de agregação.
- [ ] Integração real com `08-AGENT-ENGINE` (tradução de `MotivoEncerramento` para
      `Sucesso`/`Falha`) testada de ponta a ponta — este volume descreve o contrato; a
      integração testada é trabalho do ciclo em que ambos os volumes tiverem código citável (ver
      `16-Roadmap.md`).

O último item permanece aberto porque este volume, no ciclo atual, não cita código executável —
registro honesto do que falta, não lacuna escondida.
