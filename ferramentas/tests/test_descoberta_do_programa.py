"""A macro-DESCOBERTA mora no `programa.json`, e a do ciclo no `estado.json`.

Este arquivo cobre o defeito R4 e as três coisas que o aceite dele exige. O defeito era
de MORADIA, não de lógica: as duas entrevistas dividiam a chave `descoberta` do
`.engine/estado.json`, que é arquivo de vida útil de CICLO. Duas consequências, e as
duas apareceram em uso real:

1. **`ligar` apagava a descoberta do programa.** `estado._novo_ciclo_sem_cadeado` monta
   um dicionário novo (sem a chave) e grava por cima; só `historico` sobrevive. O fluxo
   `programa "X"` → macro-DESCOBERTA → `programa plano` → `aprovar` → `proximo` →
   `ligar "<objetivo do C1>"` deixava a entrevista do sistema para trás, e o
   replanejamento posterior era recusado com "descoberta não registrada" — sem outra
   saída senão refazer a entrevista do sistema inteiro.
2. **O primeiro ciclo do programa nunca fazia descoberta própria.** Como os dois gates
   liam a MESMA chave, a entrevista da CONCEPCAO satisfazia também `DESCOBERTA ->
   ANALISE` do ciclo em que ela tinha sido feita. Ninguém percebia: o portão abria.

Havia ainda um terceiro sintoma, o que denunciou tudo: registrar a macro-DESCOBERTA
exigia `ligar` um ciclo só para ter onde gravar (`registrar` recusa sem continente), e
esse mesmo `ligar` apagava o que se acabara de gravar.

Cada teste nomeia na docstring a mutação que o derruba. O fluxo completo roda pela CLI
como subprocesso, que é como a skill a usa, e é o único jeito de medir código de saída.
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

from ferramentas import descoberta, estado, programa  # noqa: E402
from ferramentas.tests.apoio_descoberta import fechar_descoberta  # noqa: E402

#: O pedido do SISTEMA e o do CICLO são textos diferentes de propósito: é por eles que
#: se prova que cada gate leu a entrevista certa. Fossem iguais, um gate lendo o arquivo
#: errado passaria em todos os testes deste arquivo.
PEDIDO_DO_SISTEMA = "construir um sistema novo de agendamento para a clinica"
PEDIDO_DO_CICLO = "construir um sistema novo que soma dois numeros"

PLANO = {
    "aceite_de_sistema": "a clinica marca uma consulta de ponta a ponta e o teste prova",
    "ciclos": [
        {
            "id": "C1",
            "objetivo": "guardar os horarios livres",
            "depende_de": [],
            "aceite": "a suite de C1 passa inteira",
            "comando_de_aceite": "python -c \"raise SystemExit(0)\"",
        },
        {
            "id": "C2",
            "objetivo": "marcar a consulta",
            "depende_de": ["C1"],
            "aceite": "a suite de C2 passa inteira",
            "comando_de_aceite": "python -c \"raise SystemExit(0)\"",
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


def _digital(alvo: Path) -> str:
    """SHA-256 dos BYTES do arquivo — reordenar chave ou mexer no carimbo também é escrita."""
    return hashlib.sha256(alvo.read_bytes()).hexdigest()


def _plano_em_arquivo(raiz: Path) -> Path:
    arquivo = raiz / "plano.json"
    arquivo.write_text(json.dumps(PLANO, ensure_ascii=False), encoding="utf-8")
    return arquivo


def _abrir_programa_com_descoberta(raiz: Path) -> Path:
    """Programa aberto e macro-DESCOBERTA fechada — **sem** ciclo nenhum ligado."""
    assert _cli(raiz, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    fechar_descoberta(raiz, PEDIDO_DO_SISTEMA, escopo=descoberta.PROGRAMA)
    return _plano_em_arquivo(raiz)


# ---------------------------------------------------------------------------
# 1. `ligar` NÃO apaga a descoberta do programa
# ---------------------------------------------------------------------------


def test_ligar_nao_apaga_a_descoberta_do_programa(tmp_path):
    """Cai se a macro-DESCOBERTA voltar a morar no `estado.json`.

    É o aceite nº 1, e o teste mais direto do defeito: com a entrevista do sistema na
    chave `descoberta` do estado, este `ligar` a apagava inteira — `_novo_ciclo_sem_cadeado`
    monta o dicionário do zero e só `historico` atravessa. Comparar o bloco antes e
    depois, e não só "existe", porque a metade traiçoeira era o mapa de `respostas`: um
    bloco recriado vazio ainda "existe" e não bloqueia nada.
    """
    _abrir_programa_com_descoberta(tmp_path)
    antes = descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)
    assert antes["respostas"], "o preparo precisa de uma entrevista já respondida"

    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0

    depois = descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)
    assert depois == antes, "`ligar` mexeu na entrevista do PROGRAMA"
    assert descoberta.avaliar_do_disco(
        tmp_path, escopo=descoberta.PROGRAMA
    ).liberado_para_planejar


def test_dois_ligar_seguidos_nao_apagam_a_descoberta_do_programa(tmp_path):
    """Cai se a preservação for feita copiando a chave dentro de `ligar` (remendo frágil).

    Um programa de N ciclos chama `ligar` N vezes, e a segunda chamada é onde um remendo
    do tipo "copie a chave do estado anterior" quebraria: o estado do ciclo 2 herdaria a
    chave do ciclo 1, não a do programa. A separação por arquivo não tem esse degrau —
    `ligar` simplesmente não toca no `programa.json`.
    """
    _abrir_programa_com_descoberta(tmp_path)
    antes = _digital(programa.caminho(tmp_path))

    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    assert _cli(tmp_path, "desligar").returncode == 0
    assert _cli(tmp_path, "ligar", "outro trabalho qualquer", "--forcar").returncode == 0

    assert _digital(programa.caminho(tmp_path)) == antes, (
        "algum `ligar` escreveu no programa.json"
    )


def test_registrar_a_do_programa_nao_toca_o_estado_do_ciclo(tmp_path):
    """Cai se `escopo=PROGRAMA` continuar gravando no `estado.json` (escopo ignorado).

    A separação vale nos dois sentidos, e este é o sentido que o gate do ciclo protege:
    a entrevista do sistema não pode aparecer no arquivo que decide `DESCOBERTA ->
    ANALISE`. Byte a byte, porque um bloco escrito e removido depois deixaria o arquivo
    diferente sem deixar a chave.
    """
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    antes = _digital(estado.caminho(tmp_path))

    fechar_descoberta(tmp_path, PEDIDO_DO_SISTEMA, escopo=descoberta.PROGRAMA)

    assert _digital(estado.caminho(tmp_path)) == antes
    assert descoberta.CHAVE not in estado.carregar(tmp_path)


def test_registrar_a_do_ciclo_nao_toca_o_programa(tmp_path):
    """Cai se o escopo padrão de `registrar` virar "o que existir em disco".

    O caminho oposto do teste anterior: a entrevista do ciclo não pode vazar para o
    arquivo que decide `CONCEPCAO -> PLANO_MESTRE`, ou o primeiro ciclo de um programa
    abriria a porta do plano-mestre sem ninguém ter descrito o sistema.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    antes = _digital(programa.caminho(tmp_path))

    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)

    assert _digital(programa.caminho(tmp_path)) == antes
    assert descoberta.CHAVE not in programa.carregar(tmp_path)


