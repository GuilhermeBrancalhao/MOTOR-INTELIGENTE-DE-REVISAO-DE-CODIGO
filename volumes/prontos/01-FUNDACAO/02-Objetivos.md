---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Classificar qualquer volume do acervo pelo seu tipo** (`ENGINE`, `ARQUITETURA`, `PROCESSO`,
`BIBLIOTECA`, `GOVERNANCA`) e explicar por que essa classificação existe: cada tipo relaxa um
subconjunto diferente das 18 seções base, para que um volume de processo não seja forçado a
inventar uma máquina de estados que não tem, e um volume de biblioteca não seja forçado a
inventar uma arquitetura própria que também não tem.

**Aplicar os quatro critérios da Definição de PRONTO** a um volume concreto e dizer, com
evidência, qual dos quatro falta: gate estrutural verde, testes dos exemplos citados verdes,
auditoria por outro modelo com média ≥ 8,0 sem seção abaixo de 6, e registro datado no
`CHANGELOG.md`. Saber que "449 testes passam" nunca substitui esse critério — foi exatamente essa
confusão, documentada em `10-Anti-Patterns.md`, que produziu uma entrega prematura deste próprio
acervo em 2026-08-02.

**Decidir quando uma mudança precisa de segundo par de olhos**, usando a matriz de controles de
`07-Regras.md` — não por instinto, mas por categoria de risco explícita (mudança em contrato,
mudança em volume `PRONTO`, mudança em regra de segurança).

**Descrever o ciclo de vida de um volume** do primeiro `_VOLUME.yml` até `PRONTO`, incluindo os
dois becos-sem-saída que existem de propósito: `REQUER_REVISAO` (auditoria reprovou) e a
impossibilidade de gravar `PRONTO` com qualquer gate vermelho, mesmo que a pessoa que está
gravando tenha certeza de que o conteúdo está bom.

**Explicar por que `depende_de` é grafo acíclico de pré-requisito de leitura**, e não é o mesmo
conceito que "assunto vizinho" — distinção que evita ciclo falso entre volumes que se citam
mutuamente sem que um seja pré-requisito do outro.
