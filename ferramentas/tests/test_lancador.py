"""Testes de `hooks/engine.sh`, o lançador multiplataforma dos hooks.

`hooks.json` usa a forma shell do Claude Code (sem `args`), então quem decide
o interpretador Python é este script — daqui em diante, um elo tão crítico
quanto os próprios hooks `.py`. Cobrimos por subprocesso, com PATH controlado
via `env`, os quatro cenários pedidos: repasse de stdin/código de saída com
Python disponível, trava com `--travar-sem-python` sem Python, saída silenciosa
sem a flag e sem Python, e um caminho de script com espaço e acentuação.

Todo o módulo é pulado se não houver um bash utilizável nesta máquina — sem
shell não há como exercitar o lançador, e a suíte não pode quebrar por causa
disso em um ambiente sem Git Bash/WSL/sh. "Utilizável" exclui o stub da
Microsoft Store; ver `_achar_bash`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
LANCADOR = RAIZ_PLUGIN / "hooks" / "engine.sh"

def _achar_bash() -> str | None:
    """Acha um bash que de fato executa scripts, descartando o stub da Store.

    Numa máquina Windows sem WSL instalado, `shutil.which("bash")` acha o stub
    que o sistema registra em `AppData\\Local\\Microsoft\\WindowsApps`: ele
    existe, responde a `which` e, ao ser executado, imprime "instale uma distro"
    em UTF-16 e sai 1 — sem jamais ler o script pedido. É exatamente o stub que
    `hooks/engine.sh` já descarta para o Python, pelo mesmo motivo: um bash que
    não roda bash é pior que nenhum, porque a falha não se parece com ausência
    de shell, e sim com defeito do lançador.

    A comparação ignora a caixa: caminho no Windows não distingue maiúsculas, e
    já houve regressão neste repositório por filtro sensível a caixa.
    """
    candidatos: list[str] = []
    do_path = shutil.which("bash")
    if do_path:
        candidatos.append(do_path)
    # Git Bash não entra no PATH do PowerShell por padrão, mas é o shell que o
    # próprio Claude Code usa no Windows — é ele que o lançador vai encontrar em
    # produção, então é ele que o teste deve exercitar.
    candidatos += [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]
    for caminho in candidatos:
        if "windowsapps" in caminho.lower():
            continue
        if Path(caminho).is_file():
            return caminho
    return None


_BASH = _achar_bash()

pytestmark = pytest.mark.skipif(
    _BASH is None,
    reason="nenhum bash utilizável nesta máquina (o stub WindowsApps não conta)",
)


def _rodar(argumentos: list[str], entrada: str, path_env: str) -> subprocess.CompletedProcess:
    """Executa o lançador via `bash`, com PATH controlado e stdin dado.

    `env` é uma cópia do ambiente atual com só o PATH sobrescrito — preserva
    variáveis que o Windows/Git Bash precisam para funcionar (SystemRoot,
    TEMP etc.) sem deixar o PATH real da máquina vazar para dentro do teste.
    """
    ambiente = dict(os.environ)
    ambiente["PATH"] = path_env
    return subprocess.run(
        [_BASH, str(LANCADOR), *argumentos],
        input=entrada,
        capture_output=True,
        text=True,
        env=ambiente,
    )


def _script_eco_e_sai(tmp_path: Path, nome: str, codigo: int) -> Path:
    """Cria um `.py` que ecoa o stdin recebido e sai com `codigo` conhecido."""
    caminho = tmp_path / nome
    caminho.write_text(
        textwrap.dedent(
            f"""\
            import sys
            sys.stdout.write(sys.stdin.read())
            sys.exit({codigo})
            """
        ),
        encoding="utf-8",
    )
    return caminho


def _diretorio_do_interpretador() -> str:
    """Diretório do Python que está rodando os testes — um Python "de verdade"."""
    return str(Path(sys.executable).resolve().parent)


def test_repassa_stdin_e_codigo_de_saida_com_python_disponivel(tmp_path):
    alvo = _script_eco_e_sai(tmp_path, "alvo.py", 17)
    resultado = _rodar([str(alvo)], "conteudo de teste\n", _diretorio_do_interpretador())
    assert resultado.returncode == 17
    assert resultado.stdout == "conteudo de teste\n"


def test_travar_sem_python_sai_2_e_stderr_menciona_python(tmp_path):
    alvo = _script_eco_e_sai(tmp_path, "alvo.py", 0)
    resultado = _rodar(["--travar-sem-python", str(alvo)], "", "")
    assert resultado.returncode == 2
    assert "python" in resultado.stderr.lower()


def test_sem_flag_sai_0_em_silencio_sem_python(tmp_path):
    alvo = _script_eco_e_sai(tmp_path, "alvo.py", 0)
    resultado = _rodar([str(alvo)], "", "")
    assert resultado.returncode == 0
    assert resultado.stdout == ""


def test_caminho_com_espaco_e_acento_e_repassado_corretamente(tmp_path):
    alvo = _script_eco_e_sai(tmp_path, "script com espaço e acentuação á é.py", 5)
    resultado = _rodar([str(alvo)], "olá mundo\n", _diretorio_do_interpretador())
    assert resultado.returncode == 5
    assert resultado.stdout == "olá mundo\n"


def test_descarta_stub_windowsapps_e_usa_o_python_de_verdade(tmp_path):
    """Reproduz o caso real: `python3` só existe como stub da Microsoft Store.

    Nesta própria máquina, `command -v python3` resolve para
    `...\\AppData\\Local\\Microsoft\\WindowsApps\\python3` — um stub que abre a
    loja em vez de rodar Python. Monta um PATH com um "python3" falso dentro
    de uma pasta chamada `WindowsApps` (para casar com o filtro por
    substring) e o Python de verdade numa outra pasta; o lançador tem que
    descartar o stub e cair para o candidato seguinte (`python`), nunca
    invocar o stub.
    """
    pasta_stub = tmp_path / "AppData" / "Local" / "Microsoft" / "WindowsApps"
    pasta_stub.mkdir(parents=True)
    stub = pasta_stub / "python3"
    # Se o lançador invocar isto por engano, o código de saída (66) denuncia
    # o erro claramente — bem diferente do código esperado (17) do teste.
    stub.write_text("#!/usr/bin/env bash\nexit 66\n", encoding="utf-8")
    stub.chmod(0o755)

    alvo = _script_eco_e_sai(tmp_path, "alvo.py", 17)
    path_env = os.pathsep.join([str(pasta_stub), _diretorio_do_interpretador()])
    resultado = _rodar([str(alvo)], "passou pelo stub? nao.\n", path_env)
    assert resultado.returncode == 17
    assert resultado.stdout == "passou pelo stub? nao.\n"


def test_descarta_stub_windowsapps_com_caixa_diferente(tmp_path):
    """O filtro do stub não pode depender da caixa do caminho.

    Caminho no Windows não distingue maiúsculas, e o PATH pode chegar
    normalizado por outra ferramenta. Com a comparação sensível a caixa, uma
    pasta `windowsapps` minúscula passava pelo filtro, o stub era executado e
    devolvia um código arbitrário — que, não sendo 2, LIBERA a ação no hook de
    risco. É a pior falha possível aqui: o gate acha que rodou.
    """
    pasta_stub = tmp_path / "local" / "microsoft" / "windowsapps"
    pasta_stub.mkdir(parents=True)
    stub = pasta_stub / "py"
    stub.write_text("#!/usr/bin/env bash\nexit 9009\n", encoding="utf-8")
    stub.chmod(0o755)

    alvo = _script_eco_e_sai(tmp_path, "alvo.py", 0)
    resultado = _rodar(["--travar-sem-python", str(alvo)], "", str(pasta_stub))
    assert resultado.returncode == 2, resultado
    assert "python" in resultado.stderr.lower()


# --- O modo de falha que importa -------------------------------------------
#
# No Claude Code, SÓ `exit 2` bloqueia uma ação; qualquer outro código é erro
# não-bloqueante e a ação acontece assim mesmo. Para o hook de risco isso
# inverte a intuição: um erro qualquer não é "proteção ausente", é "proteção
# que deixa passar". Por isso o lançador traduz todo código inesperado para 2
# quando roda com `--travar-sem-python`.

CODIGOS_INESPERADOS = [1, 7, 66, 127, 9009]


@pytest.mark.parametrize("codigo", CODIGOS_INESPERADOS)
def test_codigo_inesperado_do_classificador_vira_2(tmp_path, codigo):
    alvo = _script_eco_e_sai(tmp_path, "alvo.py", codigo)
    resultado = _rodar(
        ["--travar-sem-python", str(alvo)], "", _diretorio_do_interpretador()
    )
    assert resultado.returncode == 2, f"codigo {codigo} deveria virar 2: {resultado}"


@pytest.mark.parametrize("codigo", [0, 2])
def test_codigo_legitimo_do_classificador_e_preservado(tmp_path, codigo):
    """A tradução não pode engolir os dois códigos que o contrato define."""
    alvo = _script_eco_e_sai(tmp_path, "alvo.py", codigo)
    resultado = _rodar(
        ["--travar-sem-python", str(alvo)], "", _diretorio_do_interpretador()
    )
    assert resultado.returncode == codigo, resultado


def test_script_quebrado_trava_em_vez_de_liberar(tmp_path):
    """Erro de sintaxe faz o Python sair 1 — que liberaria a ação."""
    alvo = tmp_path / "quebrado.py"
    alvo.write_text("isto nao e python valido (((\n", encoding="utf-8")
    resultado = _rodar(
        ["--travar-sem-python", str(alvo)], "", _diretorio_do_interpretador()
    )
    assert resultado.returncode == 2, resultado


def test_script_inexistente_trava_no_modo_de_risco(tmp_path):
    ausente = tmp_path / "nao_existe.py"
    resultado = _rodar(
        ["--travar-sem-python", str(ausente)], "", _diretorio_do_interpretador()
    )
    assert resultado.returncode == 2, resultado
    assert "nao encontrado" in resultado.stderr.lower()


def test_script_inexistente_nao_atrapalha_os_outros_hooks(tmp_path):
    """Os outros quatro hooks nunca podem bloquear o turno do usuário."""
    ausente = tmp_path / "nao_existe.py"
    resultado = _rodar([str(ausente)], "", _diretorio_do_interpretador())
    assert resultado.returncode == 0, resultado
    assert resultado.stdout == ""


def test_sem_alvo_nenhum_nao_estoura(tmp_path):
    com_flag = _rodar(["--travar-sem-python"], "", _diretorio_do_interpretador())
    assert com_flag.returncode == 2, com_flag
    sem_flag = _rodar([], "", _diretorio_do_interpretador())
    assert sem_flag.returncode == 0, sem_flag
