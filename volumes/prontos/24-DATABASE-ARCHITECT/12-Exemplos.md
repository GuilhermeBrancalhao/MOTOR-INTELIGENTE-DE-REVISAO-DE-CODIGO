---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — migração compatível aceita, incompatível rejeitada

Uma migração que adiciona um campo novo opcional é aceita normalmente. Uma migração que remove um
campo ainda em uso por código não migrado é rejeitada antes de ser registrada no histórico.

## Caso 2 — conteúdo de IA sem proveniência é rejeitado na criação

Uma tentativa de criar `RegistroDeConteudo` sem `Procedencia` falha imediatamente — nunca existe
um registro de conteúdo gerado por IA sem saber qual modelo o produziu.

## Caso 3 — conflito de concorrência entre dois workers

Dois workers leem o mesmo registro na versão 3. O primeiro grava com sucesso, avançando para
versão 4. O segundo tenta gravar ainda esperando versão 3 e recebe `ConflitoDeConcorrencia` — ele
releva o estado atual antes de decidir como proceder.

## Caso 4 — leitura tolera campo desconhecido

Um registro bruto contém um campo `"confianca_do_modelo": 0.92` que o código atual não conhece.
`ler_tolerante` preserva esse campo em `campos_desconhecidos` em vez de falhar ou descartá-lo
silenciosamente.

## Caso 5 — exclusão bloqueada por referência ativa

Uma tentativa de remover um registro ainda referenciado por outro é rejeitada com
`ReferenciaAtiva`. Removendo primeiro a referência (ou decidindo explicitamente propagar a
exclusão), a remoção original passa a ser permitida.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 3 sozinho ilustra tanto o lado
que perde a corrida (recebe o conflito) quanto implicitamente o lado que venceu (cuja escrita foi
preservada sem ser sobrescrita), tornando visível o comportamento das duas partes envolvidas numa
mesma disputa de concorrência.