---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Instrumentar motivo de encerramento com a mesma granularidade que `08-AGENT-ENGINE` e
`09-ORCHESTRATOR` já definem**, não um "sucesso/falha" simplificado. Colapsar
`OBJETIVO_ATINGIDO`/`ORCAMENTO_EXCEDIDO`/`ERRO_NAO_RECUPERAVEL` num booleano de dois estados
perde exatamente a informação que orienta qual ação corretiva é a certa.

**Calibrar limiar de alerta observando pelo menos um ciclo completo de variação esperada do
sinal** (diário, semanal, dependendo do padrão de uso) antes de fixar o valor crítico — um limiar
calibrado em poucas horas de dado pode confundir variação normal com anomalia.

**Testar o canal de notificação com a mesma disciplina que se testa o sinal em si.** Um alerta
que nunca chega por falha silenciosa do canal (não do sinal) produz a ilusão de que "está tudo
sob controle" quando na verdade só ninguém foi avisado — testar o heartbeat do canal
periodicamente é parte da instrumentação, não um extra.

**Decompor todo painel de custo agregado por tipo de etapa antes de publicar**, mesmo quando a
decomposição parece óbvia para quem construiu o painel — quem consome o painel depois pode não
ter esse contexto, e um número agregado sem decomposição convida a otimizar a etapa errada.

**Registrar a proveniência de todo limiar (de onde o valor veio) junto com o valor em si.** Um
limiar sem essa proveniência, revisado meses depois, não tem como ser avaliado quanto a ainda ser
apropriado — a decisão original se perde junto com o contexto que a justificou.
