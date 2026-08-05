"""`programa verificar <CICLO>`: o veredito do ciclo deixa de ser digitado.

O que faltava, medido antes
---------------------------
O P2C1 entregou o executor (roda comando, lê código de saída, devolve veredito com
evidência) e o P2C2 fez todo plano-mestre declarar `comando_de_aceite`. Nada ligava os
dois: o único jeito de fechar um ciclo continuava sendo alguém digitar `programa aceite
C1 ok`, e o motor acreditava. Um plano com o comando declarado no arquivo e um veredito
digitado por cima é pior do que não ter comando nenhum — dá aparência de verificado ao
que ninguém rodou.

O que este arquivo cobra
------------------------
1. **o ciclo fecha sozinho pelo código de saída** — 0 vira CONCLUIDO, 1 vira REPROVADO,
   e em nenhum dos dois alguém digita veredito;
2. **REPROVADO bloqueia dependente**, que é o coração de A2 chegando por evidência;
3. **a evidência aparece**: comando, código de saída e saída impressos, e comando +
   código de saída na trilha;
4. **a ordem executar-fora / registrar-dentro**, provada pelo efeito: com o cadeado
   tomado o comando ROda (marcador em disco) e o veredito NÃO é gravado (bytes iguais);
5. **o critério que muda no meio não é registrado** — falha fechada na janela que a
   ordem acima abre;
6. **o veredito digitado exige justificativa**, e ela vai para a trilha;
7. **ciclo sem comando é recusado pelo `verificar`** — o motor não inventa comando.

Cada docstring nomeia a mutação que derruba o teste.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import estado, programa, trilha  # noqa: E402

AGORA = "2026-08-05T10:00:00"

#: Um script que sai 0 e imprime um marcador reconhecível na saída padrão. Marcador
#: com pinta de nada: se ele aparecer no relatório, veio da execução de verdade.
PASSA = "print('EVIDENCIA-VERDE-8811')\nraise SystemExit(0)\n"

#: O par vermelho. Imprime nos DOIS canos, porque o executor funde `stderr` em `stdout`
#: e a evidência de uma suíte quebrada costuma sair pelos dois.
FALHA = (
    "import sys\n"
    "print('EVIDENCIA-VERMELHA-4277')\n"
    "print('detalhe no stderr', file=sys.stderr)\n"
    "raise SystemExit(1)\n"
)

#: Um script que sai 0 **e** reescreve o `comando_de_aceite` do C1 no `programa.json`.
#: Simula, de forma determinística, a corrida real: outra sessão replanejando enquanto o
#: comando roda fora do cadeado.
REPLANEJA_NO_MEIO = (
    "import json\n"
    "from pathlib import Path\n"
    "alvo = Path('.engine/programa.json')\n"
    "dados = json.loads(alvo.read_text(encoding='utf-8'))\n"
    "for c in dados['ciclos']:\n"
    "    if c['id'] == 'C1':\n"
    "        c['comando_de_aceite'] = 'python outro_criterio.py'\n"
    "alvo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')\n"
    "raise SystemExit(0)\n"
)

#: Sai 0 e deixa um arquivo para trás. É o que permite provar EXECUÇÃO por efeito
#: colateral, sem depender do que foi impresso.
MARCA = "from pathlib import Path\nPath('rodou.txt').write_text('sim')\nraise SystemExit(0)\n"


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _impressao_digital(raiz: Path) -> str:
    """SHA-256 dos BYTES do `programa.json` — reordenação de chave também é escrita."""
    return hashlib.sha256(programa.caminho(raiz).read_bytes()).hexdigest()


def _script(raiz: Path, nome: str, corpo: str) -> str:
    """Escreve um script no projeto e devolve a linha de comando que o roda.

    Script em arquivo, e não `python -c "..."`: o comando atravessa o shell (o executor
    usa `shell=True` de propósito), e escapar aspas dentro de aspas no Windows é a
    fonte de flakiness que não tem nada a ver com o que estes testes medem.
    """
    (raiz / nome).write_text(corpo, encoding="utf-8")
    return f"python {nome}"


def _programa_pronto(raiz: Path, comandos: dict[str, str]) -> dict:
    """Um programa aprovado, em EXECUCAO, com um ciclo por item de `comandos`.

    `C2` depende de `C1` quando os dois existem — é o par que prova o bloqueio do
    dependente. Montado pela máquina de estado e gravado direto, como os demais testes
    de programa fazem: o que está sob teste aqui são os VERBOS, não o caminho do plano.
    """
    ciclos = [
        {
            "id": cid,
            "objetivo": f"construir {cid}",
            "depende_de": ["C1"] if cid == "C2" else [],
            "aceite": f"o critério de {cid} é satisfeito",
            "comando_de_aceite": comando,
        }
        for cid, comando in comandos.items()
    ]
    dados = programa.novo(raiz, "sistema com veredito automático", AGORA)
    dados = programa.propor_plano(dados, ciclos, "o sistema sobe e responde")
    dados = programa.aprovar(dados, AGORA)
    programa.gravar(raiz, dados)
    return dados


def _status(raiz: Path, cid: str) -> str:
    dados = programa.carregar(raiz)
    return next(c["status"] for c in dados["ciclos"] if c["id"] == cid)


def _linhas_do_executor(raiz: Path) -> list[dict]:
    return [
        linha
        for linha in trilha.ler(raiz)["linhas"]
        if linha.get("ferramenta") == "executor"
    ]


# ---------------------------------------------------------------------------
# 1. o veredito sai do código de saída, e de mais nada
# ---------------------------------------------------------------------------


def test_comando_que_sai_zero_fecha_o_ciclo_sem_ninguem_digitar_veredito(tmp_path):
    """Mutação que derruba: `passou=True` fixo, ou o verbo só imprimir sem registrar.

    É o teste central do ciclo, e o critério de aceite dele rodado literalmente. Ninguém
    passa `ok` em lugar nenhum: o único argumento do verbo é o id do ciclo, e o que
    decide é o `raise SystemExit(0)` do script.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert _status(tmp_path, "C1") == "CONCLUIDO"
    assert "Traceback" not in saida.stdout + saida.stderr


