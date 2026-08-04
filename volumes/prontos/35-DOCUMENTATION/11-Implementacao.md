---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/35-documentation/documentacao.py -->

`documentacao.py`, citado acima, formaliza W1-W6: `ADR.__post_init__` recusa criação sem
`contexto`, `decisao` ou `consequencia` (W1); `RegistroDeADRs.registrar` recusa sobrescrever
número já existente, e `substituir` marca o ADR anterior como `SUPERADO` sem removê-lo (W2);
`Documento.__post_init__` recusa `versionado_junto_do_codigo=False` (W3); `verificar_vigencia`
levanta `DocumentoDesatualizado` quando uma afirmação não é mais verdadeira (W4);
`editar_documento` recusa edição sobre documento `gerado_automaticamente` (W5); `publico_alvo`
restrito a dois valores válidos, sem terceira opção que misture os dois (W6).

`RegistroDeADRs.substituir` usa `dataclasses.replace` para produzir uma nova instância do ADR
anterior com `status="SUPERADO"`, em vez de mutar o objeto existente — a mesma disciplina de
imutabilidade de histórico já vista em `19-DEVOPS`, `24-DATABASE-ARCHITECT` e
`30-AI-GOVERNANCE`, reafirmando que fato histórico registrado não deveria ser alterável in-place
em nenhum lugar deste acervo.

Essa escolha de design reforça que o histórico de decisão, uma vez aceito, nunca é um alvo válido de mutação direta em nenhuma parte deste exemplo.

Nenhuma outra parte do módulo contorna essa disciplina, nem mesmo através de acesso direto a
atributo, já que o próprio dataclass congelado impede a mutação em tempo de execução, levantando
`FrozenInstanceError` diante de qualquer tentativa de reatribuição direta de campo já existente
no objeto, sem exceção alguma para nenhum dos campos declarados na definição da classe.