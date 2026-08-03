---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Reconciliação de conta com múltiplas moedas — os cinco módulos assumem valor numérico numa
única unidade monetária implícita; conversão fica fora de escopo até `52-CONSOLIDACAO-CONTAS`
ser reescrito e definir onde a conversão deveria acontecer na cadeia. Camada de palavras-chave
por conta específica (vocabulário de boilerplate diferente por banco ou por cliente) — hoje
`BOILERPLATE` em `casamento.py` é um único conjunto global; uma versão futura poderia receber
esse conjunto como parâmetro, mantendo o padrão genérico como default. Consolidação de múltiplos
títulos abertos casando com um único movimento (pagamento agregado de várias faturas de uma vez)
— `casar()` hoje devolve no máximo um título por movimento.

## Ordem de cobertura pretendida

Primeiro, os três volumes que este depende conceitualmente e ainda não foram reescritos —
`43-CONTABILIDADE-BASICA`, `53-AUDITORIA-TRILHA`, `54-INTEGRACAO-ERP` — porque só depois deles é
possível preencher `depende_de` de verdade e mostrar o motor operando com dado de origem real
(ainda que sintético). Depois, os itens de vocabulário por conta e consolidação de múltiplos
títulos, ambos motivados por casos observados em operação real de conciliação bancária.

## O que este volume assume que pode mudar

Os limiares numéricos em `confianca.py`
(`LIMIAR_HISTORICO_OCORRENCIAS`, `LIMIAR_HISTORICO_DOMINANCIA`) e em `casamento.py`
(`tolerancia_valor`, `limiar_similaridade`) são constantes de módulo, não configuração externa —
uma extensão natural é torná-los parâmetros calibráveis por conta, uma vez que exista volume
suficiente de decisão real auditada para calibrar com segurança em vez de achismo.
