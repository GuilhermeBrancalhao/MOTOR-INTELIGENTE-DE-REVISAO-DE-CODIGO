---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Comparação automática entre gerações sucessivas da mesma especificação, para detectar mudança
inesperada de comportamento entre versões do gerador — hoje o modelo verifica determinismo dentro
de uma única execução, não entre execuções separadas por tempo ou versão de ferramenta.

Métrica de qualidade de especificação (ambiguidade, completude) calculada antes da geração
acontecer, como sinal preditivo de taxa de sucesso — hoje a especificação é validada apenas por
presença de campo obrigatório, não por qualidade de conteúdo.

Integração formal com o processo de aprovação de caso de uso do `30-AI-GOVERNANCE` quando código
gerado implementa uma decisão automatizada que afeta pessoa diretamente.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (especificação versionada, validação obrigatória,
marcação e imutabilidade manual, revisão humana), testado por mutação nas seis regras. Depois,
integração real com o pipeline de validação do `19-DEVOPS`.

## O que este volume assume que pode mudar

O modelo de validação binária (compilou/não compilou, testes passaram/não passaram) é o mínimo
suficiente hoje — um esquema mais granular (cobertura de teste do código gerado, análise estática
adicional) pode ser necessário conforme a criticidade do código gerado cresce, sem alterar o
princípio central de nunca dispensar validação pela origem do código.
