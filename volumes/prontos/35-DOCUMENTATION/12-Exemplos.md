---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — ADR completo registrado corretamente

Um ADR com contexto, decisão e consequência preenchidos é aceito pelo registro sem ressalva.

## Caso 2 — tentativa de reescrever ADR existente é rejeitada

Uma segunda tentativa de registrar um ADR com o mesmo número de um já existente, sem passar por
`substituir`, é rejeitada — o registro original permanece intocado.

## Caso 3 — substituição preserva o ADR anterior como SUPERADO

Uma decisão que muda gera um novo ADR com `supersede` apontando para o anterior. O ADR anterior
passa a `status="SUPERADO"`, mas continua no registro, consultável.

## Caso 4 — documento gerado não pode ser editado manualmente

Uma tentativa de `editar_documento` sobre um documento marcado como `gerado_automaticamente` é
rejeitada — a mudança precisa ir para a fonte de verdade que gera o conteúdo.

## Caso 5 — vigência detecta documento desatualizado

Uma verificação de vigência confirma que uma afirmação específica de um documento não é mais
verdadeira no código atual, levantando `DocumentoDesatualizado` com a afirmação exata que falhou.


Os cinco casos cobrem, juntos, as seis regras completas — os Casos 2 e 3 formam um par que prova
W2 nos dois sentidos (sobrescrita direta rejeitada, substituição explícita aceita e preservando o
histórico), enquanto os demais casos cobrem W1, W4 e W5 isoladamente.

Essa cobertura pareada é deliberada, escolhida especificamente para deixar claro o contraste entre o caminho rejeitado e o caminho aceito da mesma regra.

Ler os cinco em sequência dá uma visão relativamente completa do ciclo de vida de uma decisão documentada, do registro inicial até sua eventual substituição por uma versão mais recente.