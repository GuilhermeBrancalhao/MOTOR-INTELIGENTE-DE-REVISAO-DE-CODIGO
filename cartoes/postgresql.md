---
tecnologia: postgresql
detectar: ["postgresql.conf", "pg_hba.conf", "pg_ident.conf", ".pgpass"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- Toda coluna usada em `WHERE`, `JOIN` ou `ORDER BY` com frequência tem índice — e a decisão vem de olhar o plano (`EXPLAIN`), não de suposição.
- Migração que altera tabela grande em produção evita reescrever a tabela inteira de uma vez (adicionar coluna `NOT NULL` sem default, por exemplo); prefira passos que não bloqueiam a tabela por muito tempo.
- Transação só fica aberta pelo tempo da unidade de trabalho — nunca aberta esperando input do usuário ou uma chamada de rede.
- Nome de tabela e coluna em `snake_case`, minúsculo — identificador com maiúscula sem aspas o Postgres já dobra para minúsculo, então misturar caixa convida a confusão entre o nome escrito e o nome real.

## Armadilhas
- `WHERE coluna NOT IN (subquery ou lista)` não devolve nenhuma linha se **qualquer** valor da lista/subquery for `NULL` — a comparação com `NULL` avalia para desconhecido, e isso contamina o `AND` implícito do `NOT IN` inteiro. Use `NOT EXISTS` quando a lista pode conter `NULL`.
- `EXPLAIN` sozinho mostra o plano estimado (sem rodar a query); só `EXPLAIN ANALYZE` roda de fato e mostra tempo e linhas reais — os dois podem divergir bastante quando a estatística da tabela está desatualizada.
- Transação aberta e esquecida (`idle in transaction`) segura o `VACUUM` de limpar linhas mortas na tabela inteira, não só na linha que a transação tocou — isso incha tabela e índice para todo mundo, não só para quem esqueceu a transação aberta.
- `DELETE`/`UPDATE` sem `WHERE` afeta a tabela inteira; sem transação em volta (ou com autocommit ligado), não tem como desfazer depois de rodar.

## Comandos
- Plano de execução real: `EXPLAIN ANALYZE <query>;`
- Cliente interativo: `psql -d <banco>`

## Checklist de review
- [ ] Nenhum `NOT IN` sobre coluna/subquery que pode conter `NULL` sem ser `NOT EXISTS`.
- [ ] Toda migração em tabela grande foi pensada em passos que não travam a tabela por muito tempo.
- [ ] Nenhuma transação fica aberta esperando I/O externo.
- [ ] Consulta lenta foi investigada com `EXPLAIN ANALYZE`, não só suposição de índice faltando.
