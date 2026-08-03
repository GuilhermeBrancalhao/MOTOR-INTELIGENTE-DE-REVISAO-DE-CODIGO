# Auditoria — Volume 21 OBSERVABILITY

**Data:** 2026-08-03
**Revisao:** 1
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada:**

```
$ python -m ferramentas.validar 21
ok: volume 21 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/21-observability
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

Auditor (Opus 5) distinto do redator (Sonnet 5), mesma sessao — independencia parcial. Ver a
mesma ressalva no relatorio do volume 01.

## Método

Este volume consome conceitos definidos em outros quatro. Conferida a coerencia de cada
emprestimo: `MotivoEncerramento` existe em `08-AGENT-ENGINE/08-Modelos.md` com os tres valores
citados; os dois estados de espera (`AguardandoSinal`, `Pausado`) existem em
`10-WORKFLOW/06-Fluxogramas.md` e mapeiam para os dois sub-ramos de intervencao humana como o
mindmap afirma; a taxonomia de risco que este volume assume pronta e a de `17-SECURITY`. Nenhuma
divergencia. Conferida a existencia de "Prova por mutacao" em `13-Testes`, afirmada por
`31-TESTING`. Conferido que o link relativo para `08-AGENT-ENGINE/08-Modelos.md` resolve (gate 1).

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | Nomeia a lacuna certa: o modelo responde com sucesso tecnico e ainda produz saida errada — classe de falha invisivel a metrica de infraestrutura. A relacao irma com `17-SECURITY` (aquele define o que precisa ser detectavel, este como se instrumenta) e precisa. |
| 02-Objetivos | 8 | Cinco objetivos. O ultimo delimita bem o volume: as listas de metricas especificas vivem em cada volume de dominio; este define como qualquer uma delas e coletada e monitorada de forma consistente. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas, incluindo a mais facil de confundir: as metricas de `01-FUNDACAO` medem saude do processo de documentacao, nao telemetria de producao. |
| 04-Arquitetura | 8.5 | A decisao central — nem todo sinal instrumentado gera alerta — evita os dois extremos com nome (fadiga de alerta; anomalia sem aviso). O `flowchart` mapeia as tres categorias para o mesmo teste de limiar. |
| 05-Diagramas | 8 | O mindmap nao inventa taxonomia: consolida conceitos ja definidos em `08`, `09` e `10`, e isso esta dito. O `sequenceDiagram` da decomposicao justifica por que `tokens` e `None` para etapa deterministica — ausencia estrutural, nao dado faltante. Precisou de duas expansoes para atingir o minimo de prosa. |
| 06-Fluxogramas | 8 | O processo de calibracao (observar antes de fixar; recalibrar so depois de distinguir limiar errado de comportamento mudado) e a parte que o codigo nao daria de graca. O "caminho que nunca deveria existir" nomeia o cenario mais perigoso. |
| 07-Regras | 8.5 | Cinco invariantes. A quinta — falha do proprio mecanismo de alerta e ela mesma um sinal monitorado — e a generalizacao correta do mesmo principio que `17-SECURITY` aplica ao proprio painel de controle. Matriz com quatro controles. |
| 08-Modelos | 8 | Quatro estruturas. `Alerta.notificado_em` sendo `None` apos o limiar cruzado e a condicao de falha critica formalizada como campo — desenho, nao decoracao. `Limiar.base_observacao` registra proveniencia. |
| 09-Boas-Praticas | 8 | Cinco praticas. "Testar o canal de notificacao com a mesma disciplina que se testa o sinal" ataca o ponto cego real: a falha do canal e silenciosa por natureza. |
| 10-Anti-Patterns | 8.5 | Cinco padroes. "Recalibrar limiar para parar de alertar sem investigar se o alerta estava certo" nomeia a troca perigosa — visibilidade de problema real por silencio confortavel. |
| 11-Implementacao | 7.5 | Mesma limitacao estrutural dos volumes 08, 09 e 10: sem codigo. Salva-se pela decisao de desenho defendida (o motor de origem emite o sinal; nao inferir de log generico depois do fato, que perderia granularidade na traducao). |
| 12-Exemplos | 8.5 | Tres casos que cobrem as tres falhas distintas do volume: qualidade mascarada por sucesso tecnico, limiar mal calibrado com fadiga, e canal mudo por tres dias. O terceiro liga com `17-SECURITY` e mostra o custo real do ponto cego. |
| 13-Testes | 8 | Propoe testar os dois caminhos de falha do proprio mecanismo, nao so o sinal. A prova por mutacao (trocar notificacao por registro em log) e discriminante e cobre a invariante central. |
| 14-Metricas | 8.5 | Secao incomum e bem resolvida: as metricas deste volume medem a saude do proprio mecanismo de observabilidade. "Taxa de sinais emitidos que nunca chegam ao coletor" e o pre-requisito de confiabilidade de todas as outras. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 1). Oito itens verificaveis, desmarcados. |
| 16-Roadmap | 8 | Tres lacunas, incluindo recalibracao automatica por deteccao de deriva — com a ressalva certa: automatizar a deteccao de *quando* recalibrar nao e automatizar a decisao de *qual valor*, que continua exigindo julgamento sobre causa. |
| 17-Conclusao | 8 | Fecha com as duas ideias que sustentam o volume (sucesso tecnico nao implica resultado correto; canal de alerta precisa de monitoramento proprio) e declara o proprio estado. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos com a relacao dita; o link para `08-AGENT-ENGINE/08-Modelos.md` aponta para o conceito que este volume instrumenta e resolve. |

media: 8.2

## Problemas encontrados

1. **(médio — corrigido) 15-Checklist vinha com sete itens marcados `[x]`**, dois afirmando
   testes inexistentes ("Existe teste que forca um sinal a cruzar o limiar e verifica disparo
   real de notificacao..."). Defeito sistemico dos sete volumes deste ciclo. Corrigido nos sete.
2. **(menor — corrigido) duas ocorrencias de "excepcao"** (pt-PT) uniformizadas para "excecao".
3. **(observacao) 05-Diagramas precisou de duas expansoes para atingir o minimo de prosa** — a
   segunda repetindo, em `05`, a explicacao de `tokens: None` que ja estava em `08-Modelos`. Nao e
   erro (a explicacao e correta nos dois lugares), mas e a passagem mais redundante do volume.
4. **(observacao) o volume e o mais dependente de outros do ciclo.** Consome definicoes de `08`,
   `09`, `10` e `17`. Isso e coerente com o escopo declarado, e todas as dependencias conferem —
   mas significa que uma mudanca de contrato em qualquer um daqueles quatro exige revisao deste.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 21-OBSERVABILITY/
(saida vazia)
```

**Limpo.** Os exemplos usam dominio inventado (classificacao de documento) ou referencias
internas ao proprio acervo.

## Veredicto

**Criterio 3 satisfeito. Volume NAO promovido.** Media 8.2, nenhuma secao abaixo de 6. O
**criterio 2 nao e satisfeito** — nao existe `exemplos/21-observability/`. `status` permanece
`RASCUNHO`.
