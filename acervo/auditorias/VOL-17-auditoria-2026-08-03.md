# Auditoria — Volume 17 SECURITY

**Data:** 2026-08-03
**Revisao:** 1
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada:**

```
$ python -m ferramentas.validar 17
ok: volume 17 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/17-security
(nao existe — o volume nao cita codigo executavel formalmente)
```

## Ressalva de independencia

Auditor (Opus 5) distinto do redator (Sonnet 5), mesma sessao — independencia parcial. Ver a
mesma ressalva no relatorio do volume 01.

## Método

Este e o unico dos sete volumes deste ciclo cujo conteudo descreve um sistema **que existe e
roda**. Toda afirmacao sobre o motor `ENGINE` foi conferida contra o codigo e o `README.md`:

```
$ grep -rn "def test_nenhum_comando_de_shell_e_livre" ferramentas/tests/
ferramentas/tests/test_risco.py:400                                        [existe — confere]

$ grep -rn "R8" ferramentas/risco.py
"execucao indireta, cano para interpretador e substituicao de comando"
  -> a prosa dizia "execucao de codigo (python -c, exec)": estreito demais  [corrigido]

$ grep -rn "R9" ferramentas/risco.py
"escrita no painel de controle" / ".engine/estado.json guarda 'ativo'"      [confere]

$ grep -rn "R12" ferramentas/risco.py
existe (teto de tamanho)                                                    [confere]
```

Os seis vetores de contorno citados em `12-Exemplos` (`bash -c "rm"`, `echo $(rm -rf)`, quebra de
linha depois de `echo`, `cmd /c del`, `git -c core.fsmonitor=./script status`, `git diff
--output=`), o numero de rodadas (sete) e de contornos (doze), e o falso positivo da string
`'EXEC(ruim)'` foram conferidos contra o `README.md` do motor — **todos conferem literalmente**.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 9 | Isola a classe de risco que e propria de sistema com IA (a fronteira entre instrucao e dado desaparece porque o modelo le ambos como texto) e ancora no historico real e verificavel do motor deste repositorio. E a introducao mais bem fundamentada dos sete. |
| 02-Objetivos | 8.5 | Cinco objetivos, todos operacionais. O segundo (inversao de default para risco nao enumeravel) transmite o argumento estrutural, nao so a regra — o leitor sai sabendo *por que* blocklist perde. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas, com a distincao critica contra `01-FUNDACAO`: as duas matrizes de controle auditam coisas diferentes (texto contra comportamento de sistema). |
| 04-Arquitetura | 9 | A decisao central — classificar por comprovacao de inocuidade, nao por enumeracao de perigo — e apresentada com o argumento que a sustenta e com o custo historico real (doze contornos em sete rodadas). O `flowchart` mapeia as tres categorias no mesmo funil. |
| 05-Diagramas | 8 | O mindmap acerta que as tres categorias nao sao exclusivas num incidente real: injecao e vetor, exfiltracao e execucao sao os efeitos buscados. O `sequenceDiagram` isola a variavel certa — a mesma injecao chega nos dois ramos, o que muda e a confirmacao interposta. |
| 06-Fluxogramas | 8.5 | Detalha o gatilho de cada categoria e acerta o ponto que evita a defesa fragil: o gatilho de isolamento e **origem** (condicao estrutural), nao "este texto parece suspeito" (heuristica de conteudo). |
| 07-Regras | 9 | Cinco invariantes com o vetor por tras. A matriz tem quatro controles e um deles cita um teste **real e verificado** (`test_nenhum_comando_de_shell_e_livre`) — a unica matriz dos sete volumes com verificacao existente, nao proposta. |
| 08-Modelos | 8 | Quatro estruturas. `NivelRisco` corresponde aos tres niveis reais do motor. `OrigemDado` formaliza a distincao que `06-Fluxogramas` usa como gatilho. `VetorRisco` com data e exemplo concreto e o registro que `07-Regras` exige. |
| 09-Boas-Praticas | 8.5 | Cinco praticas com razao. "Nunca deixar a propria infraestrutura de seguranca fora do escopo de protecao" e a generalizacao correta do caso R9 real, escrita como principio e nao como anedota. |
| 10-Anti-Patterns | 9 | Cinco padroes, cada um com o custo. "Detectar prompt injection por filtro de padrao de texto" e "corrigir um contorno sem generalizar para a familia" sao os dois erros que o historico do motor de fato cometeu e pagou — o volume nao inventa anti-padrao, relata. |
| 11-Implementacao | 8.5 | **Corrigido nesta auditoria** (ver Problema 1). Unica secao 11 dos sete volumes que aponta para implementacao real e rodando. A observacao sobre falso positivo como evidencia de que o mecanismo esta ativo e uma leitura correta e nao obvia. |
| 12-Exemplos | 9 | Tres casos **reais e verificados** contra o `README.md` e o codigo: os doze contornos, o falso positivo do `'EXEC(ruim)'` e a familia R9. Nenhum inventado. E a melhor secao 12 dos sete volumes deste ciclo, pela mesma razao: tem historico real por tras. |
| 13-Testes | 8 | Propoe catalogo de vetores conhecidos mais teste estrutural que trava a politica — e o teste estrutural citado existe. Acerta ao exigir prova tambem do caso positivo (destino autorizado executa), nao so do bloqueio. |
| 14-Metricas | 8 | Quatro metricas com fonte e leitura nao obvia: taxa de falso positivo exatamente zero por muito tempo e sinal de suspeita, nao de qualidade. O tempo entre descoberta do vetor e o controle em producao e a metrica que mede exposicao real. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 2). Oito itens, desmarcados. O item sobre teste estrutural e o unico dos sete volumes que aponta para algo que de fato existe. |
| 16-Roadmap | 8 | Duas lacunas honestas, incluindo a mais importante: o catalogo de vetores atual e inteiramente sobre execucao insegura; injecao e exfiltracao ainda nao tem caso real documentado com o mesmo detalhe. |
| 17-Conclusao | 8.5 | Fecha com a licao estrutural correta — doze contornos nao significam que a lista estava quase completa, significam que listas fechadas nao convergem contra esse risco. |
| 18-Referencias-Cruzadas | 8 | Tres vizinhos com a fronteira dita, incluindo o link para o `README.md` do motor, que e a fonte real deste volume e resolve (gate 1). |

