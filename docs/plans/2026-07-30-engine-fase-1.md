# ENGINE — Plano de Implementação da Fase 1 (núcleo)

> **Para trabalhadores agênticos:** SUB-SKILL OBRIGATÓRIA: use
> `superpowers:subagent-driven-development` (recomendado) ou
> `superpowers:executing-plans` para executar este plano tarefa a tarefa. Os passos usam
> caixa de seleção (`- [ ]`) para acompanhamento.

**Objetivo:** entregar o núcleo do ENGINE — um modo de engenharia que sobrevive à
compactação do contexto e que trava, por conta própria, as sete famílias de ação
irreversível.

**Arquitetura:** três módulos Python de biblioteca padrão (`config`, `risco`, `estado`)
guardam a lógica; dois hooks do Claude Code os acionam (`UserPromptSubmit` injeta o estado a
cada turno, `PreToolUse` classifica cada ação antes de ela acontecer); uma skill `/engine`
liga, desliga e reporta. O estado vive em `.engine/estado.json` no projeto hospedeiro — é
disco, não contexto, e é por isso que o modo persiste.

**Stack:** Python 3.11+, apenas biblioteca padrão. `pytest` para os testes. Markdown para
skill, agentes e cartões. Sem dependência externa.

**Especificação de origem:** `docs/specs/2026-07-30-engine-design.md`

## Restrições globais

Valem para **todas** as tarefas, implicitamente.

- **Apenas biblioteca padrão do Python.** Nenhuma dependência de runtime. `pytest` é
  ferramenta de desenvolvimento, não dependência do produto.
- **Falha segura = TRAVADO.** Qualquer exceção no caminho de classificação de risco resulta
  em bloqueio da ação, nunca em liberação.
- **Precedência de risco:** uma ação recebe o nível **mais restritivo** que casar. Nenhum
  critério de nível baixo rebaixa um casamento de nível alto.
- **Nada fora de `C:\Users\Usuário\Desktop\ENGINE\`** é criado, editado ou apagado por este
  plano.
- **Prosa em português do Brasil.** Identificadores em português no domínio do motor
  (`Classificacao`, `nivel`, `fase`), em inglês onde a plataforma impõe (`hookEventName`).
- **Datas em ISO:** `YYYY-MM-DD` e `YYYY-MM-DDTHH:MM:SS`.
- **Teto do cartão de estado: 40 linhas.** Verificado por teste, não por disciplina.
- **Nunca ajustar o teste para o código passar.** O teste é o contrato.

## Estrutura de arquivos da Fase 1

| Arquivo | Responsabilidade |
|---|---|
| `ferramentas/config.py` | defaults + fusão com `engine.config.json` do plugin e `.engine/config.json` do projeto |
| `ferramentas/risco.py` | classificar uma ação em `livre` / `rastreado` / `travado` |
| `ferramentas/estado.py` | ler, gravar e transicionar `.engine/estado.json` |
| `ferramentas/cli.py` | interface de linha de comando usada pela skill (`ligar`, `desligar`, `status`, `fase`) |
| `hooks/engine_risco.py` | hook `PreToolUse`: chama `risco.classificar` e bloqueia quando travado |
| `hooks/engine_contexto.py` | hook `UserPromptSubmit`: monta e injeta o cartão de estado |
| `hooks/hooks.json` | registro dos dois hooks no plugin |
| `.claude-plugin/plugin.json` | manifesto do plugin |
| `skills/engine/SKILL.md` | a skill `/engine` |
| `agents/{arquiteto,implementador,revisor,documentador}.md` | os 4 papéis da Fase 1 |
| `cartoes/{python,pytest,ui-ux}.md` | os 3 cartões da Fase 1 |
| `engine.config.json` | configuração default do plugin |
| `ferramentas/tests/` | `test_config.py`, `test_risco.py`, `test_estado.py`, `test_hooks.py`, `test_cli.py` |

**Desvio consciente da especificação:** a seção 12 do spec não lista `ferramentas/cli.py`.
Ele é necessário porque a skill precisa de um ponto de entrada estável para ligar, desligar
e reportar. A Tarefa 7 inclui o passo de atualizar a tabela da seção 12 do spec — o spec é
o contrato, então é ele que cede, por escrito, e não o código que diverge em silêncio.

**Fora da Fase 1** (não implementar, mesmo que pareça faltar): `detectar.py`, `trilha.py`,
`relatorio.py`, os hooks `engine_trilha`, `engine_salvar` e `engine_gate`, os papéis
`descobridor`, `cartografo`, `designer`, `testador`, `sentinela`, os 9 cartões restantes,
`/engine retomar` e `--dry`. Na Fase 1 os cartões são lidos diretamente pelos papéis; a
detecção automática de stack é Fase 2.

---

### Tarefa 1: Esqueleto do repositório e configuração

**Arquivos:**
- Criar: `ferramentas/__init__.py`
- Criar: `ferramentas/config.py`
- Criar: `ferramentas/tests/__init__.py`
- Criar: `ferramentas/tests/test_config.py`
- Criar: `engine.config.json`
- Criar: `.gitignore`

**Interfaces:**
- Consome: nada.
- Produz: `config.PADRAO` (dict), `config.raiz_plugin() -> Path`,
  `config.carregar(raiz_projeto: Path) -> dict`. O dict retornado sempre contém as chaves de
  `PADRAO` e a chave `_avisos: list[str]`.

- [ ] **Passo 1: Escrever o teste que falha**

Criar `ferramentas/tests/test_config.py`:

```python
"""Testes de ferramentas/config.py."""
import json

from ferramentas import config


def test_padrao_tem_as_chaves_do_contrato():
    for chave in ("porta_plano", "teto_cartao_linhas", "padroes_segredo", "travado_extra"):
        assert chave in config.PADRAO


def test_carregar_sem_arquivo_devolve_os_defaults(tmp_path):
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is True
    assert cfg["teto_cartao_linhas"] == 40
    assert cfg["_avisos"] == []


def test_config_do_projeto_sobrepoe_o_default(tmp_path):
    destino = tmp_path / ".engine"
    destino.mkdir()
    (destino / "config.json").write_text(
        json.dumps({"porta_plano": False}), encoding="utf-8"
    )
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is False
    assert cfg["teto_cartao_linhas"] == 40


def test_config_quebrada_cai_no_default_e_avisa(tmp_path):
    destino = tmp_path / ".engine"
    destino.mkdir()
    (destino / "config.json").write_text("{ isso nao e json", encoding="utf-8")
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is True
    assert len(cfg["_avisos"]) == 1
    assert "config.json" in cfg["_avisos"][0]
```

- [ ] **Passo 2: Rodar o teste e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_config.py -v
```

Esperado: `ModuleNotFoundError: No module named 'ferramentas'`.

- [ ] **Passo 3: Escrever a implementação mínima**

Criar `ferramentas/__init__.py` e `ferramentas/tests/__init__.py` vazios.

Criar `ferramentas/config.py`:

```python
"""Configuração do ENGINE.

Ordem de precedência, da mais fraca para a mais forte:
PADRAO -> <plugin>/engine.config.json -> <projeto>/.engine/config.json

Arquivo malformado nunca derruba a sessão nem passa despercebido: cai no default
e registra um aviso em `_avisos`, que o hook de contexto mostra uma vez.
"""
from __future__ import annotations

import json
from pathlib import Path

PADRAO: dict = {
    "porta_plano": True,
    "teto_cartao_linhas": 40,
    "padroes_segredo": [
        ".env",
        ".env.*",
        "*.pfx",
        "*.pem",
        "*.key",
        "*.p12",
        "credentials*",
        "*_secret*",
        "*secrets*",
    ],
    "travado_extra": [],
}


def raiz_plugin() -> Path:
    """Raiz do repositório do plugin (pai de `ferramentas/`)."""
    return Path(__file__).resolve().parent.parent


def carregar(raiz_projeto: Path) -> dict:
    """Devolve a configuração efetiva para um projeto hospedeiro."""
    cfg = dict(PADRAO)
    cfg["_avisos"] = []
    candidatos = (
        raiz_plugin() / "engine.config.json",
        Path(raiz_projeto) / ".engine" / "config.json",
    )
    for caminho in candidatos:
        if not caminho.is_file():
            continue
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as erro:
            cfg["_avisos"].append(
                f"{caminho.name} ilegível ({erro.__class__.__name__}); usando o default"
            )
            continue
        if isinstance(dados, dict):
            cfg.update(dados)
        else:
            cfg["_avisos"].append(f"{caminho.name} não é um objeto JSON; usando o default")
    return cfg
```