def test_comando_que_sai_um_reprova_o_ciclo_sem_ninguem_digitar_veredito(tmp_path):
    """Mutação que derruba: tratar qualquer execução bem-sucedida como aprovação.

    O par obrigatório do teste acima. Um verbo que aprova sempre passa naquele e é
    inútil: o que se está construindo é a capacidade de o motor **reprovar sozinho**.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "falha.py", FALHA)})

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert _status(tmp_path, "C1") == "REPROVADO"
    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "Traceback" not in saida.stdout + saida.stderr


def test_o_codigo_de_saida_do_verbo_espelha_o_veredito(tmp_path):
    """Mutação que derruba: sair 0 sempre que a verificação ocorreu.

    Decisão explícita, e o motivo é o mesmo que a recusa do plano já registra: uma
    verificação que reprova e sai 0 é indistinguível de sucesso para quem automatiza, e
    o passo seguinte do laço seria ligar o próximo ciclo por cima de um que falhou. Num
    verbo cujo assunto é "o código de saída decide", o próprio código de saída não pode
    mentir.
    """
    verde = tmp_path / "verde"
    vermelho = tmp_path / "vermelho"
    for pasta in (verde, vermelho):
        pasta.mkdir()
    _programa_pronto(verde, {"C1": _script(verde, "passa.py", PASSA)})
    _programa_pronto(vermelho, {"C1": _script(vermelho, "falha.py", FALHA)})

    assert _cli(verde, "programa", "verificar", "C1").returncode == 0
    assert _cli(vermelho, "programa", "verificar", "C1").returncode == 1


def test_ciclo_reprovado_bloqueia_o_dependente(tmp_path):
    """Mutação que derruba: registrar CONCLUIDO mesmo com código diferente de zero.

    A2 chegando por evidência: o REPROVADO que ninguém digitou tem de bloquear o
    dependente exatamente como o digitado bloqueava. Sem isso, o programa seguiria para
    C2 apoiado num C1 que falhou.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "falha.py", FALHA),
            "C2": _script(tmp_path, "passa.py", PASSA),
        },
    )

    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1

    proximo = _cli(tmp_path, "programa", "proximo")
    assert proximo.returncode == 1, proximo.stdout
    assert "REPROVADO" in proximo.stdout
    assert _status(tmp_path, "C2") == "PENDENTE"


