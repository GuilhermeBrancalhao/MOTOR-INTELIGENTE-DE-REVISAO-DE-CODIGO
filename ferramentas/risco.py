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
motor (qualquer alvo sob um diretório `.engine/`) · **R10** escrita em caminho de
execução persistente (hook de git, `.claude/`/`.vscode/`/`.idea/`, init de shell, perfil
do PowerShell, `Startup`, `crontab`, `.gitconfig`, `authorized_keys`) · **R11**
destruição de dados ou de infraestrutura (`truncate`, `dd`, `robocopy /MIR`, `format`,
`wsl --unregister`, `reg delete /f`, `pip uninstall`, truncamento por `>`) · **R12**
comando grande demais para classificar com segurança. `R0` é a falha segura do próprio
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

#: Todo quantificador ilimitado (`.*`, `[^\n]*`, `[^...]*`) que varre o comando cru vira
#: um `{0,N}` limitado. `[^\n]*` era O(n²) no classificador: `\bcurl\b[^\n]*\s-X…`
#: sobre `'curl '*6400` levava segundos porque o motor tentava casar o sufixo a partir
#: de cada `curl`. Um teto no comprimento do trecho varrido corta o retrocesso pela raiz
#: sem cegar nenhum caso real — comando útil não tem 200+ caracteres entre um verbo e a
#: sua flag perigosa.
_JANELA = "{0,200}"

FAMILIAS: tuple[tuple[str, str, str], ...] = (
    (
        "R1",
        "escrita de rede",
        r"\bcurl\b[^\n]" + _JANELA + r"\s-X\s*(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]" + _JANELA + r"\s--request\s+(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]" + _JANELA + r"\s(-d|--data|--data-raw|--data-binary)\b"
        r"|\bcurl\b[^\n]" + _JANELA + r"\s(--upload-file|-T)\b"
        r"|\bwget\b[^\n]" + _JANELA + r"--post",
    ),
    (
        "R2",
        "git que sai da máquina ou reescreve história",
        r"\bgit\s+" + _GIT_GLOBAL + r"(push|rebase)\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"reset\s+--hard\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"clean\s+-[a-zA-Z]*f"
        r"|\bgit\s+" + _GIT_GLOBAL + r"checkout\s+--\s"
        # Reescrita/descarte de história e de árvore de trabalho: apagam trabalho local
        # sem passar pela rede, mas sem volta. `git restore .`/`git checkout .` jogam
        # fora mudanças não commitadas; `reflog expire`/`gc --prune`/`stash clear`
        # descartam o histórico de recuperação; `worktree remove`/`update-ref -d`
        # removem referências.
        r"|\bgit\s+" + _GIT_GLOBAL + r"restore\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"checkout\s+\.(?:\s|$)"
        r"|\bgit\s+" + _GIT_GLOBAL + r"stash\s+clear\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"reflog\s+expire\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"gc\b[^\n]" + _JANELA + r"--prune"
        r"|\bgit\s+" + _GIT_GLOBAL + r"worktree\s+remove\b"
        r"|\bgit\s+" + _GIT_GLOBAL + r"update-ref\s+-d\b",
    ),
    (
        "R3",
        "deleção",
        r"(^|[\s;|&])(rm|rmdir|del|erase)\s"
        r"|\bRemove-Item\b"
        r"|\bClear-Content\b"
        r"|\bshred\b"
        r"|\bfind\b[^\n]" + _JANELA + r"\s-delete\b"
        r"|\bxargs\b[^\n]" + _JANELA + r"\brm\b"
        r"|(^|[\s;|&])/(?:usr/)?bin/rm\b",
    ),
    (
        "R4",
        "alteração destrutiva de banco",
        r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b"
        r"|\bALTER\s+TABLE\b"
        r"|\bDELETE\s+FROM\b(?![^;\"']" + _JANELA + r"\bWHERE\b)"
        r"|\b(alembic|flyway|liquibase)\b[^\n]" + _JANELA + r"\b(upgrade|migrate)\b"
        r"|\bmanage\.py\s+migrate\b",
    ),
    (
        "R6",
        "deploy ou infraestrutura",
        r"\bdocker\s+push\b"
        r"|\bdocker\s+(?:system\s+)?prune\b"
        r"|\bkubectl\s+apply\b"
        r"|\bterraform\s+apply\b"
        r"|\bgh\s+workflow\s+run\b"
        r"|\bnpm\s+publish\b"
        r"|\btwine\s+upload\b",
    ),
    (
        "R7",
        "instalação global",
        # `pip install` de PACOTE AVULSO é global; `pip install -r`, `-e` e `.` instalam
        # a dependência declarada DO PROJETO — rotina, não pode travar. A distinção
        # entra por um lookahead negativo: só trava se NÃO houver `-r`/`-e`/`.` logo em
        # seguida.
        r"\bnpm\s+(i|install)\b[^\n]" + _JANELA + r"\s-g\b"
        r"|\bpip[0-9.]*\s+install\b(?![^\n]" + _JANELA
        + r"(?:\s-r\b|\s--requirement\b|\s-e\b|\s--editable\b|\s\.(?:\s|$)))"
        r"|\bwinget\s+install\b"
        r"|\bchoco\s+install\b",
    ),
    (
        "R11",
        "destruição de dados ou de infraestrutura",
        # Zeram/sobrescrevem arquivo ou volume sem passar por `rm`, e desregistram
        # infraestrutura inteira. `> arquivo` (só o redirecionamento, sem comando à
        # esquerda) trunca o arquivo a zero — `echo x > arquivo`, que TEM comando à
        # esquerda, não casa este padrão.
        r"\btruncate\s+-s\b"
        r"|\bdd\s+[^\n]" + _JANELA + r"\bof="
        r"|\brobocopy\b[^\n]" + _JANELA + r"/MIR\b"
        r"|\bcipher\s+/w"
        r"|\bformat\s+[A-Za-z]:"
        r"|\bwsl\b[^\n]" + _JANELA + r"--unregister\b"
        r"|\breg\s+delete\b[^\n]" + _JANELA + r"/f\b"
        r"|\bpip[0-9.]*\s+uninstall\b"
        r"|^\s*:?\s*>\s*[^\s;|&>]",
    ),
)

