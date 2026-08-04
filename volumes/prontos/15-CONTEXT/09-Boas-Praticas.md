---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

**Declarar orçamento com margem de segurança abaixo do limite técnico real do modelo**, nunca no
limite exato. Modelos frequentemente reservam parte da janela para a própria resposta gerada —
orçar no limite de entrada sem essa margem produz erro de janela excedida no primeiro uso real.

**Revisar a ordem de prioridade quando o sistema ganha uma nova categoria de conteúdo** (por
exemplo, adicionar resultado de ferramenta a um sistema que antes só tinha histórico e instrução).
Uma categoria nova sem posição definida na prioridade tende a herdar a prioridade mais baixa por
padrão do código, não porque alguém decidiu que deveria ser a menos importante.

**Testar o caminho de descarte com orçamento artificialmente pequeno**, não só com orçamento
generoso o suficiente para nunca pressionar o sistema. Um gestor de orçamento nunca exercitado sob
pressão real pode ter bug de prioridade que só aparece quando o descarte de fato precisa
acontecer.

**Medir o tamanho médio de cada categoria de conteúdo antes de definir a margem de
compactação.** Uma margem calibrada sem esse dado tende a ser arbitrária, ou muito conservadora
(desperdiça espaço útil) ou muito apertada (compactação não tem tempo de operar antes do limite).

**Preferir registrar descarte de forma estruturada (categoria, motivo, timestamp)**, não como
texto livre num log — estrutura permite análise agregada de quais categorias mais sofrem
descarte, texto livre não.
