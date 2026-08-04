---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/29-prompt-optimizer/otimizador.py -->

`otimizador.py`, citado acima, formaliza O1-O6: `avaliar_variante` é sempre chamada com o mesmo
`casos_de_ouro` para baseline e para cada candidato dentro de uma execução de `buscar` (O1);
apenas candidatos cuja `taxa_acerto` supera o baseline por mais que `limiar_melhoria_minima`
tornam-se proposta (O2); `Otimizador` não expõe nenhum método de nome relacionado a promoção —
verificado por inspeção da lista de métodos públicos da classe (O3); o loop de `buscar` para
assim que `max_tentativas` é atingido, mesmo com candidatos restantes no gerador (O4); todo
`ResultadoDeAvaliacao`, aprovado ou não, é acrescentado a `HistoricoDeBusca` antes da próxima
iteração (O5); `avaliar_variante` é uma função totalmente externa ao `Otimizador`, que nunca
modifica `casos_de_ouro` internamente (O6).

O comentário final em `buscar` — que nenhum método altera `casos_de_ouro` nem promove nada —
existe porque essas duas garantias não têm um teste dedicado por si só; elas são verificadas pela
ausência estrutural de qualquer caminho de código que faria essas coisas, não por uma checagem
em tempo de execução que poderia ser removida por engano.

Essa escolha reflete a mesma filosofia usada em R10 do 07-PROMPT-ENGINE: algumas garantias são melhor expressas pela ausência estrutural de um caminho de código do que por uma verificação explícita em tempo de execução.