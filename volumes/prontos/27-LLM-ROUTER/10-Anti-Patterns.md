---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Roteador que aceita qualquer candidato passado a ele, sem verificar aprovação do 26.** Viola
L1 — a fronteira entre seleção e roteamento desaparece, e o roteador passa a decidir elegibilidade
por conta própria.

**Fallback disparado por uma única chamada com erro, sem considerar volume de amostra.** Viola
L4 — reage a ruído como se fosse sinal, tornando o sistema mais instável do que a degradação
original justificaria.

**Retorno ao principal no primeiro sinal saudável após fallback, sem janela de estabilidade.**
Viola L5 — o padrão clássico de flapping, alternando entre dois candidatos repetidamente sob
condição de degradação intermitente.

**Estado de roteamento que só existe implicitamente, reconstruído a partir de log depois de um
incidente.** Viola L6 — a resposta para "qual candidato está ativo agora" deveria ser uma
consulta direta, não uma investigação.

**Combinar decisão de roteamento com decisão de custo na mesma lógica, sem separação clara.**
Confunde a fronteira com o `34-COST-OPTIMIZATION` — saúde e custo são eixos diferentes de decisão,
mesmo quando as duas acabam influenciando o mesmo roteamento.


**Testar o roteador apenas no caminho de degradação, nunca no de recuperação.** A janela de
estabilidade (L5) é onde a maioria dos bugs de flapping se escondem, e sem teste dedicado a esse
caminho específico, ele frequentemente só é descoberto em produção.