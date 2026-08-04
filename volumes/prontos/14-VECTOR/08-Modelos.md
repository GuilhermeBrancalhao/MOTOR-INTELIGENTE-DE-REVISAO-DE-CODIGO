---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## Vetor

`Vetor(id_documento: str, valores: tuple[float, ...], versao_modelo: str, particao: str)` — a
`versao_modelo` é obrigatória e nunca inferida do contexto; dois vetores só são comparáveis se
`versao_modelo` for idêntica entre eles (V1).

## Consulta

`Consulta(vetor_busca: tuple[float, ...], metrica: Metrica, particao: str, versao_modelo: str,
limite: int)` — os quatro primeiros campos são obrigatórios; uma consulta que omite qualquer um
deles é rejeitada antes de qualquer comparação (V2, V3).

## Metrica

`Metrica`: `COSSENO`, `PRODUTO_ESCALAR`, `EUCLIDIANA` — enum fechado, porque métrica ad-hoc
declarada como string livre abriria espaço para erro de digitação silencioso que nenhuma
validação capturaria.

## ResultadoBusca

`ResultadoBusca(id_documento: str, score: float, particao: str)` — o `score` é interpretável
apenas dentro da mesma métrica que gerou a consulta; comparar `score` de consultas com métricas
diferentes não tem significado, mesmo que os números pareçam comparáveis numericamente.

## Exclusão

`conjunto_excluidos: set[str]` — mantido separado do índice físico, consultado antes de devolver
qualquer resultado (V6). A separação existe precisamente para que a garantia de exclusão não
dependa da velocidade de compactação física do índice.

## Por que `ResultadoBusca` carrega `particao`

Mesmo que uma consulta já declare a partição esperada, o resultado repete esse campo — não por
redundância inútil, mas porque um consumidor que agrega resultados de múltiplas consultas
(por exemplo, buscando em duas partições separadamente e combinando depois) precisa saber de qual
partição cada resultado individual veio, sem depender de lembrar qual consulta gerou qual lista.
