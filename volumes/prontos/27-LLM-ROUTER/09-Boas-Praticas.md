---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Calibrar `minimo_de_chamadas` e a janela de estabilidade contra o volume real de tráfego da
tarefa — uma tarefa de baixíssimo volume pode levar muito tempo para acumular amostra suficiente,
o que precisa ser considerado ao decidir esses parâmetros.

Expor o histórico de decisões de roteamento como recurso consultável para quem investiga
incidente, não apenas como log interno — a pergunta "por que essa chamada foi para o fallback"
deveria ter resposta rápida.

Testar o comportamento de flapping deliberadamente, alternando sinal saudável e degradado em
sequência controlada, para confirmar que a janela de estabilidade de fato previne oscilação
antes de confiar no roteador em produção.

Revisar os limiares de degradação periodicamente contra o comportamento real observado — um
limiar calibrado para um padrão de tráfego antigo pode não fazer mais sentido conforme o volume
ou o perfil de latência muda.


Registrar não apenas a decisão de roteamento, mas o valor do sinal de saúde que a motivou —
"fallback_por_degradacao" sozinho é menos útil para investigação do que a mesma informação
acompanhada da taxa de falha e latência que de fato dispararam a transição.

Esse detalhe adicional custa pouco para registrar e economiza tempo de investigação considerável quando alguém precisa entender, meses depois, por que uma troca específica aconteceu.