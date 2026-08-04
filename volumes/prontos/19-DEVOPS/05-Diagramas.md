---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Autor da mudanca")
    System(pipeline, "Pipeline de Entrega", "Estagios BUILD-TESTE-SEGURANCA-STAGING-PRODUCAO")
    System_Ext(seguranca, "Gate de Seguranca (18)", "Controles do 17-SECURITY enforçados")
    System_Ext(infra, "Infraestrutura (20-CLOUD)", "Hospeda o sistema em execucao")
    System_Ext(observ, "Observabilidade (21)", "Sinal que motiva reversao")

    Rel(dev, pipeline, "Envia commit")
    Rel(pipeline, seguranca, "Executa estagio de seguranca")
    Rel(pipeline, infra, "Implanta artefato validado")
    Rel(infra, observ, "Emite sinal de execucao")
    Rel(observ, dev, "Alerta sobre degradacao, motiva reversao")
```

O time de desenvolvimento nunca fala diretamente com a infraestrutura — toda mudança passa pelo
pipeline, que por sua vez consulta o gate de segurança do 18 como uma de suas etapas antes de
alcançar a infraestrutura do 20. O sinal de observabilidade do 21 fecha o ciclo, informando a
decisão de reverter sem fazer parte do caminho de implantação em si.

```mermaid
sequenceDiagram
    participant Dev as Time de desenvolvimento
    participant Pipe as Pipeline
    participant Sec as Gate de Seguranca (18)
    participant Infra as Infraestrutura (20-CLOUD)

    Dev->>Pipe: commit (artefato candidato)
    Pipe->>Pipe: BUILD
    Pipe->>Pipe: TESTE
    Pipe->>Sec: estagio SEGURANCA
    Sec-->>Pipe: aprovado (ou excecao com waiver)
    Pipe->>Pipe: STAGING
    alt deploy gradual (padrao)
        Pipe->>Infra: implanta 25% do trafego
    else deploy completo (excecao justificada)
        Pipe->>Infra: implanta 100% do trafego
    end
    Infra-->>Dev: artefato rastreavel ao commit original
```

A troca de mensagens entre `Pipe` e `Sec` no diagrama de sequência é a mesma etapa que o
diagrama de estados do `06-Fluxogramas.md` detalha por dentro — aqui aparece como uma única
interação porque, do ponto de vista do pipeline, o resultado do gate é tudo o que importa para
decidir se avança; a lógica interna de waiver e expiração já foi resolvida pelo 18 antes de
responder.

```mermaid
flowchart TD
    A[Commit chega ao pipeline] --> B[BUILD]
    B --> C{Passou?}
    C -->|Nao| X[Bloqueado, nenhum estagio seguinte roda]
    C -->|Sim| D[TESTE]
    D --> E{Passou?}
    E -->|Nao| X
    E -->|Sim| F[SEGURANCA - gate do 18-DEVSECOPS]
    F --> G{Passou ou tem waiver ativo?}
    G -->|Nao| X
    G -->|Sim| H[STAGING]
    H --> I{Passou?}
    I -->|Nao| X
    I -->|Sim| J{Deploy completo sem justificativa?}
    J -->|Sim| K[Rejeitado: exige justificativa explicita]
    J -->|Nao| L[PRODUCAO - rollout gradual por padrao]
```

O nó `X` (bloqueio) tem várias entradas mas nenhuma saída que contorne o pipeline — cada estágio
que falha leva ao mesmo destino, e não existe um caminho alternativo que permita a uma mudança
chegar a `L` sem ter passado por todos os nós anteriores em ordem. O nó `J` é a materialização de
P3: o padrão do fluxo é a resposta "não" (rollout gradual), e a resposta "sim" (deploy completo)
é o caminho que exige uma decisão explícita para ser tomado, nunca o caminho de menor resistência.
