---
tecnologia: mermaid
detectar: ["*.mmd", "*.mermaid"]
papeis: [arquiteto, documentador]
versao: 2026-07-31
---

## Convenções
- Todo diagrama vem acompanhado de descrição textual ao lado — regra do próprio projeto: quem não consegue processar o diagrama (leitor de tela, texto puro) ainda precisa entender o que ele mostra.
- Nó/label com caractere especial (parênteses, dois-pontos, aspas) vem entre aspas — sem isso o parser pode interpretar o caractere como parte da sintaxe do diagrama, não do texto do nó.
- Um diagrama, um assunto: fluxo de decisão não vira diagrama de sequência com anotação de estado dentro — cada tipo de diagrama (`flowchart`, `sequenceDiagram`, `classDiagram`, etc.) existe para modelar uma coisa.
- Nome de nó curto e estável (`A`, `B`, `ValidaEntrada`); o texto legível vai no label (`A[Valida entrada]`), não no id do nó.

## Armadilhas
- Diagrama que não renderiza quase nunca é bug do Mermaid — é erro de sintaxe (aspas não fechadas, palavra-chave errada, frontmatter com algo além de `---` na primeira linha); revisar a sintaxe antes de assumir limitação da ferramenta.
- Mermaid tem diretivas de acessibilidade próprias (`accTitle`, `accDescr`) que geram `aria-labelledby`/`aria-describedby` no SVG — usar isso não substitui a descrição textual ao lado do diagrama (leitor markdown pode não renderizar o SVG gerado, e sim mostrar só o bloco de código).
- Diagrama grande demais (muitos nós/arestas numa figura só) fica ilegível tanto renderizado quanto como texto-fonte para quem revisa o diff — prefira dividir em diagramas menores e conectados por referência.

## Checklist de review
- [ ] Todo diagrama tem descrição textual ao lado (não só o código-fonte do diagrama).
- [ ] Label com caractere especial está entre aspas.
- [ ] O tipo de diagrama escolhido é o que o Mermaid define para aquele conteúdo (fluxo, sequência, classe, etc.), não um tipo forçado a caber.
- [ ] Diagrama renderiza sem erro antes de ser considerado pronto.
