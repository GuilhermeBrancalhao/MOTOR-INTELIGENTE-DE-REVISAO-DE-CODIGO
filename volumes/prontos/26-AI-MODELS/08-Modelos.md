---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`RequisitoDeCapacidade`, `ResultadoDeAvaliacao`, `PlanoDeTarefa` e `RegistroDeTroca` são todos
imutáveis — cada um representa um fato específico de um momento (o que a tarefa exige, o
resultado de uma avaliação específica, o plano vigente, uma troca que aconteceu), e nenhum desses
fatos deveria ser alterado depois de registrado.

`CandidatoDeModelo.aprovado()` calcula a taxa de aprovação a partir de
`casos_de_ouro_aprovados / casos_de_ouro_total` no momento da chamada, em vez de armazenar um
booleano de aprovação pré-calculado — isso evita que o limiar de aprovação usado numa decisão
antiga (talvez diferente do limiar atual) fique congelado num campo que ninguém lembra de
recalcular quando o limiar muda.


Nenhum dos quatro tipos carrega um campo de preço fixo ou nome de modelo como valor padrão —
todos os campos relevantes (`preco_por_1k_entrada`, `modelo`, `data_avaliacao`) são obrigatórios,
fornecidos explicitamente a cada uso, nunca com um valor implícito que poderia envelhecer sem
ninguém perceber.

Essa ausência de valor padrão é uma escolha visível ao ler a assinatura de cada dataclass — quem
constrói `CustoPorTarefa`, por exemplo, precisa fornecer os dois preços explicitamente, nunca
herdando um valor implícito de uma execução anterior.

A obrigatoriedade é o mecanismo, não apenas a intenção documentada em prosa — o interpretador do
Python já recusa a construção antes de qualquer lógica de validação adicional entrar em jogo.