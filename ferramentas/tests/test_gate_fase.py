"""Gate DURO da transição DESCOBERTA -> ANALISE, pela CLI de verdade.

Cada teste nomeia, na docstring, a mutação que o derrubaria — é o que separa teste que
prova de teste que acompanha o código. Quatro coisas são cobradas aqui, e nenhuma delas
é "a mensagem está bonita":

1. bloqueante aberta recusa e **sai 1**;
2. a recusa não escreve nada — o `estado.json` sai **byte-idêntico**;
3. respondidas as bloqueantes, a mesma transição passa e **sai 0**;
4. o predicado que estoura **fecha** o portão, nunca o abre.

Os testes de ponta a ponta rodam a CLI como subprocesso (é assim que a skill a usa, e é
o único jeito de medir código de saída de verdade). Os de injeção de exceção rodam
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

from ferramentas import cli, descoberta, estado  # noqa: E402
from ferramentas.tests.apoio_descoberta import fechar_descoberta  # noqa: E402


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _ligar(raiz: Path) -> None:
    assert _cli(raiz, "ligar", "construir um sistema novo").returncode == 0


def _impressao_digital(raiz: Path) -> str:
    """SHA-256 dos BYTES do estado. Comparar o dicionário carregado esconderia
    reordenação de chaves, carimbo novo e mudança de indentação — todas escritas."""
    return hashlib.sha256(estado.caminho(raiz).read_bytes()).hexdigest()


# --- 1. bloqueante aberta recusa e sai 1 -------------------------------------------


def test_transicao_com_bloqueante_aberta_sai_1(tmp_path):
    """Cai se o gate deixar de existir, ou se recusar imprimindo e devolvendo 0.

    Código de saída é o que a skill lê para saber se a fase mudou. Um gate que imprime
    "recusado" e sai 0 é indistinguível de sucesso para quem automatiza.
    """
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)["fase"] == "DESCOBERTA"


def test_a_recusa_nomeia_as_lacunas_e_traz_a_pergunta_inteira(tmp_path):
    """Cai se a mensagem virar um "bloqueado" genérico, ou listar só os ids.

    Sem a pergunta inteira, quem leu a recusa não sabe o que responder e volta a
    perguntar ao modelo — que foi o motivo de a decisão aberta carregar a pergunta em
    vez de um rótulo, lá em `DecisaoAberta`.
    """
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")
    abertas = descoberta.avaliar_do_disco(tmp_path).bloqueantes
    assert abertas, "o preparo deste teste precisa de pelo menos uma bloqueante"

    saida = _cli(tmp_path, "fase", "ANALISE")

    for decisao in abertas:
        assert decisao.id in saida.stdout
        assert decisao.pergunta in saida.stdout


# --- 2. a recusa não escreve nada ---------------------------------------------------


def test_estado_fica_byte_identico_depois_da_recusa(tmp_path):
    """Cai se o gate for checado DEPOIS de `transicionar`, ou fora do mutador.

    É o teste central do ciclo. Um gate que recusa mas deixa `fases_concluidas` com
    DESCOBERTA dentro (porque `transicionar` já rodou e mutou o dicionário no lugar)
    passaria em todos os outros testes deste arquivo e corromperia o ciclo em silêncio:
    a fase voltaria a poder ser "concluída" sem nunca ter passado.
    """
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 1
    assert _impressao_digital(tmp_path) == antes, (
        "a recusa gravou no estado: o gate tem de decidir antes de qualquer escrita"
    )


def test_recusa_nao_inventa_fases_concluidas(tmp_path):
    """Cai se `transicionar` rodar antes do gate: ele acrescenta a fase atual à lista.

    Redundante com o teste de bytes de propósito — este nomeia o campo exato que a
    inversão de ordem estragaria, e é o que aparece no relatório de quem depurar.
    """
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")

    _cli(tmp_path, "fase", "ANALISE")

    assert estado.carregar(tmp_path)["fases_concluidas"] == []


# --- 3. respondida a bloqueante, passa ----------------------------------------------


def test_depois_de_responder_as_bloqueantes_a_transicao_passa(tmp_path):
    """Cai se o gate bloquear sempre — o modo de falhar mais fácil de não perceber.

    Um gate que nunca abre passa em todo teste de recusa e trava o motor inteiro na
    primeira fase. Este é o par obrigatório de todos os testes acima.
    """
    _ligar(tmp_path)
    fechar_descoberta(tmp_path)
    assert descoberta.avaliar_do_disco(tmp_path).liberado_para_planejar

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    dados = estado.carregar(tmp_path)
    assert dados["fase"] == "ANALISE"
    assert dados["fases_concluidas"] == ["DESCOBERTA"]


def test_a_mesma_transicao_recusada_passa_apos_as_respostas(tmp_path):
    """Cai se a recusa deixar rastro que impeça a transição depois (marca de bloqueio
    persistida, contador, o que for). A sequência recusa -> responde -> passa é o
    caminho real de uma sessão, e ela tem de funcionar no MESMO ciclo, sem religar."""
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")
    assert _cli(tmp_path, "fase", "ANALISE").returncode == 1

    fechar_descoberta(tmp_path)

    assert _cli(tmp_path, "fase", "ANALISE").returncode == 0
    assert estado.carregar(tmp_path)["fase"] == "ANALISE"


# --- 4. falha FECHADA ----------------------------------------------------------------


def test_predicado_que_estoura_bloqueia_a_transicao(tmp_path, monkeypatch, capsys):
    """Cai se o `except` do gate virar `return None` (liberar) em vez de recusar.

    A exceção é injetada em `descoberta.avaliar`, que é o predicado inteiro. Rodar no
    mesmo processo é o que permite injetar; o preço é não medir o código de saída de um
    processo de verdade, e por isso os outros testes usam subprocesso.
    """
    _ligar(tmp_path)
    fechar_descoberta(tmp_path)  # sem bloqueante nenhuma: se liberasse, seria por erro
    antes = _impressao_digital(tmp_path)

    def _explodir(_dados):
        raise RuntimeError("catálogo inválido, estado corrompido, o que for")

    monkeypatch.setattr(descoberta, "avaliar", _explodir)
    monkeypatch.setenv("ENGINE_RAIZ", str(tmp_path))

    codigo = cli.principal(["fase", "ANALISE"])

    assert codigo == 1
    assert "FECHADO" in capsys.readouterr().out
    assert _impressao_digital(tmp_path) == antes
    assert estado.carregar(tmp_path)["fase"] == "DESCOBERTA"


def test_bloco_de_descoberta_em_versao_desconhecida_bloqueia(tmp_path):
    """Cai se o gate tratar `DescobertaInvalida` como "sem bloqueante".

    Falha fechada pela CLI de verdade, sem injeção: um bloco gravado por um motor mais
    novo faz `descoberta.avaliar` levantar. Ler campos que mudaram de significado
    produziria uma avaliação plausível — e avaliação plausível abre portão.
    """
    _ligar(tmp_path)
    fechar_descoberta(tmp_path)

    def _envelhecer(dados):
        dados[descoberta.CHAVE]["versao"] = descoberta.VERSAO_BLOCO + 99
        return dados

    estado.atualizar(tmp_path, _envelhecer)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "FECHADO" in saida.stdout
    assert _impressao_digital(tmp_path) == antes


def test_estado_antigo_sem_descoberta_bloqueia_sem_quebrar(tmp_path):
    """Cai se o gate exigir a chave `descoberta` (levantaria `KeyError`) ou se tratar
    a ausência como "nada bloqueia".

    Estado gravado antes deste ciclo não tem a chave, e `estado.VERSAO` não subiu: o
    arquivo tem de carregar. Carregar não é passar — "não sei quais lacunas existem" e
    "não há lacuna" são frases opostas, e é a confusão entre as duas que este teste
    cobra.
    """
    _ligar(tmp_path)
    assert descoberta.CHAVE not in estado.carregar(tmp_path)
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "não foi registrada" in saida.stdout
    assert "Traceback" not in saida.stderr
    assert _impressao_digital(tmp_path) == antes


# --- nenhum caminho termina em traceback ---------------------------------------------


@pytest.mark.parametrize(
    "preparo",
    ["sem_ciclo", "sem_descoberta", "com_bloqueante", "liberado", "bloco_quebrado"],
)
def test_nenhum_caminho_do_gate_termina_em_traceback(tmp_path, preparo):
    """Cai se alguma exceção nova escapar do gate — `DescobertaInvalida`,
    `KeyError` do bloco, `ValueError` de eixo fora da taxonomia.

    Traceback no terminal do usuário é o formato de erro que a CLI proíbe no topo do
    próprio arquivo: a skill lê esta saída para decidir o que reportar.
    """
    if preparo != "sem_ciclo":
        _ligar(tmp_path)
    if preparo == "com_bloqueante":
        descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")
    if preparo == "liberado":
        fechar_descoberta(tmp_path)
    if preparo == "bloco_quebrado":
        fechar_descoberta(tmp_path)

        def _quebrar(dados):
            dados[descoberta.CHAVE]["contextos"] = ["ISTO_NAO_E_UM_CONTEXTO"]
            return dados

        estado.atualizar(tmp_path, _quebrar)

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert "Traceback" not in saida.stderr, saida.stderr
    assert "Traceback" not in saida.stdout, saida.stdout
    assert saida.returncode in (0, 1)
    if preparo != "liberado":
        assert saida.returncode == 1


# --- só a aresta DESCOBERTA -> ANALISE é afetada --------------------------------------


def test_outras_arestas_seguem_sem_gate_de_descoberta(tmp_path):
    """Cai se o gate for aplicado a toda transição (ou pela fase de DESTINO apenas).

    Um ciclo que chegou em ANALISE sem bloco de descoberta — porque veio de antes deste
    ciclo de trabalho — não pode ficar preso: só a passagem que a elicitação protege é
    a que exige a entrevista fechada.
    """
    _ligar(tmp_path)

    def _pular_para_analise(dados):
        dados["fase"] = "ANALISE"
        return dados

    estado.atualizar(tmp_path, _pular_para_analise)
    assert descoberta.CHAVE not in estado.carregar(tmp_path)

    saida = _cli(tmp_path, "fase", "PLANO")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)["fase"] == "PLANO"


def test_transicao_fora_do_grafo_continua_reprovando_pelo_grafo(tmp_path):
    """Cai se o gate passar à frente de `transicionar` e trocar a mensagem de erro.

    Pedir ENTREGA a partir de DESCOBERTA é erro de grafo, não de descoberta, e a
    mensagem tem de continuar dizendo isso — mesmo com a descoberta fechada.
    """
    _ligar(tmp_path)
    fechar_descoberta(tmp_path)

    saida = _cli(tmp_path, "fase", "ENTREGA")

    assert saida.returncode == 1
    assert "não existe no grafo" in saida.stdout


# --- forma da mensagem: o que a skill lê ---------------------------------------------


def test_a_recusa_diz_que_nada_foi_gravado(tmp_path):
    """Cai se a mensagem sumir. Quem lê "bloqueado" precisa saber que o ciclo continua
    em DESCOBERTA e que não há nada para desfazer — sem isso a reação natural é mexer
    no `estado.json` à mão."""
    _ligar(tmp_path)
    descoberta.registrar(tmp_path, "construir um sistema novo", intencao="MATERIALIZAR")

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert "Nada foi gravado" in saida.stdout


def test_o_gate_nao_e_o_hook_de_stop(tmp_path):
    """Cai se alguém copiar a política de `hooks/engine_gate.py` para cá.

    Aquele hook engole exceção e sai 0 — é rede secundária no Stop, e derrubar o turno
    por defeito do motor seria pior. Este é o caminho real da transição e o custo do
    erro é invertido. A checagem é sobre o texto do `cli.py`: o `except` do gate não
    pode devolver `None`.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _gate_descoberta")[1].split("\ndef ")[0]
    depois_do_except = corpo.split("except Exception")[1]
    assert "return None" not in depois_do_except, (
        "o tratamento de exceção do gate está liberando a transição"
    )


