---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## Sistema

`Sistema(id: str, fornecedor: str, modelo: str, fonte_de_dado: str)` — os três últimos campos são
obrigatórios e não vazios (E1); um `Sistema` sem eles não é aceito pelo inventário, o que torna
impossível registrar dependência incompleta por acidente.

## Categoria de capacidade

`categoria: str` — uma classificação livre, mas consistente o suficiente para permitir
agrupamento (por exemplo, "recuperação de conhecimento", "classificação de documento"). É o
campo que `duplicacoes()` usa para comparar sistemas entre si — dois sistemas na mesma categoria,
sem relação declarada, são candidatos a duplicação.

## Decisão de portfólio

`DecisaoDePortfolio(sistemas_envolvidos: tuple[str, ...], consequencia: str, decisao: str)` — o
campo `consequencia` é obrigatório e é o que materializa E2: toda decisão registrada carrega a
razão nomeada que a justificou, nunca uma decisão sem essa âncora.

## Inventário

`Inventario(sistemas: dict[str, Sistema])` — a estrutura central, com os métodos de consulta
(`custo_total_agregado`, `concentracao_por_fornecedor`, `duplicacoes`) descritos em
`11-Implementacao.md` e formalizados em `exemplos/06-enterprise-architecture/inventario.py`.

## Por que não há um campo de "aprovado"

Nenhuma das quatro estruturas carrega um campo booleano de aprovação. Isso é deliberado: E6
estabelece que o inventário registra fato, não avalia mérito — um campo de aprovação embutido no
próprio registro sugeriria que o sistema decide por conta própria se algo é aceitável, quando essa
decisão é sempre humana e vive em `DecisaoDePortfolio`, uma estrutura separada e explícita. A
separação também facilita auditoria: revisar todo o histórico de decisões de portfólio não exige
varrer o inventário inteiro procurando um campo mutado, só consultar a lista de decisões, que
nunca é reescrita — cada decisão é um registro novo, não uma atualização de um registro anterior.
