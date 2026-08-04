---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Inicia busca com baseline e gerador de candidatos")
    System(otim, "Prompt Optimizer", "Busca variante, avalia, propoe, nunca promove")
    System_Ext(ouro, "Casos de Ouro (07)", "Funcao objetivo fixa durante toda a busca")
    System_Ext(prompt, "Prompt Engine (07)", "Unico lugar onde uma versao e promovida")

    Rel(dev, otim, "Inicia busca: baseline, candidatos, orcamento")
    Rel(otim, ouro, "Avalia cada candidato contra a mesma amostra")
    Rel(otim, dev, "Retorna proposta (ou nenhuma) e historico completo")
    Rel(dev, prompt, "Submete proposta ao fluxo normal de versionamento e promocao")
```

Não existe seta direta entre `Prompt Optimizer` e `Prompt Engine (07)` decidindo promoção — a
proposta sempre volta para quem iniciou a busca, e é esse fluxo humano (ou automatizado, mas
externo a este volume) que submete a proposta ao 07 como qualquer outra versão candidata.

```mermaid
sequenceDiagram
    participant Dev as Time de desenvolvimento
    participant Otim as Prompt Optimizer
    participant Ouro as Casos de Ouro (07)

    Dev->>Otim: buscar(baseline, gerador_de_candidatos)
    Otim->>Ouro: avalia baseline contra casos_de_ouro
    Ouro-->>Otim: taxa_acerto do baseline
    loop ate orcamento ou candidatos esgotarem
        Otim->>Ouro: avalia candidato contra casos_de_ouro (mesma amostra)
        Ouro-->>Otim: taxa_acerto do candidato
        Otim->>Otim: registra tentativa no historico (mesmo se rejeitada)
    end
    Otim-->>Dev: melhor proposta (se houver) + historico completo
```

A amostra `casos_de_ouro` aparece em toda iteração do loop como o mesmo valor — nunca uma amostra
diferente por candidato, porque comparar candidatos avaliados sob condições diferentes invalidaria
qualquer conclusão sobre qual de fato é melhor.


O diagrama de sequência mostra a mesma amostra `casos_de_ouro` sendo passada em cada iteração do
laço — essa repetição visual é intencional, reforçando que não existe um caminho alternativo onde
um candidato específico recebe tratamento diferente dos demais.

Nenhum outro valor aparece nessa posição em nenhuma parte do fluxo representado, do início ao fim da busca completa.

Essa consistência visual é o próprio argumento de O1 expresso em forma de diagrama, sem precisar
de explicação textual adicional para ser percebida por quem lê o fluxo pela primeira vez, sem
contexto prévio sobre as regras específicas deste volume — o diagrama já comunica a garantia
antes mesmo de o leitor chegar à seção de regras formais mais adiante no mesmo documento.