Criar `engine.config.json` na raiz:

```json
{
  "porta_plano": true,
  "teto_cartao_linhas": 40
}
```

Criar `.gitignore` na raiz:

```
__pycache__/
*.pyc
.pytest_cache/
.engine/
```

- [ ] **Passo 4: Rodar os testes e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_config.py -v
```

Esperado: `4 passed`. Cole a saída no relato da tarefa.

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add ferramentas engine.config.json .gitignore && git commit -m "feat(config): configuracao com defaults e fusao de arquivos"
```

---

### Tarefa 2: Classificador de risco — as famílias travadas

Esta é a tarefa mais importante do plano. É o único código entre o motor e um estrago
irreversível. Ela vem antes de qualquer agente, de qualquer skill e de qualquer hook.

**Arquivos:**
- Criar: `ferramentas/risco.py`
- Criar: `ferramentas/tests/test_risco.py`

**Interfaces:**
- Consome: `ferramentas.config.PADRAO`.
- Produz:
  - constantes `risco.LIVRE = "livre"`, `risco.RASTREADO = "rastreado"`, `risco.TRAVADO = "travado"`
  - `@dataclass(frozen=True) risco.Classificacao(nivel: str, regra: str, motivo: str)`
  - `risco.classificar(ferramenta: str, entrada: dict, *, raiz: Path, config: dict) -> Classificacao`
  - a função interna `risco._classificar_comando(comando: str, config: dict) -> Classificacao`,
    cujo nome o teste de falha segura substitui por monkeypatch

- [ ] **Passo 1: Escrever o teste que falha — tabela das famílias travadas**

Criar `ferramentas/tests/test_risco.py`:

```python
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


def test_excecao_interna_resulta_em_travado(tmp_path, monkeypatch):
    """Falha segura: classificador quebrado nunca libera."""

    def explode(*_args, **_kwargs):
        raise RuntimeError("falha proposital")

    monkeypatch.setattr(risco, "_classificar_comando", explode)
    resultado = risco.classificar("Bash", {"command": "ls"}, raiz=tmp_path, config=CFG)
    assert resultado.nivel == risco.TRAVADO
    assert resultado.regra == "R0"
```