def test_as_duas_entrevistas_coexistem_e_nao_se_misturam(tmp_path):
    """Cai se as duas voltarem a dividir a mesma chave do mesmo arquivo.

    Com um arquivo só, a segunda a ser registrada sobrescrevia a primeira em silêncio —
    `registrar` reescreve o bloco inteiro. Os pedidos são textos diferentes justamente
    para que a troca apareça aqui, e não seis passos adiante.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_SISTEMA, escopo=descoberta.PROGRAMA)
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)

    do_programa = descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA)
    do_ciclo = descoberta.avaliar_do_disco(tmp_path)

    assert do_programa.pedido == PEDIDO_DO_SISTEMA
    assert do_ciclo.pedido == PEDIDO_DO_CICLO
    assert do_programa.escopo == "programa"
    assert do_ciclo.escopo == "ciclo"


# ---------------------------------------------------------------------------
# 2. o gate CONCEPCAO -> PLANO_MESTRE continua cobrando — agora a do PROGRAMA
# ---------------------------------------------------------------------------


def test_o_gate_do_plano_continua_cobrando_a_entrevista_do_programa(tmp_path):
    """Cai se a mudança de arquivo tiver desligado o gate (o modo de falhar mais caro).

    É o aceite nº 2. Mover a entrevista de lugar é exatamente o tipo de mudança que
    desliga um gate sem que nenhum teste antigo caia: o gate passaria a ler uma chave que
    nunca existe e — se falhasse ABERTO — deixaria todo plano passar. Aqui ele recusa por
    ausência, recusa por bloqueante aberta e só passa depois de fechada.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    arquivo = _plano_em_arquivo(tmp_path)

    sem_entrevista = _cli(tmp_path, "programa", "plano", str(arquivo))
    assert sem_entrevista.returncode == 1
    assert "não foi registrada" in sem_entrevista.stdout

    descoberta.registrar(
        tmp_path, PEDIDO_DO_SISTEMA, intencao="MATERIALIZAR", escopo=descoberta.PROGRAMA
    )
    so_registrada = _cli(tmp_path, "programa", "plano", str(arquivo))
    assert so_registrada.returncode == 1
    assert "bloqueante" in so_registrada.stdout
    assert programa.carregar(tmp_path)["estado"] == "CONCEPCAO"

    fechar_descoberta(tmp_path, PEDIDO_DO_SISTEMA, escopo=descoberta.PROGRAMA)

    fechada = _cli(tmp_path, "programa", "plano", str(arquivo))
    assert fechada.returncode == 0, fechada.stdout + fechada.stderr
    assert programa.carregar(tmp_path)["estado"] == "PLANO_MESTRE"


