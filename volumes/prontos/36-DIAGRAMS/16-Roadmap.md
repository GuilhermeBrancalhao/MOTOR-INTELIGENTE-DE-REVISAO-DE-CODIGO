---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Verificação automática de sintaxe Mermaid válida antes de aceitar um diagrama no catálogo — hoje
a validação é sobre metadado (tipo, prosa, escopo), não sobre a sintaxe do diagrama em si.

Extração automática de diagrama desatualizado a partir de mudança de código detectada — hoje a
vigência (X4) é verificada manualmente, sem gatilho automático quando o componente representado
muda.

Convenção de nomenclatura de nó e aresta dentro de cada tipo (por exemplo, como nomear estado em
`stateDiagram-v2` de forma consistente entre volumes) — hoje o catálogo trata de tipo, não de
convenção detalhada de nomenclatura interna.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (tipo catalogado, entrada com prosa e escopo, escolha
por necessidade, vigência), testado por mutação nas seis regras. Depois, integração real como
referência para os volumes ENGINE e ARQUITETURA deste acervo que já usam os quatro tipos.

## O que este volume assume que pode mudar

O conjunto fechado de quatro tipos é o mínimo suficiente hoje — um quinto tipo pode ser
necessário se um propósito genuinamente não coberto pelos quatro existentes aparecer, sem
alterar o princípio central de catalogação disciplinada com propósito declarado.
