---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`CasoDeUso` carrega `nivel_de_risco` e `dono_responsavel` como campos obrigatórios —
`RegistroDeCasosDeUso.registrar_caso` recusa um caso sem dono, tornando a responsabilidade
nomeada uma condição de existência do registro, não uma etiqueta adicionada depois.

`registrar_decisao` verifica o nível de risco do caso de uso associado antes de aceitar uma
`DecisaoAutomatizada` — decisão de risco alto ou crítico sem `revisada_por_humano=True` é
recusada, nunca silenciosamente aceita como se a revisão tivesse acontecido.

Toda decisão aceita entra num histórico que nunca é editado ou removido — a trilha de auditoria
(G4) é construída pela mesma disciplina de histórico imutável já vista em outros volumes deste
acervo (`19-DEVOPS`, `27-LLM-ROUTER`): cada entrada é um fato, não um estado mutável.

`RegistroDeCasosDeUso.verificar_pronto_para_producao` recusa um caso sem aprovação explícita
registrada — não existe caminho de código que permita produção sem essa aprovação ter acontecido
antes.


Nenhum desses quatro componentes conhece o mecanismo técnico de defesa do 17-SECURITY — a
governança aqui opera numa camada acima, sobre o caso de uso e a decisão em si, independente de
qual controle técnico de segurança protege a chamada por baixo.

Essa separação de camadas é o que permite auditar cada uma independentemente, sem que uma falha de governança oculte uma falha de segurança técnica, ou vice-versa.