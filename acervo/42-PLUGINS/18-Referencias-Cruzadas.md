---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de contrato de extensão,
isolamento de falha e permissão declarada é conceito autocontido, embora reaproveite
explicitamente o princípio de versionamento de `41-SDK`.

| Volume vizinho | Relação |
|---|---|
| `41-SDK` | AD6 reaproveita diretamente a disciplina de versionamento semântico de AC1/AC5 aplicada ao contrato de extensão |
| `20-CLOUD` | Isolamento de falha entre componentes; aqui aplicado especificamente à relação host-plugin |
| `18-DEVSECOPS` | Menor privilégio e permissão explícita; AD3 aplica o mesmo princípio a capacidade de plugin |
| `30-AI-GOVERNANCA` | Registro auditável de ativação; mesma disciplina de trilha aplicada aqui ao ciclo de vida de plugin |

## Links que resolvem hoje

- [`../41-SDK/07-Regras.md`](../41-SDK/07-Regras.md) — regras de versionamento reaproveitadas por
  AD6
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
ativação e desativação: `06-Fluxogramas.md` (o `stateDiagram-v2`).
