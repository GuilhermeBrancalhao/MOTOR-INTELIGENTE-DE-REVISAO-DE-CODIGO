---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
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
| `32-QUALITY` | O indicador agregado que mede se esta prática está sendo aplicada em escala; este volume é a prática, `32` é a medição |
| `08-AGENT-ENGINE` / `09-ORCHESTRATOR` / `10-WORKFLOW` / `17-SECURITY` / `21-OBSERVABILITY` | Cada um aplica o padrão de prova por mutação na própria seção `13-Testes.md`, com exemplo concreto do próprio domínio |
| `18-DEVSECOPS` | Executa esses testes continuamente no pipeline; este volume define o que um teste deveria ser, não quando roda |
| `33-PERFORMANCE` | Trata latência de execução da suíte, fora do escopo deste volume |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../08-AGENT-ENGINE/13-Testes.md`](../08-AGENT-ENGINE/13-Testes.md) — aplicação concreta do padrão descrito aqui

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `04-Arquitetura.md` (o fluxo de
prova por mutação) e `07-Regras.md`. Para ver o padrão aplicado: `12-Exemplos.md`, com três casos
num domínio neutro inventado, e depois a seção `13-Testes.md` de qualquer volume de motor deste
ciclo, onde o mesmo padrão aparece no domínio próprio daquele volume.
