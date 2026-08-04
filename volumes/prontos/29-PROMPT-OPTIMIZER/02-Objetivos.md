---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Avaliar toda variante candidata contra exatamente a mesma amostra de casos de ouro usada para
avaliar a versão atual — comparação entre amostras diferentes não prova nada sobre qual versão é
de fato melhor.

Considerar uma variante como candidata a substituir a versão atual apenas quando a melhoria supera
uma margem mínima acima de ruído — nunca tratar uma diferença marginal, dentro da variação
esperada da amostra, como melhoria real.

Nunca promover uma variante automaticamente — a busca propõe, `07-PROMPT-ENGINE` decide se
promove, seguindo a mesma barreira que qualquer versão de prompt, manual ou automática, precisa
atravessar.

Limitar toda busca a um orçamento de tentativas declarado — nunca uma busca aberta sem critério
de parada definido antecipadamente.

Registrar toda tentativa avaliada, mesmo as rejeitadas — o espaço de busca já explorado fica
visível, evitando reexplorar às cegas o que já foi tentado e não funcionou.

Os cinco objetivos existem para conter as duas tentações centrais deste tipo de busca: fazer
parecer que encontrou melhoria sem ter encontrado (O1, O2 protegem contra isso) e pular a
revisão que qualquer mudança de prompt deveria atravessar (O3 protege diretamente). O4 e O5 são
disciplina operacional — sem eles, uma busca real se torna cara ou opaca demais para confiar,
mesmo que as garantias de honestidade estejam corretas.