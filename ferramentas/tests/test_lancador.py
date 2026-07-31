"""Testes de `hooks/engine.sh`, o lançador multiplataforma dos hooks.

`hooks.json` usa a forma shell do Claude Code (sem `args`), então quem decide
o interpretador Python é este script — daqui em diante, um elo tão crítico
quanto os próprios hooks `.py`. Cobrimos por subprocesso, com PATH controlado
via `env`, os quatro cenários pedidos: repasse de stdin/código de saída com
Python disponível, trava com `--travar-sem-python` sem Python, saída silenciosa
sem a flag e sem Python, e um caminho de script com espaço e acentuação.

Todo o módulo é pulado se `bash` não estiver no PATH desta máquina — sem
shell não há como exercitar o lançador, e a suíte não pode quebrar por causa
disso em um ambiente sem Git Bash/WSL/sh.
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

_BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(
    _BASH is None, reason="bash não está no PATH desta máquina"
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
