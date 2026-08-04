---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Revisar diagrama junto de mudança significativa no código que ele representa, não apenas quando
alguém percebe a divergência por acaso — a mesma disciplina de vigência ativa já recomendada para
documentação em geral vale com ainda mais força para diagrama, que é mais fácil de deixar
desatualizado silenciosamente por ser visual.

Preferir dois diagramas simples e focados a um único diagrama tentando mostrar tudo — um
diagrama que tenta cobrir estrutura, interação e ciclo de vida ao mesmo tempo geralmente
comunica pior do que três diagramas, cada um focado no que seu tipo faz melhor.

Nomear explicitamente, na prosa que acompanha o diagrama, qual decisão de design o diagrama
revela — o objetivo não é apenas mostrar como o sistema funciona, é destacar a escolha que
alguém poderia questionar sem o contexto.

Manter os quatro tipos catalogados como vocabulário fechado, resistindo à tentação de introduzir
um quinto tipo sem necessidade genuína — mais tipos significa mais notação para quem lê aprender,
e cada tipo novo precisa justificar seu próprio propósito específico como os quatro já fazem.


Revisar o catálogo periodicamente contra os diagramas de fato presentes nos volumes do acervo —
um catálogo que descreve tipos em abstrato, mas nunca é comparado contra o uso real, corre o
risco de divergir da prática sem que ninguém perceba.