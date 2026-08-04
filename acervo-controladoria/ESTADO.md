# Estado do acervo de Controladoria

**Atualizado em:** 2026-08-04

Este acervo foi **reduzido ao que nele é real** em 2026-08-04, por decisão do autor. Restam dois
volumes, e os dois hoje passam o gate estrutural com zero violações: `45-CONCILIACAO-CONTAS` e
`54-INTEGRACAO-ERP`. Os dez volumes que eram esqueletos foram removidos.

## Como reproduzir a medição

```
cd acervo
python -m ferramentas.validar --raiz ../acervo-controladoria --tudo
cd .. && python -m pytest acervo-controladoria/exemplos -q
```

## Estado atual

| Volume | Tipo | Violações | Prosa | Exemplo | Estado |
|---|---|---:|---:|---|---|
| **45-CONCILIACAO-CONTAS** | ENGINE | **0** | 5.665 | 6 módulos | **conforme** |
| **54-INTEGRACAO-ERP** | ARQUITETURA | **0** | 4.647 | 1 módulo | **conforme** |

Os 33 testes de `exemplos/` passam, e desde 2026-08-04 rodam na CI.

### 45-CONCILIACAO-CONTAS — conforme

Passa o gate estrutural com zero violações: 18 seções com front-matter, 5.665 palavras de prosa
real, seis módulos de exemplo (`ancora`, `casamento`, `confianca`, `guarda`, `trilha` e um teste
de fluxo completo). Satisfaz o critério 1 da Definição de PRONTO. Falta-lhe o critério 3 —
auditoria por modelo distinto registrada em `auditorias/` — para ser promovido a `PRONTO`.

### 54-INTEGRACAO-ERP — conforme (reescrito em 2026-08-04, depois desta auditoria)

A medição original desta auditoria encontrou 41 violações — 17 seções sem front-matter, 15
seções abaixo do mínimo de substância, os dois diagramas que o tipo `ARQUITETURA` exige
(`C4Context` e `sequenceDiagram`) ausentes, e uma citação defeituosa (`11-Implementacao.md`
citava `tests/test_normalizar.py` como se fosse módulo de exemplo, fazendo o gate cobrar um
teste *do teste*). As 18 seções foram reescritas com prosa real ancorada no único exemplo que
existe de fato — `normalizar.py`, normalização de CSV de banco/fintech sem API, com detecção
automática de coluna crítica e testado contra dado real do DIGIO — e os dois diagramas exigidos
foram adicionados em `04-Arquitetura.md` (`C4Context`) e `05-Diagramas.md` (`sequenceDiagram`).
A citação defeituosa foi corrigida separadamente, antes desta reescrita.

Satisfaz o critério 1 da Definição de PRONTO, como o 45. Falta-lhe, além do critério 3
(auditoria por modelo distinto): cobertura contra mais de um banco (hoje só DIGIO, e um dos dois
arquivos do DIGIO tem bug conhecido de BOM UTF-8 ainda não corrigido, ver `12-Exemplos.md`
daquele volume) e o conector de API de ERP, que permanece só intenção declarada.

## O que foi removido, e por quê

Dez volumes — `43`, `44`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53` — foram removidos por
`git rm` em 2026-08-04. Cada um tinha 18 arquivos de seção somando cerca de 280 palavras, isto é,
aproximadamente 15 palavras por seção, sem front-matter e sem exemplo. O `01-Introducao.md` de
`43-CONTABILIDADE-BASICA` tinha cinco linhas: título, uma frase de escopo, o tipo e a frase
"Volume essencial para Controladoria moderna".

Eram andaime gerado em lote, não conteúdo — a mesma patologia que o `ROADMAP.md` do acervo
principal registrou em 2026-08-03. **Continuam recuperáveis pelo histórico do git** (estavam em
`HEAD` até o commit desta remoção), caso venha a existir intenção concreta de escrevê-los.

O `contrato.json` foi reduzido junto: declarava doze volumes, declara agora os dois que existem.
Contrato que promete o que não existe deixa de ser fonte de verdade.

## Medição anterior, preservada como registro

A validação de 2026-08-04, antes da redução, encontrou **420 violações** nos doze volumes.

O total aparente inicial era **186**, e a diferença tinha causa mecânica: seis volumes declaravam
`tipo: PROCESSO` no `_VOLUME.yml` enquanto o `contrato.json` os definia como `ENGINE`,
`GOVERNANCA` ou `ARQUITETURA`. O validador reprovava por `volume-tipo` e **parava ali**, sem
examinar as 18 seções — um volume inteiro de esqueletos aparecia como "1 violação".

Os stubs haviam carimbado `PROCESSO` nos doze indiscriminadamente; o gerador escreveu a linha
`Tipo: PROCESSO` até dentro do corpo de `01-Introducao.md`. O `45`, único escrito de verdade,
declarava `ENGINE` e casava com o contrato — o que identificou com segurança qual lado errara.

**É a mesma classe de defeito do bug de BOM UTF-8 de 2026-08-03**, que fazia 39 violações
aparentes esconderem 657 reais. Vale como regra para este repositório: quando um gate reprovar
por metadado, o total não é confiável até o metadado estar correto.

## Dívida quitada: os testes órfãos

`acervo-controladoria/exemplos/` tinha 33 testes que passavam e que **nenhuma suíte
coletava**. A raiz coleta só a suíte do motor por decisão documentada no `pytest.ini`
— dois pacotes `ferramentas`, o da raiz e o de `acervo/`, colidem numa sessão só de
pytest — e o acervo roda de dentro de si. Este acervo não era contemplado por nenhum
dos dois arranjos, então seus testes passavam por ninguém ter mexido no código, não
por verificação de rotina.

Em 2026-08-04 isso deixou de ser verdade: `.github/workflows/suites.yml` roda as três
suítes a cada push, em jobs separados (o job `controladoria` roda estes 33 testes e o
gate estrutural dos dois volumes).

| Suíte | Testes | Como roda |
|---|---:|---|
| motor | 450 | `pytest` na raiz — CI, job `motor` |
| acervo | 789 | `pytest` de dentro de `acervo/` — CI, job `acervo` |
| controladoria | 33 | `pytest acervo-controladoria/exemplos` — CI, job `controladoria` |
