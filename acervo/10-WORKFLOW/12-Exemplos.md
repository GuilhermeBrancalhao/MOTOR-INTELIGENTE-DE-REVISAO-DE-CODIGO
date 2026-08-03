---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — processamento de documento com aprovação humana no meio

Um workflow de três passos: (1) determinístico, extrai texto de um documento recebido; (2) de
IA, classifica o documento numa categoria e extrai campos estruturados, com formato de saída
validado; (3) espera aprovação humana antes de (4) determinístico, arquivar o documento com a
categoria e campos aprovados. Entre o passo 2 e o passo 3, o checkpoint grava a categoria e os
campos extraídos — se a aprovação demorar dois dias e o processo do motor reiniciar nesse
intervalo, a retomada não reexecuta a extração nem a classificação, só continua esperando o
sinal de aprovação a partir do checkpoint.

## Caso 2 — saída de IA malformada com correção automática

No passo de classificação do caso 1, o modelo devolve um campo de data em formato de texto livre
("terça-feira passada") em vez do formato ISO esperado pelo schema declarado. O validador rejeita
a saída; o workflow declara correção automática para este passo, então o motor reexecuta o passo
de IA com uma instrução adicional apontando o formato esperado. Na segunda tentativa, a saída
bate com o schema, e o workflow segue para a espera de aprovação. Se a segunda tentativa também
falhasse e o limite de correções automáticas fosse um, o motor pausaria em vez de tentar
indefinidamente.

## Caso 3 — retomada após falha de infraestrutura

O mesmo workflow, agora falhando por queda do processo do motor logo depois do passo 2, antes da
confirmação do checkpoint. Na retomada, como o checkpoint da conclusão do passo 2 nunca foi
confirmado, o motor reexecuta o passo 2 (a classificação de IA) — não porque o passo tenha
falhado de fato, mas porque a garantia do motor é "sem checkpoint confirmado, o passo é tratado
como não concluído", mesmo ao custo de uma reexecução ocasionalmente desnecessária. É essa regra
conservadora, descrita em `07-Regras.md`, que evita o cenário oposto e mais perigoso: avançar
com base em um passo que pode não ter de fato terminado.