- [ ] **Passo 2: Rodar o teste e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_risco.py -v
```

Esperado: `ModuleNotFoundError: No module named 'ferramentas.risco'`.

- [ ] **Passo 3: Escrever a implementação**

Criar `ferramentas/risco.py`:

```python
"""Classificador de risco do ENGINE.

Regra de ouro: na dúvida, TRAVADO. Este módulo nunca libera por falha.

As famílias são casadas sobre o comando CRU, de propósito: SQL perigoso quase sempre
chega dentro de aspas (`psql -c "DROP TABLE x"`), então limpar literais antes de casar
cegaria justamente a família mais cara. A proteção contra falso positivo é estreita e
explícita: emissores inertes (`echo`, `printf`) e o texto de `-m` do git.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

LIVRE = "livre"
RASTREADO = "rastreado"
TRAVADO = "travado"

_ORDEM = {LIVRE: 0, RASTREADO: 1, TRAVADO: 2}


@dataclass(frozen=True)
class Classificacao:
    nivel: str
    regra: str
    motivo: str


FAMILIAS: tuple[tuple[str, str, str], ...] = (
    (
        "R1",
        "escrita de rede",
        r"\bcurl\b[^\n]*\s-X\s*(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]*\s(-d|--data|--data-raw|--data-binary)\b"
        r"|\bwget\b[^\n]*--post",
    ),
    (
        "R2",
        "git que sai da máquina ou reescreve história",
        r"\bgit\s+(push|rebase)\b"
        r"|\bgit\s+reset\s+--hard\b"
        r"|\bgit\s+clean\s+-[a-zA-Z]*f"
        r"|\bgit\s+checkout\s+--\s",
    ),
    (
        "R3",
        "deleção",
        r"(^|[\s;|&])(rm|rmdir|del|erase)\s|\bRemove-Item\b",
    ),
    (
        "R4",
        "alteração destrutiva de banco",
        r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b"
        r"|\bALTER\s+TABLE\b"
        r"|\bDELETE\s+FROM\b(?![^;\"']*\bWHERE\b)"
        r"|\b(alembic|flyway|liquibase)\b[^\n]*\b(upgrade|migrate)\b"
        r"|\bmanage\.py\s+migrate\b",
    ),
    (
        "R6",
        "deploy ou infraestrutura",
        r"\bdocker\s+push\b"
        r"|\bkubectl\s+apply\b"
        r"|\bterraform\s+apply\b"
        r"|\bgh\s+workflow\s+run\b"
        r"|\bnpm\s+publish\b"
        r"|\btwine\s+upload\b",
    ),
    (
        "R7",
        "instalação global",
        r"\bnpm\s+(i|install)\b[^\n]*\s-g\b"
        r"|\bpip[0-9.]*\s+install\b"
        r"|\bwinget\s+install\b"
        r"|\bchoco\s+install\b",
    ),
)

_INERTE = re.compile(r"^\s*(echo|printf|:|#)\b", re.I)
_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
_SEPARADORES = re.compile(r"&&|\|\||;|\|")
_REDIRECT = re.compile(r">>?\s*([^\s;|&]+)")
_EXEC_INDIRETA = re.compile(
    r"\b(bash|sh|zsh)\s+-c\s|\bpowershell(\.exe)?\s+(-Command|-c)\s|\beval\s", re.I
)
_PY_INLINE = re.compile(r"\bpython[0-9.]*\s+-c\s", re.I)
_PY_PERIGO = re.compile(
    r"shutil\.rmtree|os\.remove|os\.unlink|os\.rmdir|subprocess"
    r"|requests\.(post|put|delete|patch)|urlopen",
    re.I,
)

_LEITURA = {"Read", "Glob", "Grep", "NotebookRead"}
_ESCRITA = {"Write", "Edit", "NotebookEdit"}
_COMANDO = {"Bash", "PowerShell"}


def classificar(ferramenta: str, entrada: dict, *, raiz: Path, config: dict) -> Classificacao:
    """Classifica uma ação. Qualquer exceção vira TRAVADO (falha segura)."""
    try:
        if ferramenta in _LEITURA:
            return _classificar_leitura(entrada, config)
        if ferramenta in _ESCRITA:
            return _classificar_escrita(entrada, config)
        if ferramenta in _COMANDO:
            return _classificar_comando(str(entrada.get("command", "")), config)
        return Classificacao(RASTREADO, "", f"ferramenta não classificada: {ferramenta}")
    except Exception as erro:  # noqa: BLE001 — falha segura é o requisito
        return Classificacao(
            TRAVADO,
            "R0",
            f"classificador falhou ({erro.__class__.__name__}); travando por segurança",
        )


def _pior(a: Classificacao, b: Classificacao) -> Classificacao:
    return b if _ORDEM[b.nivel] > _ORDEM[a.nivel] else a


def _e_segredo(alvo: str, config: dict) -> bool:
    if not alvo:
        return False
    caminho = Path(alvo)
    nome = caminho.name
    inteiro = caminho.as_posix()
    for padrao in config.get("padroes_segredo", []):
        if fnmatch(nome, padrao) or fnmatch(inteiro, f"*{padrao}"):
            return True
    return False


def _classificar_leitura(entrada: dict, config: dict) -> Classificacao:
    alvo = str(
        entrada.get("file_path") or entrada.get("path") or entrada.get("pattern") or ""
    )
    if _e_segredo(alvo, config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {Path(alvo).name}")
    return Classificacao(LIVRE, "", "leitura")


def _classificar_escrita(entrada: dict, config: dict) -> Classificacao:
    alvo = str(entrada.get("file_path") or entrada.get("notebook_path") or "")
    if not alvo:
        return Classificacao(RASTREADO, "", "escrita sem alvo identificável")
    if _e_segredo(alvo, config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {Path(alvo).name}")
    caminho = Path(alvo)
    if "tests" in caminho.parts or caminho.name.startswith("test_"):
        return Classificacao(LIVRE, "", "arquivo de teste")
    if caminho.exists():
        return Classificacao(RASTREADO, "", "arquivo já existe em disco")
    return Classificacao(LIVRE, "", "arquivo novo")


def _classificar_comando(comando: str, config: dict) -> Classificacao:
    if not comando.strip():
        return Classificacao(LIVRE, "", "comando vazio")
    resultado = Classificacao(LIVRE, "", "nenhuma regra travada casou")
    for segmento in _SEPARADORES.split(comando):
        resultado = _pior(resultado, _classificar_segmento(segmento, config))
    return resultado


def _classificar_segmento(segmento: str, config: dict) -> Classificacao:
    for alvo in _REDIRECT.findall(segmento):
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    if _INERTE.match(segmento):
        return Classificacao(LIVRE, "", "emissor inerte")

    limpo = _MSG_GIT.sub(" ", segmento) if re.match(r"\s*git\b", segmento) else segmento

    for regra, motivo, padrao in _familias(config):
        if re.search(padrao, limpo, re.I):
            return Classificacao(TRAVADO, regra, motivo)

    if _PY_INLINE.search(segmento):
        if _PY_PERIGO.search(segmento):
            return Classificacao(TRAVADO, "R8", "python -c com chamada perigosa")
        return Classificacao(
            RASTREADO, "R8", "python -c: conteúdo não inspecionável a fundo"
        )

    if _EXEC_INDIRETA.search(segmento):
        return Classificacao(RASTREADO, "R8", "execução indireta")

    return Classificacao(LIVRE, "", "comando sem regra travada")


def _familias(config: dict) -> tuple[tuple[str, str, str], ...]:
    extras = tuple(
        (item["regra"], item["motivo"], item["padrao"])
        for item in config.get("travado_extra", [])
    )
    return FAMILIAS + extras
```

- [ ] **Passo 4: Rodar os testes e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_risco.py -v
```

Esperado: `30 passed`. Se algum caso travado não travar, **corrija o padrão, nunca o
caso** — cada linha da tabela é uma decisão de política.

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add ferramentas && git commit -m "feat(risco): familias travadas com falha segura e 30 casos de mesa"
```

---

### Tarefa 3: Classificador de risco — livre, rastreado e os falsos positivos

**Arquivos:**
- Modificar: `ferramentas/tests/test_risco.py` (acrescentar ao fim)
- Modificar: `ferramentas/risco.py` (somente se algum caso falhar)

**Interfaces:**
- Consome: tudo o que a Tarefa 2 produziu.
- Produz: nenhuma função nova. Produz a garantia de que o classificador não trava trabalho
  legítimo — que é o que impede o usuário de aprovar no automático.

- [ ] **Passo 1: Escrever os testes que faltam**

Acrescentar ao fim de `ferramentas/tests/test_risco.py`:

```python
LIVRES = [
    ("pytest", "Bash", {"command": "pytest -q"}),
    ("git-status", "Bash", {"command": "git status --short"}),
    ("git-diff", "Bash", {"command": "git diff HEAD~1"}),
    ("ls", "Bash", {"command": "ls -la"}),
    ("echo-com-rm-dentro", "Bash", {"command": 'echo "rm -rf /"'}),
    ("git-commit-falando-de-rm", "Bash", {"command": 'git commit -m "remove rm morto"'}),
    ("npm-run-build", "Bash", {"command": "npm run build"}),
]


@pytest.mark.parametrize("ident,ferramenta,entrada", LIVRES, ids=[c[0] for c in LIVRES])
def test_comandos_legitimos_ficam_livres(ident, ferramenta, entrada, tmp_path):
    resultado = risco.classificar(ferramenta, entrada, raiz=tmp_path, config=CFG)
    assert resultado.nivel == risco.LIVRE, f"{ident} não devia travar: {resultado}"


def test_arquivo_novo_e_livre(tmp_path):
    alvo = tmp_path / "app" / "novo.py"
    resultado = risco.classificar(
        "Write", {"file_path": str(alvo)}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.LIVRE


def test_arquivo_existente_e_rastreado(tmp_path):
    alvo = tmp_path / "servico.py"
    alvo.write_text("x = 1", encoding="utf-8")
    resultado = risco.classificar(
        "Edit", {"file_path": str(alvo)}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.RASTREADO


def test_teste_existente_continua_livre(tmp_path):
    destino = tmp_path / "tests"
    destino.mkdir()
    alvo = destino / "test_algo.py"
    alvo.write_text("def test_x(): pass", encoding="utf-8")
    resultado = risco.classificar(
        "Write", {"file_path": str(alvo)}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.LIVRE


def test_caminho_windows_com_acento_e_espaco(tmp_path):
    destino = tmp_path / "meu projeto acentuação"
    destino.mkdir()
    alvo = destino / "novo.py"
    resultado = risco.classificar(
        "Write", {"file_path": str(alvo)}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.LIVRE


def test_ferramenta_desconhecida_e_rastreada(tmp_path):
    resultado = risco.classificar(
        "mcp__servico__gravar", {"dado": 1}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.RASTREADO


def test_python_inline_inofensivo_e_rastreado(tmp_path):
    resultado = risco.classificar(
        "Bash", {"command": 'python -c "print(1)"'}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.RASTREADO


def test_bash_c_e_rastreado(tmp_path):
    resultado = risco.classificar(
        "Bash", {"command": 'bash -c "make build"'}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.RASTREADO


def test_bash_c_com_rm_dentro_trava(tmp_path):
    """A família casa no comando cru, então o payload entre aspas não escapa."""
    resultado = risco.classificar(
        "Bash", {"command": 'bash -c "rm -rf /tmp/x"'}, raiz=tmp_path, config=CFG
    )
    assert resultado.nivel == risco.TRAVADO
    assert resultado.regra == "R3"


def test_delete_from_com_where_nao_trava(tmp_path):
    resultado = risco.classificar(
        "Bash",
        {"command": 'psql -c "DELETE FROM contas WHERE id = 1"'},
        raiz=tmp_path,
        config=CFG,
    )
    assert resultado.nivel != risco.TRAVADO
```

- [ ] **Passo 2: Rodar e ver quais falham**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_risco.py -v
```

Esperado: a maioria passa de primeira; os falsos positivos aparecem como falha. Anote quais.

- [ ] **Passo 3: Ajustar os padrões de `risco.py` até os falsos positivos sumirem**

Regra do ajuste: **nunca afrouxar uma família inteira para calar um caso**. A correção
certa é estreitar o padrão ou acrescentar uma exceção nomeada (como `_INERTE` e `_MSG_GIT`
já fazem). Se um ajuste exigir afrouxar uma família, pare e reporte — é mudança de política,
e política é decisão do usuário.

- [ ] **Passo 4: Rodar a suíte inteira**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `46 passed` (4 de config + 42 de risco). Cole a saída.

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add ferramentas && git commit -m "test(risco): livre, rastreado e os falsos positivos conhecidos"
```

---

### Tarefa 4: Estado e máquina de fases

**Arquivos:**
- Criar: `ferramentas/estado.py`
- Criar: `ferramentas/tests/test_estado.py`

**Interfaces:**
- Consome: nada além da biblioteca padrão.
- Produz:
  - `estado.FASES: tuple[str, ...]`
  - `estado.TRANSICOES: dict[str, tuple[str, ...]]`
  - `estado.TransicaoInvalida(Exception)`
  - `estado.caminho(raiz: Path) -> Path` → `raiz/.engine/estado.json`
  - `estado.carregar(raiz: Path) -> dict | None`
  - `estado.gravar(raiz: Path, dados: dict) -> None` (escrita atômica)
  - `estado.novo_ciclo(raiz: Path, objetivo: str, agora: str, modo: str = "normal") -> dict`
  - `estado.transicionar(dados: dict, destino: str) -> dict`
  - `estado.desligar(raiz: Path) -> dict`
  - `estado.registrar_diff(raiz: Path, caminho_arquivo: str) -> dict`

- [ ] **Passo 1: Escrever o teste que falha**

Criar `ferramentas/tests/test_estado.py`:

```python
"""Testes da máquina de fases e da persistência do estado."""
import json

import pytest

from ferramentas import estado

AGORA = "2026-07-30T14:02:11"


def test_novo_ciclo_grava_em_disco_e_comeca_na_descoberta(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "somar dois numeros", AGORA)
    assert dados["ativo"] is True
    assert dados["fase"] == "DESCOBERTA"
    assert dados["ciclo"]["objetivo"] == "somar dois numeros"
    assert dados["ciclo"]["iniciado_em"] == AGORA
    gravado = json.loads(estado.caminho(tmp_path).read_text(encoding="utf-8"))
    assert gravado == dados


def test_carregar_sem_estado_devolve_none(tmp_path):
    assert estado.carregar(tmp_path) is None


def test_transicao_valida_avanca_e_registra(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    dados = estado.transicionar(dados, "ANALISE")
    assert dados["fase"] == "ANALISE"
    assert dados["fases_concluidas"] == ["DESCOBERTA"]


def test_transicao_invalida_levanta(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    with pytest.raises(estado.TransicaoInvalida):
        estado.transicionar(dados, "ENTREGA")


def test_teste_volta_para_build(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    for destino in ("ANALISE", "PLANO", "BUILD", "TESTE"):
        dados = estado.transicionar(dados, destino)
    dados = estado.transicionar(dados, "BUILD")
    assert dados["fase"] == "BUILD"


def test_todas_as_fases_do_grafo_sao_alcancaveis():
    alcancadas = {"DESCOBERTA"}
    fronteira = ["DESCOBERTA"]
    while fronteira:
        atual = fronteira.pop()
        for destino in estado.TRANSICOES[atual]:
            if destino not in alcancadas:
                alcancadas.add(destino)
                fronteira.append(destino)
    assert alcancadas == set(estado.FASES)


def test_desligar_preserva_o_ciclo(tmp_path):
    estado.novo_ciclo(tmp_path, "x", AGORA)
    dados = estado.desligar(tmp_path)
    assert dados["ativo"] is False
    assert dados["ciclo"]["objetivo"] == "x"


def test_registrar_diff_nao_duplica(tmp_path):
    estado.novo_ciclo(tmp_path, "x", AGORA)
    estado.registrar_diff(tmp_path, "app/servico.py")
    dados = estado.registrar_diff(tmp_path, "app/servico.py")
    assert dados["diffs_pendentes"] == ["app/servico.py"]


def test_gravacao_e_atomica(tmp_path):
    """Não pode sobrar arquivo temporário depois de gravar."""
    estado.novo_ciclo(tmp_path, "x", AGORA)
    restos = list((tmp_path / ".engine").glob("*.tmp"))
    assert restos == []
```

- [ ] **Passo 2: Rodar e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_estado.py -v
```

Esperado: `ModuleNotFoundError: No module named 'ferramentas.estado'`.

- [ ] **Passo 3: Escrever a implementação**

Criar `ferramentas/estado.py`:

```python
"""Estado do ENGINE: persistência em disco e máquina de fases.

