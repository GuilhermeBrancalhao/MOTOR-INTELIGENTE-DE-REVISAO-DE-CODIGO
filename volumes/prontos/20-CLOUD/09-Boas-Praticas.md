---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Declarar o alvo de disponibilidade de cada ambiente de forma explícita, mesmo quando o alvo é
"nenhuma redundância exigida" — a ausência de exigência declarada é diferente de exigência
esquecida, e só a primeira é uma decisão consciente.

Revisar a lista de recursos sem dono atribuído com a mesma prioridade que se revisaria uma falha
de segurança — um recurso órfão é, na prática, um recurso que ninguém vai notar quando algo der
errado com ele.

Rodar a detecção de drift (N6) em agenda regular, não apenas quando um problema já é suspeitado —
o valor da detecção está em encontrar divergência antes que ela cause impacto perceptível, não
depois.

Preferir referência a cofre de segredo em vez de qualquer forma de ofuscação de segredo na
própria configuração — ofuscar não é o mesmo que não declarar, e um segredo ofuscado ainda é um
segredo exposto a quem tem acesso ao repositório.


Tratar toda exceção de redundância (um recurso que conscientemente não é redundante, apesar de o
alvo exigir) como uma decisão registrada com prazo de revisão — não uma lacuna que fica aberta
indefinidamente só porque foi identificada uma vez e depois esquecida.

Nomear explicitamente, no próprio registro do recurso, o motivo pelo qual ele não é redundante
quando essa é uma decisão consciente — a ausência de motivo registrado é indistinguível, para
quem audita depois, de uma lacuna simplesmente esquecida.