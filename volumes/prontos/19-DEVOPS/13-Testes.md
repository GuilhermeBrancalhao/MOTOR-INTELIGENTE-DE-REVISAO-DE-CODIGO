---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_estagio_fora_de_ordem_e_rejeitado` prova P5: a mutação alvo é o pipeline aceitar um estágio
fora da posição esperada da sequência.

`test_estagio_que_falha_bloqueia_seguinte` prova P1/P5: a mutação alvo é permitir que um estágio
seguinte rode depois de o anterior ter falhado.

`test_pipeline_incompleto_nao_pode_implantar` prova P1: a mutação alvo é permitir deploy em
produção sem que todos os estágios anteriores tenham passado.

`test_deploy_completo_sem_justificativa_e_rejeitado` e
`test_deploy_gradual_e_aceito_por_padrao` provam P3 nos dois sentidos — o padrão aceita, a
exceção exige sinalização explícita.

`test_artefato_atual_rastreia_o_que_esta_em_producao` prova P4: consulta o histórico após
múltiplos deploys e confirma que a resposta é sempre o último, sem ambiguidade.

`test_reverter_sem_versao_anterior_falha` e `test_reverter_restaura_artefato_anterior` provam P2
nos dois sentidos: falha explícita quando não há para onde reverter, sucesso restaurando o
artefato correto quando há.

`test_artefato_do_pipeline_e_imutavel` prova P6: tenta reatribuir o artefato de um `Pipeline` já
construído e confirma que a estrutura do dataclass congelado rejeita a operação — a paridade entre
staging e produção não depende de disciplina, é impossível de violar pela própria forma do tipo.


Nenhum teste depende de infraestrutura real ou de tempo de execução de rede — `Pipeline` e
`GerenciadorDeploy` operam inteiramente em memória, o que torna a suíte determinística e capaz de
rodar em milissegundos, sem mocks de sistema externo escondendo o comportamento real da lógica de
decisão que este volume formaliza.