#: Ferramentas de busca de texto. Quando o PRIMEIRO token do segmento é uma delas, o SQL
#: que aparece é ARGUMENTO de busca (`grep 'DELETE FROM' log.txt`), não uma execução —
#: a família de banco (R4) não se aplica.
_FERRAMENTAS_BUSCA = {
    "grep", "egrep", "fgrep", "rg", "findstr", "ag", "ack", "sift",
}

_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
_REDIRECT = re.compile(r"(?:&>|>\||>>?)\s*([^\s;|&]+)")
#: Disparadores de execução indireta. Inclui os interpretadores do Windows — o projeto
#: roda em Windows e `cmd /c "del /s /q C:\dados"` precisa ter o payload inspecionado.
#: Aceita flags ARBITRÁRIAS entre o interpretador e o `-c`/`-Command`/`-EncodedCommand`
#: (`bash --norc -c`, `powershell -NoProfile -EncodedCommand`) e as formas combinadas do
#: shell (`-lc`, `-ic`, `-lic`): sem isso, uma única flag desarmava a inspeção do payload.
_EXEC_INDIRETA = re.compile(
    r"\b(?:bash|sh|zsh|ksh|dash)(?:\s+-{1,2}[\w-]+)*\s+-\w*c\b"
    r"|\b(?:pwsh|powershell)(?:\.exe)?(?:\s+-{1,2}[\w-]+)*\s+"
    r"(?:-Command|-c|-EncodedCommand|-enc|-ec|-e|-File|-f)\b"
    r"|\bcmd(?:\.exe)?\s+/[ck]\b"
    r"|\beval\s",
    re.I,
)
#: Baixar-e-executar: só é `cano para interpretador` quando a ORIGEM do cano é uma busca
#: de rede (`curl`/`wget`/`iwr`/`Invoke-WebRequest`). `cat dados.json | python -m
#: json.tool` cana para um interpretador, mas a origem é um arquivo local — não é o
#: idioma de baixar e executar, e travá-lo é falso positivo.
_CANO_INTERPRETE = re.compile(
    r"\b(?:curl|wget|iwr|invoke-webrequest|invoke-restmethod|irm)\b[^\n]{0,500}"
    r"\|\s*(?:sudo\s+)?"
    r"(?:bash|sh|zsh|ksh|python[0-9.]*|perl|ruby|node"
    r"|powershell(?:\.exe)?|pwsh|cmd(?:\.exe)?|iex|invoke-expression)\b",
    re.I,
)

