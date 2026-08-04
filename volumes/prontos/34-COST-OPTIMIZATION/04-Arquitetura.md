---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`CustoDeTarefa.__post_init__` recusa registro sem `tarefa` ou sem `escopo` preenchidos — custo
sem contexto de qual trabalho o gerou, ou sem dono atribuído, nunca entra no registro.

`OrcamentoDeEscopo` carrega `limiar_de_alerta` como fração entre 0 e 1, validado no momento da
construção — `verificar_orcamento` usa esse limiar para retornar um de três estados (OK, ALERTA,
ESTOURADO) contra o gasto atual, nunca um booleano binário que esconderia a diferença entre "ainda
folga" e "próximo do limite".

`detectar_tendencia_de_custo` exige pelo menos dois períodos no histórico antes de produzir
qualquer resultado — a mesma disciplina de H4 (`32-QUALITY`) e J4 (`33-PERFORMANCE`) aplicada
aqui: tendência nunca é julgada por uma medição isolada.

`validar_otimizacao_de_custo` recusa uma mudança proposta como redução de custo se o gasto medido
depois não for de fato menor que o gasto medido antes — nenhuma suposição substitui a comparação
numérica real.


Nenhum desses quatro componentes conhece preço de provedor específico — todos operam sobre
valores fornecidos como parâmetro, o que mantém o modelo central neutro a qualquer tabela de
custo real, consistente com a regra de volume perecível deste grupo.

Essa neutralidade a preço real é verificável por leitura direta do código, não apenas prometida em texto separado do que o módulo de fato implementa.