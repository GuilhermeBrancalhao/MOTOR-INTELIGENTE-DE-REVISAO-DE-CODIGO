"""Gate da macro-DESCOBERTA: `CONCEPCAO -> PLANO_MESTRE`, pela CLI de verdade.

A spec da Fase 4 declara, por escrito, que `CONCEPCAO` **é** a macro-DESCOBERTA
conduzida pelo papel `descobridor`. Até este ciclo isso era só declaração:
`programa.propor_plano` transicionava exigindo `aceite_de_sistema` não-vazio e DAG
válido, e nada verificava que a entrevista tinha acontecido. Declarado e nunca
verificado é a definição de invariante que não existe.

Cinco coisas são cobradas aqui, e cada docstring nomeia a mutação que a derruba:

1. bloqueante aberta levanta `programa.DescobertaIncompleta`, **sai 1** e não transiciona;
2. sem bloqueante, a mesma proposta passa e **sai 0**;
3. o predicado que estoura **fecha** o portão — nunca o abre;
4. `propor_plano` continua pura sobre dicionário (é disso que dependem os 29 testes de
   `test_programa.py`), e o gate continua vindo ANTES dela no `cli.py`;
5. a recusa lista as lacunas com a **pergunta inteira**, como o gate de fase faz.

Os testes de ponta a ponta rodam a CLI como subprocesso — é assim que a skill a usa, e
é o único jeito de medir código de saída de verdade. Os de injeção de exceção rodam
`cli.principal` no mesmo processo, porque `monkeypatch` não atravessa `subprocess`.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import cli, descoberta, estado, programa  # noqa: E402
from ferramentas.tests.apoio_descoberta import fechar_descoberta  # noqa: E402

OBJETIVO = "construir um sistema novo que soma dois numeros"

#: Decomposição mínima e **válida**: DAG trivial, aceite falsificável **com comando
#: executável**, aceite de sistema declarado. Válida de propósito — um plano inválido
#: faria os testes passarem pela recusa errada, e o gate poderia nem existir sem ninguém
#: notar. Depois do aceite executável isso ficou literal: sem `comando_de_aceite`, todo
#: teste de recusa deste arquivo passaria pelo `PlanoInvalido` do comando ausente, e os
#: dois testes que exigem `returncode == 0` cairiam.
PLANO_VALIDO = {
    "aceite_de_sistema": "python -m pytest -q sai 0 e a soma de 2+2 responde 4",
    "ciclos": [
        {
            "id": "C1",
            "objetivo": "ler os dois numeros",
            "depende_de": [],
            "aceite": "pytest tests/c1 -q sai 0",
            "comando_de_aceite": "python -m pytest tests/c1 -q",
        },
        {
            "id": "C2",
            "objetivo": "somar e responder",
            "depende_de": ["C1"],
            "aceite": "pytest tests/c2 -q sai 0",
            "comando_de_aceite": "python -m pytest tests/c2 -q",
        },
    ],
}


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _abrir_programa(raiz: Path) -> Path:
    """Liga o ciclo, abre o programa em CONCEPCAO e escreve o plano em disco.

    O ciclo continua sendo ligado, mesmo depois de a macro-DESCOBERTA ter mudado de
    arquivo: é o cenário real (um programa é conduzido com ciclos), e é ele que garante
    que o gate do plano lê o `programa.json` e **não** o estado do ciclo que está ao
    lado. Sem o ciclo ligado, um gate que voltasse a ler o `estado.json` recusaria por
    ausência de arquivo e todos os testes de recusa passariam pelo motivo errado.
    """
    assert _cli(raiz, "ligar", OBJETIVO).returncode == 0
    assert _cli(raiz, "programa", OBJETIVO).returncode == 0
    arquivo = raiz / "plano.json"
    arquivo.write_text(json.dumps(PLANO_VALIDO, ensure_ascii=False), encoding="utf-8")
    return arquivo


def _descoberta_do_programa(raiz: Path) -> None:
    """Registra a macro-DESCOBERTA **sem** responder nada: o gate tem de recusar."""
    descoberta.registrar(
        raiz, OBJETIVO, intencao="MATERIALIZAR", escopo=descoberta.PROGRAMA
    )


def _fechar_a_do_programa(raiz: Path) -> None:
    """Fecha a macro-DESCOBERTA — a entrevista que o gate do plano lê."""
    fechar_descoberta(raiz, OBJETIVO, escopo=descoberta.PROGRAMA)


def _ate_desvio(raiz: Path, aceitar: tuple[str, ...] = ()) -> Path:
    """Leva o programa até DESVIO: plano proposto, aprovado, ciclos aceitos, execução parada.

    É o preparo da SEGUNDA aresta de entrada em PLANO_MESTRE. Só se chega a ela
    atravessando a primeira, então o caminho é necessariamente longo — e a descoberta
    fica fechada no fim dele, o que obriga cada teste a declarar se quer reabri-la.

    `aceitar` fecha ciclos em EXECUCAO, ANTES do desvio, que é a ordem real: o desvio
    acontece no meio de um trabalho que já andou.

    O fechamento é pelo veredito DIGITADO (com `--porque`, obrigatório desde que existe
    `programa verificar`) de propósito: o que estes testes medem é o que o
    replanejamento faz com um veredito **já dado**, e rodar comando de aceite de
    verdade aqui trocaria isso pela verificação de outro ciclo do motor.
    """
    arquivo = _abrir_programa(raiz)
    _fechar_a_do_programa(raiz)
    assert _cli(raiz, "programa", "plano", str(arquivo)).returncode == 0
    assert _cli(raiz, "programa", "aprovar").returncode == 0
    for cid in aceitar:
        assert _cli(
            raiz, "programa", "aceite", cid, "ok",
            "--porque", "preparo do teste de replanejamento",
        ).returncode == 0
    assert _cli(
        raiz, "programa", "desviar", "stack-fora-do-plano", "o plano previa SQLite"
    ).returncode == 0
    assert programa.carregar(raiz)["estado"] == "DESVIO"
    return arquivo


def _reabrir_a_entrevista(raiz: Path) -> None:
    """Apaga as respostas da macro-DESCOBERTA: ela volta a ter bloqueante aberta.

    Muta o `programa.json` pelo mutador do programa — que é onde a entrevista do sistema
    mora. Apagar as respostas do `estado.json` aqui não reabriria nada para este gate, e
    o teste passaria a medir a recusa por um motivo que não existe.
    """

    def _mutar(dados):
        dados[descoberta.CHAVE]["respostas"] = {}
        return dados

    programa.atualizar(raiz, _mutar)
    assert descoberta.avaliar_do_disco(raiz, escopo=descoberta.PROGRAMA).bloqueantes


def _impressao_digital(raiz: Path) -> str:
    """SHA-256 dos BYTES do `programa.json`.

    Comparar o dicionário carregado esconderia reordenação de chaves, carimbo novo e
    mudança de indentação — todas escritas.
    """
    return hashlib.sha256(programa.caminho(raiz).read_bytes()).hexdigest()


# --- 1. bloqueante aberta recusa, sai 1 e não transiciona -----------------------------


def test_plano_com_bloqueante_aberta_sai_1(tmp_path):
    """Cai se o gate deixar de existir, ou se recusar imprimindo e devolvendo 0.

    Código de saída é o que a skill lê para saber se o plano-mestre foi registrado. Um
    gate que imprime "recusado" e sai 0 é indistinguível de sucesso para quem automatiza
    — e o passo seguinte do orquestrador seria `programa aprovar`.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert programa.carregar(tmp_path)["estado"] == "CONCEPCAO"


