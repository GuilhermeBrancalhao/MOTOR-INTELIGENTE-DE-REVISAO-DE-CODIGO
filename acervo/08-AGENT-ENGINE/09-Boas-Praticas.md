---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 09-Boas-Praticas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Definir orçamento antes de conhecer a complexidade real da tarefa, e revisar depois de
observar execuções reais.** Um orçamento generoso demais no início não é erro — é o ponto de
partida seguro; o ajuste vem de medir quantos passos execuções bem-sucedidas de fato consomem
(ver `14-Metricas.md`), não de estimar de antemão.

**Tratar erro de ferramenta como observação, não como exceção do motor.** Um erro que sobe como
exceção interrompe o loop de forma que o modelo nunca vê o que aconteceu e não tem chance de
tentar outra abordagem — captura e devolução como observação é o que preserva a capacidade do
agente de se recuperar.

**Registrar o critério de sucesso explicitamente quando ele existir**, mesmo que informal — um
objetivo com critério de sucesso permite ao motor rejeitar uma resposta final que não o satisfaz
e devolver ao loop, em vez de aceitar a primeira coisa que o modelo chamar de "pronto".

**Nunca reutilizar o histórico de uma execução encerrada por erro não recuperável como ponto de
partida de uma nova execução sem revisão humana.** O estado que levou ao erro pode se repetir
exatamente, e o motor não tem mecanismo de detectar "isso já falhou assim antes" sem essa
revisão.

**Medir consumo de orçamento por tipo de motivo de encerramento separadamente.** Execuções que
terminam por objetivo atingido consumindo 80% do orçamento típico são um sinal diferente de
execuções que terminam por orçamento excedido consumindo 100% — a primeira sugere orçamento bem
calibrado, a segunda sugere tarefa maior que o orçamento suporta ou loop sem progresso real.

**Validar a resposta do modelo contra o contrato antes de despachar qualquer ferramenta.** Uma
resposta malformada despachada sem validação pode chamar ferramenta com argumento inválido, e o
custo de detectar isso depois (na ferramenta, ou pior, em produção) é maior que validar no
próprio motor, no ponto de entrada do passo.
