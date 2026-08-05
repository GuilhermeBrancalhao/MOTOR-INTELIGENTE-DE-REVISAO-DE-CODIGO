"""O critério de aceite de cada ciclo passa a declarar COMANDO, não só prosa.

`validar_plano` já exigia um `aceite` não-vazio — e aceitava qualquer frase. Frase não
se executa: o `executor.py` entregue no P2C1 sabe rodar comando e ler código de saída, e
não sabe rodar prosa. Enquanto o plano-mestre trouxesse só a frase, o veredito de cada
ciclo continuava saindo de alguém digitar `programa aceite C1 ok`, que é exatamente a
opinião do modelo que o programa 2 existe para eliminar.

Este arquivo cobra quatro coisas, e cada docstring nomeia a mutação que a derruba:

1. **plano NOVO sem comando é recusado** — ausente, vazio, tipo errado, e pela CLI de
   verdade, com código de saída 1 e sem tocar no `programa.json`;
2. **plano NOVO com comando passa** — o par obrigatório de todo teste de recusa, sem o
   qual "recusar sempre" passaria em tudo;
3. **plano VELHO continua carregando** — `programa.json` gravado antes deste ciclo não
   tem o campo, e nada que apenas *lê* pode quebrar. A fronteira é estrutural: a
   exigência vive só no caminho de escrita;
4. **a decisão de NÃO classificar risco aqui** — comando travado atravessa
   `validar_plano` de propósito, e é o `executor` que o recusa sem executar. O teste
   prova que a falha continua fechada onde importa.
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

from ferramentas import executor, programa  # noqa: E402
from ferramentas.tests.apoio_descoberta import fechar_descoberta  # noqa: E402

AGORA = "2026-08-05T10:00:00"
OBJETIVO = "construir um sistema novo que soma dois numeros"


def _ciclo(cid: str, deps: tuple[str, ...] = (), **campos) -> dict:
    """Um ciclo COMPLETO no formato novo. `campos` sobrescreve para o caso do teste."""
    base = {
        "id": cid,
        "objetivo": f"construir {cid}",
        "depende_de": list(deps),
        "aceite": f"a suíte de {cid} passa inteira",
        "comando_de_aceite": f"python -m pytest tests/{cid.lower()} -q",
    }
    base.update(campos)
    return base


def _ciclo_antigo(cid: str, deps: tuple[str, ...] = (), **campos) -> dict:
    """Um ciclo no formato ANTERIOR a este ciclo do motor: prosa e nada mais.

    Sem `comando_de_aceite` **e sem a chave**, que é como os arquivos gravados até aqui
    estão no disco. Um fixture que pusesse a chave com `""` testaria outra coisa.
    """
    ciclo = _ciclo(cid, deps, **campos)
    ciclo.pop("comando_de_aceite")
    return ciclo


def _programa_antigo_em_disco(raiz: Path, *, estado: str = "EXECUCAO") -> dict:
    """Escreve à mão um `programa.json` no formato velho — sem passar por `propor_plano`.

    À mão de propósito: passar pela API atual gravaria o campo novo e o teste deixaria de
    exercitar o arquivo legado, que é justamente o que não pode quebrar.
    """
    dados = {
        "versao": 1,
        "programa": "2026-07-01-1",
        "objetivo": "programa gravado antes do aceite executável",
        "estado": estado,
        "iniciado_em": "2026-07-01T09:00:00",
        "aceite_de_sistema": "o sistema sobe e responde",
        "ciclos": [
            {**_ciclo_antigo("C1"), "status": "CONCLUIDO", "ciclo_do_estado": "2026-07-01-a"},
            {**_ciclo_antigo("C2", ("C1",)), "status": "PENDENTE", "ciclo_do_estado": None},
        ],
        "desvio": None,
        "historico": ["2026-07-01-1"],
        "aprovado_em": "2026-07-01T09:30:00",
    }
    programa.gravar(raiz, dados)
    return dados


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


def _preparar_para_o_plano(raiz: Path, plano: dict) -> Path:
    """Ciclo ligado, programa aberto, descoberta fechada e o plano escrito em arquivo.

    A descoberta é fechada porque o gate de `CONCEPCAO -> PLANO_MESTRE` vem ANTES da
    validação do plano: sem fechá-la, todo teste deste arquivo mediria a recusa do gate
    da descoberta e nunca chegaria a exercitar `validar_plano`.
    """
    assert _cli(raiz, "ligar", OBJETIVO).returncode == 0
    assert _cli(raiz, "programa", OBJETIVO).returncode == 0
    fechar_descoberta(raiz, OBJETIVO)
    arquivo = raiz / "plano.json"
    arquivo.write_text(json.dumps(plano, ensure_ascii=False), encoding="utf-8")
    return arquivo


# ---------------------------------------------------------------------------
# 1. plano novo sem comando é recusado
# ---------------------------------------------------------------------------


def test_ciclo_sem_comando_de_aceite_e_recusado():
    """Mutação que derruba: apagar a checagem de `comando_de_aceite` em `validar_plano`.

    É o teste central do ciclo. Sem ele o plano volta a passar com prosa pura, e o
    veredito de cada ciclo volta a depender de alguém digitar `aceite C1 ok`.
    """
    with pytest.raises(programa.PlanoInvalido, match="sem comando executável"):
        programa.validar_plano([_ciclo_antigo("C1")])


def test_comando_de_aceite_vazio_e_recusado():
    """Mutação que derruba: checar a PRESENÇA da chave (`in ciclo`) em vez do conteúdo.

    `"comando_de_aceite": "   "` satisfaz "a chave existe" e não roda nada. É o mesmo
    furo que a checagem do `aceite` já fechava com `.strip()`, e ele voltaria inteiro se
    a checagem nova fosse escrita com menos cuidado que a vizinha.
    """
    with pytest.raises(programa.PlanoInvalido, match="sem comando executável"):
        programa.validar_plano([_ciclo("C1", comando_de_aceite="   \n  ")])


def test_comando_de_aceite_de_tipo_errado_e_recusado_sem_estourar():
    """Mutação que derruba: `(c.get(campo) or "").strip()` direto, sem checar o tipo.

    Uma lista no JSON não é vazia, então passaria pela validação — e só apareceria lá na
    frente, quando `executor.executar` recebesse algo que não é comando. Escrito sem a
    checagem de tipo, o mesmo campo estoura `AttributeError` dentro da CLI, que é
    traceback no terminal do usuário: os dois desfechos são erros, e nenhum é este.
    """
    for valor in ([_ciclo("C1")["comando_de_aceite"]], {"cmd": "pytest"}, 7):
        with pytest.raises(programa.PlanoInvalido, match="precisa ser texto"):
            programa.validar_plano([_ciclo("C1", comando_de_aceite=valor)])


def test_a_prosa_do_aceite_continua_obrigatoria_ao_lado_do_comando():
    """Mutação que derruba: trocar a exigência do `aceite` pela do comando, em vez de somar.

    Os dois campos são dois porque dizem coisas diferentes: a prosa é a afirmação
    falsificável que o humano lê na porta P1, o comando é como ela se verifica. Só o
    comando deixaria o revisor da porta sem nada para julgar além de uma linha de shell.
    """
    with pytest.raises(programa.PlanoInvalido, match="sem critério de aceite"):
        programa.validar_plano([_ciclo("C1", aceite="   ")])


def test_a_recusa_nomeia_o_ciclo_e_o_campo():
    """Mutação que derruba: recusar com "plano inválido" genérico.

    Num plano de 20 ciclos, quem lê a recusa precisa saber QUAL ciclo e QUAL campo — sem
    isso a mensagem manda reler o JSON inteiro à mão, e o custo cai sobre quem já estava
    fazendo a coisa certa.
    """
    with pytest.raises(programa.PlanoInvalido) as erro:
        programa.validar_plano([_ciclo("C1"), _ciclo_antigo("C7-RELATORIO")])

    texto = str(erro.value)
    assert "C7-RELATORIO" in texto
    assert programa.CAMPO_COMANDO in texto


def test_a_recusa_do_comando_nao_apaga_as_outras_validacoes():
    """Mutação que derruba: pôr a checagem nova ANTES do DAG e sair na primeira falha.

    Um plano com dependência cíclica **e** sem comando tem de continuar sendo reportado
    como cíclico: dependência cíclica é o defeito mais caro de diagnosticar depois, e
    trocar essa mensagem pela do campo faltante manda o autor consertar o campo e bater
    de novo no mesmo muro.
    """
    ciclico = [_ciclo("C1", ("C2",)), _ciclo("C2", ("C1",))]
    with pytest.raises(programa.PlanoInvalido, match="cíclica"):
        programa.validar_plano(ciclico)


# ---------------------------------------------------------------------------
# 2. plano novo COM comando passa — o par obrigatório
# ---------------------------------------------------------------------------


def test_plano_com_comando_em_todos_os_ciclos_passa():
    """Mutação que derruba: uma checagem que recusa sempre (a mais fácil de não perceber).

    Recusar sempre passa em todos os testes de recusa acima e trava qualquer programa em
    CONCEPCAO para sempre. Todo gate precisa do teste que prova que ele abre.
    """
    programa.validar_plano([_ciclo("C1"), _ciclo("C2", ("C1",))])


def test_o_comando_declarado_e_gravado_no_ciclo(tmp_path):
    """Mutação que derruba: validar o campo e não copiá-lo em `_reaproveitar`.

    Um plano que passa na validação e grava o ciclo sem o comando é o pior desfecho
    possível: o `programa.json` fica com aparência de novo e o verbo que for rodar o
    aceite (P2C3) não encontra o que rodar.
    """
    dados = programa.novo(tmp_path, "sistema", AGORA)
    dados = programa.propor_plano(dados, [_ciclo("C1")], "o sistema sobe e responde")

    assert programa.comando_de_aceite(dados["ciclos"][0]) == (
        "python -m pytest tests/c1 -q"
    )


# ---------------------------------------------------------------------------
# 3. plano velho continua carregando — a fronteira é o caminho de ESCRITA
# ---------------------------------------------------------------------------


def test_programa_gravado_antes_do_comando_continua_legivel(tmp_path):
    """Mutação que derruba: transformar `aceite` em objeto `{descricao, comando}`.

    É o motivo de o campo ser NOVO e não uma reforma do `aceite`. Com o objeto, todo
    leitor que faz `c["aceite"]` (o `programa proximo` e o `_prog_imprimir` da CLI, entre
    outros) quebraria em cima de um arquivo que ninguém tocou — e `VERSAO` continua 1,
    sem migração escrita.
    """
    _programa_antigo_em_disco(tmp_path)

    relido = programa.carregar_estrito(tmp_path)

    assert relido is not None
    assert isinstance(relido["ciclos"][0]["aceite"], str)
    assert programa.resumo(relido)["concluidos"] == 1
    assert programa.proximo_elegivel(relido)["id"] == "C2"


def test_programa_antigo_percorre_o_ciclo_de_vida_inteiro(tmp_path):
    """Mutação que derruba: chamar `validar_plano` em qualquer caminho de LEITURA.

    A retrocompatibilidade não vem de uma exceção escrita para o arquivo velho; vem de a
    exigência morar só na escrita. Se alguém revalidasse o plano ao carregar, ao resumir
    ou ao registrar aceite — uma "checagem de sanidade" plausível —, todo programa em
    andamento pararia de funcionar no meio, sem ter feito nada de errado.
    """
    _programa_antigo_em_disco(tmp_path)
    dados = programa.carregar_estrito(tmp_path)

    dados = programa.iniciar_ciclo(dados, "C2", "2026-07-01-b")
    dados = programa.registrar_aceite(dados, "C2", passou=True)
    dados = programa.entrar_em_aceite(dados)
    dados = programa.concluir(dados, passou=True, agora=AGORA)

    assert dados["estado"] == "CONCLUIDO"


def test_comando_de_aceite_de_ciclo_antigo_e_vazio_e_nunca_estoura():
    """Mutação que derruba: ler `ciclo["comando_de_aceite"]` direto no lugar do acessor.

    `KeyError` em cima de um ciclo antigo é o modo de falhar que transforma "o arquivo
    continua legível" em mentira. E o valor devolvido tem de ser `""` — que é o que
    `executor.executar` já recusa com REPROVADO fundamentado, nunca aprovando por
    omissão.
    """
    assert programa.comando_de_aceite(_ciclo_antigo("C1")) == ""
    assert programa.comando_de_aceite({}) == ""
    assert programa.comando_de_aceite({programa.CAMPO_COMANDO: None}) == ""
    assert programa.comando_de_aceite({programa.CAMPO_COMANDO: ["pytest"]}) == ""
    assert programa.comando_de_aceite({programa.CAMPO_COMANDO: "  pytest -q  "}) == (
        "pytest -q"
    )


def test_validar_plano_so_e_chamada_no_caminho_de_escrita():
    """Mutação que derruba: acrescentar `validar_plano(...)` a `carregar`, `resumo` ou
    `proximo_elegivel`.

    A fronteira entre "arquivo velho carrega" e "plano novo é recusado" não está escrita
    em lugar nenhum como regra — ela É o fato de a validação só existir na escrita. Trava
    textual, pela mesma tática do C4 e do gate do plano: propriedade que ninguém enuncia
    é propriedade que alguém apaga sem perceber.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "programa.py").read_text(encoding="utf-8")
    chamadas = [
        linha.strip()
        for linha in fonte.splitlines()
        if "validar_plano(" in linha and not linha.lstrip().startswith(("#", "def "))
    ]
    assert chamadas == ["validar_plano(ciclos)"], (
        f"`validar_plano` passou a ser chamada fora de `propor_plano`: {chamadas}"
    )


