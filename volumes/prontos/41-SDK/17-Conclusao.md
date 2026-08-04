---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 17-Conclusao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Conclusão

Um SDK é a promessa mais duradoura que um produto faz a quem constrói sobre ele — código de
terceiros compilado ou publicado contra uma versão específica precisa continuar funcionando
exatamente como a convenção de versionamento semântico promete, ou a confiança nessa promessa
desaparece para sempre, não apenas para aquela versão específica. As seis regras deste volume
protegem essa promessa: versão real, superfície deliberada, erro acionável, compatibilidade
garantida, depreciação avisada, exemplo verificado.

A regra mais fácil de violar sob pressão de corrigir algo rápido é AC1 — versionamento semântico
real. "É só uma correção de bug" é a justificativa mais comum para lançar uma mudança que quebra
como versão menor, mas se alguém dependia do comportamento antigo, mesmo incorreto, a mudança
ainda quebra código real — e é exatamente esse código real que a versão maior existe para
proteger com aviso explícito.

A disciplina descrita aqui não é sobre burocracia de processo — é sobre reconhecer que, uma vez
publicado, um SDK carrega uma responsabilidade que o código interno do próprio produto nunca
carrega da mesma forma: alguém fora da organização escreveu código real contra ele, e esse código
continua existindo e rodando independentemente de qualquer decisão futura da equipe que mantém o
SDK.