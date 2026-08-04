---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Inventário de sistemas com componente de IA no portfólio, com dependência de fornecedor/modelo/
fonte de dado explícita por sistema. Critério de quando uma decisão de projeto se torna decisão
de portfólio (consequência que cruza fronteira de projeto). Custo total de propriedade agregado
e detecção de capacidade duplicada entre projetos.

## Fora deste volume, e para onde vai

**Arquitetura técnica interna de um sistema** é `02-CORE` e os volumes de arquitetura de camada
(`22`-`25`) — este volume nunca decide como um sistema é construído por dentro, só onde ele se
encaixa no conjunto.

**Seleção de modelo específico por critério técnico** (latência, qualidade de resposta) é
`27-LLM-ROUTER` — este volume só entra quando a escolha de modelo cria dependência de fornecedor
que se repete entre projetos; a escolha técnica pontual continua sendo do projeto.

**Governança de uso de IA** (política de uso aceitável, revisão humana obrigatória) é
`30-AI-GOVERNANCE` — este volume trata de onde o sistema se encaixa estruturalmente no portfólio,
não de como o uso de IA dentro dele é governado eticamente.

**Integração entre sistemas** (contrato de API entre um sistema e outro) é `16-INTEGRATION` —
este volume identifica que dois sistemas deveriam se integrar em vez de duplicar capacidade; o
contrato técnico da integração em si é daquele volume.

## Fronteira deliberada

Este volume não tem autoridade de veto sobre decisão técnica de projeto — só sobre decisão que
tem consequência de portfólio explícita e nomeável. Uma decisão de portfólio sem essa
justificativa nomeada é overreach, tratado como anti-padrão em `10-Anti-Patterns.md`.