def test_reabrir_e_verificar_de_novo_fecha_o_ciclo_consertado(tmp_path):
    """Mutação que derruba: gravar o veredito uma vez só (guardar "já verificado").

    O caminho de recuperação inteiro, ponta a ponta: reprova, conserta o comando,
    reabre, verifica de novo e fecha — sempre pelo código de saída. Um verbo que
    recusasse a segunda verificação deixaria o programa preso no primeiro vermelho.
    """
    comando = _script(tmp_path, "aceite.py", FALHA)
    _programa_pronto(tmp_path, {"C1": comando, "C2": comando})
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1

    (tmp_path / "aceite.py").write_text(PASSA, encoding="utf-8")  # o conserto
    assert _cli(tmp_path, "programa", "reabrir", "C1").returncode == 0
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 0

    assert _status(tmp_path, "C1") == "CONCLUIDO"
    assert programa.proximo_elegivel(programa.carregar(tmp_path))["id"] == "C2"


# ---------------------------------------------------------------------------
# 2. a evidência: impressa e na trilha
# ---------------------------------------------------------------------------


def test_a_evidencia_impressa_traz_comando_codigo_e_saida(tmp_path):
    """Mutação que derruba: imprimir só o veredito ("C1 CONCLUIDO").

    Veredito sem evidência é a opinião de que estamos saindo, com outro remetente. Quem
    lê o relatório precisa poder discordar do motor — e para isso precisa ver o que
    rodou, o que saiu e com que código.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "falha.py", FALHA)})

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert "python falha.py" in saida.stdout
    assert "Código de saída:** 1" in saida.stdout
    assert "EVIDENCIA-VERMELHA-4277" in saida.stdout, "a saída do comando não apareceu"
    assert "detalhe no stderr" in saida.stdout, "o stderr do comando se perdeu"


def test_a_trilha_registra_comando_e_codigo_de_saida_de_cada_verificacao(tmp_path):
    """Mutação que derruba: chamar o executor com `registrar_na_trilha=False`.

    A trilha é o que sobrevive à compactação e à sessão nova. Sem comando e código de
    saída nela, a auditoria de amanhã encontra "C1 CONCLUIDO" e nenhuma forma de saber
    o que provou isso — que é o estado de antes deste programa, preservado em JSON.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "falha.py", FALHA),
            "C2": _script(tmp_path, "passa.py", PASSA),
        },
    )

    _cli(tmp_path, "programa", "verificar", "C1")
    _cli(tmp_path, "programa", "reabrir", "C1")
    (tmp_path / "falha.py").write_text(PASSA, encoding="utf-8")
    _cli(tmp_path, "programa", "verificar", "C1")
    _cli(tmp_path, "programa", "verificar", "C2")

    linhas = _linhas_do_executor(tmp_path)
    assert [(l["alvo"], l["codigo_saida"], l["ciclo"]) for l in linhas] == [
        ("python falha.py", 1, "C1"),
        ("python falha.py", 0, "C1"),
        ("python passa.py", 0, "C2"),
    ]
    assert all(l["do_motor"] is True for l in linhas), (
        "a linha do executor deixaria de ser marcada como do motor e passaria a contar "
        "como evidência do trabalho do ciclo"
    )


def test_a_trilha_registra_tambem_o_passo_do_programa(tmp_path):
    """Mutação que derruba: apagar o `_prog_trilha` do verbo, confiando só no executor.

    As duas linhas dizem coisas diferentes e as duas fazem falta: a do executor é a
    execução (comando, saída, duração), a do programa é o **efeito** — qual ciclo mudou
    de status por causa dela. Quem lê a trilha do programa não deveria ter de reconstruir
    isso cruzando timestamps.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})

    _cli(tmp_path, "programa", "verificar", "C1")

    alvos = [
        linha["alvo"]
        for linha in trilha.ler(tmp_path)["linhas"]
        if linha.get("ferramenta") == "cli.py"
    ]
    assert any(
        "verificacao-de-aceite-C1" in alvo
        and "codigo_saida=0" in alvo
        and "python passa.py" in alvo
        for alvo in alvos
    ), alvos


# ---------------------------------------------------------------------------
# 3. ordem e atomicidade: executar fora do cadeado, registrar dentro
# ---------------------------------------------------------------------------


def test_o_comando_roda_fora_do_cadeado_e_o_veredito_nao_e_gravado_sem_ele(tmp_path):
    """Mutação que derruba: tomar o cadeado antes de executar (ou gravar sem cadeado).

    As duas metades da ordem, medidas por efeito no mesmo teste, com o cadeado do
    programa na mão do processo de teste:

    - o marcador `rodou.txt` EXISTE ⇒ a execução não esperou o cadeado. Executar lá
      dentro travaria toda sessão da pasta pelo tempo de uma suíte (a deste motor leva
      ~114 s, o teto do executor é 600 s) e envelheceria o próprio cadeado além do
      limite de órfão (30 s), fazendo outra sessão tomá-lo no meio da seção crítica;
    - os bytes do `programa.json` NÃO mudam e o verbo sai 1 dizendo "ocupado" ⇒ o
      registro exigiu o cadeado. Sem ele, é o *lost update* que o `_prog_mutar`
      documenta: o REPROVADO de uma sessão sumindo sob o CONCLUIDO de outra.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "marca.py", MARCA)})
    antes = _impressao_digital(tmp_path)

    with estado.cadeado(
        tmp_path, nome=programa.NOME_CADEADO, idade_maxima=estado.IDADE_MAXIMA_CADEADO
    ):
        saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert (tmp_path / "rodou.txt").is_file(), (
        "o comando de aceite não rodou: a execução passou a esperar o cadeado"
    )
    assert _impressao_digital(tmp_path) == antes, (
        "`programa verificar` gravou o veredito com o cadeado tomado por outra sessão"
    )
    assert saida.returncode == 1
    assert "ocupado" in saida.stdout, saida.stdout
    assert _status(tmp_path, "C1") == "PENDENTE"


