---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Decisão arquitetural importante comunicada só verbalmente numa reunião, nunca registrada como
ADR.** Viola W1 — a decisão existe apenas na memória de quem estava presente, e essa memória
degrada ou desaparece com rotatividade de equipe.

**Editar um ADR antigo diretamente para "corrigir" a decisão registrada.** Viola W2 — apaga o
contexto histórico que explicaria por que a decisão original fazia sentido no momento em que foi
tomada, mesmo que hoje pareça errada.

**Documentação mantida em ferramenta separada do repositório de código, sem versionamento
correspondente.** Viola W3 — a documentação perde qualquer conexão rastreável com o commit
específico que mudou o comportamento que ela descreve.

**Editar manualmente um arquivo de documentação gerado automaticamente, sem perceber que é
gerado.** Viola W5 — a edição desaparece silenciosamente na próxima geração, e quem a fez nem
sabe que ela nunca chegou a persistir.

**Documento único tentando servir tanto usuário final quanto mantenedor técnico ao mesmo
tempo.** Viola W6 — geralmente resulta em um documento longo demais para o usuário e superficial
demais para o mantenedor.


**Registrar ADR só depois que alguém pergunta "por que isso foi feito assim", em vez de no
momento da decisão.** Produz um contexto reconstruído de memória, com viés de retrospectiva, em
vez do raciocínio real que existia no momento em que a decisão foi tomada.