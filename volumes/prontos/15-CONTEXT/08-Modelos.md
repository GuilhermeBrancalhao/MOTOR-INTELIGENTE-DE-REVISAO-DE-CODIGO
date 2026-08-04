---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## ItemDeContexto

`ItemDeContexto(id: str, categoria: Categoria, tokens: int, conteudo: str)` — `categoria`
determina a prioridade via `ORDEM_DE_PRIORIDADE`, nunca inferida do conteúdo ou da ordem de
chegada.

## Categoria

`Categoria`: `INSTRUCAO_SISTEMA`, `HISTORICO_RECENTE`, `DOCUMENTO_RECUPERADO`,
`RESULTADO_FERRAMENTA`, `HISTORICO_ANTIGO` — enum fechado, com `ORDEM_DE_PRIORIDADE` mapeando
cada valor a um inteiro; menor número significa maior prioridade (nunca descartado primeiro).

## Descarte

`Descarte(item_id: str, categoria: Categoria, motivo: str, timestamp: str)` — todo descarte
gera um registro (C3); a ausência de registro para um item removido é, por definição, bug, não
comportamento esperado do gestor.

## Orcamento

`Orcamento(limite_total: int, margem_compactacao: int)` — `margem_compactacao` é a distância do
limite em que o gatilho de compactação (C4) é acionado; um valor igual a zero equivaleria a
acionar compactação só no próprio limite, contrariando C4, e é rejeitado na configuração.

## JanelaMontada

`JanelaMontada(itens: tuple[ItemDeContexto, ...], descartes: tuple[Descarte, ...],
tokens_usados: int)` — `tokens_usados` nunca excede `Orcamento.limite_total`; essa invariante é
verificada a cada montagem, não confiada silenciosamente ao processo de adição.

## Por que `Descarte` não referencia `Orcamento` diretamente

Um registro de descarte é válido e completo sem precisar apontar de volta para a configuração de
orçamento que o motivou — isso mantém o registro portável entre diferentes configurações de
orçamento ao longo do tempo (se o limite mudar, registros antigos continuam interpretáveis sem
precisar de uma versão histórica de `Orcamento` para dar sentido a eles).