def test_a_recusa_nao_transiciona_nem_grava_a_decomposicao(tmp_path):
    """Cai se o gate for checado DEPOIS de `propor_plano`, ou depois de `programa.gravar`.

    É o teste central deste ciclo. Um gate posto depois recusaria na tela e deixaria
    `ciclos` e `aceite_de_sistema` gravados no `programa.json` — e o programa passaria a
    ter uma decomposição que ninguém aprovou, atrás de um estado que diz CONCEPCAO.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1
    assert _impressao_digital(tmp_path) == antes, (
        "a recusa gravou no programa: o gate tem de decidir antes de qualquer escrita"
    )
    depois = programa.carregar(tmp_path)
    assert depois["ciclos"] == []
    assert depois["aceite_de_sistema"] == ""


def test_a_recusa_e_a_excecao_nomeada_do_programa(tmp_path, monkeypatch, capsys):
    """Cai se o gate devolver mensagem em vez de levantar, ou levantar `Exception` crua.

    O tipo é o contrato: `DescobertaIncompleta` diz "vá responder as lacunas", enquanto
    `PlanoInvalido` diz "reescreva o JSON". Fundidas, quem trata a recusa teria de
    distinguir pelo texto da mensagem — e texto não é contrato.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)
    monkeypatch.setenv("ENGINE_RAIZ", str(tmp_path))

    # Um argumento só, e é o dicionário do programa: o gate deixou de ler um segundo
    # arquivo quando a macro-DESCOBERTA passou a morar no que ele já recebe.
    with pytest.raises(programa.DescobertaIncompleta):
        cli._exigir_descoberta_para_o_plano(programa.carregar(tmp_path))

    capsys.readouterr()
    assert cli.principal(["programa", "plano", str(arquivo)]) == 1


