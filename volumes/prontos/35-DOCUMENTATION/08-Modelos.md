---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`ADR` é imutável (`frozen=True`) — a única forma de "mudar" um ADR é criar um novo com
`supersede` apontando para o anterior, nunca alterar campos de um ADR existente. Essa
imutabilidade é a implementação estrutural direta de W2.

`Documento` carrega `publico_alvo` como valor restrito a `"USUARIO"` ou `"MANTENEDOR"` — não
existe terceiro valor que tente servir os dois públicos ao mesmo tempo, o que é a materialização
de W6 no próprio tipo.

`RegistroDeADRs.adrs` é um dicionário indexado por número — a estrutura escolhida garante que
verificar "este número já existe" seja uma operação direta e barata, o que é exatamente a
verificação que `registrar` precisa fazer antes de aceitar qualquer novo ADR.


Nenhum dos três tipos centrais (`ADR`, `Documento`, `VerificacaoDeVigencia`) permite
representar um estado ambíguo — cada um força, pela própria forma do tipo, que a informação
necessária para as seis regras esteja presente e seja internamente consistente antes de o objeto
poder existir, sem depender de validação externa posterior.

Essa rigidez estrutural é o que torna os testes deste volume simples de escrever e de confiar, sem precisar simular cenários complexos de estado parcialmente inválido.

A ausência de qualquer campo opcional que pudesse ser deixado parcialmente preenchido reforça essa garantia em todos os três tipos, sem exceção.