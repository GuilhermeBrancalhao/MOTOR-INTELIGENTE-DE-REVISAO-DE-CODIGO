---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Nomear o waiver com o motivo específico da exceção, não uma justificativa genérica — "aguardando
correção do fornecedor X, ticket Y" é rastreável; "temporário" não é.

Tratar controle sem check automatizado como prioridade de automação, não como controle
inexistente — a lacuna visível (D1) só cumpre sua função se motivar a automação, não se for
ignorada indefinidamente.

Revisar waivers ativos periodicamente, mesmo antes da expiração — uma exceção concedida para uma
condição que já não existe mais deveria ser removida cedo, não esperar o prazo vencer sozinho.

Registrar o vetor de risco do controle na própria mensagem de falha do gate, não em um documento
separado que precisa ser procurado — a regra D5 só entrega valor se a informação está onde quem
recebe a falha efetivamente olha primeiro.

Tratar expiração de waiver como evento que gera notificação, não como algo que só é percebido
quando a próxima mudança falha inesperadamente.

Preferir um waiver de prazo curto renovável mediante revisão explícita a um waiver de prazo longo
concedido de uma vez — o custo de renovar com frequência é pequeno comparado ao risco de uma
exceção de meses passar despercebida.

Ligar o identificador de verificação automatizada de cada controle ao commit ou job específico do
pipeline que o implementa, para que a rastreabilidade entre "o que o 17 declara" e "o que
realmente roda" sobreviva a reorganizações do pipeline ao longo do tempo.