def test_a_excecao_nova_herda_de_plano_invalido(tmp_path):
    """Cai se `DescobertaIncompleta` virar uma hierarquia paralela (herdar de `Exception`).

    Um chamador que já escrevia `except programa.PlanoInvalido` — e o próprio `cli.py` é
    um deles — precisa continuar recusando a transição sem alteração. Hierarquia
    paralela transforma cada `except` esquecido num vazamento silencioso: o plano
    passaria com a descoberta aberta, que é exatamente o buraco que este ciclo fecha.
    """
    assert issubclass(programa.DescobertaIncompleta, programa.PlanoInvalido)


# --- 5. a mensagem: lacunas com a pergunta inteira ------------------------------------


def test_a_recusa_nomeia_as_lacunas_e_traz_a_pergunta_inteira(tmp_path):
    """Cai se a mensagem virar um "bloqueado" genérico, ou listar só os ids.

    Sem a pergunta inteira, quem leu a recusa não sabe o que responder e volta a
    perguntar ao modelo — que foi o motivo de `DecisaoAberta` carregar a pergunta em vez
    de um rótulo. É a mesma exigência do gate de fase, e o gate é o mesmo.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)
    abertas = descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA).bloqueantes
    assert abertas, "o preparo deste teste precisa de pelo menos uma bloqueante"

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    for decisao in abertas:
        assert decisao.id in saida.stdout
        assert decisao.pergunta in saida.stdout


def test_a_recusa_nomeia_a_aresta_do_programa_e_nao_a_do_ciclo(tmp_path):
    """Cai se a mensagem do gate de fase for copiada literalmente para cá.

    Quem lê "transição DESCOBERTA -> ANALISE recusada" ao rodar `programa plano` procura
    o defeito no ciclo, não no programa. Os dois gates compartilham a implementação de
    propósito; o que não podem compartilhar é o rótulo da aresta.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert "CONCEPCAO -> PLANO_MESTRE" in saida.stdout
    assert "DESCOBERTA -> ANALISE" not in saida.stdout
    assert "propor o plano-mestre" in saida.stdout
    assert "Nada foi gravado" in saida.stdout


def test_a_recusa_nao_sai_com_prefixo_duplicado(tmp_path):
    """Cai se a cláusula `except` reprefixar a mensagem, imprimindo "ENGINE: ENGINE:".

    A recusa já vem formatada pelo gate. Reprefixar é o erro natural de quem copia a
    cláusula vizinha (`print(f"ENGINE: {erro}")`), e o resultado passa em todo teste de
    código de saída.
    """
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert "ENGINE: ENGINE:" not in saida.stdout


# --- 2. sem bloqueante, transiciona normalmente ---------------------------------------


