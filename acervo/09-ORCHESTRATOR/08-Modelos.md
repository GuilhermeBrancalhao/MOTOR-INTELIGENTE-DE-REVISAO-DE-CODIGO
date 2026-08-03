---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Modelos

## Nó

`No(id: str, dependencias: list[str], politica_falha: PoliticaFalha, executavel: Callable)` — o
`executavel` é a caixa-preta descrita em `03-Escopo.md`: recebe entrada (composta das saídas das
dependências) e devolve `Sucesso(saida: Any)` ou `Falha(motivo: str, recuperavel: bool)`.
`dependencias` é a lista de ids de outros nós no mesmo grafo — arestas do DAG, direcionadas do
nó atual para cada dependência.

## Política de falha

`PoliticaFalha` é uma união de três variantes: `AbortarDependentes` (falha propaga para todo nó
que depender, direta ou transitivamente, deste), `PularDependentes` (dependentes são marcados
`Abortado` mas ramos independentes continuam — equivalente a `AbortarDependentes` do ponto de
vista dos dependentes diretos, mas o grafo inteiro não é abortado), `RetryComBackoff(tentativas:
int, backoff_inicial_s: float, fator: float)`. O campo `fator` multiplica o intervalo de espera a
cada nova tentativa (backoff exponencial) — com `backoff_inicial_s=2` e `fator=2`, os intervalos
entre tentativas são 2s, 4s, 8s, crescendo até o número de `tentativas` se esgotar.

## Grafo

`Grafo(nos: dict[str, No])` — a estrutura submetida pelo chamador. `validar()` devolve lista de
erros (ciclo detectado, dependência referenciando id inexistente) ou lista vazia se válido;
`ordem_topologica()` só é chamado depois de `validar()` devolver lista vazia.

## Resultado do grafo

`ResultadoGrafo(status_por_no: dict[str, StatusNo])` — `StatusNo` é o enum de estados finais
(`Sucesso`, `FalhaDefinitiva`, `Abortado`) descrito em `06-Fluxogramas.md`. Não existe campo de
"sucesso do grafo" agregado — quem consome o resultado decide, a partir do `status_por_no`, se o
resultado parcial é aceitável para o propósito da tarefa maior.
