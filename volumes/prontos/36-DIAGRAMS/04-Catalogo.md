---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 04-Catalogo
status: PRONTO
atualizado_em: 2026-08-04
---

# Catálogo

**`C4Context`** — mostra o sistema em relação a atores externos e sistemas vizinhos, numa visão de
alto nível. Usado quando a pergunta é "quem fala com quem, e por quê" — nunca para mostrar detalhe
de implementação interna, que pertence a outro nível de zoom.

**`sequenceDiagram`** — mostra a ordem temporal de mensagens entre participantes numa interação
específica. Usado quando a pergunta é "o que acontece, passo a passo, nesta chamada específica" —
particularmente útil para revelar onde uma verificação acontece antes de outra, ou onde um erro
interrompe um fluxo que de outra forma pareceria linear.

**`stateDiagram-v2`** — mostra os estados possíveis de uma entidade e as transições válidas entre
eles. Usado quando a pergunta é "o que pode acontecer com isto ao longo do seu ciclo de vida" —
essencial para revelar transições que não deveriam existir (o que não está no diagrama é tão
importante quanto o que está).

**`flowchart`** — mostra ramificação de decisão condicional, com nós de decisão explícitos e
caminhos alternativos. Usado quando a pergunta é "que caminho uma execução específica toma,
dependendo de quê" — o tipo mais versátil, e por isso o mais fácil de usar incorretamente para
algo que um dos outros três representaria melhor.

Cada entrada deste catálogo carrega prosa explicativa própria e escopo declarado — nenhum tipo é
apenas listado sem contexto de quando escolhê-lo e o que ele deliberadamente não tenta mostrar.
