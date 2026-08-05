"""Testes da camada de PROGRAMA (Fase 4).

Cobrem os oito casos de aceite da spec `docs/specs/2026-08-05-engine-fase-4-programa.md`.
Cada teste nomeia no docstring a mutação que deve derrubá-lo — a mesma convenção que
o acervo estabelece no volume 31-TESTING. Um teste que nunca ficou vermelho é uma
hipótese, não um teste.
"""

import json

import pytest

from ferramentas import programa

AGORA = "2026-08-05T10:00:00"


def _plano(*ids_e_deps):
    """Monta uma decomposição válida a partir de (id, [deps]).

    Válida quer dizer, desde o aceite executável: prosa **e** comando. Um fixture que
    ficasse só na prosa faria toda esta suíte medir a recusa errada — os testes de DAG
    passariam pelo `PlanoInvalido` do comando ausente, e o detector de ciclo poderia ser
    apagado sem ninguém notar.
    """
    return [
        {
            "id": cid,
            "objetivo": f"construir {cid}",
            "depende_de": list(deps),
            "aceite": f"pytest tests/{cid.lower()} -q sai 0",
            "comando_de_aceite": f"python -m pytest tests/{cid.lower()} -q",
        }
        for cid, deps in ids_e_deps
    ]


def _ate_execucao(tmp_path, ciclos=None):
    """Atalho: cria o programa, propõe o plano e atravessa a porta."""
    dados = programa.novo(tmp_path, "sistema de teste", AGORA)
    dados = programa.propor_plano(
        dados, ciclos or _plano(("C1", []), ("C2", ["C1"]), ("C3", ["C2"])), "o sistema sobe e responde"
    )
    return programa.aprovar(dados, AGORA)


# ---------------------------------------------------------------------------
# A1 — encadeamento
# ---------------------------------------------------------------------------


def test_encadeia_tres_ciclos_em_ordem_de_dependencia():
    """A1. Mutação alvo: `proximo_elegivel` ignorar `depende_de` devolveria C2 antes de C1."""
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "PENDENTE"},
            {"id": "C2", "depende_de": ["C1"], "status": "PENDENTE"},
            {"id": "C3", "depende_de": ["C2"], "status": "PENDENTE"},
        ],
    }
    assert programa.proximo_elegivel(dados)["id"] == "C1"

    dados = programa.registrar_aceite(dados, "C1", passou=True)
    assert programa.proximo_elegivel(dados)["id"] == "C2"

    dados = programa.registrar_aceite(dados, "C2", passou=True)
    assert programa.proximo_elegivel(dados)["id"] == "C3"

    dados = programa.registrar_aceite(dados, "C3", passou=True)
    assert programa.proximo_elegivel(dados) is None


def test_ciclos_independentes_saem_em_ordem_estavel_do_plano():
    """A1. Mutação alvo: escolher o "melhor" elegível tornaria duas execuções divergentes."""
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "A", "depende_de": [], "status": "PENDENTE"},
            {"id": "B", "depende_de": [], "status": "PENDENTE"},
        ],
    }
    assert programa.proximo_elegivel(dados)["id"] == "A"


# ---------------------------------------------------------------------------
# A2 — aceite vermelho não avança
# ---------------------------------------------------------------------------


def test_ciclo_reprovado_nao_libera_dependentes():
    """A2. Mutação alvo: `registrar_aceite` marcar CONCLUIDO sempre faria C2 ligar com C1 vermelho."""
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "PENDENTE"},
            {"id": "C2", "depende_de": ["C1"], "status": "PENDENTE"},
        ],
    }
    dados = programa.registrar_aceite(dados, "C1", passou=False)

    assert dados["ciclos"][0]["status"] == "REPROVADO"
    assert programa.proximo_elegivel(dados) is None, (
        "C2 não pode ficar elegível enquanto C1 está reprovado"
    )


