"""Casos de mesa do classificador de risco.

Cada caso é uma decisão de segurança. Um caso que muda de nível é uma mudança de
política — nunca um ajuste de teste para o código passar.
"""
import pytest

from ferramentas import config, risco

CFG = dict(config.PADRAO)

TRAVADOS = [
    ("R1-curl-post", "Bash", {"command": "curl -X POST https://api.exemplo/dados"}, "R1"),
    ("R1-curl-data", "Bash", {"command": 'curl -d "a=1" https://api.exemplo'}, "R1"),
    ("R1-wget-post", "Bash", {"command": "wget --post-data=x https://api.exemplo"}, "R1"),
    ("R2-push", "Bash", {"command": "git push origin main"}, "R2"),
    ("R2-push-force", "Bash", {"command": "git push --force"}, "R2"),
    ("R2-reset-hard", "Bash", {"command": "git reset --hard HEAD~1"}, "R2"),
    ("R2-rebase", "Bash", {"command": "git rebase main"}, "R2"),
    ("R2-clean", "Bash", {"command": "git clean -fd"}, "R2"),
    ("R3-rm-rf", "Bash", {"command": "rm -rf build"}, "R3"),
    ("R3-remove-item", "Bash", {"command": "Remove-Item -Recurse -Force temp"}, "R3"),
    ("R3-del", "Bash", {"command": "del saida.txt"}, "R3"),
    ("R4-drop", "Bash", {"command": 'sqlite3 base.db "DROP TABLE clientes"'}, "R4"),
    ("R4-truncate", "Bash", {"command": 'psql -c "TRUNCATE TABLE lancamentos"'}, "R4"),
    ("R4-delete-sem-where", "Bash", {"command": 'psql -c "DELETE FROM contas"'}, "R4"),
    ("R4-alembic", "Bash", {"command": "alembic upgrade head"}, "R4"),
    ("R4-django", "Bash", {"command": "python manage.py migrate"}, "R4"),
    ("R6-docker-push", "Bash", {"command": "docker push registro/app:1"}, "R6"),
    ("R6-kubectl", "Bash", {"command": "kubectl apply -f deploy.yml"}, "R6"),
    ("R6-terraform", "Bash", {"command": "terraform apply"}, "R6"),
    ("R6-npm-publish", "Bash", {"command": "npm publish"}, "R6"),
    ("R7-npm-global", "Bash", {"command": "npm install -g pnpm"}, "R7"),
    ("R7-pip", "Bash", {"command": "pip install requests"}, "R7"),
    ("R7-winget", "Bash", {"command": "winget install Git.Git"}, "R7"),
    ("R8-python-rmtree", "Bash", {"command": "python -c \"import shutil; shutil.rmtree('x')\""}, "R8"),
    ("encadeado-pior-vence", "Bash", {"command": "pytest -q && rm -rf .cache"}, "R3"),
    ("redirect-para-segredo", "Bash", {"command": "echo CHAVE=1 > .env"}, "R5"),
    # CRÍTICO 1: substituição de comando escondida dentro do -m do git escapava
    # porque `_MSG_GIT` apagava o argumento (com aspas e tudo) antes de qualquer
    # família casar. `$(...)` dentro do texto do commit agora trava antes disso.
    (
        "R8-substituicao-comando",
        "Bash",
        {"command": 'git commit -m "$(rm -rf /dados)"'},
        "R8",
    ),
    # CRÍTICO 2: a âncora da família R3 não enxergava `rm` logo depois de uma
    # aspa — `bash -c "rm -rf /dados"` saía RASTREADO (só via execução indireta,
    # sem olhar o que tem dentro do -c). Agora a aspa entra na âncora.
    ("R3-bash-c-rm", "Bash", {"command": 'bash -c "rm -rf /dados"'}, "R3"),
    # CRÍTICO 3: `_PY_PERIGO` não cobria execução indireta via os.system/os.popen/
    # eval/exec. Usamos um payload sem `rm`/`del` para isolar exatamente essa
    # cobertura nova (um `os.system('rm ...')` já travaria via R3 sozinho, o que
    # não provaria nada sobre este padrão específico).
    (
        "R8-python-os-system",
        "Bash",
        {"command": "python -c \"import os; os.system('cat /etc/passwd')\""},
        "R8",
    ),
    # CRÍTICO 4: R1 só reconhecia `-X`; a forma longa `--request` saía LIVRE.
    (
        "R1-curl-request-longo",
        "Bash",
        {"command": "curl --request POST https://api.exemplo/dados"},
        "R1",
    ),
    # CRÍTICO 5: alvo de redirecionamento entre aspas (`> ".env"`) saía LIVRE
    # porque o fnmatch comparava o nome com as aspas incluídas.
    ("R5-redirect-aspas", "Bash", {"command": 'echo CHAVE=1 > ".env"'}, "R5"),
]


