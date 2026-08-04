---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`TipoDeDiagrama` carrega `nome`, `proposito` e `quando_usar` como campos obrigatórios, e
`__post_init__` recusa um `nome` fora do conjunto de tipos reconhecidos (`C4Context`,
`sequenceDiagram`, `stateDiagram-v2`, `flowchart`) — a materialização direta de X3, impedindo que
um tipo ad-hoc entre no catálogo sem passar pela mesma disciplina dos quatro já estabelecidos.

`EntradaDeCatalogo` recusa registro sem `prosa_explicativa` (X2) ou sem `fora_de_escopo` (X6) —
as duas exigências verificadas juntas na mesma operação, porque nenhuma sozinha torna um diagrama
confiável.

`VerificacaoDeVigenciaDoDiagrama` espelha `VerificacaoDeVigencia` do `35-DOCUMENTATION`
deliberadamente — o mesmo padrão de tipo, aplicado ao mesmo problema (algo que era verdade e pode
ter deixado de ser), mas escopado especificamente a diagrama.


`TipoDeDiagrama` e `EntradaDeCatalogo` são deliberadamente tipos separados — o primeiro
representa a categoria geral (o que `sequenceDiagram` é, de forma abstrata); o segundo representa
uma instância específica catalogada (este diagrama específico, deste volume específico, usando
aquele tipo). A separação evita misturar propósito genérico do tipo com escopo específico de uma
instância particular.

Essa distinção de responsabilidade entre os dois tipos mantém cada um simples de raciocinar isoladamente, sem misturar conceito abstrato com instância concreta no mesmo objeto.

Um sistema que precisasse relacionar as duas instâncias de forma mais rica poderia adicionar referência cruzada explícita entre elas, sem alterar a responsabilidade central de cada tipo isoladamente.