def test_dependente_nao_pode_ser_dado_por_concluido_com_dependencia_vermelha():
    """A2, no ponto que decide. Mutação alvo: tirar a guarda de `registrar_aceite`.

    O achado do P2C5: o teste acima cobrava A2 só pela via consultiva
    (`proximo_elegivel`), e por isso passava mesmo com a via que DECIDE aberta —
    `registrar_aceite(dados, "C2", passou=True)` carimbava CONCLUIDO com C1 vermelho.
    A2 diz "aceite vermelho não avança"; sem esta guarda, ele não avançava só para quem
    pedia licença.
    """
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "PENDENTE"},
            {"id": "C2", "depende_de": ["C1"], "status": "PENDENTE"},
        ],
    }
    dados = programa.registrar_aceite(dados, "C1", passou=False)

    with pytest.raises(programa.DependenciaNaoConcluida):
        programa.registrar_aceite(dados, "C2", passou=True)

    assert dados["ciclos"][1]["status"] == "PENDENTE"


def test_dependente_tambem_e_barrado_com_a_dependencia_apenas_pendente():
    """Mutação alvo: olhar só para REPROVADO em vez de exigir CONCLUIDO.

    Dependência que ainda nem foi tentada é tão pouco satisfeita quanto uma que falhou.
    Uma guarda escrita como `status == "REPROVADO"` deixaria passar a ordem invertida,
    que é o caso mais comum: fechar C2 antes de alguém ter olhado para C1.
    """
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "PENDENTE"},
            {"id": "C2", "depende_de": ["C1"], "status": "PENDENTE"},
        ],
    }
    with pytest.raises(programa.DependenciaNaoConcluida):
        programa.registrar_aceite(dados, "C2", passou=True)


def test_reprovar_um_dependente_continua_permitido():
    """Mutação alvo: barrar os dois vereditos, e não só o verde.

    Um vermelho no dependente não afirma nada sobre pré-requisito satisfeito — é só o
    fato de que o teste dele falhou. Barrá-lo obrigaria a inventar um terceiro estado
    para "rodou e falhou, mas não podia rodar" sem ganhar informação nenhuma.
    """
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "PENDENTE"},
            {"id": "C2", "depende_de": ["C1"], "status": "PENDENTE"},
        ],
    }
    dados = programa.registrar_aceite(dados, "C2", passou=False)

    assert dados["ciclos"][1]["status"] == "REPROVADO"


def test_dependencias_pendentes_nomeia_quais_faltam():
    """Mutação alvo: devolver booleano em vez da lista.

    Num plano de vinte ciclos, "há dependência aberta" manda a pessoa procurar à mão o
    que a máquina já sabe — e a recusa da CLI imprime justamente esta lista.
    """
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [
            {"id": "C1", "depende_de": [], "status": "CONCLUIDO"},
            {"id": "C2", "depende_de": [], "status": "REPROVADO"},
            {"id": "C3", "depende_de": ["C1", "C2"], "status": "PENDENTE"},
        ],
    }
    assert programa.dependencias_pendentes(dados, "C1") == []
    assert programa.dependencias_pendentes(dados, "C3") == ["C2"]


def test_ciclo_reprovado_pode_ser_reaberto_e_volta_a_ser_elegivel():
    """A2. Mutação alvo: `reabrir` aceitar qualquer status permitiria reabrir um CONCLUIDO."""
    dados = {
        "estado": "EXECUCAO",
        "ciclos": [{"id": "C1", "depende_de": [], "status": "PENDENTE"}],
    }
    dados = programa.registrar_aceite(dados, "C1", passou=False)
    dados = programa.reabrir(dados, "C1")

    assert programa.proximo_elegivel(dados)["id"] == "C1"

    dados = programa.registrar_aceite(dados, "C1", passou=True)
    with pytest.raises(programa.TransicaoInvalida):
        programa.reabrir(dados, "C1")


# ---------------------------------------------------------------------------
# A3 — DAG validado na porta
# ---------------------------------------------------------------------------


def test_dependencia_ciclica_e_recusada_no_plano():
    """A3. Mutação alvo: remover `_recusar_ciclo_no_grafo` trava a execução sem mensagem."""
    with pytest.raises(programa.PlanoInvalido, match="cíclica"):
        programa.validar_plano(_plano(("C1", ["C2"]), ("C2", ["C1"])))


