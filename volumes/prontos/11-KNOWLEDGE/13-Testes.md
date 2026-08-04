---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este motor exige simular os dois pontos de decisão mais importantes: rejeição de
documento sem autoridade, e não-devolução de documento expirado — não só o caminho de ingestão
bem-sucedida.

## O que a suíte precisa cobrir

Autoridade obrigatória: um teste que tenta ingerir documento sem `Origem` completa e verifica
rejeição (K1). Expiração: um teste que avança o estado de um documento até `Expirado` e confirma
que `consultar_valido` não o devolve, mesmo que o documento ainda exista na estrutura (K2).
Conflito: um teste com dois documentos do mesmo `fato_chave` verificando que nenhum é
automaticamente descartado sem sinalização (K3). Revalidação: um teste que confirma que só a
transição explícita `Expirando -> Valido` existe, nunca uma renovação implícita por tempo (K6).

## Prova por mutação

Um teste forte para K2 é um que falha se `consultar_valido` for trocado para devolver todo
documento independente do estado — mutação que reintroduziria exatamente o risco que a regra
existe para prevenir: documento vencido tratado como atual.

## Testes de integração com volumes vizinhos

Um teste relevante verifica que `13-RAG`, ao consultar disponibilidade de um documento, respeita
o estado de ciclo de vida deste volume mesmo quando `14-VECTOR` ainda tem o vetor indexado — a
integração testa que a fronteira entre curadoria e índice é respeitada na prática, não só na
prosa.

## O que a suíte não cobre ainda

Resolução de conflito por regra declarada (por exemplo, "origem jurídica sempre prevalece") não
está no exemplo mínimo — hoje toda resolução é uma chamada explícita a `resolver_conflito` com o
vencedor nomeado manualmente. Automatizar isso exigiria uma camada de regra que o exemplo não
tenta cobrir, registrada como lacuna honesta em `16-Roadmap.md`, não escondida.