O estado vive em `<projeto>/.engine/estado.json`. É disco, não contexto — é isso que
faz o modo sobreviver à compactação.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

FASES: tuple[str, ...] = (
    "DESCOBERTA",
    "ANALISE",
    "EVOLUCAO",
    "PLANO",
    "BUILD",
    "TESTE",
    "REVISAO",
    "DOC",
    "ENTREGA",
)

TRANSICOES: dict[str, tuple[str, ...]] = {
    "DESCOBERTA": ("ANALISE",),
    "ANALISE": ("EVOLUCAO", "PLANO"),
    "EVOLUCAO": ("PLANO",),
    "PLANO": ("BUILD",),
    "BUILD": ("TESTE",),
    "TESTE": ("BUILD", "REVISAO"),
    "REVISAO": ("BUILD", "DOC"),
    "DOC": ("ENTREGA",),
    "ENTREGA": (),
}

VERSAO = 1


class TransicaoInvalida(Exception):
    """Passagem de fase que não existe no grafo da especificação."""


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "estado.json"


def carregar(raiz: Path) -> dict | None:
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        return json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def gravar(raiz: Path, dados: dict) -> None:
    """Escrita atômica: grava num temporário e substitui.

    Um hook interrompido no meio da escrita não pode deixar o estado corrompido —
    seria a única forma de o motor perder o ciclo sem ninguém perceber.
    """
    alvo = caminho(raiz)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    temporario = alvo.with_suffix(".json.tmp")
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporario, alvo)


def novo_ciclo(raiz: Path, objetivo: str, agora: str, modo: str = "normal") -> dict:
    dados = {
        "versao": VERSAO,
        "ativo": True,
        "ciclo": {
            "id": f"{agora[:10]}-1",
            "objetivo": objetivo,
            "iniciado_em": agora,
            "modo": modo,
        },
        "fase": "DESCOBERTA",
        "fases_concluidas": [],
        "cartoes": [],
        "decisoes": [],
        "pendencias": [],
        "diffs_pendentes": [],
        "cobrancas_por_fase": {},
    }
    gravar(raiz, dados)
    return dados


def transicionar(dados: dict, destino: str) -> dict:
    atual = dados["fase"]
    if destino not in TRANSICOES.get(atual, ()):
        permitidas = ", ".join(TRANSICOES.get(atual, ())) or "nenhuma"
        raise TransicaoInvalida(
            f"{atual} -> {destino} não existe no grafo; a partir de {atual} só: {permitidas}"
        )
    if atual not in dados["fases_concluidas"]:
        dados["fases_concluidas"].append(atual)
    dados["fase"] = destino
    return dados


def desligar(raiz: Path) -> dict:
    dados = carregar(raiz) or {}
    dados["ativo"] = False
    gravar(raiz, dados)
    return dados


def registrar_diff(raiz: Path, caminho_arquivo: str) -> dict:
    dados = carregar(raiz)
    if dados is None:
        return {}
    pendentes = dados.setdefault("diffs_pendentes", [])
    if caminho_arquivo not in pendentes:
        pendentes.append(caminho_arquivo)
    gravar(raiz, dados)
    return dados
```

- [ ] **Passo 4: Rodar e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `55 passed`. Cole a saída.

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add ferramentas && git commit -m "feat(estado): maquina de fases e persistencia atomica"
```

---

### Tarefa 5: Hook `PreToolUse` — o risco vira bloqueio de verdade

**Arquivos:**
- Criar: `hooks/engine_risco.py`
- Criar: `ferramentas/tests/test_hooks.py`

**Interfaces:**
- Consome: `ferramentas.risco.classificar`, `ferramentas.estado.carregar`,
  `ferramentas.estado.registrar_diff`, `ferramentas.config.carregar`.
- Produz: `hooks/engine_risco.py` executável, que lê JSON no stdin e comunica a decisão por
  código de saída: `0` libera, `2` bloqueia com o motivo no stderr.

- [ ] **Passo 1: Confirmar o contrato do hook antes de escrever**

Antes de implementar, confirme na documentação oficial do Claude Code o formato de entrada
do evento `PreToolUse` (chaves `tool_name`, `tool_input`, `cwd`) e o significado do código
de saída `2`. Despache o subagente `claude-code-guide` com a pergunta:
*"Qual é o JSON de entrada e o contrato de código de saída de um hook PreToolUse?"*

Se a documentação divergir do que este plano assume, **ajuste o plano e reporte** — não
implemente contra um contrato que você não confirmou.

- [ ] **Passo 2: Escrever o teste que falha**

Criar `ferramentas/tests/test_hooks.py`:

```python
"""Testes dos hooks: entrada JSON no stdin, decisão pelo código de saída."""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
HOOK_RISCO = RAIZ_PLUGIN / "hooks" / "engine_risco.py"

sys.path.insert(0, str(RAIZ_PLUGIN))
from ferramentas import estado  # noqa: E402


def _rodar(hook: Path, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env={**os.environ},
    )


def _ligar(raiz: Path) -> None:
    estado.novo_ciclo(raiz, "teste", "2026-07-30T00:00:00")


def test_motor_desligado_nao_bloqueia_nada(tmp_path):
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf x"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0


def test_acao_travada_bloqueia_com_motivo(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_RISCO,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git push origin main"},
            "cwd": str(tmp_path),
        },
        tmp_path,
    )
    assert saida.returncode == 2
    assert "R2" in saida.stderr


def test_acao_livre_passa(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0


def test_acao_rastreada_passa_e_registra_o_diff(tmp_path):
    _ligar(tmp_path)
    alvo = tmp_path / "servico.py"
    alvo.write_text("x = 1", encoding="utf-8")
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Edit", "tool_input": {"file_path": str(alvo)}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert str(alvo) in dados["diffs_pendentes"]


def test_stdin_invalido_bloqueia(tmp_path):
    _ligar(tmp_path)
    saida = subprocess.run(
        [sys.executable, str(HOOK_RISCO)],
        input="isso nao e json",
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
    )
    assert saida.returncode == 2
```

