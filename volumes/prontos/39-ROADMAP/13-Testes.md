---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_criterio_de_priorizacao_incompleto_e_rejeitado` prova AA1: a mutação alvo é aceitar
`CriterioDePriorizacao` com campo vazio.

`test_item_direcional_com_data_comprometida_e_rejeitado` e
`test_item_comprometido_com_data_e_aceito` provam AA5 nos dois sentidos.

`test_item_fora_de_escopo_sem_motivo_e_rejeitado` prova AA2: a mutação alvo é aceitar
`ItemForaDeEscopo` sem motivo.

`test_decisao_sem_autoridade_declarada_e_rejeitada` prova AA3: a mutação alvo é aceitar
`DecisaoQueExigeAutoridade` sem autoridade nomeada.

`test_revisao_com_atraso_sem_motivo_e_rejeitada` e
`test_revisao_sem_atraso_nao_exige_motivo` provam AA4 nos dois sentidos.

`test_dependencia_entre_ciclos_incompleta_e_rejeitada` prova AA6: a mutação alvo é aceitar
`DependenciaEntreCiclos` com qualquer campo vazio.


Nenhum teste depende de ferramenta de gestão de backlog real nem de sistema externo de rastreio
de item — todos operam sobre estruturas de dado Python puras, suficientes para provar as seis
regras de governança de roadmap sem qualquer custo de integração com infraestrutura externa.

Essa escolha de projeto mantém a suíte determinística e extremamente rápida, seguindo a mesma filosofia de teste já estabelecida pelos demais volumes de processo deste acervo.

Mesmo o teste que envolve revisão periódica evita qualquer dependência de tempo real, recebendo
a data como argumento explícito em vez de consultar o relógio do sistema durante a execução,
mantendo o resultado do teste completamente previsível entre diferentes execuções da suíte,
mesmo quando rodadas em máquinas diferentes ou em horários muito distantes entre si no calendário.