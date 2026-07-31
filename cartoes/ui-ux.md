---
tecnologia: ui-ux
detectar: ["**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.html", "**/*.css"]
papeis: [arquiteto, designer, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- Hierarquia antes de ornamento: o que o usuário precisa ver primeiro tem que ser o maior contraste da tela.
- Escala tipográfica limitada (4 a 6 tamanhos) e espaçamento em múltiplos de uma unidade base.
- Estado vazio, estado de carregamento e estado de erro fazem parte da tela — tela só com o caminho feliz está incompleta.
- Cor nunca é o único portador de informação (daltonismo); acompanhe de forma, ícone ou texto.

## Armadilhas
- Contraste abaixo de 4.5:1 em texto de corpo reprova em WCAG AA.
- Alvo de toque menor que 44×44 px é inutilizável em telefone.
- Animação sem `prefers-reduced-motion` causa mal-estar em quem tem sensibilidade vestibular.
- Foco de teclado removido (`outline: none`) sem substituto torna a interface inoperável sem mouse.

## Checklist de review
- [ ] Todo controle é alcançável e visível por teclado.
- [ ] Contraste de texto de corpo ≥ 4.5:1.
- [ ] Estados vazio, carregando e erro existem.
- [ ] Nenhuma informação transmitida só por cor.
