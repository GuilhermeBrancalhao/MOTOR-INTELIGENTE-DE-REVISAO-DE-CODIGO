---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 11-Implementacao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Implementação

Este volume descreve o motor em nível de contrato e comportamento, não cita código executável
específico — nenhuma seção deste volume tem `<!-- exemplo: -->`, por decisão explícita do ciclo
atual (ver `16-Roadmap.md`): a prioridade de 2026-08-03 foi fechar prosa e diagramas para os 10
volumes essenciais primeiro; código de referência citável é trabalho de um ciclo seguinte, e
citar um exemplo fictício aqui seria inventar uma implementação que não existe, o que o próprio
`Convencoes.md` proíbe.

## Como um motor real implementaria este contrato

O executor de passo é uma função pura no sentido de que, dado o mesmo histórico e o mesmo
orçamento restante, produz a mesma chamada ao modelo — a variabilidade de resultado vem do
modelo, não do motor. Isso importa para teste: o executor de passo pode ser testado com um
modelo fake que devolve respostas fixas, sem precisar de um modelo real, porque o contrato do
motor (o que ele envia, o que ele espera) é independente da implementação do modelo.

O guardião de orçamento é o componente mais simples e o mais crítico de acertar primeiro — três
decrementos e três comparações, sem lógica condicional complexa. A ordem de implementação
recomendada é: guardião de orçamento primeiro, com testes que provam que ele nunca deixa uma
dimensão ficar negativa; despachante de ferramenta segundo, com captura de exceção garantida;
executor de passo terceiro, integrando os dois anteriores; registrador de trilha por último,
porque ele observa os outros três sem afetar seu comportamento.

## Onde a integração com outros volumes acontece

A seleção de modelo (`27-LLM-ROUTER`) e a compilação do prompt (`28-PROMPT-COMPILER`) acontecem
antes da chamada que este motor faz ao modelo — do ponto de vista deste volume, "chamar o
modelo" é uma interface única, e o que está atrás dela (qual modelo, como o prompt foi montado)
é responsabilidade de outros volumes.
