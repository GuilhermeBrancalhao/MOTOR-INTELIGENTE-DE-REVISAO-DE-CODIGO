---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

**Declarar a versão mínima esperada de contrato explicitamente no código de integração**, não
apenas documentá-la separadamente. Uma verificação que vive só em documentação, não no código, não
impede uma resposta incompatível de ser processada silenciosamente.

**Gerar chave de idempotência a partir de dados da operação, não de timestamp de execução.** Uma
chave baseada em timestamp muda a cada retry, o que anula completamente a proteção de I2 — a
chave precisa identificar a operação lógica, não a tentativa específica de executá-la.

**Configurar timeout mais curto que o limite de paciência do consumidor da integração**, nunca
igual ou maior. Se o timeout da chamada externa é igual ao tempo que o usuário final aceita
esperar, não sobra margem para retry nem para resposta de erro tratada adequadamente.

**Testar o circuit breaker sob falha simulada antes de depender dele em produção.** Um circuit
breaker nunca exercitado sob falha real pode ter limiar mal calibrado — muito sensível (abre por
falhas transitórias normais) ou pouco sensível (não protege a tempo de falha sustentada real).

**Revisar a versão de contrato de toda integração externa periodicamente**, não só quando uma
falha de incompatibilidade já aconteceu. Fornecedores frequentemente anunciam depreciação de
versão com antecedência — descobrir isso proativamente é mais barato que descobrir por erro em
produção.
