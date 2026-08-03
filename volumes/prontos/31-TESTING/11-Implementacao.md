---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/31-testing/rastreabilidade.py -->

`rastreabilidade.py`, citado acima, torna a prática deste volume verificável: dada a lista de
invariantes e a lista de nomes de teste, quais regras ficaram sem proteção, e quais testes de
regressão nunca foram vistos falhar. A regra de nomeação vira um predicado — `test_guarda_2` não
casa com nenhuma regra, e essa impossibilidade é o argumento.

Os princípios também estão em prática nas seções `13-Testes.md` de `08-AGENT-ENGINE`,
`09-ORCHESTRATOR`, `10-WORKFLOW`, `17-SECURITY` e `21-OBSERVABILITY`.

## Como o padrão aparece nos volumes essenciais

Cada um desses volumes descreve, na sua seção `13-Testes.md`, pelo menos um teste que só se
justifica por sobreviver a uma mutação específica da regra que protege — por exemplo, o teste que
prova que o guardião de orçamento de `08-AGENT-ENGINE` é consultado antes da chamada ao modelo,
não depois, é provado contando quantas vezes o modelo fake foi chamado quando o orçamento já
zerado: um teste que só confirmasse "o motor encerra quando o orçamento acaba" não distinguiria
entre as duas ordens possíveis, e é essa distinção que a prova por mutação exige verificar
explicitamente.

## Ordem de aplicação recomendada num sistema novo

Primeiro, listar as invariantes do sistema (o que nunca pode acontecer, o que sempre precisa
acontecer) — normalmente já documentadas na seção `07-Regras.md` de cada volume de domínio.
Segundo, escrever um teste por invariante, nomeado pela violação que previne. Terceiro, mutar o
código de propósito para cada invariante e confirmar a falha correspondente. Quarto, só depois
de completar esse ciclo para os componentes individuais, escrever o teste de fluxo completo que
exercita a composição na ordem real de uso.

## Onde a integração com outros volumes acontece

A execução contínua desses testes no pipeline é `18-DEVSECOPS`; o indicador agregado de quanto
da suíte segue esse padrão (versus quanto é só caminho feliz não provado) é `32-QUALITY`.
