---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 17-Conclusao
status: RASCUNHO
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

Este volume permanece `RASCUNHO` no front-matter: presumivelmente passa no gate estrutural, não
tem exemplo de código formalmente citado (gate 2 não se aplica ainda, embora a implementação real
exista e seja referenciada em prosa), e não passou pela auditoria do critério 3.
