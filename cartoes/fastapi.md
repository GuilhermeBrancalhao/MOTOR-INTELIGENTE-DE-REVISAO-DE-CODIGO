---
tecnologia: fastapi
detectar: ["routers/*.py", "**/routers/*.py"]
papeis: [arquiteto, implementador, testador, revisor]
versao: 2026-07-31
---

## Convenções
- Rota que só faz I/O (chamada a banco, HTTP, arquivo) é `async def`; rota com trabalho de CPU síncrono pode ficar `def` — nesse caso o FastAPI já roda a função num threadpool por fora.
- Todo endpoint declara `response_model` (ou o retorno tipado): além de documentar o contrato no OpenAPI, o Pydantic filtra do JSON de saída qualquer campo que não esteja no modelo.
- Regra de negócio compartilhada entra por `Depends(...)` (injeção de dependência), não repetida dentro de cada rota.
- Modelo de entrada e modelo de saída são classes Pydantic separadas — nunca o mesmo modelo do banco reaproveitado como schema de request/response.

## Armadilhas
- `async def` que chama código bloqueante sem `await` (uma lib sem suporte a async, um `time.sleep`) trava o event loop inteiro — todas as outras requisições esperam. Se a chamada é bloqueante, ou ela roda em threadpool (`run_in_threadpool`/`run_in_executor`) ou a rota é `def` puro, nunca `async def` sem `await`.
- `response_model` filtra o JSON de saída, mas não impede que o objeto retornado internamente carregue o campo sensível (senha, hash, id interno) até ali — quem lê o código sem saber do filtro assume que o campo nunca existiu.
- Dependência com `yield` (setup/teardown, ex.: sessão de banco) só roda o código depois do `yield` se a rota de fato terminar; exceção não tratada na rota ainda executa o teardown, mas um `os._exit` ou crash do processo não.

## Comandos
- Subir localmente: `uvicorn main:app --reload`
- Testes: `python -m pytest -q` (via `TestClient`/`httpx.AsyncClient`)

## Checklist de review
- [ ] Toda rota `async def` só chama código que também é `async` (ou passa por threadpool explicitamente).
- [ ] Toda rota declara `response_model` ou retorno tipado.
- [ ] Modelo de request e de resposta são classes Pydantic distintas do modelo de persistência.
- [ ] Dependência com `yield` tem o teardown coberto por teste (inclusive no caminho de exceção).
