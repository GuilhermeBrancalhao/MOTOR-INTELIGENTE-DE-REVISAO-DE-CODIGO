---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Registrar toda decisão arquitetural com consequência duradoura como ADR — contexto, decisão e
consequência explícitos — nunca deixada como julgamento implícito que só existe na memória de
quem decidiu.

Nunca apagar ou reescrever um ADR aceito — uma decisão que muda é registrada como um novo ADR
que substitui o anterior, preservando o contexto original em vez de apagá-lo.

Manter documentação versionada junto do código que ela descreve, nunca em sistema desconectado do
histórico de mudança que altera esse código.

Detectar explicitamente quando documentação deixa de corresponder ao código real — nunca assumir
que documentação permanece correta automaticamente com o tempo.

Marcar conteúdo gerado automaticamente de uma fonte de verdade única como tal, e nunca editá-lo
manualmente — uma edição manual em conteúdo gerado é sobrescrita silenciosamente na próxima
geração, criando falsa confiança de que a mudança persistiu.

Os cinco objetivos protegem contra cinco formas específicas de perda de conhecimento: decisão sem
registro (primeiro) perde o motivo; registro apagado (segundo) perde a história; documentação
desconectada do código (terceiro) perde rastreabilidade; vigência não verificada (quarto) perde
confiabilidade; e edição manual sobre conteúdo gerado (quinto) perde a própria mudança feita, sem
que quem a fez perceba a perda até tarde demais.

Nenhum desses cinco riscos é exclusivo de sistema com IA, mas todos se tornam mais caros num contexto onde decisões tecnicas evoluem rapidamente e a rotatividade de conhecimento é alta.