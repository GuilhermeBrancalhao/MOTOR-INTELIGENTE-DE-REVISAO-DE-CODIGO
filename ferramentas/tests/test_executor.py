"""Testes de `ferramentas/executor.py`: veredito de aceite decidido por evidência.

Cada teste nomeia, no próprio docstring, a MUTAÇÃO que o derrubaria — é a única forma
de saber se ele prova alguma coisa ou se só acompanha o código.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import executor, trilha  # noqa: E402


def _py(codigo: str) -> str:
    """Comando de shell que roda `codigo` no MESMO interpretador da suíte.

    Com o caminho entre aspas porque ele contém espaço em muitas máquinas, e sempre
    aspas simples dentro do código: aspas duplas aninhadas quebram no `cmd.exe`.
    """
    return f'"{sys.executable}" -c "{codigo}"'


def _config_sem_extra() -> dict:
    """Configuração mínima aceita por `risco.classificar` (sem travas adicionais)."""
    return {"padroes_segredo": [], "travado_extra": []}


# ---------------------------------------------------------------------------
# O item 1 do aceite: código de saída decide, e só ele
# ---------------------------------------------------------------------------


def test_comando_que_sai_zero_produz_aprovado(tmp_path):
    """Mutação que derruba: `julgar` devolvendo REPROVADO para 0, ou `executar`
    ignorando `returncode` e chutando o resultado."""
    veredito = executor.executar(
        _py("raise SystemExit(0)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.APROVADO
    assert veredito.codigo_saida == 0
    assert veredito.aprovado is True
    assert veredito.houve_execucao is True


def test_comando_que_sai_um_produz_reprovado(tmp_path):
    """Mutação que derruba: `julgar` devolvendo APROVADO para qualquer código, ou
    `executar` tratando "rodou até o fim" como sucesso."""
    veredito = executor.executar(
        _py("raise SystemExit(1)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida == 1
    assert veredito.aprovado is False


def test_codigo_de_saida_diferente_de_zero_e_um_tambem_reprova(tmp_path):
    """Mutação que derruba: `julgar` comparando `codigo == 1` em vez de `codigo == 0`
    (pytest sai 2, 3, 4, 5 em situações distintas, e nenhuma delas é sucesso)."""
    veredito = executor.executar(
        _py("raise SystemExit(5)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida == 5


def test_julgar_olha_o_codigo_e_mais_nada():
    """Mutação que derruba: qualquer parâmetro extra em `julgar` (texto da saída,
    duração, nome do comando) influenciando o resultado."""
    assert executor.julgar(0) == executor.APROVADO
    for codigo in (1, 2, 5, 127, -1, 3221225786):
        assert executor.julgar(codigo) == executor.REPROVADO, codigo


def test_saida_gritando_falha_com_codigo_zero_ainda_aprova(tmp_path):
    """Mutação que derruba: reintroduzir heurística de texto (`if 'FAILED' in saida`).

    É o coração do ciclo: interpretar a saída devolve o veredito ao julgamento do
    modelo, que é o que este módulo existe para eliminar."""
    veredito = executor.executar(
        _py("print('FAILED - 3 errors - ERROR: tudo quebrou'); raise SystemExit(0)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.APROVADO
    assert "FAILED" in veredito.saida  # a evidência fica visível para o humano


def test_saida_dizendo_ok_com_codigo_um_ainda_reprova(tmp_path):
    """Mutação que derruba: a mesma heurística de texto pelo outro lado
    (`if 'passed' in saida: APROVADO`)."""
    veredito = executor.executar(
        _py("print('OK - 100 passed - tudo verde'); raise SystemExit(1)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert "100 passed" in veredito.saida


# ---------------------------------------------------------------------------
# O item 2 do aceite: veredito não existe sem código de saída capturado
# ---------------------------------------------------------------------------


def test_veredito_nao_pode_ser_construido_sem_codigo_de_saida():
    """Mutação que derruba: dar um default a `codigo_saida` (`= None`, `= 0`) no
    dataclass. Aí o veredito passa a existir sem evidência nenhuma, que é a opinião
    disfarçada de resultado que este ciclo fecha."""
    with pytest.raises(TypeError):
        executor.Veredito(resultado=executor.APROVADO, comando="pytest -q")


def test_veredito_aprovado_com_codigo_ausente_e_recusado():
    """Mutação que derruba: remover a checagem de `codigo_saida is None` do
    `__post_init__`. Sem ela, `None` vira a porta dos fundos do default."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.APROVADO,
            codigo_saida=None,
            comando="pytest -q",
            motivo="tempo esgotado",
        )


