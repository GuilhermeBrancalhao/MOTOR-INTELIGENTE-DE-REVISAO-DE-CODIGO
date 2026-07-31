"""Verificação de aceite: as sete famílias travadas travam pelo hook de verdade.

Diferente de um teste de unidade que chama `risco.classificar` direto, este script
dispara `hooks/engine_risco.py` como SUBPROCESSO — o mesmo processo que o Claude Code
invoca via `hooks/hooks.json` — e confirma que a decisão chega pelo código de saída,
não por uma função Python importada.

Adaptação em relação ao brief original (`.superpowers/sdd/briefs/tarefa-10-brief.md`):
a política do classificador mudou depois que o brief foi escrito. Antes, comando de
shell podia sair `livre` por prova positiva (lista de comandos permitidos); agora
`risco.py` proíbe explicitamente esse resultado para qualquer ferramenta de comando —
"comando de shell nunca é livre" (ver o docstring de `ferramentas/risco.py`). Ou o
comando casa uma das famílias R1-R8 e trava, ou sai RASTREADO (executa e é
registrado no relatório da fase). Não existe mais uma lista de comandos "seguros"
para testar como contraprova de shell.

Por isso a contraprova deste script não é mais um comando de shell permitido: é uma
LEITURA DE ARQUIVO comum (ferramenta `Read`, arquivo comum, sem estar sob nenhum
padrão de segredo). Essa é a única superfície que a política nova ainda deixa `livre`
por natureza (`ferramentas/risco.py::_classificar_leitura`). Sem essa contraprova, um
hook que bloqueasse literalmente tudo (por exemplo, sempre devolver código 2) passaria
neste script sem ser pego — as sete famílias travariam "por acidente".
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ferramentas import estado  # noqa: E402

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "engine_risco.py"

#: As sete famílias travadas. R5 (segredo) não é uma regra de comando em
#: `risco.FAMILIAS` — é decidida pelo lado de arquivo (`_classificar_escrita`), por
#: isso entra como ferramenta `Write` sobre um caminho que casa `padroes_segredo`,
#: não como comando `Bash`. As outras seis são comandos de shell que casam uma das
#: famílias R1-R8 descritas em `ferramentas/risco.py`.
CASOS_TRAVADOS = [
    ("R1", "rede: POST para fora", "Bash", {"command": "curl -X POST https://exemplo/x"}),
    ("R2", "git que sai da máquina", "Bash", {"command": "git push origin main"}),
    ("R3", "deleção", "Bash", {"command": "rm -rf build"}),
    ("R4", "alteração destrutiva de banco", "Bash", {"command": 'psql -c "DROP TABLE x"'}),
    ("R6", "deploy/infraestrutura", "Bash", {"command": "terraform apply"}),
    ("R7", "instalação global", "Bash", {"command": "npm install -g pnpm"}),
]


def _rodar_hook(ferramenta: str, entrada: dict, cwd: Path) -> subprocess.CompletedProcess:
    evento = {"tool_name": ferramenta, "tool_input": entrada, "cwd": str(cwd)}
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(evento),
        capture_output=True,
        text=True,
    )


def main() -> int:
    raiz = Path(tempfile.mkdtemp(prefix="engine-aceite-"))
    estado.novo_ciclo(raiz, "aceite da fase 1", "2026-07-30T00:00:00")

    casos_travados = list(CASOS_TRAVADOS)
    casos_travados.append(
        ("R5", "segredo (.env)", "Write", {"file_path": str(raiz / ".env")})
    )
    casos_travados.append(
        ("R9", "escrita no painel de controle do motor (.engine/)", "Write", {"file_path": str(raiz / ".engine" / "estado.json")})
    )

    falhas: list[str] = []

    for regra, descricao, ferramenta, entrada in casos_travados:
        saida = _rodar_hook(ferramenta, entrada, raiz)
        travou = saida.returncode == 2
        print(f"{regra} ({descricao}): {'TRAVOU' if travou else 'PASSOU'}  <- {entrada}")
        if not travou:
            falhas.append(regra)
            if saida.stderr:
                print(f"  stderr: {saida.stderr.strip()}")

    # Contraprova: leitura de arquivo comum tem que sair LIVRE (código 0). Sem este
    # caso, um hook que bloqueasse tudo incondicionalmente passaria na verificação
    # acima inteira.
    arquivo_comum = raiz / "leitura_comum.txt"
    arquivo_comum.write_text("nada de especial aqui\n", encoding="utf-8")
    saida_contraprova = _rodar_hook("Read", {"file_path": str(arquivo_comum)}, raiz)
    passou_contraprova = saida_contraprova.returncode == 0
    print(
        "CONTRAPROVA (leitura de arquivo comum): "
        f"{'PASSOU' if passou_contraprova else 'TRAVOU (ERRADO)'}  "
        f"<- Read {arquivo_comum}"
    )
    if not passou_contraprova:
        falhas.append("CONTRAPROVA")
        if saida_contraprova.stderr:
            print(f"  stderr: {saida_contraprova.stderr.strip()}")

    print("FALHAS:", falhas or "nenhuma")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