def test_autodependencia_e_recusada():
    """A3. Mutação alvo: tratar só ciclos de comprimento ≥2 deixaria passar C1 -> C1."""
    with pytest.raises(programa.PlanoInvalido, match="cíclica"):
        programa.validar_plano(_plano(("C1", ["C1"])))


def test_dependencia_para_id_inexistente_e_recusada():
    """A3. Mutação alvo: sem esta checagem o ciclo nunca fica elegível e o programa trava mudo."""
    with pytest.raises(programa.PlanoInvalido, match="não existe no plano"):
        programa.validar_plano(_plano(("C1", ["FANTASMA"])))


def test_id_repetido_e_recusado():
    """A3. Mutação alvo: sem isso o encadeamento não sabe qual ciclo marcar como concluído."""
    with pytest.raises(programa.PlanoInvalido, match="repetido"):
        programa.validar_plano(_plano(("C1", []), ("C1", [])))


def test_plano_vazio_e_recusado():
    """A3. Mutação alvo: um programa sem ciclos "concluiria" sem construir nada."""
    with pytest.raises(programa.PlanoInvalido, match="nenhum ciclo"):
        programa.validar_plano([])


def test_ciclo_sem_aceite_e_recusado():
    """A3/P5. Mutação alvo: sem aceite, "concluído" vira opinião do modelo."""
    ruim = _plano(("C1", []))
    ruim[0]["aceite"] = "   "
    with pytest.raises(programa.PlanoInvalido, match="sem critério de aceite"):
        programa.validar_plano(ruim)


def test_dag_valido_passa():
    """A3. Mutação alvo: um detector de ciclo agressivo demais recusaria diamante legítimo."""
    programa.validar_plano(
        _plano(("A", []), ("B", ["A"]), ("C", ["A"]), ("D", ["B", "C"]))
    )


# ---------------------------------------------------------------------------
# A4 — a porta P1
# ---------------------------------------------------------------------------


def test_execucao_nao_comeca_sem_aprovar(tmp_path):
    """A4. Mutação alvo: `propor_plano` já ir para EXECUCAO anula a porta única."""
    dados = programa.novo(tmp_path, "sistema", AGORA)
    dados = programa.propor_plano(dados, _plano(("C1", [])), "sobe e responde")

    assert dados["estado"] == "PLANO_MESTRE"
    with pytest.raises(programa.PortaNaoAtravessada):
        programa.iniciar_ciclo(dados, "C1", "2026-08-05-1")


def test_aprovar_atravessa_a_porta(tmp_path):
    """A4. Mutação alvo: `aprovar` não mudar o estado deixaria o programa preso na porta."""
    dados = _ate_execucao(tmp_path)
    assert dados["estado"] == "EXECUCAO"
    dados = programa.iniciar_ciclo(dados, "C1", "2026-08-05-1")
    assert dados["ciclos"][0]["status"] == "ATIVO"
    assert dados["ciclos"][0]["ciclo_do_estado"] == "2026-08-05-1"


def test_aprovar_fora_de_plano_mestre_e_recusado(tmp_path):
    """A4. Mutação alvo: aprovar de qualquer estado permitiria pular a concepção."""
    dados = programa.novo(tmp_path, "sistema", AGORA)
    with pytest.raises(programa.TransicaoInvalida):
        programa.aprovar(dados, AGORA)


def test_programa_sem_aceite_de_sistema_e_recusado(tmp_path):
    """A7/P4. Mutação alvo: aceite opcional deixaria o programa fechar sem provar integração."""
    dados = programa.novo(tmp_path, "sistema", AGORA)
    with pytest.raises(programa.PlanoInvalido, match="aceite de sistema"):
        programa.propor_plano(dados, _plano(("C1", [])), "  ")


# ---------------------------------------------------------------------------
# A5 — durabilidade
# ---------------------------------------------------------------------------