def test_veredito_sem_codigo_exige_motivo_explicito():
    """Mutação que derruba: aceitar REPROVADO sem código E sem motivo — um veredito
    vermelho órfão, que ninguém sabe se foi tempo, risco ou falha de infraestrutura."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.REPROVADO, codigo_saida=None, comando="pytest -q"
        )


def test_veredito_que_contradiz_o_codigo_capturado_e_recusado():
    """Mutação que derruba: tirar do `__post_init__` a comparação com `julgar`. Sem
    ela, um chamador monta APROVADO por cima de um código 1 e a estrutura deixa."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.APROVADO, codigo_saida=1, comando="pytest -q"
        )
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.REPROVADO, codigo_saida=0, comando="pytest -q"
        )


def test_codigo_de_saida_booleano_e_recusado():
    """Mutação que derruba: remover a checagem de `bool`. Como `bool` é `int` em
    Python, `codigo_saida=False` passaria como o código 0 — um APROVADO construído a
    partir de um "deu certo?" de quem chamou."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.APROVADO, codigo_saida=False, comando="pytest -q"
        )


def test_codigo_de_saida_de_tipo_errado_e_recusado():
    """Mutação que derruba: aceitar `"0"` (texto) como código. Uma string vinda de um
    JSON mal lido nunca casaria `== 0` e reprovaria tudo em silêncio."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(
            resultado=executor.APROVADO, codigo_saida="0", comando="pytest -q"
        )


def test_resultado_fora_do_conjunto_fechado_e_recusado():
    """Mutação que derruba: abrir `RESULTADOS` para um terceiro valor. "PARCIAL" é a
    gaveta onde o caso duvidoso é guardado sem ninguém decidir nada."""
    with pytest.raises(executor.VereditoSemEvidencia):
        executor.Veredito(resultado="PARCIAL", codigo_saida=0, comando="pytest -q")


# ---------------------------------------------------------------------------
# Timeout
# ---------------------------------------------------------------------------


def test_comando_que_trava_reprova_por_tempo_sem_travar_o_programa(tmp_path):
    """Mutação que derruba: passar `timeout=None` ao `subprocess`, ou capturar
    `TimeoutExpired` e devolver APROVADO. O teste mede o relógio: um executor sem
    prazo ficaria 60 s parado aqui."""
    inicio = time.monotonic()
    veredito = executor.executar(
        _py("import time; time.sleep(60)"),
        raiz=tmp_path,
        timeout_s=2,
        config_efetiva=_config_sem_extra(),
    )
    decorrido = time.monotonic() - inicio

    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida is None
    assert veredito.houve_execucao is False
    assert "tempo esgotado" in veredito.motivo
    assert decorrido < 30, f"o timeout não interrompeu: {decorrido:.1f}s"


