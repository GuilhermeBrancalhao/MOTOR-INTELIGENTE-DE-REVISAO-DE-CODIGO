---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

`depende_de` está vazio de propósito — FUNDACAO é o volume "01", lido antes de qualquer outro, e
não tem pré-requisito de leitura por definição. A vizinhança abaixo é relação lateral, fora do
grafo:

| Volume vizinho | Relação |
|---|---|
| `02-CORE` | Consome os papéis e ciclo de vida daqui para decidir a fronteira determinístico/probabilístico da arquitetura core |
| `17-SECURITY` | Tem sua própria matriz de controles, sobre o sistema de IA em produção — não confundir com a matriz de controles deste volume, sobre o processo de documentação |
| `21-OBSERVABILITY` | As métricas de `14-Metricas.md` deste volume medem saúde do processo de documentação; `21` mede telemetria de sistema em produção |
| `35-DOCUMENTATION` | Trata documentação como produto de engenharia em geral; este volume trata especificamente a governança deste acervo |

## Links que resolvem hoje

- [`../00-INTRODUCAO/contrato.json`](../00-INTRODUCAO/contrato.json) — a fonte de verdade legível por máquina
- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — a projeção humana do contrato
- [`../ROADMAP.md`](../ROADMAP.md) — decisão de escopo do ciclo atual, com data
- [`../../ENTREGA.md`](../../ENTREGA.md) — estado real da entrega, atualizado 2026-08-03

## Navegação interna

Para aplicar o gate a um volume: `07-Regras.md` (a matriz) seguido de `06-Fluxogramas.md` (o
caminho de decisão). Para entender o histórico que motivou este volume: `10-Anti-Patterns.md`
seguido de `12-Exemplos.md`, que narram o bug de BOM e a decisão de escopo com o nível de detalhe
que `17-Conclusao.md` só resume.
