---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar um motor de curadoria de conhecimento maduro. Nenhum item vem marcado: quem
verifica marca cada um com evidência à mão.

- [ ] Todo documento ingerido carrega origem, validado_por e confiança explícitos.
- [ ] Consulta padrão de documento válido nunca devolve documento em estado Expirado.
- [ ] Conflito entre documentos do mesmo fato_chave é sinalizado, nunca resolvido por ordem de
      chegada.
- [ ] Falha de ingestão é registrada com motivo, nunca silenciosa.
- [ ] Revalidação de documento expirando é sempre ação explícita, nunca renovação automática por
      tempo.
- [ ] Curadoria (este volume) não decide relevância para consulta específica — isso é 13-RAG.
- [ ] Existe teste que prova que documento expirado não é devolvido por consulta padrão, mesmo
      fisicamente indexado.
- [ ] Existe teste que prova que documento sem origem completa é rejeitado na ingestão.