def test_a_descoberta_do_CICLO_nao_abre_a_porta_do_plano(tmp_path):
    """Cai se o gate do plano voltar a ler o `.engine/estado.json`.

    O sentido "de baixo para cima" da confusão: a entrevista de UM ciclo — que fala de um
    pedaço, e não do sistema — passaria a autorizar a decomposição do sistema inteiro. Com
    os dois arquivos separados isto só falha se alguém devolver a leitura do estado ao
    gate do plano, que é a mutação que este teste existe para pegar.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)
    assert descoberta.avaliar_do_disco(tmp_path).liberado_para_planejar
    arquivo = _plano_em_arquivo(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "não foi registrada" in saida.stdout
    assert programa.carregar(tmp_path)["estado"] == "CONCEPCAO"


def test_estado_ilegivel_nao_barra_mais_o_plano(tmp_path):
    """Cai se o gate do plano continuar abrindo o `estado.json` para decidir.

    Comportamento NOVO e deliberado, fixado aqui para não voltar por descuido: o veredito
    do plano-mestre depende só do `programa.json`. Antes, um `estado.json` quebrado —
    lixo de outro ciclo, arquivo truncado por um crash — travava a decomposição do sistema
    por um motivo que nada tinha a ver com ela. O ciclo continua protegido pelo seu
    próprio gate, que lê o seu próprio arquivo e falha fechado como sempre.
    """
    arquivo = _abrir_programa_com_descoberta(tmp_path)
    estado.caminho(tmp_path).write_text("{ isto não é json", encoding="utf-8")

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert programa.carregar(tmp_path)["estado"] == "PLANO_MESTRE"


# ---------------------------------------------------------------------------
# 3. o gate DESCOBERTA -> ANALISE passa a exigir descoberta PRÓPRIA do ciclo
# ---------------------------------------------------------------------------


def test_a_descoberta_do_programa_nao_abre_a_fase_do_ciclo(tmp_path):
    """Cai se as duas entrevistas voltarem a dividir a chave — é o aceite nº 3.

    Era o defeito silencioso: a entrevista da CONCEPCAO satisfazia o gate do primeiro
    ciclo, que assim nunca perguntava nada sobre o próprio trabalho. Nada travava, nada
    avisava; o ciclo simplesmente pulava a fase de descoberta. Aqui a macro-DESCOBERTA
    está fechada e o ciclo tem de continuar em DESCOBERTA.
    """
    _abrir_programa_com_descoberta(tmp_path)
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "DESCOBERTA -> ANALISE" in saida.stdout
    assert "não foi registrada" in saida.stdout
    assert estado.carregar(tmp_path)["fase"] == "DESCOBERTA"


def test_o_ciclo_avanca_com_a_entrevista_propria(tmp_path):
    """O par obrigatório do teste acima: cai se o gate do ciclo passar a bloquear sempre.

    Um gate que nunca abre passa em todo teste de recusa e trava o motor para sempre na
    primeira fase — e, com dois arquivos em jogo, o jeito mais fácil de escrever esse
    defeito é o gate do ciclo ler o `programa.json`, que num projeto sem programa nunca
    tem nada.
    """
    _abrir_programa_com_descoberta(tmp_path)
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert estado.carregar(tmp_path)["fase"] == "ANALISE"


# ---------------------------------------------------------------------------
# O fluxo inteiro que quebrava, de ponta a ponta, pela CLI
# ---------------------------------------------------------------------------


def test_o_fluxo_completo_do_programa_sobrevive_ao_replanejamento(tmp_path):
    """Cai se qualquer passo do caminho real voltar a apagar a entrevista do sistema.

    É a reprodução literal do defeito relatado: `programa "X"` → macro-DESCOBERTA →
    `plano` → `aprovar` → `proximo` → `ligar "<objetivo do C1>"` → desvio →
    **replanejar**. O `ligar` do meio era o que apagava a entrevista, e o replanejamento
    era recusado com "descoberta não registrada" — obrigando a refazer a entrevista do
    sistema inteiro. Aqui o replanejamento tem de passar **sem** registrar nada de novo.

    Vai pela CLI de ponta a ponta, e não pela API, porque era pela CLI que o usuário
    esbarrava nisso: cada passo é o comando que a skill roda.
    """
    arquivo = _abrir_programa_com_descoberta(tmp_path)
    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 0
    assert _cli(tmp_path, "programa", "aprovar").returncode == 0

    proximo = _cli(tmp_path, "programa", "proximo")
    assert proximo.returncode == 0
    assert "C1" in proximo.stdout

    assert _cli(tmp_path, "ligar", "guardar os horarios livres").returncode == 0
    assert _cli(
        tmp_path, "programa", "desviar", "stack-fora-do-plano", "o banco escolhido nao serve"
    ).returncode == 0

    replanejamento = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert replanejamento.returncode == 0, replanejamento.stdout + replanejamento.stderr
    depois = programa.carregar(tmp_path)
    assert depois["estado"] == "PLANO_MESTRE"
    assert depois["desvio"] is None
    assert descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)["pedido"] == PEDIDO_DO_SISTEMA


# ---------------------------------------------------------------------------
# A entrevista do programa dispensa ciclo — e é por isso que ela cabe aqui
# ---------------------------------------------------------------------------


def test_a_macro_descoberta_nao_exige_ciclo_ligado(tmp_path):
    """Cai se `registrar` do escopo PROGRAMA voltar a exigir `.engine/estado.json`.

    É o terceiro sintoma do defeito, e o que o denunciou: para registrar a
    macro-DESCOBERTA era preciso `ligar` um ciclo que não correspondia a trabalho nenhum
    — e esse mesmo `ligar` apagava o que se acabara de gravar. O teste também cobra que
    nenhum estado seja criado de lado, porque um `estado.json` fabricado aqui faria
    `status` passar a imprimir ciclo em projeto que não tem ciclo.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0

    saida = _cli(tmp_path, "descoberta", "--programa", PEDIDO_DO_SISTEMA,
                 "--intencao", "MATERIALIZAR")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert not estado.caminho(tmp_path).is_file(), "registrou a do programa e criou estado"
    assert descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)["pedido"] == PEDIDO_DO_SISTEMA


