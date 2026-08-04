---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Recurso criado manualmente pelo console "só desta vez, é rápido", sem declaração
correspondente.** É exatamente esse recurso que, meses depois, ninguém lembra por que existe nem
consegue reproduzir se for perdido.

**Redundância adicionada apenas depois de um incidente de indisponibilidade, nunca antes.**
Inverte a lógica de N2 — a verificação deveria encontrar a ausência de redundância antes do
incidente, não depois.

**Segredo "temporariamente" hardcoded na configuração, com plano de mover para o cofre depois.**
O "depois" raramente chega antes de o segredo já ter sido versionado e potencialmente exposto —
não existe hardcoded temporário seguro.

**Mudança de infraestrutura aplicada diretamente em produção durante um teste, "só para
verificar rápido".** É exatamente o cenário que o isolamento de ambiente (N4) existe para tornar
estruturalmente difícil, não apenas desaconselhado por convenção.

**Drift detectado e ignorado repetidamente, por já ser "conhecido".** Um drift crônico ignorado
não é menos risco por ser antigo — é sinal de que a declaração está permanentemente desatualizada
em relação à realidade, o que corrói a confiança em toda a configuração declarada.


**Verificação de drift rodando, mas sem ninguém designado para triar o resultado.** Detectar
divergência sem um processo que a examine tem o mesmo efeito prático de não detectar — a
informação existe, mas não influencia nenhuma decisão.