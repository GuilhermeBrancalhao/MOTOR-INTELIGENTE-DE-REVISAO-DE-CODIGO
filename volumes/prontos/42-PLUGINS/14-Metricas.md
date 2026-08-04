---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Métricas

**Número de tentativa de ativação recusada por incompatibilidade de contrato, por período.** Um
número alto pode indicar documentação de contrato pouco clara para quem desenvolve plugin novo,
não necessariamente um problema do próprio mecanismo de verificação.

**Número de falha de hook contida pelo isolamento, por plugin, por período.** Um plugin com taxa
de falha crescente é candidato a revisão ou desativação preventiva antes que afete a experiência
de quem o mantém ativo.

**Número de tentativa de acesso a capacidade não declarada, por plugin.** Qualquer ocorrência
maior que zero merece investigação — pode indicar tanto um bug no plugin quanto uma tentativa
deliberada de exceder o que foi autorizado na ativação.

**Tempo entre publicação de nova versão maior de contrato e migração completa dos plugins
existentes para a versão nova.** Contextualiza se o ciclo de depreciação do próprio contrato de
extensão está dando tempo real de adaptação a quem mantém plugin publicado.

Nenhuma dessas métricas substitui revisão humana periódica de quais plugins seguem ativos e por
quê — elas servem como sinal agregado que orienta onde investigar primeiro, não como critério
automático único para desativar ou aprovar um plugin específico sem revisão de quem opera o
host.

Comparar essas métricas entre plugins diferentes do mesmo host pode revelar qual deles concentra
desproporcionalmente falha, tentativa de capacidade indevida, ou tempo de migração lento —
sinalizando onde investir revisão adicional antes que o problema afete negativamente a experiência
de quem depende daquele plugin específico no dia a dia.