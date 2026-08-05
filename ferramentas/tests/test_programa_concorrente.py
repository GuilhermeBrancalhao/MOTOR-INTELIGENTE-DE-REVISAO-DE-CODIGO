"""Colisão entre sessões no `.engine/programa.json` — a máquina de estado de cima.

O defeito, medido antes da correção
-----------------------------------
`ferramentas/estado.py` ganhou cadeado e mutador em 2026-08-04, e o `test_estado_
concorrente.py` fechou o *lost update* do CICLO. O PROGRAMA ficou de fora: os oito
sub-verbos que alteram `programa.json` liam o disco solto, decidiam, e gravavam — três
passos, cadeado nenhum —, apesar de `programa.atualizar` existir desde o primeiro dia,
relendo de dentro da seção crítica, sem um único chamador de produção.

O estrago não era teórico e não parava numa linha perdida. Duas sessões rodando
`programa aceite C1 falhou` e `programa aceite C2 ok` ao mesmo tempo faziam o REPROVADO
de C1 desaparecer sem erro nenhum; e um programa sem veredito vermelho no disco passa
em `pronto_para_aceite`, entra em ACEITE_SISTEMA e **conclui com um ciclo que falhou**.
É o modo de falhar que o próprio `programa.py` documenta como "o coração de A2".

Como aqui se prova
------------------
Três camadas, porque cada uma cai por um motivo diferente:

1. `test_seis_sessoes_...` — a corrida genérica sobre `programa.atualizar`, com atraso
   artificial na seção crítica. Cai se o mutador deixar de reler de dentro do cadeado.
2. `test_dois_aceites_...` — o cenário exato do laudo, com o veredito e a consequência
   (`pronto_para_aceite` continuar falso). Cai se o REPROVADO se perder.
3. `test_o_verbo_..._respeita_o_cadeado` — a camada que faltava, e a que o defeito
   habitava: os testes 1 e 2 já passariam com a CLI inteira gravando por fora, porque
   chamam a máquina diretamente. Aqui o cadeado é tomado pelo processo de teste e a CLI
   é executada de verdade: um sub-verbo que não peça o cadeado **consegue** gravar, e o
   teste o pega pelos bytes do arquivo.

Subprocessos de verdade, não threads: a exclusão mútua é entre processos (o Claude Code
roda cada hook e cada chamada da CLI como um processo novo), e threads sob o GIL
mascarariam a corrida.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

RAIZ_DO_MOTOR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ_DO_MOTOR))

from ferramentas import estado, programa  # noqa: E402

AGORA = "2026-08-05T10:00:00"

#: Quantos processos disputam o programa ao mesmo tempo.
CONCORRENTES = 6

#: Quanto tempo cada mutador segura a seção crítica. É este atraso que transforma a
#: corrida de "provável" em "certa": sem cadeado, os seis leem o mesmo programa antes de
#: qualquer um gravar, e cinco contribuições se perdem.
ATRASO_NA_SECAO_CRITICA = 0.05


def _programa_em_execucao(raiz: Path, quantos_ciclos: int = 3) -> dict:
    """Um programa aprovado, com N ciclos independentes, pronto para receber aceites."""
    ciclos = [
        {
            "id": f"C{n}",
            "objetivo": f"construir C{n}",
            "depende_de": [],
            "aceite": f"pytest tests/c{n} -q sai 0",
        }
        for n in range(1, quantos_ciclos + 1)
    ]
    dados = programa.novo(raiz, "sistema sob concorrência", AGORA)
    dados = programa.propor_plano(dados, ciclos, "o sistema sobe e responde")
    dados = programa.aprovar(dados, AGORA)
    programa.gravar(raiz, dados)
    return dados


# --------------------------------------------------------------------------
# 1. a corrida genérica sobre `programa.atualizar`
# --------------------------------------------------------------------------

_TRABALHADOR = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path

    sys.path.insert(0, {raiz!r})
    from ferramentas import programa

    raiz = Path(sys.argv[1])
    marca = sys.argv[2]
    partida = float(sys.argv[3])
    atraso = float(sys.argv[4])

    # Todos os processos comecam a disputar no MESMO instante de relogio de parede.
    # Sem esta barreira o custo de arranque do interpretador (dezenas de ms, e
    # diferente a cada processo) espalharia as tentativas e a corrida nao aconteceria
    # nem sem cadeado -- o teste passaria por acidente.
    while time.time() < partida:
        time.sleep(0.001)

    def mutar(atual):
        marcas = list(atual.get("marcas", []))
        time.sleep(atraso)          # a janela entre ler e gravar
        marcas.append(marca)
        atual["marcas"] = marcas
        return atual

    try:
        programa.atualizar(raiz, mutar, espera=30.0)
    except Exception as erro:
        print(f"{{type(erro).__name__}}: {{erro}}", file=sys.stderr)
        raise SystemExit(1)
    """
)