def test_programa_sobrevive_a_sessao_nova(tmp_path):
    """A5. Mutação alvo: guardar estado em memória em vez do disco quebra a retomada."""
    dados = _ate_execucao(tmp_path)
    dados = programa.iniciar_ciclo(dados, "C1", "2026-08-05-1")
    programa.gravar(tmp_path, dados)

    # "sessão nova": nada além do disco.
    relido = programa.carregar(tmp_path)
    assert relido["estado"] == "EXECUCAO"
    assert programa.resumo(relido)["objetivo"] == "sistema de teste"
    assert relido["ciclos"][0]["status"] == "ATIVO"


def test_programa_ilegivel_nao_e_sobrescrito_em_silencio(tmp_path):
    """A5. Mutação alvo: `carregar_estrito` devolver None apagaria a decomposição inteira."""
    alvo = programa.caminho(tmp_path)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text("{ isto não é json", encoding="utf-8")

    with pytest.raises(programa.ProgramaCorrompido):
        programa.carregar_estrito(tmp_path)
    assert programa.carregar(tmp_path) is None  # tolerante, para hooks


def test_novo_recusa_sobrescrever_programa_em_andamento(tmp_path):
    """A5. Mutação alvo: sem a trava, abrir um programa apagaria outro em andamento."""
    programa.novo(tmp_path, "primeiro", AGORA)
    with pytest.raises(programa.ProgramaJaAtivo):
        programa.novo(tmp_path, "segundo", AGORA)

    forcado = programa.novo(tmp_path, "segundo", AGORA, forcar=True)
    assert forcado["objetivo"] == "segundo"


def test_gravacao_e_atomica(tmp_path):
    """A5. Mutação alvo: escrever direto no alvo deixaria o programa ilegível se interrompido."""
    dados = programa.novo(tmp_path, "sistema", AGORA)
    programa.gravar(tmp_path, dados)
    conteudo = json.loads(programa.caminho(tmp_path).read_text(encoding="utf-8"))
    assert conteudo["objetivo"] == "sistema"
    restos = list(programa.caminho(tmp_path).parent.glob("programa.json.*.tmp"))
    assert restos == [], f"temporário não removido: {restos}"


# ---------------------------------------------------------------------------
# A6 — desvio é conjunto fechado
# ---------------------------------------------------------------------------


def test_desvio_com_motivo_livre_e_recusado(tmp_path):
    """A6/P2. Mutação alvo: motivo livre faz parada por exceção virar parada por etapa."""
    dados = _ate_execucao(tmp_path)
    with pytest.raises(programa.DesvioInvalido):
        programa.desviar(dados, "achei estranho", "qualquer coisa")


def test_desvio_valido_para_e_retomada_limpa_o_registro(tmp_path):
    """A6. Mutação alvo: retomar sem limpar `desvio` deixaria o motivo velho grudado."""
    dados = _ate_execucao(tmp_path)
    dados = programa.desviar(dados, "stack-fora-do-plano", "precisa de Redis")

    assert dados["estado"] == "DESVIO"
    assert dados["desvio"]["motivo"] == "stack-fora-do-plano"

    dados = programa.retomar_apos_desvio(dados)
    assert dados["estado"] == "EXECUCAO"
    assert dados["desvio"] is None


# ---------------------------------------------------------------------------
# A6 — replanejar a partir do desvio não desfaz trabalho aceito
# ---------------------------------------------------------------------------


def _ate_desvio(tmp_path):
    """Programa em DESVIO com C1 CONCLUIDO e C2 REPROVADO — o cenário do replanejamento."""
    dados = _ate_execucao(tmp_path)
    dados = programa.registrar_aceite(dados, "C1", passou=True)
    dados = programa.registrar_aceite(dados, "C2", passou=False)
    return programa.desviar(dados, "stack-fora-do-plano", "o plano previa SQLite")


