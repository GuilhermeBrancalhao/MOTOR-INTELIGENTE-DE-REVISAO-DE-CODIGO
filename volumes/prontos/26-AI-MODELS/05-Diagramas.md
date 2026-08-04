---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Declara requisito de capacidade da tarefa")
    System(selecao, "Selecao de Modelo", "Requisito, avaliacao, fallback, custo por tarefa")
    System_Ext(ouro, "Casos de Ouro (07)", "Barra de avaliacao reaproveitada para modelo")
    System_Ext(router, "LLM Router (27)", "Roteia chamada entre candidatos ja selecionados")

    Rel(dev, selecao, "Declara requisito e recebe lista de candidatos aprovados")
    Rel(selecao, ouro, "Avalia candidato contra os mesmos casos de ouro do 07")
    Rel(selecao, router, "Fornece candidatos aprovados, principal e fallback")
```

O `LLM Router (27)` nunca decide sozinho quais modelos são elegíveis — ele recebe a lista já
filtrada por este volume, o que mantém a fronteira entre "quais modelos podem ser usados" (aqui)
e "qual candidato específico atende esta chamada agora" (naquele) sem sobreposição.

```mermaid
sequenceDiagram
    participant Dev as Time de desenvolvimento
    participant Sel as Selecao de Modelo
    participant Ouro as Casos de Ouro (07)

    Dev->>Sel: declara RequisitoDeCapacidade da tarefa
    Sel->>Sel: filtra candidatos que atendem o requisito
    Sel->>Ouro: avalia cada candidato restante
    Ouro-->>Sel: ResultadoDeAvaliacao por candidato
    Sel->>Sel: aprova candidatos acima do limiar
    Sel-->>Dev: PlanoDeTarefa (modelo principal + fallback)
```

Nenhum candidato chega à etapa de aprovação sem antes passar pelo filtro de requisito — um modelo
poderoso mas que não atende a modalidade ou janela de contexto exigida nunca chega a ser avaliado
contra os casos de ouro, economizando o custo de uma avaliação que já seria descartada de
qualquer forma.


O C4Context deixa explícito que `Selecao de Modelo` nunca conversa diretamente com um provedor de
modelo específico — essa conversa, quando existe, acontece através do `LLM Router (27)`, mantendo
este volume livre de qualquer acoplamento a fornecedor específico, alinhado à regra de volume
perecível.

O `sequenceDiagram` termina na entrega de um `PlanoDeTarefa`, não numa chamada real ao modelo —
esse limite é intencional, porque o que acontece depois da seleção (a chamada em si, roteada pelo
27) já não é responsabilidade deste volume.

Isso mantém o diagrama estável mesmo quando o mecanismo de roteamento do 27 mudar por dentro,
sem exigir revisão deste volume só porque a implementação daquele mudou de tecnologia.