def test_sem_programa_a_recusa_diz_o_que_falta(tmp_path):
    """Cai se a ausência de `programa.json` virar traceback, ou se o bloco for criado do nada.

    `registrar` levanta em vez de inventar o continente pelo mesmo motivo de sempre:
    criar exigiria inventar o pedido e a intenção, e intenção inventada escolhe quais
    perguntas existem. A mensagem tem de dizer qual verbo abre o programa — recusa sem
    saída é portão sem porta.
    """
    saida = _cli(tmp_path, "descoberta", "--programa", PEDIDO_DO_SISTEMA,
                 "--intencao", "MATERIALIZAR")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stdout + saida.stderr
    assert "não há programa nesta pasta" in saida.stdout
    assert not programa.caminho(tmp_path).is_file()


@pytest.mark.parametrize(
    "argumentos",
    [
        ("descoberta", "--programa", "status"),
        ("descoberta", "status", "--programa"),
    ],
)
def test_a_bandeira_vale_em_qualquer_posicao(tmp_path, argumentos):
    """Cai se `--programa` for lido como sub-verbo (ou como palavra do pedido).

    A bandeira é retirada da linha ANTES de separar o sub-verbo. Sem isso,
    `descoberta --programa status` tentaria registrar uma descoberta cujo pedido é
    "status" — que é pior do que um erro de uso, porque grava.
    """
    _abrir_programa_com_descoberta(tmp_path)

    saida = _cli(tmp_path, *argumentos)

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert "# Descoberta do PROGRAMA" in saida.stdout
    assert PEDIDO_DO_SISTEMA in saida.stdout


