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
# Claude Code intactos — é o código de saída que decide se a ação do usuário
# é bloqueada (só `exit 2` bloqueia; qualquer outro código é erro
# não-bloqueante). Por isso o interpretador é sempre chamado com `exec`: troca
# o processo do shell pelo do Python, em vez de rodar como filho — sem isso,
# o código de saída que voltaria ao Claude Code seria o do shell, não o do
# Python.
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

# Detecta o interpretador tentando, nesta ordem, py (Windows Launcher),
# python3 (padrão POSIX) e python (fallback de ambientes mais antigos ou
# venvs que só expõem esse nome). Usamos só `command -v` para descobrir o
# caminho — nunca executamos o candidato para testá-lo. O PreToolUse roda a
# cada chamada de ferramenta; iniciar um interpretador Python só para sondar
# se ele "funciona de verdade" pagaria latência extra em toda e qualquer ação
# do usuário, e `command -v` já é suficiente para achar um executável válido
# no PATH.
interpretador=""
for candidato in py python3 python; do
    caminho="$(command -v "$candidato" 2>/dev/null || true)"
    if [ -z "$caminho" ]; then
        continue
    fi
    # Descarta qualquer caminho que contenha "WindowsApps": é o stub que o
    # Windows registra em AppData\Local\Microsoft\WindowsApps quando nenhum
    # Python de verdade está instalado. Esse stub aparece no PATH e responde
    # a `command -v`, mas ao ser executado ele abre a Microsoft Store em vez
    # de rodar qualquer script — um "Python" que não roda Python é pior que
    # nenhum, porque a falha é silenciosa até alguém tentar usá-lo de fato.
    case "$caminho" in
        *WindowsApps*)
            continue
            ;;
    esac
    interpretador="$caminho"
    break
done

if [ -n "$interpretador" ]; then
    exec "$interpretador" "$alvo" "$@"
fi

# Nenhum interpretador Python utilizável foi encontrado.
if [ "$travar_sem_python" -eq 1 ]; then
    # Este é o hook PreToolUse (classificador de risco). Um gate de segurança
    # que não consegue rodar tem que travar, nunca liberar — por isso este é
    # o único caminho deste script que sai com o único código que bloqueia
    # (2), com uma mensagem explicando o motivo real.
    echo "ENGINE: nenhum interpretador Python encontrado no PATH (tentei py, python3, python)." >&2
    echo "ENGINE: por isso o classificador de risco NAO esta protegendo nada neste turno." >&2
    echo "ENGINE: instale Python 3.11+ (e garanta que 'python3' ou 'python' fiquem no PATH)," >&2
    echo "ENGINE: ou desinstale o plugin ENGINE se nao pretende usa-lo." >&2
    exit 2
fi

# Os outros quatro hooks (UserPromptSubmit, PostToolUse, PreCompact, Stop) não
# podem atrapalhar o turno do usuário: sem Python, eles simplesmente não têm
# opinião sobre nada, em silêncio.
exit 0
