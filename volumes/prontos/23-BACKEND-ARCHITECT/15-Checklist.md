---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

- [ ] Toda operação que pode exceder o timeout de requisição síncrona é modelada como trabalho
  assíncrono com estado consultável.
- [ ] Nenhum worker mantém estado exclusivo que impediria outro worker de continuar um trabalho.
- [ ] Backpressure é aplicada explicitamente, testada sob carga simulada antes de produção.
- [ ] Toda solicitação repetida com a mesma chave de idempotência é reconhecida, nunca duplicada.
- [ ] Toda transição de estado de trabalho passa por uma operação nomeada e testável.
- [ ] Trabalho que esgota tentativas de retry permanece consultável em estado terminal.
- [ ] O limite de tentativas é configurável por tipo de trabalho, não um valor único global.


- [ ] Nenhum campo do modelo de trabalho registra qual worker específico o processou.
- [ ] A contagem de tentativas é visível junto do estado, não apenas o estado final isolado.
