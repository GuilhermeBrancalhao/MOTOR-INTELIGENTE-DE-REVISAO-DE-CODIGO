---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/22-frontend-architect/painel_ia.py -->

`painel_ia.py`, citado acima, formaliza F1-F6: `RequisicaoDeIA.iniciar` marca estado CARREGANDO
distinto de OCIOSO (F1); `receber_fragmento` acumula incrementalmente em `fragmentos`, nunca
armazena em buffer separado para revelar tudo de uma vez (F2); `resolver_exibicao` nunca retorna
ambiguidade entre fresco e fallback, sempre com `e_fallback` explícito (F3); `promover_para_global`
recusa promoção sem `autorizado=True` (F4); `cancelar` e a checagem de estado CANCELADO em
`receber_fragmento` garantem que fragmento tardio é descartado (F5); `adaptar_resposta_do_provedor`
isola o formato bruto atrás de uma função de tradução (F6).


Todas as transições de estado em `RequisicaoDeIA` são métodos nomeados no imperativo
(`iniciar`, `concluir`, `falhar`, `cancelar`), nunca atribuição direta ao campo `estado` — isso
mantém cada transição como um ponto único onde a lógica de "isso pode acontecer depois de
cancelado?" é decidida uma vez, em vez de espalhada por todo lugar que toca o campo diretamente.

O tipo de retorno `ResultadoExibido | None` de `resolver_exibicao` espelha a escolha já discutida
em `19-DEVOPS` para `artefato_atual`: ausência de resultado exibível (ainda carregando, ou erro
sem fallback) é um estado válido e explícito na assinatura da função, não uma condição excepcional
disfarçada de valor de retorno especial.

`adaptar_resposta_do_provedor` recebe a função de tradução como parâmetro em vez de embuti-la no
exemplo — deliberado, porque o formato real de um provedor específico (OpenAI, Anthropic, ou
qualquer outro) é detalhe de integração que muda conforme o provedor escolhido, enquanto o
princípio de F6 (nunca consumir o bruto diretamente) permanece o mesmo independentemente de qual
provedor está por trás da chamada.