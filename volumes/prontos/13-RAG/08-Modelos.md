---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## Candidato

`Candidato(id_documento: str, score_proximidade: float, score_relevancia: float | None)` —
`score_relevancia` é `None` até passar pela reordenação (R3); os dois scores nunca são
confundidos, porque medem coisas diferentes e um candidato pode ter proximidade alta e relevância
baixa para a pergunta específica.

## Citacao

`Citacao(id_documento: str, trecho: str, valido_no_momento_da_citacao: bool)` — o campo
`valido_no_momento_da_citacao` materializa R6: é reavaliado a cada consulta, nunca herdado do
momento em que o documento foi indexado.

## RespostaComFidelidade

`RespostaComFidelidade(texto: str, citacoes: tuple[Citacao, ...], fidelidade: float,
recusada: bool, motivo_recusa: str | None)` — `recusada` cobre tanto R4 (sem fonte suficiente)
quanto o caso de fidelidade insuficiente medida depois da geração; `motivo_recusa` distingue os
dois casos, para que a causa da recusa nunca fique ambígua para quem consome a resposta.

## Fidelidade

Valor entre 0 e 1, calculado como proporção de afirmações extraídas da resposta que rastreiam a
alguma citação presente. Um valor de 1.0 significa que toda afirmação tem suporte; um valor
menor sinaliza extrapolação — conteúdo gerado além do que as fontes citadas de fato sustentam.

## Por que `RespostaComFidelidade` carrega os dois campos de recusa juntos

`recusada` e `motivo_recusa` vivem na mesma estrutura que `texto` e `citacoes`, mesmo que uma
resposta recusada tenha `texto` vazio — a alternativa (uma estrutura separada só para recusa)
forçaria quem consome a resposta a checar dois tipos diferentes dependendo do resultado, o que é
mais frágil do que checar um único campo booleano na mesma estrutura.
