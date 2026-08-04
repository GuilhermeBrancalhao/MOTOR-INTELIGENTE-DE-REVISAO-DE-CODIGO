---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**A1 — Toda mudança de schema é aplicável sem quebrar o que já está gravado, compatível com a
versão anterior por pelo menos um ciclo de deploy.** *Consequência:* nenhum deploy de código
depende de uma migração de schema ter terminado no mesmo instante — os dois evoluem
independentemente, dentro de uma janela de compatibilidade conhecida.

**A2 — Proveniência (modelo e versão que produziram o conteúdo) é inseparável de todo conteúdo
gerado por IA persistido.** *Consequência:* uma divergência entre dois resultados aparentemente
similares é diagnosticável como mudança de modelo, não confundida com um bug de processamento.

**A3 — Escrita concorrente conflitante é detectada e rejeitada explicitamente, nunca resolvida
por sobrescrita silenciosa.** *Consequência:* nenhuma mudança concorrente desaparece sem que
quem a fez saiba que um conflito aconteceu e precise decidir o que fazer.

**A4 — Toda coleção de dado com crescimento não limitado tem política de retenção declarada.**
*Consequência:* acúmulo indefinido de dado é sempre uma decisão consciente registrada, nunca uma
consequência de nunca ter sido considerada.

**A5 — Leitura de registro tolera campo desconhecido sem falhar.** *Consequência:* um schema que
ganha um campo novo não quebra código antigo que ainda não sabe da existência desse campo,
permitindo evolução incremental sem coordenação forçada entre todos os leitores.

**A6 — Exclusão de registro referenciado por outro registro é rejeitada, nunca deixa referência
quebrada.** *Consequência:* nenhuma referência aponta para algo que não existe mais sem que a
exclusão original tenha sido uma decisão explícita sobre essa consequência.
