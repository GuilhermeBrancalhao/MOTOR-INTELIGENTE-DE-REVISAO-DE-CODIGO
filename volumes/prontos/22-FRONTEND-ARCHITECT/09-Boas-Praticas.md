---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Testar o estado de carregamento de IA visualmente com latência artificialmente alta durante
desenvolvimento — um indicador que parece bom com resposta em 200ms pode se revelar confuso ou
ausente quando a resposta real leva oito segundos.

Tratar cancelamento como caminho de primeira classe no design da interface, não como um caso
extra adicionado depois — perguntar "o que acontece se o usuário sair desta tela agora" durante o
design, não durante a depuração de um bug relatado depois.

Nomear visualmente o estado de fallback de forma que não dependa só de cor ou ícone sutil — texto
explícito ("mostrando resultado anterior") é mais robusto a diferença de percepção entre usuários
do que apenas uma mudança visual discreta.

Manter a camada de adaptação de resposta do provedor (F6) coberta por teste específico sempre que
um novo formato de provedor é adicionado — é o ponto exato onde uma mudança externa não avisada
tem mais chance de quebrar silenciosamente algo na interface.


Registrar, em código de revisão, toda ocorrência de estado promovido a global como um ponto de
atenção explícito — mesmo quando autorizado, é o tipo de decisão arquitetural que vale a pena
revisar com mais cuidado do que uma mudança de escopo puramente local.