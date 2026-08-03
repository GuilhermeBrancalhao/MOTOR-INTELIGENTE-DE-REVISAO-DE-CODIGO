---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**Gravar `PRONTO` com qualquer gate vermelho é proibido**, sem exceção de julgamento humano —
não é uma questão de estilo, é a única coisa que impede o acervo de mentir sobre o próprio
estado. Essa regra sozinha é o motivo de este arquivo existir: uma entrega anterior deste acervo
declarou "PRONTO PARA AUDITORIA" com 39 volumes que não passavam nem no gate 1, e o dano não foi
o conteúdo fraco em si — foi a afirmação de que o conteúdo tinha sido verificado quando não
tinha.

**O contrato (`contrato.json`) é a única fonte de verdade sobre a regra; a prosa (este volume,
`Convencoes.md`) explica o porquê, mas não decide.** Quando os dois divergem, o contrato vence, e
divergência é bug de documentação, não ambiguidade a ser interpretada.

**`depende_de` é pré-requisito de leitura, e o grafo é acíclico.** Vizinhança de assunto entre
dois volumes que se citam mutuamente (por exemplo, `07` e `28`) não entra em `depende_de` — mora
em `18-Referencias-Cruzadas.md` de cada um. Confundir os dois conceitos produziria ciclo falso e
o teste `depende-de-ciclo` do validador existe justamente para pegar essa confusão.

**Auditoria não pode ser feita pela mesma entidade que redigiu.** O critério 3 da Definição de
PRONTO exige "outro modelo" precisamente para que a verificação não compartilhe o viés de quem
escreveu — um redator inclinado a achar o próprio texto suficiente é o padrão, não a exceção.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Gate estrutural (`validar NN`) obrigatório antes de qualquer promoção | Volume declarado `PRONTO`/`REQUER_REVISAO` sem front-matter, substância ou diagrama corretos | Exit code do `ferramentas.validar`; qualquer violação impede a promoção |
| Auditoria por entidade distinta do redator | Viés de autoavaliação inflando a nota de qualidade | Registro em `auditorias/VOL-NN-auditoria-YYYY-MM-DD.md` com identidade do auditor distinta do commit de redação |
| `depende_de` restrito a grafo acíclico | Pré-requisito circular tornando a ordem de leitura impossível | `ferramentas.validar --cross-refs`, regra `depende-de-ciclo` |
| Mudança em `contrato.json` exige atualização sincronizada de `Convencoes.md` | Documentação humana divergir silenciosamente da regra executável | `test_convencoes_nao_derivou` reprova a suíte do motor se a tabela de tipos divergir |
| Registro datado em `CHANGELOG.md` como quarto gate | Promoção a `PRONTO` sem trilha auditável de quando e por quem | `status.py` lê a linha `media:` do relatório de auditoria mais recente; ausência de registro mantém o volume fora de `PRONTO` |

A tabela acima é o controle de verdade — cada linha corresponde a um teste ou regra nomeada que
falha de forma reprodutível se o controle for violado, não a uma expectativa de boa conduta.
