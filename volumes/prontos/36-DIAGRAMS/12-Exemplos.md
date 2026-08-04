---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — entrada de catálogo completa, aceita sem ressalva

Uma entrada com tipo reconhecido, prosa explicativa e escopo declarado é registrada normalmente
no catálogo.

## Caso 2 — tipo não catalogado é rejeitado

Uma tentativa de declarar `TipoDeDiagrama` com nome `"ganttDiagram"`, fora do conjunto de quatro
tipos reconhecidos por este acervo, é rejeitada antes de qualquer outra verificação.

## Caso 3 — entrada sem prosa explicativa é rejeitada

Uma entrada de catálogo com diagrama válido mas sem texto explicando o que não é óbvio na
imagem é rejeitada pelo registro.

## Caso 4 — necessidade mapeia corretamente para o tipo certo

Uma necessidade declarada como "mostrar transição de estado de uma entidade" é mapeada
corretamente para `stateDiagram-v2`, nunca para outro tipo do catálogo.

## Caso 5 — vigência detecta diagrama desatualizado

Uma verificação de vigência confirma que um diagrama específico não reflete mais o comportamento
real do sistema, levantando exceção nomeada com o título do diagrama afetado.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 4 é o mais didático porque
mostra diretamente a tradução de uma necessidade em linguagem natural para o tipo específico de
diagrama que a atende, o núcleo prático de X5 aplicado concretamente.

Os demais casos cobrem as rejeições específicas de cada regra, formando junto com o Caso 4 a cobertura mínima necessária para confiar nas seis regras deste volume.

Essa progressão de casos, do sucesso ao caminho de rejeição de cada regra, é o padrão de cobertura que este acervo já aplica consistentemente em praticamente todo volume promovido.