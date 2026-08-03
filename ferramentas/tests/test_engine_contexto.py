#!/usr/bin/env python3
"""Testes de integração do hook VIVO `hooks/engine_contexto.py`.

Cobrem o cartão estendido de ponta a ponta: motores por fase, sugestão
automática via diff, volumes PRONTO detectados dinamicamente e o teto de
linhas. Este arquivo nasceu dos antigos testes das cópias `engine_contexto_v3`
e `engine_contexto_v4` (removidas), reapontados para o módulo que o
`hooks.json` executa de verdade.
"""
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "hooks"))

# O hook vivo — o mesmo caminho de import de test_hooks.py, para que o módulo
# exista uma única vez na sessão do pytest.
import engine_contexto as hook  # noqa: E402


def criar_estrutura_teste(tmp_path: Path, volumes=("07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING", "99-NOVO-VOLUME")) -> Path:
    """Cria estrutura mínima de projeto: motores/ e volumes/prontos/."""
    for motor_nome in [
        "revisar-codigo",
        "materializar-ideia",
        "otimizar-performance",
        "arquitetar-sistema",
    ]:
        motor_dir = tmp_path / "motores" / motor_nome
        motor_dir.mkdir(parents=True)
        (motor_dir / "SKILL.md").write_text(
            f'---\nname: {motor_nome}\ndescription: "Teste {motor_nome}"\n---\n',
            encoding="utf-8",
        )

    for vol_nome in volumes:
        vol_dir = tmp_path / "volumes" / "prontos" / vol_nome
        vol_dir.mkdir(parents=True)
        (vol_dir / "README.md").write_text(
            f"# {vol_nome}\n\nDescrição dinamicamente descoberta",
            encoding="utf-8",
        )

    return tmp_path


# --- Contrato de superfície do módulo vivo ---------------------------------------


def test_hook_expoe_a_superficie_esperada():
    """O módulo vivo expõe as funções que o cartão estendido usa."""
    assert hasattr(hook, "montar_cartao_estendido")
    assert hasattr(hook, "_analisar_e_sugerir_motor")
    assert hasattr(hook, "_detectar_volumes_dinamicos")


# --- Cartão estendido: fases e teto ----------------------------------------------


def test_monta_cartao_na_fase_plano(tmp_path):
    """Cartão da fase PLANO traz cabeçalho, invariantes e os motores da fase."""
    raiz = criar_estrutura_teste(tmp_path)

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

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert cartao is not None
    assert "== ENGINE ativo ==" in cartao
    assert "PLANO" in cartao
    assert "Invariantes:" in cartao
    # Motores da fase PLANO, lidos do MOTORES_POR_FASE vivo
    assert "arquitetar-sistema" in cartao
    assert "materializar-ideia" in cartao
    assert len(cartao.split("\n")) <= 50


def test_respeita_teto_em_build(tmp_path):
    """Teto de 50 linhas é respeitado mesmo com corpo cheio."""
    raiz = criar_estrutura_teste(tmp_path)

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

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert len(cartao.split("\n")) <= 50


def test_nao_sugere_motor_em_descoberta(tmp_path):
    """Em DESCOBERTA o hook nunca sugere motor (retorna antes de olhar o diff)."""
    raiz = criar_estrutura_teste(tmp_path)

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "DESCOBERTA",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert "💡 Sugestão" not in cartao


def test_funcoes_auxiliares():
    """_cortar respeita o limite; _teto_efetivo nunca fica abaixo do piso."""
    cortado = hook._cortar("a" * 200, 50)
    assert len(cortado) <= 50

    teto = hook._teto_efetivo({})
    assert teto >= hook.MINIMO_CARTAO


# --- Volumes dinâmicos ------------------------------------------------------------


def test_detecta_volumes_dinamicamente(tmp_path):
    """Detecção lista exatamente o que está em volumes/prontos/."""
    raiz = criar_estrutura_teste(tmp_path)

    volumes = hook._detectar_volumes_dinamicos(raiz)

    assert len(volumes) == 4
    nomes = [v[0] for v in volumes]
    assert "07-PROMPT-ENGINE" in nomes
    assert "99-NOVO-VOLUME" in nomes