_TRABALHADOR_ACEITE = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path

    sys.path.insert(0, {raiz!r})
    from ferramentas import programa

    raiz = Path(sys.argv[1])
    ciclo = sys.argv[2]
    passou = sys.argv[3] == "ok"
    partida = float(sys.argv[4])
    atraso = float(sys.argv[5])

    while time.time() < partida:
        time.sleep(0.001)

    def mutar(atual):
        time.sleep(atraso)          # a janela entre ler e gravar
        return programa.registrar_aceite(atual, ciclo, passou=passou)

    try:
        programa.atualizar(raiz, mutar, espera=30.0)
    except Exception as erro:
        print(f"{{type(erro).__name__}}: {{erro}}", file=sys.stderr)
        raise SystemExit(1)
    """
)


def _disparar(nome: str, molde: str, raiz: Path, argumentos: list[list[str]]):
    script = raiz / nome
    script.write_text(molde.format(raiz=str(RAIZ_DO_MOTOR)), encoding="utf-8")

    partida = time.time() + 1.0
    processos = [
        subprocess.Popen(
            [sys.executable, str(script), str(raiz), *args, str(partida),
             str(ATRASO_NA_SECAO_CRITICA)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for args in argumentos
    ]
    resultados = []
    for processo in processos:
        saida, erro = processo.communicate(timeout=120)
        resultados.append(
            subprocess.CompletedProcess(processo.args, processo.returncode, saida, erro)
        )
    falhas = [r for r in resultados if r.returncode != 0]
    assert not falhas, "processo concorrente falhou: " + "; ".join(
        r.stderr.strip() for r in falhas
    )
    return resultados


def test_seis_sessoes_simultaneas_nao_perdem_escrita_no_programa(tmp_path):
    """Nenhuma contribuição some quando seis processos mutam o programa juntos.

    Mutação alvo: trocar `programa.atualizar` no trabalhador por carregar + mutar +
    gravar faz este teste reprovar com uma ou duas marcas em vez de seis.
    """
    _programa_em_execucao(tmp_path)

    _disparar(
        "_trabalhador_programa.py",
        _TRABALHADOR,
        tmp_path,
        [[f"m{n}"] for n in range(CONCORRENTES)],
    )

    final = json.loads(programa.caminho(tmp_path).read_text(encoding="utf-8"))
    assert sorted(final["marcas"]) == [f"m{n}" for n in range(CONCORRENTES)], (
        "escrita perdida: o programa final tem "
        f"{len(final['marcas'])} das {CONCORRENTES} contribuições"
    )


# --------------------------------------------------------------------------
# 2. o cenário do laudo: o REPROVADO que sumia
# --------------------------------------------------------------------------


def test_dois_aceites_concorrentes_nao_perdem_o_veredito_vermelho(tmp_path):
    """`aceite C1 falhou` e `aceite C2 ok` ao mesmo tempo: os dois vereditos sobrevivem.

    Mutação alvo: qualquer volta ao padrão ler-solto → gravar. Sem cadeado, as duas
    sessões leem o mesmo programa com C1 e C2 PENDENTE e a última a gravar apaga o
    veredito da outra — em metade das execuções o REPROVADO de C1 é o que some.

    A segunda asserção é a que dói: com o vermelho fora do disco, `pronto_para_aceite`
    fica verdadeiro e o programa pode CONCLUIR carregando um ciclo que falhou.
    """
    _programa_em_execucao(tmp_path, quantos_ciclos=2)

    _disparar(
        "_trabalhador_aceite.py",
        _TRABALHADOR_ACEITE,
        tmp_path,
        [["C1", "falhou"], ["C2", "ok"]],
    )

    final = programa.carregar(tmp_path)
    por_id = {c["id"]: c["status"] for c in final["ciclos"]}
    assert por_id == {"C1": "REPROVADO", "C2": "CONCLUIDO"}, (
        f"veredito perdido na corrida: {por_id}"
    )
    assert not programa.pronto_para_aceite(final), (
        "com o REPROVADO apagado o programa concluiria com um ciclo que falhou"
    )


def test_atualizar_do_programa_ve_o_disco_e_nao_o_que_quem_chamou_leu(tmp_path):
    """O coração da correção, sem subprocesso: o mutador recebe o programa RELIDO.

    Mutação alvo: fazer `programa.atualizar` receber o dicionário de quem chamou em vez
    de reler. O cadeado viraria decoração — serializaria as gravações e continuaria
    perdendo escrita.
    """
    _programa_em_execucao(tmp_path, quantos_ciclos=2)
    lido_antes = programa.carregar(tmp_path)

    # Outra sessão reprova C1 enquanto esta ainda segura o retrato velho.
    programa.gravar(tmp_path, programa.registrar_aceite(lido_antes, "C1", passou=False))

    vistos: list[str] = []

    def _mutar(atual):
        vistos.append({c["id"]: c["status"] for c in atual["ciclos"]}["C1"])
        return programa.registrar_aceite(atual, "C2", passou=True)

    programa.atualizar(tmp_path, _mutar)

    assert vistos == ["REPROVADO"], "o mutador viu um programa velho, não o do disco"
    final = {c["id"]: c["status"] for c in programa.carregar(tmp_path)["ciclos"]}
    assert final == {"C1": "REPROVADO", "C2": "CONCLUIDO"}


# --------------------------------------------------------------------------
# 3. a camada que faltava: os VERBOS pedem o cadeado
# --------------------------------------------------------------------------


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_DO_MOTOR / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _impressao_digital(raiz: Path) -> str:
    return hashlib.sha256(programa.caminho(raiz).read_bytes()).hexdigest()


#: Um comando por sub-verbo que ALTERA o programa. `status`, `proximo` e `relatorio`
#: ficam de fora de propósito: são leitura, e travar leitura deixaria quem esbarrou
#: numa recusa sem conseguir olhar o programa para entender por quê.
VERBOS_QUE_MUTAM = [
    ("aceite", ("programa", "aceite", "C1", "falhou")),
    ("reabrir", ("programa", "reabrir", "C1")),
    ("desviar", ("programa", "desviar", "stack-fora-do-plano", "precisa de Redis")),
    ("retomar", ("programa", "retomar")),
    ("sistema", ("programa", "sistema", "ok")),
    ("abortar", ("programa", "abortar")),
    ("aprovar", ("programa", "aprovar")),
]


@pytest.mark.parametrize("nome, comando", VERBOS_QUE_MUTAM, ids=[v[0] for v in VERBOS_QUE_MUTAM])
def test_o_verbo_do_programa_respeita_o_cadeado(tmp_path, nome, comando):
    """Com o cadeado do programa na mão de outra sessão, nenhum verbo grava.

    **É este o teste que teria pegado o defeito.** Os de corrida acima chamam a máquina
    de estado diretamente e passariam com a CLI inteira gravando por fora — foi
    exatamente essa a situação encontrada no aceite de sistema: mutador seguro escrito,
    coberto por teste, e nenhum verbo o chamando.

    Aqui o cadeado é tomado pelo processo de teste. Um sub-verbo que peça o cadeado
    espera, desiste e sai 1 dizendo que a pasta está ocupada; um que grave por fora
    **consegue**, e a impressão digital do arquivo muda. A asserção sobre os bytes é a
    que importa: uma implementação futura poderia até imprimir a recusa e gravar assim
    mesmo, e o código de saída sozinho não pegaria isso.

    Mutação alvo: devolver qualquer um destes sub-verbos ao padrão ler-solto → gravar.
    """
    _programa_em_execucao(tmp_path)
    antes = _impressao_digital(tmp_path)

    with estado.cadeado(
        tmp_path, nome=programa.NOME_CADEADO, idade_maxima=estado.IDADE_MAXIMA_CADEADO
    ):
        saida = _cli(tmp_path, *comando)

    assert _impressao_digital(tmp_path) == antes, (
        f"`programa {nome}` gravou com o cadeado do programa tomado por outra sessão"
    )
    assert saida.returncode == 1, saida.stdout + saida.stderr
    assert "ocupado" in saida.stdout, saida.stdout
    assert "Traceback" not in saida.stdout + saida.stderr


def test_o_verbo_plano_respeita_o_cadeado(tmp_path):
    """O sub-verbo `plano` também, e ele é o que mais tem a perder.

    `plano` grava a decomposição inteira e o aceite de sistema de uma vez. Gravando por
    fora do cadeado, ele sobrescreveria o programa que outra sessão acabou de mover — e
    o plano-mestre é justamente o que a porta P1 obriga o usuário a aprovar.

    Mutação alvo: mover a chamada do gate e a proposta do plano para fora do mutador.
    """
    from ferramentas.tests.apoio_descoberta import fechar_descoberta

    assert _cli(tmp_path, "ligar", "objetivo qualquer do ciclo").returncode == 0
    assert _cli(tmp_path, "programa", "sistema de teste").returncode == 0
    fechar_descoberta(tmp_path, "sistema de teste")
    arquivo = tmp_path / "plano.json"
    arquivo.write_text(
        json.dumps(
            {
                "aceite_de_sistema": "o sistema sobe e responde",
                "ciclos": [
                    {
                        "id": "C1",
                        "objetivo": "construir C1",
                        "depende_de": [],
                        "aceite": "pytest tests/c1 -q sai 0",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    antes = _impressao_digital(tmp_path)

    with estado.cadeado(
        tmp_path, nome=programa.NOME_CADEADO, idade_maxima=estado.IDADE_MAXIMA_CADEADO
    ):
        saida = _cli(tmp_path, "programa", "plano", str(arquivo))

    assert _impressao_digital(tmp_path) == antes, (
        "`programa plano` gravou a decomposição com o cadeado tomado"
    )
    assert saida.returncode == 1
    assert "ocupado" in saida.stdout, saida.stdout


def test_verbos_de_leitura_nao_travam_com_o_cadeado_tomado(tmp_path):
    """O par obrigatório: `status` e `relatorio` continuam respondendo.

    Mutação alvo: pôr o cadeado no `_verbo_programa` inteiro. Um motor que trava a
    leitura quando outra sessão está gravando deixa o usuário sem o único comando que
    explicaria o que está acontecendo — e ensina a matar o cadeado à mão, que é pior do
    que a corrida que ele previne.
    """
    _programa_em_execucao(tmp_path)

    with estado.cadeado(
        tmp_path, nome=programa.NOME_CADEADO, idade_maxima=estado.IDADE_MAXIMA_CADEADO
    ):
        assert _cli(tmp_path, "programa", "status").returncode == 0
        assert _cli(tmp_path, "programa", "relatorio").returncode == 0
