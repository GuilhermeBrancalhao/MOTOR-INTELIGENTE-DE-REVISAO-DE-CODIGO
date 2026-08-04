---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o método de selecionar modelo para uma tarefa: requisito de capacidade,
avaliação contra casos de ouro, fallback, comparação de custo por tarefa, e registro de troca.

**Fronteira com `27-LLM-ROUTER`.** Este volume decide quais modelos são candidatos válidos para
uma tarefa e sob qual critério; o 27 decide, em tempo de execução, para qual candidato específico
uma chamada é roteada. A lista de candidatos vem deste volume; a decisão de roteamento em si é
daquele.

**Fronteira com `07-PROMPT-ENGINE`.** Caso de ouro como mecanismo de avaliação é definido
naquele volume; este volume reaproveita o mesmo mecanismo para avaliar modelo, não prompt.

**Fronteira com `34-COST-OPTIMIZATION`.** Comparação de custo por tarefa, aqui, é sobre a decisão
de qual modelo usar; otimização de custo agregado ao longo do tempo, incluindo tendência e
alocação de orçamento, é daquele volume.

Como volume perecível, não cobre nome de modelo, preço ou limite específico como fato duradouro —
qualquer exemplo numérico é ilustração datada de método, nunca referência a ser reutilizada.


Essa fronteira entre seleção (aqui) e roteamento (27) existe porque as duas decisões têm ritmo
diferente: selecionar candidatos válidos é uma decisão relativamente estável, revisada em
semanas; rotear uma chamada específica entre candidatos já aprovados é uma decisão de tempo de
execução, potencialmente diferente a cada chamada. Misturar as duas dificultaria testar cada uma
isoladamente.