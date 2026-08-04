---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

A diferença entre uma interface que trata bem uma chamada de IA e uma que apenas reaproveita o
padrão de uma chamada CRUD comum não está em nenhum detalhe visual sofisticado — está em
reconhecer que a latência é maior e mais variável, que a resposta pode chegar incrementalmente, e
que a falha pode acontecer de formas menos previsíveis. As seis regras deste volume convergem
para uma ideia central: o usuário deveria sempre conseguir distinguir entre "ainda carregando",
"resposta fresca", "fallback de dado anterior" e "falhou" — e nenhum desses quatro estados
deveria ser confundido com outro por economia de esforço de implementação.

A regra mais fácil de negligenciar sob pressão de prazo é F5 — cancelamento de requisição
abandonada. Parece uma otimização opcional até o momento em que um fragmento tardio de uma
requisição já esquecida atualiza um componente que o usuário nem está mais vendo, produzindo um
bug que só aparece sob condição de corrida específica e é desproporcionalmente difícil de
reproduzir depois.
