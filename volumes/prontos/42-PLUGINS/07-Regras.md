---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Regras

**AD1 — Contrato de extensão é versionado; plugin com contrato alvo incompatível é rejeitado
antes da ativação.** *Consequência:* incompatibilidade nunca é descoberta como falha de execução
em produção — é recusada no momento da tentativa de ativação.

**AD2 — Falha originada dentro de um plugin nunca propaga ao host; é sempre isolada e
contida.** *Consequência:* um plugin com defeito nunca derruba o processo do host nem afeta
outro plugin ativo ao mesmo tempo.

**AD3 — Toda capacidade usada por um plugin é declarada explicitamente; capacidade não declarada
é negada.** *Consequência:* nenhum plugin acessa recurso sensível além do que foi explicitamente
autorizado no momento da ativação.

**AD4 — Ativação de plugin exige registro explícito (nome, versão de contrato, ponto de
entrada); nunca execução implícita por presença em caminho de busca.** *Consequência:* nenhum
código de terceiro roda sem uma decisão explícita e rastreável de ativação.

**AD5 — Desativação de plugin libera todo recurso alocado durante a ativação, sem efeito
residual.** *Consequência:* o estado do host após desativar um plugin é equivalente ao estado
anterior à ativação, nunca com resíduo esquecido.

**AD6 — O próprio contrato de extensão evolui seguindo a disciplina de versionamento semântico
de `41-SDK`; mudança que quebra um hook exige versão maior nova do contrato.**
*Consequência:* plugin já publicado contra uma versão de contrato continua funcionando enquanto
essa versão maior permanecer suportada pelo host.
