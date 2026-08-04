import pytest

from repositorio import (
    ConflitoDeConcorrencia,
    Migracao,
    MigracaoIncompativel,
    PoliticaDeRetencaoAusente,
    Procedencia,
    ProcedenciaAusente,
    ReferenciaAtiva,
    RegistroDeConteudo,
    Repositorio,
    aplicar_migracao,
)


def registro(id_="r1", conteudo="ola", modelo="claude-opus-5", versao="1.0"):
    return RegistroDeConteudo(id=id_, conteudo=conteudo, procedencia=Procedencia(modelo, versao))


def test_migracao_incompativel_e_rejeitada():
    """A1: a mutação alvo é registrar uma migração incompatível sem rejeição."""
    historico = []
    with pytest.raises(MigracaoIncompativel):
        aplicar_migracao(historico, Migracao("remove-campo-x", compativel_com_versao_anterior=False))
    assert historico == []


def test_migracao_compativel_e_aceita():
    historico = []
    aplicar_migracao(historico, Migracao("adiciona-campo-y", compativel_com_versao_anterior=True))
    assert len(historico) == 1


def test_registro_sem_procedencia_e_rejeitado():
    """A2: a mutação alvo é aceitar RegistroDeConteudo sem Procedencia."""
    with pytest.raises(ProcedenciaAusente):
        RegistroDeConteudo(id="r1", conteudo="x", procedencia=None)


def test_salvar_com_versao_desatualizada_gera_conflito():
    """A3: a mutação alvo é sobrescrever silenciosamente sem checar a versao esperada."""
    repo = Repositorio()
    repo.salvar(registro(), versao_esperada=0)  # primeira gravacao, versao real = 0
    with pytest.raises(ConflitoDeConcorrencia):
        repo.salvar(registro(conteudo="outra mudanca"), versao_esperada=0)  # ja avancou p/ 1


def test_salvar_com_versao_correta_funciona_e_incrementa():
    repo = Repositorio()
    repo.salvar(registro(), versao_esperada=0)
    assert repo.registros["r1"].versao_do_registro == 1
    repo.salvar(registro(conteudo="atualizado"), versao_esperada=1)
    assert repo.registros["r1"].versao_do_registro == 2
    assert repo.registros["r1"].conteudo == "atualizado"


def test_declarar_tabela_sem_retencao_e_rejeitada():
    """A4: a mutação alvo é aceitar declaração de tabela sem política de retenção."""
    repo = Repositorio()
    with pytest.raises(PoliticaDeRetencaoAusente):
        repo.declarar_tabela("logs_de_execucao")


def test_leitura_tolera_campo_desconhecido():
    """A5: a mutação alvo é falhar ou descartar silenciosamente um campo não reconhecido."""
    repo = Repositorio()
    bruto = {
        "id": "r1",
        "conteudo": "resultado",
        "procedencia": {"modelo": "claude-opus-5", "versao": "1.0"},
        "confianca_do_modelo": 0.92,
    }
    r = repo.ler_tolerante(bruto)
    assert r.campos_desconhecidos == {"confianca_do_modelo": 0.92}
    assert r.conteudo == "resultado"


def test_remover_registro_referenciado_e_rejeitado():
    """A6: a mutação alvo é excluir um registro deixando referência quebrada."""
    repo = Repositorio()
    repo.salvar(registro(id_="r1"), versao_esperada=0)
    repo.referencias["r1"] = {"r2"}
    with pytest.raises(ReferenciaAtiva):
        repo.remover("r1")
    assert "r1" in repo.registros


def test_remover_registro_sem_referencia_funciona():
    repo = Repositorio()
    repo.salvar(registro(id_="r1"), versao_esperada=0)
    repo.remover("r1")
    assert "r1" not in repo.registros
