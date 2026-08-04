---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`EspecificacaoDeGeracao` e `CodigoGerado` são tipos separados e imutáveis — a especificação
representa a intenção (o que deveria ser gerado); o código gerado representa o resultado. Manter
os dois como tipos distintos, em vez de um único objeto mutável, preserva a rastreabilidade entre
intenção e resultado mesmo quando várias gerações são tentadas para a mesma especificação.

`ResultadoDeValidacao` carrega `compilou` e `testes_passaram` como campos separados, não um
booleano único de "válido" — a distinção importa porque as duas falhas têm causas e correções
diferentes: um erro de compilação é sintático; um teste falho pode compilar perfeitamente e ainda
estar semanticamente errado.

`CodigoGerado.revisado_por_humano` é um campo explícito no próprio tipo, não inferido de outro
sistema — a revisão precisa estar registrada diretamente no objeto que representa o código, para
que `aceitar_codigo_gerado` consiga verificar sua presença sem depender de consulta externa.


A separação entre `EspecificacaoDeGeracao` (intenção) e `CodigoGerado` (resultado) preserva
rastreabilidade mesmo quando múltiplas tentativas de geração acontecem para a mesma
especificação — cada resultado carrega sua própria referência à especificação que o produziu,
nunca compartilhando identidade com o resultado de uma tentativa anterior ou posterior.

Essa preservação de identidade separada entre tentativas é o que permite, mais tarde, comparar diferentes gerações da mesma especificação sem confundir qual produziu qual resultado específico.