---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Rotear apenas entre candidatos já aprovados pelo `26-AI-MODELS` — o roteador nunca inventa
critério de elegibilidade próprio, apenas escolhe entre o que já foi validado.

Alternar automaticamente para o fallback declarado quando o candidato principal está degradado,
sem bloquear esperando recuperação quando uma alternativa já aprovada existe.

Detectar degradação por sinal explícito acumulado numa janela de chamadas, nunca por uma única
falha isolada — um blip não prova degradação, um padrão sim.

Exigir estabilidade antes de voltar ao candidato principal depois de um fallback, para não
alternar repetidamente entre os dois numa sucessão de trocas que causaria mais instabilidade do
que a degradação original.

Registrar toda decisão de roteamento — qual candidato foi escolhido e por quê — e manter o estado
atual sempre consultável, nunca uma decisão implícita reconstruída só a partir de log posterior.

Os seis objetivos, lidos em conjunto, descrevem um comportamento assimétrico deliberado: reagir
rápido a degradação real (L2, L4) mas devagar ao considerar recuperação (L5) — essa assimetria
não é acidente de implementação, é a defesa central contra o padrão de falha mais comum em
roteador ingênuo, que é alternar repetidamente entre dois candidatos sob condição intermitente.

Um roteador que só implementasse a metade rápida (reagir a degradação) sem a metade lenta (recuperar com estabilidade) resolveria metade do problema e criaria uma nova falha no processo.