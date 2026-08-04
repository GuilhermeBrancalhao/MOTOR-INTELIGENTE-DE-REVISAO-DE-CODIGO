---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 11-Implementacao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/42-plugins/plugins.py -->

`plugins.py`, citado acima, formaliza AD1-AD6: `ativar_plugin` recusa contrato alvo incompatível
com o contrato do host (AD1); `executar_hook_isolado` sempre captura exceção do hook e retorna
`ResultadoDeHook` estruturado, nunca propagando a falha (AD2); `acessar_capacidade` recusa
capacidade não declarada em `DeclaracaoDePlugin.capacidades_solicitadas` (AD3);
`DeclaracaoDePlugin.__post_init__` recusa declaração sem `ponto_de_entrada` (AD4);
`EstadoDoHost.desativar` remove plugin e recursos associados na mesma operação (AD5);
`evoluir_contrato` recusa mudança que quebra hook sem incremento de versão maior do próprio
contrato (AD6, mesma lógica de `validar_release` em `41-SDK`).

Nenhuma das seis funções depende de sistema de isolamento de processo real ou biblioteca de
sandbox externa — a captura de exceção Python simples em `executar_hook_isolado` é suficiente
para provar o princípio central de AD2 sem o custo de configurar um ambiente de isolamento mais
sofisticado apenas para rodar a suíte de teste deste volume específico.

A escolha de modelar capacidade como `frozenset` de string, em vez de um objeto de permissão mais
elaborado, mantém `acessar_capacidade` simples de auditar visualmente — qualquer capacidade
concedida a um plugin está sempre visível como um conjunto plano na própria declaração de
ativação, sem precisar navegar estrutura aninhada para confirmar o que foi de fato autorizado.

Se um sistema real precisasse de isolamento mais forte que captura de exceção em memória — por
exemplo, limite de tempo de execução ou de uso de memória por hook — essa camada poderia ser
adicionada dentro de `executar_hook_isolado` sem alterar sua assinatura pública nem exigir mudança
em nenhum dos chamadores já existentes que dependem do contrato atual da função.