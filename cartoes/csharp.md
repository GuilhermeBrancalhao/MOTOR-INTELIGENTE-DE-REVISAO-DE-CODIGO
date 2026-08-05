---
tecnologia: csharp
detectar: ["*.csproj", "*.cs"]
papeis: [arquiteto, implementador, testador, revisor]
versao: 2026-08-05
---

## Convencoes
- `nullable` habilitado no projeto (`<Nullable>enable</Nullable>`) para tratar referencia nula como contrato de compilacao.
- Assincronismo fim a fim: metodo que chama operacao de I/O assincrona tambem e assincrono (`async`/`await`), sem bloquear com `.Result` ou `.Wait()`.
- Dependencia por abstracao (`interface`) e injecao de dependencia para servicos de aplicacao; regra de negocio nao depende de infraestrutura concreta.
- DTO de entrada/saida separado de entidade de dominio; entidade nao vira contrato externo da API por padrao.

## Armadilhas
- Capturar `Exception` e seguir sem tratar mascara falha e dificulta diagnostico.
- `async void` fora de handler de evento perde propagacao de erro e nao permite composicao.
- `ToList()`/`AsEnumerable()` cedo demais em consulta faz materializacao prematura e piora performance.
- Repositorio retornando `IQueryable` para fora da camada de dados vaza detalhes de persistencia para camadas de cima.

## Comandos
- Restore + build: `dotnet restore && dotnet build`
- Testes: `dotnet test`

## Checklist de review
- [ ] Projeto com `nullable` habilitado e sem supressao ampla (`!`) sem justificativa.
- [ ] Caminho assincrono nao bloqueia thread com `.Result`/`.Wait()`.
- [ ] Regras de dominio nao dependem de detalhes de infraestrutura.
- [ ] Consultas nao materializam cedo sem necessidade (`ToList` antes da hora).
