from casamento import Movimento, TituloAberto, casar, similaridade


def test_casa_por_valor_exato_e_nome_similar():
    aberto = [TituloAberto("T1", "FORNECEDOR AGUA MINERAL LTDA", 500.0)]
    mov = Movimento("PAGTO FORNECEDOR AGUA MINERAL", -500.0)
    assert casar(mov, aberto) is aberto[0]


def test_nao_casa_quando_nao_ha_titulo_no_valor():
    aberto = [TituloAberto("T1", "FORNECEDOR X", 500.0)]
    mov = Movimento("PAGTO FORNECEDOR X", -900.0)
    assert casar(mov, aberto) is None


def test_boilerplate_nao_derruba_a_identificacao_de_fornecedores_diferentes():
    """Duas descricoes de cartao compartilham o boilerplate 'COMPRA NACIONAL
    DEBIT' mas os fornecedores sao diferentes -- sem descontar o boilerplate a
    similaridade ficaria parecida demais entre os dois e o casamento arriscaria
    escolher o titulo errado."""
    aberto = [
        TituloAberto("T1", "COMPRA NACIONAL DEBIT PADARIA CENTRAL", 80.0),
        TituloAberto("T2", "COMPRA NACIONAL DEBIT FARMACIA BOA SAUDE", 80.0),
    ]
    mov = Movimento("COMPRA NACIONAL DEBIT FARMACIA BOA SAUDE", -80.0)
    resultado = casar(mov, aberto)
    assert resultado is not None
    assert resultado.id == "T2"


def test_consumo_variavel_ainda_casa_dentro_da_tolerancia():
    aberto = [TituloAberto("T1", "PROVEDOR INTERNET FIBRA", 200.0)]
    mov = Movimento("PROVEDOR INTERNET FIBRA", -204.50)
    assert casar(mov, aberto) is aberto[0]


def test_similaridade_zero_quando_os_dois_lados_sao_so_boilerplate():
    assert similaridade("PAGAMENTO TRANSFERENCIA", "RECEBIMENTO CONTA") == 0.0
