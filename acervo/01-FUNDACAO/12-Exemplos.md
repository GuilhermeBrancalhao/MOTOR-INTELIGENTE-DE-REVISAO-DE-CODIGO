---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — um volume passa no gate 1 e ainda não está PRONTO

Um redator escreve as 18 seções de um volume `ENGINE`, com front-matter completo, prosa acima do
mínimo em todas, diagramas Mermaid dos três tipos exigidos, cada um com parágrafo descritivo.
`python -m ferramentas.validar NN` devolve `ok: volume NN sem violacoes`. O redator ainda não
pode gravar `status: PRONTO` — faltam o critério 2 (testes dos exemplos citados, se houver
código citado), o critério 3 (auditoria por outro modelo, média ≥ 8,0) e o critério 4 (registro
em `CHANGELOG.md`). Esse é exatamente o estado em que `45-CONCILIACAO-CONTAS`, no acervo irmão
`acervo-controladoria`, ficou depois de sua reescrita: gates 1, 2 e 3 mecânicos verdes,
`status: RASCUNHO` mantido porque a auditoria por outro modelo nunca aconteceu.

## Caso 2 — o BOM mascarando 618 violações

Antes da correção de 2026-08-03, `python -m ferramentas.validar --tudo` reportava 39 violações —
uma por volume, sempre `[volume-yml] campos ausentes: volume`. Parecia um problema pequeno e
uniforme. Depois de remover o BOM dos 39 `_VOLUME.yml`, o mesmo comando passou a reportar 657
violações — porque o gate, antes bloqueado na primeira checagem (existência do campo `volume`),
passou a avançar para dentro de cada seção e encontrar os problemas reais: substância abaixo do
mínimo, front-matter de seção ausente, e dois casos de `tipo` divergente do contrato (`41-SDK` e
`42-PLUGINS`, declarados `BIBLIOTECA` no arquivo mas `ENGINE` no contrato). O número menor não
era o acervo mais saudável — era o gate cego mais cedo.

## Caso 3 — decisão de escopo registrada, não inventada

Em 2026-08-03, diante de 39 volumes esqueleto, a escolha não foi "completar todos" nem "abandonar
o acervo de conhecimento" — foi reduzir o escopo do ciclo para o motor mais 10 volumes essenciais
(`01`, `03`, `07`, `08`, `09`, `10`, `12`, `17`, `21`, `31`), com os outros 32 permanecendo
`RASCUNHO` declarado. A decisão está registrada com data e responsável em `ROADMAP.md` e
`ENTREGA.md` — não é regra inferida do código, é julgamento humano documentado, exatamente a
terceira camada de governança descrita em `04-Arquitetura.md`.