#: Interpretadores com código embutido na linha. Cada um recebe uma família de flags
#: entre o nome e o `-c`/`-e` (inclusive a forma colada `-Bc`) e um conjunto próprio de
#: chamadas perigosas. `py` é *o* launcher do Windows e precisava estar aqui tanto quanto
#: `python`; `node`/`perl`/`ruby` executam deleção e processo como qualquer outro.
_PY_INLINE = re.compile(
    r"\b(?:python[0-9.]*|py)(?:\.exe)?(?:\s+-{1,2}[\w-]+(?:\s+\S+)?)*\s+-\w*c\b",
    re.I,
)
_NODE_INLINE = re.compile(
    r"\bnode(?:\.exe)?(?:\s+-{1,2}[\w-]+(?:\s+\S+)?)*\s+-\w*e\b", re.I
)
_PERL_INLINE = re.compile(r"\bperl(?:\s+-{1,2}[\w-]+(?:\s+\S+)?)*\s+-\w*e\b", re.I)
_RUBY_INLINE = re.compile(r"\bruby(?:\s+-{1,2}[\w-]+(?:\s+\S+)?)*\s+-\w*e\b", re.I)

#: Chamadas perigosas dentro de um interpretador embutido.
#:
#: SEM `re.I`, de propósito. Estes são identificadores, e identificador é sensível a
#: maiúsculas: `SHUTIL.RMTREE` não é chamada nenhuma, é texto. Casar sem distinguir caixa
#: produzia falso positivo em prosa e em literal de string — o caso real que expôs isso
#: foi a string `'EXEC(ruim)'` dentro de um comando de diagnóstico inofensivo, travado
#: por `\beval\(|\bexec\(`. Falso positivo frequente é o que leva o humano a aprovar no
#: automático, e aprovação automática anula a proteção inteira.
_PY_PERIGO = re.compile(
    r"shutil\.rmtree|shutil\.move|os\.remove|os\.unlink|os\.rmdir|subprocess"
    r"|requests\.(post|put|delete|patch)|urlopen"
    r"|os\.system|os\.popen|os\.exec\w*|os\.spawn\w*"
    r"|\beval\(|\bexec\(|Path\(.{0,200}\)\.unlink"
)
_NODE_PERIGO = re.compile(
    r"rmSync|unlinkSync|rmdirSync|child_process|execSync|spawnSync"
)
_PERL_PERIGO = re.compile(r"\bunlink\b|\bsystem\s*\(|\bexec\s*\(")
_RUBY_PERIGO = re.compile(
    r"FileUtils|File\.delete|File\.unlink|\bsystem\s*\(|\bexec\s*\(|%x"
)
#: Ordem de inspeção dos interpretadores embutidos: (reconhecedor, perigo, nome).
_INTERPRETES_INLINE = (
    (_PY_INLINE, _PY_PERIGO, "python -c"),
    (_NODE_INLINE, _NODE_PERIGO, "node -e"),
    (_PERL_INLINE, _PERL_PERIGO, "perl -e"),
    (_RUBY_INLINE, _RUBY_PERIGO, "ruby -e"),
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
        if padrao == "*token*":
            # `*token*` casava nome de arquivo de código comum (`token_store.py`,
            # `tokenizer.py`) e até o argumento `token` de `pytest -k token`. Estreita
            # para o que é de fato um arquivo de token: extensão `.token`, ou o nome
            # traz `token` JUNTO de `secret`/`credential`.
            if _nome_e_arquivo_de_token(nome):
                return True
            continue
        if fnmatch(nome, padrao) or fnmatch(inteiro, f"*{padrao}"):
            return True
    return False


def _nome_e_arquivo_de_token(nome: str) -> bool:
    baixo = nome.lower()
    if baixo.endswith(".token"):
        return True
    if "token" in baixo and ("secret" in baixo or "credential" in baixo):
        return True
    return False


def _sob_painel(alvo: str) -> bool:
    """Diz se o alvo está sob um diretório `.engine/` (o painel de controle).

    Olha os componentes do caminho, não o prefixo textual: `.engine/estado.json`,
    `C:/proj/.engine/config.json` e `sub/.engine/x` casam todos, enquanto um arquivo
    chamado `.engineering` não casa. A comparação IGNORA A CAIXA: no Windows o
    filesystem não distingue maiúsculas, então `.ENGINE/estado.json` atinge o mesmo
    arquivo real — e sem ignorar a caixa a família R9 inteira era contornável só
    trocando a caixa do nome. Continua sendo por componente EXATO (ignorando caixa),
    nunca por prefixo, para que `.engineering` siga de fora. Normaliza a barra invertida
    do Windows antes, porque o alvo de um redirecionamento de shell chega como texto cru.
    """
    if not alvo:
        return False
    return any(
        parte.lower() == _PAINEL for parte in Path(alvo.replace("\\", "/")).parts
    )


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
    if _e_execucao_persistente(caminho):
        # R10: caminho que instala execução de código para rodar depois, sozinho
        # (hook do git, config do editor, arquivo de inicialização de shell, perfil do
        # PowerShell, pasta Startup, crontab, chave autorizada). Trava dentro OU fora da
        # raiz — sem isso, `Write .git/hooks/pre-commit` instalava um `rm -rf` que rodava
        # a cada commit sem nunca aparecer no relatório.
        return Classificacao(
            TRAVADO, "R10", "escrita em caminho de execução persistente"
        )
    if _e_unc(alvo):
        # Caminho de rede (`//servidor/...`): nunca livre, e sem chamar `exists()` nele
        # — a consulta a um compartilhamento remoto custa segundos de I/O.
        return Classificacao(RASTREADO, "", "escrita em caminho de rede (UNC)")
    if caminho.exists():
        # Ordem invertida de propósito: a checagem de `tests/` ficava ACIMA desta e
        # liberava a sobrescrita de teste existente. Existir em disco decide primeiro.
        if _e_teste(caminho):
            return Classificacao(RASTREADO, "", "teste que já existe em disco")
        return Classificacao(RASTREADO, "", "arquivo já existe em disco")
    if _fora_da_raiz(caminho, raiz):
        # Arquivo NOVO fora da raiz do projeto: nunca livre. Escrever `../../.bashrc` ou
        # `C:/Windows/Temp/x.ps1` sai do território do trabalho e, no mínimo, tem de
        # aparecer no relatório.
        return Classificacao(RASTREADO, "", "escrita fora da raiz do projeto")
    if _e_teste(caminho):
        return Classificacao(LIVRE, "", "arquivo de teste novo")
    return Classificacao(LIVRE, "", "arquivo novo")


def _e_teste(caminho: Path) -> bool:
    return "tests" in caminho.parts or caminho.name.startswith("test_")


#: Diretórios cuja escrita instala execução persistente (rodam código depois, sozinhos).
_DIRS_EXEC_PERSISTENTE = {".claude", ".vscode", ".idea"}
#: Nomes de arquivo que instalam execução persistente (init de shell, agendador, chave).
_NOMES_EXEC_PERSISTENTE = {
    ".bashrc",
    ".bash_profile",
    ".bash_login",
    ".zshrc",
    ".zprofile",
    ".profile",
    "crontab",
    ".gitconfig",
    "authorized_keys",
}


def _e_execucao_persistente(caminho: Path) -> bool:
    """Diz se escrever neste caminho instala execução de código para rodar depois.

    Cobre `.git/hooks/`, `.claude/`, `.vscode/`, `.idea/`, a pasta `Startup` do Windows,
    os arquivos de inicialização de shell, o perfil do PowerShell (`*profile.ps1`),
    `crontab`, `.gitconfig` e `authorized_keys`. Comparação por componente, ignorando a
    caixa (o filesystem do Windows não distingue).
    """
    partes = [parte.lower() for parte in caminho.parts]
    nome = caminho.name.lower()
    if ".git" in partes:
        i = partes.index(".git")
        if i + 1 < len(partes) and partes[i + 1] == "hooks":
            return True
    if _DIRS_EXEC_PERSISTENTE.intersection(partes):
        return True
    if "startup" in partes:
        return True
    if nome in _NOMES_EXEC_PERSISTENTE:
        return True
    if nome.endswith("profile.ps1"):
        return True
    return False


def _e_unc(alvo: str) -> bool:
    """Caminho UNC (`//servidor/share` ou `\\\\servidor\\share`)."""
    return alvo.replace("\\", "/").startswith("//")


def _fora_da_raiz(caminho: Path, raiz: Path) -> bool:
    """Diz se `caminho` (já resolvido `..` e absolutos) cai FORA da raiz do projeto."""
    try:
        caminho.resolve().relative_to(raiz.resolve())
        return False
    except (ValueError, OSError):
        return True


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

    A contrabarra escapa o caractere seguinte fora de aspas e **dentro de aspas
    duplas** — não dentro de aspas simples, onde o shell a trata como literal. Sem
    isso havia um desvio de verdade, não uma imprecisão teórica: em
    `bash -c "python -c \\"import shutil; shutil.rmtree('/dados')\\""` o `\\"` era
    lido como fim da string, o `;` seguinte virava separador, e a expressão
    perigosa nunca cabia inteira em um segmento — R8 saía `rastreado` no lugar de
    `travado`. Medido antes de corrigir.
    """
    segmentos: list[str] = []
    atual: list[str] = []
    aspas: str | None = None
    i = 0
    n = len(comando)
    while i < n:
        ch = comando[i]
        if ch == "\\" and aspas != "'" and i + 1 < n:
            # Escape: o par inteiro é conteúdo, e o caractere escapado nunca
            # separa nem abre/fecha aspas. Em aspas simples não há escape.
            atual.append(ch)
            atual.append(comando[i + 1])
            i += 2
            continue
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

#: Teto de tamanho do comando. Acima disto, o comando NÃO é analisado padrão a padrão:
#: ele é anormal por definição (comando útil não tem dezenas de milhares de caracteres) e
#: varrer cada família sobre ele é justamente o vetor de ReDoS. Travar é o lado certo do
#: erro — o humano confirma um comando gigante em vez de a sessão congelar analisando-o.
_TETO_COMANDO = 20000


def _classificar_comando(comando: str, config: dict, profundidade: int = 0) -> Classificacao:
    if len(comando) > _TETO_COMANDO:
        return Classificacao(
            TRAVADO,
            "R12",
            f"comando grande demais para classificar com segurança "
            f"({len(comando)} caracteres, teto {_TETO_COMANDO})",
        )
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
    tokens = _tokens(segmento)

    for token in tokens:
        # R9 abrangente: QUALQUER token de qualquer comando que aponte para dentro de
        # `.engine/` desliga ou desarma o motor. `tee`, `cp`, `mv`, `sed -i`, `install`,
        # `Set-Content` — cobrir só o redirecionamento `>` deixava todos esses de fora.
        if _sob_painel(token):
            return Classificacao(
                TRAVADO, "R9", "escrita no painel de controle do motor"
            )

    for alvo_cru in _REDIRECT.findall(segmento):
        # O alvo pode vir entre aspas (`> ".env"`): tira as aspas antes de comparar
        # com os padrões de segredo, senão o fnmatch nunca casa.
        alvo = alvo_cru.strip("'\"")
        if _sob_painel(alvo):
            return Classificacao(
                TRAVADO, "R9", "escrita no painel de controle do motor"
            )
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    # A mesma credencial no mesmo arquivo travava por `Write` e passava por `Bash`.
    # R5 no comando só olhava o NOME do alvo, então `echo 'AKIA…' >> config.py` saía
    # `rastreado` — e a assimetria transformava o shell no caminho fácil para
    # contornar uma regra que existe justamente para não deixar segredo virar
    # commit. Os padrões exigem a forma que o emissor deu à chave (prefixo fixo e
    # comprimento mínimo), então não é adivinhação sobre texto qualquer.
    achado = _PADROES_CREDENCIAL.search(segmento)
    if achado:
        return Classificacao(
            TRAVADO, "R5", f"credencial no corpo do comando: {achado.group(0)[:12]}…"
        )

    e_git = bool(re.match(r"\s*git\b", segmento))
    if e_git:
        # O texto de `-m` é literal: apagá-lo evita que a mensagem do commit case uma
        # família por engano. Mas a limpeza precisa vir ANTES da checagem de substituição
        # de comando, senão `git commit -m "usa $(date)"` travava por um `$(...)`
        # inofensivo no corpo da mensagem. O que executa de verdade dentro do `-m` é
        # reclassificado à parte, logo abaixo.
        limpo = _MSG_GIT.sub(" ", segmento)
        perigo_msg = _substituicao_perigosa_na_mensagem(segmento, config, profundidade)
        if perigo_msg is not None:
            return perigo_msg
    else:
        limpo = segmento

    if _tem_execucao_escondida(limpo):
        # `$(...)`, crase e substituição de processo executam um comando escondido
        # dentro do argumento de outro. Fora de aspas simples — `awk '{print $(NF)}'`
        # tem `$(` LITERAL (aspas simples não expandem no shell) e não é substituição.
        return Classificacao(
            TRAVADO, "R8", "substituição de comando dentro do argumento"
        )

    primeiro = tokens[0].lower() if tokens else ""
    primeiro_e_busca = Path(primeiro).name in _FERRAMENTAS_BUSCA
    for regra, motivo, padrao in _familias(config):
        if regra == "R4" and primeiro_e_busca:
            # `grep 'DELETE FROM' log.txt`: o SQL é o alvo da busca, não uma execução.
            continue
        if re.search(padrao, limpo, re.I):
            return Classificacao(TRAVADO, regra, motivo)

    for token in tokens[1:]:
        # `cat .env` não é leitura inócua: sem isto, só a ferramenta `Read` travaria
        # segredo, e qualquer leitura pelo shell escaparia.
        if _e_segredo(token, config):
            return Classificacao(TRAVADO, "R5", f"argumento aponta para segredo: {token}")

    for reconhecedor, perigo, nome in _INTERPRETES_INLINE:
        if reconhecedor.search(segmento):
            if perigo.search(segmento):
                return Classificacao(TRAVADO, "R8", f"{nome} com chamada perigosa")
            return Classificacao(
                RASTREADO, "R8", f"{nome}: conteúdo não inspecionável a fundo"
            )

    if _EXEC_INDIRETA.search(segmento):
        return _classificar_execucao_indireta(segmento, config, profundidade)

    return Classificacao(RASTREADO, "", _MOTIVO_COMANDO)


def _tem_execucao_escondida(segmento: str) -> bool:
    """Diz se há substituição de comando ativa (`$(...)`, crase, `<(`/`>(`).

    Ignora o que está dentro de ASPAS SIMPLES: no shell, aspas simples não expandem, então
    o `$(` de `awk '{print $(NF)}'` é texto literal, não uma substituição. Dentro de aspas
    duplas, `$(...)` e crase EXPANDEM — continuam contando.
    """
    aspas: str | None = None
    i = 0
    n = len(segmento)
    while i < n:
        ch = segmento[i]
        prox = segmento[i + 1] if i + 1 < n else ""
        if aspas == "'":
            if ch == "'":
                aspas = None
            i += 1
            continue
        if aspas == '"':
            if ch == '"':
                aspas = None
            elif ch == "$" and prox == "(":
                return True
            elif ch == "`":
                return True
            i += 1
            continue
        if ch == "'":
            aspas = "'"
            i += 1
            continue
        if ch == '"':
            aspas = '"'
            i += 1
            continue
        if ch == "$" and prox == "(":
            return True
        if ch == "`":
            return True
        if ch in "<>" and prox == "(":
            return True
        i += 1
    return False


def _substituicao_perigosa_na_mensagem(
    segmento: str, config: dict, profundidade: int
) -> Classificacao | None:
    """Classifica a substituição de comando embutida no texto de `-m`/`--message`.

    `git commit -m "$(date)"` é inofensivo; `git commit -m "$(rm -rf /dados)"` executa
    uma deleção escondida na mensagem. A distinção é o CONTEÚDO da substituição: extrai o
    comando interno e reclassifica; se ele trava, a mensagem trava por R8, senão é
    ignorada e o commit segue.
    """
    for _flag, aspado in _MSG_GIT.findall(segmento):
        interior = aspado[1:-1] if len(aspado) >= 2 else aspado
        for interno in _substituicoes_de(interior):
            resultado = _classificar_comando(interno, config, profundidade + 1)
            if resultado.nivel == TRAVADO:
                return Classificacao(
                    TRAVADO, "R8", "substituição de comando dentro da mensagem do git"
                )
    return None


def _substituicoes_de(texto: str) -> list[str]:
    """Comandos internos de cada `$(...)` e crase no texto (sem aninhar)."""
    achados = [m.group(1) for m in re.finditer(r"\$\(([^()]{0,500})\)", texto)]
    achados += [m.group(1) for m in re.finditer(r"`([^`]{0,500})`", texto)]
    return achados


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
