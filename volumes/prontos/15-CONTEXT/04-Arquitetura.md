---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

```mermaid
C4Context
    title Contexto do gestor de orcamento de janela
    Person(dev, "Quem desenha o sistema", "Declara orcamento total e prioridade entre categorias de conteudo")
    System(gestor, "Context Engine", "Orcamento, prioridade, descarte registrado, gatilho de compactacao")
    System_Ext(rag, "13-RAG", "Documentos recuperados competem por espaço, sem tratamento especial implicito")
    System_Ext(historico, "Historico de conversa", "Cresce a cada turno, candidato a compactacao quando antigo")
    System_Ext(modelo, "Chamada ao modelo", "Recebe a janela ja dentro do orcamento declarado")
    Rel(dev, gestor, "Declara orcamento total e ordem de prioridade")
    Rel(rag, gestor, "Documentos recuperados, um tipo de conteudo entre outros")
    Rel(historico, gestor, "Turnos de conversa, candidatos a compactacao")
    Rel(gestor, modelo, "Janela montada dentro do orcamento, com descarte registrado")
```

O gestor recebe candidatos de múltiplas fontes — histórico, documentos recuperados, resultado de
ferramenta — e nenhuma delas tem prioridade implícita sobre as outras só por ser a fonte mais
recente ou mais frequentemente usada. A prioridade é sempre uma decisão declarada por quem desenha
o sistema, não uma consequência acidental da ordem em que o conteúdo chegou ao gestor.

## Componentes

O **orçador** mantém o limite total de tokens e o consumo corrente, recusando adicionar conteúdo
que excederia o limite sem antes aplicar a política de descarte. O **priorizador** aplica a ordem
declarada entre categorias de conteúdo quando o orçamento não comporta tudo — instrução do
sistema tipicamente tem prioridade máxima (nunca descartada), seguida de ordem específica para
histórico, documentos recuperados e resultado de ferramenta. O **registrador de descarte** grava
o que foi removido e por qual categoria de prioridade, nunca descarta sem esse registro. O
**gatilho de compactação** decide, com margem antes do limite ser atingido, quando resumir
histórico antigo em vez de simplesmente descartá-lo.

## Por que categoria, não conteúdo, determina prioridade

A prioridade é atribuída à categoria do item (instrução, histórico, documento), nunca ao
conteúdo específico de um item individual dentro da categoria. Isso mantém a decisão de
prioridade simples e auditável — qualquer pessoa pode ler `ORDEM_DE_PRIORIDADE` inteira em
segundos, o que não seria possível se a prioridade dependesse de julgamento sobre o conteúdo de
cada item específico.
