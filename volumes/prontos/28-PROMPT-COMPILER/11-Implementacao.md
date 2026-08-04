---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/28-prompt-compiler/compilador.py -->

`compilador.py`, citado acima, formaliza Q1-Q6: `compilar` recusa prompt fora do estado
PROMOVIDO (Q1); a mesma chamada com os mesmos argumentos produz `PayloadCompilado` igual, porque
todos os tipos envolvidos são imutáveis e a lógica é livre de estado externo (Q2);
`OrcamentoExcedido` é levantado após a renderização, comparando tokens estimados contra o
orçamento (Q3); `Dialeto.formatar_mensagens` isola toda formatação específica de provedor (Q4);
`PosicaoDeCacheInvalida` rejeita qualquer posição diferente de `"inicio_estavel"` (Q5);
`VariavelAusente` é levantada antes da renderização, para toda variável declarada sem valor
fornecido (Q6).

`compilar` não mantém nenhum estado entre chamadas — todos os seus efeitos dependem
exclusivamente dos argumentos recebidos, o que é a implementação literal de Q2: sem estado
compartilhado ou variável global influenciando o resultado, a mesma entrada produz sempre a mesma
saída, verificável por comparação direta de valor entre duas execuções.

Essa ausência de estado compartilhado também é o que torna os testes de determinismo (Q2) triviais de escrever — não há necessidade de resetar nenhum contexto global entre chamadas sucessivas.

Isso também simplifica execução paralela de múltiplas compilações, já que nenhuma delas pode
interferir no resultado de outra por meio de estado compartilhado — cada chamada a `compilar` é
inteiramente independente das demais, o que dispensa qualquer mecanismo de sincronização.