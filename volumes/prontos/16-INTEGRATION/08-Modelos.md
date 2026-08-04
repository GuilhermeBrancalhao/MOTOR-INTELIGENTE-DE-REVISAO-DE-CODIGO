---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## VersaoContrato

`VersaoContrato(major: int, minor: int)` — mudança incompatível incrementa `major`; mudança
compatível (campo novo opcional, por exemplo) incrementa `minor`. Um consumidor declara a
`major` mínima esperada; qualquer resposta com `major` diferente é incompatibilidade (I1).

## ChamadaIdempotente

`ChamadaIdempotente(chave: str, operacao: str, resultado_cache: dict | None)` — `chave` é única
por operação lógica (não por tentativa de rede); duas chamadas com a mesma `chave` são a mesma
operação, mesmo que a segunda seja um retry da primeira.

## PoliticaDeRetry

`PoliticaDeRetry(timeout_s: float, max_tentativas: int, backoff_inicial_s: float)` — os três
campos são obrigatórios por integração (I3); não há valor padrão implícito aplicado quando
algum campo está ausente — a ausência é erro de configuração, não motivo para assumir um padrão.

## CircuitBreaker

`CircuitBreaker(estado: EstadoCircuito, falhas_consecutivas: int, limiar_abertura: int,
tempo_espera_s: float)` — `EstadoCircuito` é `FECHADO`, `ABERTO`, `MEIO_ABERTO` (testando
recuperação), com as transições descritas em `05-Diagramas.md`.

## RespostaVerificada

`RespostaVerificada(dados: dict, versao: VersaoContrato, compativel: bool)` — `compativel` é
calculado contra a versão mínima esperada pelo consumidor, nunca assumido verdadeiro por padrão.

## Por que `CircuitBreaker` não é compartilhado entre integrações diferentes

Cada integração externa tem seu próprio `CircuitBreaker`, nunca um único circuito compartilhado
entre múltiplos sistemas externos distintos. Se um único circuito cobrisse várias integrações,
falha de uma delas abriria o circuito para todas, mesmo que as outras estivessem funcionando
normalmente — o isolamento de falha (I4) precisa ser por integração específica, não agregado.
