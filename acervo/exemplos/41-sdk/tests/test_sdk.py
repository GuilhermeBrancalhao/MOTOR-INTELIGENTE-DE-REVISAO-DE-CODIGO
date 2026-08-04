import pytest

from sdk import (
    DepreciacaoSemMotivo,
    ErroDoSDK,
    ErroSemOrientacao,
    ExemploDeUso,
    ExemploNaoVerificado,
    ExposicaoSemJustificativa,
    MembroDeSDK,
    MembroNaoEncontrado,
    MudancaDeSuperficie,
    RemocaoSemDeprecacao,
    SuperficieDoSDK,
    VersaoSemantica,
    VersionamentoIncorreto,
    aceitar_exemplo,
    validar_release,
)


def test_release_que_quebra_sem_bump_de_major_e_rejeitado():
    """Mutação alvo: aceitar release com quebra de compatibilidade sem incrementar major (AC1)."""
    anterior = VersaoSemantica(1, 4, 0)
    nova = VersaoSemantica(1, 5, 0)
    mudanca = MudancaDeSuperficie("remove parametro obrigatorio", quebra_compatibilidade=True)

    with pytest.raises(VersionamentoIncorreto):
        validar_release(anterior, nova, mudanca)


def test_release_compativel_sem_bump_de_major_e_aceito():
    """Mutação alvo: rejeitar release compatível que só incrementa minor (AC1)."""
    anterior = VersaoSemantica(1, 4, 0)
    nova = VersaoSemantica(1, 5, 0)
    mudanca = MudancaDeSuperficie("adiciona metodo novo", quebra_compatibilidade=False)

    validar_release(anterior, nova, mudanca)


def test_release_que_quebra_com_bump_de_major_e_aceito():
    """Mutação alvo: rejeitar release que quebra mesmo com major corretamente incrementado (AC1)."""
    anterior = VersaoSemantica(1, 4, 0)
    nova = VersaoSemantica(2, 0, 0)
    mudanca = MudancaDeSuperficie("remove parametro obrigatorio", quebra_compatibilidade=True)

    validar_release(anterior, nova, mudanca)


def test_membro_publico_sem_justificativa_e_rejeitado():
    """Mutação alvo: aceitar MembroDeSDK publico=True sem motivo_publico (AC2)."""
    with pytest.raises(ExposicaoSemJustificativa):
        MembroDeSDK(nome="Cliente", publico=True)


def test_membro_publico_com_justificativa_funciona():
    """Mutação alvo: rejeitar MembroDeSDK publico com motivo declarado (AC2)."""
    membro = MembroDeSDK(nome="Cliente", publico=True, motivo_publico="ponto de entrada do SDK")
    assert membro.publico is True


def test_erro_sem_orientacao_de_correcao_e_rejeitado():
    """Mutação alvo: aceitar ErroDoSDK sem como_corrigir (AC3)."""
    with pytest.raises(ErroSemOrientacao):
        ErroDoSDK(o_que_falhou="timeout de rede", como_corrigir="")


def test_membro_depreciado_sem_motivo_e_rejeitado():
    """Mutação alvo: aceitar MembroDeSDK depreciado=True sem motivo_de_depreciacao (AC5)."""
    with pytest.raises(DepreciacaoSemMotivo):
        MembroDeSDK(nome="ClienteAntigo", publico=True, motivo_publico="legado", depreciado=True)


def test_remocao_de_membro_publico_sem_depreciacao_e_rejeitada():
    """Mutação alvo: permitir remover membro publico nunca depreciado (AC5)."""
    superficie = SuperficieDoSDK(versao_atual=VersaoSemantica(1, 0, 0))
    superficie.adicionar_membro(
        MembroDeSDK(nome="Cliente", publico=True, motivo_publico="ponto de entrada")
    )

    with pytest.raises(RemocaoSemDeprecacao):
        superficie.remover_membro("Cliente", VersaoSemantica(2, 0, 0))


def test_remocao_de_membro_publico_depreciado_sem_bump_de_major_e_rejeitada():
    """Mutação alvo: permitir remover membro depreciado sem incrementar major (AC1/AC4)."""
    superficie = SuperficieDoSDK(versao_atual=VersaoSemantica(1, 0, 0))
    superficie.adicionar_membro(
        MembroDeSDK(
            nome="Cliente",
            publico=True,
            motivo_publico="ponto de entrada",
            depreciado=True,
            motivo_de_depreciacao="substituido por ClienteV2",
        )
    )

    with pytest.raises(VersionamentoIncorreto):
        superficie.remover_membro("Cliente", VersaoSemantica(1, 1, 0))


def test_remocao_apos_depreciacao_com_major_bump_funciona():
    """Mutação alvo: rejeitar remoção correta após ciclo completo de depreciação (AC1/AC4/AC5)."""
    superficie = SuperficieDoSDK(versao_atual=VersaoSemantica(1, 0, 0))
    superficie.adicionar_membro(
        MembroDeSDK(
            nome="Cliente",
            publico=True,
            motivo_publico="ponto de entrada",
            depreciado=True,
            motivo_de_depreciacao="substituido por ClienteV2",
        )
    )

    superficie.remover_membro("Cliente", VersaoSemantica(2, 0, 0))

    assert "Cliente" not in superficie.membros
    assert superficie.versao_atual == VersaoSemantica(2, 0, 0)


def test_remocao_de_membro_inexistente_e_rejeitada():
    """Mutação alvo: aceitar remoção silenciosa de membro que não existe na superfície."""
    superficie = SuperficieDoSDK(versao_atual=VersaoSemantica(1, 0, 0))

    with pytest.raises(MembroNaoEncontrado):
        superficie.remover_membro("Fantasma", VersaoSemantica(2, 0, 0))


def test_exemplo_nao_verificado_e_rejeitado():
    """Mutação alvo: aceitar ExemploDeUso sem resultado_verificado=True (AC6)."""
    exemplo = ExemploDeUso(descricao="quickstart", codigo="cliente.buscar(id=1)")

    with pytest.raises(ExemploNaoVerificado):
        aceitar_exemplo(exemplo)


def test_exemplo_verificado_e_aceito():
    """Mutação alvo: rejeitar ExemploDeUso já verificado contra o código real (AC6)."""
    exemplo = ExemploDeUso(
        descricao="quickstart", codigo="cliente.buscar(id=1)", resultado_verificado=True
    )

    aceitar_exemplo(exemplo)
