---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Garantir que todo recurso de infraestrutura seja declarado em configuração versionável, nunca
criado apenas através de uma ação manual não registrada.

Garantir redundância para todo recurso que sustenta um alvo de disponibilidade que a exige, sem
exceção implícita — ausência de redundância onde é necessária é uma lacuna visível, não uma
suposição de que "provavelmente está tudo bem".

Atribuir todo recurso a um dono responsável, para que custo e risco de infraestrutura sejam
sempre justificáveis por alguém específico, nunca difusos.

Isolar mudança de infraestrutura por ambiente — uma alteração destinada a staging nunca alcança
produção de forma implícita.

Detectar divergência entre o estado declarado e o estado real da infraestrutura, em vez de
assumir que os dois coincidem só porque a configuração foi aplicada uma vez no passado.

Os cinco objetivos não são independentes: declaração (N1) é o pré-requisito de todos os outros —
não é possível verificar redundância, atribuir dono ou detectar drift de um recurso que nunca foi
declarado formalmente. Isolamento por ambiente (N4) e detecção de drift (N6) se reforçam
mutuamente: um ambiente bem isolado reduz a superfície onde drift pode se originar, e a detecção
de drift é o que confirma que o isolamento está de fato sendo respeitado na prática, não apenas
prescrito.