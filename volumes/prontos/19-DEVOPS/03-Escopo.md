---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o pipeline de entrega: a sequência de estágios (build, teste, segurança,
staging, produção), a estratégia de rollout que limita raio de impacto, e o mecanismo de
reversão.

**Fronteira com `18-DEVSECOPS`.** O gate de segurança é uma etapa deste pipeline, executada na
posição que a ordem de estágios determina — este volume define a sequência e a regra de que
nenhum estágio é pulado; o 18 define o que acontece dentro da etapa de segurança especificamente
(bloqueio por padrão, waiver com prazo). Uma falha no estágio de segurança bloqueia o pipeline
pela mesma regra que qualquer outro estágio falho bloquearia — este volume não duplica a lógica
de waiver do 18, apenas garante que o resultado dela é respeitado na ordem correta.

**Fronteira com `20-CLOUD`.** A infraestrutura que hospeda o sistema em execução — computação,
rede, armazenamento — é do 20. Este volume trata de como uma mudança chega até essa
infraestrutura, não de como a infraestrutura em si é provisionada ou dimensionada.

**Fronteira com `21-OBSERVABILITY`.** A decisão de reverter um deploy frequentemente é informada
por sinal de observabilidade (métrica degradando após rollout), mas este volume define o
mecanismo de reversão em si, não a detecção do sinal que motiva usá-lo.

Não cobre política de quando um deploy é aprovado por humano versus automático — isso depende de
`32-QUALITY` e do apetite a risco específico de cada organização, fora do escopo deste volume.