def test_programa_antigo_e_lido_pela_cli_sem_quebrar(tmp_path):
    """Mutação que derruba: qualquer leitura do campo novo por indexação na CLI.

    `programa status` e `programa proximo` são o que alguém roda ao voltar a um programa
    em andamento. Quebrá-los em cima de um arquivo legado deixa o usuário sem conseguir
    nem olhar o programa para entender o que aconteceu — a mesma razão pela qual o gate
    da descoberta não trava os sub-verbos de leitura.
    """
    _programa_antigo_em_disco(tmp_path)

    status = _cli(tmp_path, "programa", "status")
    proximo = _cli(tmp_path, "programa", "proximo")

    assert status.returncode == 0, status.stdout + status.stderr
    assert proximo.returncode == 0, proximo.stdout + proximo.stderr
    assert "Traceback" not in status.stdout + status.stderr
    assert "Traceback" not in proximo.stdout + proximo.stderr
    assert "C2" in proximo.stdout


# ---------------------------------------------------------------------------
# a CLI, de ponta a ponta: o critério de aceite deste ciclo, rodado literalmente
# ---------------------------------------------------------------------------


def test_cli_recusa_plano_cujo_aceite_nao_traz_comando(tmp_path):
    """Mutação que derruba: recusar imprimindo e devolvendo 0, ou recusar DEPOIS de gravar.

    Código de saída é o que a skill lê para saber se o plano-mestre foi registrado; uma
    recusa que sai 0 é indistinguível de sucesso para quem automatiza, e o passo seguinte
    seria `programa aprovar`. E a impressão digital cobra a outra metade: recusar depois
    de `propor_plano` deixaria a decomposição gravada atrás de um estado que diz
    CONCEPCAO.
    """
    arquivo = _preparar_para_o_plano(
        tmp_path,
        {
            "aceite_de_sistema": "o sistema soma 2+2 e responde 4",
            "ciclos": [_ciclo_antigo("C1"), _ciclo_antigo("C2", ("C1",))],
        },
    )
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "sem comando executável" in saida.stdout
    assert "Traceback" not in saida.stdout + saida.stderr
    assert _impressao_digital(tmp_path) == antes, "a recusa gravou no programa"
    assert programa.carregar(tmp_path)["estado"] == "CONCEPCAO"


