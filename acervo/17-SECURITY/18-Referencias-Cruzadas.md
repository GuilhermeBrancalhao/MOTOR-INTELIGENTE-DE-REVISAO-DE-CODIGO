---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

`depende_de` está vazio de propósito — a fronteira com os volumes abaixo é lateral, não
pré-requisito de leitura.

| Volume vizinho | Relação |
|---|---|
| `18-DEVSECOPS` | O processo que faz os controles deste volume rodarem no pipeline continuamente; este volume define a política, `18` define o processo |
| `21-OBSERVABILITY` | Instrumenta e monitora a detecção definida aqui; este volume define o que precisa ser detectável |
| `01-FUNDACAO` | Tem sua própria matriz de controles, sobre o processo de documentação — não confundir com a matriz deste volume, sobre comportamento de sistema de IA em produção |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../../README.md`](../../README.md) — histórico real do classificador de risco do motor ENGINE, referência concreta deste volume

## Navegação interna

Para entender a decisão central: `04-Arquitetura.md` seguido de `07-Regras.md` (a matriz de
controles). Para o histórico real que motiva a política: `11-Implementacao.md` seguido de
`12-Exemplos.md`, que narram os três casos concretos do motor `ENGINE` com o nível de detalhe que
`17-Conclusao.md` só resume.