def test_replanejar_preserva_o_status_dos_ciclos_que_permanecem(tmp_path):
    """A6. Mutação alvo: reconstruir `ciclos` com PENDENTE para todos.

    Era o comportamento até o aceite de sistema reprovar: `propor_plano` montava a lista
    do zero, e pela aresta `DESVIO -> PLANO_MESTRE` isso apagava em silêncio o veredito
    de todo ciclo já fechado. O `programa.json` passava a afirmar que nada tinha sido
    feito — e o REPROVADO some junto, que é a metade pior: um vermelho apagado deixa o
    programa elegível a concluir.
    """
    dados = _ate_desvio(tmp_path)
    mesmo_plano = _plano(("C1", []), ("C2", ["C1"]), ("C3", ["C2"]))

    novo = programa.propor_plano(dados, mesmo_plano, "o sistema sobe e responde")

    por_id = {c["id"]: c["status"] for c in novo["ciclos"]}
    assert por_id == {"C1": "CONCLUIDO", "C2": "REPROVADO", "C3": "PENDENTE"}


def test_replanejar_zera_o_ciclo_cujo_criterio_de_aceite_mudou(tmp_path):
    """A6. Mutação alvo: preservar o status só pelo `id`, ignorando o aceite.

    O id é rótulo; o aceite é o enunciado falsificável que decidiu o veredito. Manter
    CONCLUIDO sob um critério reescrito é dar por satisfeito um requisito que ninguém
    verificou — o mesmo defeito dos "42 volumes entregues" que eram esqueletos, em
    escala menor e mais difícil de ver.
    """
    dados = _ate_desvio(tmp_path)
    plano_novo = _plano(("C1", []), ("C2", ["C1"]), ("C3", ["C2"]))
    plano_novo[0]["aceite"] = "agora tem de responder em menos de 200ms também"

    novo = programa.propor_plano(dados, plano_novo, "o sistema sobe e responde")

    assert novo["ciclos"][0]["status"] == "PENDENTE"
    assert novo["ciclos"][0]["ciclo_do_estado"] is None, (
        "trabalho que vai ser refeito não pode ficar amarrado à execução antiga"
    )
    assert novo["ciclos"][1]["status"] == "REPROVADO", "só o ciclo alterado é zerado"


def test_replanejar_preserva_a_amarracao_ao_ciclo_do_estado(tmp_path):
    """A6. Mutação alvo: copiar só o `status` e largar `ciclo_do_estado`.

    A amarração é o que permite auditar depois qual execução de ciclo produziu qual
    entrega. Perdida no replanejamento, a trilha e o programa voltam a contar histórias
    paralelas — exatamente o que `iniciar_ciclo` existe para impedir.
    """
    dados = _ate_execucao(tmp_path)
    dados = programa.iniciar_ciclo(dados, "C1", "2026-08-05-1")
    dados = programa.registrar_aceite(dados, "C1", passou=True)
    dados = programa.desviar(dados, "dependencia-nao-prevista", "faltou fila")

    novo = programa.propor_plano(
        dados, _plano(("C1", []), ("C2", ["C1"])), "o sistema sobe e responde"
    )

    assert novo["ciclos"][0]["ciclo_do_estado"] == "2026-08-05-1"


def test_replanejar_aceita_ciclos_novos_e_esquece_os_removidos(tmp_path):
    """A6. Mutação alvo: reaproveitar por posição em vez de por id.

    Replanejar é justamente mudar a decomposição: ciclo que entra nasce PENDENTE, ciclo
    que sai do plano some. Casar por posição faria o status de C2 aterrissar no ciclo
    novo que ocupou o lugar dele.
    """
    dados = _ate_desvio(tmp_path)
    plano_novo = _plano(("C0", []), ("C1", ["C0"]), ("C9", ["C1"]))

    novo = programa.propor_plano(dados, plano_novo, "o sistema sobe e responde")

    por_id = {c["id"]: c["status"] for c in novo["ciclos"]}
    assert por_id == {"C0": "PENDENTE", "C1": "CONCLUIDO", "C9": "PENDENTE"}


def test_replanejar_fecha_o_desvio(tmp_path):
    """A6. Mutação alvo: deixar o registro do desvio grudado após o replanejamento.

    Propor o plano novo É a resposta ao conflito. Um motivo que sobrevive à aprovação
    fica sendo impresso para sempre num programa em EXECUCAO, e ruído permanente treina
    a ignorar o campo — o oposto do que a parada por exceção (P2) existe para produzir.
    """
    dados = _ate_desvio(tmp_path)

    novo = programa.propor_plano(
        dados, _plano(("C1", []), ("C2", ["C1"])), "o sistema sobe e responde"
    )

    assert novo["desvio"] is None