def test_cli_aceita_plano_com_comando(tmp_path):
    """Mutação que derruba: a checagem recusar sempre, pela CLI de verdade.

    O par obrigatório do teste acima, medido no mesmo caminho: mesmo plano, mesma
    entrevista fechada, só o campo a mais. Sai 0, transiciona para PLANO_MESTRE e grava
    o comando de cada ciclo.
    """
    arquivo = _preparar_para_o_plano(
        tmp_path,
        {
            "aceite_de_sistema": "o sistema soma 2+2 e responde 4",
            "ciclos": [_ciclo("C1"), _ciclo("C2", ("C1",))],
        },
    )

    saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert saida.returncode == 0, saida.stdout + saida.stderr
    gravado = programa.carregar(tmp_path)
    assert gravado["estado"] == "PLANO_MESTRE"
    assert [programa.comando_de_aceite(c) for c in gravado["ciclos"]] == [
        "python -m pytest tests/c1 -q",
        "python -m pytest tests/c2 -q",
    ]


def test_cli_mostra_o_comando_do_proximo_ciclo(tmp_path):
    """Mutação que derruba: `programa proximo` continuar imprimindo só a prosa.

    Quem conduz a EXECUCAO pergunta ao motor qual é o próximo ciclo e o que prova que ele
    passou. Guardar o comando no arquivo e não mostrá-lo devolve a decisão de "o que
    rodar" para quem lê a frase — que é de onde estamos saindo.
    """
    arquivo = _preparar_para_o_plano(
        tmp_path,
        {
            "aceite_de_sistema": "o sistema soma 2+2 e responde 4",
            "ciclos": [_ciclo("C1")],
        },
    )
    assert _cli(tmp_path, "programa", "plano", str(arquivo)).returncode == 0
    assert _cli(tmp_path, "programa", "aprovar").returncode == 0

    saida = _cli(tmp_path, "programa", "proximo")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert "python -m pytest tests/c1 -q" in saida.stdout


