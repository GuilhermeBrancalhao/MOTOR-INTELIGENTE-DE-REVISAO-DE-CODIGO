---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_custo_sem_tarefa_e_rejeitado` e `test_custo_sem_escopo_e_rejeitado` provam U1 e U2: a
mutação alvo de cada um é aceitar `CustoDeTarefa` sem o respectivo campo preenchido.

`test_orcamento_estado_ok_alerta_estourado` prova U3: confirma os três estados distintos
retornados pelo mesmo orçamento sob três níveis crescentes de gasto.

`test_tendencia_exige_duas_medicoes` e `test_tendencia_detectada_entre_dois_periodos` provam U4
nos dois sentidos.

`test_otimizacao_de_custo_nao_validada_e_rejeitada` e
`test_otimizacao_de_custo_validada_e_aceita` provam U5 nos dois sentidos — a mutação alvo do
primeiro é aceitar mudança sem redução real de gasto medido.


Nenhum teste depende de integração real com provedor de IA nem de valor de custo real observado
em produção — todos os valores usados são sintéticos, escolhidos apenas para exercitar cada regra
de forma clara e isolada, sem introduzir dependência externa nenhuma na suíte.

Essa escolha de projeto mantém a suíte inteira determinística e rápida, seguindo a mesma filosofia já estabelecida pelos outros volumes de processo deste acervo.

Nenhuma parte da suíte depende de rede real nem de qualquer serviço externo provisionado, o que
garante execução previsível independente do ambiente onde os testes rodam, seja localmente ou em
qualquer pipeline de integração contínua, sem exigir configuração adicional de credencial ou
acesso a serviço externo algum para rodar com sucesso do início ao fim.