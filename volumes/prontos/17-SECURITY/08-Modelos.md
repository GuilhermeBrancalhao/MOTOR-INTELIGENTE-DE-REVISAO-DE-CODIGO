---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-03
---

# Modelos

## Classificação de risco de ação

`NivelRisco` é um enum de três valores: `Travado` (bloqueia e exige confirmação humana antes de
executar), `Rastreado` (executa, mas o evento entra em relatório auditável), `Livre` (executa sem
verificação adicional — reservado para ação comprovadamente inócua por construção, nunca por
suposição). A classificação é função da ação, não da intenção declarada de quem a solicitou —
duas solicitações com a mesma ação recebem a mesma classificação, independente de quem pediu.

## Origem do dado

`OrigemDado` distingue `Operador` (texto digitado diretamente pelo humano na sessão atual) de
`Processado` (qualquer outra origem: arquivo lido, resultado de busca, saída de ferramenta
anterior, conteúdo de mensagem recebida). Essa distinção é o que alimenta a regra de isolamento
de `07-Regras.md` — uma ação de risco decidida a partir de conteúdo com `OrigemDado.Processado`
exige confirmação explícita antes de `NivelRisco.Livre` ou `NivelRisco.Rastreado` serem
aplicados sem intervenção.

## Destino de chamada de ferramenta

`Destino(identificador: str, autorizado: bool)` — a lista de destinos autorizados é configurada
por sistema, não inferida da natureza aparente do dado enviado. Uma chamada para destino com
`autorizado=False` é sempre `Travado`, independente do conteúdo específico daquela chamada.

## Vetor de risco documentado

`VetorRisco(familia: str, exemplo_concreto: str, data_descoberta: date)` — o registro mínimo que
acompanha toda família de controle nova, análogo às famílias R1 a R12 do motor `ENGINE`. Sem os
três campos, um controle não tem contexto suficiente para ser reavaliado quando as condições do
sistema mudarem.
