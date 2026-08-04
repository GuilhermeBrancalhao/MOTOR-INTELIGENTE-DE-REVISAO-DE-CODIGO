---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar um pipeline de RAG maduro para produção. Nenhum item vem marcado: quem
verifica marca cada um com evidência à mão.

- [ ] Toda afirmação na resposta final rastreia a uma citação presente, sem exceção.
- [ ] Reordenação por relevância é etapa distinta de recuperação por proximidade, com scores
      separados e não confundidos.
- [ ] Validade de cada documento citado é confirmada no momento da consulta, não herdada do
      momento da indexação.
- [ ] O sistema recusa explicitamente quando não há fonte válida suficiente, em vez de gerar
      resposta sem fundamento.
- [ ] Fidelidade é medida depois da geração, nunca assumida pela presença de citação.
- [ ] Um problema de fonte desatualizada é distinguível, no diagnóstico, de um problema de
      citação ou fidelidade deste volume.
- [ ] Existe teste que prova que documento expirado entre indexação e consulta não é citado como
      válido.
- [ ] Existe teste que prova recusa explícita quando zero candidato válido sobrevive à
      confirmação.
