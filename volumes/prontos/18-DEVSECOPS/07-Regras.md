---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**D1 — Todo controle declarado em `17-SECURITY` tem, neste volume, um identificador de
verificação automatizada correspondente, ou é registrado como lacuna explícita.**
*Consequência:* a distinção entre "existe como política" e "está sendo enforçado" nunca fica
implícita — uma política sem automação aparece como tal, em vez de ser tratada como se já
estivesse protegendo o sistema.

**D2 — Gate de segurança bloqueia por padrão quando um controle falha; prosseguir exige waiver
explícito, nomeado e com prazo.** *Consequência:* não existe caminho de "ignorar e seguir" sem
deixar rastro — toda exceção é uma decisão registrada, não um silêncio.

**D3 — Waiver expirado é tratado como inexistente, sem exigir revogação manual.**
*Consequência:* uma exceção temporária nunca se torna permanente por ausência de alguém lembrar
de removê-la; o prazo declarado no próprio waiver é o mecanismo de reversão.

**D4 — A verificação roda em toda mudança, não em agenda periódica.** *Consequência:* o risco é
prevenido no momento em que é introduzido, não descoberto semanas depois em uma auditoria — o
custo de corrigir cresce com o tempo entre introdução e detecção, e este processo mantém esse
tempo próximo de zero.

**D5 — O resultado do gate carrega o vetor de risco de cada controle que falhou, não apenas um
booleano.** *Consequência:* quem recebe a falha consegue triá-la sem abrir um segundo documento
para entender o que o controle protegia.

**D6 — Controle novo declarado no 17 não é considerado enforçado até que seu identificador de
verificação exista neste processo.** *Consequência:* declarar uma política e automatizá-la são
dois eventos distintos, e a janela entre eles é uma lacuna conhecida, não uma suposição de
cobertura completa.
