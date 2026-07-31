---
tecnologia: typescript
detectar: ["tsconfig.json", "tsconfig.*.json", "*.tsx"]
papeis: [arquiteto, implementador, testador, revisor]
versao: 2026-07-31
---

## Convenções
- `strict: true` no `tsconfig.json` — é um pacote de verificações (entre elas `strictNullChecks` e `noImplicitAny`), não uma flag isolada; ligar só parte dele é escolha explícita, não omissão.
- Dado de fonte não confiável (resposta de API, `JSON.parse`, entrada de usuário) entra como `unknown`, nunca como `any` — `unknown` obriga a validar/estreitar o tipo antes de usar; `any` desliga a checagem de tipos naquele valor (e em tudo que ele tocar).
- Estreitar tipo (`typeof`, `instanceof`, `in`, type guard próprio) em vez de `as` (type assertion) — `as` é o desenvolvedor afirmando um tipo para o compilador aceitar, não uma conversão verificada em runtime.
- Tipo de união discriminada (um campo literal comum, tipo `kind: "a" | "b"`) para modelar variantes, em vez de vários campos opcionais que só fazem sentido em combinações específicas.

## Armadilhas
- `any` se propaga: uma vez que um valor é `any`, tudo que deriva dele também vira `any` silenciosamente, mesmo em código que parecia tipado.
- `as Tipo` (type assertion) não converte nem valida nada em runtime — só manda o compilador parar de reclamar; se o valor real não bate com o tipo afirmado, o erro estoura mais tarde, longe de onde a asserção foi escrita.
- Tipo estreitado dentro de uma função de callback (arrow function, `.then`, `setTimeout`) pode não ser mantido pelo compilador depois que a variável é reatribuída ou o escopo muda — o TypeScript não rastreia estreitamento através de closures do mesmo jeito que rastreia num bloco linear.
- Interface com todos os campos opcionais (`campo?: T`) aceita `{}` como valor válido, mesmo que o código sempre espere pelo menos um campo preenchido.

## Comandos
- Checar tipos sem gerar saída: `tsc --noEmit`
- Testes (quando o projeto usa Vitest ou Jest): `npm test`

## Checklist de review
- [ ] `strict` está ligado no `tsconfig.json` do projeto (ou o motivo de não estar está documentado).
- [ ] Nenhum `any` novo sem comentário explicando por que o tipo não pôde ser expresso.
- [ ] `as` (type assertion) só aparece onde o tipo já foi validado por outro meio, não como atalho para calar o compilador.
- [ ] Tipo de união usa campo discriminante em vez de vários opcionais soltos.
