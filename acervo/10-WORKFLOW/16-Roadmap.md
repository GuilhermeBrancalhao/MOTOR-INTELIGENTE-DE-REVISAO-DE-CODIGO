---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Código executável de referência — este ciclo (2026-08-03) priorizou contrato, regras e diagramas
para os 10 volumes essenciais antes de implementação citável, decisão registrada em
`ENTREGA.md`.

Compensação/rollback de passos já concluídos quando um passo posterior falha de forma definitiva
(o padrão saga) — o contrato mínimo atual não especifica compensação automática, só retomada a
partir de checkpoint; um workflow que precisa desfazer efeito colateral de passo já concluído
teria que implementar essa lógica fora do motor hoje.

Timeout configurável para `AguardandoSinal`, com escalonamento automático — hoje o motor espera
indefinidamente por sinal externo; um timeout com alerta é extensão natural, registrada como
pendente, não parte do contrato atual.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (gestor de checkpoint com gravação atômica, testado com
falha injetada) — é a garantia mais crítica do motor e a mais fácil de isolar para teste sem
depender de outro volume. Depois, a integração real com `08-AGENT-ENGINE` para passos de IA que
invocam agente.

## O que este volume assume que pode mudar

O formato do `estado_acumulado` no checkpoint pode evoluir entre versões do motor — a separação
deliberada entre estado técnico e estado de negócio, descrita em `10-Anti-Patterns.md`, existe
justamente para que essa evolução seja possível sem quebrar checkpoints já gravados por versões
anteriores, desde que a compatibilidade de leitura seja mantida na camada técnica.
