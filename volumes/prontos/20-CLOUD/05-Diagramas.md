---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(op, "Time de operacao", "Declara e mantem a infraestrutura")
    System(plano, "Plano de Infraestrutura", "Recursos declarados, redundancia, atribuicao de custo")
    System_Ext(deploy, "Pipeline de Entrega (19)", "Implanta artefato sobre a infraestrutura declarada")
    System_Ext(real, "Estado Real Provisionado", "O que de fato existe no provedor de nuvem")
    System_Ext(portfolio, "Enterprise Architecture (06)", "Consome custo e concentracao para decisao de portfolio")

    Rel(op, plano, "Declara recursos, ambiente, dono")
    Rel(deploy, plano, "Implanta sobre recursos ja declarados")
    Rel(plano, real, "Detecta divergencia (drift) contra o real")
    Rel(plano, portfolio, "Expoe custo e redundancia para decisao de portfolio")
```

O time de operação nunca interage diretamente com o estado real provisionado — toda declaração
passa pelo `Plano de Infraestrutura`, que é o único componente que compara o declarado contra o
real. Essa centralização é o que torna a detecção de divergência (N6) possível: sem um ponto único
de comparação, cada parte do sistema poderia ter uma visão diferente e desatualizada do que
realmente existe.

```mermaid
sequenceDiagram
    participant Op as Time de operacao
    participant Plano as Plano de Infraestrutura
    participant Real as Estado Real Provisionado

    Op->>Plano: declara Recurso (nome, tipo, ambiente, dono, redundante)
    Plano->>Plano: valida dono presente (N3) e ausencia de segredo inline (N5)
    Plano-->>Op: recurso aceito ou rejeitado
    Op->>Plano: verifica redundancia contra alvo de disponibilidade
    Plano-->>Op: lista de recursos sem redundancia exigida (N2)
    Plano->>Real: consulta estado real provisionado
    Real-->>Plano: recursos efetivamente existentes
    Plano->>Plano: compara declarado x real
    Plano-->>Op: divergencias encontradas (N6)
```

A validação de N3 e N5 acontece antes de qualquer verificação de redundância ou drift — um
recurso mal declarado (sem dono, ou com segredo inline) nunca chega a ser avaliado quanto a
disponibilidade ou comparado contra o estado real, porque ele nem deveria existir como declaração
válida em primeiro lugar.


O `Estado Real Provisionado`, no C4Context, é deliberadamente um sistema externo, não parte do
`Plano de Infraestrutura` — essa separação reflete que o real é observado, nunca controlado
diretamente pelo plano; o plano só consegue comparar, nunca impor, o que de fato existe do lado
do provedor.


O diagrama de sequência mostra a ordem de validação como uma cadeia estrita: N3 e N5 antes de
qualquer avaliação de N2, e N6 só depois que a declaração já é conhecida válida. Inverter essa
ordem — checar redundância antes de garantir que o recurso tem dono, por exemplo — produziria
verificações sobre um recurso que talvez nem devesse ter sido aceito como declaração em primeiro
lugar.