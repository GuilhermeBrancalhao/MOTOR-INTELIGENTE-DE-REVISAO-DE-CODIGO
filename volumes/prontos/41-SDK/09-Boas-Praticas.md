---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 09-Boas-Praticas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Boas Práticas

Anunciar depreciação com antecedência suficiente para que consumidores reais do SDK tenham tempo
de migrar antes da próxima versão maior remover o elemento — o tempo exato depende do ritmo de
release, mas nunca deveria ser tão curto que a migração vire urgência inesperada.

Escrever mensagem de erro do SDK pensando em alguém que nunca leu o código-fonte da biblioteca —
"como corrigir" deveria ser acionável só com a informação que a mensagem já carrega, sem exigir
investigação adicional no repositório do SDK.

Rodar todo exemplo de documentação como parte da suíte de teste automatizada do próprio SDK, não
apenas revisado manualmente uma vez — a única forma confiável de garantir que exemplo não diverge
do comportamento real é executá-lo de fato contra o código atual.

Revisar a superfície pública periodicamente em busca de elemento exposto sem uso real conhecido —
um elemento público nunca usado por ninguém pode ser candidato a depreciação, reduzindo a
superfície que precisa ser mantida compatível para sempre.

Manter um arquivo de changelog dedicado à evolução da superfície pública, separado do changelog
geral do produto, para que o desenvolvedor externo encontre rapidamente apenas o que afeta o
código que ele escreveu contra o SDK, sem precisar filtrar mudança interna irrelevante para
quem consome a biblioteca de fora.