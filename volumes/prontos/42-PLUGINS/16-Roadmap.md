---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Isolamento em nível de processo ou sandbox de sistema operacional real — hoje o isolamento
modelado é apenas de captura de exceção em memória, suficiente para provar o princípio, mas sem
proteção contra um plugin que consome recurso de sistema (memória, CPU, tempo de execução) de
forma desproporcional sem lançar exceção alguma.

Descoberta automática de plugin compatível a partir de um repositório central, com verificação de
assinatura de autenticidade antes da ativação — hoje a declaração de plugin é sempre fornecida
diretamente, sem um mecanismo de distribuição e descoberta remota modelado.

Renegociação de capacidade em tempo de execução, permitindo que um plugin já ativo solicite
capacidade adicional sem precisar de reativação completa — hoje toda capacidade é fixada no
momento da declaração original.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (contrato versionado, isolamento por captura de exceção,
capacidade declarada, registro explícito, desativação limpa, evolução de contrato), testado por
mutação nas seis regras. Depois, isolamento de processo real e descoberta remota de plugin.

## O que este volume assume que pode mudar

O modelo de capacidade como conjunto plano de string (`frozenset`) é o mínimo suficiente hoje —
um esquema hierárquico de capacidade (com escopo, expiração, ou capacidade composta de outras
capacidades menores) pode ser necessário conforme a superfície de extensão do host cresce, sem
alterar o princípio central de que nenhuma capacidade é concedida por omissão.