def test_monta_cartao_com_volumes(tmp_path):
    """Cartão inclui a seção de volumes PRONTO com os nomes detectados."""
    raiz = criar_estrutura_teste(tmp_path)

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste volumes dinâmicos", "modo": "normal"},
        "fase": "BUILD",
        "cartoes": ["python"],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert "== ENGINE ativo ==" in cartao
    assert "BUILD" in cartao
    assert "Volumes PRONTO" in cartao
    assert "07-PROMPT-ENGINE" in cartao
    assert "99-NOVO-VOLUME" in cartao
    assert len(cartao.split("\n")) <= 50


def test_volume_novo_descoberto_sem_mudar_codigo(tmp_path):
    """Volume criado depois aparece no cartão — nada de lista hardcoded."""
    raiz = criar_estrutura_teste(tmp_path)

    novo_vol = raiz / "volumes" / "prontos" / "55-NOVO-DESCOBERTO"
    novo_vol.mkdir(parents=True)
    (novo_vol / "README.md").write_text(
        "# 55-NOVO-DESCOBERTO\n\nNovo volume descoberto", encoding="utf-8"
    )

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "DOC",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert "55-NOVO-DESCOBERTO" in cartao


def test_volumes_em_ordem_alfabetica(tmp_path):
    """Volumes aparecem no cartão em ordem alfabética."""
    raiz = criar_estrutura_teste(tmp_path)

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "PLANO",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    linhas = cartao.split("\n")
    vol_indices = []
    for i, linha in enumerate(linhas):
        for nome in ("07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING", "99-NOVO-VOLUME"):
            if nome in linha:
                vol_indices.append((i, nome))

    esperado = ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING", "99-NOVO-VOLUME"]
    obtido = [nome for _, nome in sorted(vol_indices)]
    assert obtido == esperado, f"Esperado {esperado}, obteve {obtido}"


def test_volume_com_status_nao_pronto_fica_fora_do_cartao(tmp_path):
    """`_VOLUME.yml` com status != PRONTO exclui o volume do cartão.

    Este é o comportamento vivo que substituiu a lista hardcoded
    `VOLUMES_PRONTOS` das cópias antigas: quem manda é o `status` do
    `_VOLUME.yml`, não o código.
    """
    raiz = criar_estrutura_teste(tmp_path, volumes=("31-TESTING",))

    rascunho = raiz / "volumes" / "prontos" / "40-RASCUNHO"
    rascunho.mkdir(parents=True)
    (rascunho / "_VOLUME.yml").write_text(
        "status: RASCUNHO\nescopo: Ainda em escrita\n", encoding="utf-8"
    )
    (rascunho / "README.md").write_text("# 40-RASCUNHO\n\nEm escrita", encoding="utf-8")

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "BUILD",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert "31-TESTING" in cartao
    assert "40-RASCUNHO" not in cartao


def test_volume_pronto_usa_escopo_do_volume_yml_como_resumo(tmp_path):
    """Com `_VOLUME.yml` `status: PRONTO`, o resumo do cartão vem do `escopo`."""
    raiz = criar_estrutura_teste(tmp_path, volumes=())

    vol = raiz / "volumes" / "prontos" / "12-MEMORY"
    vol.mkdir(parents=True)
    (vol / "_VOLUME.yml").write_text(
        "status: PRONTO\nescopo: Persistência de estado entre sessões\n",
        encoding="utf-8",
    )

    dados = {
        "ativo": True,
        "ciclo": {"objetivo": "Teste", "modo": "normal"},
        "fase": "BUILD",
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
    }
    cfg = {"teto_cartao_linhas": 50}

    cartao = hook.montar_cartao_estendido(dados, cfg, raiz, str(raiz))

    assert "12-MEMORY" in cartao
    assert "Persistência de estado entre sessões" in cartao
