---
tecnologia: fsharp
detectar: ["*.fsproj", "*.fs", "*.fsx"]
papeis: [arquiteto, implementador, testador, revisor]
versao: 2026-08-05
---

## Convencoes
- Modelar dominio com tipos algebricos (`record`, `union`) para representar estados validos de forma explicita.
- Preferir funcoes puras e composicao; efeitos colaterais ficam nas bordas (I/O, banco, rede).
- Tratar ausencia e erro com `option` e `Result`, evitando `null` como controle de fluxo.
- Modulos pequenos, com funcoes coesas e assinatura clara; evitar script monolitico.

## Armadilhas
- Usar `failwith` como fluxo normal de dominio dificulta rastreabilidade e testes.
- Misturar mutabilidade (`mutable`) em cadeia de transformacao quebra previsibilidade e dificulta raciocinio.
- Pattern matching incompleto deixa casos sem tratamento e estoura em runtime.
- Conversao apressada para tipos .NET orientados a objeto pode perder garantias do modelo funcional.

## Comandos
- Build: `dotnet build`
- Testes: `dotnet test`

## Checklist de review
- [ ] Estados de dominio criticos representados por `union`/`record`, nao por string solta.
- [ ] Casos de `match` cobrem todas as variantes relevantes.
- [ ] Fluxo de erro explicito com `Result`/`option` em vez de excecao para caminho esperado.
- [ ] Mutabilidade usada so quando necessaria e confinada.
