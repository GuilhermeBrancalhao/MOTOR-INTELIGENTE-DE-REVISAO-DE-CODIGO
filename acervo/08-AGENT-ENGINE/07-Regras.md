---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**Um passo produz exatamente uma ação.** O modelo nunca decide duas chamadas de ferramenta
simultâneas dentro do mesmo passo — se paralelismo é necessário, ele é responsabilidade de
`09-ORCHESTRATOR` coordenando múltiplas execuções, não deste motor tentando paralelizar dentro de
uma única execução. Essa restrição existe porque uma ação por passo é o que torna o histórico
linear e a trilha de auditoria não ambígua sobre a ordem causal dos eventos.

**O guardião de orçamento é consultado antes de qualquer decisão do modelo ser executada, nunca
depois.** Se o orçamento já foi excedido, o motor nem chama o modelo para decidir o próximo
passo — chamar e descartar a decisão desperdiçaria a dimensão de orçamento (tokens, tempo) que a
verificação existe para proteger.

**Erro de ferramenta nunca aborta o loop silenciosamente.** Toda observação de erro volta ao
histórico e é registrada na trilha, mesmo quando o motor decide, por regra de erro não
recuperável, encerrar em seguida — o encerramento é uma decisão explícita e auditável, não um
efeito colateral de uma exceção não tratada subindo pela pilha.

**As três dimensões de orçamento (passos, tokens, tempo) são independentes e nenhuma substitui
as outras.** Um motor que só limita passos permite uma ferramenta lenta consumir tempo
ilimitado; um motor que só limita tempo permite um loop de passos muito rápidos e muito
numerosos consumir tokens sem limite. As três precisam de limite próprio, verificado a cada
passo.

**Todo encerramento carrega motivo explícito** (objetivo, orçamento, erro) — nunca um booleano
genérico de "terminou". A trilha e o chamador dependem dessa distinção para decidir o que fazer
com o resultado: um resultado por orçamento excedido é parcial por definição e não deveria ser
tratado como equivalente a um resultado por objetivo atingido.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Guardião de orçamento roda antes de cada chamada ao modelo | Consumo ilimitado de tokens/tempo por loop sem parada | Teste que força orçamento zero e verifica que o modelo nunca é chamado |
| Erro de ferramenta sempre registrado antes de qualquer decisão de encerramento | Perda de trilha auditável em caminho de erro | Teste que injeta erro de ferramenta e verifica registro na trilha antes do encerramento |
| Uma ação por passo, validada contra o contrato | Ambiguidade de ordem causal na trilha; resposta de modelo fora do formato esperado sendo executada sem validação | Teste que envia resposta malformada do modelo e verifica rejeição antes de despachar qualquer ferramenta |