- [ ] **Passo 3: Rodar e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_hooks.py -v
```

Esperado: falha porque `hooks/engine_risco.py` não existe.

- [ ] **Passo 4: Escrever a implementação**

Criar `hooks/engine_risco.py`:

```python
#!/usr/bin/env python3
"""Hook PreToolUse do ENGINE.

Contrato: recebe o evento em JSON no stdin.
  saída 0  -> a ação segue
  saída 2  -> a ação é bloqueada; o stderr explica o motivo ao Claude

Falha segura: qualquer erro no caminho de decisão bloqueia. A única exceção é o motor
desligado — aí o hook não tem opinião sobre nada.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado, risco  # noqa: E402


def principal() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        print("ENGINE: evento do hook ilegível; bloqueando por segurança", file=sys.stderr)
        return 2

    raiz = Path(evento.get("cwd") or ".")

    dados = estado.carregar(raiz)
    if not dados or not dados.get("ativo"):
        return 0

    try:
        cfg = config.carregar(raiz)
        veredito = risco.classificar(
            evento.get("tool_name", ""),
            evento.get("tool_input") or {},
            raiz=raiz,
            config=cfg,
        )
    except Exception as erro:  # noqa: BLE001
        print(
            f"ENGINE: falha ao classificar ({erro}); bloqueando por segurança",
            file=sys.stderr,
        )
        return 2

    if dados.get("ciclo", {}).get("modo") == "dry" and veredito.nivel != risco.LIVRE:
        print("ENGINE [modo seco]: nenhuma escrita é executada neste ciclo", file=sys.stderr)
        return 2

    if veredito.nivel == risco.TRAVADO:
        print(
            f"ENGINE [{veredito.regra}] ação travada: {veredito.motivo}.\n"
            f"Apresente ao usuário o que pretende fazer e o impacto, e peça confirmação "
            f"com opções clicáveis antes de tentar de novo.",
            file=sys.stderr,
        )
        return 2

    if veredito.nivel == risco.RASTREADO:
        alvo = (evento.get("tool_input") or {}).get("file_path")
        if alvo:
            try:
                estado.registrar_diff(raiz, alvo)
            except Exception:  # noqa: BLE001
                pass  # registrar é acessório; não pode bloquear ação já liberada
    return 0


if __name__ == "__main__":
    sys.exit(principal())
```

- [ ] **Passo 5: Rodar e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `60 passed`. Cole a saída.

- [ ] **Passo 6: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add hooks ferramentas && git commit -m "feat(hook): PreToolUse bloqueia acao travada com falha segura"
```

---

### Tarefa 6: Hook `UserPromptSubmit` — o cartão de estado

**Arquivos:**
- Criar: `hooks/engine_contexto.py`
- Modificar: `ferramentas/tests/test_hooks.py` (acrescentar ao fim)

**Interfaces:**
- Consome: `ferramentas.estado.carregar`, `ferramentas.config.carregar`.
- Produz: `hooks/engine_contexto.py` executável. Imprime o cartão no stdout (que o Claude
  Code injeta como contexto adicional) e sai com `0`. Motor desligado: não imprime nada.
- Produz `montar_cartao(dados: dict, cfg: dict) -> str`, importável e testável sem
  subprocesso.

- [ ] **Passo 1: Escrever o teste que falha**

Acrescentar ao fim de `ferramentas/tests/test_hooks.py`:

```python
HOOK_CONTEXTO = RAIZ_PLUGIN / "hooks" / "engine_contexto.py"


def _importar_contexto():
    sys.path.insert(0, str(RAIZ_PLUGIN / "hooks"))
    import engine_contexto

    return engine_contexto


def test_motor_desligado_nao_injeta_nada(tmp_path):
    saida = _rodar(HOOK_CONTEXTO, {"cwd": str(tmp_path)}, tmp_path)
    assert saida.returncode == 0
    assert saida.stdout.strip() == ""


def test_cartao_traz_fase_objetivo_e_invariantes(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(HOOK_CONTEXTO, {"cwd": str(tmp_path)}, tmp_path)
    assert saida.returncode == 0
    assert "DESCOBERTA" in saida.stdout
    assert "teste" in saida.stdout
    assert "Nunca afirmar sucesso sem ter olhado" in saida.stdout


def test_cartao_respeita_o_teto_de_linhas():
    from ferramentas import config

    contexto = _importar_contexto()
    cfg = dict(config.PADRAO)
    dados = {
        "ativo": True,
        "fase": "BUILD",
        "ciclo": {"objetivo": "o" * 400, "modo": "normal"},
        "cartoes": [f"cartao-{i}" for i in range(50)],
        "decisoes": [{"o_que": f"decisao {i}", "porque": "motivo"} for i in range(50)],
        "diffs_pendentes": [f"arquivo_{i}.py" for i in range(50)],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    assert len(cartao.splitlines()) <= cfg["teto_cartao_linhas"]
```

- [ ] **Passo 2: Rodar e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_hooks.py -v
```

Esperado: falha porque `hooks/engine_contexto.py` não existe.

- [ ] **Passo 3: Escrever a implementação**

Criar `hooks/engine_contexto.py`:

```python
#!/usr/bin/env python3
"""Hook UserPromptSubmit do ENGINE.

Injeta o cartão de estado a cada turno. É este hook — e não o texto da skill — que faz
o modo sobreviver à compactação do contexto.

Teto duro de linhas: acima dele, o motor passa a competir com o pedido do usuário pelo
mesmo espaço de atenção, que é exatamente a doença que ele veio curar.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado  # noqa: E402

INVARIANTES = (
    "1. Nunca afirmar sucesso sem ter olhado. Rodou, cola a saída; não rodou, diz que não rodou.",
    "2. Nunca ajustar o teste para o código passar. O teste é o contrato.",
    "3. Nunca inventar arquivo, API, número ou regra de negócio. Sem evidência, é pendência.",
    "4. Nunca tocar em item fora do escopo declarado do ciclo.",
    "5. Toda decisão técnica sai com a justificativa junto.",
)


def _cortar(texto: str, limite: int) -> str:
    texto = " ".join(str(texto).split())
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def montar_cartao(dados: dict, cfg: dict) -> str:
    teto = int(cfg.get("teto_cartao_linhas", 40))
    ciclo = dados.get("ciclo", {})
    cabecalho = [
        "== ENGINE ativo ==",
        f"Fase: {dados.get('fase', '?')}   Modo: {ciclo.get('modo', 'normal')}",
        f"Objetivo do ciclo: {_cortar(ciclo.get('objetivo', ''), 160)}",
    ]
    rodape = ["Invariantes:", *INVARIANTES]

    orcamento = max(teto - len(cabecalho) - len(rodape), 0)
    corpo: list[str] = []

    def acrescentar(linha: str) -> None:
        if len(corpo) < orcamento:
            corpo.append(linha)

    cartoes = dados.get("cartoes") or []
    if cartoes:
        acrescentar(f"Cartões: {_cortar(', '.join(cartoes), 120)}")

    decisoes = dados.get("decisoes") or []
    if decisoes:
        acrescentar("Decisões fechadas:")
        for item in decisoes:
            acrescentar(
                f"  - {_cortar(item.get('o_que', ''), 70)}: {_cortar(item.get('porque', ''), 70)}"
            )

    diffs = dados.get("diffs_pendentes") or []
    if diffs:
        acrescentar(f"Diffs por apresentar ({len(diffs)}): {_cortar(', '.join(diffs), 120)}")

    pendencias = dados.get("pendencias") or []
    if pendencias:
        acrescentar(f"Pendências ({len(pendencias)}): {_cortar('; '.join(pendencias), 120)}")

    linhas = cabecalho + corpo[:orcamento] + rodape
    return "\n".join(linhas[:teto])


def principal() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0  # sem contexto injetado; nunca atrapalha o turno do usuário

    raiz = Path(evento.get("cwd") or ".")
    dados = estado.carregar(raiz)
    if not dados or not dados.get("ativo"):
        return 0

    cfg = config.carregar(raiz)
    saida = montar_cartao(dados, cfg)
    for aviso in cfg.get("_avisos", []):
        saida += f"\nENGINE aviso: {aviso}"
    print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(principal())
```

- [ ] **Passo 4: Rodar e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `63 passed`. Cole a saída.

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add hooks ferramentas && git commit -m "feat(hook): UserPromptSubmit injeta o cartao de estado com teto de linhas"
```

---

### Tarefa 7: CLI e a skill `/engine`

**Arquivos:**
- Criar: `ferramentas/cli.py`
- Criar: `skills/engine/SKILL.md`
- Criar: `ferramentas/tests/test_cli.py`
- Modificar: `docs/specs/2026-07-30-engine-design.md` (tabela da seção 12)

**Interfaces:**
- Consome: `ferramentas.estado`.
- Produz: `python -m ferramentas.cli <verbo> [args]` com os verbos `ligar <objetivo>`,
  `desligar`, `status`, `fase <DESTINO>`. Sucesso sai com `0`; erro de uso, `1`. A raiz do
  projeto hospedeiro vem da variável de ambiente `ENGINE_RAIZ`, caindo no diretório corrente.

- [ ] **Passo 1: Escrever o teste que falha**

