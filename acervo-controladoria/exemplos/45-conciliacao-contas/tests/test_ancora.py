from datetime import date

from ancora import Movimento, achar_ancora


def test_ancora_bate_quando_saldo_projetado_fecha_com_banco():
    movimentos = [Movimento(date(2026, 1, 2), 100.0), Movimento(date(2026, 1, 3), -40.0)]
    saldos_banco = {date(2026, 1, 2): 1100.0, date(2026, 1, 3): 1060.0}
    ancora = achar_ancora(1000.0, date(2026, 1, 1), movimentos, saldos_banco)
    assert ancora is not None
    assert ancora.data == date(2026, 1, 3)
    assert ancora.residuo == 0.0


def test_sem_ancora_quando_residuo_nao_fecha():
    movimentos = [Movimento(date(2026, 1, 2), 100.0)]
    saldos_banco = {date(2026, 1, 2): 5000.0}
    assert achar_ancora(1000.0, date(2026, 1, 1), movimentos, saldos_banco) is None


def test_lancamento_com_data_retroativa_fecha_o_dia_correto_quando_chega():
    """Um lancamento que chega depois (D+2) mas com data de registro D tem de
    fechar o dia D quando incluido -- nao o dia em que foi baixado."""
    saldos_banco = {date(2026, 1, 5): 1050.0}

    sem_o_tardio = achar_ancora(1000.0, date(2026, 1, 1), [], saldos_banco)
    assert sem_o_tardio is None

    com_o_tardio = achar_ancora(
        1000.0,
        date(2026, 1, 1),
        [Movimento(date(2026, 1, 5), 50.0)],
        saldos_banco,
    )
    assert com_o_tardio is not None
    assert com_o_tardio.data == date(2026, 1, 5)
