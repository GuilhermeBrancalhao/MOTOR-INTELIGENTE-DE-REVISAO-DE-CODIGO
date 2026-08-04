---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O componente central é o `Recurso` — declarativo e imutável, identificado por nome, tipo,
ambiente e dono. `Recurso` recusa sua própria criação quando o dono está ausente, tornando
atribuição de responsabilidade (N3) uma condição de existência, não uma etiqueta adicionada
depois. Não existe, na modelagem, um caminho de "criar recurso sem declarar" — todo recurso que o
sistema reconhece passou por essa validação.

`PlanoDeInfraestrutura` mantém a lista de recursos declarados e é o único ponto que aplica mudança
a um recurso específico, sempre validando que o ambiente da mudança corresponde ao ambiente do
recurso alvo — isolamento por ambiente (N4) é imposto na própria operação de mudança, não deixado
como convenção que depende de disciplina de quem aplica a mudança.

A validação de configuração sem segredo inline (N5) roda sobre a configuração bruta antes de um
recurso ser aceito, rejeitando explicitamente chaves que parecem carregar segredo em texto plano.
A detecção de divergência (`detectar_drift`, N6) compara a lista declarada contra um estado real
observado, nunca assumindo que os dois coincidem — cada comparação retorna divergências
explícitas, nunca um booleano genérico de "está tudo bem".


Nenhum desses componentes conhece o provedor de nuvem específico por trás dele — a arquitetura é
deliberadamente neutra a fornecedor, porque as garantias que este volume exige (declaração,
redundância, atribuição de custo, isolamento, detecção de drift) precisam valer
independentemente de qual provedor efetivamente executa o provisionamento.