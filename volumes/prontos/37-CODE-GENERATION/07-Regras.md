---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**Y1 — Código gerado é validado com a mesma disciplina de código escrito manualmente —
compilação e teste — nunca aceito sem essa validação.** *Consequência:* a origem do código nunca
concede passe livre; a garantia de correção vem da verificação, não da confiança na fonte.

**Y2 — Código gerado é marcado como tal e nunca editado manualmente; mudança vai para a
especificação.** *Consequência:* nenhuma edição desaparece silenciosamente na próxima geração —
a mudança sempre está no lugar certo para persistir.

**Y3 — Geração é determinística: mesma especificação produz mesmo código gerado.**
*Consequência:* a saída é auditável e comparável entre execuções, sem variação inexplicada para a
mesma entrada.

**Y4 — Código gerado exige revisão humana antes de produção, independente de validação
automatizada ter passado completamente.** *Consequência:* nenhum código gerado alcança produção
sem que uma pessoa tenha revisado, mesmo quando toda verificação automática já confirmou
correção técnica.

**Y5 — A especificação que produz código gerado é versionada junto do código.**
*Consequência:* todo código gerado é rastreável até exatamente o que o produziu e quando.

**Y6 — Código gerado declara escopo explícito — o que foi pensado para fazer, e o que não foi.**
*Consequência:* código gerado nunca é usado silenciosamente fora do limite para o qual foi
originalmente especificado.
