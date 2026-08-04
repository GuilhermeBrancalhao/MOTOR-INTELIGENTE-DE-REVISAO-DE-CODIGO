---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Começar todo rollout novo com o menor percentual de tráfego que ainda produz sinal estatístico
confiável, aumentando por etapas — não pular direto para metade do tráfego só porque o primeiro
incremento passou sem alarme.

Testar o caminho de reversão fora de um incidente real, como parte da validação do próprio
pipeline — a primeira vez que uma reversão é executada não deveria ser durante uma emergência.

Manter o histórico de deploys legível por humano, não apenas por máquina — quem está triando um
incidente precisa conseguir ver rapidamente qual foi o último artefato estável antes do problema.

Tratar toda justificativa de deploy completo (P3) como registrada, não verbal — a mesma disciplina
de rastreabilidade que vale para waiver de segurança (18) vale para exceção de rollout.


Documentar, junto de cada estágio do pipeline, qual sinal externo (log, métrica, relatório de
teste) prova que ele passou — a confiança na sequência depende de cada estágio de fato verificar
algo real, não apenas retornar sucesso por padrão quando a verificação não está implementada
ainda.


Registrar o motivo de cada reversão junto do registro de rollback, mesmo que o mecanismo não
exija esse campo estruturalmente — o histórico de deploy é lido por humanos tentando entender o
que aconteceu, e "revertido, motivo desconhecido" é quase tão inútil quanto não ter revertido.