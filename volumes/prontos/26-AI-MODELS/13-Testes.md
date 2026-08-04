---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_modelo_nao_avaliado_nao_pode_ser_aprovado` prova M2: a mutação alvo é `aprovado()` retornar
`False` silenciosamente em vez de levantar exceção quando não há avaliação.

`test_modelo_avaliado_abaixo_do_limiar_e_reprovado` e
`test_modelo_avaliado_acima_do_limiar_e_aprovado` provam M2 nos dois sentidos.

`test_modelo_que_nao_atende_requisito_e_reprovado_mesmo_com_boa_avaliacao` prova M1: um candidato
com ótima avaliação, mas que não atende o requisito de capacidade, ainda é reprovado.

`test_plano_sem_fallback_e_rejeitado` prova M3: a mutação alvo é aceitar `PlanoDeTarefa` sem
fallback.

`test_comparacao_de_custo_favorece_menor_custo_total_nao_menor_preco_unitario` prova M4: monta um
cenário onde o modelo com preço unitário maior tem custo total menor, e confirma que a comparação
segue o total, não o preço isolado.

`test_toda_troca_fica_registrada_no_historico` prova M6: confirma que `registrar_troca` adiciona
uma entrada completa (data, motivo, avaliação) ao histórico.


Nenhum teste depende de chamada real a um provedor de modelo — todos operam sobre valores
fornecidos diretamente nos próprios testes, o que mantém a suíte rápida, determinística, e livre
de qualquer acoplamento a preço ou comportamento real de um fornecedor específico no momento em
que os testes são escritos.

`test_comparacao_de_custo_favorece_menor_custo_total_nao_menor_preco_unitario` inclui uma
asserção intermediária que confirma o cenário antes de testar a função em si — garantindo que o
teste não passaria por acidente caso os números do cenário estivessem invertidos.

Essa asserção intermediária é, ela mesma, parte da prova, não apenas apoio de depuração.