Criar `ferramentas/tests/test_cli.py`:

```python
"""Testes da CLI usada pela skill /engine."""
import os
import subprocess
import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]


def _cli(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "ferramentas.cli", *args],
        capture_output=True,
        text=True,
        cwd=str(RAIZ_PLUGIN),
        env={**os.environ, "ENGINE_RAIZ": str(cwd)},
    )


def test_ligar_cria_o_estado(tmp_path):
    saida = _cli(tmp_path, "ligar", "somar dois numeros")
    assert saida.returncode == 0
    assert (tmp_path / ".engine" / "estado.json").is_file()
    assert "DESCOBERTA" in saida.stdout


def test_status_com_motor_desligado(tmp_path):
    saida = _cli(tmp_path, "status")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


def test_desligar_depois_de_ligar(tmp_path):
    _cli(tmp_path, "ligar", "x")
    saida = _cli(tmp_path, "desligar")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


def test_fase_invalida_reporta_erro_sem_estourar(tmp_path):
    _cli(tmp_path, "ligar", "x")
    saida = _cli(tmp_path, "fase", "ENTREGA")
    assert saida.returncode == 1
    assert "não existe no grafo" in saida.stdout + saida.stderr


def test_verbo_desconhecido_sai_com_erro(tmp_path):
    saida = _cli(tmp_path, "voar")
    assert saida.returncode == 1
```

