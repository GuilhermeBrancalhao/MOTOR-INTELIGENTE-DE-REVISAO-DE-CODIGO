---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar um gestor de orçamento de contexto maduro para produção. Nenhum item vem
marcado: quem verifica marca cada um com evidência à mão.

- [ ] Orçamento total de tokens é declarado explicitamente na configuração, nunca implícito.
- [ ] Ordem de prioridade entre categorias de conteúdo está definida antes de qualquer pressão de
      orçamento acontecer.
- [ ] Todo item descartado gera registro com categoria e motivo, nunca ausência silenciosa.
- [ ] Compactação é acionada com margem configurada antes do limite, nunca no próprio limite.
- [ ] Documento recuperado por RAG (se o sistema usa) compete pelo mesmo orçamento que qualquer
      outro conteúdo, sem prioridade automática implícita.
- [ ] Instrução de prioridade máxima nunca é descartada silenciosamente; só recusada
      explicitamente se sozinha exceder o orçamento.
- [ ] Existe teste que prova ordem de descarte por prioridade declarada, não por ordem de
      chegada.
- [ ] Existe teste que prova recusa explícita quando a própria instrução de prioridade máxima
      excede o orçamento total.
