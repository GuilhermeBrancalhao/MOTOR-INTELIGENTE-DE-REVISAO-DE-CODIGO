---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-03
---

# Conclusão

Este volume trata segurança de sistema com IA como três categorias de risco estrutural — prompt
injection, exfiltração, execução insegura — cada uma mitigada por um controle verificável, não por
intenção declarada. A decisão central, generalizada do histórico real do motor `ENGINE` deste
próprio repositório, é inverter o default de classificação: comprovadamente inócuo executa,
qualquer outra coisa trava ou é rastreada — porque uma lista de proibições perde, de forma
estruturalmente previsível, contra um espaço de contorno não enumerável.

O que o leitor deve levar embora: doze contornos em sete rodadas de revisão adversarial não são
sinal de que a lista de proibições estava quase completa — são sinal de que listas fechadas não
convergem contra esse tipo de risco, e a mudança de abordagem (não a décima terceira regra) foi
o que resolveu a classe. E proteger o próprio mecanismo de segurança com o mesmo rigor que ele
aplica a outras ações (família R9) não é excesso de cautela — é reconhecer que um sistema de
defesa que não se protege não se protege de fato.

Este volume passa nos quatro critérios da Definição de PRONTO: gate estrutural verde, os 21
testes de `exemplos/17-security` passando, auditoria registrada em
`auditorias/VOL-17-auditoria-2026-08-03.md` e registro datado no `CHANGELOG.md`.
