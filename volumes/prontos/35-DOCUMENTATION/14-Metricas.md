---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de decisões arquiteturais significativas com ADR registrado.** Deveria tender a 100%
— uma queda indica decisões importantes acontecendo fora do processo de registro.

**Número de ADRs superados por novo ADR, versus editados diretamente (se detectável).** Deveria
ser 100% substituição, 0% edição direta — qualquer edição direta indica violação de W2.

**Proporção de documentação com verificação de vigência automatizada versus dependente de
revisão manual esporádica.** Um número baixo de automação é sinal de risco de desatualização
silenciosa.

**Frequência de documento desatualizado detectado e corrigido, por área do sistema.** Áreas com
alta frequência de mudança podem precisar de verificação de vigência mais frequente que áreas
estáveis.


Estas quatro métricas, lidas em conjunto, revelam se a disciplina de documentação está sendo
seguida na prática — alta proporção de decisão registrada e zero edição direta detectada são os
dois sinais mais diretos de que o processo está funcionando como projetado, não apenas existindo
como intenção documentada em algum lugar.

Qualquer desvio persistente entre essas quatro métricas e o comportamento esperado merece investigação antes de ser aceito como novo padrão silencioso.

Nenhuma delas deveria ser lida como julgamento definitivo isolado, sempre como parte de um quadro mais amplo sobre a saúde do processo de documentação ao longo do tempo.