---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Declarar toda variável obrigatória de um template explicitamente — nunca implícita, descoberta
apenas lendo a saída gerada e tentando adivinhar o que precisava ser preenchido.

Versionar todo template — uma mudança de estrutura é uma versão nova, e conteúdo gerado de uma
versão antiga nunca é presumido compatível com uma versão mais recente sem verificação.

Validar o uso de um template antes de a geração se completar — variável obrigatória ausente falha
explicitamente, nunca produz saída com placeholder vazio silencioso.

Manter todo template livre de conteúdo específico de domínio — nome de cliente, sistema
particular — permanecendo genérico e reutilizável, com conteúdo específico entrando apenas via
substituição de variável no momento do uso.

Depreciar template de forma explícita, com motivo e substituto quando possível, nunca removido
silenciosamente enquanto uso existente ainda referencia ele.

Os cinco objetivos, lidos em conjunto, garantem que um template catalogado aqui seja de fato
reutilizável na prática, não apenas em teoria — declaração explícita e validação de uso
(primeiro e terceiro) protegem contra uso incorreto; versionamento (segundo) protege contra
mudança silenciosa; neutralidade de domínio (quarto) protege reutilização real entre contextos
diferentes; depreciação explícita (quinto) protege quem ainda depende de uma versão anterior.

Nenhum desses cinco objetivos, isoladamente, garante um catálogo confiável — é a combinação completa que sustenta reutilização segura ao longo do tempo.