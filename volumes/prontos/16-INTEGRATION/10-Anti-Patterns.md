---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Assumir que a resposta de uma integração externa sempre terá o formato esperado**, sem
verificação de versão. Isso é o oposto direto de I1, e o sintoma é falha de parsing obscura em
produção, muito depois do ponto onde a incompatibilidade poderia ter sido detectada com clareza.

**Usar timestamp ou UUID gerado a cada tentativa como chave de idempotência.** Isso anula I2
completamente — cada retry vira uma chave nova, e o sistema externo processa a operação
múltiplas vezes, exatamente o efeito duplicado que idempotência existe para prevenir.

**Deixar timeout no padrão da biblioteca cliente**, sem configurar explicitamente por
integração. Um padrão genérico de biblioteca raramente é calibrado para as características
específicas de latência de cada sistema externo real que o código consome.

**Deixar uma integração externa lenta ou fora do ar consumir todos os recursos de conexão do
sistema interno**, sem circuit breaker nem timeout agressivo. Isso transforma indisponibilidade
de um fornecedor específico em indisponibilidade do sistema inteiro — o modo de falha que I4
existe para prevenir.

**Tratar integração entre times da mesma empresa, mas de squads diferentes, como se fosse
interna e confiável por padrão.** A pergunta de I5 ("o outro lado pode mudar sem que eu saiba
antes?") frequentemente responde "sim" mesmo dentro da mesma empresa — squad diferente, ciclo de
release diferente, é integração externa para efeitos deste volume.
