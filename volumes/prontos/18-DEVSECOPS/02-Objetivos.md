---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Garantir que todo controle declarado em `17-SECURITY` tenha uma verificação automatizada
correspondente, e que a ausência dessa verificação seja visível, não presumida.

Bloquear por padrão a mudança que falha um gate de segurança, com exceção só através de waiver
explícito, nomeado e com prazo de expiração.

Rodar a verificação em toda mudança, não em agenda periódica — o objetivo é prevenir a entrada do
risco, não descobri-lo depois que já entrou.

Preservar o vetor específico que cada controle mitiga na saída do gate, para que uma falha seja
diagnosticável sem precisar consultar outro documento para saber o que ela significa.

Tornar a expiração de uma exceção um evento visível — waiver vencido volta a bloquear, nunca
permanece aberto por omissão.

Estes cinco objetivos formam uma cadeia, não uma lista solta: sem o primeiro (todo controle com
verificação correspondente), o segundo (bloqueio por padrão) não tem o que bloquear de verdade —
um gate que verifica menos controles do que o 17 declara está apenas parcialmente enforçando a
política, mesmo que aprove tudo o que de fato checa. E sem o quarto (rodar em toda mudança), o
terceiro (waiver com prazo) perde sentido, porque uma exceção só existe em relação a uma
verificação que aconteceria de outra forma — se a verificação em si é esporádica, o waiver está
protegendo contra uma checagem que talvez nem rode antes do prazo expirar.

O objetivo final — expiração visível — é o que impede os outros quatro de se degradarem
silenciosamente ao longo do tempo, porque exceção que nunca expira é política que mudou sem
passar pela decisão explícita de mudar.