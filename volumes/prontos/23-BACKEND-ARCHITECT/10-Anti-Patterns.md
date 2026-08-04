---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Requisição HTTP síncrona bloqueada esperando resposta de IA que pode levar minutos.** É
exatamente o cenário que S1 existe para evitar — o timeout da requisição se torna o limite real
de duração do trabalho, independente de quanto tempo o processamento em si realmente precisaria.

**Worker que mantém, em memória local, o único registro de qual trabalho está processando.** Se
esse worker morre, o trabalho fica órfão sem que nenhum outro worker saiba que ele existia —
viola S2 e frequentemente também compromete S6, porque o trabalho nunca chega a um estado
terminal visível.

**Fila sem limite de concorrência, aceitando todo trabalho recebido independente da capacidade de
processamento disponível.** Não é ausência de backpressure — é backpressure aplicada tarde
demais, quando o sistema já está sem recurso, em vez de cedo, quando ainda há escolha sobre como
degradar.

**Retry que repete a chamada de IA sem verificar se a chamada anterior já teve efeito.** Reintroduz
o problema que a idempotência (S4, e a idempotência da chamada externa em si, tratada no
16-INTEGRATION) existe para eliminar.

**Trabalho que esgota tentativas e é simplesmente removido da fila sem deixar registro.** Torna
invisível exatamente o tipo de falha que mais precisa de atenção humana — a que já foi tentada
várias vezes e continua falhando.
