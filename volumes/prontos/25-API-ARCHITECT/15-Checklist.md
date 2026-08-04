---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Todo endpoint é versionado explicitamente.
- [ ] Nenhuma resposta expõe o formato de persistência interna diretamente.
- [ ] Todo erro, em qualquer endpoint, segue o mesmo formato consistente.
- [ ] Status de trabalho assíncrono é exposto como recurso consultável com URL própria.
- [ ] Nenhum campo já exposto foi repropositado para significar algo diferente na mesma versão.
- [ ] Toda operação síncrona declara orçamento de latência explícito.
- [ ] A latência real observada é comparada periodicamente contra o orçamento declarado.


- [ ] Nenhum campo foi removido sem considerar que clientes existentes podem depender de sua
  presença.
- [ ] O changelog de contrato está separado do changelog de mudanças internas não visíveis ao
  cliente.
