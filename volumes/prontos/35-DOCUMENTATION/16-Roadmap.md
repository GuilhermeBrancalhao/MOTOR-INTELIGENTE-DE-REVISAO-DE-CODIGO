---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Verificação automática de vigência integrada ao pipeline de CI (hoje `verificar_vigencia` é uma
operação que precisa ser chamada explicitamente, sem gatilho automático em mudança de código).

Índice pesquisável de ADRs por tópico ou componente afetado — hoje o registro é apenas por
número sequencial, sem categorização adicional que facilite encontrar decisões relacionadas.

Processo formal de revisão periódica de ADR antigo para avaliar se ainda deveria ser considerado
vigente, mesmo sem um ADR novo o substituindo explicitamente.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (ADR imutável com substituição, documento versionado,
vigência verificada, distinção gerado/manual), testado por mutação nas seis regras. Depois,
integração real com o pipeline de CI do `19-DEVOPS` para verificação automática de vigência.

## O que este volume assume que pode mudar

O modelo de ADR com três campos (contexto, decisão, consequência) é o mínimo suficiente hoje —
um esquema mais rico (alternativas consideradas e descartadas, participantes da decisão) pode ser
necessário conforme a complexidade das decisões documentadas cresce, sem alterar o princípio
central de imutabilidade e substituição explícita.
