---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Chamador (backend, 23)", "Solicita roteamento para uma tarefa")
    System(router, "LLM Router", "Escolhe candidato, detecta degradacao, aplica fallback")
    System_Ext(selecao, "Selecao de Modelo (26)", "Fornece candidatos aprovados e fallback declarado")
    System_Ext(saude, "Sinal de Saude", "Taxa de falha e latencia observadas por janela")

    Rel(dev, router, "Solicita roteamento para a tarefa")
    Rel(selecao, router, "Fornece candidatos aprovados")
    Rel(saude, router, "Alimenta janela de sinal usada para julgar degradacao")
    Rel(router, dev, "Retorna candidato escolhido e motivo")
```

O roteador nunca consulta `Selecao de Modelo (26)` durante o roteamento em si — a lista de
candidatos aprovados é fornecida a ele previamente, mantendo a decisão de roteamento rápida e
sem depender de uma chamada síncrona adicional a cada requisição.

```mermaid
sequenceDiagram
    participant Backend as Backend (23)
    participant Router as LLM Router
    participant Saude as Sinal de Saude

    Backend->>Router: rotear(tarefa, principal, fallback, sinal_principal)
    Router->>Router: valida que principal e fallback sao aprovados (L1)
    Router->>Saude: consulta sinal acumulado do principal
    Saude-->>Router: SinalDeSaude (chamadas, falhas, latencia)
    Router->>Router: esta_degradado? (L4, exige amostra minima)
    alt principal saudavel
        Router-->>Backend: DecisaoDeRoteamento(principal, "principal_saudavel")
    else principal degradado
        Router-->>Backend: DecisaoDeRoteamento(fallback, "fallback_por_degradacao")
    end
    Router->>Router: registra decisao no historico (L3)
```

A validação de candidatos aprovados (L1) acontece antes de qualquer consulta a sinal de saúde —
não há razão para avaliar degradação de um candidato que nem deveria estar sendo considerado.


Essa escolha de design — buscar a lista de candidatos previamente, não a cada chamada — é o que
torna o roteamento rápido o suficiente para ficar no caminho crítico de cada requisição, sem
adicionar uma consulta síncrona extra a outro sistema toda vez que uma decisão precisa ser
tomada.

O diagrama de sequência não modela retry da chamada de sinal de saúde em si — essa responsabilidade, se necessária, pertence à integração real com observabilidade, fora do escopo deste modelo mínimo.

Esse limite de escopo mantém o diagrama focado na decisão que este volume de fato governa, sem
tentar documentar comportamento que já é responsabilidade de outro volume vizinho, como o 16 ou
o 21. Manter os dois diagramas enxutos, cobrindo só a decisão de roteamento em si, é consistente
com a regra de volume perecível — menos superfície documentada significa menos texto que
envelhece mal quando a topologia real do sistema mudar.