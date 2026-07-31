# Aceite da Fase 2 — ENGINE

**Data:** 2026-07-31 (saídas reexecutadas na mesma data, após a revisão adversarial)

> **Passada de revisão adversarial (2026-07-31).** As saídas coladas aqui são as de
> DEPOIS das seis correções da revisão. O que mudou no que este documento afirma:
>
> - **O gate passou a cobrar de verdade.** O único caminho real de entrada em
>   BUILD/TESTE/REVISAO é rodar `cli.py fase <DESTINO>` por um comando de shell, e
>   esse comando disparava o `PostToolUse`, que gravava na trilha uma linha já
>   carimbada com a fase NOVA — o gate lia isso como evidência e nunca cobrava nada
>   em operação real. As linhas da própria CLI agora vão marcadas com `do_motor` e o
>   gate as ignora.
> - **A trilha não guarda mais segredo em claro** (senha embutida em URL, valor de
>   cabeçalho `Authorization:`, chaves de formato conhecido), nem no disco nem na
>   impressão do relatório e do verbo `retomar`.
> - **A trilha separa ciclos** (campo `ciclo` em cada linha) e nenhum relatório passa
>   de 300 linhas. Medido: uma trilha de 50 mil linhas ia a 23,5 s e 3,1 MB impressos
>   no contexto; agora dá 0,33 s e 12,9 KB, com a contagem ainda correta e a listagem
>   cortada com aviso de quantas ficaram de fora.
> - **`aceite/simular_turnos.py` deixou de ter uma verificação tautológica** e passou
>   a exercitar o quinto hook, `engine_gate.py` — verificações **(f)** e **(g)**,
>   novas. A verificação (a) agora afirma o valor literal `PLANO`: apagando as duas
>   transições do meio do roteiro, ela FALHA (confirmado por execução), o que antes
>   não acontecia.
> - **A detecção de stack parou de dar falso positivo grosseiro:** um projeto com
>   `main.py` + `dados.db` + `schema.sql` disparava `fastapi`, `postgresql` **e**
>   `sqlite` ao mesmo tempo.
> - **`agents/sentinela.md` e `agents/designer.md`** deixaram de prometer capacidades
>   que suas `tools` não têm (despachar outro revisor; falar com o MCP `open-design`).

Este documento é o registro do aceite. Ele não escreve produto — decide, com saída
real colada, se a Fase 2 está pronta. As três saídas abaixo foram rodadas nesta
data, neste repositório (`C:\Users\Usuário\Desktop\ENGINE`, branch `feat/fase-2`), e
coladas sem edição de conteúdo (só a formatação em bloco de código). Os comandos
foram rodados com `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` para a acentuação sair
legível no console — sem isso o console do Windows (cp1252) mostra mojibake nas
mensagens em português; o comportamento dos hooks e dos testes é idêntico com ou
sem essa variável, ela só afeta a exibição.

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
collecting ... collected 261 items

