---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Fluxogramas

```mermaid
flowchart TD
    A[Pergunta recebida] --> B[Recupera N candidatos via 14-VECTOR]
    B --> C[Reordena por relevancia especifica a pergunta]
    C --> D[Confirma validade de cada sobrevivente via 11-KNOWLEDGE]
    D --> E{Ha candidatos validos suficientes?}
    E -->|Nao| F[Recusa explicita: sem fonte suficiente]
    E -->|Sim| G[Compoe contexto, gera resposta]
    G --> H[Mede fidelidade da resposta contra o contexto]
    H --> I{Fidelidade aceitavel?}
    I -->|Nao| J[Resposta rejeitada ou sinalizada como nao confiavel]
    I -->|Sim| K[Resposta entregue com citacoes]
```

Dois pontos de recusa existem no fluxo (`E` e `I`), e são propositalmente distintos: `E` recusa
por falta de fonte antes mesmo de gerar qualquer resposta; `I` recusa depois de gerar, porque a
geração produziu algo que não se sustenta no que foi citado, mesmo com fonte suficiente
disponível. Confundir os dois pontos de recusa esconde qual das duas causas está de fato
acontecendo quando o sistema não entrega resposta.

## O caminho que mais se ignora

Pular `D` (confirmar validade depois da reordenação) "porque o índice já garantiria isso" é um
erro sutil — `14-VECTOR` garante correção da busca vetorial, não validade de ciclo de vida do
documento, que é responsabilidade de `11-KNOWLEDGE` e pode ter mudado entre a indexação original
e o momento desta consulta específica.

## Estados de uma consulta ao longo do pipeline

```mermaid
stateDiagram-v2
    [*] --> Recuperando
    Recuperando --> Reordenando: candidatos obtidos
    Reordenando --> ConfirmandoValidade: relevancia calculada
    ConfirmandoValidade --> RecusadaSemFonte: zero candidato valido
    ConfirmandoValidade --> Gerando: candidato valido suficiente
    Gerando --> MedindoFidelidade: resposta produzida
    MedindoFidelidade --> RecusadaPorFidelidade: abaixo do limiar
    MedindoFidelidade --> Entregue: fidelidade aceitavel
    RecusadaSemFonte --> [*]
    RecusadaPorFidelidade --> [*]
    Entregue --> [*]
```

Os dois estados de recusa (`RecusadaSemFonte`, `RecusadaPorFidelidade`) nunca se confundem no
diagrama, porque nascem de transições diferentes — a primeira sai de `ConfirmandoValidade`, antes
de qualquer geração acontecer; a segunda só é alcançável depois de `Gerando`, o que por si só já
documenta que a causa da recusa é posterior à existência de fonte válida. Um sistema de logs que
registra só "recusada: true/false" sem preservar de qual estado a recusa veio perde exatamente a
informação que esse diagrama existe para tornar visível.
