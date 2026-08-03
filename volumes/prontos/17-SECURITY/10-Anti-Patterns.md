---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Detectar prompt injection por filtro de padrão de texto no dado processado.** Um filtro que
procura frases como "ignore as instruções anteriores" é contornável por paráfrase, tradução, ou
qualquer formulação que o filtro não previu — a defesa robusta é isolamento estrutural de origem,
não reconhecimento de conteúdo suspeito.

**Classificar risco de ação pela intenção declarada de quem solicita, não pela ação em si.**
Confiar que "esta chamada é para fim legítimo porque o operador disse que é" remove a verificação
exatamente no ponto em que ela é mais necessária — a classificação de risco tem que ser função da
ação, verificável independentemente da intenção declarada.

**Corrigir um contorno de segurança específico sem generalizar para a família.** Um patch pontual
para o vetor exato que foi descoberto ("bloquear esta string específica") deixa aberta qualquer
variação não idêntica — o histórico do motor `ENGINE` mostra doze contornos diferentes para a
mesma classe de proibição antes de a abordagem mudar de blocklist para inversão de default.

**Deixar o próprio mecanismo de segurança fora do escopo que ele protege.** Um classificador de
risco que não trava escrita no próprio arquivo de configuração pode ser desligado por uma ação
que ele mesmo classificaria como perigosa se o alvo fosse outro — essa foi a motivação real da
família R9 do motor `ENGINE`.

**Analisar comando de shell gigante por regex em vez de travar por tamanho.** Um comando muito
maior que qualquer uso legítimo esperado é, em si, sinal de anomalia — tentar analisar seu
conteúdo completo por padrão de texto é caro computacionalmente e pode ser explorado como vetor
de negação de serviço contra o próprio classificador.
