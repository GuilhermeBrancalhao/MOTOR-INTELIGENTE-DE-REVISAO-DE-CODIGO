"""Classificador de risco do ENGINE.

Regra de ouro: na dúvida, **RASTREADO** — nunca LIVRE. Este módulo nunca libera por
falha e nunca libera por omissão.

**Comando de shell nunca é `livre`.** Só existem duas saídas para um comando: ou ele
casa uma das famílias R1–R9 (a checagem de segredo, o cano para interpretador, a
substituição de comando e a escrita no painel de controle entram aqui) e vira
`TRAVADO`, ou vira `RASTREADO` — executa e aparece no relatório de fim de fase.

Famílias documentadas: **R1** escrita de rede · **R2** git que sai da máquina ou
reescreve história · **R3** deleção · **R4** alteração destrutiva de banco · **R5**
segredo (caminho **e** conteúdo com padrão de credencial) · **R6** deploy ou
infraestrutura · **R7** instalação global · **R8** execução indireta, cano para
interpretador e substituição de comando · **R9** escrita no painel de controle do
motor (qualquer alvo sob um diretório `.engine/`). `R0` é a falha segura do próprio
classificador.

**R9 protege o painel de controle.** `.engine/estado.json` guarda `"ativo"`, o
interruptor dos dois hooks; `.engine/config.json` guarda `padroes_segredo`, o único
insumo da família R5. Sem R9, uma única escrita nesses dois arquivos desligava o motor
inteiro (`"ativo": false`) ou desarmava a checagem de segredo (`"padroes_segredo": []`)
— e a escrita saía `rastreado` ou até `livre`, isto é, executava. Leitura de `.engine/`
continua `livre`: ler o painel não muda nada.

A política anterior tentava liberar comando por prova positiva: uma lista de nomes
permitidos, depois lista de nomes **mais** forma de argumento. Sete rodadas de revisão
adversarial atacaram essa lista e, a cada rodada, acharam um caminho novo para `livre`
com ação destrutiva — a última foi `git diff --output=/home/user/.bashrc` e o apelido
`where` do PowerShell rodando .NET arbitrário dentro de um bloco de script. A causa é
estrutural, não uma flag esquecida: **cada comando permitido é ele próprio uma
linguagem**, com flags, apelidos e formas de argumento que nenhuma lista enumera até o
fim. Enquanto existir a categoria, existe a próxima rodada.

Eliminar a categoria fecha a família inteira de uma vez, incluindo o emissor inerte
(`echo`/`printf`), que era a última válvula capaz de liberar um segmento por prefixo.
O custo aceito é o relatório de fim de fase ficar mais longo: todo comando aparece
nele. `rastreado` custa uma linha de relatório; `livre` errado custa um estrago.

As famílias são casadas sobre o comando CRU, de propósito: SQL perigoso quase sempre
chega dentro de aspas (`psql -c "DROP TABLE x"`), então limpar literais antes de casar
cegaria justamente a família mais cara. A única proteção contra falso positivo que
sobrou é estreita e explícita: o texto de `-m` do git.

Ferramenta de ARQUIVO mantém a política de sempre — leitura que não é segredo é livre,
escrita em arquivo NOVO (inclusive sob `tests/`) é livre, escrita em arquivo que já
existe é rastreada, segredo é travado dos dois lados.

**Sobrescrever teste que já existe é `rastreado`, não `livre`.** Antes, todo alvo sob
`tests/` (ou com nome `test_*`) saía `livre` mesmo por cima de um arquivo existente —
o que fazia da violação do invariante "nunca ajustar o teste para o código passar"
justamente a única escrita invisível no relatório da fase. Criar teste novo continua
`livre`; reescrever um que já existe aparece no relatório.
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


#: Motivo único de todo comando que não trava. Não há mais graduação a explicar: ou
#: travou por regra, ou executa e fica registrado.
_MOTIVO_COMANDO = "comando de shell: executado e registrado no relatório da fase"

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

_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
#: Formas que EXECUTAM um comando escondido dentro do argumento de outro. Checadas
#: sobre o segmento inteiro, não só dentro de `echo`/`-m`: `ls $(rm -rf /dados)` e
#: ``ls `rm -rf /dados` `` escapavam justamente porque a checagem era local.
_EXECUCAO_ESCONDIDA = re.compile(r"\$\(|`|<\(|>\(")
_REDIRECT = re.compile(r">>?\s*([^\s;|&]+)")
#: Disparadores de execução indireta. Inclui os interpretadores do Windows — o projeto
#: roda em Windows e `cmd /c "del /s /q C:\dados"` precisa ter o payload inspecionado.
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

#: Nome do diretório do painel de controle do motor. Estado e configuração vivem
#: dentro dele, e escrever ali é desligar ou desarmar o próprio motor (família R9).
_PAINEL = ".engine"

#: Padrões de chave conhecidos, casados contra o CONTEÚDO de uma escrita. A spec
#: (seção 5, item 5) sempre prometeu esta checagem; sem ela, `Write` com uma chave da
#: AWS no corpo saía `livre` só porque o nome do arquivo não casava `padroes_segredo`.
#: São formas com prefixo fixo e comprimento mínimo, de propósito: reconhecem a chave
#: pela forma que o emissor lhe deu, não por adivinhação sobre o texto em volta.
_PADROES_CREDENCIAL = re.compile(
    r"sk-[A-Za-z0-9]{16,}"
    r"|ghp_[A-Za-z0-9]{16,}"
    r"|github_pat_[A-Za-z0-9_]{20,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\."
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
                # Sem comando legível não há nada a inspecionar — e nada a liberar.
                return Classificacao(
                    RASTREADO, "", "comando ausente ou nulo: nada a inspecionar"
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


def _sob_painel(alvo: str) -> bool:
    """Diz se o alvo está sob um diretório `.engine/` (o painel de controle).

    Olha os componentes do caminho, não o prefixo textual: `.engine/estado.json`,
    `C:/proj/.engine/config.json` e `sub/.engine/x` casam todos, enquanto um arquivo
    chamado `.engineering` não casa. Normaliza a barra invertida do Windows antes,
    porque o alvo de um redirecionamento de shell chega como texto cru.
    """
    if not alvo:
        return False
    return _PAINEL in Path(alvo.replace("\\", "/")).parts


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
    if _sob_painel(alvo) or _sob_painel(caminho.as_posix()):
        # R9 vem antes de tudo: gravar em `.engine/` é mexer no interruptor do motor,
        # e é o único alvo cuja escrita compromete a decisão sobre todos os outros.
        return Classificacao(TRAVADO, "R9", "escrita no painel de controle do motor")
    if _e_segredo(caminho.as_posix(), config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {caminho.name}")
    if _conteudo_com_credencial(entrada):
        return Classificacao(TRAVADO, "R5", "conteúdo com padrão de credencial")
    if caminho.exists():
        # Ordem invertida de propósito: a checagem de `tests/` ficava ACIMA desta e
        # liberava a sobrescrita de teste existente. Existir em disco decide primeiro.
        if _e_teste(caminho):
            return Classificacao(RASTREADO, "", "teste que já existe em disco")
        return Classificacao(RASTREADO, "", "arquivo já existe em disco")
    if _e_teste(caminho):
        return Classificacao(LIVRE, "", "arquivo de teste novo")
    return Classificacao(LIVRE, "", "arquivo novo")


def _e_teste(caminho: Path) -> bool:
    return "tests" in caminho.parts or caminho.name.startswith("test_")


def _conteudo_com_credencial(entrada: dict) -> bool:
    """Procura padrão de chave conhecida no corpo que a escrita vai gravar.

    `Write` traz o texto inteiro em `content`; `Edit` traz o trecho novo em
    `new_string`. Sem inspecioná-los, a família R5 só via o NOME do arquivo — e
    `Write` de um `AKIA…` dentro de `config.py` saía `livre`.
    """
    for chave in ("content", "new_string"):
        valor = entrada.get(chave)
        if isinstance(valor, str) and _PADROES_CREDENCIAL.search(valor):
            return True
    return False


def _dividir_segmentos(comando: str) -> list[str]:
    """Divide o comando nos separadores de shell (`&&`, `||`, `;`, `|` e **quebra de
    linha**), mas nunca dentro de aspas simples ou duplas.

    Quebra de linha é separador de comando tanto quanto `;`: um bloco de várias linhas
    é uma LISTA de comandos. Sem tratá-la, `"echo ok\\nrm -rf /dados"` chegava como um
    segmento só, e a família R3 nunca via o `rm` no início de um segmento.

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
        return Classificacao(RASTREADO, "", "comando vazio: nada a inspecionar")
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
        return Classificacao(RASTREADO, "", "comando vazio: nada a inspecionar")
    return resultado


