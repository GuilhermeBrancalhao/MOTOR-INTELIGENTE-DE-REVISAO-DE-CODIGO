---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Modelos

`DeclaracaoDePlugin` exige `ponto_de_entrada` não vazio já em `__post_init__` — a mesma
disciplina de validação na criação já usada por outros modelos deste acervo, tornando uma
declaração sem ponto de entrada estruturalmente impossível de existir, não apenas
desencorajada por convenção de uso correto.

`ResultadoDeHook` é imutável e carrega tanto o caminho de sucesso quanto o de falha na mesma
estrutura — a escolha de um único tipo de retorno, em vez de levantar exceção diretamente, é o que
torna `executar_hook_isolado` capaz de garantir isolamento sem exigir que todo chamador precise
lidar com um bloco `try/except` próprio.

`EstadoDoHost` mantém `plugins_ativos` e `recursos_por_plugin` como dois dicionários indexados
pelo mesmo nome de plugin — a simetria entre as duas estruturas é o que permite `desativar`
remover as duas entradas relacionadas numa única operação coerente, sem risco de esquecer uma das
duas.

`VersaoDeContrato` usa apenas `major` e `minor`, sem campo `patch` — diferente de
`VersaoSemantica` em `41-SDK`, o contrato de extensão não precisa distinguir correção de patch de
adição de funcionalidade menor para os fins deste modelo, já que a única decisão que
`evoluir_contrato` precisa tomar é sobre o número maior.

`EstadoDoHost` não é imutável, diferente dos outros modelos deste volume — ele representa o
estado vivo e mutável do host em execução, e é exatamente por isso que `desativar` precisa
remover as duas entradas relacionadas de forma atômica dentro do mesmo método, em vez de depender
de reconstrução de um novo objeto imutável a cada mudança de estado.