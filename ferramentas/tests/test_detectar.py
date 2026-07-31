"""Testes de ferramentas/detectar.py."""
from __future__ import annotations

from pathlib import Path

from ferramentas import detectar

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]


def _escrever_cartao(diretorio: Path, nome: str, tecnologia: str, padroes: list[str]) -> Path:
    padroes_str = ", ".join(f'"{p}"' for p in padroes)
    conteudo = (
        "---\n"
        f"tecnologia: {tecnologia}\n"
        f"detectar: [{padroes_str}]\n"
        "papeis: [arquiteto]\n"
        "versao: 2026-07-30\n"
        "---\n\n"
        "## Convenções\n- nada.\n"
    )
    caminho = diretorio / nome
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


# --- ler_cartao ---------------------------------------------------------


def test_ler_cartao_devolve_as_quatro_chaves(tmp_path):
    caminho = _escrever_cartao(tmp_path, "foo.md", "foo", ["*.foo"])
    cartao = detectar.ler_cartao(caminho)
    assert cartao["tecnologia"] == "foo"
    assert cartao["detectar"] == ["*.foo"]
    assert cartao["papeis"] == ["arquiteto"]
    assert cartao["versao"] == "2026-07-30"


def test_cartao_sem_front_matter_levanta_erro(tmp_path):
    caminho = tmp_path / "sem_front_matter.md"
    caminho.write_text("## Só prosa, sem front-matter\n", encoding="utf-8")
    try:
        detectar.ler_cartao(caminho)
        assert False, "deveria ter levantado CartaoInvalido"
    except detectar.CartaoInvalido:
        pass


def test_cartao_com_campo_obrigatorio_ausente_levanta_erro(tmp_path):
    caminho = tmp_path / "incompleto.md"
    caminho.write_text(
        "---\ntecnologia: incompleto\ndetectar: [\"*.x\"]\n---\n", encoding="utf-8"
    )
    try:
        detectar.ler_cartao(caminho)
        assert False, "deveria ter levantado CartaoInvalido (faltam papeis e versao)"
    except detectar.CartaoInvalido:
        pass


def test_todos_os_cartoes_reais_sao_lidos_sem_erro():
    diretorio = RAIZ_PLUGIN / "cartoes"
    cartoes = [c for c in diretorio.glob("*.md") if not c.name.startswith("_")]
    tecnologias = set()
    for caminho in cartoes:
        cartao = detectar.ler_cartao(caminho)
        for chave in ("tecnologia", "detectar", "papeis", "versao"):
            assert chave in cartao, f"{caminho.name}: falta {chave!r}"
        tecnologias.add(cartao["tecnologia"])
    for esperada in ("python", "pytest", "ui-ux"):
        assert esperada in tecnologias, f"cartão {esperada!r} não encontrado/lido"


def test_os_doze_cartoes_do_elenco_completo_sao_validos():
    """Elenco completo da Fase 2: os 3 cartões da Fase 1 + os 9 novos, todos com
    `detectar` e `papeis` não vazios. É esse teste que impede um cartão malformado
    (ou um cartão esquecido) entrar no acervo sem ser percebido."""
    diretorio = RAIZ_PLUGIN / "cartoes"
    cartoes = [c for c in diretorio.glob("*.md") if not c.name.startswith("_")]

    esperados = {
        "python", "pytest", "ui-ux",
        "fastapi", "excel-vba", "office-scripts", "power-query", "react",
        "typescript", "postgresql", "sqlite", "mermaid",
    }
    assert len(cartoes) == 12, (
        f"esperava 12 cartões em cartoes/, achou {len(cartoes)}: "
        f"{sorted(c.name for c in cartoes)}"
    )

    tecnologias = set()
    for caminho in cartoes:
        cartao = detectar.ler_cartao(caminho)
        assert cartao["tecnologia"], f"{caminho.name}: 'tecnologia' vazia"
        assert cartao["detectar"], f"{caminho.name}: 'detectar' vazio"
        assert cartao["papeis"], f"{caminho.name}: 'papeis' vazio"
        tecnologias.add(cartao["tecnologia"])

    assert tecnologias == esperados, (
        f"tecnologias lidas != esperadas. faltando={esperados - tecnologias} "
        f"sobrando={tecnologias - esperados}"
    )


# --- cartoes_do_projeto --------------------------------------------------


def test_projeto_com_pyproject_detecta_python_e_pytest(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    resultado = detectar.cartoes_do_projeto(tmp_path, RAIZ_PLUGIN)
    assert "python" in resultado
    assert "pytest" in resultado


def test_projeto_vazio_devolve_lista_vazia(tmp_path):
    resultado = detectar.cartoes_do_projeto(tmp_path, RAIZ_PLUGIN)
    assert resultado == []


def test_resultado_e_ordenado_e_sem_duplicata(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    resultado = detectar.cartoes_do_projeto(tmp_path, RAIZ_PLUGIN)
    assert resultado == sorted(set(resultado))


def test_glob_com_subdiretorio_casa(tmp_path):
    testes = tmp_path / "tests" / "unit"
    testes.mkdir(parents=True)
    (testes / "test_algo.py").write_text("def test_algo(): pass\n", encoding="utf-8")
    resultado = detectar.cartoes_do_projeto(tmp_path, RAIZ_PLUGIN)
    assert "pytest" in resultado, "tests/**/test_*.py deveria casar arquivo em subdiretório"


def test_arquivo_em_diretorio_ignorado_nao_dispara_deteccao(tmp_path):
    plugin = tmp_path / "plugin"
    (plugin / "cartoes").mkdir(parents=True)
    _escrever_cartao(plugin / "cartoes", "python_sintetico.md", "python-sintetico", ["**/*.py"])

    projeto = tmp_path / "projeto"
    node_modules = projeto / "node_modules" / "pacote"
    node_modules.mkdir(parents=True)
    (node_modules / "arquivo.py").write_text("x = 1\n", encoding="utf-8")

    resultado = detectar.cartoes_do_projeto(projeto, plugin)
    assert resultado == []


def test_cartao_com_underscore_e_ignorado(tmp_path):
    plugin = tmp_path / "plugin"
    (plugin / "cartoes").mkdir(parents=True)
    _escrever_cartao(plugin / "cartoes", "_rascunho.md", "rascunho", ["*.txt"])

    projeto = tmp_path / "projeto"
    projeto.mkdir()
    (projeto / "arquivo.txt").write_text("x\n", encoding="utf-8")

    resultado = detectar.cartoes_do_projeto(projeto, plugin)
    assert resultado == []


def test_padrao_invalido_e_ignorado_com_seguranca(tmp_path):
    plugin = tmp_path / "plugin"
    (plugin / "cartoes").mkdir(parents=True)
    caminho = plugin / "cartoes" / "quebrado.md"
    caminho.write_text(
        "---\n"
        "tecnologia: quebrado\n"
        'detectar: ["[abertura-sem-fechamento"]\n'
        "papeis: [arquiteto]\n"
        "versao: 2026-07-30\n"
        "---\n",
        encoding="utf-8",
    )

    projeto = tmp_path / "projeto"
    projeto.mkdir()
    (projeto / "arquivo.txt").write_text("x\n", encoding="utf-8")

    resultado = detectar.cartoes_do_projeto(projeto, plugin)
    assert resultado == []
