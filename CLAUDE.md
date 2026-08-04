# CLAUDE.md — ENGINE

Este repositório é **um projeto só**, com duas metades que se alimentam:

| Pasta | O que é | Suíte |
|---|---|---|
| raiz (`ferramentas/`, `hooks/`, `agents/`, `cartoes/`, `motores/`, `skills/`) | o **motor**: plugin do Claude Code, modo de engenharia persistente | `py -m pytest` (466) |
| `acervo/` | a **plataforma** que produz os volumes de conhecimento (42 volumes, contrato legível por máquina, 3 gates) | `cd acervo && py -m pytest` (789) |
| `acervo-controladoria/` | acervo de Controladoria — 2 volumes reais (`45`, `54`) e os seus exemplos | `py -m pytest acervo-controladoria/exemplos` (33) |
| `volumes/prontos/` | **artefato derivado** — a cópia que o plugin carrega | gerado, nunca editado |

As suítes rodam separadas de propósito: o motor e o acervo têm cada um o seu próprio
pacote `ferramentas`, e numa sessão única de pytest eles colidem. Ver `pytest.ini`.
As três rodam juntas na CI (`.github/workflows/suites.yml`), em jobs separados.

## A regra que não se quebra

**`volumes/prontos/` é gerado. Ninguém edita nada lá dentro.**

```bash
py -m ferramentas.sincronizar --verificar   # a cópia está em dia?
py -m ferramentas.sincronizar               # regenera a partir de acervo/
```

Mudou um volume? Muda em `acervo/NN-NOME/` e sincroniza. O critério de inclusão é o `status`
do `_VOLUME.yml` **da fonte**, e só ele: `RASCUNHO` não viaja no plugin, porque rascunho
carregado no contexto como conhecimento pronto é pior que volume ausente — quem lê não tem
como saber.

`test_a_copia_do_plugin_esta_em_dia` reprova a suíte se os dois lados divergirem. Se ele ficar
vermelho, a correção é sincronizar, nunca editar a cópia.

## Por que essa regra existe (custou de verdade)

Antes da unificação a cópia era manual, e derivou até o ponto de **mentir**: `31-TESTING`
estava em `volumes/prontos/` marcado `PRONTO` enquanto a fonte dizia `RASCUNHO`, e
`03-DISCOVERY`, esse sim `PRONTO`, nunca chegou. Mais 8 arquivos com conteúdo divergente em
`07-PROMPT-ENGINE` e `12-MEMORY`.

## Armadilhas conhecidas

- **`.engine/estado.json` é arquivo único, e agora tem cadeado.** Duas sessões no mesmo projeto
  se atropelavam: toda mutação era ler → alterar → gravar em três passos soltos, a segunda lia
  antes de a primeira gravar, e as transições que a CLI já tinha confirmado sumiam do disco.
  Não era corrupção (`gravar` sempre foi atômico) — era pior: JSON válido, sem o trabalho.
  Corrigido em 2026-08-04 com `estado.cadeado` (`.engine/estado.lock`, `O_EXCL`) e
  `estado.atualizar`, que relê **de dentro** da seção crítica. Quem muta estado usa
  `atualizar()`, nunca `gravar()` direto — `test_nenhum_gravar_fora_do_estado` trava a regra.
  Rodar o motor com várias sessões abertas na mesma pasta deixou de ser proibido.
- **Erro de caixa volta.** Já apareceu quatro vezes (`re.I` em `_PY_PERIGO`, filtro
  `*WindowsApps*` do lançador, `.ENGINE/` em `_sob_painel`, `shutil.which("bash")` no teste do
  lançador). Quando achar um, **varra o repositório inteiro** — não conserte só a ocorrência.
- **Falso positivo do classificador é defeito de segurança**, não incômodo: treina o humano a
  aprovar no automático, e aí o gate não protege mais nada.
- **Comando de shell nunca é `livre`.** Decisão que custou 7 rodadas de revisão e 12 bypasses;
  não reabrir. Ou trava (R1–R9) ou é `rastreado`. Só ferramenta de arquivo pode ser `livre`.
  Travado por `test_nenhum_comando_de_shell_e_livre`.
- **O plugin instalado é uma cópia** feita no momento do `install`: mudar o repositório não
  muda o que roda até reinstalar.
- **Push exige `fetch` + merge antes**, sempre, e `--force` nunca: já houve sessão paralela
  empurrando 17 commits neste mesmo repositório.
- **A durabilidade não é observação, é propriedade.** O cartão sobrevive à compactação porque
  `hooks/engine_contexto.py` lê do evento **só `cwd`** — nada de `transcript_path`,
  `session_id` ou contexto. Enriquecer o cartão com a transcrição quebra a durabilidade no
  mesmo commit; `test_o_cartao_nao_depende_de_nada_que_a_compactacao_destroi` reprova.

## Contexto de história

O acervo entrou aqui em 2026-08-03 com o histórico preservado (`git subtree`, remoto
`plataforma`). Ele continua tendo repositório público próprio; o motor tem o dele. A
unificação não renomeou nada nem reapontou o plugin. Detalhes no `CHANGELOG.md`.