def test_o_status_de_cada_escopo_fala_do_seu_arquivo(tmp_path):
    """Cai se o retrato deixar de dizer de qual entrevista é.

    Os dois `status` imprimem o mesmo formato e convivem na mesma tela durante a condução
    de um programa. Sem o escopo no título e no comando sugerido, quem lê responde a
    lacuna da entrevista errada — e `descoberta responder` sem `--programa` grava no
    `estado.json`.
    """
    _abrir_programa_com_descoberta(tmp_path)
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)

    do_programa = _cli(tmp_path, "descoberta", "--programa", "status").stdout
    do_ciclo = _cli(tmp_path, "descoberta", "status").stdout

    assert ".engine/programa.json" in do_programa
    assert "programa plano" in do_programa
    assert PEDIDO_DO_SISTEMA in do_programa

    assert ".engine/estado.json" in do_ciclo
    assert "fase ANALISE" in do_ciclo
    assert PEDIDO_DO_CICLO in do_ciclo


def test_responder_com_a_bandeira_muda_so_o_programa(tmp_path):
    """Cai se `--programa` for aceito no registro e ignorado no `responder`.

    Meia conversão é o pior estado possível: a entrevista abriria num arquivo e seria
    respondida no outro, deixando as duas eternamente incompletas. A impressão digital do
    `estado.json` é o que pega isso.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    descoberta.registrar(
        tmp_path, PEDIDO_DO_SISTEMA, intencao="MATERIALIZAR", escopo=descoberta.PROGRAMA
    )
    alvo = descoberta.avaliar_do_disco(tmp_path, escopo=descoberta.PROGRAMA).bloqueantes[0]
    antes = _digital(estado.caminho(tmp_path))

    saida = _cli(tmp_path, "descoberta", "--programa", "responder", alvo.id, "porque sim")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert _digital(estado.caminho(tmp_path)) == antes
    respostas = descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)["respostas"]
    assert alvo.id in respostas


def test_registrar_de_novo_no_programa_e_recusado_sem_forcar(tmp_path):
    """Cai se a guarda de reescrita olhar o `estado.json` enquanto grava no programa.

    `registrar` reescreve o bloco inteiro, respostas incluídas. A guarda que exige
    `--forcar` só protege se ela ler o MESMO arquivo em que vai escrever: lendo o outro,
    ela veria "não há respostas" e deixaria passar — apagando a entrevista do sistema em
    silêncio, que é a versão nova do defeito que este ciclo corrige.
    """
    _abrir_programa_com_descoberta(tmp_path)
    antes = _digital(programa.caminho(tmp_path))

    recusado = _cli(tmp_path, "descoberta", "--programa", "outro pedido qualquer",
                    "--intencao", "MATERIALIZAR")

    assert recusado.returncode == 1
    assert "já existe descoberta de programa registrada" in recusado.stdout
    assert _digital(programa.caminho(tmp_path)) == antes

    forcado = _cli(tmp_path, "descoberta", "--programa", "outro pedido qualquer",
                   "--intencao", "MATERIALIZAR", "--forcar")

    assert forcado.returncode == 0, forcado.stdout + forcado.stderr
    assert descoberta.ler(tmp_path, escopo=descoberta.PROGRAMA)["pedido"] == (
        "outro pedido qualquer"
    )


def test_a_escrita_do_escopo_programa_passa_pelo_cadeado_do_programa(tmp_path):
    """Cai se `registrar(escopo=PROGRAMA)` gravar sem tomar o cadeado do programa.

    Escrita fora do mutador é o *lost update* de volta, e ele some em silêncio até duas
    sessões se atropelarem. Com o cadeado do programa preso por outro processo, a escrita
    tem de esperar e desistir com `EstadoOcupado` — se ela gravar assim mesmo, é porque
    passou por fora de `programa.atualizar`.
    """
    assert _cli(tmp_path, "programa", PEDIDO_DO_SISTEMA).returncode == 0
    antes = _digital(programa.caminho(tmp_path))
    preso = programa.caminho_cadeado(tmp_path)
    preso.write_text("9999\n", encoding="utf-8")

    try:
        with pytest.raises(estado.EstadoOcupado):
            descoberta.registrar(
                tmp_path,
                PEDIDO_DO_SISTEMA,
                intencao="MATERIALIZAR",
                escopo=descoberta.PROGRAMA,
            )
    finally:
        preso.unlink()

    assert _digital(programa.caminho(tmp_path)) == antes


# ---------------------------------------------------------------------------
# Retrocompatibilidade: nem o programa antigo nem o estado antigo podem quebrar
# ---------------------------------------------------------------------------


#: Um `programa.json` no formato de antes desta mudança: em EXECUCAO, com ciclos já
#: fechados e **sem** a chave `descoberta`. É a forma do arquivo que este próprio
#: repositório tem em disco no momento desta correção.
PROGRAMA_ANTIGO = {
    "versao": 1,
    "programa": "2026-08-04-1",
    "objetivo": "um sistema qualquer decomposto antes desta correcao",
    "estado": "EXECUCAO",
    "iniciado_em": "2026-08-04T09:00:00",
    "aceite_de_sistema": "o sistema inteiro roda de ponta a ponta",
    "ciclos": [
        {
            "id": "C1",
            "objetivo": "primeiro pedaco",
            "depende_de": [],
            "aceite": "a suite de C1 passa",
            "comando_de_aceite": "python -c \"raise SystemExit(0)\"",
            "status": "CONCLUIDO",
            "ciclo_do_estado": "2026-08-04-1",
        },
        {
            "id": "C2",
            "objetivo": "segundo pedaco",
            "depende_de": ["C1"],
            "aceite": "a suite de C2 passa",
            "comando_de_aceite": "python -c \"raise SystemExit(0)\"",
            "status": "PENDENTE",
            "ciclo_do_estado": None,
        },
    ],
    "desvio": None,
    "historico": ["2026-08-04-1"],
    "aprovado_em": "2026-08-04T09:30:00",
}


def _gravar_programa_antigo(raiz: Path) -> None:
    caminho = programa.caminho(raiz)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(PROGRAMA_ANTIGO, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def test_programa_antigo_sem_a_chave_continua_sendo_conduzido(tmp_path):
    """Cai se algum caminho de LEITURA passar a exigir a chave `descoberta`.

    Retrocompatibilidade dura: `programa.VERSAO` não subiu e não há migração escrita, então
    o arquivo gravado ontem tem de continuar carregando, imprimindo e encadeando. Só o
    caminho que ENTRA em PLANO_MESTRE cobra a entrevista — e este programa está em
    EXECUCAO, longe dele.
    """
    _gravar_programa_antigo(tmp_path)

    assert _cli(tmp_path, "programa", "status").returncode == 0
    assert _cli(tmp_path, "programa", "relatorio").returncode == 0
    proximo = _cli(tmp_path, "programa", "proximo")
    assert proximo.returncode == 0, proximo.stdout + proximo.stderr
    assert "C2" in proximo.stdout

    verificacao = _cli(tmp_path, "programa", "verificar", "C2")
    assert verificacao.returncode == 0, verificacao.stdout + verificacao.stderr
    assert {c["id"]: c["status"] for c in programa.carregar(tmp_path)["ciclos"]} == {
        "C1": "CONCLUIDO",
        "C2": "CONCLUIDO",
    }


def test_programa_antigo_aceita_a_entrevista_sem_migracao(tmp_path):
    """Cai se `registrar` exigir um bloco preexistente para escrever no programa antigo.

    O caminho de conserto de quem tem um programa em disco: registrar a macro-DESCOBERTA
    agora, sem tocar em mais nada do arquivo. Nenhuma migração automática faz isso
    sozinha — de propósito. Copiar a chave do `estado.json` para cá seria adivinhar que a
    entrevista de lá é a do sistema, e depois de um `ligar` ela é a de um CICLO: o motor
    carimbaria como descoberta do sistema uma conversa sobre um pedaço dele.
    """
    _gravar_programa_antigo(tmp_path)

    fechar_descoberta(tmp_path, PEDIDO_DO_SISTEMA, escopo=descoberta.PROGRAMA)

    depois = programa.carregar(tmp_path)
    assert descoberta.avaliar(
        depois, escopo=descoberta.PROGRAMA
    ).liberado_para_planejar
    for campo in ("versao", "programa", "objetivo", "estado", "ciclos", "historico"):
        assert depois[campo] == PROGRAMA_ANTIGO[campo], f"{campo} foi alterado"


def test_estado_antigo_com_descoberta_continua_servindo_o_gate_do_ciclo(tmp_path):
    """Cai se a leitura da entrevista do ciclo mudar de chave ou de formato.

    O outro lado da retrocompatibilidade: este repositório tem um `estado.json` com a
    chave `descoberta` gravada pelo motor anterior. Ela continua sendo, e tem de continuar
    sendo, a entrevista do CICLO — o gate de fase lê exatamente o mesmo bloco de antes.
    """
    assert _cli(tmp_path, "ligar", PEDIDO_DO_CICLO).returncode == 0
    fechar_descoberta(tmp_path, PEDIDO_DO_CICLO)
    bloco_antigo = descoberta.ler(tmp_path)
    assert bloco_antigo["versao"] == descoberta.VERSAO_BLOCO

    saida = _cli(tmp_path, "fase", "ANALISE")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert descoberta.ler(tmp_path) == bloco_antigo, "o gate escreveu no bloco"