def test_sem_bloqueante_aberta_o_plano_passa(tmp_path):
    """Cai se o gate bloquear sempre — o modo de falhar mais fácil de não perceber.

    Um gate que nunca abre passa em todo teste de recusa e trava o programa para sempre
    em CONCEPCAO. Este é o par obrigatório de todos os testes de recusa acima.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)
    assert descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA).liberado_para_planejar

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 0, saida.stdout + saida.stderr
    depois = programa.carregar(tmp_path)
    assert depois["estado"] == "PLANO_MESTRE"
    assert [c["id"] for c in depois["ciclos"]] == ["C1", "C2"]


def test_o_mesmo_plano_recusado_passa_apos_as_respostas(tmp_path):
    """Cai se a recusa deixar rastro que impeça a proposta depois (marca persistida,
    contador, o que for). A sequência recusa -> responde -> passa é o caminho real de
    uma sessão, e tem de funcionar no MESMO programa, sem reabrir."""
    arquivo = _abrir_programa(tmp_path)
    _descoberta_do_programa(tmp_path)
    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 1

    from ferramentas.tests.apoio_descoberta import responder_bloqueantes

    responder_bloqueantes(tmp_path, escopo=descoberta.PROGRAMA)

    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 0
    assert programa.carregar(tmp_path)["estado"] == "PLANO_MESTRE"


def test_o_gate_nao_substitui_a_porta_p1(tmp_path):
    """Cai se o gate for confundido com a aprovação: descoberta fechada não é aval.

    Passar no gate leva a PLANO_MESTRE, e PLANO_MESTRE é a parada obrigatória — o
    programa continua parado até o usuário rodar `programa aprovar`. Um gate que
    "adiantasse" a porta porque a entrevista está completa anularia P1, que é a única
    parada garantida do programa.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert programa.carregar(tmp_path)["estado"] == "PLANO_MESTRE"
    assert "Porta do plano-mestre" in saida.stdout


# --- 3. falha FECHADA ------------------------------------------------------------------


def test_predicado_que_estoura_bloqueia_o_plano(tmp_path, monkeypatch, capsys):
    """Cai se o `except` do gate virar liberação em vez de recusa.

    A exceção é injetada em `descoberta.avaliar`, que é o predicado inteiro, com a
    descoberta JÁ FECHADA: se o plano passasse, seria por erro, não por veredito.
    Rodar no mesmo processo é o que permite injetar; o preço é não medir o código de
    saída de um processo de verdade, e por isso os outros testes usam subprocesso.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)
    antes = _impressao_digital(tmp_path)

    def _explodir(_dados, **_):
        raise RuntimeError("catálogo inválido, estado corrompido, o que for")

    monkeypatch.setattr(descoberta, "avaliar", _explodir)
    monkeypatch.setenv("ENGINE_RAIZ", str(tmp_path))

    codigo = cli.principal(["programa", "plano", str(arquivo)])

    assert codigo == 1
    assert "FECHADO" in capsys.readouterr().out
    assert _impressao_digital(tmp_path) == antes
    assert programa.carregar(tmp_path)["estado"] == "CONCEPCAO"


def test_bloco_de_descoberta_em_versao_desconhecida_bloqueia_o_plano(tmp_path):
    """Cai se o gate tratar `DescobertaInvalida` como "sem bloqueante".

    Falha fechada pela CLI de verdade, sem injeção: um bloco gravado por um motor mais
    novo faz `descoberta.avaliar` levantar. Ler campos que mudaram de significado
    produziria uma avaliação plausível — e avaliação plausível abre portão.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)

    def _envelhecer(dados):
        dados[descoberta.CHAVE]["versao"] = descoberta.VERSAO_BLOCO + 99
        return dados

    programa.atualizar(tmp_path, _envelhecer)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "FECHADO" in saida.stdout
    assert _impressao_digital(tmp_path) == antes


