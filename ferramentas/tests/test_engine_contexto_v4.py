#!/usr/bin/env python3
"""Testes de integração para engine_contexto_v4.py com volumes dinâmicos."""
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

import engine_contexto_v4 as hook_v4


def criar_estrutura_teste():
    """Cria estrutura ENGINE com volumes dinâmicos."""
    tmpdir = Path(tempfile.mkdtemp())

    # ENGINE
    engine_dir = tmpdir / ".engine"
    engine_dir.mkdir()

    # Motores
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

    # Volumes dinâmicos
    volumes_dir = tmpdir / "volumes" / "prontos"
    volumes_dir.mkdir(parents=True)
    for vol_nome in ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING", "99-NOVO-VOLUME"]:
        vol_dir = volumes_dir / vol_nome
        vol_dir.mkdir()
        readme = vol_dir / "README.md"
        readme.write_text(f"# {vol_nome}\n\nDescrição dinamicamente descoberta")

    # Estado
    estado = {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "test-v4",
            "objetivo": "Testar volumes dinâmicos",
            "modo": "normal",
        },
        "fase": "BUILD",
        "cartoes": ["python"],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    (engine_dir / "estado.json").write_text(json.dumps(estado))

    # Config
    config = {"porta_plano": True, "teto_cartao_linhas": 50}
    (engine_dir / "config.json").write_text(json.dumps(config))

    return tmpdir


def test_v4_carrega_sem_erro():
    """Valida que V4 carrega sem erro."""
    assert hook_v4 is not None
    assert hasattr(hook_v4, "_detectar_volumes_dinamicos")
    print("✅ test_v4_carrega_sem_erro PASSOU")


def test_v4_detecta_volumes():
    """Valida que V4 detecta volumes dinamicamente."""
    tmpdir = criar_estrutura_teste()
    raiz = tmpdir

    volumes = hook_v4._detectar_volumes_dinamicos(raiz)

    assert len(volumes) == 4
    nomes = [v[0] for v in volumes]
    assert "07-PROMPT-ENGINE" in nomes
    assert "99-NOVO-VOLUME" in nomes
    print("✅ test_v4_detecta_volumes PASSOU")


def test_v4_monta_cartao_com_volumes():
    """Valida que cartão inclui volumes dinâmicos."""
    tmpdir = criar_estrutura_teste()

    raiz = tmpdir
    cwd = str(tmpdir)

    dados = {
        "ativo": True,
        "ciclo": {
            "objetivo": "Teste volumes dinâmicos",
            "modo": "normal",
        },
        "fase": "BUILD",
        "cartoes": ["python"],
        "decisoes": [],
        "diffs_pendentes": [],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v4.montar_cartao_estendido(dados, cfg, raiz, cwd)

    assert cartao is not None
    assert "== ENGINE ativo ==" in cartao
    assert "BUILD" in cartao
    assert "Volumes PRONTO" in cartao
    assert "07-PROMPT-ENGINE" in cartao
    assert "99-NOVO-VOLUME" in cartao
    assert len(cartao.split("\n")) <= 50
    print("✅ test_v4_monta_cartao_com_volumes PASSOU")


def test_v4_respeita_teto():
    """Valida que teto é respeitado com volumes."""
    tmpdir = criar_estrutura_teste()

    raiz = tmpdir
    cwd = str(tmpdir)

    dados = {
        "ativo": True,
        "ciclo": {
            "objetivo": "Objetivo muito longo para testar",
            "modo": "normal",
        },
        "fase": "REVISAO",
        "cartoes": ["python", "pytest", "docker", "kubernetes"],
        "decisoes": [
            {"o_que": "Pattern A"},
            {"o_que": "Pattern B"},
        ],
        "diffs_pendentes": ["file1.py", "file2.py"],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v4.montar_cartao_estendido(dados, cfg, raiz, cwd)

    linhas = cartao.split("\n")
    assert len(linhas) <= 50, f"Cartão tem {len(linhas)} linhas"
    print("✅ test_v4_respeita_teto PASSOU")


def test_v4_volumes_novo_nao_hardcoded():
    """Valida que novo volume é descoberto automaticamente."""
    tmpdir = criar_estrutura_teste()

    raiz = tmpdir
    cwd = str(tmpdir)

    # Criar novo volume após a estrutura
    novo_vol = raiz / "volumes" / "prontos" / "55-NOVO-DESCOBERTO"
    novo_vol.mkdir(parents=True)
    (novo_vol / "README.md").write_text("# 55-NOVO-DESCOBERTO\n\nNovo volume descoberto")

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "DOC",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v4.montar_cartao_estendido(dados, cfg, raiz, cwd)

    # Novo volume deve aparecer (não hardcoded)
    assert "55-NOVO-DESCOBERTO" in cartao
    print("✅ test_v4_volumes_novo_nao_hardcoded PASSOU")


def test_v4_ordem_alfabetica():
    """Valida que volumes aparecem em ordem alfabética."""
    tmpdir = criar_estrutura_teste()

    raiz = tmpdir
    cwd = str(tmpdir)

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "PLANO",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }

    cfg = {"teto_cartao_linhas": 50}

    cartao = hook_v4.montar_cartao_estendido(dados, cfg, raiz, cwd)

    # Extrair nomes de volumes do cartão
    linhas = cartao.split("\n")
    vol_indices = []
    for i, linha in enumerate(linhas):
        if "07-PROMPT-ENGINE" in linha:
            vol_indices.append((i, "07-PROMPT-ENGINE"))
        elif "12-MEMORY" in linha:
            vol_indices.append((i, "12-MEMORY"))
        elif "31-TESTING" in linha:
            vol_indices.append((i, "31-TESTING"))
        elif "99-NOVO-VOLUME" in linha:
            vol_indices.append((i, "99-NOVO-VOLUME"))

    # Verificar ordem
    expected_order = ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING", "99-NOVO-VOLUME"]
    actual_order = [nome for _, nome in sorted(vol_indices)]
    assert actual_order == expected_order, f"Esperado {expected_order}, obteve {actual_order}"
    print("✅ test_v4_ordem_alfabetica PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTES DE INTEGRAÇÃO: Engine Contexto V4 - Volumes Dinâmicos")
    print("=" * 80)

    test_v4_carrega_sem_erro()
    test_v4_detecta_volumes()
    test_v4_monta_cartao_com_volumes()
    test_v4_respeita_teto()
    test_v4_volumes_novo_nao_hardcoded()
    test_v4_ordem_alfabetica()

    print("\n" + "=" * 80)
    print("✅ TODOS OS TESTES PASSARAM")
    print("=" * 80)
