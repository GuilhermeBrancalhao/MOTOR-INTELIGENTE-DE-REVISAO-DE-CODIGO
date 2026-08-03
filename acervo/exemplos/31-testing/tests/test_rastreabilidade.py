from rastreabilidade import Proposito, Regra, Suite, Teste, cobre

R_DUPLICATA = Regra("R1", frozenset({"duplicata", "dias_diferentes"}))
R_ORDEM = Regra("R2", frozenset({"ordem", "dependencia"}))

NOMEADO_PELA_VIOLACAO = Teste(
    "test_dois_pedidos_de_mesmo_valor_em_dias_diferentes_nao_sao_duplicata",
    Proposito.REGRESSAO_DE_REGRA,
    mutacao_registrada="comparar so valor, ignorando data",
)
NOMEADO_PELA_FUNCAO = Teste("test_guarda_2", Proposito.REGRESSAO_DE_REGRA)


def test_nome_que_descreve_a_violacao_casa_com_a_regra():
    assert cobre(NOMEADO_PELA_VIOLACAO, R_DUPLICATA) is True


def test_nome_generico_nao_casa_com_regra_nenhuma():
    """O argumento central da regra de nomeacao, como predicado: `test_guarda_2`
    nao pode ser rastreado a nenhuma regra sem abrir o corpo do teste."""
    assert cobre(NOMEADO_PELA_FUNCAO, R_DUPLICATA) is False
    assert cobre(NOMEADO_PELA_FUNCAO, R_ORDEM) is False


def test_regra_sem_teste_aparece_como_lacuna():
    s = Suite((R_DUPLICATA, R_ORDEM), (NOMEADO_PELA_VIOLACAO,))
    assert s.regras_sem_teste() == (R_ORDEM,)


def test_regressao_sem_mutacao_registrada_e_hipotese():
    """Um teste que afirma proteger regra e nunca foi visto vermelho nao conta
    como provado -- e a diferenca entre especificacao e intencao."""
    s = Suite((R_DUPLICATA,), (Teste(
        "test_duplicata_em_dias_diferentes_nao_sao_duplicata",
        Proposito.REGRESSAO_DE_REGRA,
    ),))
    assert len(s.regressoes_nao_provadas()) == 1
    assert s.madura() is False


def test_caminho_feliz_nao_precisa_de_prova_por_mutacao():
    """Os dois tipos servem propositos diferentes: o de caminho feliz documenta
    comportamento e nao afirma proteger invariante nenhuma."""
    t = Teste("test_fluxo_normal_devolve_saida", Proposito.CAMINHO_FELIZ)
    assert t.provado is True


def test_suite_madura_exige_as_duas_condicoes():
    s = Suite((R_DUPLICATA,), (NOMEADO_PELA_VIOLACAO,))
    assert s.madura() is True


def test_uma_regra_pode_ter_mais_de_um_teste():
    """Rastreabilidade nao exige um-para-um; exige pelo menos um por regra."""
    outro = Teste(
        "test_duplicata_em_dias_diferentes_com_contraparte_distinta",
        Proposito.REGRESSAO_DE_REGRA,
        mutacao_registrada="ignorar contraparte",
    )
    s = Suite((R_DUPLICATA,), (NOMEADO_PELA_VIOLACAO, outro))
    assert len(s.testes_de(R_DUPLICATA)) == 2
    assert s.madura() is True
