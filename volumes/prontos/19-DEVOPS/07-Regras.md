---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**P1 — Toda mudança que chega a produção passa pela mesma sequência de estágios do pipeline, sem
exceção por urgência.** *Consequência:* não existe caminho de deploy direto que contorne build,
teste e segurança — a pressão de um incidente é exatamente o momento em que pular etapas custa
mais caro, não menos.

**P2 — Todo deploy tem caminho de reversão definido e testado antes de a estratégia ser
confiada em produção.** *Consequência:* reverter nunca é improvisado durante um incidente — é
uma operação já validada, disponível no momento em que é precisa.

**P3 — Rollout gradual é o padrão; deploy completo de uma vez é exceção que exige justificativa
explícita.** *Consequência:* um defeito não capturado pelos estágios anteriores afeta uma fração
do tráfego, não a totalidade, dando tempo e sinal para reverter antes do impacto se generalizar.

**P4 — O artefato em produção é sempre rastreável ao commit exato que o produziu, sem
ambiguidade.** *Consequência:* "o que está rodando agora" é sempre uma pergunta com resposta
determinística, nunca uma suposição baseada em quem lembra do último deploy.

**P5 — Estágio do pipeline só executa na posição correta da sequência; falha em um estágio
bloqueia todos os seguintes.** *Consequência:* a ordem do pipeline não é uma convenção seguida
por hábito — é uma regra que a própria estrutura do código impõe.

**P6 — O artefato validado em staging é o mesmo artefato implantado em produção, nunca
reconstruído no caminho.** *Consequência:* elimina a classe de defeito onde o comportamento em
produção diverge do que foi testado por causa de uma diferença introduzida na reconstrução.