- [ ] **Passo 2: Rodar e confirmar que falha**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_cli.py -v
```

Esperado: `No module named ferramentas.cli`.

- [ ] **Passo 3: Escrever a implementação**

Criar `ferramentas/cli.py`:

```python
"""Interface de linha de comando do ENGINE, usada pela skill /engine.

A raiz do projeto hospedeiro vem de ENGINE_RAIZ quando definida; senão, do diretório
corrente. Isso mantém a CLI testável sem depender de onde ela é executada.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from ferramentas import estado

USO = "uso: python -m ferramentas.cli {ligar <objetivo>|desligar|status|fase <DESTINO>}"


def _raiz() -> Path:
    return Path(os.environ.get("ENGINE_RAIZ") or Path.cwd())


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _relatar(dados: dict) -> str:
    ciclo = dados.get("ciclo", {})
    linhas = [
        f"**ENGINE:** {'ativo' if dados.get('ativo') else 'desligado'}",
        f"**Fase:** {dados.get('fase', '?')}  ·  **Modo:** {ciclo.get('modo', 'normal')}",
        f"**Objetivo:** {ciclo.get('objetivo', '(nenhum)')}",
        f"**Fases concluídas:** {', '.join(dados.get('fases_concluidas') or []) or '(nenhuma)'}",
        f"**Diffs por apresentar:** {len(dados.get('diffs_pendentes') or [])}",
        f"**Pendências:** {len(dados.get('pendencias') or [])}",
    ]
    for item in dados.get("decisoes") or []:
        linhas.append(f"- decisão: {item.get('o_que')} — {item.get('porque')}")
    return "\n".join(linhas)


def principal(argumentos: list[str]) -> int:
    if not argumentos:
        print(USO)
        return 1
    verbo, *resto = argumentos
    raiz = _raiz()

    if verbo == "ligar":
        objetivo = " ".join(resto).strip()
        if not objetivo:
            print("ENGINE: 'ligar' exige o objetivo do ciclo em uma frase.")
            return 1
        print(_relatar(estado.novo_ciclo(raiz, objetivo, _agora())))
        return 0

    if verbo == "desligar":
        print(_relatar(estado.desligar(raiz)))
        return 0

    if verbo == "status":
        dados = estado.carregar(raiz)
        if not dados:
            print("**ENGINE:** desligado (nenhum ciclo neste projeto).")
            return 0
        print(_relatar(dados))
        return 0

    if verbo == "fase":
        if not resto:
            print(USO)
            return 1
        dados = estado.carregar(raiz)
        if not dados:
            print("**ENGINE:** desligado; não há fase para mudar.")
            return 1
        try:
            dados = estado.transicionar(dados, resto[0].upper())
        except estado.TransicaoInvalida as erro:
            print(f"ENGINE: {erro}")
            return 1
        estado.gravar(raiz, dados)
        print(_relatar(dados))
        return 0

    print(USO)
    return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
```

Criar `skills/engine/SKILL.md`:

```markdown
---
name: engine
description: Liga o modo ENGINE — motor de engenharia com ciclo em fases, elenco de agentes por papel e portas de segurança graduadas por risco. Use quando o pedido for "/engine", "/engine off", "/engine status", "ligar o motor", "desligar o motor", ou quando o usuário pedir para conduzir um trabalho de engenharia de ponta a ponta.
---

# ENGINE

Motor de engenharia persistente. O ciclo é sempre do motor: ferramenta externa (ECC,
superpowers) executa **dentro** de uma fase; nenhuma decide qual é a fase seguinte nem
quando o ciclo termina. Instrução direta do usuário sempre vence o motor.

## Verbos

| Pedido do usuário | O que fazer |
|---|---|
| `/engine <pedido>` | rode `python -m ferramentas.cli ligar "<objetivo em uma frase>"` e entre em DESCOBERTA |
| `/engine off` | rode `python -m ferramentas.cli desligar` e apresente o resumo do ciclo |
| `/engine status` | rode `python -m ferramentas.cli status` e apresente a saída |

Rode sempre a partir da raiz do plugin, com `ENGINE_RAIZ` apontando para a raiz do projeto
em que se está trabalhando.

## O ciclo

`DESCOBERTA → ANALISE → [EVOLUCAO, se o projeto já existe] → PLANO → ⟨porta⟩ → BUILD ⇄
TESTE → REVISAO → DOC → ENTREGA`

Avance de fase com `python -m ferramentas.cli fase <DESTINO>`. A CLI recusa transição fora
do grafo — se ela recusar, a fase pretendida está errada, não a máquina.

**Porta do plano.** Ao terminar PLANO, apresente arquitetura, stack, estrutura e a
justificativa de cada decisão, e **espere** o usuário. É a única parada por fase.

## Papéis

Despache o subagente do papel correspondente à fase (`agents/`): `arquiteto` no PLANO,
`implementador` no BUILD, `revisor` na REVISAO, `documentador` no DOC. Antes de despachar,
leia os cartões de `cartoes/` relevantes à stack e passe o conteúdo ao subagente.

## Quando o hook travar uma ação

O hook de risco devolve `[R<n>] ação travada`. Não tente de novo por outro caminho, não
contorne com outra ferramenta. Apresente ao usuário **o que pretende fazer e o impacto**, e
peça confirmação com opções clicáveis.

## Invariantes

Valem em toda fase, e o hook de contexto os relembra a cada turno:

1. Nunca afirmar sucesso sem ter olhado.
2. Nunca ajustar o teste para o código passar.
3. Nunca inventar arquivo, API, número ou regra de negócio.
4. Nunca tocar em item fora do escopo declarado do ciclo.
5. Toda decisão técnica sai com a justificativa junto.
```

- [ ] **Passo 4: Atualizar a tabela da seção 12 do spec**

Em `docs/specs/2026-07-30-engine-design.md`, na tabela da seção 12, acrescentar a linha:

```markdown
| `cli.py` | ponto de entrada da skill: `ligar`, `desligar`, `status`, `fase` |
```

O spec é o contrato; quando o código precisa de algo que ele não previu, é o spec que cede,
por escrito.

- [ ] **Passo 5: Rodar e confirmar que passam**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `68 passed`. Cole a saída.

- [ ] **Passo 6: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add ferramentas skills docs && git commit -m "feat(cli): verbos ligar/desligar/status/fase e a skill engine"
```

---

### Tarefa 8: Empacotar como plugin e registrar os hooks

**Arquivos:**
- Criar: `.claude-plugin/plugin.json`
- Criar: `hooks/hooks.json`
- Criar: `README.md`

**Interfaces:**
- Consome: `hooks/engine_risco.py`, `hooks/engine_contexto.py`, `skills/engine/SKILL.md`.
- Produz: um plugin instalável em escopo de usuário.

- [ ] **Passo 1: Confirmar o contrato do plugin antes de escrever**

Confirme na documentação oficial: o esquema de `.claude-plugin/plugin.json`; se o arquivo de
hooks do plugin é `hooks/hooks.json`; e se `${CLAUDE_PLUGIN_ROOT}` é a variável que resolve
a raiz do plugin dentro do comando de um hook. Despache `claude-code-guide` com:
*"Como um plugin do Claude Code declara hooks e qual variável aponta para a raiz do plugin?"*

Se divergir, ajuste este plano e reporte antes de implementar.

- [ ] **Passo 2: Escrever o manifesto, o registro dos hooks e o README**

Criar `.claude-plugin/plugin.json`:

```json
{
  "name": "engine",
  "version": "0.1.0",
  "description": "Motor de engenharia persistente: ciclo em fases, papéis por etapa e portas de segurança graduadas por risco."
}
```

Criar `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/engine_risco.py\""
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/engine_contexto.py\""
          }
        ]
      }
    ]
  }
}
```

Criar `README.md`:

````markdown
# ENGINE

Motor de engenharia para o Claude Code. Liga com `/engine`, desliga com `/engine off`.

O que o distingue de um prompt longo: o modo vive em `.engine/estado.json` no projeto, é
re-injetado a cada turno por um hook, e sobrevive à compactação do contexto. E cada ação
passa por um classificador de risco antes de acontecer — o que é barato desfazer acontece
sozinho; o que é irreversível para e pergunta.

- Especificação: `docs/specs/2026-07-30-engine-design.md`
- Plano da Fase 1: `docs/plans/2026-07-30-engine-fase-1.md`

## Testes

```bash
python -m pytest ferramentas/tests -v
```

## Estado atual

Fase 1 (núcleo). Fases 2 e 3 descritas na seção 15 da especificação.
````

- [ ] **Passo 3: Verificar que a suíte segue verde**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -q
```

Esperado: `68 passed`.

- [ ] **Passo 4: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add .claude-plugin hooks README.md && git commit -m "feat(plugin): manifesto, registro dos hooks e README"
```

---

### Tarefa 9: Os quatro papéis e os três cartões

**Arquivos:**
- Criar: `agents/arquiteto.md`, `agents/implementador.md`, `agents/revisor.md`, `agents/documentador.md`
- Criar: `cartoes/python.md`, `cartoes/pytest.md`, `cartoes/ui-ux.md`, `cartoes/_catalogo.md`

**Interfaces:**
- Consome: a skill `skills/engine/SKILL.md`, que despacha estes papéis por fase.
- Produz: quatro subagentes nomeados `arquiteto`, `implementador`, `revisor`, `documentador`.

- [ ] **Passo 1: Escrever os quatro agentes**

Criar `agents/arquiteto.md`:

```markdown
---
name: arquiteto
description: Decide stack, estrutura, contratos, estratégia de teste e de deploy — cada decisão com a justificativa junto. Papel da fase PLANO do ENGINE. Não escreve código de produção.
tools: Read, Grep, Glob, Write
---

# Arquiteto

**Missão.** Transformar o objetivo do ciclo e o mapa do projeto num plano que outra pessoa
consiga executar sem adivinhar nada.

**Entradas.** O objetivo do ciclo; o mapa do projeto quando houver; os cartões da stack.

**Saídas.** Um plano com: estrutura de arquivos e a responsabilidade de cada um; contratos
(assinaturas, tipos, nomes) entre as partes; estratégia de teste; estratégia de entrega. E,
para cada decisão, uma linha de justificativa — sem ela a decisão não está tomada, está
apenas escrita.

**Limitações.** Não escreve código de produção. Não decide por evidência que não viu: se um
arquivo importa para a decisão, leia-o antes; se não puder lê-lo, diga isso no plano em vez
de supor.

**Critério de pronto.** Cada arquivo do plano tem dono e responsabilidade; cada contrato
entre partes tem nome e tipo; cada decisão tem justificativa.
```

Criar `agents/implementador.md`:

```markdown
---
name: implementador
description: Escreve o código do plano — completo, funcional, comentado onde o porquê não é óbvio. Papel da fase BUILD do ENGINE. Único papel com escrita ampla.
tools: Read, Grep, Glob, Write, Edit, Bash
---

# Implementador

**Missão.** Executar o plano do arquiteto, arquivo por arquivo, até o código rodar.

**Entradas.** O plano; a direção visual quando houver; os cartões da stack.

**Saídas.** Código completo e funcional. Nada de pseudocódigo, nada de `TODO` deixado no
lugar da implementação, nada de função que devolve valor fixo esperando alguém terminar.

**Limitações.** Não muda o plano no meio: se o plano estiver errado, pare e relate — o
arquiteto revisa. Não escreve teste que apenas confirma o próprio código.

**Critério de pronto.** O código roda, a suíte existente continua verde, e a saída real da
execução está colada no relato — não "deve passar".
```

Criar `agents/revisor.md`:

```markdown
---
name: revisor
description: Revisa arquitetura, legibilidade e manutenibilidade do diff do ciclo. Papel da fase REVISAO do ENGINE. Relata; não conserta.
tools: Read, Grep, Glob, Bash
---

# Revisor

**Missão.** Encontrar, no que foi escrito neste ciclo, o que vai custar caro depois.

**Entradas.** O diff do ciclo; o plano; os cartões da stack.

**Saídas.** Achados classificados em BLOQUEANTE / IMPORTANTE / SUGESTÃO, cada um com
arquivo, linha, o defeito e o cenário concreto em que ele falha. Achado sem cenário concreto
é opinião — não entre com ele.

**Limitações.** **Não edita nada.** Conserto silencioso destrói o valor do relatório: quem
lê não fica sabendo o que estava errado. Não repita o que um linter já pega.

**Critério de pronto.** Todo achado BLOQUEANTE tem um cenário de falha reproduzível descrito
em uma frase.
```

Criar `agents/documentador.md`:

```markdown
---
name: documentador
description: Produz documentação técnica e funcional, diagramas Mermaid, ADRs e contratos de API a partir do que o ciclo realmente entregou. Papel da fase DOC do ENGINE.
tools: Read, Grep, Glob, Write, Edit
---

# Documentador

**Missão.** Registrar o que o ciclo entregou, de modo que alguém sem contexto consiga usar e
manter.

**Entradas.** O plano, o diff do ciclo, os achados da revisão.

**Saídas.** Documentação técnica e funcional; diagramas em Mermaid **sempre seguidos de
descrição textual** (diagrama sozinho não é acessível e não sobrevive a quem lê em texto
puro); ADR para cada decisão arquitetural; contrato de API e modelo de dados quando houver.

**Limitações.** Documenta o que existe, não o que se pretendia. Se o código diverge do
plano, documente o código e **registre a divergência** — nunca documente o plano fingindo
que é o código.

**Critério de pronto.** Todo diagrama tem descrição; toda decisão arquitetural do ciclo tem
ADR; nenhum exemplo de uso foi escrito sem ter sido executado.
```

- [ ] **Passo 2: Escrever os três cartões**

Criar `cartoes/python.md`:

```markdown
---
tecnologia: python
detectar: ["pyproject.toml", "setup.py", "requirements*.txt", "**/*.py"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-30
---

## Convenções
- PEP 8; nomes em `snake_case`; classes em `CapWords`.
- `from __future__ import annotations` no topo de módulo que usa anotação de tipo moderna.
- Caminho de arquivo com `pathlib.Path`, nunca por concatenação de string.
- Escrita de arquivo sempre com `encoding="utf-8"` explícito — no Windows o default não é UTF-8.

## Armadilhas
- Argumento default mutável (`def f(x=[])`) é compartilhado entre chamadas.
- `except Exception` sem re-levantar engole o erro; só é aceitável quando a falha segura é o requisito, e aí precisa de comentário dizendo isso.
- `os.replace` é atômico; `shutil.move` entre volumes diferentes não é.
- Comparar float com `==` falha; use `math.isclose`.

## Comandos
- Suíte: `python -m pytest -q`
- Um teste: `python -m pytest caminho/test_x.py::test_y -v`

## Checklist de review
- [ ] Toda exceção capturada é tratada ou re-levantada.
- [ ] Nenhum caminho de arquivo montado por concatenação.
- [ ] Nenhuma escrita de arquivo sem `encoding`.
- [ ] Funções com uma responsabilidade; arquivo grande foi dividido.
```

Criar `cartoes/pytest.md`:

```markdown
---
tecnologia: pytest
detectar: ["pytest.ini", "pyproject.toml:pytest", "tests/**/test_*.py"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-30
---

## Convenções
- Arquivo `test_*.py`, função `test_*`, um comportamento por teste.
- O nome do teste descreve o comportamento, não a função chamada: `test_arquivo_novo_e_livre`, não `test_classificar_2`.
- `tmp_path` para qualquer coisa que toque disco. Teste que escreve no repositório é teste quebrado.
- Tabela de casos com `@pytest.mark.parametrize` e `ids=` legíveis — o `id` é o que aparece quando falha.

## Armadilhas
- Teste que depende da ordem de execução de outro teste é falso-verde.
- `assert x` sem mensagem numa tabela parametrizada esconde qual caso quebrou; passe a mensagem.
- Mockar o que se está testando transforma o teste em tautologia.
- Ajustar o teste para o código passar destrói o único contrato que existe.

## Comandos
- Suíte: `python -m pytest -q`
- Verboso com os nomes dos casos: `python -m pytest -v`

## Checklist de review
- [ ] Cada teste falha se o comportamento que ele descreve for removido.
- [ ] Nenhum teste escreve fora de `tmp_path`.
- [ ] Casos parametrizados têm `ids` legíveis.
```

Criar `cartoes/ui-ux.md`:

```markdown
---
tecnologia: ui-ux
detectar: ["**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.html", "**/*.css"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-30
---

## Convenções
- Hierarquia antes de ornamento: o que o usuário precisa ver primeiro tem que ser o maior contraste da tela.
- Escala tipográfica limitada (4 a 6 tamanhos) e espaçamento em múltiplos de uma unidade base.
- Estado vazio, estado de carregamento e estado de erro fazem parte da tela — tela só com o caminho feliz está incompleta.
- Cor nunca é o único portador de informação (daltonismo); acompanhe de forma, ícone ou texto.

## Armadilhas
- Contraste abaixo de 4.5:1 em texto de corpo reprova em WCAG AA.
- Alvo de toque menor que 44×44 px é inutilizável em telefone.
- Animação sem `prefers-reduced-motion` causa mal-estar em quem tem sensibilidade vestibular.
- Foco de teclado removido (`outline: none`) sem substituto torna a interface inoperável sem mouse.

## Checklist de review
- [ ] Todo controle é alcançável e visível por teclado.
- [ ] Contraste de texto de corpo ≥ 4.5:1.
- [ ] Estados vazio, carregando e erro existem.
- [ ] Nenhuma informação transmitida só por cor.
```

Criar `cartoes/_catalogo.md`:

```markdown
# Catálogo de cartões

| Cartão | Papéis que carregam | Fase do ENGINE |
|---|---|---|
| `python` | arquiteto, implementador, revisor | 1 |
| `pytest` | arquiteto, implementador, revisor | 1 |
| `ui-ux` | arquiteto, implementador, revisor | 1 |

A Fase 2 acrescenta: `fastapi`, `excel-vba`, `office-scripts`, `power-query`, `react`,
`typescript`, `postgresql`, `sqlite`, `mermaid`.

Na Fase 1 os cartões são lidos diretamente pelos papéis. A detecção automática de stack
(`ferramentas/detectar.py`) é Fase 2.
```

- [ ] **Passo 3: Verificar que cada agente tem front-matter**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -c "import pathlib,sys; falhas=[p.name for p in pathlib.Path('agents').glob('*.md') if not p.read_text(encoding='utf-8').startswith('---')]; print('sem front-matter:', falhas); sys.exit(1 if falhas else 0)"
```

Esperado: `sem front-matter: []` e código de saída 0.

- [ ] **Passo 4: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add agents cartoes && git commit -m "feat(papeis): arquiteto, implementador, revisor, documentador e 3 cartoes"
```

---

### Tarefa 10: Aceite da Fase 1

Esta tarefa não escreve produto. Ela decide se a Fase 1 está pronta — e a resposta pode ser
"não".

**Arquivos:**
- Criar: `aceite/fase-1.md`
- Criar: `CHANGELOG.md`

**Interfaces:**
- Consome: tudo.
- Produz: o registro datado do que foi verificado, com a saída real colada.

- [ ] **Passo 1: Rodar a suíte completa e colar a saída**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests -v
```

Esperado: `68 passed`. Cole a saída literal em `aceite/fase-1.md`.

- [ ] **Passo 2: Verificar que as sete famílias travam pelo hook, e não só na unidade**

Criar `aceite/verificar_familias.py`:

```python
"""Verificação de aceite: as sete famílias travadas travam pelo hook de verdade."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ferramentas import estado  # noqa: E402

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "engine_risco.py"

