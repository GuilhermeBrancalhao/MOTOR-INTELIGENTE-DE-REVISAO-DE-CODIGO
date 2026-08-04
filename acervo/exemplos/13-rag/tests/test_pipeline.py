from pipeline import Candidato, compor_resposta, confirmar_validade, medir_fidelidade, reordenar


def test_reordenar_produz_score_relevancia_distinto_de_proximidade():
    """R3: proximidade alta nao garante relevancia alta apos reordenar."""
    candidatos = (
        Candidato("perto-mas-irrelevante", score_proximidade=0.95),
        Candidato("longe-mas-relevante", score_proximidade=0.50),
    )
    relevancia = {"perto-mas-irrelevante": 0.1, "longe-mas-relevante": 0.9}
    resultado = reordenar(candidatos, "pergunta", relevancia)
    assert resultado[0].id_documento == "longe-mas-relevante"
    assert resultado[0].score_relevancia != resultado[0].score_proximidade


def test_confirmar_validade_roda_depois_e_filtra_expirados():
    """R6: a mutação alvo é pular esta etapa — este teste falha se um
    documento expirado continuar entre os candidatos."""
    candidatos = (Candidato("d1", 0.9, 0.9), Candidato("d2", 0.8, 0.8))
    validos = {"d1"}  # d2 "expirou"
    resultado = confirmar_validade(candidatos, lambda id_: object() if id_ in validos else None)
    assert [c.id_documento for c in resultado] == ["d1"]


def test_compor_resposta_sem_candidato_valido_recusa_explicitamente():
    """R4: silêncio explícito, nunca resposta sem fundamento."""
    r = compor_resposta((), gerar_texto=lambda c: "nunca chamado", trechos_por_id={}, afirmacoes_sustentadas=set())
    assert r.recusada is True
    assert r.motivo_recusa == "sem fonte valida suficiente"
    assert r.texto == ""


def test_compor_resposta_com_candidato_valido_gera_e_mede_fidelidade():
    candidatos = (Candidato("d1", 0.9, 0.9),)
    r = compor_resposta(
        candidatos,
        gerar_texto=lambda c: "O prazo e 30 dias.",
        trechos_por_id={"d1": "prazo de 30 dias para reembolso"},
        afirmacoes_sustentadas={"O prazo e 30 dias"},
    )
    assert r.recusada is False
    assert r.fidelidade == 1.0
    assert len(r.citacoes) == 1


def test_medir_fidelidade_com_afirmacao_nao_sustentada_e_parcial():
    """R2: fidelidade medida por fato, nao assumida pela presenca de citacao."""
    texto = "O prazo e 30 dias. O produto tambem vem com garantia vitalicia."
    citacoes = ()
    sustentadas = {"O prazo e 30 dias"}  # a segunda afirmacao nao esta sustentada
    fidelidade = medir_fidelidade(texto, citacoes, sustentadas)
    assert 0.0 < fidelidade < 1.0


def test_medir_fidelidade_totalmente_nao_sustentada_e_zero():
    texto = "Isto nao esta em nenhuma fonte."
    fidelidade = medir_fidelidade(texto, (), afirmacoes_sustentadas=set())
    assert fidelidade == 0.0
