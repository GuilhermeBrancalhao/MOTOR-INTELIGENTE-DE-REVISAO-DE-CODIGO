---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Integração entre os motores deste ciclo. O exemplo deste volume prova o contrato isoladamente;
a ponte com os volumes vizinhos — traduzir os tipos de um para os do outro — ainda não tem teste
que a exercite de ponta a ponta.

Otimização de agendamento entre nós prontos simultaneamente (qual executar primeiro quando há
mais nós prontos do que capacidade de concorrência disponível) — hoje o contrato não especifica
critério de prioridade, só respeita dependência e limite de concorrência. Um critério de
prioridade explícito (por exemplo, priorizar nós com mais dependentes transitivos) é extensão
possível, não parte do contrato mínimo atual.

Cancelamento de nós já em `Executando` quando o chamador decide abortar o grafo inteiro
externamente (não por falha de outro nó, mas por decisão do chamador) — não especificado hoje;
o contrato assume que uma vez que um nó começou a executar, ele é observado até seu próprio
encerramento.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (planejador topológico com detecção de ciclo, testado por
mutação) — é o componente mais fácil de isolar e testar sem depender de nenhum outro volume.
Depois, a integração real com `08-AGENT-ENGINE`, quando aquele volume também tiver código
citável.

## O que este volume assume que pode mudar

O conjunto de três políticas de falha (`AbortarDependentes`, `PularDependentes`,
`RetryComBackoff`) pode crescer se um caso de uso real expuser uma quarta política necessária —
por exemplo, uma política de "substituir por valor padrão e continuar" para nós não-críticos.
Qualquer política nova precisa manter a garantia de resultado granular por nó descrita em
`07-Regras.md`.
