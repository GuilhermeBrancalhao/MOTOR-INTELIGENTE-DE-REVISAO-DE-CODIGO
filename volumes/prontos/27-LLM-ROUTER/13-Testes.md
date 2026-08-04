---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_roteamento_para_candidato_nao_aprovado_e_rejeitado` prova L1: a mutação alvo é aceitar
roteamento para um candidato fora da lista aprovada.

`test_principal_saudavel_e_escolhido` cobre o caminho de sucesso normal.

`test_falha_unica_isolada_nao_aciona_fallback` prova L4: a mutação alvo é tratar uma única falha
como degradação suficiente, ignorando o tamanho mínimo de amostra.

`test_degradacao_sustentada_aciona_fallback` prova L2: a mutação alvo é manter roteamento no
principal mesmo com sinal degradado sustentado e amostra suficiente.

`test_recuperacao_exige_janela_de_estabilidade` prova L5: confirma que sinais saudáveis
consecutivos abaixo da janela não retornam o roteamento ao principal, e que completar a janela
sim.

`test_toda_decisao_fica_registrada_no_historico` prova L3: confirma que cada chamada a `rotear`
adiciona uma entrada ao histórico com o motivo correspondente.

`test_estado_atual_e_consultavel` prova L6: confirma que `estado_de` reflete o candidato ativo
sem exigir nenhuma chamada adicional de roteamento.


Nenhum teste depende de sinal de saúde real observado em produção — todos constroem `SinalDeSaude`
diretamente com valores que representam o cenário sendo testado, o que torna cada mutação alvo
isolável sem depender de reproduzir condição real de rede ou provedor.

Essa escolha de design nos testes reflete a mesma filosofia da implementação: nenhuma parte deste volume depende de infraestrutura externa para ser verificada.

Isso mantém a suíte rápida e livre de qualquer dependência de rede ou de provedor real durante a execução.