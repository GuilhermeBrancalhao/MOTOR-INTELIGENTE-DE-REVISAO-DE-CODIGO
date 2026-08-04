---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/27-llm-router/roteador.py -->

`roteador.py`, citado acima, formaliza L1-L6: `Roteador.rotear` recusa candidato fora de
`candidatos_aprovados` (L1); fallback é escolhido automaticamente quando `esta_degradado` é
verdadeiro (L2); toda decisão é acrescentada a `historico` (L3); `JanelaDeSaude.esta_degradado`
retorna `False` quando a amostra está abaixo de `minimo_de_chamadas`, independente da taxa de
falha (L4); o contador `chamadas_consecutivas_saudaveis_apos_fallback` só permite retorno ao
principal após atingir `janela_estabilidade` (L5); `Roteador.estado_de` expõe o candidato ativo
por tarefa a qualquer momento (L6).

`consecutivas_saudaveis` é resetado para zero assim que um sinal degradado é observado enquanto
já em fallback — não decrementado gradualmente, zerado por completo. Essa escolha significa que
qualquer sinal de degradação durante a janela de estabilidade reinicia a contagem do zero, tornando
a barra de recuperação mais rigorosa: não basta uma maioria de sinais saudáveis, é preciso uma
sequência ininterrupta.

Um esquema de decremento gradual, alternativa considerada e descartada para este modelo mínimo, tornaria a barra de recuperação mais permissiva, mas também mais complexa de raciocinar e testar exaustivamente.

A simplicidade do reset total também torna o comportamento mais fácil de explicar e de testar
exaustivamente, sem casos de borda adicionais sobre quanto cada sinal deveria pesar na
contagem. Um esquema ponderado exigiria decidir, adicionalmente, como cada nova falha durante a
janela de estabilidade deveria descontar da contagem acumulada — uma complexidade que este
modelo mínimo evita deliberadamente.