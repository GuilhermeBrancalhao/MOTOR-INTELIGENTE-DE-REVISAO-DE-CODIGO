---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Separar recuperação de reordenação como dois passos distintos.** Recuperação (consultar
`14-VECTOR`) devolve candidatos por proximidade vetorial; reordenação decide, entre os candidatos,
quais de fato respondem à pergunta — proximidade vetorial alta não garante relevância para a
pergunta específica, só similaridade textual/semântica geral.

**Exigir citação rastreável em toda resposta gerada.** Uma afirmação sem documento de origem
citável não é aceita como parte da resposta final — ou é removida, ou a resposta é marcada
explicitamente como sem suporte suficiente na base.

**Medir fidelidade como propriedade verificável**, não como impressão de qualidade — o quanto do
conteúdo da resposta é de fato sustentado pelos documentos citados, aplicando verificação, não
confiando que citação presente implica fidelidade automática.

**Recusar responder quando a base não sustenta a pergunta**, em vez de gerar resposta plausível
sem fundamento — o silêncio explícito ("não há fonte suficiente") é preferível a uma resposta
convincente e não verificável.

**Traçar a fronteira com `11-KNOWLEDGE` e `14-VECTOR`**: este volume nunca decide se um documento
deveria existir na base (isso é `11`) nem como o índice compara vetores (isso é `14`) — consome
os dois como infraestrutura já correta.

**Diagnosticar corretamente de qual dos três volumes um problema de resposta vem** — fonte
desatualizada (`11-KNOWLEDGE`), busca incorreta (`14-VECTOR`), ou citação/fidelidade
(este volume) — usando a fronteira declarada em vez de investigar o sistema inteiro a cada
resposta suspeita.
