---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

Este volume, por definição, é sobre a infraestrutura que produz métricas de outros volumes — as
métricas próprias dele medem a saúde do próprio mecanismo de observabilidade, não o comportamento
dos sistemas observados.

**Taxa de sinais emitidos que nunca chegam ao coletor** (perda de telemetria). Fonte: comparação
entre contagem de eventos que o motor de origem registra ter emitido e contagem que o coletor
confirma ter recebido. Uma taxa de perda maior que zero é, em si, um problema de observabilidade
sobre a observabilidade — sinal de que a infraestrutura de coleta precisa de atenção antes de
qualquer análise dos sinais em si ser confiável.

**Tempo entre um sinal cruzar o limiar e a notificação correspondente ser confirmada como
entregue.** Fonte: timestamp do `Alerta.notificado_em` menos timestamp do `Sinal`. Esse
intervalo é a latência real de resposta possível a um problema — um sinal detectado
instantaneamente mas notificado horas depois oferece pouca vantagem sobre não ter sido detectado.

**Frequência de recalibração de limiar por categoria de sinal**, com o motivo registrado (ajuste
por comportamento real do sistema versus ajuste por limiar mal calibrado inicialmente). Essa
métrica, ao longo do tempo, indica se os limiares deste sistema estão convergindo para valores
estáveis ou continuam sendo ajustados com frequência alta, o que sugeriria instabilidade real no
comportamento do sistema observado, não só imprecisão do processo de calibração.

**Disponibilidade do canal de notificação, medida por heartbeat periódico** — a métrica que
`07-Regras.md` trata como controle obrigatório, não opcional.
