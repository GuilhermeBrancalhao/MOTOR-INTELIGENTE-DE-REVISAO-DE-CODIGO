---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Este é um volume perecível (regra 9 de `00-INTRODUCAO/Convencoes.md`), como o `26-AI-MODELS` de
quem depende diretamente. O método de rotear descrito aqui não muda com a mesma velocidade que um
preço de fornecedor, mas ainda assim é mantido deliberadamente fino, sem número fixo além de
ilustração datada — o foco é o mecanismo de decisão em tempo de execução, não uma tabela de
custo, que é assunto do `34-COST-OPTIMIZATION`.

`26-AI-MODELS` decide quais modelos são candidatos válidos para uma tarefa, com avaliação e
fallback declarados. Este volume trata de uma decisão diferente e mais frequente: para uma
chamada específica, agora, qual desses candidatos já aprovados de fato recebe a chamada — o
principal, saudável, ou o fallback, quando o principal está degradado.

A distinção importa porque as duas decisões têm ritmo diferente: seleção de candidato (26) é
revisada em semanas; roteamento (aqui) acontece a cada chamada, potencialmente reagindo a sinal
de saúde que muda em segundos. Router que reage rápido demais a uma única falha isolada, ou que
troca de candidato repetidamente sem estabilidade, causa mais instabilidade do que resolve.

A mesma regra de perecibilidade que governa o `26-AI-MODELS` vale aqui: o gate estrutural exige
piso de substância por seção independente de perecibilidade — o que muda é o que pode ser
afirmado como fato duradouro, não quanto texto é exigido para passar no gate.