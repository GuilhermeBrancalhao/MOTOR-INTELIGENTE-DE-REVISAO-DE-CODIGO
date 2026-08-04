---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Compilar prompt em rascunho "só para testar rápido em produção".** Viola Q1 diretamente — o
prompt nunca passou pela barra de avaliação do 07, e usar seu payload em chamada real é
exatamente o risco que a máquina de estados do 07 existe para prevenir.

**Truncar silenciosamente o conteúdo quando o payload excede o orçamento.** Viola Q3 — a
alternativa correta é falhar explicitamente, nunca enviar um payload cortado que pode ter perdido
justamente a parte mais importante da instrução.

**Condicional de provedor espalhada por várias partes do código de compilação.** Viola Q4 — torna
impossível trocar ou adicionar um provedor sem caçar cada lugar que precisa de ajuste.

**Variável ausente substituída por string vazia sem erro.** Viola Q6 — o payload compilado parece
válido estruturalmente, mas carrega uma lacuna de conteúdo que só é percebida quando a resposta do
provedor já não faz sentido.

**Ponto de cache posicionado dentro de conteúdo gerado dinamicamente a cada chamada.** Viola Q5 —
desperdiça completamente a vantagem que o cache deveria oferecer, sem nenhum ganho correspondente.


**Ignorar o erro de orçamento excedido e enviar a chamada mesmo assim "para ver o que acontece".**
Contorna Q3 completamente e transfere o risco de falha para o momento da chamada real, quando o
custo de descobrir o problema já é maior.