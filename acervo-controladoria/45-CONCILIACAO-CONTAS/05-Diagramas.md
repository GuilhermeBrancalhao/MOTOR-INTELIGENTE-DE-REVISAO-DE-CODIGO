---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 05-Diagramas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Diagramas

```mermaid
sequenceDiagram
    participant Op as Operador
    participant Anc as ancora.py
    participant Cas as casamento.py
    participant Conf as confianca.py
    participant Grd as guarda.py
    participant Tri as trilha.py

    Anc->>Anc: achar_ancora(saldo, movimentos, saldos_banco)
    Anc-->>Op: dia fechado no centavo (ou None)
    Cas->>Cas: casar(movimento, titulos_abertos)
    Cas-->>Conf: titulo casado (ou None)
    Conf->>Conf: classificar(evidencia)
    alt confianca ALTA
        Conf->>Grd: ja_registrado(chave)?
        Grd-->>Conf: nao
        Conf->>Tri: registrar(chave, usuario, quando, acao)
        Tri-->>Op: escrita confirmada
    else confianca MEDIA ou BAIXA
        Conf-->>Op: pendencia para revisao humana
    end
```

A sequência mostra a ordem real de chamada dentro de um ciclo de conciliação: a âncora roda
primeiro e de forma independente do restante — ela responde "os saldos batem no geral?", não
"este movimento específico casa com o quê?". Casamento e confiança rodam por movimento, e só
depois de a confiança classificar como ALTA é que guarda e trilha entram, nessa ordem — a
guarda é consultada antes de qualquer escrita, e só se a chave for nova é que a trilha registra.
Quando a confiança fica em MEDIA ou BAIXA, o fluxo nunca chega a guarda ou trilha: a decisão
correta é não escrever, e devolver a pendência para revisão humana, comportamento coberto pelo
teste `test_fluxo_nao_escreve_quando_confianca_e_baixa`.

## Entidades e relação

```mermaid
erDiagram
    MOVIMENTO ||--o| TITULO_ABERTO : "casa com (0 ou 1)"
    MOVIMENTO ||--|| EVIDENCIA : "gera"
    EVIDENCIA ||--|| CONFIANCA : "classifica em"
    MOVIMENTO ||--o| CHAVE_MOVIMENTO : "vira, se escreve"
    CHAVE_MOVIMENTO ||--|| REGISTRO_TRILHA : "registra"
```

Um movimento casa com no máximo um título aberto — nunca mais de um, porque `casar()` sempre
devolve um único candidato ou `None`. A relação entre movimento e chave de escrita é opcional
porque nem todo movimento vira escrita: só os que atingem confiança ALTA chegam a ter uma
`ChaveMovimento` registrada na trilha, e essa é exatamente a fronteira que `06-Fluxogramas.md`
detalha como máquina de estados. A relação entre `EVIDENCIA` e `CONFIANCA` é sempre um-para-um e
sempre obrigatória — todo movimento casado gera uma evidência, e toda evidência é classificada,
mesmo quando o resultado é `BAIXA`; não existe estado intermediário em que um movimento casado
fique sem classificação. Essa obrigatoriedade é o que garante que a máquina de estados de
`06-Fluxogramas.md` nunca trave num nó sem saída definida.
