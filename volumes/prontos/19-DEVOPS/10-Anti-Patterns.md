---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Deploy direto em produção "só desta vez", contornando o pipeline por urgência.** É exatamente
nos momentos de maior pressão que os estágios evitáveis mais importam — a urgência não reduz o
risco de pular etapas, aumenta o custo de um erro não capturado.

**Rollback que reconstrói a partir do código-fonte em vez de promover o artefato anterior já
validado.** Reintroduz o próprio risco de divergência que a imutabilidade do artefato (P6) existe
para eliminar, e converte uma operação que deveria ser rápida em outro ciclo completo de
pipeline.

**Deploy completo como padrão, com rollout gradual reservado para mudanças "arriscadas".**
Inverte a lógica de P3 — a decisão de que uma mudança é segura o suficiente para pular o rollout
gradual é justamente a decisão mais fácil de errar, porque é feita antes de qualquer sinal real
de produção existir.

**Histórico de deploy que não distingue um deploy normal de uma reversão.** Sem essa distinção,
entender a história recente de uma produção instável fica mais difícil do que precisa ser.


**Confiar no rollout gradual sem checar sinal de observabilidade entre incrementos.** Um
percentual crescente de tráfego sem verificação no meio do caminho equivale, na prática, a um
deploy completo dividido em etapas cronometradas, não a um deploy que de fato reage a sinal de
problema antes de avançar.