---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Perseguir cobertura de linha como meta, sem relação com prova de regra.** Viola H1 na essência —
um número de cobertura de linha alto que não prova nada específico é otimização do número errado.

**Conceder exceção de gate repetidamente, sem nunca revisar por que o limiar continua sendo
atingido.** Transforma a exceção (pensada para casos raros e justificados) em rotina disfarçada
de exceção, esvaziando o propósito de H2.

**Dívida técnica mencionada verbalmente em reunião, nunca registrada como item formal.** Viola H3
— sem registro datado, a dívida existe apenas enquanto alguém específico lembrar dela.

**Julgar qualidade do sistema por uma única execução recente da suíte, ignorando tendência.**
Viola H4 — uma medição isolada não tem contexto suficiente para separar ruído de sinal.

**Aceitar uma queda de indicador como "é assim mesmo agora", sem investigar o motivo.** Viola H5
diretamente — normaliza uma regressão sem entender se ela é aceitável ou sintoma de problema real.


**Tratar a taxa de prova por mutação como aprovada permanentemente depois de atingir o limiar uma
vez, sem remedir depois de mudanças no código.** O indicador precisa refletir o estado atual do
sistema, não uma fotografia antiga que já não corresponde ao código real.

Esse tipo de suposição implícita é particularmente perigoso porque parece disciplina — o número foi medido uma vez, então parece que o processo está funcionando, mesmo sem remedição nenhuma depois.