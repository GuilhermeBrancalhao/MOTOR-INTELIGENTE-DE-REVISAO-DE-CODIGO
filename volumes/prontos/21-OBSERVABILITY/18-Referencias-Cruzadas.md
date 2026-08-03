---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

`depende_de` está vazio de propósito — a fronteira com os volumes abaixo é lateral, não
pré-requisito de leitura.

| Volume vizinho | Relação |
|---|---|
| `08-AGENT-ENGINE` / `09-ORCHESTRATOR` / `10-WORKFLOW` | Produzem os sinais de motivo de encerramento e intervenção humana que este volume instrumenta e monitora |
| `17-SECURITY` | Define a taxonomia de risco a detectar; este volume define como o sinal correspondente é instrumentado continuamente |
| `01-FUNDACAO` | Tem métricas próprias sobre saúde do processo de documentação; não confundir com telemetria de sistema em produção, assunto deste volume |
| `27-LLM-ROUTER` / `07-PROMPT-ENGINE` | Destinos naturais de investigação quando a decomposição de custo por etapa de IA aponta para lá |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../08-AGENT-ENGINE/08-Modelos.md`](../08-AGENT-ENGINE/08-Modelos.md) — o `MotivoEncerramento` que este volume instrumenta

## Navegação interna

Para entender a decisão central: `04-Arquitetura.md` seguido de `07-Regras.md` (a matriz de
controles). Para calibração de limiar na prática: `06-Fluxogramas.md` seguido de `12-Exemplos.md`,
que narra um caso concreto de limiar mal calibrado e sua correção.
