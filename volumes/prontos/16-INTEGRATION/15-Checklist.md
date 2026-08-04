---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 15-Checklist
status: PRONTO
atualizado_em: 2026-08-04
---

# Checklist

Antes de considerar uma integração externa madura para produção. Nenhum item vem marcado: quem
verifica marca cada um com evidência à mão.

- [ ] Contrato da integração é versionado, e a versão é verificada antes de consumir a resposta.
- [ ] Toda chamada com efeito colateral usa chave de idempotência derivada da operação, nunca de
      timestamp ou identificador de tentativa.
- [ ] Timeout e política de retry são configurados explicitamente para esta integração
      específica, não herdados de padrão genérico.
- [ ] Circuit breaker (ou padrão equivalente) isola falha desta integração da disponibilidade do
      sistema interno inteiro.
- [ ] A pergunta "o outro lado pode mudar sem que eu saiba antes?" foi aplicada para confirmar
      que esta chamada de fato pertence a este volume, não a 22-25.
- [ ] Mudança de contrato que este sistema expõe para consumidores externos é sempre versionada.
- [ ] Existe teste que prova que duas chamadas com a mesma chave de idempotência produzem efeito
      colateral uma única vez.
- [ ] Existe teste que prova que o circuit breaker abre após o limiar de falhas consecutivas e
      impede novas tentativas imediatas.