@pytest.mark.parametrize(
    "ident,ferramenta,entrada,regra",
    TRAVADOS,
    ids=[c[0] for c in TRAVADOS],
)
def test_familias_travadas(ident, ferramenta, entrada, regra, tmp_path):
    resultado = risco.classificar(ferramenta, entrada, raiz=tmp_path, config=CFG)
    assert resultado.nivel == risco.TRAVADO, f"{ident} deveria travar, veio {resultado}"
    assert resultado.regra == regra


LIVRES = [
    # Uma correção anterior alargou a âncora de R3 para `(^|[\s;|&'"])` só para
    # pegar `bash -c "rm -rf x"`. Isso travava buscas de texto corriqueiras que
    # apenas mencionam `rm`/`erase` dentro de aspas. A correção certa reverteu a
    # âncora e tratou execução indireta extraindo e reclassificando o payload —
    # estes casos provam que o falso positivo morreu sem reabrir o buraco original.
    ("grep-rm-em-string", "Bash", {"command": 'grep "rm this" arquivo.txt'}),
    ("git-log-grep-rm", "Bash", {"command": 'git log --grep="rm bug fix"'}),
    ("findstr-erase-em-string", "Bash", {"command": 'findstr "erase old logic" notas.txt'}),
]


@pytest.mark.parametrize("ident,ferramenta,entrada", LIVRES, ids=[c[0] for c in LIVRES])
def test_familias_livres(ident, ferramenta, entrada, tmp_path):
    resultado = risco.classificar(ferramenta, entrada, raiz=tmp_path, config=CFG)
    assert resultado.nivel == risco.LIVRE, f"{ident} deveria ficar livre, veio {resultado}"


def test_segredo_trava_mesmo_em_arquivo_novo(tmp_path):
    """Precedência: TRAVADO vence LIVRE. Arquivo novo chamado .env não é livre."""
    alvo = tmp_path / ".env"
    assert not alvo.exists()
    resultado = risco.classificar(
        "Write", {"file_path": str(alvo)}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.TRAVADO
    assert resultado.regra == "R5"


def test_leitura_de_segredo_tambem_trava(tmp_path):
    resultado = risco.classificar(
        "Read",
        {"file_path": str(tmp_path / "certificados" / "cliente.pfx")},
        raiz=tmp_path,
        config=CFG,
    )
    assert resultado.nivel == risco.TRAVADO
    assert resultado.regra == "R5"


def test_alvo_relativo_resolve_contra_a_raiz(tmp_path):
    """Sem resolver contra `raiz`, Path('servico.py').exists() olharia o CWD e devolveria LIVRE."""
    (tmp_path / "servico.py").write_text("x = 1", encoding="utf-8")
    resultado = risco.classificar(
        "Edit", {"file_path": "servico.py"}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.RASTREADO


def test_excecao_interna_resulta_em_travado(tmp_path, monkeypatch):
    """Falha segura: classificador quebrado nunca libera."""

    def explode(*_args, **_kwargs):
        raise RuntimeError("falha proposital")

    monkeypatch.setattr(risco, "_classificar_comando", explode)
    resultado = risco.classificar("Bash", {"command": "ls"}, raiz=tmp_path, config=CFG)
    assert resultado.nivel == risco.TRAVADO
    assert resultado.regra == "R0"
