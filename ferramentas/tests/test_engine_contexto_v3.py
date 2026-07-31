#!/usr/bin/env python3
"""Testes de integração para engine_contexto_v3.py."""
import sys
import json
import tempfile
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "hooks"))

# Importar o hook v3
import engine_contexto_v3 as hook_v3


def criar_estrutura_teste():
    """Cria estrutura mínima para teste."""
    tmpdir = Path(tempfile.mkdtemp())

    # Criar estrutura ENGINE
    engine_dir = tmpdir / ".engine"
    engine_dir.mkdir()

    # Criar motores
    motores_dir = tmpdir / "motores"
    for motor_nome in [
        "revisar-codigo",
        "materializar-ideia",
        "otimizar-performance",
    ]:
        motor_dir = motores_dir / motor_nome
        motor_dir.mkdir(parents=True)
        skill_file = motor_dir / "SKILL.md"
        skill_file.write_text(
            f'---\nname: {motor_nome}\ndescription: "Teste {motor_nome}"\n---\n'
        )

    # Criar volumes
    volumes_dir = tmpdir / "volumes" / "prontos"
    volumes_dir.mkdir(parents=True)
    for vol_nome in ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]:
        vol_dir = volumes_dir / vol_nome
        vol_dir.mkdir()
        readme = vol_dir / "README.md"
        readme.write_text(f"# {vol_nome}\n\nDescrição do volume")

    # Criar estado
    estado = {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "test-cycle",
            "objetivo": "Testar motor sugerido",
            "modo": "normal",
        },
        "fase": "PLANO",
        "cartoes": ["python"],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    (engine_dir / "estado.json").write_text(json.dumps(estado))

    # Criar config
    config = {"porta_plano": True, "teto_cartao_linhas": 50}
    (engine_dir / "config.json").write_text(json.dumps(config))

    return tmpdir


def test_v3_carrega_sem_erro():
    """Valida que V3 carrega sem erro."""
    assert hook_v3 is not None
    assert hasattr(hook_v3, "montar_cartao_estendido")
    assert hasattr(hook_v3, "_analisar_e_sugerir_motor")
    print("✅ test_v3_carrega_sem_erro PASSOU")


def test_v3_monta_cartao_com_sugestao():
    """Valida que sugestão aparece no cartão."""
    tmpdir = criar_estrutura_teste()

    # Simular dados
    raiz = tmpdir
    cwd = str(tmpdir)

    dados = {
        "ativo": True,
        "ciclo": {
            "id": "test-cycle",
            "objetivo": "Testar motor sugerido",
            "modo": "normal",
        },
        "fase": "PLANO",
        "cartoes": ["python"],
        "decisoes": [],
        "diffs_pendentes": [],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v3.montar_cartao_estendido(dados, cfg, raiz, cwd)

    assert cartao is not None
    assert "== ENGINE ativo ==" in cartao
    assert "PLANO" in cartao
    assert "Invariantes:" in cartao
    assert len(cartao.split("\n")) <= 50
    print("✅ test_v3_monta_cartao_com_sugestao PASSOU")


def test_v3_respeita_teto():
    """Valida que teto de 50 linhas é respeitado."""
    tmpdir = criar_estrutura_teste()

    raiz = tmpdir
    cwd = str(tmpdir)

    dados = {
        "ativo": True,
        "ciclo": {
            "id": "test-cycle",
            "objetivo": "Objetivo muito longo que poderia ocupar várias linhas",
            "modo": "normal",
        },
        "fase": "BUILD",
        "cartoes": ["python", "pytest", "docker"],
        "decisoes": [
            {"o_que": "Usar pattern A"},
            {"o_que": "Usar pattern B"},
        ],
        "diffs_pendentes": ["file1.py", "file2.py", "file3.py"],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v3.montar_cartao_estendido(dados, cfg, raiz, cwd)

    linhas = cartao.split("\n")
    assert len(linhas) <= 50, f"Cartão tem {len(linhas)} linhas, max 50"
    print("✅ test_v3_respeita_teto PASSOU")


def test_v3_nao_sugere_em_descoberta():
    """Valida que não há sugestão em DESCOBERTA."""
    tmpdir = criar_estrutura_teste()

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "DESCOBERTA",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v3.montar_cartao_estendido(dados, cfg, tmpdir, str(tmpdir))

    # Não deve conter sugestão de motor em DESCOBERTA
    assert "💡 Sugestão" not in cartao
    print("✅ test_v3_nao_sugere_em_descoberta PASSOU")


def test_v3_funcoes_auxiliares():
    """Testa funções auxiliares."""
    # Teste _cortar
    texto_longo = "a" * 200
    cortado = hook_v3._cortar(texto_longo, 50)
    assert len(cortado) <= 50

    # Teste _teto_efetivo
    teto = hook_v3._teto_efetivo({})
    assert teto >= hook_v3.MINIMO_CARTAO

    print("✅ test_v3_funcoes_auxiliares PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTES DE INTEGRAÇÃO: Engine Contexto V3")
    print("=" * 80)

    test_v3_carrega_sem_erro()
    test_v3_monta_cartao_com_sugestao()
    test_v3_respeita_teto()
    test_v3_nao_sugere_em_descoberta()
    test_v3_funcoes_auxiliares()

    print("\n" + "=" * 80)
    print("✅ TODOS OS TESTES PASSARAM")
    print("=" * 80)
