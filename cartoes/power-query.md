---
tecnologia: power-query
detectar: ["*.pq", "*.pqm", "*.mez"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- M é sensível a maiúsculas/minúsculas em tudo — nome de função (`Table.SelectRows`, nunca `table.selectrows`), nome de variável e até valor de texto (`"Foo"` ≠ `"foo"`).
- Nome de passo com espaço precisa do identificador com `#` e aspas: `#"Nome do Passo"`.
- Um passo por transformação, com nome descritivo (renomear o passo automático `Custom1`/`Changed Type1` para o que ele realmente faz) — a lista de passos é a documentação da consulta.
- Consulta que só prepara dados para outra (staging) fica com carregamento desligado ("Habilitar carregamento" desmarcado), em vez de subir uma tabela intermediária inútil para a planilha/modelo.

## Armadilhas
- O passo "Changed Type" gerado automaticamente embute a cultura/locale da máquina que criou a consulta (datas e números são interpretados nesse formato); abrir o mesmo arquivo numa máquina com região diferente, ou compartilhar com alguém de outro país, pode reinterpretar a data errado ou quebrar o passo.
- Passo renomeado ou removido no meio da lista pode derrubar um passo posterior que referencia esse nome (`#"Nome Antigo"`) diretamente na fórmula — a referência não é atualizada sozinha.
- Transformação que impede "query folding" (empurrar o trabalho para a fonte, ex.: SQL) força o Power Query a trazer todos os dados brutos para processar localmente; inserir uma coluna customizada ou um filtro complexo cedo na cadeia de passos pode quebrar o folding dos passos seguintes.

## Checklist de review
- [ ] Nenhum identificador ou valor de texto depende de diferença de maiúscula/minúscula por acidente.
- [ ] Passos têm nome descritivo, não o nome automático genérico.
- [ ] "Changed Type" de coluna de data/hora usa "Usando Local" quando a consulta pode rodar em outra região.
- [ ] Consultas que só existem para alimentar outra estão com carregamento desabilitado.
