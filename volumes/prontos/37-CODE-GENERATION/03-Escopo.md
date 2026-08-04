---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a disciplina de geração de código: validação obrigatória, marcação e
imutabilidade manual, reprodutibilidade, revisão humana, versionamento de especificação, e
escopo declarado.

**Fronteira com `28-PROMPT-COMPILER`.** Aquele volume compila prompt em payload para chamar um
modelo; este volume trata do código que uma chamada de IA (ou outra ferramenta determinística)
produz como saída, e da disciplina de validar e integrar esse código ao sistema.

**Fronteira com `35-DOCUMENTATION`.** A disciplina de conteúdo gerado nunca editado manualmente
(W5) já existe naquele volume para documentação — este volume aplica o mesmo princípio
especificamente a código, com a exigência adicional de validação por compilação e teste que
documentação não tem.

**Fronteira com `30-AI-GOVERNANCE`.** Revisão humana obrigatória para decisão de alto risco (G3
daquele volume) é o mesmo princípio geral aplicado aqui de forma mais específica: todo código
gerado que afeta produção é tratado como merecendo revisão humana, sem depender de classificação
de risco caso a caso.

Não cobre a ferramenta específica de geração (modelo de IA, gerador de código a partir de schema)
— os princípios deste volume valem independentemente de qual mecanismo produz o código.


Essas três fronteiras (28, 35, 30/19) evitam que este volume duplique disciplina já estabelecida
em outro lugar do acervo — ele reaproveita a mesma lógica de conteúdo gerado versus manual do 35,
e a mesma exigência de revisão humana do 30, aplicando as duas especificamente ao caso de código
que entra num pipeline de build e teste real.