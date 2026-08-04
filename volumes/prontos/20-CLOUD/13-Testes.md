---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_recurso_sem_dono_e_rejeitado` prova N3: a mutação alvo é aceitar um `Recurso` construído
sem dono.

`test_segredo_inline_e_detectado` prova N5: a mutação alvo é aceitar uma configuração com chave
de segredo em texto plano.

`test_redundancia_ausente_e_reportada_para_alvo_critico` e
`test_redundancia_nao_exigida_para_alvo_sem_requisito` provam N2 nos dois sentidos — a falta é
sinalizada quando o alvo exige, e não é sinalizada como problema quando o alvo não exige.

`test_mudanca_fora_do_ambiente_e_rejeitada` prova N4: a mutação alvo é permitir que uma mudança
destinada a um ambiente seja aplicada a um recurso de ambiente diferente.

`test_drift_detectado_quando_recurso_ausente_do_real` e
`test_drift_detectado_quando_redundancia_diverge` provam N6 em dois cenários distintos de
divergência; `test_sem_drift_quando_declarado_bate_com_real` prova o caso negativo — nenhuma
divergência espúria quando os dois estados de fato coincidem.


Nenhum teste depende de um provedor de nuvem real — `PlanoDeInfraestrutura` e `detectar_drift`
operam inteiramente sobre estruturas em memória, o que torna a suíte determinística e capaz de
validar a lógica de decisão (redundância, isolamento, drift) sem custo nem instabilidade de rede
real.


`test_config_sem_segredo_passa` e `test_redundancia_nao_exigida_para_alvo_sem_requisito` cobrem
os casos negativos correspondentes a N5 e N2 — sem eles, a suíte provaria apenas que o sistema
sabe rejeitar o caso errado, não que ele aceita corretamente o caso certo, e um sistema que rejeita
tudo passaria os testes positivos sem de fato implementar a regra.