def test_programa_corrompido_bloqueia_o_plano_sem_traceback(tmp_path):
    """Cai se o `programa.json` ilegível virar "descoberta ausente e pronto" — ou pior,
    se `ProgramaCorrompido` escapar como traceback.

    O veredito sai do arquivo que a entrevista habita. Arquivo ilegível é ausência de
    veredito, e ausência de veredito fecha o portão. A mensagem tem de dizer que o
    arquivo está quebrado, e não culpar a entrevista: quem lê "descoberta não
    registrada" vai registrá-la de novo por cima de um arquivo corrompido.

    Era o `estado.json` que este teste quebrava, enquanto a macro-DESCOBERTA morava lá.
    Trocar o arquivo aqui não é enfraquecer o teste — é apontá-lo para o arquivo de que
    o veredito agora depende. Que o `estado.json` quebrado tenha deixado de barrar
    `programa plano` é comportamento novo e deliberado, e está coberto em
    `test_descoberta_do_programa.py`.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)
    programa.caminho(tmp_path).write_text("{ isto não é json", encoding="utf-8")
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "Traceback" not in saida.stdout + saida.stderr
    assert "ilegível" in saida.stdout
    assert _impressao_digital(tmp_path) == antes


def test_projeto_sem_descoberta_registrada_recusa_sem_quebrar(tmp_path):
    """Cai se o gate exigir a chave `descoberta` (levantaria `KeyError`) ou se tratar a
    ausência como "nada bloqueia".

    Retrocompatibilidade: `programa.json` gravado antes deste ciclo não tem a chave, e
    `programa.VERSAO` não subiu — o arquivo tem de carregar. Carregar não é passar. "Não
    sei quais lacunas existem" e "não há lacuna" são frases opostas, e é a confusão
    entre as duas que este teste cobra.
    """
    arquivo = _abrir_programa(tmp_path)
    assert descoberta.CHAVE not in programa.carregar(tmp_path)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "não foi registrada" in saida.stdout
    assert "Traceback" not in saida.stderr
    assert _impressao_digital(tmp_path) == antes


def test_programa_sem_ciclo_ligado_recusa_sem_quebrar(tmp_path):
    """Cai se o gate voltar a exigir `.engine/estado.json` para julgar o plano.

    `programa <objetivo>` não exige ciclo ligado, e a macro-DESCOBERTA também não desde
    que mudou de arquivo. Sem estado nenhum na pasta, a recusa tem de sair da entrevista
    do programa que não foi registrada — não de um `AttributeError` sobre um arquivo que
    não é mais consultado.
    """
    assert _cli(tmp_path, "programa", OBJETIVO).returncode == 0
    arquivo = tmp_path / "plano.json"
    arquivo.write_text(json.dumps(PLANO_VALIDO, ensure_ascii=False), encoding="utf-8")
    assert not estado.caminho(tmp_path).is_file()

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "não foi registrada" in saida.stdout
    assert "Traceback" not in saida.stdout + saida.stderr


@pytest.mark.parametrize(
    "preparo",
    ["sem_programa", "sem_descoberta", "com_bloqueante", "liberado", "bloco_quebrado"],
)
def test_nenhum_caminho_do_gate_do_plano_termina_em_traceback(tmp_path, preparo):
    """Cai se alguma exceção nova escapar do gate — `DescobertaInvalida`, `KeyError` do
    bloco, `ValueError` de eixo fora da taxonomia.

    Traceback no terminal do usuário é o formato de erro que a CLI proíbe no topo do
    próprio arquivo: a skill lê esta saída para decidir o que reportar.
    """
    arquivo = tmp_path / "plano.json"
    arquivo.write_text(json.dumps(PLANO_VALIDO, ensure_ascii=False), encoding="utf-8")
    if preparo != "sem_programa":
        _abrir_programa(tmp_path)
    if preparo == "com_bloqueante":
        _descoberta_do_programa(tmp_path)
    if preparo in ("liberado", "bloco_quebrado"):
        _fechar_a_do_programa(tmp_path)
    if preparo == "bloco_quebrado":

        def _quebrar(dados):
            dados[descoberta.CHAVE]["contextos"] = ["ISTO_NAO_E_UM_CONTEXTO"]
            return dados

        programa.atualizar(tmp_path, _quebrar)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert "Traceback" not in saida.stderr, saida.stderr
    assert "Traceback" not in saida.stdout, saida.stdout
    assert saida.returncode in (0, 1)
    if preparo != "liberado":
        assert saida.returncode == 1


# --- só a aresta CONCEPCAO -> PLANO_MESTRE é afetada ----------------------------------


def test_outros_subverbos_do_programa_seguem_sem_gate(tmp_path):
    """Cai se o gate for posto em `_verbo_programa` inteiro, e não no sub-verbo `plano`.

    `programa status` e `programa relatorio` são leitura: travá-los deixaria quem
    esbarrou na recusa sem conseguir nem olhar o programa para entender por quê.
    """
    _abrir_programa(tmp_path)
    assert descoberta.CHAVE not in programa.carregar(tmp_path)

    assert _cli(tmp_path, "programa", "status").returncode == 0
    assert _cli(tmp_path, "programa", "relatorio").returncode == 0


def test_plano_fora_de_concepcao_continua_reprovando_pelo_grafo(tmp_path):
    """Cai se o gate rodar em qualquer estado do programa e trocar a mensagem de erro.

    Pedir `programa plano` com o programa já em PLANO_MESTRE é erro de grafo, não de
    descoberta, e a mensagem tem de continuar dizendo isso — mesmo com a entrevista
    aberta. Um gate que fala primeiro manda o usuário responder lacunas que não são o
    problema.
    """
    arquivo = _abrir_programa(tmp_path)
    _fechar_a_do_programa(tmp_path)
    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 0

    def _apagar_as_respostas(dados):
        dados[descoberta.CHAVE]["respostas"] = {}
        return dados

    programa.atualizar(tmp_path, _apagar_as_respostas)
    assert descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA).bloqueantes

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1
    assert "não existe no grafo" in saida.stdout
    assert "CONCEPCAO -> PLANO_MESTRE recusada" not in saida.stdout


def test_erro_de_uso_do_subverbo_nao_vira_recusa_de_descoberta(tmp_path):
    """Cai se o gate for chamado antes de validar os argumentos do sub-verbo.

    Arquivo de plano inexistente é erro de comando. Respondê-lo com "responda as
    lacunas" manda o usuário para o lado errado, e ele só descobre o engano depois de
    fechar a entrevista inteira.
    """
    _abrir_programa(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(tmp_path / "nao-existe.json"))

    assert saida.returncode == 1
    assert "não encontrado" in saida.stdout
    assert "bloqueante" not in saida.stdout


# --- a SEGUNDA aresta de entrada: DESVIO -> PLANO_MESTRE ------------------------------
#
# O grafo declara `"DESVIO": ("EXECUCAO", "PLANO_MESTRE")` desde o primeiro dia, e por
# um bom tempo o gate olhava só `CONCEPCAO`. Resultado: a macro-DESCOBERTA era exigida
# na primeira vez e dispensada no REPLANEJAMENTO — que é o momento em que ela tem mais
# chance de estar vencida, porque os quatro MOTIVOS_DESVIO são, um a um, a constatação
# de que a entrevista original não previu o que apareceu.


def test_replanejar_a_partir_de_desvio_tambem_passa_pelo_gate(tmp_path):
    """Cai se o gate voltar a comparar o estado com uma origem fixa (`CONCEPCAO`).

    É o teste central da segunda aresta. Com a entrevista reaberta e o programa em
    DESVIO, `programa plano` tem de recusar exatamente como recusaria em CONCEPCAO —
    mesmo código de saída, mesma exceção, e sem tocar no `programa.json`.
    """
    arquivo = _ate_desvio(tmp_path)
    _reabrir_a_entrevista(tmp_path)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert _impressao_digital(tmp_path) == antes, (
        "a recusa no replanejamento gravou no programa"
    )
    assert programa.carregar(tmp_path)["estado"] == "DESVIO"


def test_a_recusa_do_replanejamento_nomeia_a_aresta_do_desvio(tmp_path):
    """Cai se a mensagem trouxer `CONCEPCAO -> PLANO_MESTRE` fixo no texto.

    Quem lê "CONCEPCAO -> PLANO_MESTRE recusada" com o programa em DESVIO procura o
    defeito num estado em que o programa não está mais. A origem sai do estado real.
    """
    arquivo = _ate_desvio(tmp_path)
    _reabrir_a_entrevista(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert "DESVIO -> PLANO_MESTRE" in saida.stdout
    assert "CONCEPCAO -> PLANO_MESTRE" not in saida.stdout
    assert "propor o plano-mestre" in saida.stdout


def test_replanejar_com_a_descoberta_fechada_passa(tmp_path):
    """O par obrigatório: cai se o gate na segunda aresta bloquear sempre.

    Um gate que nunca abre no replanejamento prende para sempre em DESVIO todo programa
    que precisou parar — e a única saída seria editar o JSON à mão.
    """
    arquivo = _ate_desvio(tmp_path)
    assert descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA).liberado_para_planejar

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 0, saida.stdout + saida.stderr
    depois = programa.carregar(tmp_path)
    assert depois["estado"] == "PLANO_MESTRE"
    assert depois["desvio"] is None, (
        "replanejar É a resposta ao desvio: o motivo não pode continuar aberto"
    )
    assert "Porta do plano-mestre" in saida.stdout, (
        "o replanejamento volta a passar pela porta P1, como qualquer plano-mestre"
    )


def test_toda_aresta_de_entrada_em_plano_mestre_tem_gate(tmp_path):
    """Cai se alguém acrescentar uma terceira aresta para PLANO_MESTRE sem gate.

    A lista de origens protegidas é DERIVADA de `programa.TRANSICOES`, e não escrita à
    mão, justamente para que a aresta nova nasça protegida. Este teste é a trava dessa
    derivação: escrever a lista à mão de novo o derruba no dia em que o grafo mudar.
    """
    do_grafo = {
        origem
        for origem, destinos in programa.TRANSICOES.items()
        if "PLANO_MESTRE" in destinos
    }
    assert do_grafo == set(cli.ORIGENS_COM_GATE_DE_PLANO), (
        "há aresta para PLANO_MESTRE fora do conjunto de origens com gate"
    )
    assert do_grafo == {"CONCEPCAO", "DESVIO"}, (
        "o grafo mudou: confirme que a origem nova deve mesmo exigir a descoberta"
    )


def test_replanejar_preserva_o_veredito_dos_ciclos_pela_cli(tmp_path):
    """Cai se `propor_plano` voltar a reconstruir `ciclos` com PENDENTE para todos.

    O defeito irmão do gate ausente: pela aresta do DESVIO, reconstruir do zero apagava
    em silêncio o CONCLUIDO de C1 e o programa passava a afirmar que nada tinha sido
    feito. Aqui isso é medido de ponta a ponta, pela CLI, e não só na função pura.
    """
    arquivo = _ate_desvio(tmp_path, aceitar=("C1",))

    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 0

    por_id = {c["id"]: c["status"] for c in programa.carregar(tmp_path)["ciclos"]}
    assert por_id == {"C1": "CONCLUIDO", "C2": "PENDENTE"}, (
        f"o replanejamento desfez trabalho já aceito: {por_id}"
    )


# --- 4. a pureza de `propor_plano` e a ordem no `cli.py` ------------------------------


def test_propor_plano_continua_pura_sobre_dicionario(tmp_path):
    """Cai se `propor_plano` passar a receber `raiz` ou a ler o disco.

    Os 29 testes de `test_programa.py` chamam esta função sobre dicionário montado à
    mão, sem projeto em disco. Mais do que conveniência de teste, é a propriedade que
    permite ao gate rodar com cadeado na mão sem tentar retomá-lo — e cadeado deste
    motor não é reentrante.
    """
    import inspect

    parametros = list(inspect.signature(programa.propor_plano).parameters)
    assert parametros == ["dados", "ciclos", "aceite_de_sistema"]

    corpo = inspect.getsource(programa.propor_plano).split('"""')[2]
    for proibido in ("open(", "read_text", "Path(", "carregar", "avaliar_do_disco"):
        assert proibido not in corpo, f"`propor_plano` deixou de ser pura: {proibido}"


