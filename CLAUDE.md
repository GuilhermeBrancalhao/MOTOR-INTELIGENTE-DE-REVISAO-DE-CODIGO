# CLAUDE.md — ENGINE

Este repositório é **um projeto só**, com duas metades que se alimentam:

| Pasta | O que é | Suíte |
|---|---|---|
| raiz (`ferramentas/`, `hooks/`, `agents/`, `cartoes/`, `motores/`, `skills/`) | o **motor**: plugin do Claude Code, modo de engenharia persistente | `py -m pytest` (449) |
| `acervo/` | a **plataforma** que produz os volumes de conhecimento (42 volumes, contrato legível por máquina, 3 gates) | `cd acervo && py -m pytest` (455) |
| `volumes/prontos/` | **artefato derivado** — a cópia que o plugin carrega | gerado, nunca editado |

As duas suítes rodam separadas de propósito: cada metade tem o seu próprio pacote
`ferramentas`, e numa sessão única de pytest eles colidem. Ver `pytest.ini`.

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

- **`.engine/estado.json` é arquivo único.** Duas sessões no mesmo projeto se atropelam: a
  segunda sobrescreve o ciclo da primeira, e as transições que a CLI confirmou somem do disco.
  Não ligar o motor em pasta com mais de uma sessão aberta.
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

## Contexto de história

O acervo entrou aqui em 2026-08-03 com o histórico preservado (`git subtree`, remoto
`plataforma`). Ele continua tendo repositório público próprio; o motor tem o dele. A
unificação não renomeou nada nem reapontou o plugin. Detalhes no `CHANGELOG.md`.
