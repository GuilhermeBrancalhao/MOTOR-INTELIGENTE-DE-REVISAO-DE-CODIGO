---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Processo formal de descomissionamento de sistema — quando um projeto é encerrado, o inventário
precisa refletir isso, mas o gatilho e a responsabilidade por atualizar não estão especificados
neste ciclo.

Integração automatizada com fonte de verdade externa (faturamento de fornecedor, por exemplo)
para validar que o inventário está completo sem depender de registro manual disciplinado — hoje
o registro é manual, no momento da decisão técnica, sem verificação cruzada automática.

Critério quantitativo de quando concentração de fornecedor deixa de ser aceitável e vira
bloqueio — hoje o limiar de sinalização (E2, exemplo de três projetos) é ilustrativo; o critério
de quando isso vira veto, não só sinalização, depende de julgamento humano registrado caso a
caso.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (`Sistema`, `Inventario`, detecção de concentração e
duplicação), testado por mutação nas seis regras. Depois, integração real com
`30-AI-GOVERNANCE` para o caso concreto de dependência cruzando fronteira de dado sensível.

## O que este volume assume que pode mudar

O critério de "consequência nomeável" que justifica decisão de portfólio (E2) é qualitativo hoje
— uma lista fechada de categorias de consequência (fornecedor, dado, custo) pode emergir com uso
real e substituir o critério aberto atual, sem alterar o princípio central do volume.
