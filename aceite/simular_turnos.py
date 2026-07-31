"""Verificação de aceite: o modo sobrevive a 20 turnos e a uma compactação.

A Fase 1 (`aceite/fase-1.md`, seção "O que NÃO foi verificado") deixou explícito que
não tinha rodado nenhuma sessão real — nem sintética — de 20 turnos com os hooks de
verdade. Este script fecha essa lacuna NA MECÂNICA: sobe um ciclo num diretório
temporário sintético e, para cada um dos 20 turnos, dispara os hooks REAIS como
SUBPROCESSO, na mesma ordem em que o Claude Code os chamaria dentro de um turno:

    engine_contexto.py (UserPromptSubmit) -> engine_risco.py (PreToolUse)
        -> engine_trilha.py (PostToolUse), só se a ação não foi bloqueada.

Depois dos 20 turnos, o roteiro dispara o quinto hook, `engine_gate.py` (Stop) — o
único que BLOQUEIA a saída do Claude e, até a revisão adversarial da Fase 2, o único
que este aceite nunca exercitava. A entrada na fase BUILD é feita pelo caminho REAL
(`ferramentas/cli.py fase BUILD` em subprocesso, seguido do `PostToolUse` sobre o
mesmo comando), e o Stop é disparado duas vezes: a primeira tem de cobrar evidência,
a segunda não.

No turno 10, entre um turno e o próximo, dispara `engine_salvar.py` (PreCompact) —
a mesma simulação da compactação de contexto. No meio da sequência (turnos 4 e 8),
a fase avança de verdade via `ferramentas.estado.transicionar` + `estado.gravar`,
para provar que a fase escolhida se MANTÉM nos turnos seguintes (inclusive depois da
compactação), não é reprocessada do zero a cada turno.

Adaptação da mesma natureza que `aceite/verificar_familias.py` fez pela família de
risco: aqui a variação está nos EVENTOS por turno, não nas famílias. Os 20 turnos
cobrem leitura (`Read`), escrita de arquivo novo (`Write`), escrita em arquivo que já
existe (`Edit`) e um comando travado (`git push origin main`, família R2) — o
suficiente para exercitar os três níveis de risco (`livre`, `rastreado`, `travado`)
dentro da mesma sequência.

O que este script NÃO prova (ver `aceite/fase-2.md`, seção "O que NÃO foi
verificado"): que uma sessão REAL do Claude Code de 20 turnos se comporta assim —
isso exige o plugin instalado e uma conversa de verdade, reservado para a Fase 3.
Aqui os "turnos" são chamadas de subprocesso em sequência, não uma conversa real;
o que se prova é que a MECÂNICA (disco + hooks) aguenta 20 idas e vindas e uma
consolidação sem perder fase, objetivo nem trilha.

Só biblioteca padrão. Usa `sys.executable`, nunca `py` (ver `aceite/fase-1.md`,
adaptação 4, sobre por que `sys.executable` é o único caminho garantido correto).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PLUGIN))
from ferramentas import config, estado, trilha  # noqa: E402

HOOK_CONTEXTO = RAIZ_PLUGIN / "hooks" / "engine_contexto.py"
HOOK_RISCO = RAIZ_PLUGIN / "hooks" / "engine_risco.py"
HOOK_TRILHA = RAIZ_PLUGIN / "hooks" / "engine_trilha.py"
HOOK_SALVAR = RAIZ_PLUGIN / "hooks" / "engine_salvar.py"
HOOK_GATE = RAIZ_PLUGIN / "hooks" / "engine_gate.py"

#: Fase esperada ao fim dos 20 turnos, dado o ROTEIRO e TRANSICOES_NO_MEIO abaixo.
#: Valor LITERAL de propósito: a verificação (a) comparava o cartão do turno 20 com
#: a fase lida do mesmo disco que o cartão leu — tautologia. Apagar as duas
#: transições do meio mantinha a verificação verde, que é exatamente o defeito que
#: ela deveria pegar. Se o ROTEIRO mudar, este valor muda junto, à mão.
FASE_ESPERADA_NO_FIM = "PLANO"

#: Fase em que o gate (`engine_gate.py`) é exercitado depois dos 20 turnos. Tem de
#: ser uma das três que exigem evidência (BUILD/TESTE/REVISAO) e alcançável a partir
#: de FASE_ESPERADA_NO_FIM pelo grafo de `ferramentas.estado.TRANSICOES`.
FASE_DO_GATE = "BUILD"

OBJETIVO_CICLO = "aceite F2-T8: simular 20 turnos e uma compactacao do ENGINE"

#: Piso do teto de linhas do cartão — replica `hooks/engine_contexto.py::MINIMO_CARTAO`
#: (não importa o módulo direto: hooks são scripts standalone que ajustam o próprio
#: `sys.path`, importá-los quebraria isolamento; o valor é uma constante estável).
MINIMO_CARTAO = 9
TETO_PADRAO = 40

#: Roteiro dos 20 turnos. Cada entrada é o TIPO de evento sintético daquele turno —
#: variado de propósito: leitura, escrita de arquivo novo, escrita em arquivo que já
#: existe, e um comando travado (turno 12). "escrita-existente" sempre mira o último
#: arquivo criado por "escrita-nova" — nunca há uma edição sem um arquivo prévio no
#: roteiro, porque isso é o que aconteceria numa sessão real (não se edita o que
#: nunca foi criado).
ROTEIRO: tuple[str, ...] = (
    "leitura",             # 1
    "escrita-nova",        # 2
    "escrita-existente",   # 3  (edita o arquivo do turno 2)
    "leitura",             # 4
    "escrita-nova",        # 5
    "escrita-existente",   # 6  (edita o arquivo do turno 5)
    "leitura",             # 7
    "escrita-nova",        # 8
    "escrita-existente",   # 9  (edita o arquivo do turno 8)
    "leitura",             # 10 (compactação acontece logo depois deste turno)
    "escrita-nova",        # 11
    "comando-travado",     # 12 (git push origin main -- BLOQUEADO, família R2)
    "leitura",             # 13
    "escrita-existente",   # 14 (edita o arquivo do turno 11)
    "escrita-nova",        # 15
    "leitura",             # 16
    "escrita-existente",   # 17 (edita o arquivo do turno 15)
    "leitura",             # 18
    "escrita-nova",        # 19
    "leitura",             # 20 (cartão deste turno é o verificado ao final)
)

#: Transições de fase no meio da sequência: turno após o qual a fase avança, e o
#: destino. Prova que a fase escolhida se MANTÉM nos turnos seguintes (inclusive
#: depois da compactação do turno 10), não regride nem é reprocessada do zero.
TRANSICOES_NO_MEIO: tuple[tuple[int, str], ...] = (
    (4, "ANALISE"),
    (8, "PLANO"),
)


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _rodar(hook: Path, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def _evento_do_turno(turno: int, raiz: Path, arquivo_leitura: Path, ultimo_novo: dict) -> tuple[str, str, dict]:
    """Devolve (tipo, ferramenta, tool_input) sintético e plausível para o turno.

    `ultimo_novo` é um dicionário mutável de estado do próprio script (não do
    ENGINE): guarda o caminho e o número do turno do último arquivo criado por
    "escrita-nova", para que "escrita-existente" tenha um alvo real em disco.
    """
    tipo = ROTEIRO[turno - 1]

    if tipo == "leitura":
        return tipo, "Read", {"file_path": str(arquivo_leitura)}

    if tipo == "comando-travado":
        return tipo, "Bash", {"command": "git push origin main"}

    if tipo == "escrita-nova":
        alvo = raiz / f"modulo_{turno:02d}.py"
        conteudo = f"# modulo sintetico do turno {turno}\nvalor = {turno}\n"
        return tipo, "Write", {"file_path": str(alvo), "content": conteudo}

    # "escrita-existente": edita o último arquivo criado por "escrita-nova".
    assert ultimo_novo["caminho"] is not None, (
        f"turno {turno} é escrita-existente mas nenhum arquivo foi criado antes "
        "-- erro no ROTEIRO, não no motor"
    )
    caminho_alvo = ultimo_novo["caminho"]
    criado_no_turno = ultimo_novo["turno"]
    old_string = f"valor = {criado_no_turno}"
    new_string = f"valor = {criado_no_turno}  # editado no turno {turno}"
    return tipo, "Edit", {
        "file_path": str(caminho_alvo),
        "old_string": old_string,
        "new_string": new_string,
    }


def _aplicar_efeito_no_disco(tipo: str, tool_input: dict, ultimo_novo: dict, turno: int) -> None:
    """Simula o efeito que a ferramenta real teria em disco, DEPOIS que o hook de
    risco liberou a ação. Os hooks só classificam e registram — quem escreve o
    arquivo é a ferramenta do Claude Code, que este script não tem; sem replicar o
    efeito, "escrita-existente" nunca acharia um arquivo em disco."""
    if tipo == "escrita-nova":
        caminho = Path(tool_input["file_path"])
        caminho.write_text(tool_input["content"], encoding="utf-8")
        ultimo_novo["caminho"] = caminho
        ultimo_novo["turno"] = turno
    elif tipo == "escrita-existente":
        caminho = Path(tool_input["file_path"])
        atual = caminho.read_text(encoding="utf-8")
        caminho.write_text(
            atual.replace(tool_input["old_string"], tool_input["new_string"]),
            encoding="utf-8",
        )


def _exercitar_o_gate(
    raiz: Path, linhas_de_log: list[str]
) -> tuple[subprocess.CompletedProcess, subprocess.CompletedProcess]:
    """Roda `engine_gate.py` (Stop) de verdade, pelo caminho REAL de entrada na fase.

    O gate é o hook mais perigoso do projeto — é o único que BLOQUEIA a saída do
    Claude — e até esta correção o roteiro de aceite não o disparava uma vez sequer.

    A entrada na fase é feita como acontece de verdade: `ferramentas/cli.py fase
    BUILD` num subprocesso, seguido do `PostToolUse` sobre o mesmo comando. Esse é
    justamente o caminho que cegava o gate (a chamada da CLI gravava na trilha uma
    linha já carimbada com a fase nova, e o gate a lia como "evidência de trabalho").
    Depois disso o Stop é disparado duas vezes: a primeira tem de COBRAR (saída 2),
    a segunda NÃO (o contador `cobrancas_por_fase` está persistido em disco).
    """
    caminho_cli = RAIZ_PLUGIN / "ferramentas" / "cli.py"
    resultado_cli = subprocess.run(
        [sys.executable, str(caminho_cli), "fase", FASE_DO_GATE],
        capture_output=True,
        text=True,
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )
    linhas_de_log.append(
        f"          -- transição pela CLI REAL: {FASE_ESPERADA_NO_FIM} -> {FASE_DO_GATE} "
        f"(cli.py exit={resultado_cli.returncode})"
    )

    comando = f'{sys.executable} "{caminho_cli}" fase {FASE_DO_GATE}'
    saida_trilha = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(raiz)},
        raiz,
    )
    linhas_de_log.append(
        f"          -- PostToolUse sobre o comando da própria CLI "
        f"(exit={saida_trilha.returncode}; a linha vai para a trilha marcada do_motor)"
    )

    payload_stop = {"cwd": str(raiz), "stop_hook_active": False}
    primeira = _rodar(HOOK_GATE, payload_stop, raiz)
    linhas_de_log.append(
        f"          -- Stop (engine_gate.py) 1ª parada em {FASE_DO_GATE}: "
        f"exit={primeira.returncode} (esperado 2 = COBROU)"
    )
    segunda = _rodar(HOOK_GATE, payload_stop, raiz)
    linhas_de_log.append(
        f"          -- Stop (engine_gate.py) 2ª parada em {FASE_DO_GATE}: "
        f"exit={segunda.returncode} (esperado 0 = não cobra de novo)"
    )
    return primeira, segunda


def _teto_efetivo(raiz: Path) -> int:
    cfg = config.carregar(raiz)
    bruto = cfg.get("teto_cartao_linhas", TETO_PADRAO)
    try:
        teto = int(bruto)
    except (TypeError, ValueError):
        teto = TETO_PADRAO
    return max(teto, MINIMO_CARTAO)


def main() -> int:
    raiz = Path(tempfile.mkdtemp(prefix="engine-aceite-turnos-"))
    estado.novo_ciclo(raiz, OBJETIVO_CICLO, _agora())

    # Arquivo comum pré-existente no projeto sintético, alvo das "leitura" do
    # roteiro -- equivalente a um README que já estava lá antes do ciclo começar.
    arquivo_leitura = raiz / "README_sintetico.md"
    arquivo_leitura.write_text("Projeto sintético do aceite F2-T8.\n", encoding="utf-8")

    ultimo_novo: dict = {"caminho": None, "turno": None}
    turnos_bloqueados = 0
    cartao_turno_20 = ""
    saida_risco_turno_12: subprocess.CompletedProcess | None = None
    linhas_de_log: list[str] = []

    for turno in range(1, 21):
        tipo, ferramenta, tool_input = _evento_do_turno(turno, raiz, arquivo_leitura, ultimo_novo)

        # 1) UserPromptSubmit -- o cartão de estado, injetado a cada turno.
        saida_contexto = _rodar(HOOK_CONTEXTO, {"cwd": str(raiz)}, raiz)
        if turno == 20:
            cartao_turno_20 = saida_contexto.stdout

        # 2) PreToolUse -- classificação de risco; decide se a ação segue.
        saida_risco = _rodar(
            HOOK_RISCO,
            {"tool_name": ferramenta, "tool_input": tool_input, "cwd": str(raiz)},
            raiz,
        )
        bloqueada = saida_risco.returncode == 2
        if turno == 12:
            saida_risco_turno_12 = saida_risco

        # 3) PostToolUse -- só dispara se a ferramenta de fato executou (não
        # bloqueada). Ação bloqueada nunca roda, e por isso nunca gera trilha --
        # é o mesmo contrato que valeria numa sessão real.
        saida_trilha = None
        if bloqueada:
            turnos_bloqueados += 1
        else:
            _aplicar_efeito_no_disco(tipo, tool_input, ultimo_novo, turno)
            saida_trilha = _rodar(
                HOOK_TRILHA,
                {"tool_name": ferramenta, "tool_input": tool_input, "cwd": str(raiz)},
                raiz,
            )

        resumo_trilha = "n/a (bloqueada)" if saida_trilha is None else str(saida_trilha.returncode)
        linhas_de_log.append(
            f"turno {turno:02d} [{tipo:<18}] contexto={saida_contexto.returncode} "
            f"risco={saida_risco.returncode}{' (TRAVADO)' if bloqueada else ''} "
            f"trilha={resumo_trilha}"
        )

        # Compactação simulada logo depois do turno 10.
        if turno == 10:
            saida_salvar = _rodar(HOOK_SALVAR, {"cwd": str(raiz), "hook_event_name": "PreCompact"}, raiz)
            linhas_de_log.append(
                f"          -- PreCompact (engine_salvar.py) exit={saida_salvar.returncode}"
            )

        # Avanço de fase no meio da sequência.
        for turno_gatilho, destino in TRANSICOES_NO_MEIO:
            if turno == turno_gatilho:
                dados = estado.carregar(raiz)
                fase_antes = dados["fase"]
                estado.transicionar(dados, destino)
                estado.gravar(raiz, dados)
                linhas_de_log.append(
                    f"          -- transição de fase: {fase_antes} -> {destino} "
                    f"(via estado.transicionar + estado.gravar)"
                )

    # ---- Estado ao fim dos 20 turnos, ANTES de exercitar o gate ----
    # Capturado aqui de propósito: a etapa do gate avança a fase, e as verificações
    # (a)-(d) falam do que sobreviveu aos 20 turnos, não do que veio depois.
    estado_final = estado.carregar(raiz)
    fase_final = estado_final.get("fase") if estado_final else None
    objetivo_final = estado_final.get("ciclo", {}).get("objetivo") if estado_final else None
    # A trilha também é lida ANTES da etapa do gate: aquela etapa acrescenta a linha
    # da própria CLI, que não é um dos 20 turnos e não entra na contagem de (c).
    trilha_dados = trilha.ler(raiz)

    # ---- Etapa do gate: o hook mais perigoso do projeto, exercitado de verdade ----
    saida_gate_primeira, saida_gate_segunda = _exercitar_o_gate(raiz, linhas_de_log)

    for linha in linhas_de_log:
        print(linha)

    # ---- Verificações finais ----
    print()
    print("== Verificações finais ==")
    falhas: list[str] = []

    # (a) o cartão do turno 20 traz a fase ESPERADA (valor literal) e o objetivo.
    # Comparar o cartão com `estado.carregar()` seria circular: os dois leem o mesmo
    # disco, então apagar as transições do meio mantinha esta verificação verde.
    ok_a = bool(
        estado_final
        and fase_final == FASE_ESPERADA_NO_FIM
        and objetivo_final == OBJETIVO_CICLO
        and f"Fase: {FASE_ESPERADA_NO_FIM}" in cartao_turno_20
        and OBJETIVO_CICLO in cartao_turno_20
    )
    print(
        f"(a) fase ao fim dos 20 turnos é {FASE_ESPERADA_NO_FIM!r} (lida: {fase_final!r}) "
        f"e o cartão do turno 20 traz essa fase e o objetivo: "
        f"{'OK' if ok_a else 'FALHOU'}"
    )
    if not ok_a:
        falhas.append("(a) fase/objetivo no cartão do turno 20")

    # (b) o cartão respeita o teto de linhas.
    teto = _teto_efetivo(raiz)
    linhas_cartao = cartao_turno_20.splitlines()
    ok_b = len(linhas_cartao) <= teto
    print(
        f"(b) cartão do turno 20 respeita o teto de linhas ({len(linhas_cartao)} <= {teto}): "
        f"{'OK' if ok_b else 'FALHOU'}"
    )
    if not ok_b:
        falhas.append("(b) teto de linhas do cartão")

    # (c) a trilha tem o número esperado de linhas: um registro por turno NÃO
    # bloqueado (ações bloqueadas nunca executam, nunca geram PostToolUse).
    linhas_trilha = trilha_dados.get("linhas", [])
    esperado_trilha = 20 - turnos_bloqueados
    ok_c = len(linhas_trilha) == esperado_trilha
    print(
        f"(c) trilha tem o número esperado de linhas ({len(linhas_trilha)} == {esperado_trilha}): "
        f"{'OK' if ok_c else 'FALHOU'}"
    )
    if not ok_c:
        falhas.append("(c) contagem de linhas da trilha")
        if trilha_dados.get("_avisos"):
            print(f"    avisos da trilha: {trilha_dados['_avisos']}")

    # (d) ultima_consolidacao foi gravada pelo PreCompact (turno 10).
    consolidacao = estado_final.get("ultima_consolidacao") if estado_final else None
    consolidacao_valida = False
    if isinstance(consolidacao, str):
        try:
            datetime.fromisoformat(consolidacao)
            consolidacao_valida = True
        except ValueError:
            consolidacao_valida = False
    ok_d = consolidacao_valida
    print(
        f"(d) 'ultima_consolidacao' gravada pelo PreCompact ({consolidacao!r}): "
        f"{'OK' if ok_d else 'FALHOU'}"
    )
    if not ok_d:
        falhas.append("(d) ultima_consolidacao ausente ou inválida")

    # (e) a ação travada do turno 12 foi mesmo bloqueada (exit 2).
    ok_e = saida_risco_turno_12 is not None and saida_risco_turno_12.returncode == 2
    print(
        f"(e) ação travada do turno 12 (git push origin main) saiu com código 2: "
        f"{'OK' if ok_e else 'FALHOU'}"
    )
    if not ok_e:
        falhas.append("(e) comando travado não bloqueou")
        if saida_risco_turno_12 is not None and saida_risco_turno_12.stderr:
            print(f"    stderr: {saida_risco_turno_12.stderr.strip()}")

    # (f) o gate COBRA na primeira parada da fase sem evidência (saída 2).
    ok_f = saida_gate_primeira.returncode == 2 and FASE_DO_GATE in saida_gate_primeira.stderr
    print(
        f"(f) gate cobra evidência na 1ª parada em {FASE_DO_GATE} "
        f"(saída {saida_gate_primeira.returncode}, esperado 2): {'OK' if ok_f else 'FALHOU'}"
    )
    if not ok_f:
        falhas.append("(f) gate não cobrou na primeira parada")
        if saida_gate_primeira.stderr:
            print(f"    stderr: {saida_gate_primeira.stderr.strip()}")

    # (g) o gate NÃO cobra de novo na mesma fase (contador persistido em disco).
    ok_g = saida_gate_segunda.returncode == 0
    print(
        f"(g) gate não cobra na 2ª parada na mesma fase "
        f"(saída {saida_gate_segunda.returncode}, esperado 0): {'OK' if ok_g else 'FALHOU'}"
    )
    if not ok_g:
        falhas.append("(g) gate cobrou duas vezes na mesma fase")
        if saida_gate_segunda.stderr:
            print(f"    stderr: {saida_gate_segunda.stderr.strip()}")

    print()
    print("FALHAS:", falhas or "nenhuma")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
