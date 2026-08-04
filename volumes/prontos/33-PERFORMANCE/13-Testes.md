---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_operacao_sem_slo_e_rejeitada` e `test_operacao_sem_estrategia_de_sobrecarga_e_rejeitada`
provam J1 e J4: a mutação alvo de cada um é aceitar a operação sem o respectivo campo declarado.

`test_medicao_com_concorrencia_baixa_e_rejeitada` prova J2: a mutação alvo é aceitar medição sob
carga artificialmente baixa como representativa.

`test_regressao_de_performance_detectada` e `test_sem_regressao_quando_p95_melhora` provam J3 nos
dois sentidos.

`test_otimizacao_nao_validada_e_rejeitada` e `test_otimizacao_validada_e_aceita` provam J5 nos
dois sentidos — a mutação alvo do primeiro é aceitar mudança sem melhoria mensurável.

`test_slo_de_ia_sem_margem_e_rejeitado` prova J6: a mutação alvo é aceitar SLO de operação com IA
sem margem entre percentis.


Nenhum teste depende de infraestrutura real de carga — todas as `MedicaoDeCarga` são construídas
diretamente com valores sintéticos que representam o cenário sendo testado, o que mantém a suíte
rápida e determinística mesmo cobrindo cenários de regressão e otimização que, em produção,
exigiriam ferramentas reais de teste de carga.

Essa escolha de design é consistente com a mesma filosofia já aplicada em outros volumes de processo deste acervo, como o 32-QUALITY.

Nenhuma parte da suíte depende de temporização real de rede nem de infraestrutura de carga de
fato provisionada em algum ambiente externo ao processo de teste, o que mantém a execução
completa na casa dos milissegundos mesmo cobrindo as seis regras de ponta a ponta.