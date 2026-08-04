---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Introdução

Um SDK é o contrato mais difícil de quebrar sem aviso — diferente de um endpoint de API, que pelo
menos exige uma nova requisição para revelar mudança, código cliente escrito contra um SDK
compila (ou não) e falha (ou não) silenciosamente dependendo de como a mudança foi versionada.
Uma mudança que quebra compatibilidade lançada como versão menor engana quem confiou no
significado usual de versionamento semântico, e o dano só aparece quando o código do cliente já
está em produção.

Este volume trata da disciplina de manter um SDK confiável para desenvolvedor externo: versão
semântica real (mudança que quebra sempre exige versão maior), superfície pública mínima e
deliberada, erro que orienta correção, compatibilidade retroativa garantida dentro da mesma
versão maior, depreciação explícita antes de remoção, e exemplo de uso sempre verificado contra o
código real do SDK.

`25-API-ARCHITECT` já trata do contrato exposto ao cliente em geral — versionamento, tradução,
erro consistente. Este volume aplica princípio semelhante especificamente ao SDK empacotado: uma
biblioteca instalada e importada diretamente no código de terceiros, onde a superfície pública
exposta é o próprio código-fonte da biblioteca, não apenas um contrato de rede.

Um exemplo concreto ilustra o custo de errar essa disciplina: uma biblioteca de terceiros que
remove um parâmetro obrigatório de uma função pública, lançando isso como uma versão de correção
de bug em vez de uma versão maior, quebra silenciosamente todo código cliente que ainda chamava
essa função da forma antiga — o erro só aparece em produção, meses depois, distante do commit
que causou o problema real.