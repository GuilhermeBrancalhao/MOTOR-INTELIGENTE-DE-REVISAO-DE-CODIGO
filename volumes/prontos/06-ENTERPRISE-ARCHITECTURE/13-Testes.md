---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este processo exige simular os dois pontos de decisão do fluxograma (`06-Fluxogramas`)
explicitamente: quando uma decisão técnica cruza para portfólio, e quando concentração ou
duplicação de fato dispara achado — não só o caminho onde tudo é decisão de projeto isolada.

## O que a suíte precisa cobrir

Registro obrigatório: um teste que tenta criar `Sistema` sem fornecedor ou fonte de dado e
verifica rejeição (E1). Concentração: um teste com três sistemas no mesmo fornecedor verificando
que o terceiro dispara sinalização, mas o segundo não (o limiar é testado no ponto exato).
Duplicação: um teste com dois sistemas de mesma categoria de capacidade, sem relação declarada
entre si, verificando detecção. Custo agregado: um teste que soma custo de múltiplos sistemas do
mesmo fornecedor e confirma que o total reflete a soma, não a média nem o maior isolado.

## Prova por mutação

Um teste forte para E3 é um que falha se `custo_total_agregado` for trocado por um cálculo que
retorna só o maior custo individual em vez da soma — mutação que esconderia exatamente a
concentração de custo que a regra existe para revelar.

## Testes de integração com volumes vizinhos

Um teste de integração relevante verifica que uma dependência sinalizada como cruzando fronteira
de dado sensível de fato gera o sinal que `30-AI-GOVERNANCE` consumiria, mesmo que este volume
não implemente a política de resposta — só garante que o sinal chega correto.
