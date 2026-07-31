#!/usr/bin/env bash
# engine.sh — lançador multiplataforma dos hooks do ENGINE.
#
# Contrato:
#   engine.sh [--travar-sem-python] <caminho-do-script-py> [args...]
#
# Por que este script existe: `hooks/hooks.json` usava a forma exec do Claude
# Code (`"command": "py"` + `"args"`), que resolve `py` literalmente no PATH,
# sem shell e sem fallback. `py` é o Python Launcher — só existe no Windows.
# Em macOS/Linux o hook falhava ao iniciar. A forma shell (sem "args") entrega
# esta string a um shell de verdade (Git Bash no Windows, sh -c em
# macOS/Linux), o que permite decidir o interpretador Python EM RUNTIME em vez
# de fixá-lo no JSON.
#
# stdin/stdout/stderr e o código de saída do script Python precisam chegar ao
# Claude Code intactos — é o código de saída que decide se a ação do usuário é
# bloqueada. E aí está a regra que governa este arquivo inteiro:
#
#   SÓ `exit 2` BLOQUEIA. Qualquer outro código é erro não-bloqueante, e a
#   ação do agente acontece assim mesmo.
#
# A consequência é contraintuitiva e vale escrever: para o hook de risco, um
# erro qualquer não é "proteção ausente", é "proteção que deixa passar". Por
# isso, no modo --travar-sem-python, este script NÃO usa `exec` — ele executa
# o Python como filho e traduz qualquer código inesperado para 2. Nos outros
# quatro hooks, que nunca podem atrapalhar o turno do usuário, `exec` continua
# sendo o certo.
set -u

travar_sem_python=0
if [ "${1:-}" = "--travar-sem-python" ]; then
    travar_sem_python=1
    shift
fi

alvo="${1:-}"
if [ -n "$alvo" ]; then
    shift
fi

# Um caminho começando com "-" seria lido pelo interpretador como opção, não
# como arquivo. O caminho vem de ${CLAUDE_PLUGIN_ROOT} e é absoluto na prática,
# mas prefixar "./" custa nada e elimina a classe inteira.
case "$alvo" in
    -*) alvo="./$alvo" ;;
esac

# Sai pelo caminho correto de acordo com o modo: no hook de risco, tudo que dá
# errado tem que bloquear; nos outros, tudo que dá errado tem que ser silêncio.
sair_por_falha() {
    if [ "$travar_sem_python" -eq 1 ]; then
        exit 2
    fi
    exit 0
}

if [ -z "$alvo" ] || [ ! -f "$alvo" ]; then
    if [ "$travar_sem_python" -eq 1 ]; then
        echo "ENGINE: script do hook de risco nao encontrado: '${alvo}'." >&2
        echo "ENGINE: por isso o classificador NAO esta protegendo nada; travando por seguranca." >&2
    fi
    sair_por_falha
fi

# Detecta o interpretador tentando, nesta ordem, py (Windows Launcher),
# python3 (padrão POSIX) e python (fallback de ambientes mais antigos ou venvs
# que só expõem esse nome). Usamos só `command -v` para descobrir o caminho —
# nunca executamos o candidato para testá-lo. O PreToolUse roda a cada chamada
# de ferramenta; iniciar um interpretador Python só para sondar se ele
# "funciona de verdade" pagaria latência extra em toda e qualquer ação do
# usuário, e `command -v` já é suficiente para achar um executável no PATH.
interpretador=""
for candidato in py python3 python; do
    caminho="$(command -v "$candidato" 2>/dev/null || true)"
    if [ -z "$caminho" ]; then
        continue
    fi
    # Descarta qualquer caminho que contenha "WindowsApps": é o stub que o
    # Windows registra em AppData\Local\Microsoft\WindowsApps quando nenhum
    # Python de verdade está instalado. Esse stub aparece no PATH e responde a
    # `command -v`, mas ao ser executado ele abre a Microsoft Store em vez de
    # rodar qualquer script — um "Python" que não roda Python é pior que
    # nenhum, porque a falha é silenciosa até alguém tentar usá-lo de fato.
    #
    # O casamento IGNORA A CAIXA de propósito: caminho no Windows não
    # distingue maiúsculas, e o PATH pode chegar aqui normalizado por outra
    # ferramenta. Um `case` sensível a caixa deixava `windowsapps` minúsculo
    # passar, o stub rodava, devolvia um código arbitrário — e, não sendo 2,
    # LIBERAVA a ação.
    #
    # A classe de caracteres é feia mas é a forma certa: é glob POSIX puro,
    # resolvido pelo próprio shell. As alternativas custam caro aqui —
    # ${var,,} exige bash 4+ (o /bin/bash do macOS ainda é 3.2) e `tr` é
    # binário externo. Depender de binário externo reintroduziria exatamente
    # esta falha: com PATH restrito o `tr` não é encontrado, a substituição
    # devolve vazio em silêncio, e o filtro para de filtrar sem avisar. Este
    # script não pode depender de nada além do shell.
    case "$caminho" in
        *[Ww][Ii][Nn][Dd][Oo][Ww][Ss][Aa][Pp][Pp][Ss]*)
            continue
            ;;
    esac
    interpretador="$caminho"
    break
done

if [ -z "$interpretador" ]; then
    # Nenhum interpretador Python utilizável foi encontrado.
    if [ "$travar_sem_python" -eq 1 ]; then
        echo "ENGINE: nenhum interpretador Python encontrado no PATH (tentei py, python3, python)." >&2
        echo "ENGINE: por isso o classificador de risco NAO esta protegendo nada neste turno." >&2
        echo "ENGINE: instale Python 3.11+ (e garanta que 'python3' ou 'python' fiquem no PATH)," >&2
        echo "ENGINE: ou desinstale o plugin ENGINE se nao pretende usa-lo." >&2
    fi
    sair_por_falha
fi

if [ "$travar_sem_python" -eq 1 ]; then
    # Hook de risco: sem `exec`, para poder inspecionar o código de saída. O
    # script Python só devolve 0 (liberar) ou 2 (travar); qualquer outra coisa
    # — erro de import, sintaxe, interpretador quebrado, morte por sinal —
    # significa que a classificação NÃO aconteceu. Deixar esse código passar
    # seria liberar a ação, então ele vira 2.
    "$interpretador" "$alvo" "$@"
    codigo=$?
    case "$codigo" in
        0|2)
            exit "$codigo"
            ;;
        *)
            echo "ENGINE: o classificador de risco terminou com codigo inesperado ($codigo)." >&2
            echo "ENGINE: a acao NAO foi classificada; travando por seguranca." >&2
            exit 2
            ;;
    esac
fi

# Os outros quatro hooks (UserPromptSubmit, PostToolUse, PreCompact, Stop) não
# podem atrapalhar o turno do usuário. Aqui `exec` é o certo: troca o processo
# do shell pelo do Python, repassando stdin/stdout/stderr e o código de saída
# sem intermediário.
exec "$interpretador" "$alvo" "$@"
