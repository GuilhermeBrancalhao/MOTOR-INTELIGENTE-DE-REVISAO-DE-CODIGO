---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["17"]` — este volume operacionaliza os controles declarados no 17; não faz sentido
lido sem a matriz de controles que ele executa.

| Volume vizinho | Relação |
|---|---|
| `17-SECURITY` | Declara a política e os controles; este volume roda a verificação de cada um a cada mudança |
| `19-DEVOPS` | O gate deste volume é uma etapa do pipeline de entrega descrito naquele volume |
| `31-TESTING` | Teste de segurança é teste, escrito pela mesma prática; este volume define que ele bloqueia por padrão |
| `32-QUALITY` | O indicador agregado de qualidade pode incluir a proporção de controles enforçados que este volume mede |

## Links que resolvem hoje

- [`../17-SECURITY/07-Regras.md`](../17-SECURITY/07-Regras.md) — matriz de controles que este
  volume executa
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o mecanismo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
waiver em detalhe: `06-Fluxogramas.md`.
