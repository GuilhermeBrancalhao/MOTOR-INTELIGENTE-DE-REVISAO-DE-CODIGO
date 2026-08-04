---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_ordenacao_respeita_dependencia_real` e `test_ciclo_de_dependencia_e_detectado` provam Z1
nos dois sentidos.

`test_estimativa_sem_incerteza_e_rejeitada` prova Z2: a mutação alvo é aceitar
`estimativa_min_dias` igual a `estimativa_max_dias`.

`test_plano_sem_escopo_negociado_e_rejeitado` prova Z3: a mutação alvo é aceitar `PlanoDeCiclo`
sem escopo declarado.

`test_revisao_de_plano_sem_motivo_e_rejeitada` prova Z4: a mutação alvo é aceitar
`RevisaoDePlano` sem motivo.

`test_bloqueio_sem_motivo_e_rejeitado` prova Z5: a mutação alvo é aceitar bloqueio sem motivo
explícito, tornando `BLOQUEADA` indistinguível de um estado arbitrário.

`test_conclusao_sem_atingir_criterio_e_rejeitada` prova Z6: a mutação alvo é aceitar conclusão
sem confirmação de que o critério de pronto foi atingido.


Nenhum teste depende de sistema de gestão de projeto real nem de ferramenta externa de
planejamento — todos operam sobre estruturas de dado Python puras, suficientes para provar as
seis regras de governança de planejamento sem qualquer custo de integração externa.

Essa escolha de projeto mantém a suíte determinística e rápida, seguindo a mesma filosofia de teste já estabelecida pelos demais volumes de processo deste acervo inteiro.

Isso garante execução previsível independente do ambiente, sem exigir nenhuma configuração
adicional de infraestrutura de planejamento real, seja localmente ou em qualquer pipeline
automatizado que rode a suíte completa deste acervo de forma recorrente e sem intervenção manual de qualquer tipo, mantendo o tempo total de execução na casa dos
milissegundos mesmo cobrindo todas as seis regras deste volume de ponta a ponta.