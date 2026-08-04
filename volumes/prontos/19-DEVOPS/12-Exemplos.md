---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — pipeline completo, deploy gradual aprovado

Um artefato passa por BUILD, TESTE, SEGURANCA e STAGING, todos com sucesso. O deploy em produção é
solicitado com 25% de tráfego inicial — dentro do padrão de rollout gradual, sem exigir
justificativa adicional.

## Caso 2 — falha em TESTE bloqueia os estágios seguintes

O estágio TESTE falha. Uma tentativa de executar SEGURANCA em seguida é rejeitada, porque a
posição esperada da sequência ainda é TESTE — a falha nunca é silenciosamente contornada avançando
para o próximo estágio.

## Caso 3 — deploy completo sem justificativa é rejeitado

Um pipeline completo tenta implantar 100% do tráfego de uma vez, sem `forcar_completo=True`. A
tentativa é rejeitada — o caminho de menor resistência é o rollout gradual, e o deploy completo só
acontece quando alguém decide isso explicitamente.

## Caso 4 — reversão sem histórico anterior falha, com histórico funciona

Uma tentativa de reverter um ambiente que só recebeu um deploy até agora falha explicitamente, por
não haver versão anterior. Depois de um segundo deploy bem-sucedido, reverter promove de volta o
artefato do primeiro deploy — sem reconstruir nada, apenas reaplicando o que já foi validado.


Os quatro casos cobrem, juntos, as três formas de bloqueio (estágio fora de ordem, pipeline
incompleto, deploy completo sem justificativa) mais o ciclo completo de implantação e reversão —
a mesma cobertura que os testes da seção seguinte verificam individualmente, caso a caso.


Nenhum dos quatro casos depende de infraestrutura real ou de um provedor de nuvem específico —
todos rodam inteiramente sobre a lógica de `Pipeline` e `GerenciadorDeploy`, o que é intencional:
a garantia que este volume oferece (sequência não pulável, rollout gradual por padrão,
rastreabilidade, reversão) precisa valer independentemente de qual infraestrutura do 20-CLOUD
efetivamente executa o deploy.