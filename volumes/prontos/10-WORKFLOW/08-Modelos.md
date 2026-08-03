---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-03
---

# Modelos

## Passo

`Passo(id: str, tipo: TipoPasso, formato_entrada: Schema, formato_saida: Schema,
correcao_automatica: bool)` — `TipoPasso` é `Deterministico` ou `IA`. `correcao_automatica`
só é relevante para passos `IA`; para `Deterministico` é ignorado, porque a saída de um passo
determinístico não passa por validação de formato além da checagem de sucesso da chamada em si.

## Workflow

`Workflow(id: str, passos: list[Passo], sequencia: Grafo)` — a `sequencia` reaproveita o mesmo
conceito de grafo de dependência descrito em `09-ORCHESTRATOR/08-Modelos.md`, porque um workflow
com ramificação condicional ou passos paralelos é, na sua forma mais geral, um DAG. Um workflow
puramente linear é um caso particular onde cada passo depende só do anterior.

## Checkpoint

`Checkpoint(workflow_id: str, passo_atual: str, estado_acumulado: dict, timestamp: datetime)` —
`estado_acumulado` contém toda saída de passo já concluído que passos futuros podem precisar
consumir. É esse dicionário, e não nenhuma variável local do processo em execução, que a
retomada usa para reconstruir o contexto necessário para continuar exatamente do `passo_atual`.
O campo `timestamp` não é decorativo — é o que permite calcular a métrica de tempo por passo
descrita em `14-Metricas.md`, e também o que permite detectar, na operação, um workflow que
ficou parado por tempo anormalmente longo num mesmo `passo_atual` sem produzir novo checkpoint.

## Espera

`EsperaSinal(tipo: TipoSinal, identificador: str)` — `TipoSinal` é `Aprovacao` ou `CallbackAssincrono`.
O `identificador` é o que permite ao gestor de sinal externo (descrito em `04-Arquitetura.md`)
casar um sinal recebido com o workflow específico que está esperando por ele, mesmo que múltiplos
workflows estejam simultaneamente em `AguardandoSinal` esperando sinais diferentes.
