---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`ADR.__post_init__` recusa sua própria criação sem `contexto`, `decisao` e `consequencia`
preenchidos — um ADR incompleto nunca chega a existir como registro válido.

`RegistroDeADRs.registrar` recusa sobrescrever um ADR já existente com o mesmo número — a única
forma de mudar uma decisão registrada é `substituir`, que marca o ADR anterior como `SUPERADO`
(nunca removido) e registra um novo ADR explicitamente ligado a ele por `supersede`.

`Documento.__post_init__` recusa um documento que não está `versionado_junto_do_codigo`, e recusa
um documento marcado como `gerado_automaticamente` sem `fonte_de_verdade` declarada — as duas
verificações acontecem na própria construção do objeto, tornando os dois estados inválidos
estruturalmente impossíveis de representar.

`verificar_vigencia` e `editar_documento` são as duas operações que protegem documentação depois
de criada: a primeira detecta quando uma afirmação específica do documento já não corresponde ao
código; a segunda recusa edição manual em documento gerado, redirecionando a mudança para a fonte
de verdade correta.


Cada uma dessas quatro verificações acontece no momento da construção do objeto correspondente,
não como validação posterior opcional — um `ADR` incompleto ou um `Documento` mal configurado
nunca chega a existir como instância válida no sistema, eliminando a possibilidade de esses
estados inválidos se propagarem para código que os consome depois.

Essa disciplina de validação na construção, em vez de depois, é consistente com o padrão já estabelecido por vários outros volumes deste acervo.