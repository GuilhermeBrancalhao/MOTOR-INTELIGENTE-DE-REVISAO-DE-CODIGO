---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/14-vector/indice.py -->

`indice.py`, citado acima, formaliza V1-V6: `Vetor` carrega `versao_modelo` obrigatória e
`comparar` recusa vetores de versões diferentes (V1); `Consulta` exige métrica e partição
explícitas, sem padrão implícito (V2, V3); `buscar` nunca devolve vetor de partição diferente da
consultada (V3) nem documento presente em `conjunto_excluidos` (V6).

## Como o motor real aplicaria isto

A implementação mínima separa claramente o armazenamento de vetores (que pode usar qualquer
estrutura de indexação eficiente — árvore, grafo de proximidade, hash locality-sensitive) da
camada de validação de consulta (que aplica V1-V3 antes de qualquer busca acontecer). Misturar as
duas camadas — deixar a estrutura de indexação também validar consulta — dificulta trocar a
implementação de indexação sem revisar toda a lógica de validação junto.

## Onde a integração com outros volumes acontece

`11-KNOWLEDGE` entrega documento validado; este volume gera e armazena o vetor correspondente,
nunca questiona se o documento deveria existir. `13-RAG` consome resultado de busca deste volume
como entrada para reordenação e composição de resposta — a fronteira exata está em
`03-Escopo.md`.

A ordem de implementação recomendada é: `Vetor` e `Consulta` primeiro, com a validação de campos
obrigatórios testada isoladamente. Comparação e busca depois, testadas contra os cenários de
cruzamento de partição e versão. Gestão de ciclo de vida de índice (construir, validar, trocar,
reter, descartar) por último, porque depende dos componentes anteriores já estarem corretos antes
de orquestrar a troca atômica entre versões.
