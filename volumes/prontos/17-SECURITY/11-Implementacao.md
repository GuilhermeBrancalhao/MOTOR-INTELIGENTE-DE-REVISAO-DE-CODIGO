---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/17-security/classificador.py -->

`classificador.py`, citado acima, é a forma mínima e executável da política deste volume — a
inversão de default, a lista de destinos autorizados, a proteção do próprio painel de controle e o
teto de tamanho. A suíte que o acompanha roda os doze vetores de contorno reais como
parametrização de um único teste, e inclui `ls` e `echo teste` de propósito: sob a política
invertida, comando de aparência inócua também não é `LIVRE`.

Além do exemplo, a política descrita aqui já roda em produção no motor `ENGINE` deste mesmo
repositório, documentada em `README.md` — o que torna este volume incomum entre os essenciais:
tem implementação de referência **e** implementação real em uso.

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
