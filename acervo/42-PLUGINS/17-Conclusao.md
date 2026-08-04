---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 17-Conclusao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Conclusão

Um plugin é a forma mais íntima de código de terceiro que um sistema pode hospedar — mais íntima
que um SDK, porque roda dentro do próprio processo do host, não apenas ao lado dele. Essa
intimidade é exatamente o motivo pelo qual isolamento de falha e permissão declarada não são
detalhes de implementação opcionais aqui: sem eles, cada plugin instalado é um risco silencioso
para todo usuário do host, não apenas para quem escolheu instalar aquele plugin específico.

A regra mais fácil de negligenciar sob pressão de lançar rápido é AD2 — isolamento de falha.
"O plugin já foi testado, não deveria falhar" é a justificativa mais comum para pular a camada de
captura de exceção, mas é exatamente o plugin não testado o suficiente, publicado por alguém fora
do controle do host, que essa camada existe para conter antes que derrube todo o resto.

As seis regras deste volume — contrato versionado, isolamento de falha, permissão declarada,
registro explícito, desativação sem resíduo, evolução disciplinada do contrato — formam juntas o
que separa um ecossistema de plugin confiável de um mero mecanismo de carregar código arbitrário
de terceiro e esperar que funcione.