---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a compilação de um prompt promovido em payload concreto: tradução de dialeto,
verificação de orçamento de tokens, posicionamento de ponto de cache, e substituição obrigatória
de variável.

**Fronteira com `07-PROMPT-ENGINE`.** O 07 define o contrato do prompt — corpo, variáveis
declaradas, hash, estado. Este volume consome esse contrato já promovido; nunca decide se um
prompt está pronto, nunca versiona, nunca avalia contra caso de ouro. Essa fronteira é a mesma
decidida em `ROADMAP.md`, grupo 1.

**Fronteira com `29-PROMPT-OPTIMIZER`.** Busca automática de variante de prompt, usando os
mesmos casos de ouro do 07 como função objetivo, é daquele volume. Este volume compila uma
variante já definida — não propõe variante nova.

**Fronteira com `26-AI-MODELS` e `27-LLM-ROUTER`.** O dialeto de compilação corresponde ao modelo
selecionado pelo 26 e roteado pelo 27 — este volume recebe qual dialeto usar como entrada, não
decide qual modelo a chamada deveria usar.

Não cobre execução da chamada ao provedor em si — o payload compilado por este volume é a entrada
para uma chamada executada por outra camada, fora do escopo deste volume.


Essas três fronteiras (07, 29, 26/27) mantêm este volume estritamente sobre tradução — ele nunca
decide se um prompt está pronto, nunca propõe melhoria de conteúdo, nunca escolhe qual modelo
usar. A responsabilidade única é pegar uma decisão já tomada em cada uma dessas dimensões e
produzir o payload concreto que a materializa.