def test_timeout_mata_a_arvore_e_nao_so_o_filho_direto(tmp_path):
    """Mutação que derruba: tirar o `/T` do `taskkill` (ou o `killpg` no POSIX) e matar
    só o filho direto.

    Medido antes de escrever o teste, com a mutação aplicada: o neto sobreviveu ao
    encerramento e escreveu o marcador **depois** de o veredito já ter saído, e o
    `executar` levou 7,1 s em vez de 2,2 s — porque o neto continuava segurando o cano
    da saída. Um comando de aceite que roda `pytest` ou um build spawna netos o tempo
    todo; encerrar só o shell deixa a máquina trabalhando para um veredito que já foi
    dado."""
    (tmp_path / "neto.py").write_text(
        "import time\ntime.sleep(4)\nopen('neto-marcador.txt','w').close()\n",
        encoding="utf-8",
    )
    (tmp_path / "avo.py").write_text(
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, 'neto.py'])\n"
        "time.sleep(60)\n",
        encoding="utf-8",
    )

    veredito = executor.executar(
        f'"{sys.executable}" avo.py',
        raiz=tmp_path,
        timeout_s=1.5,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO

    time.sleep(7)  # tempo de sobra para o neto acordar e escrever, se estiver vivo
    assert not (tmp_path / "neto-marcador.txt").exists(), (
        "o neto sobreviveu ao timeout e continuou trabalhando"
    )


def test_timeout_ausente_e_recusado(tmp_path):
    """Mutação que derruba: dar a `timeout_s` o default `None` e repassá-lo ao
    `subprocess` — que entende `None` como "espere para sempre"."""
    with pytest.raises(executor.TimeoutObrigatorio):
        executor.executar(
            _py("print(1)"),
            raiz=tmp_path,
            timeout_s=None,
            config_efetiva=_config_sem_extra(),
        )


def test_timeout_nao_positivo_ou_infinito_e_recusado(tmp_path):
    """Mutação que derruba: validar só `is None` e deixar passar `0`, `-1` ou
    `float('inf')` — os três são "sem prazo" escritos de outro jeito."""
    for prazo in (0, -1, float("inf"), float("nan"), "60", True):
        with pytest.raises(executor.TimeoutObrigatorio):
            executor.executar(
                _py("print(1)"),
                raiz=tmp_path,
                timeout_s=prazo,
                config_efetiva=_config_sem_extra(),
            )


# ---------------------------------------------------------------------------
# Teto de saída
# ---------------------------------------------------------------------------


def test_saida_longa_e_cortada_no_teto_com_aviso_do_que_ficou_de_fora(tmp_path):
    """Mutação que derruba: remover o corte (a saída inteira volta ao contexto) ou
    cortar sem dizer quanto ficou de fora — aí o leitor não sabe que houve corte."""
    veredito = executor.executar(
        _py("print('x' * 50000)"),
        raiz=tmp_path,
        timeout_s=60,
        teto_saida=500,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.APROVADO
    assert veredito.saida.count("x") <= 500
    assert "omitido" in veredito.saida
    assert "50000" not in veredito.saida  # não é o texto inteiro disfarçado


def test_corte_guarda_o_comeco_e_o_fim():
    """Mutação que derruba: cortar só pelo fim (`texto[:teto]`). O fim da saída de uma
    suíte é onde mora a linha de resumo; jogá-la fora é perder a conclusão."""
    texto = "COMECO" + ("m" * 5000) + "FIM"
    cortado = executor.preparar_saida(texto, teto=200)
    assert cortado.startswith("COMECO")
    assert cortado.endswith("FIM")
    assert "omitido" in cortado


def test_preparar_saida_nao_mexe_no_texto_que_cabe():
    """Mutação que derruba: cortar sempre, mesmo quando não precisa — a saída curta de
    um aceite viraria um texto com aviso de corte que não aconteceu."""
    assert executor.preparar_saida("3 passed in 0.10s", teto=200) == "3 passed in 0.10s"


def test_teto_de_saida_nao_positivo_e_recusado(tmp_path):
    """Mutação que derruba: aceitar `teto_saida=0` e devolver saída vazia sempre — o
    teto viraria uma forma silenciosa de apagar a evidência."""
    with pytest.raises(ValueError):
        executor.executar(
            _py("print(1)"),
            raiz=tmp_path,
            timeout_s=60,
            teto_saida=0,
            config_efetiva=_config_sem_extra(),
        )


# ---------------------------------------------------------------------------
# Redação de segredo
# ---------------------------------------------------------------------------


def test_credencial_impressa_pelo_comando_nao_chega_em_claro_na_trilha(tmp_path):
    """Mutação que derruba: registrar `saida` crua na trilha. O comando de aceite roda
    o build do projeto do cliente e imprime o que quiser — inclusive a chave que ele
    usa para publicar."""
    # A chave é montada por concatenação para que ela não exista no TEXTO do comando
    # (senão a família R5 travaria a execução, e o teste testaria outra coisa).
    veredito = executor.executar(
        _py("print('AK' + 'IA' + 'B' * 16)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    segredo = "AKIA" + "B" * 16
    assert veredito.resultado == executor.APROVADO
    assert segredo not in veredito.saida
    assert trilha.MARCA_REDIGIDO in veredito.saida

    bruto = trilha.caminho(tmp_path).read_text(encoding="utf-8")
    assert segredo not in bruto
    assert trilha.MARCA_REDIGIDO in bruto


def test_redacao_acontece_antes_do_corte():
    """Mutação que derruba: inverter a ordem (`preparar_saida` cortando e só depois
    redigindo). Uma credencial que cai em cima da fronteira do corte perde o rabo,
    deixa de casar o padrão que a reconhece, e o pedaço que sobrou vai em claro."""
    segredo = "AKIA" + "B" * 16
    texto = ("a" * 45) + segredo + ("b" * 5000)
    cortado = executor.preparar_saida(texto, teto=100)
    assert "AKIA" not in cortado, "fragmento de credencial sobreviveu ao corte"
    assert segredo not in cortado


# ---------------------------------------------------------------------------
# Recusa por risco: consulta ANTES de executar
# ---------------------------------------------------------------------------


def test_comando_travado_pela_politica_de_risco_nao_chega_a_executar(tmp_path):
    """Mutação que derruba: executar primeiro e classificar depois (ou não classificar).

    A prova é o efeito colateral: `del` apaga o arquivo se rodar. Autonomia de processo
    não é autonomia de risco — um plano-mestre não ganha o direito de rodar deleção só
    porque o campo se chama "aceite"."""
    alvo = tmp_path / "marcador.txt"
    alvo.write_text("nao me apague", encoding="utf-8")

    veredito = executor.executar(
        "del marcador.txt",
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )

    assert alvo.is_file(), "o comando travado executou mesmo assim"
    assert alvo.read_text(encoding="utf-8") == "nao me apague"
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida is None
    assert "R3" in veredito.motivo
    assert "NÃO executado" in veredito.motivo


def test_comando_que_mexe_no_painel_do_motor_e_recusado(tmp_path):
    """Mutação que derruba: classificar com uma lista própria de padrões em vez de
    chamar `risco.classificar` — a família R9 (escrita em `.engine/`) some, e o aceite
    vira o caminho para desligar o motor que o está avaliando."""
    veredito = executor.executar(
        "type .engine\\estado.json",
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida is None
    assert "R9" in veredito.motivo


def test_recusa_por_risco_fica_registrada_na_trilha_como_travada(tmp_path):
    """Mutação que derruba: sair cedo sem registrar. Recusa que não aparece no
    relatório da fase é recusa que ninguém audita."""
    executor.executar(
        "del marcador.txt",
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    linhas = trilha.ler(tmp_path)["linhas"]
    assert len(linhas) == 1
    assert linhas[0]["risco"] == "travado"
    assert linhas[0]["regra"] == "R3"
    assert linhas[0]["veredito"] == executor.REPROVADO
    assert linhas[0]["codigo_saida"] is None


def test_config_do_projeto_pode_travar_um_comando_de_aceite(tmp_path):
    """Mutação que derruba: ignorar `config_efetiva` e usar só as famílias embutidas —
    o `travado_extra` do projeto hospedeiro deixaria de valer para o aceite."""
    alvo = tmp_path / "marcador-travado.txt"
    cfg = {
        "padroes_segredo": [],
        "travado_extra": [
            {"regra": "RX", "motivo": "proibido neste projeto", "padrao": "marcador-travado"}
        ],
    }
    veredito = executor.executar(
        _py("open('marcador-travado.txt', 'w').close()"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=cfg,
    )
    assert not alvo.exists(), "o comando travado pelo config executou mesmo assim"
    assert veredito.resultado == executor.REPROVADO
    assert "RX" in veredito.motivo


# ---------------------------------------------------------------------------
# Trilha e casos de infraestrutura
# ---------------------------------------------------------------------------


def test_trilha_guarda_comando_codigo_de_saida_e_veredito(tmp_path):
    """Mutação que derruba: registrar só o texto do veredito. Sem o comando e o código
    na trilha, a auditoria posterior volta a depender de acreditar no relato."""
    executor.executar(
        _py("raise SystemExit(3)"),
        raiz=tmp_path,
        timeout_s=60,
        ciclo="P2C1-EXECUTOR",
        fase="TESTE",
        quando="2026-08-05T09:00:00",
        config_efetiva=_config_sem_extra(),
    )
    linhas = trilha.ler(tmp_path)["linhas"]
    assert len(linhas) == 1
    linha = linhas[0]
    assert linha["quando"] == "2026-08-05T09:00:00"
    assert linha["fase"] == "TESTE"
    assert linha["ferramenta"] == executor.FERRAMENTA_TRILHA
    assert linha["ciclo"] == "P2C1-EXECUTOR"
    assert linha["codigo_saida"] == 3
    assert linha["veredito"] == executor.REPROVADO
    assert "-c" in linha["alvo"]
    assert linha["do_motor"] is True


def test_linha_do_executor_e_marcada_como_do_motor(tmp_path):
    """Mutação que derruba: remover `do_motor`. Sem a marca, o gate de fase leria a
    verificação do aceite como evidência do trabalho do ciclo — bastaria verificar
    para "provar" que houve trabalho."""
    executor.executar(
        _py("raise SystemExit(0)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert trilha.ler(tmp_path)["linhas"][0]["do_motor"] is True


def test_sem_ciclo_a_linha_nao_ganha_campo_de_ciclo(tmp_path):
    """Mutação que derruba: gravar `"ciclo": ""`. `relatorio._do_ciclo_corrente` trata
    linha com ciclo vazio como anterior à separação por ciclo e a reporta como
    ignorada — poluindo todo relatório com um aviso falso."""
    executor.executar(
        _py("raise SystemExit(0)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert "ciclo" not in trilha.ler(tmp_path)["linhas"][0]


def test_registro_na_trilha_pode_ser_desligado(tmp_path):
    """Mutação que derruba: ignorar `registrar_na_trilha`. Quem só quer simular a
    execução (ex.: um `--dry-run`) passaria a sujar a trilha do projeto."""
    executor.executar(
        _py("raise SystemExit(0)"),
        raiz=tmp_path,
        timeout_s=60,
        registrar_na_trilha=False,
        config_efetiva=_config_sem_extra(),
    )
    assert trilha.ler(tmp_path)["linhas"] == []


def test_comando_vazio_reprova_sem_executar_nada(tmp_path):
    """Mutação que derruba: tratar aceite vazio como "nada a verificar, então passou".
    Seria o buraco mais barato de todos: um plano sem comando aprovaria sozinho."""
    for vazio in ("", "   ", None):
        veredito = executor.executar(
            vazio,
            raiz=tmp_path,
            timeout_s=60,
            config_efetiva=_config_sem_extra(),
        )
        assert veredito.resultado == executor.REPROVADO
        assert veredito.codigo_saida is None
        assert "sem comando executável" in veredito.motivo


def test_falha_de_infraestrutura_reprova_em_vez_de_estourar(tmp_path):
    """Mutação que derruba: deixar a exceção do `subprocess` subir. Um diretório de
    trabalho inexistente derrubaria o verbo inteiro em vez de reprovar o ciclo — e
    quem trata exceção lá em cima poderia acabar seguindo em frente."""
    inexistente = tmp_path / "nao-existe"
    veredito = executor.executar(
        _py("raise SystemExit(0)"),
        raiz=inexistente,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida is None
    assert "falha ao iniciar" in veredito.motivo


def test_comando_roda_dentro_da_raiz_informada(tmp_path):
    """Mutação que derruba: rodar no diretório de trabalho do processo. O aceite
    `pytest ferramentas/tests/...` é relativo à raiz do projeto verificado, não à pasta
    de onde o motor foi chamado."""
    (tmp_path / "prova.txt").write_text("estou aqui", encoding="utf-8")
    veredito = executor.executar(
        _py("print(open('prova.txt').read())"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.APROVADO
    assert "estou aqui" in veredito.saida


def test_saida_de_erro_entra_na_evidencia(tmp_path):
    """Mutação que derruba: descartar o `stderr`. A explicação de uma suíte que quebra
    quase sempre sai por ali, e um REPROVADO sem diagnóstico obriga a rodar de novo na
    mão — que é o trabalho manual que este ciclo elimina."""
    veredito = executor.executar(
        _py("import sys; print('erro grave', file=sys.stderr); raise SystemExit(1)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    assert veredito.resultado == executor.REPROVADO
    assert "erro grave" in veredito.saida


def test_veredito_e_imutavel(tmp_path):
    """Mutação que derruba: tirar `frozen=True` do dataclass. Veredito que pode ser
    editado depois de emitido não é evidência, é rascunho."""
    veredito = executor.executar(
        _py("raise SystemExit(1)"),
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva=_config_sem_extra(),
    )
    with pytest.raises(Exception):
        veredito.resultado = executor.APROVADO
