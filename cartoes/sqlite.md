---
tecnologia: sqlite
detectar: ["*.sqlite", "*.sqlite3", "*.db"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- Chave estrangeira declarada na tabela existe para documentar a relação, mas só é **aplicada** se `PRAGMA foreign_keys = ON` for ligado na conexão — ligar isso é parte da abertura de conexão, não opcional.
- Coluna com tipo declarado (`INTEGER`, `TEXT`) é uma dica de afinidade, não uma trava — SQLite aceita gravar um valor de outro tipo na mesma coluna; se o código depende do tipo, valide na aplicação.
- Uma conexão por vez para escrita quando o volume de escrita concorrente é baixo; para concorrência real, considerar `PRAGMA journal_mode = WAL` (permite um escritor e vários leitores ao mesmo tempo).
- Caminho do arquivo `.db`/`.sqlite` fica fora do controle de versão (dado, não código) — só o schema/migração entra no repositório.

## Armadilhas
- `PRAGMA foreign_keys` vem **desligado por padrão** em cada nova conexão — se o código assume que a integridade referencial está sendo aplicada só porque a tabela declarou `FOREIGN KEY`, está enganado até ligar o pragma explicitamente naquela conexão.
- Tipagem dinâmica (afinidade de coluna, não tipo estrito) deixa passar sem erro uma escrita de tipo errado numa coluna — um bug de conversão só aparece quando alguém lê o valor esperando o tipo declarado.
- Escrita concorrente de duas conexões ao mesmo tempo, fora do modo WAL, trava o banco inteiro para a segunda escrita (`database is locked`) — não é um erro de dado, é o modelo de concorrência do SQLite (um escritor por vez).
- `:memory:` ou banco temporário perde tudo ao fechar a conexão; usar isso em teste sem perceber que é também o comportamento em produção é fonte de bug de "sumiu o dado depois do restart".

## Comandos
- Cliente interativo: `sqlite3 arquivo.db`
- Ver o schema: `sqlite3 arquivo.db ".schema"`

## Checklist de review
- [ ] Toda conexão que grava liga `PRAGMA foreign_keys = ON` explicitamente, se a integridade referencial importa.
- [ ] Nenhum código assume tipo de coluna sem validar o valor lido.
- [ ] Escrita concorrente de múltiplas conexões foi pensada (WAL, fila, ou serialização) — não ignorada até o erro `database is locked` aparecer.
- [ ] Banco de dado (`.db`/`.sqlite`) não está versionado junto com o código.
