---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 09-Boas-Praticas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Conciliar diariamente, não em lote no fim do mês.** Um resíduo de um centavo descoberto no dia
seguinte custa uma consulta; o mesmo resíduo descoberto trinta dias depois, misturado com outros
vinte novos, custa uma investigação inteira. O motor deste volume é barato o bastante para rodar
todo dia — nenhuma das cinco funções faz chamada de rede.

**Tratar a ausência de evidência como degradação, nunca como erro.** Quando uma fonte de
histórico não está disponível (ambiente sem acesso a dado de terceiro, por exemplo), o padrão
correto — implementado em `classificar()` — é a confiança cair para o nível que a evidência
restante sustenta, nunca lançar exceção nem travar o processamento inteiro. Mais itens caem em
revisão humana, e isso é seguro; nenhum item é escrito com confiança inflada.

**Separar puramente a decisão da persistência.** `casar()`, `classificar()` e `achar_ancora()`
não escrevem nada — devolvem uma resposta. Só `trilha.registrar()` e `guarda.registrar()` têm
efeito colateral, e ambos são explícitos, chamados depois que a decisão já foi tomada. Essa
separação é o que torna os cinco módulos testáveis sem mock de rede ou banco de dados.

**Normalizar antes de comparar, sempre.** Nome de contraparte com capitalização diferente ou
espaço nas pontas não pode virar duas chaves diferentes na guarda, nem dois candidatos
diferentes no casamento. `ChaveMovimento.normalizada()` e `_tokens()` em `casamento.py` existem
por esse motivo específico.

**Tratar toda transição para pendência humana como sucesso do desenho, não como falha.** Um
motor que nunca produz pendência não é mais preciso — é mais permissivo, e permissivo demais é
o que causa escrita errada. A métrica que importa não é "quantos itens o motor escreveu", é
"quantos itens o motor escreveu errado" — que deveria ser zero por construção, coberto em
`14-Metricas.md`.

**Testar a ordem de chamada, não só cada módulo isolado.** `test_fluxo_completo.py` existe
porque a composição correta dos cinco módulos é, em si, um comportamento que pode quebrar mesmo
com cada módulo individualmente correto — por exemplo, se alguém invertesse a ordem de guarda e
trilha, cada teste unitário continuaria verde.
