---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Carregar e executar automaticamente qualquer arquivo encontrado numa pasta de plugins, sem
declaração explícita de ativação.** Viola AD4 — código de terceiro passa a rodar sem qualquer
decisão rastreável, apenas por estar presente num caminho de busca.

**Deixar uma exceção de hook de plugin propagar sem captura até o loop principal do host.**
Viola AD2 — um único plugin com defeito pode derrubar o processo inteiro, afetando todo usuário
do host, não apenas quem instalou aquele plugin específico.

**Conceder a todo plugin ativo acesso amplo por padrão, exigindo apenas que capacidade sensível
demais seja explicitamente negada.** Viola AD3 — inverte o princípio de permissão declarada,
tornando o padrão inseguro em vez de seguro.

**Desativar um plugin removendo-o da lista de ativos sem liberar recurso que ele alocou durante
a ativação.** Viola AD5 — o host acumula resíduo de todo plugin já desativado ao longo do tempo,
um vazamento de recurso que cresce silenciosamente.

**Quebrar a assinatura de um hook existente numa versão menor do contrato de extensão, "porque é
só um ajuste pequeno".** Viola AD6 — qualquer plugin já publicado contra a versão anterior do
contrato passa a falhar sem aviso prévio algum.

**Reaproveitar o resultado de uma verificação de compatibilidade anterior ao reativar um plugin,
sem repetir a checagem contra o estado atual do contrato do host.** Viola o espírito de AD1 —
uma mudança no contrato do host entre a desativação e a reativação pode passar despercebida,
justamente o cenário que a verificação de compatibilidade existe para capturar a cada tentativa.