import pytest

from compilador import (
    Dialeto,
    OrcamentoExcedido,
    PontoDeCache,
    PosicaoDeCacheInvalida,
    PromptNaoPromovido,
    PromptPromovido,
    VariavelAusente,
    compilar,
)


def prompt(corpo="Resuma o texto a seguir: {texto}", estado="PROMOVIDO"):
    return PromptPromovido(
        nome="resumo",
        corpo=corpo,
        variaveis_declaradas=frozenset({"texto"}),
        hash="abc123",
        estado=estado,
    )


def dialeto_simples(nome="dialeto-A"):
    return Dialeto(nome=nome, formatar_mensagens=lambda corpo: ({"role": "user", "content": corpo},))


def dialeto_com_sistema(nome="dialeto-B"):
    return Dialeto(
        nome=nome,
        formatar_mensagens=lambda corpo: (
            {"role": "system", "content": "Você é um assistente."},
            {"role": "user", "content": corpo},
        ),
    )


def test_compilar_prompt_nao_promovido_e_rejeitado():
    """Q1: a mutação alvo é compilar prompt fora do estado PROMOVIDO."""
    with pytest.raises(PromptNaoPromovido):
        compilar(
            prompt(estado="RASCUNHO"),
            variaveis={"texto": "conteudo"},
            dialeto=dialeto_simples(),
            orcamento_tokens=1000,
        )


def test_variavel_ausente_e_rejeitada():
    """Q6: a mutação alvo é renderizar com placeholder vazio em vez de rejeitar."""
    with pytest.raises(VariavelAusente):
        compilar(prompt(), variaveis={}, dialeto=dialeto_simples(), orcamento_tokens=1000)


def test_compilacao_e_deterministica_para_mesma_entrada():
    """Q2: mesma entrada produz PayloadCompilado igual por valor."""
    kwargs = dict(
        prompt=prompt(),
        variaveis={"texto": "conteudo de exemplo"},
        dialeto=dialeto_simples(),
        orcamento_tokens=1000,
    )
    resultado_1 = compilar(**kwargs)
    resultado_2 = compilar(**kwargs)
    assert resultado_1 == resultado_2


def test_orcamento_excedido_e_rejeitado():
    """Q3: a mutação alvo é aceitar payload acima do orçamento sem erro."""
    with pytest.raises(OrcamentoExcedido):
        compilar(
            prompt(corpo="Resuma: {texto}"),
            variaveis={"texto": "uma frase razoavelmente longa com muitas palavras diferentes"},
            dialeto=dialeto_simples(),
            orcamento_tokens=3,
        )


def test_dois_dialetos_produzem_formatacoes_diferentes():
    """Q4: a formatação vem do adaptador injetado, não de lógica fixa em compilar."""
    resultado_a = compilar(
        prompt(), {"texto": "x"}, dialeto=dialeto_simples(), orcamento_tokens=1000
    )
    resultado_b = compilar(
        prompt(), {"texto": "x"}, dialeto=dialeto_com_sistema(), orcamento_tokens=1000
    )
    assert len(resultado_a.mensagens) == 1
    assert len(resultado_b.mensagens) == 2
    assert resultado_b.mensagens[0]["role"] == "system"


def test_ponto_de_cache_em_posicao_invalida_e_rejeitado():
    """Q5: a mutação alvo é aceitar ponto de cache fora de posição estável."""
    with pytest.raises(PosicaoDeCacheInvalida):
        compilar(
            prompt(),
            {"texto": "x"},
            dialeto=dialeto_simples(),
            orcamento_tokens=1000,
            pontos_de_cache=(PontoDeCache("fim_variavel"),),
        )


def test_ponto_de_cache_em_posicao_estavel_e_aceito():
    resultado = compilar(
        prompt(),
        {"texto": "x"},
        dialeto=dialeto_simples(),
        orcamento_tokens=1000,
        pontos_de_cache=(PontoDeCache("inicio_estavel"),),
    )
    assert resultado.pontos_de_cache[0].posicao == "inicio_estavel"
