---
tecnologia: vbnet
detectar: ["*.vbproj", "*.vb"]
papeis: [arquiteto, implementador, testador, revisor]
versao: 2026-08-05
---

## Convencoes
- `Option Strict On` e `Option Explicit On` no projeto para evitar conversao implicita arriscada e variavel sem declaracao.
- Separar camada de dominio/aplicacao de infraestrutura; codigo de UI e acesso a dados nao concentra regra de negocio.
- Preferir metodos com responsabilidade unica e nomes descritivos (`PascalCase`), evitando modulos com funcoes grandes e acopladas.
- Validacao de entrada na borda (API/UI/importacao), deixando o nucleo do dominio operar com invariantes ja garantidos.

## Armadilhas
- `On Error Resume Next` engole erro e continua com estado inconsistente.
- Conversoes implicitas com `Option Strict Off` mudam comportamento em runtime sem aviso do compilador.
- Dependencia direta de `DataTable`/`DataRow` no dominio acopla regra de negocio ao formato de transporte.
- Metodo `Async` sem `Await` executa sincrono e pode passar falsa impressao de nao bloqueio.

## Comandos
- Build: `dotnet build`
- Testes: `dotnet test`

## Checklist de review
- [ ] `Option Strict On` e `Option Explicit On` ativos.
- [ ] Nenhum `On Error Resume Next` novo em codigo de producao.
- [ ] Regra de negocio desacoplada de UI e de estrutura tabular (`DataTable`).
- [ ] Metodos `Async` tem `Await` real no fluxo de I/O.
