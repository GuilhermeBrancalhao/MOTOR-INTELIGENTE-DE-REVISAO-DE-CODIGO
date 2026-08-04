---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**AB1 — Todo template declara suas variáveis obrigatórias explicitamente.**
*Consequência:* nenhuma variável é descoberta apenas lendo a saída gerada e adivinhando o que
precisava ser preenchido.

**AB2 — Todo template é versionado; conteúdo gerado de versão antiga nunca é presumido
compatível com versão mais recente.** *Consequência:* uma mudança de estrutura do template é
sempre uma versão nova, verificável contra o conteúdo que ela gerou no passado.

**AB3 — Uso de template é validado antes de a geração se completar.** *Consequência:* variável
obrigatória ausente falha explicitamente, nunca produz saída com placeholder vazio silencioso.

**AB4 — Template nunca embute conteúdo específico de domínio; permanece genérico e
reutilizável.** *Consequência:* conteúdo específico entra apenas via substituição de variável no
momento do uso, nunca fixado dentro do próprio template.

**AB5 — Depreciação de template é explícita, com motivo e substituto quando possível, nunca
removida silenciosamente.** *Consequência:* uso existente que ainda referencia um template
depreciado sabe explicitamente que precisa migrar, e para onde.

**AB6 — Todo template declara escopo explícito — o que produz, o que não produz.**
*Consequência:* quem usa o template nunca assume que ele cobre mais do que de fato foi pensado
para cobrir.

Juntas, as seis regras tratam template com o mesmo rigor que este acervo já aplica a qualquer
outro artefato reutilizável — nenhuma delas exige ferramenta sofisticada, todas exigem apenas
disciplina de declarar explicitamente o que, de outra forma, ficaria implícito e sujeito a
divergência silenciosa entre cópias do mesmo template usadas em contextos diferentes.