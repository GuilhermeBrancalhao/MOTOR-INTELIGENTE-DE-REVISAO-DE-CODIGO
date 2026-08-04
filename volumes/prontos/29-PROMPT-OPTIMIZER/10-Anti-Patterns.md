---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Otimizador que promove diretamente a variante vencedora, pulando o fluxo do 07.** Viola O3 —
mesmo uma variante genuinamente melhor não deveria entrar em produção sem passar pela mesma
barreira que qualquer outra versão atravessa.

**Ajustar os casos de ouro durante a busca para que uma variante já encontrada passe a pontuar
melhor.** Viola O6 diretamente — é uma forma de trapacear a própria avaliação, tornando o
resultado da busca sem sentido.

**Aceitar qualquer variante com taxa de acerto numericamente maior, sem margem mínima acima do
baseline.** Viola O2 — confunde ruído de amostra pequena com melhoria real, e pode substituir uma
versão estável por outra estatisticamente indistinguível.

**Busca sem limite de tentativas, rodando até esgotar o gerador de candidatos, seja qual for o
tamanho.** Viola O4 — o custo de avaliação (cada chamada a `avaliar_variante` normalmente envolve
uma chamada de modelo real) precisa de um teto declarado.

**Descartar tentativas rejeitadas sem registrar, mantendo só o resultado vencedor.** Viola O5 —
perde visibilidade sobre o que já foi tentado, arriscando reexploração cega do mesmo espaço em
buscas futuras.


**Reduzir o limiar de melhoria mínima especificamente para fazer um candidato específico passar,
depois de já ver o resultado.** Tecnicamente não altera os casos de ouro (O6), mas produz o mesmo
efeito prático — ajusta o critério de sucesso depois de já saber a resposta.