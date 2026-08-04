---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Estratégia de indexação específica (árvore, grafo de proximidade, hash locality-sensitive) — este
volume trata do contrato de correção (versão, métrica, partição, exclusão), não da estrutura de
dado que torna a busca eficiente em grande escala; a escolha de estratégia é decisão de
infraestrutura fora do escopo do contrato.

Migração incremental segura de modelo de embedding para bases muito grandes, onde reindexação
completa de uma vez pode ser inviável — o contrato atual assume reindexação completa como
operação atômica, mas não descreve como fatiar essa operação para bases que não cabem numa única
janela de manutenção.

Compactação física de documentos excluídos como processo formal — o volume garante exclusão
lógica (V6), mas não especifica gatilho nem frequência de compactação física, deixando isso como
decisão operacional não coberta.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (`Vetor`, `Consulta`, validação de campos obrigatórios,
exclusão lógica), testado por mutação nas seis regras. Depois, integração real com
`11-KNOWLEDGE` (o momento exato em que documento validado chega para indexação) e `13-RAG`
(consumo de resultado de busca).

## O que este volume assume que pode mudar

O conjunto fechado de três métricas (V2) reflete o que é suficiente hoje — uma métrica adicional
pode emergir com caso de uso real, mas a regra de que métrica é sempre declarada explicitamente,
nunca inferida, permanece independente de quantas métricas existirem.
