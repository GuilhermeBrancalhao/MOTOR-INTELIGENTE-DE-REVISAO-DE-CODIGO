---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 11-Implementacao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Implementação

Este volume descreve política e controle, não cita código executável específico deste ciclo (ver
`16-Roadmap.md`) — mas a política que descreve já está implementada e observada em produção no
motor `ENGINE` deste mesmo repositório, o que torna este volume incomum entre os sete essenciais:
a referência de implementação real existe, documentada em `README.md`, mesmo sem citação formal
via `<!-- exemplo: -->` (que exigiria também o teste correspondente no formato deste acervo,
trabalho de um ciclo seguinte).

## O que o motor ENGINE implementa, generalizado por este volume

O classificador de risco do motor roda como hook antes de cada ação de ferramenta (`PreToolUse`),
aplicando exatamente o fluxo de `04-Arquitetura.md`: comprovadamente inócuo executa; qualquer
outra coisa passa pelas famílias de risco nomeadas (R1 a R12) e recebe `Travado` ou `Rastreado`.
A família R8, especificamente, cobre execução indireta — cano para interpretador e substituição
de comando dentro do argumento, o que inclui o caso `python -c` — e um caso real documentado em
`README.md` mostra um falso positivo nessa família (a string `'EXEC(ruim)'` casando o padrão por
case-insensitivity ausente), corrigido depois da observação. Esse falso
positivo é evidência de que o mecanismo estava de fato rodando e verificando, não decorativo —
um classificador que nunca bloqueia nada legítimo por engano provavelmente também não está
bloqueando o que deveria.

## Ordem de implementação recomendada para um sistema novo

Isolamento estrutural de origem de dado primeiro (a defesa contra prompt injection é a mais
barata de implementar corretamente desde o início e a mais cara de adicionar depois). Lista de
destinos autorizados para chamada de ferramenta em segundo. Classificador de risco de execução
por último, porque é o que exige mais iteração adversarial — o histórico de sete rodadas do
motor `ENGINE` para as famílias R1-R8 sugere que a primeira versão de qualquer classificador
deste tipo não vai ser a versão final.