def test_criterio_que_muda_durante_a_execucao_nao_vira_veredito(tmp_path):
    """Mutação que derruba: registrar o aceite sem reconferir o comando na releitura.

    É o preço da ordem "executa fora, registra dentro", e ele tem de ser pago: entre a
    execução e a gravação outra sessão pode replanejar. O comando aqui sai 0 **e**
    reescreve o `comando_de_aceite` do C1 — determinístico, sem corrida de relógio. O
    verde na mão passou a ser prova sobre um comando que não é mais o critério, e
    carimbá-lo seria a mesma mentira que `_reaproveitar` evita ao devolver a PENDENTE o
    ciclo cujo critério mudou.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "replaneja.py", REPLANEJA_NO_MEIO)})

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "critério do ciclo" in saida.stdout, saida.stdout
    assert _status(tmp_path, "C1") == "PENDENTE", "o veredito obsoleto foi registrado"
    assert "Traceback" not in saida.stdout + saida.stderr


def test_o_verbo_executa_antes_de_mutar(tmp_path):
    """Mutação que derruba: mover `executor.executar` para dentro do mutador.

    Trava textual, pela mesma tática do C4 e do gate do plano: a ordem é uma propriedade
    do desenho que nenhum assert de comportamento pega sozinho — um refator que passasse
    a executar dentro do mutador continuaria fechando o ciclo corretamente, e só quebraria
    quando duas sessões reais se atropelassem, meses depois.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _prog_verificar")[1].split("\ndef ")[0]

    assert corpo.index("executor.executar(") < corpo.index("_prog_mutar("), (
        "a execução do comando de aceite passou a acontecer depois (ou dentro) da "
        "mutação sob cadeado"
    )
    assert "programa.registrar_aceite(" in corpo
    assert corpo.index("_prog_mutar(") < corpo.index("_prog_trilha("), (
        "a trilha do programa passou a ser escrita antes de o veredito ser gravado"
    )


