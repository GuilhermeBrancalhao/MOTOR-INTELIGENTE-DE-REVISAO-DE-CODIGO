---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_gate_ignora_cobertura_de_linha_alta_com_mutacao_baixa` prova H1: a mutação alvo é o gate
considerar `cobertura_de_linha` na decisão, mascarando taxa de prova baixa.

`test_gate_bloqueia_taxa_abaixo_do_limiar` e `test_gate_com_excecao_permite_passagem` provam H2
nos dois sentidos.

`test_item_de_divida_incompleto_e_rejeitado` prova H3: a mutação alvo é aceitar `ItemDeDivida`
com algum campo vazio.

`test_regressao_exige_pelo_menos_duas_medicoes` prova H4: confirma `None` com histórico de uma
medição só.

`test_regressao_detectada_entre_duas_medicoes` e `test_sem_regressao_quando_taxa_mantem_ou_sobe`
provam H5 nos dois sentidos.

`test_medicao_expoe_submetricas_nomeadas` prova H6: confirma que `Medicao` carrega os três campos
separadamente, nunca um único valor agregado sem decomposição possível.


Nenhum teste depende de rodar mutação real sobre código de produção — todos constroem `Medicao`
diretamente com os números que representam o cenário sendo testado, o que isola a lógica de
decisão (gate, regressão, dívida) do processo, potencialmente caro, de gerar essas medições de
verdade em um sistema real.

Essa escolha de design deliberada mantém a suíte inteira rodando em milissegundos, mesmo cobrindo as seis regras de forma exaustiva e sem margem para instabilidade externa.

Rodar a suíte inteira continua sendo praticamente instantâneo mesmo à medida que novos casos de
teste forem adicionados no futuro, o que reduz o atrito de manter a cobertura crescendo junto do
próprio código deste volume ao longo do tempo.