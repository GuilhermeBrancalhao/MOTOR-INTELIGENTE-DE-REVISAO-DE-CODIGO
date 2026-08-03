from definicao_de_pronto import (
    Auditoria,
    Exemplos,
    Gates,
    Status,
    decidir_status,
    motivo_de_nao_promocao,
)

APROVADA = Auditoria(media=8.5, menor_nota_de_secao=7.0)


def _gates(**troca):
    base = dict(
        estrutural_verde=True,
        exemplos=Exemplos.PASSAM,
        auditoria=APROVADA,
        registrado_no_changelog=True,
    )
    base.update(troca)
    return Gates(**base)


def test_os_quatro_criterios_juntos_promovem():
    assert decidir_status(_gates()) is Status.PRONTO
    assert motivo_de_nao_promocao(_gates()) is None


def test_volume_sem_exemplo_citado_nao_e_pronto():
    """A decisao de leitura do criterio 2 que manteve sete volumes em RASCUNHO em
    2026-08-03: nao citar exemplo nao e caso vacuo que passa -- e criterio nao
    satisfeito, porque `pytest exemplos/<vol>` nao tem o que rodar."""
    g = _gates(exemplos=Exemplos.NAO_CITADOS)
    assert decidir_status(g) is not Status.PRONTO
    assert "criterio 2" in motivo_de_nao_promocao(g)


def test_auditoria_alta_sozinha_nao_promove():
    """Media 8,5 com gate estrutural vermelho continua RASCUNHO -- julgamento bom
    nao compra verificacao mecanica."""
    g = _gates(estrutural_verde=False)
    assert decidir_status(g) is Status.RASCUNHO


def test_secao_abaixo_de_seis_reprova_mesmo_com_media_alta():
    """A media esconde a secao fraca; o piso por secao existe para isso."""
    g = _gates(auditoria=Auditoria(media=9.0, menor_nota_de_secao=5.5))
    assert decidir_status(g) is Status.REQUER_REVISAO


def test_media_no_limite_exato_aprova():
    g = _gates(auditoria=Auditoria(media=8.0, menor_nota_de_secao=6.0))
    assert decidir_status(g) is Status.PRONTO


def test_reprovado_no_julgamento_nao_regride_para_rascunho():
    """REQUER_REVISAO e RASCUNHO nao sao intercambiaveis: o primeiro ja passou os
    gates mecanicos, o segundo nao. Colapsar os dois perde essa informacao."""
    g = _gates(auditoria=Auditoria(media=7.0, menor_nota_de_secao=7.0))
    assert decidir_status(g) is Status.REQUER_REVISAO
    assert decidir_status(_gates(estrutural_verde=False)) is Status.RASCUNHO


def test_changelog_ausente_impede_promocao():
    g = _gates(registrado_no_changelog=False)
    assert decidir_status(g) is not Status.PRONTO
    assert "criterio 4" in motivo_de_nao_promocao(g)


def test_criterio_barato_e_relatado_antes_do_caro():
    """Com gate 1 vermelho E auditoria ausente, o motivo relatado e o gate 1 --
    para nao mandar gastar auditoria num volume que nem passa no validador."""
    g = _gates(estrutural_verde=False, auditoria=None)
    assert "criterio 1" in motivo_de_nao_promocao(g)
