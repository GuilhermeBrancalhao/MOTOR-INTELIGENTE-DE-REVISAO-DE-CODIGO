---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_melhoria_marginal_nao_supera_baseline` e `test_melhoria_significativa_supera_baseline`
provam O2 nos dois sentidos — o primeiro tem como mutação alvo tratar diferença de ruído como
melhoria real.

`test_busca_respeita_orcamento_maximo_de_tentativas` prova O4: a mutação alvo é continuar
avaliando candidatos além de `max_tentativas`.

`test_toda_tentativa_e_registrada_mesmo_rejeitada` prova O5: confirma que o histórico contém
tentativas rejeitadas, não apenas a proposta vencedora.

`test_mesma_amostra_usada_em_todas_as_avaliacoes` prova O1: captura a amostra passada em cada
chamada e confirma identidade entre todas.

`test_otimizador_nunca_promove_sozinho` prova O3: inspeciona os métodos públicos de `Otimizador`
e confirma ausência de qualquer método relacionado a promoção — a mutação alvo é a introdução de
um método desse tipo no futuro, e este teste falharia imediatamente se isso acontecesse.


`test_busca_respeita_orcamento_maximo_de_tentativas` verifica não apenas o número de chamadas,
mas especificamente que o candidato além do orçamento nunca aparece entre os nomes avaliados —
uma contagem correta por acidente (por exemplo, se um candidato fosse avaliado duas vezes e outro
nenhuma) não seria suficiente para provar a regra.

Esse nível de precisão na asserção é o que separa um teste que realmente prova a regra de um que apenas parece prová-la.

Um teste que apenas contasse o número de chamadas, sem verificar quais candidatos especificamente foram avaliados, poderia passar mesmo com um bug que pulasse um candidato válido e avaliasse outro duas vezes.