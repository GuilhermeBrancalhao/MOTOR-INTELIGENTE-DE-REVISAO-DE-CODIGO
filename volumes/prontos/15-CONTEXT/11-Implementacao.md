---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/15-context/orcamento.py -->

`orcamento.py`, citado acima, formaliza C1-C6: `Orcamento` recusa `margem_compactacao` zero
(C4); `montar_janela` descarta por `ORDEM_DE_PRIORIDADE`, nunca por ordem de chegada (C2); todo
item removido gera `Descarte` correspondente (C3); `INSTRUCAO_SISTEMA` só é recusada, nunca
descartada silenciosamente, quando sozinha excede o orçamento total (C6).

## Como o motor real aplicaria isto

A implementação mínima trata orçamento como recurso a ser reservado antecipadamente por
categoria de prioridade alta antes de preencher com categorias de prioridade menor — não como
preenchimento livre seguido de poda quando o limite é atingido. As duas abordagens chegam a
resultado parecido no caso comum, mas a reserva antecipada torna mais fácil garantir C6 (nunca
descartar silenciosamente instrução de prioridade máxima).

## Onde a integração com outros volumes acontece

Documento recuperado por `13-RAG` chega como `ItemDeContexto` de categoria
`DOCUMENTO_RECUPERADO` — a tradução acontece na fronteira entre os dois volumes, e a partir daí
este volume trata o documento como qualquer outro item competindo por orçamento, sem
conhecimento de que veio de um pipeline de RAG especificamente.

A ordem de implementação recomendada é: `ItemDeContexto`, `Categoria` e `Orcamento` primeiro,
testados contra os cenários de configuração inválida. `montar_janela` com descarte por prioridade
depois, testado sob pressão artificial de orçamento pequeno. Gatilho de compactação
(`proximo_da_margem`) por último, porque é independente da lógica de montagem e pode ser
verificado isoladamente antes de integrar ao ciclo completo.
