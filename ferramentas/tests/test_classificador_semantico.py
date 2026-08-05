from __future__ import annotations

from ferramentas import classificador_semantico


def test_classificador_detecta_seguranca_critica_com_confianca_alta():
    saida = classificador_semantico.classificar(
        evidencia="erro critico de seguranca: token JWT exposto no log",
        cartoes=["python", "fastapi"],
        categoria_origem="pendencia",
        severidade_inicial="alto",
        tecnologia_inicial="python",
    )

    assert saida["categoria_semantica"] == "seguranca"
    assert saida["severidade"] == "critico"
    assert saida["confianca"] >= 0.7
    assert saida["origem"] == "ia-semantica"


def test_classificador_prioriza_tecnologia_por_sinal_semantico():
    saida = classificador_semantico.classificar(
        evidencia="query LINQ com timeout e lock em repositorio csproj",
        cartoes=["python", "csharp"],
        categoria_origem="pendencia",
        severidade_inicial="medio",
        tecnologia_inicial="python",
    )

    assert saida["tecnologia"] == "csharp"
    assert saida["categoria_semantica"] in {"performance", "concorrencia", "arquitetura"}
    assert saida["origem"] == "ia-semantica"


def test_classificador_fallback_regra_quando_sem_sinal_semantico():
    saida = classificador_semantico.classificar(
        evidencia="ajustar texto da mensagem",
        cartoes=["python"],
        categoria_origem="pendencia",
        severidade_inicial="alto",
        tecnologia_inicial="python",
    )

    assert saida["origem"] == "regra"
    assert saida["tecnologia"] == "python"
    assert saida["severidade"] == "alto"