def test_o_verbo_nao_tem_veredito_literal_para_digitar(tmp_path):
    """Mutação que derruba: `passou=True` (ou qualquer literal) dentro de `_prog_verificar`.

    É a mutação mais barata de escrever e a mais cara de perceber: o verbo continuaria
    rodando o comando, imprimindo a saída inteira e fechando o ciclo — verde sempre,
    com evidência vermelha impressa logo acima. Os testes de comportamento acima pegam
    isso hoje; esta trava impede que ele volte por um caminho que ninguém cobriu.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _prog_verificar")[1].split("\ndef ")[0]

    assert "passou=veredito.aprovado" in corpo
    for literal in ("passou=True", "passou=False", 'passou="ok"'):
        assert literal not in corpo, f"veredito digitado de volta em `verificar`: {literal}"


# ---------------------------------------------------------------------------
# 4. o que o verbo recusa: sem comando, id inexistente, comando travado
# ---------------------------------------------------------------------------


def test_ciclo_sem_comando_de_aceite_e_recusado_com_mensagem_clara(tmp_path):
    """Mutação que derruba: inventar um comando (chutar `pytest`, deduzir da prosa).

    Plano antigo não tem o que rodar, e fabricar a linha que ninguém declarou seria
    carimbar o ciclo com um critério inventado — a versão automática do veredito
    digitado, e pior, porque teria aparência de verificação. A recusa precisa dizer o
    que fazer: o caminho manual com justificativa, ou replanejar declarando o comando.
    """
    dados = _programa_pronto(tmp_path, {"C1": "python passa.py"})
    dados["ciclos"][0].pop(programa.CAMPO_COMANDO)  # o formato anterior ao P2C2
    programa.gravar(tmp_path, dados)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert saida.returncode == 1
    assert programa.CAMPO_COMANDO in saida.stdout
    assert "--porque" in saida.stdout, "a recusa não diz qual é o outro caminho"
    assert _impressao_digital(tmp_path) == antes
    assert not _linhas_do_executor(tmp_path), "recusou e mesmo assim executou algo"


def test_ciclo_inexistente_e_recusado_sem_executar_nada(tmp_path):
    """Mutação que derruba: descobrir o ciclo só dentro do mutador, depois de executar.

    Com a checagem tardia, um id digitado errado faria a suíte inteira rodar para depois
    dizer que o ciclo não existe — minutos gastos e, pior, um veredito real sem onde ser
    registrado. A recusa por id é barata e vem antes.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "marca.py", MARCA)})

    saida = _cli(tmp_path, "programa", "verificar", "C9")

    assert saida.returncode == 1
    assert "C9" in saida.stdout and "C1" in saida.stdout
    assert not (tmp_path / "rodou.txt").exists(), "executou o comando de outro ciclo"
    assert not _linhas_do_executor(tmp_path)


def test_comando_travado_pela_politica_de_risco_reprova_sem_executar(tmp_path):
    """Mutação que derruba: tirar a classificação de risco do caminho do programa.

    Autonomia de processo não é autonomia de risco. O comando de aceite atravessa
    `ferramentas.risco` como qualquer comando de shell do motor, e o travado não roda:
    vira REPROVADO fundamentado. A prova é o efeito colateral — o arquivo sobrevive.
    """
    alvo = tmp_path / "marcador.txt"
    alvo.write_text("nao me apague", encoding="utf-8")
    _programa_pronto(tmp_path, {"C1": "del marcador.txt"})

    saida = _cli(tmp_path, "programa", "verificar", "C1")

    assert alvo.is_file(), "o comando travado executou mesmo assim"
    assert saida.returncode == 1
    assert _status(tmp_path, "C1") == "REPROVADO"
    assert "risco" in saida.stdout.lower()


# ---------------------------------------------------------------------------
# 5. o caminho manual continua existindo — e passou a custar justificativa
# ---------------------------------------------------------------------------


def test_aceite_digitado_sem_porque_e_recusado_e_nao_grava(tmp_path):
    """Mutação que derruba: manter `aceite <C> ok` funcionando como antes.

    O verbo manual não foi removido (plano antigo não tem comando a rodar), mas deixou
    de ser o caminho fácil: enquanto digitar veredito custar menos do que verificá-lo,
    digitar continua sendo o padrão — e o programa 2 inteiro existe para inverter isso.
    A impressão digital cobra a metade que o código de saída não pega: recusar e gravar
    assim mesmo.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "aceite", "C1", "ok")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "justificativa" in saida.stdout
    assert "verificar" in saida.stdout, "a recusa não aponta o caminho verificado"
    assert _impressao_digital(tmp_path) == antes
    assert _status(tmp_path, "C1") == "PENDENTE"


def test_porque_vazio_nao_satisfaz_a_exigencia(tmp_path):
    """Mutação que derruba: checar a presença da bandeira (`"--porque" in args`).

    `--porque ""` satisfaz "a bandeira veio" e não justifica nada — é o mesmo furo que a
    validação do `comando_de_aceite` fecha com `.strip()`, e ele voltaria inteiro se a
    checagem nova fosse escrita com menos cuidado que a vizinha.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})

    for cauda in (("--porque",), ("--porque", "   ")):
        saida = _cli(tmp_path, "programa", "aceite", "C1", "ok", *cauda)
        assert saida.returncode == 1, saida.stdout
        assert _status(tmp_path, "C1") == "PENDENTE"


