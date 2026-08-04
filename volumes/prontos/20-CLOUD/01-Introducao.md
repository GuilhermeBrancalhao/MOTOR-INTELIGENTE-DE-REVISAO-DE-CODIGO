---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

A infraestrutura que hospeda um sistema em execução — computação, rede, armazenamento — é
frequentemente tratada como um detalhe de operação, algo que "só precisa funcionar" enquanto a
atenção vai para o código da aplicação. Essa suposição falha de formas específicas e recorrentes:
um recurso provisionado manualmente pelo console, sem registro declarativo, não pode ser
reproduzido nem auditado; um serviço crítico sem redundância é um ponto único de falha esperando
o momento errado para falhar; um custo sem dono atribuído nunca é questionado, porque ninguém tem
a responsabilidade explícita de justificá-lo.

Este volume trata da infraestrutura como algo que precisa das mesmas garantias que se exige do
código que roda sobre ela: declarada em texto versionável, não clicada em existência; redundante
onde a disponibilidade exige; com custo atribuível a um dono; e com estado real verificável contra
o que foi declarado, porque divergência silenciosa entre os dois é o início de praticamente todo
incidente de infraestrutura que "não deveria ter acontecido".

`19-DEVOPS` define como uma mudança chega até esta infraestrutura; este volume define a
infraestrutura em si — como ela é declarada, como sua disponibilidade é garantida, e como
divergência entre o que foi declarado e o que está de fato provisionado é detectada antes de virar
incidente.
