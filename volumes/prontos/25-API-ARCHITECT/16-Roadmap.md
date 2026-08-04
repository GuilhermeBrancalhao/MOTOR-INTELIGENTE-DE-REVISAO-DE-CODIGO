---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Política de depreciação formal de versão antiga de contrato (hoje o modelo cobre a criação e
estabilidade de uma versão, mas não o processo de sinalizar e eventualmente descontinuar uma
versão anterior).

Contrato de taxa de consulta (rate limit) para o endpoint de status de trabalho (T4) — hoje o
recurso é consultável, mas sem uma política explícita de com que frequência a consulta é
recomendada ou permitida.

Geração automática de documentação a partir de `ContratoDeEndpoint` — hoje a declaração de campo
existe apenas como estrutura de dados verificável, sem produzir automaticamente a documentação
que a torna visível para quem integra.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (contrato versionado, tradução explícita, erro
consistente, status consultável, orçamento de latência), testado por mutação nas seis regras.
Depois, integração real com o modelo de trabalho do `23-BACKEND-ARCHITECT` como fonte concreta do
estado exposto.

## O que este volume assume que pode mudar

O modelo de versionamento binário implícito (mesma versão = compatível, versão diferente = pode
quebrar) é o mínimo suficiente hoje — um esquema mais expressivo (versionamento semântico
completo, com depreciação gradual) pode ser necessário conforme o número de clientes integrados
cresce, sem alterar o princípio central de tradução explícita e estabilidade sob a mesma versão.
