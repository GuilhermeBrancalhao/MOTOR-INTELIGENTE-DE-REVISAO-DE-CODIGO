---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Toda migração de schema é compatível com a versão anterior por pelo menos um ciclo de
  deploy.
- [ ] Todo conteúdo gerado por IA persistido carrega proveniência (modelo e versão).
- [ ] Escrita concorrente conflitante é detectada e rejeitada, nunca sobrescreve silenciosamente.
- [ ] Toda coleção de crescimento não limitado tem política de retenção declarada.
- [ ] Leitura tolera campo desconhecido sem falhar.
- [ ] Exclusão de registro referenciado é rejeitada ou propagada explicitamente, nunca deixa
  referência quebrada.
- [ ] Testes de migração cobrem leitura e escrita no formato antigo antes de qualquer consumidor
  ser migrado.


- [ ] Nenhuma migração foi testada apenas contra schema vazio, sem dado real no formato antigo.
- [ ] Toda instância de repositório usa estruturas de dado isoladas, sem compartilhar estado
  mutável padrão entre instâncias diferentes.
