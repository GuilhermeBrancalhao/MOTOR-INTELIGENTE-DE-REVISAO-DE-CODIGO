---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**T1 — Todo endpoint é versionado explicitamente; mudança que quebra compatibilidade nunca
acontece sob a mesma versão.** *Consequência:* um cliente que já integrou contra uma versão
específica nunca é surpreendido por uma mudança de comportamento sem que a versão tenha mudado
para sinalizar isso.

**T2 — Formato de persistência interna nunca é retornado diretamente ao cliente; toda resposta
passa por tradução explícita.** *Consequência:* uma mudança de schema interno nunca se torna
automaticamente uma mudança de contrato externo — os dois evoluem de forma desacoplada.

**T3 — Formato de erro é único e consistente em todos os endpoints.** *Consequência:* o cliente
trata erro de forma genérica, sem precisar de lógica especial por endpoint.

**T4 — Status de trabalho assíncrono é exposto como recurso estável e consultável.**
*Consequência:* o cliente nunca precisa adivinhar temporização ou fazer retry sem uma política de
consulta clara e definida.

**T5 — Um campo já exposto nunca é repropositado para significar algo diferente sob a mesma
versão de contrato.** *Consequência:* estabilidade semântica, não apenas estrutural — o tipo pode
estar correto e o significado ainda assim ter mudado, e essa mudança também quebra confiança do
cliente.

**T6 — Toda operação síncrona declara orçamento de latência explícito.** *Consequência:* o
cliente nunca descobre empiricamente, em produção, que um endpoint pode levar muito mais tempo do
que o esperado.
