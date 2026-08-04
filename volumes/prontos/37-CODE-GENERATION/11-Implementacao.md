---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/37-code-generation/geracao_de_codigo.py -->

`geracao_de_codigo.py`, citado acima, formaliza Y1-Y6: `aceitar_codigo_gerado` recusa código sem
validação (`ResultadoDeValidacaoAusente`) ou com validação que falhou (`ValidacaoFalhou`) (Y1);
`CodigoNaoMarcado` e `editar_codigo_gerado` garantem marcação e imutabilidade manual (Y2);
`gerar` depende exclusivamente da especificação e do gerador injetado, sem estado externo,
garantindo determinismo (Y3); `aceitar_codigo_gerado` também recusa código sem
`revisado_por_humano=True` (`RevisaoHumanaAusente`) (Y4); `EspecificacaoDeGeracao.__post_init__`
exige `versao` (Y5) e `escopo_declarado` (Y6) preenchidos.

`gerar` recebe o gerador como parâmetro `Callable` injetado, nunca uma dependência fixa
importada dentro da função — essa escolha mantém a lógica de geração testável com um gerador
sintético determinístico nos testes, sem exigir chamada real a um modelo de IA durante a
execução da suíte, e sem acoplar o módulo central a nenhum provedor específico.

Essa injeção de dependência também é o que possibilita trocar de provedor de geração no futuro sem reescrever nenhuma parte da lógica central de aceitação e validação.

Testes que usam um gerador sintético simples, como uma função lambda determinística, já são
suficientes para provar todas as seis regras sem qualquer custo de infraestrutura real associado
a chamar um provedor de IA de verdade durante a execução da suíte de testes automatizados, o
que mantém o tempo total de execução na casa dos milissegundos mesmo cobrindo tudo.