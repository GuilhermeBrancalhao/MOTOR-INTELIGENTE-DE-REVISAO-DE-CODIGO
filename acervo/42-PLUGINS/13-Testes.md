---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_ativar_plugin_com_contrato_incompativel_e_rejeitado` e
`test_ativar_plugin_com_contrato_compativel_funciona` provam AD1 nos dois sentidos.

`test_hook_que_lanca_excecao_e_isolado_do_host` e
`test_hook_que_funciona_normalmente_retorna_resultado_de_sucesso` provam AD2 nos dois sentidos —
o primeiro é o teste mais importante do volume, porque prova diretamente que uma falha de
terceiro nunca escapa da fronteira de isolamento.

`test_acessar_capacidade_nao_declarada_e_rejeitado` e
`test_acessar_capacidade_declarada_funciona` provam AD3 nos dois sentidos.

`test_declaracao_sem_ponto_de_entrada_e_rejeitada` prova AD4: a mutação alvo é aceitar
`DeclaracaoDePlugin` sem ponto de entrada.

`test_desativacao_remove_plugin_e_seus_recursos` prova AD5: a mutação alvo é deixar recurso
associado ao plugin sobrevivendo à desativação.

`test_evolucao_de_contrato_que_quebra_sem_bump_de_major_e_rejeitada` e as duas variantes
positivas provam AD6 nos dois sentidos, seguindo o mesmo padrão de prova já usado por AC1 em
`41-SDK`.

`test_desativar_plugin_nao_ativo_e_rejeitado` prova que a operação nunca falha silenciosamente
para um plugin que nunca foi ativado — a mutação alvo é aceitar desativação de um nome ausente em
`plugins_ativos` sem levantar exceção alguma, o que mascararia um erro real de quem está
operando o host.

Nenhum teste depende de sistema de isolamento de processo real nem de mecanismo de sandbox
externo — toda a suíte roda sobre estruturas de dado Python puras e captura de exceção simples,
mantendo o tempo de execução na casa dos milissegundos.

Os testes de AD1 e AD6 seguem deliberadamente a mesma estrutura de par positivo/negativo já usada
para AC1 em `41-SDK` — a repetição do padrão entre os dois volumes não é acidental, já que AD6
reaproveita literalmente o mesmo princípio de versionamento aplicado a um tipo diferente de
superfície pública.