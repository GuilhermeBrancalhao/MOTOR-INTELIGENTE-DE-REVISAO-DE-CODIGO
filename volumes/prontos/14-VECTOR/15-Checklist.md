---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar um índice vetorial maduro para produção. Nenhum item vem marcado: quem
verifica marca cada um com evidência à mão.

- [ ] Todo vetor armazenado carrega versão de modelo explícita, nunca inferida.
- [ ] Comparação entre vetores de versões de modelo diferentes é estruturalmente impossível, não
      só evitada por convenção.
- [ ] Toda consulta declara métrica e partição explicitamente; ausência de qualquer uma rejeita a
      consulta.
- [ ] Reindexação é atômica do ponto de vista de quem consulta — nunca existe estado misto
      visível.
- [ ] Documento excluído nunca é devolvido em resultado de busca, mesmo antes de compactação
      física completa.
- [ ] O índice nunca decide relevância final ou corte de resultado — isso é sempre 13-RAG.
- [ ] Existe teste que prova rejeição de consulta sem métrica declarada.
- [ ] Existe teste que prova que documento excluído não aparece em resultado, mesmo
      fisicamente presente na estrutura.
