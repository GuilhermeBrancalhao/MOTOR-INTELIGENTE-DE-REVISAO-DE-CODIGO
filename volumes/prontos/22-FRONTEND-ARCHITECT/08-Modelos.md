---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`EstadoCarregamento` é um enum com cinco valores: OCIOSO, CARREGANDO, ERRO, CANCELADO, CONCLUIDO
— cada transição entre eles corresponde a exatamente um método de `RequisicaoDeIA`, e o enum
existe justamente para que o estado de uma requisição nunca seja representado por uma combinação
ambígua de booleanos (`carregando` e `com_erro` ao mesmo tempo, por exemplo, que um enum torna
impossível por construção).

`RequisicaoDeIA` carrega `fragmentos` como lista, não como string acumulada diretamente — isso
preserva a ordem de chegada de cada pedaço da resposta, útil para depuração e para qualquer
lógica futura que precise processar fragmento a fragmento em vez de apenas o texto concatenado
final.

`ResultadoExibido` é imutável e carrega `texto` junto de `e_fallback`, nunca separadamente — a
decisão de design é que não deveria ser possível, no tipo, expressar "aqui está o texto" sem
também expressar "e aqui está se ele é fresco ou não", tornando F3 uma garantia do tipo, não uma
convenção que depende de lembrar de checar os dois campos.


`PromocaoNaoAutorizada` e `RequisicaoJaFinalizada` são exceções distintas, não uma exceção
genérica compartilhada — cada uma corresponde a uma violação de regra específica (F4 e a
disciplina de transição de estado, respectivamente), e mantê-las separadas permite que quem
consome a API do exemplo trate cada caso de forma diferente, em vez de precisar inspecionar a
mensagem de uma exceção genérica para saber o que de fato aconteceu.