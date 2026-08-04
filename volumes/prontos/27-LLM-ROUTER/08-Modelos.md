---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`SinalDeSaude` carrega totais agregados (`total_chamadas`, `falhas`, `latencia_media_ms`), não
uma lista de chamadas individuais — o roteador julga tendência, não evento isolado, e um sinal
agregado já expressa isso na própria forma do tipo.

`JanelaDeSaude` carrega os limiares (`limiar_taxa_falha`, `limiar_latencia_ms`,
`minimo_de_chamadas`) como configuração explícita do próprio objeto, não como constante de
módulo — um roteador real pode ter janelas diferentes por tarefa, e o tipo permite isso sem
alterar a lógica de decisão em si.

`DecisaoDeRoteamento` carrega `motivo` como string categorizada, não apenas o nome do candidato
escolhido — a razão da escolha é tão parte do resultado quanto o próprio candidato, porque é o
que torna a decisão auditável depois (L3).


Nenhum desses três tipos (`SinalDeSaude`, `JanelaDeSaude`, `DecisaoDeRoteamento`) referencia
diretamente um provedor ou modelo específico — todos operam sobre valores agregados e nomes de
candidato como string, mantendo o modelo central livre de acoplamento a qualquer fornecedor
particular, o que é consistente com a regra de volume perecível deste grupo.

Essa neutralidade de fornecedor no próprio tipo é o que permite reutilizar a mesma lógica de roteamento independente de qual conjunto de provedores está em jogo em um momento específico.

Cada um dos três permanece útil mesmo se o conjunto de fornecedores em uso mudar completamente amanhã.