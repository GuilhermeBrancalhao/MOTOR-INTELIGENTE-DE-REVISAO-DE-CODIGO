---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Todo controle novo declarado no 17 tem um identificador de verificação automatizada
  correspondente neste processo, ou está registrado como lacuna explícita.
- [ ] O gate roda a cada mudança, não em agenda periódica.
- [ ] Toda falha sem waiver ativo bloqueia a mudança por padrão.
- [ ] Todo waiver ativo tem motivo nomeado e data de expiração.
- [ ] Waivers expirados voltam a bloquear sem exigir revogação manual.
- [ ] O resultado do gate expõe o vetor de risco de cada falha bloqueante.
- [ ] Não existe caminho de bypass fora do mecanismo de waiver.

- [ ] Nenhum waiver ativo tem motivo genérico ou copiado sem ajuste.
- [ ] A proporção de controles com verificação automatizada correspondente está registrada e
  sendo acompanhada ao longo do tempo, não apenas checada uma vez.