def _classificar_segmento(
    segmento: str, config: dict, profundidade: int = 0
) -> Classificacao:
    """Trava o segmento se ele casar uma regra; senão devolve RASTREADO.

    Não há terceira saída. Nenhum prefixo, nome de comando ou forma de argumento
    produz LIVRE aqui — foi exatamente a tentativa de produzir LIVRE que sete rodadas
    de revisão furaram, uma vez por rodada.
    """
    for alvo_cru in _REDIRECT.findall(segmento):
        # O alvo pode vir entre aspas (`> ".env"`): tira as aspas antes de comparar
        # com os padrões de segredo, senão o fnmatch nunca casa.
        alvo = alvo_cru.strip("'\"")
        if _sob_painel(alvo):
            # `echo '{"ativo": false}' > .engine/estado.json` desliga o motor pelo
            # shell. A porta de R9 tem de cobrir os dois transportes de escrita.
            return Classificacao(
                TRAVADO, "R9", "escrita no painel de controle do motor"
            )
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    if _EXECUCAO_ESCONDIDA.search(segmento):
        # `$(...)`, crase e substituição de processo executam um comando escondido
        # dentro do argumento de outro, seja qual for o comando de fora.
        return Classificacao(
            TRAVADO, "R8", "substituição de comando dentro do argumento"
        )

    if re.match(r"\s*git\b", segmento):
        # O texto de `-m` é literal (a substituição de comando já foi travada acima):
        # apagá-lo evita que a mensagem do commit case uma família por engano.
        limpo = _MSG_GIT.sub(" ", segmento)
    else:
        limpo = segmento

    for regra, motivo, padrao in _familias(config):
        if re.search(padrao, limpo, re.I):
            return Classificacao(TRAVADO, regra, motivo)

    for token in _tokens(limpo)[1:]:
        # `cat .env` não é leitura inócua: sem isto, só a ferramenta `Read` travaria
        # segredo, e qualquer leitura pelo shell escaparia.
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

    return Classificacao(RASTREADO, "", _MOTIVO_COMANDO)


def _tokens(segmento: str) -> list[str]:
    """Tokens do segmento, sem as aspas externas de cada um.

    Divisão por espaço em branco de propósito: é previsível e não levanta exceção com
    aspas desbalanceadas (`shlex` levanta, e uma exceção aqui viraria TRAVADO em cima
    de comando trivial).
    """
    return [bruto.strip("'\"") for bruto in segmento.split() if bruto.strip("'\"")]


def _classificar_execucao_indireta(
    segmento: str, config: dict, profundidade: int
) -> Classificacao:
    """Extrai o payload entre aspas de uma execução indireta e reclassifica-o.

    `bash -c "rm -rf x"` não pode sair RASTREADO só por reconhecer a superfície
    do padrão: o comando real mora dentro das aspas. Sem extrair e reclassificar
    esse literal recursivamente, um `rm` disfarçado de `bash -c` escaparia.

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
