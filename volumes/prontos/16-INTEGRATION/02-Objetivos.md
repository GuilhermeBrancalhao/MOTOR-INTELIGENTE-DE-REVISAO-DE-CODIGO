---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Versionar todo contrato de integração externa explicitamente**, e verificar compatibilidade de
versão antes de confiar na resposta — nunca assumir que o formato de resposta de hoje continuará
válido amanhã sem verificação.

**Aplicar idempotência a toda chamada externa com efeito colateral**, usando uma chave que
identifica a operação de forma que repetir a chamada nunca duplica o efeito, mesmo quando o
motivo do retry é desconhecido (timeout, erro de rede, resposta perdida).

**Declarar timeout e política de retry explicitamente por integração**, nunca confiar em padrão
implícito da biblioteca cliente — cada integração externa tem características de latência e
confiabilidade próprias que merecem configuração própria.

**Isolar falha de integração externa da disponibilidade interna do sistema**, usando um padrão
de proteção (como circuit breaker) que impede uma dependência externa degradada de arrastar o
sistema inteiro para baixo junto com ela.

**Traçar a fronteira com `22`-`25`**: chamada entre camadas do mesmo produto, sob controle da
mesma equipe e mesmo ciclo de release, é daqueles volumes; chamada que cruza para outro time,
outro fornecedor ou outro ciclo de release é deste. A pergunta que decide é sempre "o outro lado
pode mudar sem que eu saiba antes?".
