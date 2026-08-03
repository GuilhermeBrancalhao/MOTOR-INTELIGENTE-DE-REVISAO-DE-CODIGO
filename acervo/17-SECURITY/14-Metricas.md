---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

**Taxa de ações classificadas como `Travado` sobre o total de ações avaliadas.** Fonte: log do
classificador de risco. Uma taxa crescente ao longo do tempo, sem crescimento correspondente no
catálogo de vetores conhecidos, sugere mudança no padrão de uso do sistema (dado processado de
fontes mais arriscadas, por exemplo) que merece investigação antes de simplesmente ajustar
limiares para reduzir o número.

**Número de famílias de controle criadas por período, com o vetor que motivou cada uma.** Fonte:
registro de `VetorRisco` (`08-Modelos.md`). Esta métrica não deveria ir a zero e ficar assim
permanentemente — zero novas famílias por muito tempo pode significar sistema estável ou pode
significar que auditoria adversarial parou de acontecer; a métrica sozinha não decide qual, mas
aponta a pergunta certa.

**Taxa de falso positivo por família de controle**, medida por quantas vezes uma ação legítima
foi travada e precisou de correção posterior no classificador (como o caso da string
`'EXEC(ruim)'` documentado em `12-Exemplos.md`). Uma taxa de falso positivo exatamente zero por
longo período é tão suspeita quanto uma taxa muito alta — sugere que o classificador pode não
estar sendo exercitado por entrada real diversa.

**Tempo entre descoberta de um vetor por auditoria e a família de controle correspondente entrar
em produção.** Fonte: data de `VetorRisco.data_descoberta` até a data de deploy do controle. Esse
intervalo é o tempo em que o sistema fica exposto ao vetor já conhecido mas não mitigado —
minimizar esse intervalo é mais valioso do que minimizar o número absoluto de vetores
descobertos.
