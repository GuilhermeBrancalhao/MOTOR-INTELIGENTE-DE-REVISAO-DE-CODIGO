---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o catálogo de templates reutilizáveis: declaração de variável obrigatória,
versionamento, validação de uso, neutralidade de domínio, e depreciação explícita.

**Fronteira com `36-DIAGRAMS`.** Catálogo de tipo de diagrama visual é daquele volume. Este
volume trata de template textual reutilizável — front-matter, scaffold, prompt versionado — uma
categoria diferente de artefato reutilizável, com disciplina própria de variável e versão que
diagrama não tem da mesma forma.

**Fronteira com `35-DOCUMENTATION`.** A disciplina de conteúdo gerado nunca editado manualmente
(W5) e ADR imutável são daquele volume. Este volume trata do template que, quando preenchido,
produz o conteúdo — a fonte de verdade que o 35 protege de edição manual é, frequentemente, um
template catalogado aqui.

**Fronteira com `07-PROMPT-ENGINE`.** O contrato de prompt versionado — corpo, variável,
hash, estado — é daquele volume, com sua própria máquina de estados até PROMOVIDO. Um template
de prompt catalogado aqui pode servir de ponto de partida para um prompt versionado formalmente
pelo 07, mas os dois processos de versionamento são distintos.

Não cobre motor de template específico (Jinja, Handlebars, string simples) — os princípios deste
volume (variável declarada, versão, validação, neutralidade, depreciação explícita) valem
independentemente de qual sintaxe de substituição é usada.


Essas três fronteiras (36, 35, 07) evitam que este volume se torne um catálogo genérico demais —
ele trata especificamente de template textual reutilizável com variável e versão, deixando
diagrama visual, disciplina de conteúdo gerado, e contrato formal de prompt para os volumes que
já os tratam com profundidade própria e específica de cada domínio.