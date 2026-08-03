from datetime import date

from guarda import ChaveMovimento, GuardaDuplicidade


def test_mesma_chave_completa_e_bloqueada():
    guarda = GuardaDuplicidade()
    chave = ChaveMovimento(date(2026, 8, 3), -1000.0, "Fornecedor A")
    guarda.registrar(chave)
    assert guarda.ja_registrado(ChaveMovimento(date(2026, 8, 3), -1000.0, "fornecedor a")) is True


def test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata():
    """Dois -1000 legitimos em dias diferentes nao podem ser confundidos --
    valor isolado nunca e a chave, so o composto (data + valor + contraparte)."""
    guarda = GuardaDuplicidade()
    guarda.registrar(ChaveMovimento(date(2026, 8, 3), -1000.0, "Fornecedor A"))
    assert guarda.ja_registrado(ChaveMovimento(date(2026, 8, 4), -1000.0, "Fornecedor A")) is False


def test_valores_redondos_repetidos_para_contrapartes_diferentes_nao_sao_duplicata():
    guarda = GuardaDuplicidade()
    guarda.registrar(ChaveMovimento(date(2026, 8, 3), -1000.0, "Fornecedor A"))
    assert guarda.ja_registrado(ChaveMovimento(date(2026, 8, 3), -1000.0, "Fornecedor B")) is False


def test_sinal_importa_entrada_e_saida_do_mesmo_valor_nao_colidem():
    guarda = GuardaDuplicidade()
    guarda.registrar(ChaveMovimento(date(2026, 8, 3), 1000.0, "Cliente X"))
    assert guarda.ja_registrado(ChaveMovimento(date(2026, 8, 3), -1000.0, "Cliente X")) is False
