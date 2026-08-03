---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Identificar um vetor de prompt injection num fluxo concreto** — reconhecer quando dado
processado pelo sistema (documento, e-mail, resultado de busca) pode conter texto formulado
como instrução, e explicar por que tratar esse dado como texto plano indiferenciado da instrução
do operador é a causa raiz da vulnerabilidade, não um detalhe de implementação.

**Aplicar o princípio de inversão de default para ações de risco não enumerável.** Explicar por
que uma lista de proibições (blocklist) converge mal contra um adversário adaptativo — cada
lista fechada é uma lista de contornos conhecidos, não de todos os contornos possíveis — e por
que inverter o default (o que não é comprovadamente inócuo é auditado) resolve a classe de
problema, não só as instâncias já descobertas.

**Diferenciar exfiltração de dados por ferramenta de exfiltração por saída de texto.** A primeira
acontece quando uma chamada de ferramenta legítima é usada para enviar dado sensível para um
destino não autorizado; a segunda acontece quando a própria resposta do modelo embute a
informação de forma que passa despercebida por quem lê superficialmente.

**Desenhar sandboxing proporcional ao dano potencial de uma execução gerada por IA** — nem toda
geração de código precisa do mesmo nível de isolamento, mas subestimar o isolamento necessário
para código ou comando de shell é o erro mais caro e mais comum.

**Aplicar a matriz de controles de `07-Regras.md`** a um sistema concreto, identificando qual
controle mitiga qual risco específico e como esse controle é verificado — não como intenção, como
fato mensurável.
