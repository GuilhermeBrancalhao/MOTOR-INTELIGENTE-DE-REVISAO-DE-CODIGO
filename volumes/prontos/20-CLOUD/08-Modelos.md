---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`Recurso` é o modelo central: `nome`, `tipo`, `ambiente`, `dono` e `redundante`. É `frozen=True` e
seu `__post_init__` recusa a própria construção quando `dono` está vazio — a regra N3 não é uma
validação que roda depois de o recurso existir, é uma condição da própria existência do objeto.

`AlvoDeDisponibilidade` liga um nome (por exemplo, "produção crítica") a um booleano
`exige_redundancia` — mantendo a decisão de quanto de redundância um contexto exige separada do
recurso em si, porque o mesmo tipo de recurso pode ter exigência diferente dependendo de onde é
usado.

`PlanoDeInfraestrutura` carrega a lista de recursos declarados e expõe as três operações que as
regras exigem: verificar redundância contra um alvo (N2), aplicar mudança respeitando isolamento
de ambiente (N4), e — através da função livre `detectar_drift` — comparar declarado contra real
(N6).

`Divergencia` carrega o nome do recurso, o campo que diverge, e os dois valores (declarado e
real) lado a lado — não um booleano de "há problema", porque quem recebe a divergência precisa
saber exatamente o que mudou para decidir qual lado corrigir.


Nenhum modelo deste volume representa estado real — todos representam **declaração**. O estado
real só entra na modelagem como um `dict` de entrada para `detectar_drift`, nunca como um tipo
próprio que o sistema gerencia — essa assimetria é proposital: o sistema não controla o real
diretamente, apenas observa e compara contra ele.