def test_aceite_digitado_com_porque_grava_e_a_justificativa_vai_para_a_trilha(tmp_path):
    """Mutação que derruba: uma exigência que recusa sempre, ou que engole o motivo.

    O par obrigatório dos dois testes acima: o caminho manual precisa continuar
    funcionando, senão programa antigo fica sem forma nenhuma de fechar ciclo. E a
    justificativa só serve se ficar registrada — impressa no terminal ela some com a
    sessão, e o "CONCLUIDO" volta a ser um carimbo sem razão.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})

    saida = _cli(
        tmp_path,
        "programa",
        "aceite",
        "C1",
        "ok",
        "--porque",
        "plano antigo: aceite conferido a mao com o usuario",
    )

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert _status(tmp_path, "C1") == "CONCLUIDO"
    alvos = [linha["alvo"] for linha in trilha.ler(tmp_path)["linhas"]]
    assert any(
        "aceite-de-ciclo-ok" in alvo
        and "conferido a mao com o usuario" in alvo
        and "digitado" in alvo
        for alvo in alvos
    ), alvos


def test_a_justificativa_aceita_frase_com_espacos_sem_aspas(tmp_path):
    """Mutação que derruba: `args[indice + 1]` — só a primeira palavra vira motivo.

    Motivo é frase. Pegar uma palavra só produziria trilha com "plano" no lugar de
    "plano antigo, sem comando declarado", e o atrito de ter de citar aspas
    corretamente em dois shells diferentes é o que faz aparecer justificativa de uma
    palavra — que é justificativa nenhuma.
    """
    _programa_pronto(tmp_path, {"C1": _script(tmp_path, "passa.py", PASSA)})

    _cli(
        tmp_path, "programa", "aceite", "C1", "falhou",
        "--porque", "o", "aceite", "nao", "cobre", "o", "caso", "real",
    )

    alvos = [linha["alvo"] for linha in trilha.ler(tmp_path)["linhas"]]
    assert any("o aceite nao cobre o caso real" in alvo for alvo in alvos), alvos


def test_o_veredito_digitado_continua_valendo_para_plano_antigo(tmp_path):
    """Mutação que derruba: exigir `comando_de_aceite` também no caminho manual.

    É a razão de o verbo manual não ter sido removido, dita como teste: um
    `programa.json` sem o campo tem de conseguir fechar ciclo. Uma exigência a mais aqui
    deixaria esses programas travados para sempre, com o motor mandando replanejar um
    plano que o usuário já aprovou.
    """
    dados = _programa_pronto(tmp_path, {"C1": "python passa.py"})
    dados["ciclos"][0].pop(programa.CAMPO_COMANDO)
    programa.gravar(tmp_path, dados)

    saida = _cli(
        tmp_path, "programa", "aceite", "C1", "ok", "--porque", "plano anterior ao P2C2"
    )

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert _status(tmp_path, "C1") == "CONCLUIDO"


# ---------------------------------------------------------------------------
# 6. a documentação que o usuário lê
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "trecho",
    ["verificar <CICLO>", "--porque", "CÓDIGO DE SAÍDA"],
    ids=["verbo", "justificativa", "quem-decide"],
)
def test_o_uso_do_programa_anuncia_o_caminho_verificado(trecho):
    """Mutação que derruba: entregar o verbo e não documentá-lo no `USO_PROGRAMA`.

    O texto de uso é o que a CLI imprime quando alguém erra a linha — é o único lugar em
    que o motor se explica sem ninguém ter lido a skill. Verbo não anunciado é verbo que
    não existe para quem está com o problema na mão.
    """
    from ferramentas import cli

    assert trecho in cli.USO_PROGRAMA


def test_a_skill_manda_verificar_em_vez_de_digitar():
    """Mutação que derruba: deixar a skill mandando `programa aceite <CICLO> ok`.

    A skill é o que o modelo lê para conduzir a EXECUCAO. Com o passo antigo escrito
    lá, o caminho digitado continuaria sendo o padrão de fato por mais que a CLI
    oferecesse o verificado — e o ciclo teria entregado capacidade sem mudar
    comportamento nenhum.
    """
    texto = (RAIZ_PLUGIN / "skills" / "engine" / "SKILL.md").read_text(encoding="utf-8")

    assert "CLI programa verificar <CICLO>" in texto
    assert '--porque "<motivo>"' in texto
    assert "CLI programa aceite <CICLO> ok` — ou `falhou`" not in texto, (
        "o passo 4 antigo (veredito digitado como caminho normal) continua na skill"
    )


# ---------------------------------------------------------------------------
# 8. o dependente não fecha por cima de dependência aberta (achado do P2C5)
# ---------------------------------------------------------------------------
#
# O buraco que a cobaia do P2C5 abriu: `proximo` sempre respeitou o DAG, mas ele só
# SUGERE. Quem fecha um ciclo é `verificar`, e ele aceitava qualquer id — com C1
# REPROVADO, `programa verificar C2` rodava a suíte do dependente, saía 0 e carimbava
# C2 CONCLUIDO, logo depois de a própria CLI ter impresso que "os dependentes seguem
# bloqueados". A frase era falsa no único caminho que decide.


def test_verificar_dependente_com_dependencia_reprovada_e_recusado(tmp_path):
    """Mutação que derruba: tirar o gate de `registrar_aceite` (ou o pré-checo da CLI).

    O teste que faltava. `test_ciclo_reprovado_bloqueia_o_dependente` cobrava o bloqueio
    só pela via consultiva (`programa proximo`); ninguém tentava fechar o dependente
    direto, que é o que qualquer pessoa apressada faz quando o encadeamento reclama.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "falha.py", FALHA),
            "C2": _script(tmp_path, "passa.py", PASSA),
        },
    )
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1

    saida = _cli(tmp_path, "programa", "verificar", "C2")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert _status(tmp_path, "C2") == "PENDENTE", (
        "o dependente foi dado por concluído com a dependência vermelha"
    )
    assert "C1" in saida.stdout, "a recusa não diz qual dependência falta"
    assert "Traceback" not in saida.stdout + saida.stderr


