---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Time de desenvolvimento", "Declara schema e migracoes")
    System(repo, "Repositorio", "Migracao compativel, procedencia, concorrencia, retencao")
    System_Ext(worker, "Worker sem estado (23)", "Grava resultado de trabalho de IA")
    System_Ext(api, "API (25)", "Le e expoe dado ao cliente, formato proprio")
    System_Ext(vetor, "Indice Vetorial (14)", "Persistencia paralela, disciplina propria")

    Rel(dev, repo, "Declara migracao com flag de compatibilidade")
    Rel(worker, repo, "Grava com versao esperada e procedencia")
    Rel(repo, api, "Fornece dado para o contrato do 25 traduzir")
    Rel(repo, vetor, "Coexiste sem depender um do outro")
```

O `Indice Vetorial (14)` aparece no diagrama como sistema paralelo, não como dependência — a
seta que os liga é rotulada "coexiste sem depender", porque nenhuma das garantias deste volume
(migração compatível, proveniência, concorrência, retenção) exige que um índice vetorial exista
ou funcione de determinada forma; os dois sistemas de persistência operam sob disciplinas
independentes, mesmo compondo o mesmo produto.

```mermaid
sequenceDiagram
    participant W as Worker (23)
    participant Repo as Repositorio
    participant Outro as Outro Worker (concorrente)

    W->>Repo: ler registro, versao atual = 3
    Outro->>Repo: salvar(versao_esperada=3) -> sucesso, versao vira 4
    W->>Repo: salvar(versao_esperada=3)
    Repo-->>W: ConflitoDeConcorrencia (versao real ja e 4)
    W->>Repo: reler registro, versao atual = 4
    W->>Repo: salvar(versao_esperada=4)
    Repo-->>W: sucesso, versao vira 5
```

O worker que perde a corrida nunca sobrescreve silenciosamente o resultado do outro — ele recebe
o conflito, releva o estado atual, e decide (reaplicar sua mudança sobre o novo estado, ou
descartar) de forma explícita. Essa decisão nunca é tomada pelo repositório automaticamente,
porque só quem está gravando sabe se sua mudança ainda faz sentido sobre um estado que mudou.


O diagrama de sequência modela o cenário mais informativo — dois workers concorrentes — em vez do
caminho feliz de escrita única, porque é justamente sob concorrência que a diferença entre este
modelo e um repositório ingênuo de "última escrita vence" se torna visível.

Nenhum dos dois diagramas modela um cenário de escrita única sem concorrência — essa omissão é
deliberada, porque o caso trivial não distingue este modelo de um repositório ingênuo; a
concorrência é justamente onde a diferença de design se manifesta e vale a pena visualizar.