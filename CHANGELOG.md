# CHANGELOG

## 2026-07-30 — Fase 1 (núcleo)

- `config`, `risco`, `estado`, `cli` em Python de biblioteca padrão.
- Hooks `PreToolUse` (classificação de risco com falha segura) e `UserPromptSubmit`
  (cartão de estado com teto de linhas).
- Skill `/engine` com `ligar`, `desligar`, `status`.
- Papéis: arquiteto, implementador, revisor, documentador.
- Cartões: python, pytest, ui-ux.
- Verificação em `aceite/fase-1.md` (152 testes, verificação de aceite das sete
  famílias travadas pelo hook de verdade via `aceite/verificar_familias.py`, e o
  teste do teto do cartão de estado — todos com saída literal colada).

### A política do classificador de risco foi invertida durante a execução

`ferramentas/risco.py` não terminou a Fase 1 com a política com que começou. A versão
inicial tentava decidir se um comando de shell podia sair **livre** por prova
positiva — primeiro uma lista de comandos proibidos, depois uma lista de comandos
**permitidos**, depois essa mesma lista qualificada pela forma do argumento (nome do
comando **mais** as flags aceitas).

Sete rodadas de revisão adversarial atacaram essa lista e, em todas as sete, acharam
um caminho novo para `livre` liberando uma ação destrutiva. Os dois casos que
forçaram a virada de chave: `git diff --output=/home/user/.bashrc` (sobrescreve um
arquivo arbitrário escondido atrás do nome de um comando de leitura) e o apelido
`where` do PowerShell (que na verdade é `Where-Object`, e roda .NET arbitrário dentro
de um bloco de script). A causa não era uma flag esquecida em cada rodada — é
estrutural: **cada comando permitido é, ele próprio, uma linguagem**, com flags,
apelidos e formas de argumento que nenhuma lista fechada enumera até o fim. Enquanto
a categoria "comando liberável por prova positiva" existisse, a próxima rodada de
revisão sempre achava a próxima brecha.

A política final elimina a categoria inteira em vez de tentar fechá-la brecha por
brecha: **comando de shell nunca sai `livre`**. Ou ele casa uma das famílias fechadas
R1–R8 (rede, git destrutivo, deleção, banco, segredo, cano para interpretador,
substituição de comando, deploy/infraestrutura, instalação global) e vira
**travado**, ou vira **rastreado** — executa, e aparece no relatório de fim de fase.
Isso inclui fechar até o emissor inerte (`echo`/`printf`), que era a última válvula
capaz de liberar um segmento só por reconhecer o prefixo do comando. Só ferramenta de
**arquivo** continua podendo sair `livre` (leitura que não é segredo, escrita em
arquivo novo ou sob `tests/`).

O custo aceito, de propósito: o relatório de fim de fase fica mais longo — todo
comando de shell aparece nele, do `pytest -q` trivial ao comando perigoso. É uma
troca deliberada, registrada em `ferramentas/risco.py` e em
`docs/specs/2026-07-30-engine-design.md`: `rastreado` custa uma linha de relatório;
`livre` errado custa um estrago irreversível. `ferramentas/tests/test_risco.py::
test_nenhum_comando_de_shell_e_livre` é a trava dessa decisão — percorre comandos
cotidianos inofensivos e falha se qualquer um voltar a sair `livre`; reintroduzir uma
lista de permitidos é uma mudança de política que tem de custar esse teste vermelho
de propósito.

Essa mudança de política é também por que os números deste changelog e de
`aceite/fase-1.md` não batem com os do brief original da Tarefa 10
(`.superpowers/sdd/briefs/tarefa-10-brief.md`, escrito antes da virada): a suíte
cresceu de 68 para 152 testes cobrindo as famílias e os casos-limite achados nas
rodadas de revisão, e o script de verificação de aceite não usa mais nenhum caso de
"comando de shell liberado" como contraprova — a única superfície ainda `livre` por
natureza é leitura de arquivo comum. Detalhe completo em
`.superpowers/sdd/briefs/tarefa-10-report.md`.

**Não verificado nesta fase:** sobrevivência a 20 turnos reais e a uma compactação; os
quatro cenários de aceite com projetos-cobaia. Ambos são Fase 3.
