---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Fluxogramas

```mermaid
flowchart TD
    A[Candidato gerado] --> B{Orcamento de tentativas ainda disponivel?}
    B -->|Nao| C[Busca encerrada, retorna melhor proposta ate agora]
    B -->|Sim| D[Avalia candidato contra casos_de_ouro]
    D --> E[Registra tentativa no historico, aprovada ou nao]
    E --> F{Melhoria supera limiar minimo acima do baseline?}
    F -->|Nao| G[Candidato descartado como proposta, mas permanece no historico]
    F -->|Sim| H{E melhor que a melhor proposta ja encontrada?}
    H -->|Sim| I[Atualiza melhor proposta]
    H -->|Nao| G
    I --> B
    G --> B
```

O nó `E` (registro no histórico) acontece antes do nó `F` (critério de melhoria) — toda tentativa
é registrada independente de o resultado da avaliação de melhoria, porque o registro serve para
visibilidade do espaço já explorado, não apenas para as tentativas que "venceram".

## Ciclo de vida de uma proposta

```mermaid
stateDiagram-v2
    [*] --> Gerada
    Gerada --> Avaliada: avaliada contra a mesma amostra do baseline
    Avaliada --> Descartada: nao supera limiar de melhoria
    Avaliada --> Proposta: supera limiar e e a melhor ate agora
    Descartada --> [*]
    Proposta --> SubmetidaAo07: fluxo externo, fora deste volume
    SubmetidaAo07 --> [*]
```

O estado `Proposta` nunca transiciona diretamente para um estado de "promovida" dentro deste
volume — a única saída de `Proposta` é `SubmetidaAo07`, e o que acontece depois dessa submissão
já pertence à máquina de estados do 07, não a este volume.


## Relação entre O2 e O5

Um candidato pode ser rejeitado (não vira proposta, por O2) e ainda assim ser registrado
integralmente (por O5) — as duas regras operam em momentos diferentes: O2 decide o que se torna
saída da busca; O5 garante que a busca inteira, incluindo o que não virou saída, permanece
visível para quem quiser revisar depois.

Confundir os dois papéis levaria a um histórico incompleto ou a uma proposta contaminada por tentativa mal avaliada.

Manter os dois separados no fluxograma, com setas distintas para cada consequência, evita essa
confusão desde a leitura do próprio diagrama, antes mesmo de chegar ao texto que a explica em
bem mais detalhe logo abaixo, ainda na mesma seção deste documento específico aqui.