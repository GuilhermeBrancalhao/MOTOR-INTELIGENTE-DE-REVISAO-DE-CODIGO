---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`Otimizador.buscar` recebe uma variante baseline, um gerador de candidatos, e usa
`avaliar_variante` — uma função injetada, não conhecida internamente — para pontuar cada candidato
contra `casos_de_ouro`, a mesma amostra fixa em toda a execução da busca. Nenhuma chamada a
`avaliar_variante` dentro de uma única busca usa amostra diferente da anterior.

O loop de busca respeita `max_tentativas` como limite superior rígido — a iteração para assim que
o orçamento é atingido, independente de o gerador de candidatos ainda ter mais para oferecer.

Toda avaliação, vencedora ou não, é registrada em `HistoricoDeBusca` antes de a próxima iteração
começar — não existe caminho que descarte um resultado sem registrá-lo primeiro.

`Otimizador` não expõe nenhum método de promoção — sua única saída é uma proposta (o melhor
resultado encontrado, se houver) e o histórico completo da busca. Transformar essa proposta em
versão promovida é uma operação que só existe do lado de fora deste volume, no fluxo do 07.


A assinatura de `buscar` recebe o gerador de candidatos como parâmetro, não como algo que o
`Otimizador` sabe produzir sozinho — essa separação mantém a estratégia de geração de variante
completamente desacoplada da lógica de avaliação e controle de busca, permitindo trocar como
candidatos são gerados sem tocar em nenhuma das seis regras deste volume.