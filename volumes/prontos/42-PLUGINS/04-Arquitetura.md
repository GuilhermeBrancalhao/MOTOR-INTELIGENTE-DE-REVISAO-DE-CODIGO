---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 04-Arquitetura
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Arquitetura

`ativar_plugin` recusa ativação quando a versão maior do contrato alvo da `DeclaracaoDePlugin`
diverge da versão maior do `ContratoDeExtensao` que o host de fato oferece — a incompatibilidade é
detectada antes de qualquer hook do plugin ser chamado, nunca descoberta como falha de execução em
produção.

`executar_hook_isolado` sempre envolve a chamada ao hook do plugin em captura de exceção,
retornando um `ResultadoDeHook` estruturado tanto no caminho de sucesso quanto no de falha — o
host nunca precisa de tratamento especial porque a função de execução já garante que nenhuma
exceção de plugin escapa para o chamador.

`acessar_capacidade` recusa qualquer capacidade que não conste em
`DeclaracaoDePlugin.capacidades_solicitadas` — a verificação consulta apenas o que foi declarado
na ativação, nunca um conjunto de permissão padrão amplo que precisaria ser restringido depois.

`EstadoDoHost.desativar` remove o plugin de `plugins_ativos` e seus recursos de
`recursos_por_plugin` na mesma operação — as duas remoções acontecem juntas, garantindo que
nenhum recurso alocado durante a ativação sobreviva à desativação como resíduo esquecido.

`evoluir_contrato` compara a versão maior do `ContratoDeExtensao` atual contra a proposta,
seguindo exatamente a mesma lógica já usada por `validar_release` em `41-SDK` — a reutilização
deliberada do mesmo padrão de verificação reforça que o contrato de extensão é, ele mesmo, uma
superfície pública sujeita à mesma disciplina de versionamento aplicada a qualquer outro elemento
exposto a consumidor externo do sistema.