"""Classificador de risco do ENGINE.

Regra de ouro: na dúvida, **RASTREADO** — nunca LIVRE. Este módulo nunca libera por
falha e nunca libera por omissão.

**Arquitetura: lista de permissões, não lista de proibições.** As famílias R1–R8
continuam decidindo o que sobe para TRAVADO, mas o que sobra **não** é livre: só é
livre o que casa com uma lista curta e explícita de operações comprovadamente
inócuas (`COMANDOS_LIVRES`). Tudo o mais executa e fica no relatório.

A inversão veio de evidência: quatro rodadas de revisão acharam doze bypasses da
lista de proibições, e a quarta ainda achou cinco novos (quebra de linha como
separador, substituição de comando genérica, `cmd /c`, `git -C ... push`,
`cat .env`). Lista de proibição não converge — sempre falta um vetor que ninguém
enumerou. Lista de permissão fecha o buraco sem precisar prevê-lo.

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


# Opções globais do git, que ficam ANTES do subcomando (`git -C /repo push`). Sem
# reconhecê-las, o padrão de R2 exigia `git` colado em `push` e `git -C /repo push
# --force` saía livre.
_GIT_GLOBAL = (
    r"(?:(?:-[cC]\s+\S+|--git-dir=\S+|--work-tree=\S+|--namespace=\S+"
    r"|--exec-path=\S+|--no-pager|-p|-P)\s+)*"
)

FAMILIAS: tuple[tuple[str, str, str], ...] = (
    (
        "R1",
        "escrita de rede",
        r"\bcurl\b[^\n]*\s-X\s*(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]*\s--request\s+(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]*\s(-d|--data|--data-raw|--data-binary)\b"
        r"|\bcurl\b[^\n]*\s(--upload-file|-T)\b"
        r"|\bwget\b[^\n]*--post",
    ),
    (
        "R2",
        "git que sai da máquina ou reescreve história",
        r"\bgit\s+" + _GIT_GLOBAL + r"(push|rebase)\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"reset\s+--hard\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"clean\s+-[a-zA-Z]*f"
        r"|\bgit\s+" + _GIT_GLOBAL + r"checkout\s+--\s",
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

# ---------------------------------------------------------------------------
# Lista de permissões (o coração da política nova)
# ---------------------------------------------------------------------------

#: Primeiro token que, sozinho, pode tornar um segmento LIVRE — desde que todas as
#: outras condições de `_motivo_fora_da_lista` também valham. Conjunto deliberadamente
#: curto: só leitura/inspeção da biblioteca padrão de qualquer máquina.
COMANDOS_LIVRES: frozenset[str] = frozenset(
    {
        "ls",
        "dir",
        "pwd",
        "cd",
        "cat",
        "type",
        "head",
        "tail",
        "wc",
        "sort",
        "uniq",
        "grep",
        "findstr",
        "rg",
        "find",
        "tree",
        "echo",
        "printf",
        "which",
        "where",
        "git",
        "pytest",
        "stat",
        "file",
        "diff",
        "date",
        "whoami",
    }
)

#: Comandos livres cujo primeiro token, isolado, NÃO é inócuo: `python` só é livre
#: como `python -m pytest`, `npm` só como `npm run`/`npm test`, `node` só para pedir
#: a versão. Comparados por prefixo de tokens.
COMANDOS_LIVRES_COMPOSTOS: tuple[str, ...] = (
    "python -m pytest",
    "node --version",
    "npm run",
    "npm test",
)

#: Subcomandos de git que apenas leem o repositório.
SUBCOMANDOS_GIT_LIVRES: frozenset[str] = frozenset(
    {
        "status",
        "diff",
        "log",
        "show",
        "branch",
        "remote",
        "rev-parse",
        "ls-files",
        "blame",
        "describe",
        "shortlog",
    }
)

#: Opções globais do git que consomem o argumento seguinte.
_GIT_GLOBAIS_COM_VALOR = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"})

#: `find` que executa ou apaga não é leitura.
_FIND_PERIGOSO = ("-exec", "-execdir", "-delete", "-ok")

_INERTE = re.compile(r"^\s*(echo|printf|#)\b", re.I)
_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
#: Formas que EXECUTAM um comando escondido dentro do argumento de outro. Checadas
#: sobre o segmento inteiro, não só dentro de `echo`/`-m`: `ls $(rm -rf /dados)` e
#: ``ls `rm -rf /dados` `` escapavam justamente porque a checagem era local.
_EXECUCAO_ESCONDIDA = re.compile(r"\$\(|`|<\(|>\(")
#: Expansão de variável não executa nada, mas torna o segmento não inspecionável:
#: desqualifica da lista de permissões (vira RASTREADO), sem travar.
_EXPANSAO_VARIAVEL = re.compile(r"\$\{")
_REDIRECT = re.compile(r">>?\s*([^\s;|&]+)")
#: Disparadores de execução indireta. Inclui os interpretadores do Windows — o projeto
#: roda em Windows e `cmd /c "del /s /q C:\dados"` saía livre.
_EXEC_INDIRETA = re.compile(
    r"\b(bash|sh|zsh|ksh|dash)\s+-c\s"
    r"|\b(pwsh|powershell)(\.exe)?\s+"
    r"(-Command|-c|-EncodedCommand|-enc|-ec|-e|-File|-f)\b"
    r"|\bcmd(\.exe)?\s+/[ck]\b"
    r"|\beval\s",
    re.I,
)
_CANO_INTERPRETE = re.compile(
    r"\|\s*(sudo\s+)?"
    r"(bash|sh|zsh|ksh|python[0-9.]*|perl|ruby|node"
    r"|powershell(\.exe)?|pwsh|cmd(\.exe)?|iex|invoke-expression)\b",
    re.I,
)
_PY_INLINE = re.compile(r"\bpython[0-9.]*\s+-c\s", re.I)
_PY_PERIGO = re.compile(
    r"shutil\.rmtree|shutil\.move|os\.remove|os\.unlink|os\.rmdir|subprocess"
    r"|requests\.(post|put|delete|patch)|urlopen"
    r"|os\.system|os\.popen|os\.exec\w*|os\.spawn\w*"
    r"|\beval\(|\bexec\(|Path\(.*\)\.unlink",
    re.I,
)

_LEITURA = {"Read", "Glob", "Grep", "NotebookRead"}
_ESCRITA = {"Write", "Edit", "NotebookEdit"}
_COMANDO = {"Bash", "PowerShell"}


def classificar(ferramenta: str, entrada: dict, *, raiz: Path, config: dict) -> Classificacao:
    """Classifica uma ação. Qualquer exceção vira TRAVADO (falha segura)."""
    try:
        if ferramenta in _LEITURA:
            return _classificar_leitura(entrada, raiz, config)
        if ferramenta in _ESCRITA:
            return _classificar_escrita(entrada, raiz, config)
        if ferramenta in _COMANDO:
            bruto = entrada.get("command")
            if bruto is None:
                # Antes isto virava a string "None" (ou "") e saía LIVRE por omissão.
                # Sem comando legível não há prova positiva de inocuidade nenhuma.
                return Classificacao(
                    RASTREADO, "", "comando ausente ou nulo: nada a liberar por prova"
                )
            return _classificar_comando(str(bruto), config)
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


def _resolver_alvo(alvo: str, raiz: Path) -> Path:
    """Resolve um alvo relativo contra a raiz do projeto hospedeiro.

    Caminho absoluto passa direto — o comportamento para esse caso fica idêntico
    ao de antes. Caminho relativo (`.env`, `src/x.py`) hoje é checado contra o
    diretório de trabalho do processo, que pode não ser o projeto hospedeiro; sem
    isso, a checagem de segredo/existência mira no lugar errado.
    """
    caminho = Path(alvo)
    if caminho.is_absolute():
        return caminho
    return raiz / caminho


def _classificar_leitura(entrada: dict, raiz: Path, config: dict) -> Classificacao:
    alvo = str(
        entrada.get("file_path") or entrada.get("path") or entrada.get("pattern") or ""
    )
    if not alvo:
        return Classificacao(LIVRE, "", "leitura")
    caminho = _resolver_alvo(alvo, raiz)
    if _e_segredo(caminho.as_posix(), config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {caminho.name}")
    return Classificacao(LIVRE, "", "leitura")


def _classificar_escrita(entrada: dict, raiz: Path, config: dict) -> Classificacao:
    alvo = str(entrada.get("file_path") or entrada.get("notebook_path") or "")
    if not alvo:
        return Classificacao(RASTREADO, "", "escrita sem alvo identificável")
    caminho = _resolver_alvo(alvo, raiz)
    if _e_segredo(caminho.as_posix(), config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {caminho.name}")
    if "tests" in caminho.parts or caminho.name.startswith("test_"):
        return Classificacao(LIVRE, "", "arquivo de teste")
    if caminho.exists():
        return Classificacao(RASTREADO, "", "arquivo já existe em disco")
    return Classificacao(LIVRE, "", "arquivo novo")


def _dividir_segmentos(comando: str) -> list[str]:
    """Divide o comando nos separadores de shell (`&&`, `||`, `;`, `|` e **quebra de
    linha**), mas nunca dentro de aspas simples ou duplas.

    Quebra de linha é separador de comando tanto quanto `;`: um bloco de várias linhas
    é uma LISTA de comandos. Sem tratá-la, `"echo ok\\nrm -rf /dados"` chegava como um
    segmento só, começado por `echo` — e saía livre pela válvula do emissor inerte.

    Um separador dentro de aspas não encadeia comandos: é conteúdo literal, como o
    `;` em `python -c "import shutil; shutil.rmtree('x')"`. Dividir ali cegava a
    checagem de `python -c` perigoso — a expressão nunca aparecia inteira em um único
    segmento.
    """
    segmentos: list[str] = []
    atual: list[str] = []
    aspas: str | None = None
    i = 0
    n = len(comando)
    while i < n:
        ch = comando[i]
        if aspas:
            atual.append(ch)
            if ch == aspas:
                aspas = None
            i += 1
            continue
        if ch in ("'", '"'):
            aspas = ch
            atual.append(ch)
            i += 1
            continue
        if comando[i : i + 2] in ("&&", "||"):
            segmentos.append("".join(atual))
            atual = []
            i += 2
            continue
        if comando[i : i + 2] == "\r\n":
            segmentos.append("".join(atual))
            atual = []
            i += 2
            continue
        if ch in (";", "|", "\n", "\r"):
            segmentos.append("".join(atual))
            atual = []
            i += 1
            continue
        atual.append(ch)
        i += 1
    segmentos.append("".join(atual))
    return segmentos


_LIMITE_PROFUNDIDADE_INDIRETA = 3


def _classificar_comando(comando: str, config: dict, profundidade: int = 0) -> Classificacao:
    if not comando.strip():
        return Classificacao(RASTREADO, "", "comando vazio: nada a liberar por prova")
    if _CANO_INTERPRETE.search(comando):
        # Checagem sobre o comando INTEIRO, antes de dividir em segmentos: dividir
        # primeiro quebra `curl ... | bash` em "curl ..." de um lado e "bash" do
        # outro, e nenhum dos dois pedaços isolados casa nenhuma família — o "baixar
        # e executar" só aparece quando os dois lados são vistos juntos.
        return Classificacao(
            TRAVADO, "R8", "cano para interpretador (baixar e executar)"
        )
    resultado: Classificacao | None = None
    for segmento in _dividir_segmentos(comando):
        if not segmento.strip():
            continue
        parcial = _classificar_segmento(segmento, config, profundidade)
        resultado = parcial if resultado is None else _pior(resultado, parcial)
    if resultado is None:
        return Classificacao(RASTREADO, "", "comando vazio: nada a liberar por prova")
    return resultado


def _classificar_segmento(segmento: str, config: dict, profundidade: int = 0) -> Classificacao:
    for alvo_cru in _REDIRECT.findall(segmento):
        # O alvo pode vir entre aspas (`> ".env"`): tira as aspas antes de comparar
        # com os padrões de segredo, senão o fnmatch nunca casa e o redirecionamento
        # sai LIVRE por engano.
        alvo = alvo_cru.strip("'\"")
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    if _EXECUCAO_ESCONDIDA.search(segmento):
        # `$(...)`, crase e substituição de processo executam um comando escondido
        # dentro do argumento de outro, seja qual for o comando de fora. A checagem
        # era local (só `echo` e o `-m` do git); `ls $(rm -rf /dados)` passava.
        return Classificacao(
            TRAVADO, "R8", "substituição de comando dentro do argumento"
        )

    if _INERTE.match(segmento) and not _REDIRECT.search(segmento):
        # `echo`/`printf` sem substituição de comando e sem redirecionamento só
        # imprimem texto literal na tela. A válvula existe para não travar buscas e
        # mensagens que apenas MENCIONAM um verbo perigoso. Com `>` no meio deixa de
        # ser emissão e vira escrita em disco, que não é livre — segue o fluxo.
        return Classificacao(LIVRE, "", "emissor inerte")

    eh_git = re.match(r"\s*git\b", segmento)
    if eh_git:
        # O texto de `-m` é literal (a substituição de comando já foi travada acima):
        # apagá-lo evita que a mensagem do commit case uma família por engano.
        limpo = _MSG_GIT.sub(" ", segmento)
    else:
        limpo = segmento

    for regra, motivo, padrao in _familias(config):
        if re.search(padrao, limpo, re.I):
            return Classificacao(TRAVADO, regra, motivo)

    for token in _tokens(limpo)[1:]:
        # `cat .env` não é leitura inócua: até então só a ferramenta `Read` travava
        # segredo, e qualquer leitura pelo shell escapava.
        if _e_segredo(token, config):
            return Classificacao(TRAVADO, "R5", f"argumento aponta para segredo: {token}")

    if _PY_INLINE.search(segmento):
        if _PY_PERIGO.search(segmento):
            return Classificacao(TRAVADO, "R8", "python -c com chamada perigosa")
        return Classificacao(
            RASTREADO, "R8", "python -c: conteúdo não inspecionável a fundo"
        )

    if _EXEC_INDIRETA.search(segmento):
        return _classificar_execucao_indireta(segmento, config, profundidade)

    motivo = _motivo_fora_da_lista(segmento, config)
    if motivo is None:
        return Classificacao(LIVRE, "", "operação na lista de permissões")
    return Classificacao(RASTREADO, "", motivo)


def _tokens(segmento: str) -> list[str]:
    """Tokens do segmento, sem as aspas externas de cada um.

    Divisão por espaço em branco de propósito: é previsível e não levanta exceção com
    aspas desbalanceadas (`shlex` levanta, e uma exceção aqui viraria TRAVADO em cima
    de comando trivial).
    """
    return [bruto.strip("'\"") for bruto in segmento.split() if bruto.strip("'\"")]


def _subcomando_git(tokens: list[str]) -> str:
    """Primeiro token do git que não seja opção global (`git -C /repo status` → status)."""
    i = 1
    while i < len(tokens):
        token = tokens[i]
        if token in _GIT_GLOBAIS_COM_VALOR:
            i += 2
            continue
        if token.startswith("-"):
            i += 1
            continue
        return token
    return ""


def _motivo_fora_da_lista(segmento: str, config: dict) -> str | None:
    """Devolve `None` se o segmento é comprovadamente inócuo; senão, o motivo textual
    de ele não ter sido liberado.

    Esta função é a inversão da política: nada é livre por não casar uma proibição;
    é livre por casar uma PERMISSÃO.
    """
    tokens = _tokens(segmento)
    if not tokens:
        return "segmento sem comando identificável"

    if _EXPANSAO_VARIAVEL.search(segmento):
        return "expansão de variável (`${...}`) torna o segmento não inspecionável"
    if ">" in segmento:
        return "redirecionamento de saída: escrever não é operação livre"

    primeiro = tokens[0]
    composto = " ".join(tokens[:3])
    livre_composto = any(
        composto.startswith(prefixo) for prefixo in COMANDOS_LIVRES_COMPOSTOS
    )
    if not livre_composto and primeiro not in COMANDOS_LIVRES:
        return f"comando fora da lista de permitidos: `{primeiro}`"

    if primeiro == "git":
        sub = _subcomando_git(tokens)
        if sub not in SUBCOMANDOS_GIT_LIVRES:
            return f"subcomando git fora da lista de permitidos: `{sub or '(nenhum)'}`"

    if primeiro == "find":
        for perigoso in _FIND_PERIGOSO:
            if perigoso in tokens:
                return f"`find` com `{perigoso}` executa ou apaga, não é leitura"

    for token in tokens[1:]:
        if _e_segredo(token, config):
            return f"argumento aponta para segredo: {token}"

    return None


def _classificar_execucao_indireta(
    segmento: str, config: dict, profundidade: int
) -> Classificacao:
    """Extrai o payload entre aspas de uma execução indireta e reclassifica-o.

    `bash -c "rm -rf x"` não pode sair RASTREADO só por reconhecer a superfície
    do padrão: o comando real mora dentro das aspas. Sem extrair e reclassificar
    esse literal recursivamente, um `rm` disfarçado de `bash -c` escaparia — foi
    exatamente esse escape que motivou (erradamente) alargar a âncora de R3 no
    lugar de tratar a execução indireta de verdade.

    O mesmo vale para os interpretadores do Windows: `cmd /c "del /s /q C:\\dados"`
    e `pwsh -c "rm -rf x"`. Quando não há payload legível — o caso de
    `powershell -EncodedCommand <base64>` — não há o que inspecionar, e o que não
    se inspeciona não se libera.
    """
    if profundidade >= _LIMITE_PROFUNDIDADE_INDIRETA:
        return Classificacao(
            TRAVADO, "R8", "aninhamento de subcomando além do limite"
        )

    casamento = _EXEC_INDIRETA.search(segmento)
    payload = _extrair_payload_indireto(segmento[casamento.end() :])
    if payload is None:
        return Classificacao(
            TRAVADO, "R8", "execução indireta sem payload legível"
        )

    resultado_payload = _classificar_comando(payload, config, profundidade + 1)
    resultado_segmento = Classificacao(RASTREADO, "R8", "execução indireta")
    return _pior(resultado_segmento, resultado_payload)


def _extrair_payload_indireto(resto: str) -> str | None:
    """Devolve o literal entre aspas (simples ou duplas) logo após o disparador
    de execução indireta, ou `None` se não houver aspas para extrair."""
    casamento = re.search(r"(['\"])(.*)\1", resto, re.S)
    if not casamento:
        return None
    return casamento.group(2)


def _familias(config: dict) -> tuple[tuple[str, str, str], ...]:
    extras = tuple(
        (item["regra"], item["motivo"], item["padrao"])
        for item in config.get("travado_extra", [])
    )
    return FAMILIAS + extras