def test_a_avaliacao_do_gate_nao_le_o_disco_por_fora(tmp_path):
    """Cai se `_gate_descoberta` passar a receber a raiz e chamar `avaliar_do_disco`.

    O gate roda com o cadeado do estado tomado, e o cadeado não é reentrante: uma
    leitura por caminho ali dentro travaria até o timeout e viraria `EstadoOcupado`
    intermitente — o pior tipo de defeito para reproduzir.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _gate_descoberta")[1].split("\ndef ")[0]
    assert "avaliar_do_disco" not in corpo
    assert "descoberta.avaliar(" in corpo


def test_estado_com_descoberta_liberada_grava_o_bloco_intacto(tmp_path):
    """Cai se a transição reescrever ou apagar o bloco de descoberta ao gravar.

    O gate lê o mesmo dicionário que `transicionar` altera; um gate que devolvesse um
    dicionário novo (em vez de mutar o recebido) perderia respostas da entrevista na
    passagem de fase.
    """
    _ligar(tmp_path)
    fechar_descoberta(tmp_path)
    bloco_antes = json.loads(json.dumps(estado.carregar(tmp_path)[descoberta.CHAVE]))

    assert _cli(tmp_path, "fase", "ANALISE").returncode == 0

    assert estado.carregar(tmp_path)[descoberta.CHAVE] == bloco_antes
