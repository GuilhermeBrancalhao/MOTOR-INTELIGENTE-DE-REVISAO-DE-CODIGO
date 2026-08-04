---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Define especificacao, revisa codigo gerado")
    System(gerador, "Motor de Geracao", "Produz codigo a partir de especificacao versionada")
    System_Ext(validacao, "Pipeline de Validacao (19)", "Compilacao e teste, mesma disciplina de codigo humano")
    System_Ext(revisao, "Revisao Humana", "Portao obrigatorio antes de producao")

    Rel(dev, gerador, "Fornece especificacao versionada e escopo declarado")
    Rel(gerador, validacao, "Codigo gerado passa pela mesma validacao de codigo humano")
    Rel(validacao, revisao, "Codigo validado aguarda revisao humana obrigatoria")
    Rel(revisao, dev, "Aprovacao ou rejeicao, nunca automatica")
```

Nenhuma seta liga `Motor de Geracao` diretamente a produção — todo código gerado passa por
`Pipeline de Validacao` e por `Revisão Humana` antes de qualquer consequência real, o mesmo
caminho que código escrito manualmente atravessaria.

```mermaid
sequenceDiagram
    participant Dev as Time de desenvolvimento
    participant Ger as Motor de Geracao
    participant Val as Pipeline de Validacao
    participant Rev as Revisao Humana

    Dev->>Ger: gerar(especificacao versionada)
    Ger-->>Dev: CodigoGerado, marcado como gerado
    Dev->>Val: submete para validacao
    Val-->>Dev: compilou? testes passaram?
    alt validacao falhou
        Dev->>Ger: ajusta especificacao, gera novamente
    else validacao passou
        Dev->>Rev: submete para revisao humana
        Rev-->>Dev: aprovado ou rejeitado
    end
```

O ramo de falha de validação nunca leva a editar o código gerado diretamente — leva de volta ao
gerador, com a especificação ajustada, preservando a garantia de que o código de saída sempre
reflete sua especificação de origem.


O `C4Context` deixa claro que o `Motor de Geração` nunca fala diretamente com produção — toda
saída atravessa primeiro o `Pipeline de Validação` e depois a `Revisão Humana`, o mesmo caminho
que qualquer código escrito manualmente também atravessaria antes de qualquer consequência real
acontecer no sistema em produção.

O sequenceDiagram, por sua vez, mostra o ciclo completo de uma tentativa de geração até a decisão final, incluindo o caminho de retorno quando a validação falha.

Isso torna explícito, num único diagrama, o momento exato em que a especificação original é
revisitada em vez de o código de saída ser remendado diretamente, reforçando visualmente a
mesma disciplina que a prosa da seção anterior já descreve em detalhe textual completo, dando ao
leitor duas formas independentes de internalizar exatamente a mesma garantia central.