# ---------------------------------------------------------------------------
# 4. replanejamento: o critério agora são DOIS campos
# ---------------------------------------------------------------------------


def _ate_desvio(tmp_path, ciclos) -> dict:
    dados = programa.novo(tmp_path, "sistema", AGORA)
    dados = programa.propor_plano(dados, ciclos, "o sistema sobe e responde")
    dados = programa.aprovar(dados, AGORA)
    dados = programa.registrar_aceite(dados, "C1", passou=True)
    return programa.desviar(dados, "stack-fora-do-plano", "o plano previa SQLite")


def test_replanejar_zera_o_ciclo_cujo_COMANDO_mudou(tmp_path):
    """Mutação que derruba: comparar o critério só pela prosa do `aceite`.

    Mesma frase, comando diferente, é outra verificação — e o CONCLUIDO antigo é prova
    sobre um comando que não está mais no plano. Preservá-lo carimbaria como verificado
    algo que ninguém rodou, que é o defeito dos "42 volumes entregues" escrito no campo
    novo.
    """
    dados = _ate_desvio(tmp_path, [_ciclo("C1"), _ciclo("C2", ("C1",))])
    plano_novo = [
        _ciclo("C1", comando_de_aceite="python -m pytest tests/c1 -q --strict-markers"),
        _ciclo("C2", ("C1",)),
    ]

    novo = programa.propor_plano(dados, plano_novo, "o sistema sobe e responde")

    assert novo["ciclos"][0]["status"] == "PENDENTE"
    assert novo["ciclos"][0]["ciclo_do_estado"] is None


