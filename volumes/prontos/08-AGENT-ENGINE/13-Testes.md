---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Testar este motor exige isolar o modelo de linguagem: a suíte não deve depender de um modelo
real respondendo de forma determinística, porque a garantia que importa é o comportamento do
motor diante de qualquer resposta do modelo, incluindo respostas inválidas ou inesperadas — não
a qualidade da resposta em si. A técnica é um modelo fake que devolve uma sequência de ações
programada, permitindo simular qualquer caso (sucesso imediato, erro seguido de retry, resposta
malformada) sem custo nem variabilidade de um modelo real.

## O que a suíte precisa cobrir

Cada transição do `stateDiagram-v2` em `06-Fluxogramas.md` precisa de pelo menos um teste que a
alcance: encerramento por objetivo, por cada uma das três dimensões de orçamento
independentemente (um teste que zera só passos, outro só tokens, outro só tempo — não um teste
único que zera os três, que não provaria que cada dimensão é verificada de forma independente),
e por erro não recuperável. A prova de que o guardião de orçamento é consultado antes da chamada
ao modelo, não depois, precisa de um teste que conta quantas vezes o modelo fake foi chamado
quando o orçamento já chega zerado — a contagem esperada é zero.

## Prova por mutação

Um teste forte para a regra "erro de ferramenta nunca aborta o loop silenciosamente" é um que
falha se alguém remover a captura de exceção do despachante de ferramenta — não um teste que só
confirma que uma ferramenta bem-sucedida funciona. Mutar o despachante para deixar a exceção
subir sem captura, e confirmar que o teste correspondente passa a falhar, é a forma de provar que
o teste está de fato ancorado na regra, e não só documentando o caminho feliz.

## Testes de integração com volumes vizinhos

Como este motor consome modelo (via `27-LLM-ROUTER`) e é consumido por `09-ORCHESTRATOR`, testes
de integração relevantes verificam o contrato nas duas pontas: que o motor aceita qualquer
implementação de "chamar modelo" que respeite a interface (não amarrado a um provedor específico
por acidente de implementação), e que o resultado devolvido a `09` contém informação suficiente
para uma decisão de coordenação (motivo de encerramento, não só sucesso/falha binário).
