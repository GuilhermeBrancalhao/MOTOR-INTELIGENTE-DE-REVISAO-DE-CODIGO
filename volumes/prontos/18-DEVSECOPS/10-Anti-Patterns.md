---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Waiver sem data de expiração.** Uma exceção sem prazo é, na prática, uma mudança permanente da
política — só que sem ter passado pelo processo de decidir se o controle deveria mesmo mudar.

**Controle declarado no 17 sem verificação automatizada, tratado como se já estivesse
protegendo o sistema.** A lacuna entre política e enforcement, quando não é visível, gera falsa
confiança — pior do que não ter a política, porque ninguém sabe que precisa agir.

**Gate rodando apenas em agenda periódica, não a cada mudança.** Reintroduz o atraso entre
introdução do risco e detecção que este volume existe para eliminar.

**Bypass do gate feito diretamente na configuração do pipeline, sem passar pelo mecanismo de
waiver.** Um bypass fora do processo de exceção não fica registrado, não tem motivo nomeado e não
expira — é indistinguível, no rastro que deixa, de um controle que nunca existiu.

**Renovar um waiver automaticamente ao expirar, sem revisão.** Isso reintroduz exatamente o
problema que a expiração deveria resolver — a exceção volta a ser permanente, só que com um
prazo cosmético que nunca é de fato respeitado.

**Motivo de waiver copiado de outro waiver sem ajuste.** Um motivo genérico reaproveitado perde a
rastreabilidade que o campo deveria oferecer — cada exceção precisa de um motivo que só faz
sentido para ela.