def test_o_gate_vem_antes_de_propor_plano_no_cli(tmp_path):
    """Cai se alguém mover o gate para depois de `propor_plano`, ou apagá-lo do fluxo.

    Como a obrigatoriedade do gate foi posta no CHAMADOR (e não num argumento opcional
    de `propor_plano`, que qualquer chamada de três argumentos ignoraria), é o texto do
    `cli.py` que guarda o invariante. Este teste é a trava: mesma tática do C4, que
    verifica pelo texto que o gate de fase não voltou a ler o disco por fora do cadeado.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _verbo_programa")[1].split("\ndef ")[0]

    assert "_exigir_descoberta_para_o_plano(" in corpo, (
        "o sub-verbo `plano` deixou de chamar o gate da macro-DESCOBERTA"
    )
    assert corpo.index("_exigir_descoberta_para_o_plano(") < corpo.index(
        "programa.propor_plano("
    ), "o gate precisa vir ANTES de `propor_plano`: depois dela o estado já transicionou"


def test_o_gate_do_plano_nao_e_uma_segunda_versao_do_gate_de_fase(tmp_path):
    """Cai se alguém escrever um predicado próprio para o programa.

    Duas implementações da mesma pergunta divergem no primeiro ajuste, e a divergência
    aparece como um gate mais frouxo que o outro sem ninguém ter decidido isso. O gate
    do plano tem de delegar em `_gate_descoberta` — o mesmo predicado, a mesma política
    de falha fechada, a mesma mensagem.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _exigir_descoberta_para_o_plano")[1].split("\ndef ")[0]

    assert "_gate_descoberta(" in corpo
    assert "liberado_para_planejar" not in corpo, (
        "o gate do plano está reimplementando o predicado em vez de delegar"
    )