media: 8.4

## Problemas encontrados

1. **(menor — corrigido) 11-Implementacao descrevia R8 mais estreito do que a familia real.** O
   texto dizia "a familia R8 cobre execucao de codigo (`python -c`, `exec`)"; o `risco.py` define
   R8 como "execucao indireta, cano para interpretador e substituicao de comando dentro do
   argumento". O caso `python -c` cai em R8, mas a familia e mais ampla. Corrigido para a
   descricao real, mantendo o exemplo.
2. **(médio — corrigido) 15-Checklist vinha com sete itens marcados `[x]`.** Defeito sistemico
   dos sete volumes deste ciclo. Neste volume especificamente, um dos itens marcados era
   **verdadeiro** (o teste estrutural existe), o que tornava os outros seis mais crives — piorando
   o defeito em vez de atenuar. Corrigido nos sete.
3. **(menor — corrigido) uma ocorrencia de "excepcao"** (pt-PT) uniformizada para "excecao".
4. **(observacao) o volume descreve implementacao real mas nao a cita formalmente.** Nao ha
   `exemplos/17-security/` com o classificador extraido e testado no formato do acervo — e por
   isso o criterio 2 nao se satisfaz, mesmo sendo este o volume com mais codigo real por tras.
   `16-Roadmap` registra exatamente esse passo.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 17-SECURITY/
(saida vazia)
```

**Limpo.** As referencias sao ao motor `ENGINE` deste mesmo repositorio — procedencia legitima,
nao dominio externo.

## Veredicto

**Criterio 3 satisfeito. Volume NAO promovido.** Media 8.4 — a mais alta dos sete volumes deste
ciclo, e a razao e direta: e o unico cujo conteudo descreve um sistema que existe, com historico
verificavel. O **criterio 2 nao e satisfeito** — o classificador real vive em `ferramentas/` do
motor, nao em `exemplos/17-security/` no formato que o criterio exige. `status` permanece
`RASCUNHO`. Este e o volume onde fechar o criterio 2 e mais barato de todos: o codigo existe e
esta testado; falta extrai-lo como modulo citavel.