def test_replanejar_preserva_quando_a_prosa_e_o_comando_seguem_iguais(tmp_path):
    """Mutação que derruba: zerar sempre que o campo novo entrar na comparação.

    O par obrigatório do teste acima. Um critério que muda "sempre" desfaz trabalho aceito
    a cada replanejamento — e replanejar não desfaz trabalho aceito.
    """
    ciclos = [_ciclo("C1"), _ciclo("C2", ("C1",))]
    dados = _ate_desvio(tmp_path, ciclos)

    novo = programa.propor_plano(dados, ciclos, "o sistema sobe e responde")

    assert novo["ciclos"][0]["status"] == "CONCLUIDO"


def test_migrar_plano_antigo_devolve_os_vereditos_digitados_para_pendente(tmp_path):
    """Mutação que derruba: perdoar o ciclo antigo (`sem comando OU comando igual`).

    É a consequência deliberada da migração, e a mais tentadora de suavizar: o CONCLUIDO
    do arquivo velho foi digitado, e o critério novo exige execução. Herdá-lo seria
    carimbar como verificado exatamente o que nunca foi. O preço é rodar o comando uma
    vez — se o trabalho estava pronto, ele sai 0 e o ciclo fecha de novo.
    """
    dados = _programa_antigo_em_disco(tmp_path)
    dados = programa.desviar(dados, "aceite-inalcancavel", "o aceite era prosa")
    assert dados["ciclos"][0]["status"] == "CONCLUIDO"

    novo = programa.propor_plano(
        dados, [_ciclo("C1"), _ciclo("C2", ("C1",))], "o sistema sobe e responde"
    )

    assert novo["ciclos"][0]["status"] == "PENDENTE"
    assert programa.comando_de_aceite(novo["ciclos"][0])


