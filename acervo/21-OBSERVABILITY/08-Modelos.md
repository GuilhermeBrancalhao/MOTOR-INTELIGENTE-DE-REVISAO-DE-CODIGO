---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Modelos

## Sinal

`Sinal(categoria: CategoriaSinal, valor: float, timestamp: datetime, origem: str)` —
`CategoriaSinal` é um dos três ramos de `05-Diagramas.md`: `MotivoEncerramento`,
`IntervencaoHumana`, `CustoLatenciaPorEtapa`. `origem` identifica qual volume/motor produziu o
sinal (`08-AGENT-ENGINE`, `10-WORKFLOW` etc.) — essencial para que o agregador consiga decompor
por domínio, não só ver um fluxo indiferenciado de números.

## Limiar

`Limiar(sinal_categoria: CategoriaSinal, valor_critico: float, calibrado_em: date,
base_observacao: str)` — `base_observacao` registra de onde o valor crítico veio (por exemplo,
"p95 observado em 30 dias de produção") — um limiar sem essa proveniência não pode ser
reavaliado com confiança quando o comportamento do sistema mudar.

## Alerta

`Alerta(sinal: Sinal, limiar: Limiar, notificado_em: datetime | None)` — `notificado_em` sendo
`None` depois que o sinal cruzou o limiar é a condição de falha que `07-Regras.md` trata como
crítica: sinal detectado sem notificação confirmada.

## Decomposição de custo

`CustoDecomposto(etapa_id: str, tipo: TipoEtapa, tempo_s: float, tokens: int | None)` — `tokens`
é `None` para `TipoEtapa.Deterministico`, porque esse tipo de etapa não consome tokens de modelo
por definição; a ausência do campo é estrutural, não um dado faltante por falha de
instrumentação. O agregador que consome esta estrutura nunca trata `None` como zero na soma de
tokens — trata como "não aplicável", distinção que evita que uma etapa determinística barata
pareça artificialmente mais eficiente que uma etapa de IA só porque a primeira nunca tinha o
campo para começar.
