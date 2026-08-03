---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Modelos

## Objetivo de execução

`Objetivo(descricao: str, criterio_de_sucesso: str | None)` — a descrição é o que vai para o
prompt do modelo; o critério de sucesso, quando presente, é usado pelo motor para decidir se uma
resposta final do modelo de fato conta como "objetivo atingido" ou deveria ser tratada como
insuficiente e devolvida ao loop — nem toda resposta final do modelo é aceita sem verificação.

## Orçamento

`Orcamento(passos_restantes: int, tokens_restantes: int, tempo_restante_s: float)` — as três
dimensões descritas em `07-Regras.md`, decrementadas a cada passo pelo guardião. Um orçamento
com qualquer dimensão em zero é inválido para iniciar uma nova execução — o motor rejeita antes
do primeiro passo, não deixa a execução começar para falhar no primeiro guardião.

## Passo

`Passo(numero: int, entrada_modelo: Historico, acao: Acao, observacao: Observacao | None,
timestamp: datetime)` — o registro atômico que a trilha grava por iteração do loop. `Acao` é uma
união de `ChamarFerramenta(nome: str, argumentos: dict)` ou `RespostaFinal(conteudo: str)`;
`Observacao` é uma união de `Sucesso(resultado: Any)` ou `Erro(mensagem: str,
recuperavel: bool)`.

## Resultado de execução

`ResultadoExecucao(motivo: MotivoEncerramento, passos: list[Passo], saida: str | None)` —
`MotivoEncerramento` é o enum de três valores (`OBJETIVO_ATINGIDO`, `ORCAMENTO_EXCEDIDO`,
`ERRO_NAO_RECUPERAVEL`) que `05-Diagramas.md` e `06-Fluxogramas.md` descrevem visualmente.
`saida` é `None` quando o motivo não é `OBJETIVO_ATINGIDO` — a ausência de valor é o sinal
estrutural de que o chamador não deveria tratar o resultado como completo.