# ---------------------------------------------------------------------------
# 5. a decisão de NÃO classificar risco no plano
# ---------------------------------------------------------------------------


def test_validar_plano_nao_classifica_o_risco_do_comando():
    """Mutação que derruba: chamar `risco.classificar` dentro de `validar_plano`.

    Decisão registrada e testada, não omissão. O veredito de risco depende de `raiz` e da
    configuração efetiva do projeto — é propriedade do momento da execução, não do plano
    — e trazê-lo para cá custaria a pureza deste módulo ou viraria um argumento opcional,
    que é gate que se pode omitir. O teste fixa a decisão nos dois sentidos: aqui o
    comando travado PASSA na validação, e no teste seguinte ele é recusado sem executar.
    """
    programa.validar_plano([_ciclo("C1", comando_de_aceite="del marcador.txt")])


def test_o_comando_travado_continua_recusado_pelo_executor(tmp_path):
    """Mutação que derruba: tirar a classificação de risco do `executor` "porque o plano
    já valida".

    É a outra metade da decisão acima, e a que impede que ela vire um furo: a falha
    continua FECHADA no ponto em que importa. A prova é o efeito colateral — o arquivo
    sobrevive, então o comando não rodou.
    """
    alvo = tmp_path / "marcador.txt"
    alvo.write_text("nao me apague", encoding="utf-8")

    veredito = executor.executar(
        "del marcador.txt",
        raiz=tmp_path,
        timeout_s=60,
        config_efetiva={"padroes_segredo": [], "travado_extra": []},
        registrar_na_trilha=False,
    )

    assert alvo.is_file(), "o comando travado executou mesmo assim"
    assert veredito.resultado == executor.REPROVADO
    assert veredito.codigo_saida is None


def test_programa_nao_importa_risco_nem_conhece_raiz_na_validacao():
    """Mutação que derruba: `from . import risco` no topo de `programa.py`.

    A pureza deste módulo é a propriedade da qual a suíte inteira depende (há teste
    textual guardando `propor_plano`), e é ela que permite ao gate rodar com o cadeado na
    mão — cadeado que não é reentrante. O import é o primeiro passo de quem vai
    classificar risco no plano, e é onde a trava fica mais barata.

    Lido pela árvore sintática, e não por busca de texto: o docstring de `validar_plano`
    **explica** por que não se classifica risco ali, e cita `risco.classificar` ao fazê-lo.
    Uma trava textual reprovaria a própria justificativa da decisão que ela protege.
    """
    import ast

    fonte = (RAIZ_PLUGIN / "ferramentas" / "programa.py").read_text(encoding="utf-8")
    importados: set[str] = set()
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.Import):
            importados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom):
            importados.update(a.name for a in no.names)
            if no.module:
                importados.add(no.module.split(".")[0])

    assert not importados & {"risco", "executor"}, (
        f"`programa.py` passou a importar {importados & {'risco', 'executor'}}: a "
        "validação do plano voltou a tentar decidir risco/execução, e o módulo puro "
        "sobre dicionário passou a precisar de `raiz` e da configuração do projeto"
    )