ferramentas/tests/test_cli.py::test_ligar_cria_o_estado PASSED           [  0%]
ferramentas/tests/test_cli.py::test_status_com_motor_desligado PASSED    [  0%]
ferramentas/tests/test_cli.py::test_desligar_depois_de_ligar PASSED      [  1%]
ferramentas/tests/test_cli.py::test_fase_invalida_reporta_erro_sem_estourar PASSED [  1%]
ferramentas/tests/test_cli.py::test_verbo_desconhecido_sai_com_erro PASSED [  1%]
ferramentas/tests/test_cli.py::test_ligar_sem_objetivo_reporta_erro_sem_estourar PASSED [  2%]
ferramentas/tests/test_cli.py::test_ligar_duas_vezes_sem_forcar_reporta_erro_sem_estourar PASSED [  2%]
ferramentas/tests/test_cli.py::test_ligar_duas_vezes_com_forcar_sobrescreve PASSED [  3%]
ferramentas/tests/test_cli.py::test_fase_sem_ciclo_ativo_reporta_erro_sem_estourar PASSED [  3%]
ferramentas/tests/test_cli.py::test_desligar_sem_ciclo_nunca_ligado_nao_estoura PASSED [  3%]
ferramentas/tests/test_cli.py::test_desligar_sem_ciclo_nao_cria_arquivo_nenhum PASSED [  4%]
ferramentas/tests/test_cli.py::test_status_depois_de_desligar_sem_ciclo_segue_limpo PASSED [  4%]
ferramentas/tests/test_cli.py::test_cli_roda_como_script_de_qualquer_diretorio PASSED [  4%]
ferramentas/tests/test_cli.py::test_cli_como_script_liga_e_desliga_um_ciclo PASSED [  5%]
ferramentas/tests/test_cli.py::test_desligar_com_estado_corrompido_nao_estoura PASSED [  5%]
ferramentas/tests/test_cli.py::test_acentuacao_sai_em_utf8 PASSED        [  6%]
ferramentas/tests/test_cli.py::test_status_com_estado_corrompido_reporta_erro_sem_estourar PASSED [  6%]
ferramentas/tests/test_cli.py::test_fase_com_estado_corrompido_reporta_erro_sem_estourar PASSED [  6%]
ferramentas/tests/test_cli.py::test_ligar_com_dry_grava_modo_dry PASSED  [  7%]
ferramentas/tests/test_cli.py::test_ligar_com_dry_e_forcar_coexistem PASSED [  7%]
ferramentas/tests/test_cli.py::test_ligar_sem_dry_grava_modo_normal PASSED [  8%]
ferramentas/tests/test_cli.py::test_ligar_detecta_cartoes_do_projeto PASSED [  8%]
ferramentas/tests/test_cli.py::test_ligar_sem_nenhuma_tecnologia_grava_cartoes_vazio PASSED [  8%]
ferramentas/tests/test_cli.py::test_retomar_sem_estado_sai_1_com_mensagem PASSED [  9%]
ferramentas/tests/test_cli.py::test_retomar_com_estado_corrompido_sai_1_sem_tocar_no_arquivo PASSED [  9%]
ferramentas/tests/test_cli.py::test_retomar_com_estado_e_trilha_imprime_fase_objetivo_e_ultima_acao PASSED [  9%]
ferramentas/tests/test_cli.py::test_relatorio_ciclo_imprime_o_objetivo PASSED [ 10%]
ferramentas/tests/test_cli.py::test_relatorio_sem_argumento_usa_ciclo_por_padrao PASSED [ 10%]
ferramentas/tests/test_cli.py::test_relatorio_fase_build_roda_com_saida_0 PASSED [ 11%]
ferramentas/tests/test_cli.py::test_relatorio_fase_inexistente_nao_estoura PASSED [ 11%]
ferramentas/tests/test_config.py::test_padrao_tem_as_chaves_do_contrato PASSED [ 11%]
ferramentas/tests/test_config.py::test_carregar_sem_arquivo_devolve_os_defaults PASSED [ 12%]
ferramentas/tests/test_config.py::test_config_do_projeto_sobrepoe_o_default PASSED [ 12%]
ferramentas/tests/test_config.py::test_config_quebrada_cai_no_default_e_avisa PASSED [ 13%]
ferramentas/tests/test_config.py::test_chave_desconhecida_e_ignorada_e_avisada PASSED [ 13%]
ferramentas/tests/test_config.py::test_config_nao_pode_esvaziar_os_padroes_de_segredo PASSED [ 13%]
ferramentas/tests/test_config.py::test_config_nao_pode_reduzir_os_padroes_de_segredo PASSED [ 14%]
ferramentas/tests/test_config.py::test_config_nao_pode_injetar_avisos PASSED [ 14%]
ferramentas/tests/test_config.py::test_padroes_de_segredo_que_nao_e_lista_avisa_e_mantem_o_default PASSED [ 14%]
ferramentas/tests/test_config.py::test_carregar_nao_compartilha_listas_com_o_padrao PASSED [ 15%]
ferramentas/tests/test_detectar.py::test_ler_cartao_devolve_as_quatro_chaves PASSED [ 15%]
ferramentas/tests/test_detectar.py::test_cartao_sem_front_matter_levanta_erro PASSED [ 16%]
ferramentas/tests/test_detectar.py::test_cartao_com_campo_obrigatorio_ausente_levanta_erro PASSED [ 16%]
ferramentas/tests/test_detectar.py::test_todos_os_cartoes_reais_sao_lidos_sem_erro PASSED [ 16%]
ferramentas/tests/test_detectar.py::test_os_doze_cartoes_do_elenco_completo_sao_validos PASSED [ 17%]
ferramentas/tests/test_detectar.py::test_projeto_com_pyproject_detecta_python_e_pytest PASSED [ 17%]
ferramentas/tests/test_detectar.py::test_projeto_vazio_devolve_lista_vazia PASSED [ 18%]
ferramentas/tests/test_detectar.py::test_resultado_e_ordenado_e_sem_duplicata PASSED [ 18%]
ferramentas/tests/test_detectar.py::test_glob_com_subdiretorio_casa PASSED [ 18%]
ferramentas/tests/test_detectar.py::test_arquivo_em_diretorio_ignorado_nao_dispara_deteccao PASSED [ 19%]
ferramentas/tests/test_detectar.py::test_cartao_com_underscore_e_ignorado PASSED [ 19%]
ferramentas/tests/test_detectar.py::test_projeto_ambiguo_nao_dispara_fastapi_postgresql_nem_sqlite PASSED [ 19%]
ferramentas/tests/test_detectar.py::test_ancoras_fortes_ainda_detectam_as_tres_tecnologias PASSED [ 20%]
ferramentas/tests/test_detectar.py::test_padrao_invalido_e_ignorado_com_seguranca PASSED [ 20%]
ferramentas/tests/test_estado.py::test_novo_ciclo_grava_em_disco_e_comeca_na_descoberta PASSED [ 21%]
ferramentas/tests/test_estado.py::test_carregar_sem_estado_devolve_none PASSED [ 21%]
ferramentas/tests/test_estado.py::test_transicao_valida_avanca_e_registra PASSED [ 21%]
ferramentas/tests/test_estado.py::test_transicao_invalida_levanta PASSED [ 22%]
ferramentas/tests/test_estado.py::test_teste_volta_para_build PASSED     [ 22%]
ferramentas/tests/test_estado.py::test_todas_as_fases_do_grafo_sao_alcancaveis PASSED [ 22%]
ferramentas/tests/test_estado.py::test_desligar_preserva_o_ciclo PASSED  [ 23%]
ferramentas/tests/test_estado.py::test_registrar_diff_nao_duplica PASSED [ 23%]
ferramentas/tests/test_estado.py::test_gravacao_e_atomica PASSED         [ 24%]
ferramentas/tests/test_estado.py::test_desligar_sobre_estado_corrompido_preserva_original PASSED [ 24%]
ferramentas/tests/test_estado.py::test_registrar_diff_sobre_estado_corrompido_levanta PASSED [ 24%]
ferramentas/tests/test_estado.py::test_novo_ciclo_sobre_ciclo_ativo_levanta PASSED [ 25%]
ferramentas/tests/test_estado.py::test_novo_ciclo_com_forcar_sobrescreve_ciclo_ativo PASSED [ 25%]
ferramentas/tests/test_estado.py::test_novo_ciclo_dois_no_mesmo_dia_recebem_ids_diferentes PASSED [ 26%]
ferramentas/tests/test_hooks.py::test_motor_desligado_nao_bloqueia_nada PASSED [ 26%]
ferramentas/tests/test_hooks.py::test_acao_travada_bloqueia_com_motivo PASSED [ 26%]
ferramentas/tests/test_hooks.py::test_acao_livre_passa PASSED            [ 27%]
ferramentas/tests/test_hooks.py::test_acao_rastreada_passa_e_registra_o_diff PASSED [ 27%]
ferramentas/tests/test_hooks.py::test_stdin_invalido_bloqueia PASSED     [ 27%]
ferramentas/tests/test_hooks.py::test_modo_seco_bloqueia_escrita_em_arquivo_novo PASSED [ 28%]
ferramentas/tests/test_hooks.py::test_modo_seco_libera_leitura PASSED    [ 28%]
ferramentas/tests/test_hooks.py::test_cwd_em_subdiretorio_ainda_encontra_estado_e_bloqueia PASSED [ 29%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[null] PASSED [ 29%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[[]] PASSED [ 29%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2["texto"] PASSED [ 30%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{}] PASSED [ 30%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"cwd": 5}] PASSED [ 31%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"tool_name": "X", "tool_input": "texto em vez de objeto"}] PASSED [ 31%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[] PASSED [ 31%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nunca_sai_1_sempre_2[{"tool_name":] PASSED [ 32%]
ferramentas/tests/test_hooks.py::test_motor_desligado_nao_injeta_nada PASSED [ 32%]
ferramentas/tests/test_hooks.py::test_cartao_traz_fase_objetivo_e_invariantes PASSED [ 32%]
ferramentas/tests/test_hooks.py::test_cartao_respeita_o_teto_de_linhas PASSED [ 33%]
ferramentas/tests/test_hooks.py::test_cwd_em_subdiretorio_ainda_encontra_o_cartao PASSED [ 33%]
ferramentas/tests/test_hooks.py::test_evento_malformado_nao_injeta_nada_e_nao_bloqueia PASSED [ 34%]
ferramentas/tests/test_hooks.py::test_avisos_de_config_tambem_respeitam_o_teto PASSED [ 34%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[0] PASSED [ 34%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[-5] PASSED [ 35%]
ferramentas/tests/test_hooks.py::test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas[3] PASSED [ 35%]
ferramentas/tests/test_hooks.py::test_teto_nao_numerico_cai_no_default_sem_levantar_excecao PASSED [ 36%]
ferramentas/tests/test_hooks.py::test_teto_12_com_muitas_decisoes_e_diffs_mantem_os_cinco_invariantes PASSED [ 36%]
ferramentas/tests/test_hooks.py::test_trilha_motor_ligado_gera_linha_com_os_campos_do_contrato PASSED [ 36%]
ferramentas/tests/test_hooks.py::test_trilha_motor_desligado_nao_gera_nada PASSED [ 37%]
ferramentas/tests/test_hooks.py::test_trilha_reclassifica_acao_travada_e_registra_a_regra PASSED [ 37%]
ferramentas/tests/test_hooks.py::test_trilha_registra_alvo_de_ferramenta_de_arquivo PASSED [ 37%]
ferramentas/tests/test_hooks.py::test_trilha_linha_corrompida_pre_existente_nao_impede_append_e_ler_avisa PASSED [ 38%]
ferramentas/tests/test_hooks.py::test_trilha_stdin_malformado_sai_0 PASSED [ 38%]
ferramentas/tests/test_hooks.py::test_trilha_evento_sem_tool_name_sai_0_sem_gravar PASSED [ 39%]
ferramentas/tests/test_hooks.py::test_trilha_cwd_em_subdiretorio_ainda_encontra_o_estado PASSED [ 39%]
ferramentas/tests/test_hooks.py::test_avisos_com_teto_apertado_e_muitas_decisoes_fica_dentro_do_teto PASSED [ 39%]
ferramentas/tests/test_hooks.py::test_salvar_motor_ligado_grava_ultima_consolidacao_e_resumo_trilha PASSED [ 40%]
ferramentas/tests/test_hooks.py::test_salvar_motor_desligado_nao_cria_nada PASSED [ 40%]
ferramentas/tests/test_hooks.py::test_salvar_estado_desligado_apos_ciclo_nao_grava_resumo PASSED [ 40%]
ferramentas/tests/test_hooks.py::test_salvar_stdin_malformado_sai_0 PASSED [ 41%]
ferramentas/tests/test_hooks.py::test_gate_cobra_na_primeira_chamada_em_build_sem_acoes PASSED [ 41%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_na_segunda_chamada_contador_persistido_entre_subprocessos PASSED [ 42%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_em_descoberta PASSED [ 42%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_quando_trilha_ja_tem_acao_da_fase[BUILD] PASSED [ 42%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_quando_trilha_ja_tem_acao_da_fase[TESTE] PASSED [ 43%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_quando_trilha_ja_tem_acao_da_fase[REVISAO] PASSED [ 43%]
ferramentas/tests/test_hooks.py::test_gate_motor_desligado_nao_cobra PASSED [ 44%]
ferramentas/tests/test_hooks.py::test_gate_stop_hook_active_nao_cobra_mesmo_quando_cobraria PASSED [ 44%]
ferramentas/tests/test_hooks.py::test_gate_stdin_malformado_sai_0 PASSED [ 44%]
ferramentas/tests/test_hooks.py::test_gate_cobra_quando_a_unica_acao_da_fase_e_a_propria_cli_do_motor PASSED [ 45%]
ferramentas/tests/test_hooks.py::test_gate_nao_cobra_quando_ha_acao_de_verdade_alem_da_cli_do_motor PASSED [ 45%]
ferramentas/tests/test_relatorio.py::test_de_ciclo_com_trilha_sintetica_contem_objetivo_decisoes_e_contagens PASSED [ 45%]
ferramentas/tests/test_relatorio.py::test_de_ciclo_sem_trilha_contem_frase_de_ausencia PASSED [ 46%]
ferramentas/tests/test_relatorio.py::test_de_ciclo_sem_estado_contem_frase_de_motor_nunca_ligou PASSED [ 46%]
ferramentas/tests/test_relatorio.py::test_de_ciclo_com_estado_corrompido_nao_levanta PASSED [ 47%]
ferramentas/tests/test_relatorio.py::test_de_fase_filtra_so_a_fase_pedida PASSED [ 47%]
ferramentas/tests/test_relatorio.py::test_de_fase_sem_acao_diz_isso PASSED [ 47%]
ferramentas/tests/test_relatorio.py::test_de_fase_traz_diffs_e_pendencias_do_estado PASSED [ 48%]
ferramentas/tests/test_relatorio.py::test_trilha_com_aviso_aparece_no_relatorio_como_nota PASSED [ 48%]
ferramentas/tests/test_relatorio.py::test_de_fase_com_argumento_estranho_nao_levanta PASSED [ 49%]
ferramentas/tests/test_relatorio.py::test_de_fase_com_estado_ausente_nao_levanta PASSED [ 49%]
ferramentas/tests/test_relatorio.py::test_relatorio_do_segundo_ciclo_nao_conta_acoes_do_primeiro PASSED [ 49%]
ferramentas/tests/test_relatorio.py::test_de_fase_do_segundo_ciclo_tambem_ignora_o_primeiro PASSED [ 50%]
ferramentas/tests/test_relatorio.py::test_linhas_sem_id_de_ciclo_sao_ignoradas_e_o_relatorio_diz_quantas PASSED [ 50%]
ferramentas/tests/test_relatorio.py::test_de_fase_respeita_o_teto_de_linhas_e_diz_quantas_omitiu PASSED [ 50%]
ferramentas/tests/test_relatorio.py::test_de_ciclo_respeita_o_teto_de_linhas PASSED [ 51%]
ferramentas/tests/test_relatorio.py::test_de_fase_redige_segredo_de_trilha_antiga_gravada_em_claro PASSED [ 51%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-post] PASSED [ 52%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-data] PASSED [ 52%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-wget-post] PASSED [ 52%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-push] PASSED  [ 53%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-push-force] PASSED [ 53%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-reset-hard] PASSED [ 54%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-rebase] PASSED [ 54%]
ferramentas/tests/test_risco.py::test_familias_travadas[R2-clean] PASSED [ 54%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-rm-rf] PASSED [ 55%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-remove-item] PASSED [ 55%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-del] PASSED   [ 55%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-drop] PASSED  [ 56%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-truncate] PASSED [ 56%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-delete-sem-where] PASSED [ 57%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-alembic] PASSED [ 57%]
ferramentas/tests/test_risco.py::test_familias_travadas[R4-django] PASSED [ 57%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-docker-push] PASSED [ 58%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-kubectl] PASSED [ 58%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-terraform] PASSED [ 59%]
ferramentas/tests/test_risco.py::test_familias_travadas[R6-npm-publish] PASSED [ 59%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-npm-global] PASSED [ 59%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-pip] PASSED   [ 60%]
ferramentas/tests/test_risco.py::test_familias_travadas[R7-winget] PASSED [ 60%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-python-rmtree] PASSED [ 60%]
ferramentas/tests/test_risco.py::test_familias_travadas[encadeado-pior-vence] PASSED [ 61%]
ferramentas/tests/test_risco.py::test_familias_travadas[redirect-para-segredo] PASSED [ 61%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-substituicao-comando] PASSED [ 62%]
ferramentas/tests/test_risco.py::test_familias_travadas[R3-bash-c-rm] PASSED [ 62%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-python-os-system] PASSED [ 62%]
ferramentas/tests/test_risco.py::test_familias_travadas[R1-curl-request-longo] PASSED [ 63%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-redirect-aspas] PASSED [ 63%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-echo-substituicao] PASSED [ 63%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-printf-substituicao] PASSED [ 64%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-cano-bash] PASSED [ 64%]
ferramentas/tests/test_risco.py::test_familias_travadas[R8-cano-sh] PASSED [ 65%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-quebra-de-linha] PASSED [ 65%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-subst-generica] PASSED [ 65%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-subst-crase] PASSED [ 66%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-cmd-c] PASSED [ 66%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-pwsh-c] PASSED [ 67%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-powershell-encoded] PASSED [ 67%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-git-C] PASSED [ 67%]
ferramentas/tests/test_risco.py::test_familias_travadas[nova-cat-segredo] PASSED [ 68%]
ferramentas/tests/test_risco.py::test_familias_travadas[cat-chave-ssh] PASSED [ 68%]
ferramentas/tests/test_risco.py::test_familias_travadas[R9-edit-estado] PASSED [ 68%]
ferramentas/tests/test_risco.py::test_familias_travadas[R9-write-config] PASSED [ 69%]
ferramentas/tests/test_risco.py::test_familias_travadas[R9-notebookedit-painel] PASSED [ 69%]
ferramentas/tests/test_risco.py::test_familias_travadas[R9-caminho-aninhado] PASSED [ 70%]
ferramentas/tests/test_risco.py::test_familias_travadas[R9-redirect-shell] PASSED [ 70%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-akia] PASSED [ 70%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-sk] PASSED [ 71%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-ghp] PASSED [ 71%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-github-pat] PASSED [ 72%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-slack] PASSED [ 72%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-chave-privada] PASSED [ 72%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-jwt] PASSED [ 73%]
ferramentas/tests/test_risco.py::test_familias_travadas[R5-conteudo-em-new-string] PASSED [ 73%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-leitura-comum] PASSED [ 73%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-novo] PASSED [ 74%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-de-teste] PASSED [ 74%]
ferramentas/tests/test_risco.py::test_familias_livres[painel-leitura-estado] PASSED [ 75%]
ferramentas/tests/test_risco.py::test_familias_livres[painel-leitura-config] PASSED [ 75%]
ferramentas/tests/test_risco.py::test_familias_livres[arquivo-novo-conteudo-comum] PASSED [ 75%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-echo-literal] PASSED [ 76%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-git-status] PASSED [ 76%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-pytest] PASSED [ 77%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[shell-ls] PASSED [ 77%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cano-ps-grep-python] PASSED [ 77%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[nova-desconhecido-rastreado] PASSED [ 78%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[nova-comando-nulo] PASSED [ 78%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-c-fsmonitor] PASSED [ 78%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-exec-path] PASSED [ 79%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[sort-com-saida] PASSED [ 79%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[uniq-dois-posicionais] PASSED [ 80%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[find-fprint] PASSED [ 80%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-sort] PASSED [ 80%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-uniq] PASSED [ 81%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-find] PASSED [ 81%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-log-grep-rm] PASSED [ 81%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-log-grep-rm-bugfix] PASSED [ 82%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-diff-output] PASSED [ 82%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[ps-where-scriptblock] PASSED [ 83%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[find-okdir] PASSED [ 83%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-remote-set-url] PASSED [ 83%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[git-branch-delete] PASSED [ 84%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[grep-rm-em-string] PASSED [ 84%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[findstr-erase-em-string] PASSED [ 85%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[echo-texto-literal] PASSED [ 85%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-git-status] PASSED [ 85%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-git-log] PASSED [ 86%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-pytest] PASSED [ 86%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-ls] PASSED [ 86%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-grep] PASSED [ 87%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[permitido-cat] PASSED [ 87%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-status] PASSED [ 88%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-log] PASSED [ 88%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-git-diff] PASSED [ 88%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-pytest] PASSED [ 89%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-ls] PASSED [ 89%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-cat] PASSED [ 90%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-grep] PASSED [ 90%]
ferramentas/tests/test_risco.py::test_default_e_rastreado[cotidiano-pwd] PASSED [ 90%]
ferramentas/tests/test_risco.py::test_nenhum_comando_de_shell_e_livre PASSED [ 91%]
ferramentas/tests/test_risco.py::test_segredo_trava_mesmo_em_arquivo_novo PASSED [ 91%]
ferramentas/tests/test_risco.py::test_leitura_de_segredo_tambem_trava PASSED [ 91%]
ferramentas/tests/test_risco.py::test_alvo_relativo_resolve_contra_a_raiz PASSED [ 92%]
ferramentas/tests/test_risco.py::test_sobrescrever_teste_existente_e_rastreado PASSED [ 92%]
ferramentas/tests/test_risco.py::test_editar_teste_existente_fora_de_tests_tambem_e_rastreado PASSED [ 93%]
ferramentas/tests/test_risco.py::test_criar_teste_novo_continua_livre PASSED [ 93%]
ferramentas/tests/test_risco.py::test_escrita_no_painel_trava_com_caminho_absoluto PASSED [ 93%]
ferramentas/tests/test_risco.py::test_leitura_do_painel_continua_livre_com_caminho_absoluto PASSED [ 94%]
ferramentas/tests/test_risco.py::test_arquivo_chamado_engineering_nao_e_o_painel PASSED [ 94%]
ferramentas/tests/test_risco.py::test_excecao_interna_resulta_em_travado PASSED [ 95%]
ferramentas/tests/test_trilha.py::test_caminho_aponta_para_engine_trilha_jsonl PASSED [ 95%]
ferramentas/tests/test_trilha.py::test_registrar_cria_diretorio_e_grava_uma_linha PASSED [ 95%]
ferramentas/tests/test_trilha.py::test_registrar_faz_append_sem_apagar_linha_anterior PASSED [ 96%]
ferramentas/tests/test_trilha.py::test_ler_arquivo_ausente_devolve_listas_vazias PASSED [ 96%]
ferramentas/tests/test_trilha.py::test_ler_pula_linha_corrompida_e_reporta_aviso PASSED [ 96%]
ferramentas/tests/test_trilha.py::test_linha_corrompida_pre_existente_nao_impede_novo_append PASSED [ 97%]
ferramentas/tests/test_trilha.py::test_ler_linha_corrompida_que_nao_e_objeto_json_vira_aviso PASSED [ 97%]
ferramentas/tests/test_trilha.py::test_registrar_redige_senha_embutida_em_url PASSED [ 98%]
ferramentas/tests/test_trilha.py::test_registrar_redige_valor_do_cabecalho_authorization PASSED [ 98%]
ferramentas/tests/test_trilha.py::test_redigir_cobre_os_padroes_de_chave_conhecida_do_modulo_de_risco PASSED [ 98%]
ferramentas/tests/test_trilha.py::test_redigir_nao_mexe_em_comando_sem_credencial PASSED [ 99%]
ferramentas/tests/test_trilha.py::test_registrar_nunca_propaga_excecao_com_diretorio_sem_permissao PASSED [ 99%]
ferramentas/tests/test_trilha.py::test_registrar_nunca_propaga_excecao_com_escrita_falhando PASSED [100%]

============================ 261 passed in 12.00s =============================
```

Resultado: **261 passed** (a Fase 1 fechou com 152; a Fase 2 chegou a 247 ao longo
das tarefas F2-T1 a F2-T7 — detectar, trilha, relatório, os três hooks novos, os
verbos novos da CLI, R9-conteúdo e a família de testes dos 12 cartões; a revisão
adversarial somou 14: o gate cobrando pelo caminho REAL da CLI, a redação de
credencial na trilha, a separação por ciclo, o teto de 300 linhas do relatório e o
projeto ambíguo da detecção de stack).

Um único teste pré-existente foi alterado, e por obrigação:
`test_trilha_motor_ligado_gera_linha_com_os_seis_campos` afirmava
`set(linha.keys()) == {seis campos}` — não há como gravar o id do ciclo na linha
(exigência da correção da separação por ciclo) e manter o conjunto em seis. Ele
virou `test_trilha_motor_ligado_gera_linha_com_os_campos_do_contrato`, com os sete
campos e a checagem de que o id gravado é o do ciclo corrente. Nenhum outro teste
existente foi tocado.

---

## Passo 2 — Verificação de aceite das nove famílias travadas, pelo hook de verdade

Mesmo script da Fase 1 (`aceite/verificar_familias.py`), sem alteração nesta fase —
continua disparando `hooks/engine_risco.py` como subprocesso para um caso de cada
família travada, mais R9 (escrita no painel de controle) e a contraprova de leitura
comum.

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
R5 (segredo (.env)): TRAVOU  <- {'file_path': 'C:\\Users\\USURIO~2\\AppData\\Local\\Temp\\engine-aceite-gl0has0m\\.env'}
R9 (escrita no painel de controle do motor (.engine/)): TRAVOU  <- {'file_path': 'C:\\Users\\USURIO~2\\AppData\\Local\\Temp\\engine-aceite-gl0has0m\\.engine\\estado.json'}
CONTRAPROVA (leitura de arquivo comum): PASSOU  <- Read C:\Users\USURIO~2\AppData\Local\Temp\engine-aceite-gl0has0m\leitura_comum.txt
FALHAS: nenhuma
```

Código de saída: `0`.

Resultado: as nove famílias travaram (código 2) e a contraprova passou (código 0).
(A família R9 já tinha sido incorporada ao script durante a correção final da Fase 1
— ver `CHANGELOG.md`, entrada de 2026-07-30 — por isso já aparece aqui também, sem
mudança nesta passada.)

---

## Passo 3 — `aceite/simular_turnos.py` (NOVO nesta fase)

Este é o artefato central da Tarefa F2-T8. Ele fecha, na mecânica, o critério que a
Fase 1 declarou explicitamente **não verificado**: *"o modo sobrevive a 20 turnos e
a uma compactação"* (ver `aceite/fase-1.md`, seção "O que NÃO foi verificado",
primeiros dois itens).

O script sobe um ciclo num diretório temporário sintético e, para cada um dos 20
turnos, dispara os hooks REAIS por subprocesso na mesma ordem em que o Claude Code
os chamaria dentro de um turno: `engine_contexto.py` (UserPromptSubmit) →
`engine_risco.py` (PreToolUse) → `engine_trilha.py` (PostToolUse, só quando a ação
não foi bloqueada). Os 20 eventos são variados de propósito — leitura, escrita de
arquivo novo, escrita em arquivo que já existe, e um comando travado (`git push
origin main`, família R2) no turno 12. No turno 10, entre um turno e o outro, o
script dispara `engine_salvar.py` (PreCompact), simulando a compactação de
contexto. No meio da sequência (turnos 4 e 8) a fase avança de verdade via
`ferramentas.estado.transicionar` + `estado.gravar` (DESCOBERTA → ANALISE → PLANO),
para provar que a fase escolhida se MANTÉM nos turnos seguintes — inclusive depois
da compactação do turno 10.

Depois dos 20 turnos, o script exercita o quinto hook, `engine_gate.py` (Stop) — o
único que BLOQUEIA a saída do Claude, e o que a revisão adversarial apontou como não
exercitado por este aceite. A entrada na fase BUILD é feita pelo caminho REAL de
operação (`ferramentas/cli.py fase BUILD` em subprocesso, seguido do `PostToolUse`
sobre o mesmo comando — exatamente o caminho que cegava o gate), e o Stop é disparado
duas vezes.

Ao final, o script verifica sete coisas e imprime uma linha por verificação:

- **(a)** a fase ao fim dos 20 turnos é `PLANO` — **valor literal**, não a comparação
  com o que o disco disser (a versão anterior comparava o cartão do turno 20 com a
  fase lida do mesmo disco que o cartão leu: apagando as duas transições do meio, ela
  continuava verde). O cartão do turno 20 tem de trazer essa fase e o objetivo;
- **(b)** o cartão do turno 20 respeita o teto de linhas;
- **(c)** a trilha tem o número esperado de linhas (um registro por turno NÃO
  bloqueado — ação bloqueada nunca executa, nunca gera `PostToolUse`);
- **(d)** `ultima_consolidacao` foi gravada pelo `PreCompact` do turno 10;
- **(e)** a ação travada do turno 12 foi mesmo bloqueada (código de saída 2);
- **(f)** o `Stop` COBRA evidência na primeira parada em BUILD (código 2), mesmo
  havendo na trilha uma linha carimbada com BUILD — porque essa linha é a chamada da
  própria CLI do motor, marcada `do_motor`;
- **(g)** o `Stop` NÃO cobra na segunda parada na mesma fase (código 0): o contador
  `cobrancas_por_fase` sobreviveu em disco entre dois subprocessos.

Comando:

```
python aceite/simular_turnos.py
```

Saída literal:

```
turno 01 [leitura           ] contexto=0 risco=0 trilha=0
turno 02 [escrita-nova      ] contexto=0 risco=0 trilha=0
turno 03 [escrita-existente ] contexto=0 risco=0 trilha=0
turno 04 [leitura           ] contexto=0 risco=0 trilha=0
          -- transição de fase: DESCOBERTA -> ANALISE (via estado.transicionar + estado.gravar)
turno 05 [escrita-nova      ] contexto=0 risco=0 trilha=0
turno 06 [escrita-existente ] contexto=0 risco=0 trilha=0
turno 07 [leitura           ] contexto=0 risco=0 trilha=0
turno 08 [escrita-nova      ] contexto=0 risco=0 trilha=0
          -- transição de fase: ANALISE -> PLANO (via estado.transicionar + estado.gravar)
turno 09 [escrita-existente ] contexto=0 risco=0 trilha=0
turno 10 [leitura           ] contexto=0 risco=0 trilha=0
          -- PreCompact (engine_salvar.py) exit=0
turno 11 [escrita-nova      ] contexto=0 risco=0 trilha=0
turno 12 [comando-travado   ] contexto=0 risco=2 (TRAVADO) trilha=n/a (bloqueada)
turno 13 [leitura           ] contexto=0 risco=0 trilha=0
turno 14 [escrita-existente ] contexto=0 risco=0 trilha=0
turno 15 [escrita-nova      ] contexto=0 risco=0 trilha=0
turno 16 [leitura           ] contexto=0 risco=0 trilha=0
turno 17 [escrita-existente ] contexto=0 risco=0 trilha=0
turno 18 [leitura           ] contexto=0 risco=0 trilha=0
turno 19 [escrita-nova      ] contexto=0 risco=0 trilha=0
turno 20 [leitura           ] contexto=0 risco=0 trilha=0
          -- transição pela CLI REAL: PLANO -> BUILD (cli.py exit=0)
          -- PostToolUse sobre o comando da própria CLI (exit=0; a linha vai para a trilha marcada do_motor)
          -- Stop (engine_gate.py) 1ª parada em BUILD: exit=2 (esperado 2 = COBROU)
          -- Stop (engine_gate.py) 2ª parada em BUILD: exit=0 (esperado 0 = não cobra de novo)

== Verificações finais ==
(a) fase ao fim dos 20 turnos é 'PLANO' (lida: 'PLANO') e o cartão do turno 20 traz essa fase e o objetivo: OK
(b) cartão do turno 20 respeita o teto de linhas (10 <= 40): OK
(c) trilha tem o número esperado de linhas (19 == 19): OK
(d) 'ultima_consolidacao' gravada pelo PreCompact ('2026-07-31T01:15:06'): OK
(e) ação travada do turno 12 (git push origin main) saiu com código 2: OK
(f) gate cobra evidência na 1ª parada em BUILD (saída 2, esperado 2): OK
(g) gate não cobra na 2ª parada na mesma fase (saída 0, esperado 0): OK

FALHAS: nenhuma
```

Código de saída: `0`.

Resultado: as sete verificações passaram. O estado (fase, objetivo, cartão) e a
trilha sobreviveram aos 20 turnos e à compactação simulada; a ação travada continuou
travada em meio à sequência; e o gate cobrou uma vez — e só uma — na fase em que a
única ação registrada era a chamada da própria CLI do motor.

---

## O que NÃO foi verificado

Esta seção existe para não maquiar o alcance do que foi checado. A Fase 2 fecha, na
MECÂNICA, o critério "sobrevive a 20 turnos e a uma compactação" — mas "mecânica"
aqui quer dizer subprocessos isolados chamando os hooks reais em sequência dentro de
um script, não uma sessão de verdade do Claude Code. Especificamente, ficaram sem
verificação nesta passada:

- **A instalação real do plugin numa sessão do Claude Code.** Não foi verificado que
  `hooks/hooks.json` é reconhecido pelo Claude Code, que `${CLAUDE_PLUGIN_ROOT}`
  resolve para o caminho certo, nem que os cinco hooks disparam nos eventos
  corretos (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`)
  dentro de uma instalação de usuário de verdade.
- **A prova de que o Claude Code de fato injeta o stdout do `UserPromptSubmit` no
  contexto.** `aceite/simular_turnos.py` confirma que `engine_contexto.py` escreve
  o texto certo no stdout (e que esse texto chega intacto turno após turno), mas não
  prova que o Claude Code realmente lê esse stdout e o injeta como contexto visível
  ao modelo dentro de uma conversa real — isso depende do comportamento documentado
  do host, não do hook.
- **O comportamento do `Stop` (`engine_gate.py`) bloqueando de verdade numa sessão
  real.** Depois da revisão adversarial o gate deixou de ser um hook não exercitado:
  `aceite/simular_turnos.py` agora o dispara pelo caminho real de entrada na fase
  (verificações (f) e (g)), e a suíte cobre o cenário que o cegava. O que continua
  **não** verificado é o outro lado do contrato, que depende do host: nenhuma sessão
  real do Claude Code chegou ao fim de uma fase BUILD/TESTE/REVISAO sem evidência
  para confirmar que a saída 2 de fato impede o Claude de parar e que a mensagem de
  cobrança chega legível ao modelo. Saída 2 e stderr certos: provado aqui. Efeito
  disso dentro de uma conversa: Fase 3.
- **A redação de segredo cobre o que a trilha ESCREVE, não tudo que existe.**
  `trilha.redigir` reconhece senha embutida em URL, valor de `Authorization:` e as
  chaves de formato conhecido de `ferramentas/risco.py` (`sk-`, `ghp_`,
  `github_pat_`, `AKIA`, `xox…`, JWT, `BEGIN … PRIVATE KEY`). Um segredo sem forma
  reconhecível — uma senha solta num argumento `--password minhasenha`, um token
  proprietário sem prefixo — continua indo para a trilha em claro. Não há como
  reconhecer por forma o que não tem forma; fechar isso exigiria política de
  conteúdo, não padrão de texto.
- **Os quatro cenários de aceite com projetos-cobaia (Fase 3).** Nenhum projeto real
  (fora deste repositório) foi usado para exercitar o motor ponta a ponta com um
  hospedeiro de verdade. Isso continua reservado para a Fase 3, como já registrado
  em `aceite/fase-1.md`.
- **O fato de `hooks/hooks.json` usar `py`, que só existe no Windows.** Os testes e
  os três scripts de aceite (`verificar_familias.py`, `simular_turnos.py`, e o teste
  do teto de linhas) usam `sys.executable` de propósito — o único caminho garantido
  correto independente do ambiente (ver `aceite/fase-1.md`, adaptação 4). Mas
  `hooks/hooks.json`, o arquivo que o Claude Code de fato lê para saber como invocar
  cada hook, continua usando o lançador `py`, que é específico do instalador do
  Python no Windows e não existe em Linux/macOS nem em toda instalação Windows. Uma
  instalação do plugin fora do Windows (ou num Windows sem o lançador `py`)
  quebraria todos os cinco hooks por esse motivo, e nada nesta fase testa isso — é
  uma lacuna real de portabilidade, não uma formalidade.

Nenhum desses itens teve sua ausência de verificação escondida ou seu critério
ajustado para "passar" — eles ficam explicitamente pendentes para a Fase 3, ou como
limitações conhecidas e não corrigidas nesta fase (o lançador `py` e o alcance da
redação por forma).

---

## Veredito

A Fase 2 está pronta para o que ela se propôs a verificar: os módulos novos
(`detectar`, `trilha`, `relatorio`), os três hooks novos (`engine_trilha.py`,
`engine_salvar.py`, `engine_gate.py`), os verbos novos da CLI (`retomar`, `--dry`,
`relatorio`), os cinco papéis e os nove cartões restantes — tudo isso está coberto
por 261 testes verdes, pela verificação independente das nove famílias travadas via
subprocesso (`aceite/verificar_familias.py`), e pelo roteiro de 20 turnos com
compactação simulada e exercício do gate (`aceite/simular_turnos.py`), que fecha
explicitamente o critério que a Fase 1 tinha deixado em aberto.

A revisão adversarial desta data mudou o veredito em um ponto que importa: antes
dela, o gate — a única peça do motor que BLOQUEIA — não cobrava nada em operação
real, e nem a suíte nem o aceite pegavam isso, porque os dois entravam na fase por
um caminho que ninguém usa de verdade. O que fechou o buraco não foi mais teste sobre
a mesma superfície, foi testar pelo caminho real.

**Não está pronta**, e não pretende estar, quanto aos itens listados em "O que NÃO
foi verificado" acima — em particular, a instalação e o uso reais dentro de uma
sessão do Claude Code, e o lançador `py` em `hooks/hooks.json` que não existe fora
do Windows. Ambos são riscos conhecidos e não maquiados; o segundo, em especial, é
uma lacuna de portabilidade concreta que qualquer instalação fora do Windows vai
sentir imediatamente — não é um "não verificado" de baixo risco.
