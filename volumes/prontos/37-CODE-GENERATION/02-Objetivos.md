---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Validar todo código gerado com a mesma disciplina de código escrito manualmente — compilação e
teste — nunca aceito só porque a origem é geração automática.

Marcar todo código gerado como tal, e nunca editá-lo manualmente — qualquer mudança necessária
vai para a especificação que o gera, nunca diretamente no arquivo de saída.

Garantir que a geração seja reproduzível — mesma especificação produz mesmo código gerado,
sempre, tornando a saída auditável e comparável entre execuções.

Exigir revisão humana antes de código gerado entrar em produção, independente de quão
completamente ele passou em validação automatizada.

Versionar a especificação que produz código gerado junto do próprio código gerado, e declarar
explicitamente o escopo do que o código gerado foi pensado para fazer.

Os cinco objetivos, lidos juntos, tratam código gerado exatamente como código escrito à mão
merece ser tratado — nenhum atalho por origem, nenhuma confiança emprestada da reputação de quem
(ou o quê) o produziu. A validação (primeiro) e a revisão humana (quarto) são as duas barreiras
que nenhuma origem de código, gerada ou manual, deveria pular; marcação (segundo) e
rastreabilidade (quinto) são o que torna possível manter essa disciplina ao longo do tempo, sem
depender de lembrar de memória qual arquivo veio de onde.