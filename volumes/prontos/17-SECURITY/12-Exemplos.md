---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — doze contornos de uma lista de proibições (histórico real)

O classificador de risco do motor `ENGINE`, descrito em `README.md`, nasceu como lista de
proibições e foi contornado doze vezes em sete rodadas de revisão adversarial: `bash -c "rm"`,
`echo $(rm -rf)`, quebra de linha depois de um `echo`, `cmd /c del`, `git -c
core.fsmonitor=./script status`, `git diff --output=`, entre outros. Cada rodada encontrava outro
contorno porque comando de shell é uma linguagem própria, com aspas, substituição e apelidos —
enumerar o que é perigoso dentro dela não converge. A correção não foi adicionar o décimo terceiro
item à lista; foi inverter o default: comando de shell nunca é `Livre`.

## Caso 2 — falso positivo provando que o mecanismo funciona

Em sessão real, o hook `PreToolUse` travou um `python -c` pela família R8 quando o comando
continha a string literal `'EXEC(ruim)'` — o padrão `\bexec\(` casava porque a compilação da
regex não distinguia maiúsculas de minúsculas. Corrigido depois da observação. O valor deste
caso como exemplo não é o bug em si — é que ele prova que o classificador estava de fato
avaliando cada comando, não apenas presente como formalidade. Um sistema de segurança que nunca
produz falso positivo é suspeito de estar inativo, não de estar bem calibrado.

## Caso 3 — proteção do próprio painel de controle (família R9)

Uma auditoria adversarial encontrou que escrita em `.engine/estado.json` (o arquivo de estado do
próprio motor) não estava sob nenhuma família de controle — um atacante, ou um erro, poderia
gravar `{"ativo": false}` e desligar os dois hooks que sustentam o modo de operação inteiro. A
família R9 foi criada especificamente para travar escrita nesse caminho, generalizando o
princípio (nunca deixar a infraestrutura de segurança fora do escopo que ela protege) além
daquele arquivo específico, cobrindo qualquer caminho de configuração persistente equivalente.
