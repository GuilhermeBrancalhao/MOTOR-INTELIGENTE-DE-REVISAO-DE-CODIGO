---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Uma chamada entre dois módulos do mesmo produto e uma chamada para um sistema de outro time, outro
fornecedor ou outro ciclo de release parecem tecnicamente idênticas — as duas são uma função
chamando outra através de uma interface. A diferença que importa não está na mecânica da chamada,
está no que se pode assumir sobre o outro lado: dentro do mesmo produto, mudança de contrato é
coordenável numa única conversa entre times vizinhos; atravessando a fronteira do produto, o outro
lado pode mudar sem aviso, falhar sem explicação, ou ter ciclo de deploy completamente
dissociado do seu.

Este volume trata dessa fronteira específica — não qualquer chamada entre componentes, mas a que
cruza para fora do que uma única equipe ou um único ciclo de release controla. O contrato dessa
chamada precisa ser versionado explicitamente, porque o outro lado pode evoluir sem avisar. Toda
chamada com efeito colateral precisa de idempotência, porque retry sobre um lado que você não
controla é a norma, não a exceção. E falha do outro lado precisa ser isolada, para que
indisponibilidade de um fornecedor externo não vire indisponibilidade do sistema inteiro.

A fronteira com `22`-`25` (os volumes de arquitetura de camada) é a mesma decidida em
`ROADMAP.md`: chamada entre camadas do mesmo produto é aqueles volumes; chamada que cruza para
fora do produto é este. A pergunta prática que decide onde uma chamada específica se encaixa é
simples — o outro lado pode mudar sem que você saiba antes?
