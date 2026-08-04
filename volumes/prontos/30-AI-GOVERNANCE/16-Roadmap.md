---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Processo formal de apelação para pessoa afetada por decisão automatizada questionar o resultado
(hoje o volume trata de revisão humana antes da decisão, não de contestação depois dela já ter
sido tomada).

Métricas de equidade e viés por caso de uso, além da classificação de risco geral — hoje risco é
tratado como categoria única, sem decompor especificamente o risco de viés discriminatório contra
grupo protegido.

Integração formal com processo de auditoria externa ou regulatória — hoje a trilha de auditoria
existe internamente, sem modelar como ela seria exportada ou apresentada a um auditor externo.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (caso de uso classificado, decisão auditável, revisão
humana obrigatória por risco), testado por mutação nas seis regras. Depois, integração real com
`26-AI-MODELS` para vincular seleção de modelo à classificação de risco do caso de uso que o usa.

## O que este volume assume que pode mudar

O modelo de quatro níveis de risco (BAIXO, MEDIO, ALTO, CRITICO) é o mínimo suficiente hoje — uma
matriz de risco mais granular, cruzando probabilidade e impacto separadamente, pode ser
necessária conforme a variedade de casos de uso cresce, sem alterar o princípio central de
responsabilidade nomeada e revisão proporcional ao risco.
