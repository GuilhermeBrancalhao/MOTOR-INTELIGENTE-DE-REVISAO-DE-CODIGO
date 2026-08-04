---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Solicita compilacao para uma chamada")
    System(compilador, "Prompt Compiler", "Traduz prompt promovido em payload concreto")
    System_Ext(prompt, "Prompt Engine (07)", "Fornece prompt PROMOVIDO com contrato")
    System_Ext(dialeto, "Dialeto do Provedor", "Formatacao especifica, injetada como adaptador")

    Rel(dev, compilador, "Solicita compilacao: prompt, variaveis, dialeto, orcamento")
    Rel(compilador, prompt, "Consome prompt ja promovido, nunca rascunho")
    Rel(compilador, dialeto, "Delega formatacao de mensagem ao adaptador do provedor")
    Rel(compilador, dev, "Retorna PayloadCompilado ou erro explicito")
```

O `Prompt Compiler` nunca decide, por conta própria, que um prompt está pronto para uso — essa
decisão já foi tomada pelo `Prompt Engine (07)` antes de o prompt sequer chegar aqui. A seta entre
os dois é unidirecional: o compilador consome o contrato promovido, nunca escreve de volta no
registro do 07.

```mermaid
sequenceDiagram
    participant Dev as Time de desenvolvimento
    participant Comp as Prompt Compiler
    participant Dial as Dialeto do Provedor

    Dev->>Comp: compilar(prompt, variaveis, dialeto, orcamento)
    Comp->>Comp: prompt esta PROMOVIDO? (Q1)
    Comp->>Comp: todas as variaveis declaradas foram fornecidas? (Q6)
    Comp->>Comp: pontos de cache em posicao valida? (Q5)
    Comp->>Comp: renderiza corpo com variaveis
    Comp->>Dial: formatar_mensagens(corpo renderizado)
    Dial-->>Comp: mensagens no formato do provedor
    Comp->>Comp: tokens estimados <= orcamento? (Q3)
    Comp-->>Dev: PayloadCompilado (ou erro explicito na etapa que falhou)
```

Cada verificação do diagrama de sequência tem uma posição fixa — nenhuma delas é pulada nem
reordenada, porque cada uma pressupõe que a anterior já passou (não faz sentido checar orçamento
de um payload que nunca chegou a ser renderizado por variável ausente).


O adaptador `Dialeto do Provedor`, no C4Context, aparece como sistema externo injetado, nunca
como parte interna do `Prompt Compiler` — essa modelagem visual reforça Q4: o núcleo nunca
incorpora lógica de provedor específico, apenas consome o que o adaptador fornece.

Isso mantém o compilador substituível por qualquer implementação futura de tradução de provedor sem exigir mudança neste diagrama.

A troca de um dialeto por outro nunca exige tocar nenhum outro componente do sistema representado
nos dois diagramas, incluindo o próprio `Prompt Compiler`, cujo comportamento central permanece
idêntico independente de qual adaptador está conectado a ele no momento da compilação — essa
estabilidade é o que permite adicionar suporte a um provedor novo sem revisar código já testado.