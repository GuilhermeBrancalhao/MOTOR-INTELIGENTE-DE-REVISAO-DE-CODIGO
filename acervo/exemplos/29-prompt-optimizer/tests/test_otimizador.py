from otimizador import HistoricoDeBusca, Otimizador, Variante


CASOS_DE_OURO = ("caso-1", "caso-2", "caso-3")

# taxa de acerto fixa por nome de variante, simulando avaliacao real de forma determinística
TAXAS = {
    "baseline": 0.70,
    "candidato-marginal": 0.705,   # melhoria de 0.005, abaixo do limiar padrao 0.02
    "candidato-bom": 0.85,          # melhoria clara
    "candidato-otimo": 0.92,        # melhor ainda
    "candidato-ruim": 0.40,
}


def avaliador(chamadas_registradas=None):
    def _avaliar(variante, amostra):
        if chamadas_registradas is not None:
            chamadas_registradas.append((variante.nome, amostra))
        return TAXAS[variante.nome]

    return _avaliar


def otimizador(**kwargs):
    kwargs.setdefault("avaliar_variante", avaliador())
    kwargs.setdefault("casos_de_ouro", CASOS_DE_OURO)
    return Otimizador(**kwargs)


def test_melhoria_marginal_nao_supera_baseline():
    """O2: a mutação alvo é tratar diferença de ruído (0.005) como melhoria real."""
    otim = otimizador(limiar_melhoria_minima=0.02)
    proposta, _ = otim.buscar(
        Variante("baseline", "corpo"), [Variante("candidato-marginal", "corpo v2")]
    )
    assert proposta is None


def test_melhoria_significativa_supera_baseline():
    otim = otimizador(limiar_melhoria_minima=0.02)
    proposta, _ = otim.buscar(
        Variante("baseline", "corpo"), [Variante("candidato-bom", "corpo v2")]
    )
    assert proposta is not None
    assert proposta.variante == "candidato-bom"


def test_busca_respeita_orcamento_maximo_de_tentativas():
    """O4: a mutação alvo é continuar avaliando além de max_tentativas."""
    chamadas = []
    otim = otimizador(avaliar_variante=avaliador(chamadas), max_tentativas=2)
    candidatos = [
        Variante("candidato-ruim", "c1"),
        Variante("candidato-bom", "c2"),
        Variante("candidato-otimo", "c3"),  # nao deveria ser avaliado
    ]
    otim.buscar(Variante("baseline", "corpo"), candidatos)
    # 1 chamada para o baseline + 2 chamadas (max_tentativas) = 3 chamadas totais
    assert len(chamadas) == 3
    nomes_avaliados = {nome for nome, _ in chamadas}
    assert "candidato-otimo" not in nomes_avaliados


def test_toda_tentativa_e_registrada_mesmo_rejeitada():
    """O5: a mutação alvo é descartar tentativa rejeitada sem registrar no histórico."""
    otim = otimizador()
    _, historico = otim.buscar(
        Variante("baseline", "corpo"),
        [Variante("candidato-marginal", "c1"), Variante("candidato-bom", "c2")],
    )
    assert isinstance(historico, HistoricoDeBusca)
    assert len(historico.tentativas) == 2
    nomes_no_historico = {t.variante for t in historico.tentativas}
    assert nomes_no_historico == {"candidato-marginal", "candidato-bom"}


def test_mesma_amostra_usada_em_todas_as_avaliacoes():
    """O1: a mutação alvo é usar amostra diferente por candidato."""
    chamadas = []
    otim = otimizador(avaliar_variante=avaliador(chamadas))
    otim.buscar(
        Variante("baseline", "corpo"),
        [Variante("candidato-bom", "c1"), Variante("candidato-ruim", "c2")],
    )
    amostras_usadas = {amostra for _, amostra in chamadas}
    assert amostras_usadas == {CASOS_DE_OURO}


def test_otimizador_nunca_promove_sozinho():
    """O3: a mutação alvo é a introdução futura de um método de promoção direta."""
    metodos_publicos = {m for m in dir(Otimizador) if not m.startswith("_")}
    assert not any("promov" in m.lower() or "aprova" in m.lower() for m in metodos_publicos)
