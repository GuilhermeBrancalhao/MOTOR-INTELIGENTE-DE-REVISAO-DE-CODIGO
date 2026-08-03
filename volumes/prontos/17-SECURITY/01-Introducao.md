---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-03
---

# Introdução

Um sistema que incorpora um modelo de linguagem herda uma classe de vulnerabilidade que sistemas
puramente determinísticos não têm: a fronteira entre "instrução do operador" e "dado processado"
pode desaparecer, porque o modelo lê ambos como texto. Um documento, e-mail ou página web que o
sistema processa como dado pode conter texto formulado para ser interpretado como instrução —
prompt injection — e se o sistema não distingue estruturalmente as duas origens, o modelo pode
executar a instrução injetada com a mesma autoridade que executaria uma instrução legítima do
operador.

Este volume trata de três categorias de risco específicas de sistemas com IA, e não de segurança
de software em geral (que tem literatura própria e não é o foco aqui): prompt injection (dado
processado sequestrando o comportamento pretendido), exfiltração de dados via ferramenta ou saída
do modelo (informação sensível sendo enviada para fora do sistema através de uma chamada de
ferramenta ou embutida numa resposta aparentemente inócua), e sandboxing de execução (quando o
sistema permite que o modelo gere e execute código ou comando, o ambiente de execução precisa
conter o dano de uma geração maliciosa ou simplesmente errada).

O motor `ENGINE` deste próprio acervo (documentado em `README.md`, seção "A decisão de projeto
que mais importa") é um caso real e observado destas três categorias: seu classificador de risco
nasceu como lista de proibições e foi contornado doze vezes em sete rodadas de revisão
adversarial, até o default ser invertido — comando de shell nunca é "livre" (executa sem
verificação), sempre trava ou é rastreado. Esse histórico concreto orienta a matriz de controles
deste volume em `07-Regras.md`, generalizado para qualquer sistema com a mesma classe de risco.