def test_a_recusa_do_dependente_nao_chega_a_rodar_o_comando(tmp_path):
    """Mutação que derruba: recusar só no registro, deixando a execução acontecer antes.

    Provado por efeito colateral, não por texto: o comando de C2 escreve `rodou.txt`. Se
    o arquivo aparecer, a suíte do dependente rodou — e o pior nem é o tempo perdido, é
    a evidência VERDE impressa na tela e gravada na trilha um parágrafo antes da recusa.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "falha.py", FALHA),
            "C2": _script(tmp_path, "marca.py", MARCA),
        },
    )
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1

    _cli(tmp_path, "programa", "verificar", "C2")

    assert not (tmp_path / "rodou.txt").exists(), (
        "o comando do dependente rodou antes de a recusa acontecer"
    )
    assert [
        linha for linha in _linhas_do_executor(tmp_path) if linha.get("ciclo") == "C2"
    ] == [], "a recusa deixou veredito de C2 na trilha"


def test_o_dependente_fecha_depois_que_a_dependencia_e_consertada(tmp_path):
    """Mutação que derruba: barrar o dependente para sempre (gate largo demais).

    O par obrigatório do teste acima: o gate não pode virar um cadeado. Consertada e
    reverificada a dependência, o dependente fecha pelo mesmo verbo, sem nada de
    especial.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "aceite1.py", FALHA),
            "C2": _script(tmp_path, "passa.py", PASSA),
        },
    )
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1
    assert _cli(tmp_path, "programa", "verificar", "C2").returncode == 1

    (tmp_path / "aceite1.py").write_text(PASSA, encoding="utf-8")  # o conserto
    assert _cli(tmp_path, "programa", "reabrir", "C1").returncode == 0
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 0

    assert _cli(tmp_path, "programa", "verificar", "C2").returncode == 0
    assert _status(tmp_path, "C2") == "CONCLUIDO"


def test_o_veredito_digitado_tambem_respeita_a_dependencia(tmp_path):
    """Mutação que derruba: escrever o gate no verbo `verificar` em vez de na máquina.

    O caminho digitado (`programa aceite`) fecha o mesmo ciclo pelo mesmo
    `registrar_aceite`. Um gate escrito só no verbo verificado deixaria a porta dos
    fundos aberta — e ela é a mais fácil de usar, porque não roda nada.
    """
    _programa_pronto(
        tmp_path,
        {
            "C1": _script(tmp_path, "falha.py", FALHA),
            "C2": _script(tmp_path, "passa.py", PASSA),
        },
    )
    assert _cli(tmp_path, "programa", "verificar", "C1").returncode == 1

    saida = _cli(
        tmp_path, "programa", "aceite", "C2", "ok", "--porque", "conferi na mao"
    )

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert _status(tmp_path, "C2") == "PENDENTE"
