---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 11-Implementacao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/41-sdk/sdk.py -->

`sdk.py`, citado acima, formaliza AC1-AC6: `validar_release` recusa mudança que quebra
compatibilidade sem incremento de versão maior (AC1); `MembroDeSDK.__post_init__` recusa membro
público sem justificativa (AC2); `ErroDoSDK.__post_init__` recusa erro sem orientação de
correção (AC3); `SuperficieDoSDK.remover_membro` recusa remoção de membro público sem
depreciação prévia e sem incremento de versão maior (AC4/AC5 combinados);
`aceitar_exemplo` recusa `ExemploDeUso` sem `resultado_verificado=True` (AC6).

`SuperficieDoSDK.remover_membro` é o ponto único onde AC1, AC4 e AC5 se encontram — a mesma
chamada verifica simultaneamente se o membro já foi depreciado e se a versão proposta de fato
incrementa o número maior, recusando a operação se qualquer uma das duas condições faltar, em vez
de espalhar essa verificação combinada por múltiplos pontos separados do código que poderiam
divergir entre si ao longo do tempo.

Nenhuma parte do módulo depende de biblioteca externa de empacotamento ou de sistema real de
distribuição de pacote — todas as seis regras são provadas sobre dataclasses e funções Python
puras, suficientes para demonstrar o princípio sem o custo de configurar um ambiente de
publicação de pacote real apenas para rodar a suíte de teste deste volume.

`validar_release` e `SuperficieDoSDK.remover_membro` compartilham a mesma exceção
`VersionamentoIncorreto` para o caso de versão maior ausente — a reutilização deixa explícito que
as duas situações (release direto e remoção de membro) são, na prática, a mesma regra de
negócio aplicada em dois pontos de entrada diferentes do módulo.