---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

`depende_de` está vazio de propósito — a fronteira com os volumes abaixo é lateral (vizinhança de
assunto), não pré-requisito de leitura; nenhum deles precisa ser lido antes deste para que este
faça sentido.

| Volume vizinho | Relação |
|---|---|
| `09-ORCHESTRATOR` | Coordena múltiplas execuções deste motor; este motor não sabe que existe mais de uma execução simultânea |
| `10-WORKFLOW` | Consome este motor como uma etapa possível dentro de um workflow maior, misturado com etapas determinísticas |
| `27-LLM-ROUTER` | Seleciona o modelo que este motor chama a cada passo; este motor recebe o modelo já selecionado |
| `15-CONTEXT` | Calcula o orçamento de tokens que este motor consome como número; não define como compactar histórico |
| `13-RAG` / `11-KNOWLEDGE` | Se uma ferramenta usa recuperação de conhecimento, é implementação da ferramenta, não deste motor |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — a Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — decisão de escopo do ciclo atual

## Navegação interna

Para entender o contrato do loop: `04-Arquitetura.md` seguido de `05-Diagramas.md` (sequência) e
`06-Fluxogramas.md` (estados). Para implementar: `08-Modelos.md` primeiro, depois `11-
Implementacao.md`, que descreve a ordem recomendada de construção.
