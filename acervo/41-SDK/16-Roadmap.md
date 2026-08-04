---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Detecção automática de mudança que quebra compatibilidade por comparação de assinatura entre
versões (hoje `quebra_compatibilidade` é declarado manualmente por quem propõe a mudança, sem
verificação automática contra a superfície pública anterior real).

Geração automática de changelog de SDK a partir do histórico de mudança de superfície pública —
hoje a documentação de mudança entre versões é um processo manual separado deste modelo.

Suporte a múltiplas linguagens de SDK para o mesmo produto, com sincronização de versão entre
elas — hoje o modelo trata de um único SDK, sem modelar a coordenação entre implementações em
linguagens diferentes que precisam evoluir de forma compatível entre si.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (versão semântica, superfície pública deliberada, erro
acionável, depreciação, exemplo verificado), testado por mutação nas seis regras. Depois,
integração real com o contrato do `25-API-ARCHITECT` que o SDK encapsula.

## O que este volume assume que pode mudar

O modelo de superfície binária (público ou não) é o mínimo suficiente hoje — um esquema com
níveis intermediários (público mas experimental, público apenas para uso interno de outro
produto do mesmo fornecedor) pode ser necessário conforme a diversidade de consumidores do SDK
cresce, sem alterar o princípio central de decisão deliberada e depreciação antes de remoção.
