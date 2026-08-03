---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-03
---

# Testes

Esta é a seção mais reflexiva do acervo: como se testa um volume sobre testar. A resposta é a
mesma disciplina aplicada recursivamente — cada afirmação deste volume sobre "como testar bem"
precisa, ela mesma, ser verificável, não apenas plausível.

## Como verificar que o processo descrito aqui funciona

Aplicar o processo de `11-Implementacao.md` (listar invariante, escrever teste nomeado pela
violação, provar por mutação, só então testar composição) a um componente real e observar se ele
de fato produz testes que falham quando deveriam. Se um teste escrito seguindo esse processo
ainda passa depois de uma mutação que deveria violá-lo, o processo não falhou — o passo de
mutação capturou exatamente o caso que deveria capturar, e o teste precisa ser revisto, não o
processo.

## O que prova que a distinção entre caminho feliz e regressão de regra é real

Um teste puramente de caminho feliz, mutado, tipicamente ainda passa em muitos casos —
justamente porque ele nunca afirmou proteger uma regra específica, só documentar comportamento.
Isso não é falha do teste; é a diferença de propósito entre os dois tipos, e um exercício de
mutação em toda a suíte de um volume revela concretamente quais testes são de qual categoria,
sem depender de julgamento subjetivo sobre a intenção original de cada teste.

## Auto-referência controlada

Este volume não cita a si mesmo como exemplo de teste provado por mutação, porque não tem código
executável — a prova de sua utilidade está em quão bem os outros seis volumes essenciais deste
ciclo, que citam este padrão explicitamente em suas próprias seções `13-Testes.md`, de fato
seguem a disciplina descrita aqui.