# ---------------------------------------------------------------------------
# A7 — aceite de sistema
# ---------------------------------------------------------------------------


def test_aceite_de_sistema_exige_todos_os_ciclos_concluidos(tmp_path):
    """A7. Mutação alvo: pular a checagem reproduz os "42 volumes entregues" que eram esqueletos."""
    dados = _ate_execucao(tmp_path)
    dados = programa.registrar_aceite(dados, "C1", passou=True)

    assert not programa.pronto_para_aceite(dados)
    with pytest.raises(programa.TransicaoInvalida, match="C2, C3"):
        programa.entrar_em_aceite(dados)


def test_aceite_de_sistema_vermelho_nao_conclui(tmp_path):
    """A7. Mutação alvo: concluir independente do veredito fecharia verde com sistema quebrado."""
    dados = _ate_execucao(tmp_path)
    for cid in ("C1", "C2", "C3"):
        dados = programa.registrar_aceite(dados, cid, passou=True)
    dados = programa.entrar_em_aceite(dados)

    dados = programa.concluir(dados, passou=False, agora=AGORA)
    assert dados["estado"] == "EXECUCAO", (
        "aceite vermelho devolve para EXECUCAO, nunca conclui"
    )


def test_caminho_feliz_completo_conclui(tmp_path):
    """A1+A7. Mutação alvo: qualquer trava a mais impediria um programa legítimo de fechar."""
    dados = _ate_execucao(tmp_path)
    for cid in ("C1", "C2", "C3"):
        alvo = programa.proximo_elegivel(dados)
        assert alvo["id"] == cid
        dados = programa.iniciar_ciclo(dados, cid, f"2026-08-05-{cid}")
        dados = programa.registrar_aceite(dados, cid, passou=True)

    dados = programa.entrar_em_aceite(dados)
    dados = programa.concluir(dados, passou=True, agora=AGORA)

    assert dados["estado"] == "CONCLUIDO"
    assert programa.resumo(dados)["concluidos"] == 3


# ---------------------------------------------------------------------------
# A8 / grafo
# ---------------------------------------------------------------------------


def test_transicao_fora_do_grafo_e_recusada(tmp_path):
    """A8. Mutação alvo: aceitar qualquer destino permitiria pular a porta e o aceite."""
    dados = programa.novo(tmp_path, "sistema", AGORA)
    with pytest.raises(programa.TransicaoInvalida):
        programa.transicionar(dados, "CONCLUIDO")


def test_concluido_e_terminal(tmp_path):
    """A8. Mutação alvo: dar saída a CONCLUIDO permitiria reabrir um programa fechado."""
    assert programa.TRANSICOES["CONCLUIDO"] == ()


def test_ciclo_inexistente_levanta(tmp_path):
    """A8. Mutação alvo: ignorar id desconhecido faria o aceite sumir sem erro."""
    dados = _ate_execucao(tmp_path)
    with pytest.raises(KeyError):
        programa.registrar_aceite(dados, "NAO-EXISTE", passou=True)


def test_cadeado_do_programa_e_separado_do_cadeado_do_ciclo(tmp_path):
    """P3. Mutação alvo: compartilhar o cadeado faria o orquestrador travar contra si mesmo."""
    from ferramentas import estado

    assert programa.caminho_cadeado(tmp_path) != estado.caminho_cadeado(tmp_path)
    # O cadeado do ciclo tomado não pode impedir o programa de gravar.
    with estado.cadeado(tmp_path):
        programa.novo(tmp_path, "sistema", AGORA)
    assert programa.carregar(tmp_path)["objetivo"] == "sistema"


def test_arquivo_do_programa_e_separado_do_estado(tmp_path):
    """P3. Mutação alvo: um arquivo só faria `desligar` do ciclo destruir o programa."""
    from ferramentas import estado

    assert programa.caminho(tmp_path) != estado.caminho(tmp_path)
