# Aceite da Fase 1 — ENGINE

**Data:** 2026-07-30

Este documento é o registro do aceite. Ele não escreve produto — decide, com saída
real colada, se a Fase 1 está pronta. As três saídas abaixo foram rodadas nesta data,
neste repositório (`C:\Users\Usuário\Desktop\ENGINE`, branch `feat/fase-1`), e coladas
sem edição de conteúdo (só a formatação em bloco de código).

**Nota sobre o brief original:** `.superpowers/sdd/briefs/tarefa-10-brief.md` foi
escrito antes de a política do classificador (`ferramentas/risco.py`) mudar de "lista
de comandos proibidos" para "comando de shell nunca é livre" (ver seção de adaptações
no final deste documento e `.superpowers/sdd/briefs/tarefa-10-report.md`). Os números e
o script de verificação abaixo refletem o estado real do código nesta data, não os
números do brief.

---

## Passo 1 — Suíte completa

Comando:

```
python -m pytest ferramentas/tests -v
```

Saída literal:

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Usuário\Desktop\ENGINE
plugins: anyio-4.14.0
collecting ... collected 152 items

ferramentas/tests/test_cli.py::test_ligar_cria_o_estado PASSED           [  0%]
ferramentas/tests/test_cli.py::test_status_com_motor_desligado PASSED    [  1%]
ferramentas/tests/test_cli.py::test_desligar_depois_de_ligar PASSED      [  1%]
ferramentas/tests/test_cli.py::test_fase_invalida_reporta_erro_sem_estourar PASSED [  2%]
ferramentas/tests/test_cli.py::test_verbo_desconhecido_sai_com_erro PASSED [  3%]
ferramentas/tests/test_cli.py::test_ligar_sem_objetivo_reporta_erro_sem_estourar PASSED [  3%]
ferramentas/tests/test_cli.py::test_ligar_duas_vezes_sem_forcar_reporta_erro_sem_estourar PASSED [  4%]
ferramentas/tests/test_cli.py::test_ligar_duas_vezes_com_forcar_sobrescreve PASSED [  5%]
ferramentas/tests/test_cli.py::test_fase_sem_ciclo_ativo_reporta_erro_sem_estourar PASSED [  5%]
ferramentas/tests/test_cli.py::test_desligar_sem_ciclo_nunca_ligado_nao_estoura PASSED [  6%]
ferramentas/tests/test_cli.py::test_desligar_com_estado_corrompido_nao_estoura PASSED [  7%]
ferramentas/tests/test_cli.py::test_acentuacao_sai_em_utf8 PASSED        [  7%]
ferramentas/tests/test_cli.py::test_status_com_estado_corrompido_reporta_erro_sem_estourar PASSED [  8%]
ferramentas/tests/test_cli.py::test_fase_com_estado_corrompido_reporta_erro_sem_estourar PASSED [  9%]
ferramentas/tests/test_config.py::test_padrao_tem_as_chaves_do_contrato PASSED [  9%]
ferramentas/tests/test_config.py::test_carregar_sem_arquivo_devolve_os_defaults PASSED [ 10%]
ferramentas/tests/test_config.py::test_config_do_projeto_sobrepoe_o_default PASSED [ 11%]
ferramentas/tests/test_config.py::test_config_quebrada_cai_no_default_e_avisa PASSED [ 11%]
ferramentas/tests/test_config.py::test_carregar_nao_compartilha_listas_com_o_padrao PASSED [ 12%]
ferramentas/tests/test_estado.py::test_novo_ciclo_grava_em_disco_e_comeca_na_descoberta PASSED [ 13%]
ferramentas/tests/test_estado.py::test_carregar_sem_estado_devolve_none PASSED [ 13%]
ferramentas/tests/test_estado.py::test_transicao_valida_avanca_e_registra PASSED [ 14%]
ferramentas/tests/test_estado.py::test_transicao_invalida_levanta PASSED [ 15%]
ferramentas/tests/test_estado.py::test_teste_volta_para_build PASSED     [ 15%]
ferramentas/tests/test_estado.py::test_todas_as_fases_do_grafo_sao_alcancaveis PASSED [ 16%]
ferramentas/tests/test_estado.py::test_desligar_preserva_o_ciclo PASSED  [ 17%]
ferramentas/tests/test_estado.py::test_registrar_diff_nao_duplica PASSED [ 17%]
ferramentas/tests/test_estado.py::test_gravacao_e_atomica PASSED         [ 18%]
ferramentas/tests/test_estado.py::test_desligar_sobre_estado_corrompido_preserva_original PASSED [ 19%]
ferramentas/tests/test_estado.py::test_registrar_diff_sobre_estado_corrompido_levanta PASSED [ 19%]
ferramentas/tests/test_estado.py::test_novo_ciclo_sobre_ciclo_ativo_levanta PASSED [ 20%]
ferramentas/tests/test_estado.py::test_novo_ciclo_com_forcar_sobrescreve_ciclo_ativo PASSED [ 21%]
ferramentas/tests/test_estado.py::test_novo_ciclo_dois_no_mesmo_dia_recebem_ids_diferentes PASSED [ 21%]
ferramentas/tests/test_hooks.py::test_motor_desligado_nao_bloqueia_nada PASSED [ 22%]
ferramentas/tests/test_hooks.py::test_acao_travada_bloqueia_com_motivo PASSED [ 23%]
ferramentas/tests/test_hooks.py::test_acao_livre_passa PASSED            [ 23%]
ferramentas/tests/test_hooks.py::test_acao_rastreada_passa_e_registra_o_diff PASSED [ 24%]
ferramentas/tests/test_hooks.py::test_stdin_invalido_bloqueia PASSED     [ 25%]
ferramentas/tests/test_hooks.py::test_modo_seco_bloqueia_escrita_em_arquivo_novo PASSED [ 25%]
ferramentas/tests/test_hooks.py::test_modo_seco_libera_leitura PASSED    [ 26%]
ferramentas/tests/test_hooks.py::test_cwd_em_subdiretorio_ainda_encontra_estado_e_bloqueia PASSED [ 26%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[null] PASSED [ 27%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[[]] PASSED [ 28%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2["texto"] PASSED [ 28%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{}] PASSED [ 29%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"cwd": 5}] PASSED [ 30%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"tool_name": "X", "tool_input": "texto em vez de objeto"}] PASSED [ 30%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[] PASSED [ 31%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"tool_name":] PASSED [ 32%]
ferramentas/tests/test_hooks.py::test_motor_desligado_nao_injeta_nada PASSED [ 32%]
ferramentas/tests/test_hooks.py::test_cartao_traz_fase_objetivo_e_invariantes PASSED [ 33%]
ferramentas/tests/test_hooks.py::test_cartao_respeita_o_teto_de_linhas PASSED [ 34%]
ferramentas/tests/test_hooks.py::test_cwd_em_subdiretorio_ainda_encontra_o_cartao PASSED [ 34%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nao_injeta_nada_e_nao_bloqueia PASSED [ 35%]
ferramentas/tests/test_hooks.py::test_avisos_de_config_tambem_respeitam_o_teto PASSED [ 36%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[0] PASSED [ 36%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[-5] PASSED [ 37%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[3] PASSED [ 38%]
ferramentas/tests/test_hooks.py::test_teto_nao_numerico_cai_no_default_sem_levantar_excecao PASSED [ 38%]
ferramentas/tests/test_hooks.py::test_teto_12_com_muitas_decisoes_e_diffs_mantem_os_cinco_invariantes PASSED [ 39%]
ferramentas/tests/test_hooks.py::test_avisos_com_teto_apertado_e_muitas_decisoes_fica_dentro_do_teto PASSED [ 40%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-post] PASSED [ 40%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-data] PASSED [ 41%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-wget-post] PASSED [ 42%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-push] PASSED  [ 42%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-push-force] PASSED [ 43%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-reset-hard] PASSED [ 44%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-rebase] PASSED [ 44%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-clean] PASSED [ 45%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-rm-rf] PASSED [ 46%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-remove-item] PASSED [ 46%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-del] PASSED   [ 47%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-drop] PASSED  [ 48%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-truncate] PASSED [ 48%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-delete-sem-where] PASSED [ 49%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-alembic] PASSED [ 50%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-django] PASSED [ 50%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-docker-push] PASSED [ 51%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-kubectl] PASSED [ 51%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-terraform] PASSED [ 52%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-npm-publish] PASSED [ 53%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-npm-global] PASSED [ 53%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-pip] PASSED   [ 54%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-winget] PASSED [ 55%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-python-rmtree] PASSED [ 55%]
ferramentas/tests/test_risco.py::test_familias_travadas[encadeado-pior-vence] PASSED [ 56%]
ferramentas/tests/test_risco.py::test_familias_travadas[redirect-para-segredo] PASSED [ 57%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-substituicao-comando] PASSED [ 57%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-bash-c-rm] PASSED [ 58%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-python-os-system] PASSED [ 59%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-request-longo] PASSED [ 59%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-redirect-aspas] PASSED [ 60%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-echo-substituicao] PASSED [ 61%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-printf-substituicao] PASSED [ 61%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-cano-bash] PASSED [ 62%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-cano-sh] PASSED [ 63%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-quebra-de-linha] PASSED [ 63%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-subst-generica] PASSED [ 64%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-subst-crase] PASSED [ 65%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-cmd-c] PASSED [ 65%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-pwsh-c] PASSED [ 66%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-powershell-encoded] PASSED [ 67%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-git-C] PASSED [ 67%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-cat-segredo] PASSED [ 68%]
ferramentas/tests/test_risco.py::test_familias_travadas[cat-chave-ssh] PASSED [ 69%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-leitura-comum] PASSED [ 69%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-novo] PASSED [ 70%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-de-teste] PASSED [ 71%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-echo-literal] PASSED [ 71%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-git-status] PASSED [ 72%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-pytest] PASSED [ 73%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-ls] PASSED [ 73%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cano-ps-grep-python] PASSED [ 74%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[nova-desconhecido-rastreado] PASSED [ 75%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[nova-comando-nulo] PASSED [ 75%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-c-fsmonitor] PASSED [ 76%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-exec-path] PASSED [ 76%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[sort-com-saida] PASSED [ 77%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[uniq-dois-posicionais] PASSED [ 78%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[find-fprint] PASSED [ 78%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-sort] PASSED [ 79%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-uniq] PASSED [ 80%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-find] PASSED [ 80%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-log-grep-rm] PASSED [ 81%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-log-grep-rm-bugfix] PASSED [ 82%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-diff-output] PASSED [ 82%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[ps-where-scriptblock] PASSED [ 83%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[find-okdir] PASSED [ 84%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-remote-set-url] PASSED [ 84%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-branch-delete] PASSED [ 85%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[grep-rm-em-string] PASSED [ 86%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[findstr-erase-em-string] PASSED [ 86%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[echo-texto-literal] PASSED [ 87%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-git-status] PASSED [ 88%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-git-log] PASSED [ 88%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-pytest] PASSED [ 89%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-ls] PASSED [ 90%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-grep] PASSED [ 90%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-cat] PASSED [ 91%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-status] PASSED [ 92%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-log] PASSED [ 92%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-diff] PASSED [ 93%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-pytest] PASSED [ 94%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-ls] PASSED [ 94%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-cat] PASSED [ 95%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-grep] PASSED [ 96%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-pwd] PASSED [ 96%]
ferramentas/tests/test_risco.py::test_nenhum_comando_de_shell_e_livre PASSED [ 97%]
ferramentas/tests/test_risco.py::test_segredo_trava_mesmo_em_arquivo_novo PASSED [ 98%]
ferramentas/tests/test_risco.py::test_leitura_de_segredo_tambem_trava PASSED [ 98%]
ferramentas/tests/test_risco.py::test_alvo_relativo_resolve_contra_a_raiz PASSED [ 99%]
ferramentas/tests/test_risco.py::test_excecao_interna_resulta_em_travado PASSED [100%]

============================= 152 passed in 4.20s =============================
```

Resultado: **152 passed** (o brief original citava 68; o número real hoje é 152 — a
suíte cresceu junto com a política do classificador, ver seção de adaptações).

---

## Passo 2 — Verificação de aceite das sete famílias travadas, pelo hook de verdade

O script `aceite/verificar_familias.py` sobe um ciclo ativo num diretório temporário e
dispara `hooks/engine_risco.py` como subprocesso — o mesmo caminho que
`hooks/hooks.json` usa em produção — para um caso de cada família travada (R1 rede, R2
git, R3 deleção, R4 banco, R5 segredo, R6 deploy, R7 instalação global). Confirma que
todos os sete saem com código 2, e acrescenta uma contraprova (leitura de arquivo
comum, ferramenta `Read`) que precisa sair com código 0 — sem essa contraprova, um
hook que bloqueasse tudo incondicionalmente passaria na verificação.

Comando:

```
python aceite/verificar_familias.py
```

Saída literal:

```
R1 (rede: POST para fora): TRAVOU  <- {'command': 'curl -X POST https://exemplo/x'}
R2 (git que sai da máquina): TRAVOU  <- {'command': 'git push origin main'}
R3 (deleção): TRAVOU  <- {'command': 'rm -rf build'}
R4 (alteração destrutiva de banco): TRAVOU  <- {'command': 'psql -c "DROP TABLE x"'}
R6 (deploy/infraestrutura): TRAVOU  <- {'command': 'terraform apply'}
R7 (instalação global): TRAVOU  <- {'command': 'npm install -g pnpm'}
R5 (segredo (.env)): TRAVOU  <- {'file_path': 'C:\\Users\\USURIO~2\\AppData\\Local\\Temp\\engine-aceite-7_lk7zvl\\.env'}
CONTRAPROVA (leitura de arquivo comum): PASSOU  <- Read C:\Users\USURIO~2\AppData\Local\Temp\engine-aceite-7_lk7zvl\leitura_comum.txt
FALHAS: nenhuma
```

Código de saída: `0`.

Resultado: as sete famílias travaram (código 2) e a contraprova passou (código 0).

---

## Passo 3 — Teto de linhas do cartão de estado

Comando:

```
python -m pytest ferramentas/tests/test_hooks.py::test_cartao_respeita_o_teto_de_linhas -v
```

Saída literal:

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Usuário\Desktop\ENGINE
plugins: anyio-4.14.0
collecting ... collected 1 item

ferramentas/tests/test_hooks.py::test_cartao_respeita_o_teto_de_linhas PASSED [100%]

============================== 1 passed in 0.04s ===============================
```

Resultado: **1 passed**, conforme o esperado no brief.

---

## O que NÃO foi verificado

Esta seção existe para não maquiar o alcance do que foi checado. A Fase 1 verifica
comportamento de unidade e de hook isolado; ela **não** verifica o modo em uso real
dentro de uma sessão do Claude Code. Especificamente, ficaram sem verificação nesta
passada:

- **Sobrevivência real do modo a 20 turnos.** Os testes provam que o estado persiste
  em disco entre chamadas de hook isoladas (subprocessos independentes), mas nenhuma
  sessão real de 20 turnos do Claude Code foi rodada com o plugin ativo para confirmar
  que o cartão de estado, os hooks e a máquina de fases se comportam corretamente ao
  longo de uma conversa longa de verdade.
- **Sobrevivência a uma compactação numa sessão de verdade.** Não foi verificado que o
  estado em `.engine/estado.json` permanece íntegro e é corretamente relido pelo hook
  `UserPromptSubmit` depois que o Claude Code compacta o contexto de uma sessão real —
  só a leitura/escrita em disco foi testada isoladamente.
- **Instalação do plugin dentro do Claude Code.** Não foi verificado que
  `hooks/hooks.json` é reconhecido, que `${CLAUDE_PLUGIN_ROOT}` resolve corretamente,
  nem que o comando `py` (usado no `hooks.json`, diferente de `sys.executable` usado
  nos testes) está disponível e aponta para o Python correto no ambiente de instalação
  real de um usuário.
- **Os quatro cenários de aceite com projetos-cobaia (Fase 3).** Nenhum projeto real
  (fora deste repositório) foi usado para exercitar o motor ponta a ponta. Isso é
  trabalho explicitamente reservado para a Fase 3, junto com os dois itens de sessão
  real acima.
- **A skill `/engine` (ligar/desligar/status) dentro da interface real do Claude
  Code.** Os testes cobrem `ferramentas/cli.py` diretamente; a integração da skill
  como o usuário de fato a invoca não foi exercitada nesta passada.

Nenhum desses itens teve sua ausência de verificação escondida ou seu critério
ajustado para "passar" — eles ficam explicitamente pendentes para a Fase 3.

---

## Veredito

A Fase 1 está pronta para o que ela se propôs a verificar: núcleo (`config`, `risco`,
`estado`, `cli`), hooks (`PreToolUse` e `UserPromptSubmit`) e a política de risco
travado-por-família — tudo isso está coberto por 152 testes verdes e por uma
verificação independente de que os hooks travam de verdade, via subprocesso, com
contraprova. **Não está pronta**, e não pretende estar, quanto aos itens listados em
"O que NÃO foi verificado" — esses são objeto da Fase 3.

---

## Adaptações feitas em relação ao `tarefa-10-brief.md`

Ver `.superpowers/sdd/briefs/tarefa-10-report.md` para o detalhamento completo. Resumo:

1. **Número de testes**: o brief esperava `68 passed`; a suíte real desta data tem
   152 testes, todos verdes. Usado o número real.
2. **Casos de família em `verificar_familias.py`**: o brief listava, junto com R1-R7,
   uma variação de comando "livre" de shell como contraprova implícita da política
   antiga. Como a política mudou para "comando de shell nunca é livre", não existe
   mais essa contraprova de shell — a contraprova usada é uma leitura de arquivo comum
   (a única superfície que ainda é `livre` por natureza).
3. **Assinatura de `estado.novo_ciclo`**: confirmada em `ferramentas/estado.py` antes
   de usar (`raiz, objetivo, agora, modo="normal", forcar=False`, levanta
   `CicloJaAtivo` se já houver ciclo ativo sem `forcar=True`).
4. **Interpretador**: o script usa `sys.executable` para invocar o hook via
   subprocesso, não `python` nem `py` — `sys.executable` é o único caminho garantido
   correto independente do ambiente, como orientado.
