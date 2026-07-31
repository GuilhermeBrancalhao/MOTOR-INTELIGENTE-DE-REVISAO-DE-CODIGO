---
tecnologia: react
detectar: ["*.jsx", "*.tsx"]
papeis: [arquiteto, implementador, designer, testador, revisor]
versao: 2026-07-31
---

## Convenções
- Estado que pode ser calculado a partir de props/outro estado durante a renderização não vira `useState` próprio — é derivado na hora, senão os dois podem ficar dessincronizados.
- Lista renderizada com `.map` sempre tem `key` estável e única por item (o id do dado, não o índice do array).
- Efeito (`useEffect`) só existe para sincronizar com algo fora do React (rede, DOM, subscription); lógica que só depende de props/estado do próprio componente roda direto no corpo da função, sem efeito.
- Componente que só apresenta dado recebido por prop fica sem estado próprio (componente "burro"); estado e orquestração ficam no componente de cima.

## Armadilhas
- `useEffect`/`useCallback`/`useMemo` com array de dependências incompleto captura valores antigos (closure obsoleta) — o efeito roda com a versão da variável de quando foi criado, não a atual.
- `key={index}` numa lista que pode reordenar, filtrar ou ter item removido do meio faz o React reaproveitar o elemento de DOM errado para a linha errada — estado interno do item (um input não controlado, por exemplo) migra para a linha vizinha.
- Chamar `setState` dentro do corpo do componente sem condição de guarda gera loop de renderização infinito.
- Mutar o array/objeto de estado diretamente (`state.push(x)` ao invés de `setState([...state, x])`) não dispara nova renderização, porque a referência não mudou.

## Comandos
- Testes (quando o projeto usa Vitest ou Jest): `npm test`
- Lint: `npm run lint`

## Checklist de review
- [ ] Array de dependências de `useEffect`/`useCallback`/`useMemo` cobre tudo que a função usa de fora.
- [ ] Nenhuma lista usa o índice como `key` quando a lista pode reordenar ou perder itens do meio.
- [ ] Nenhum estado é mutado diretamente; toda atualização passa por `set...` com valor novo.
- [ ] Estado derivável de props/outro estado não virou `useState` separado.