CASOS = [
    ("R1", "Bash", {"command": "curl -X POST https://exemplo/x"}),
    ("R2", "Bash", {"command": "git push origin main"}),
    ("R3", "Bash", {"command": "rm -rf build"}),
    ("R4", "Bash", {"command": 'psql -c "DROP TABLE x"'}),
    ("R6", "Bash", {"command": "terraform apply"}),
    ("R7", "Bash", {"command": "npm install -g pnpm"}),
]


def main() -> int:
    raiz = Path(tempfile.mkdtemp())
    estado.novo_ciclo(raiz, "aceite da fase 1", "2026-07-30T00:00:00")
    casos = CASOS + [("R5", "Write", {"file_path": str(raiz / ".env")})]
    falhas = []
    for regra, ferramenta, entrada in casos:
        evento = {"tool_name": ferramenta, "tool_input": entrada, "cwd": str(raiz)}
        saida = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(evento),
            capture_output=True,
            text=True,
        )
        travou = saida.returncode == 2
        print(f"{regra}: {'TRAVOU' if travou else 'PASSOU'}  <- {entrada}")
        if not travou:
            falhas.append(regra)
    print("FALHAS:", falhas or "nenhuma")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
```

Rodar:

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python aceite/verificar_familias.py
```

Esperado: sete linhas com `TRAVOU`, `FALHAS: nenhuma`, código de saída 0. Cole a saída
literal em `aceite/fase-1.md`.

- [ ] **Passo 3: Verificar o teto do cartão de estado**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && python -m pytest ferramentas/tests/test_hooks.py::test_cartao_respeita_o_teto_de_linhas -v
```

Esperado: `1 passed`.

- [ ] **Passo 4: Registrar o aceite**

Criar `aceite/fase-1.md` com: a data (`2026-07-30`); as três saídas coladas dos passos 1 a 3;
e uma seção **"o que NÃO foi verificado"**, listando honestamente o que ficou para a Fase 3 —
a sobrevivência real a 20 turnos e a uma compactação em sessão de verdade, e os quatro
cenários de aceite com projetos-cobaia.

Criar `CHANGELOG.md`:

```markdown
# CHANGELOG

## 2026-07-30 — Fase 1 (núcleo)

- `config`, `risco`, `estado`, `cli` em Python de biblioteca padrão.
- Hooks `PreToolUse` (classificação de risco com falha segura) e `UserPromptSubmit`
  (cartão de estado com teto de linhas).
- Skill `/engine` com `ligar`, `desligar`, `status`.
- Papéis: arquiteto, implementador, revisor, documentador.
- Cartões: python, pytest, ui-ux.
- Verificação em `aceite/fase-1.md`.

**Não verificado nesta fase:** sobrevivência a 20 turnos reais e a uma compactação; os
quatro cenários de aceite com projetos-cobaia. Ambos são Fase 3.
```

- [ ] **Passo 5: Commitar**

```bash
cd "C:/Users/Usuário/Desktop/ENGINE" && git add aceite CHANGELOG.md && git commit -m "chore(aceite): verificacao da fase 1 com saida colada"
```

---

## Auto-revisão do plano

**Cobertura da especificação (Fase 1).** `config.py` → T1. `risco.py` → T2 e T3.
`estado.py` → T4. `hooks/engine_risco.py` → T5. `hooks/engine_contexto.py` → T6.
Skill `/engine` com `on/off/status` → T7. Plugin instalável → T8. Quatro papéis e três
cartões → T9. Testes de risco e de estado → T2, T3, T4. Critério de pronto da Fase 1 → T10.

**Lacuna assumida e declarada.** O critério "o modo sobrevive a 20 turnos e a uma
compactação" (spec, seção 15) **não é verificável por teste automatizado** — depende de uma
sessão real. A Tarefa 10 o registra explicitamente como não verificado, em vez de fingir
cobertura. A verificação acontece na primeira sessão de uso e vira item da Fase 3.

**Consistência de tipos.** `Classificacao(nivel, regra, motivo)` é usada com os mesmos três
campos em T2, T3 e T5. `estado.carregar` devolve `dict | None` e todos os consumidores tratam
o `None`. `montar_cartao(dados, cfg)` tem a mesma assinatura no teste e na implementação
(T6). `config.carregar(raiz)` sempre inclui `_avisos`, consumido em T6. O teste de falha
segura em T2 faz monkeypatch de `risco._classificar_comando`, que existe com esse nome exato
na implementação da mesma tarefa.

**Sem placeholders.** Nenhum passo diz "implementar depois" ou "tratar os casos de borda":
todo passo de código traz o código.
