---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de release com mudança que quebra compatibilidade corretamente versionada como
versão maior.** Deveria ser 100% por construção (AC1 impede release incorreto) — uma queda
indica falha no processo de release, não apenas descuido pontual.

**Número de elemento público sem uso externo conhecido detectável.** Um número alto sugere
superfície pública maior do que o necessário, aumentando o custo de manter compatibilidade para
elemento que talvez ninguém realmente use.

**Tempo médio entre depreciação de elemento público e sua remoção efetiva na próxima versão
maior.** Contextualiza se o ciclo de depreciação está dando tempo real de migração, não apenas
cumprindo formalidade mínima.

**Proporção de exemplo de documentação executado como parte da suíte de teste automatizada.**
Deveria tender a 100% — exemplo não executado automaticamente é o candidato mais provável a
divergir silenciosamente do comportamento real do SDK.

Nenhuma dessas métricas substitui a leitura direta do changelog de superfície pública por quem
decide sobre uma nova versão — elas servem como sinal agregado de saúde do processo de
versionamento ao longo do tempo, não como critério automático único para aprovar ou rejeitar um
release específico sem revisão humana do que de fato mudou.

Todas as quatro métricas são calculáveis a partir do próprio changelog de superfície pública e do
histórico de versão do SDK, sem exigir instrumentação adicional em tempo de execução do código
publicado — o que as torna baratas de manter atualizadas ao longo do tempo.