"""Os dois buracos que a revisão de aceite encontrou no mecanismo central da descoberta.

**D1 — resposta fora das `opcoes` abria o portão sem destravar o ramo.** `responder`
gravava qualquer texto. Quando o texto não nomeava plataforma nem contexto,
`aplicar_resposta` devolvia os eixos intactos — e a lacuna saía de `abertas` do mesmo
jeito. `onde_roda` é a única lacuna universal cuja resposta muda **quais outras lacunas
existem** (está escrito no `porque` dela, e B1 existe inteiro por causa disso): respondida
com "no navegador", ela fechava, o bloco WEB não entrava, e `web_autenticacao`,
`web_hospedagem`, `web_navegador` e `web_idioma` nunca eram ativadas, perguntadas nem
listadas como assumíveis. Respondidas as outras cinco universais, a porta abria.

**D2 — o eixo plataforma/contexto era inalcançável pela CLI.** `descoberta.confirmar`,
`descoberta.recusar` e `_resolver_palpite` não tinham chamador fora dos testes, e nem
`Avaliacao.resumo()` nem `_relatar_descoberta` imprimiam `palpites_pendentes`: o campo era
gravado, carregado e nunca lido. Um pedido de aplicativo de celular com pagamento gravava
MOBILE e LOJA_PAGAMENTOS, nenhum comando os mostrava, e a porta abria com `pag_cobranca_dupla`
(peso 9) e as cinco lacunas de MOBILE fora da entrevista.

Cada docstring nomeia a mutação que derrubaria o teste. Os dois cenários da revisão estão
reproduzidos aqui **como foram descritos**, pela CLI de verdade e por subprocesso — é o
único jeito de medir código de saída, que é o que a skill lê.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import descoberta, estado  # noqa: E402
from ferramentas.elicitacao import (  # noqa: E402
    CATALOGO,
    Contexto,
    Lacuna,
    Plataforma,
    RespostaForaDasOpcoes,
    exigir_resposta_admissivel,
)

POR_ID: dict[str, Lacuna] = {lacuna.id: lacuna for lacuna in CATALOGO}

#: O pedido do cenário D1, palavra por palavra como a revisão o escreveu.
PEDIDO_D1 = "quero um sistema novo de pedidos"

#: O pedido do cenário D2, idem. Ele não traz sinal de intenção nenhum — a CLI pergunta,
#: e a resposta da pergunta é o `--intencao` abaixo. Os palpites são o assunto do teste.
PEDIDO_D2 = (
    "um app de celular para a equipe registrar visitas, com pagamento pelo próprio app"
)

#: As quatro lacunas que só existem depois de a plataforma WEB ser confirmada. São as
#: que sumiam em silêncio no cenário D1.
RAMO_WEB = ("web_autenticacao", "web_hospedagem", "web_navegador", "web_idioma")

#: As cinco que só existem depois de MOBILE. Somadas às três de LOJA_PAGAMENTOS, são o
#: que o cenário D2 deixava de fora da entrevista.
RAMO_MOBILE = (
    "mobile_offline",
    "mobile_loja",
    "mobile_permissao",
    "mobile_notificacao",
    "mobile_tablet",
)


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


def _ligar(raiz: Path) -> None:
    assert _cli(raiz, "ligar", "atender o pedido do usuario").returncode == 0


def _impressao_digital(raiz: Path) -> str:
    """SHA-256 dos BYTES do estado — carimbo novo e reordenação de chave também contam."""
    return hashlib.sha256(estado.caminho(raiz).read_bytes()).hexdigest()


def _ids_bloqueantes(saida: str) -> list[str]:
    """Os ids da seção BLOQUEANTES da saída, lidos como o usuário os lê."""
    if "BLOQUEANTES" not in saida:
        return []
    secao = saida.split("BLOQUEANTES", 1)[1].split("DECISÕES ABERTAS", 1)[0]
    return re.findall(r"^- \[([^\]]+)\]", secao, flags=re.MULTILINE)


def _ids_abertos(raiz: Path) -> set[str]:
    return {decisao.id for decisao in descoberta.avaliar_do_disco(raiz).abertas}


# =========================================================================
# D1 — resposta fora das opções é recusada, e a lacuna continua aberta
# =========================================================================


def test_o_cenario_d1_da_revisao_e_recusado_e_nada_e_gravado(tmp_path):
    """Derrubaria este teste: `responder` voltar a gravar qualquer texto.

    É o passo 2 do cenário reproduzível, literal: `onde_roda` respondida com "no
    navegador". Nenhum membro de `Plataforma` se chama assim, então `aplicar_resposta`
    devolvia os eixos intactos e a lacuna fechava mesmo assim. A recusa tem de sair com
    código 1, sem traceback, com as opções válidas na tela — recusar sem dizer o que se
    aceita é outro portão sem saída — e com o estado byte-idêntico.
    """
    _ligar(tmp_path)
    assert _cli(tmp_path, "descoberta", PEDIDO_D1).returncode == 0
    antes = _impressao_digital(tmp_path)

    saida = _cli(tmp_path, "descoberta", "responder", "onde_roda", "no navegador")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stdout + saida.stderr
    for opcao in POR_ID["onde_roda"].opcoes:
        assert opcao in saida.stdout, f"a recusa não ofereceu {opcao}"
    assert _impressao_digital(tmp_path) == antes, "a recusa gravou no estado"


def test_a_lacuna_recusada_continua_bloqueando_e_o_ramo_nao_aparece(tmp_path):
    """Derrubaria este teste: aceitar a resposta e tirar a lacuna de `abertas`.

    Os passos 3 e 4 do cenário: com "no navegador" gravado, as outras cinco universais
    respondidas abriam a porta — e as quatro lacunas de WEB nunca tinham sido ativadas,
    nem perguntadas, nem listadas como assumíveis. Agora `onde_roda` segue bloqueante,
    `fase ANALISE` segue recusada, e o ramo segue inexistente porque plataforma nenhuma
    foi confirmada. As duas metades importam: a porta fechada **e** o ramo ausente.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO_D1)

    _cli(tmp_path, "descoberta", "responder", "onde_roda", "no navegador")
    for identificador in ("problema", "usuario", "capacidade_nova", "sucesso", "fora_de_escopo"):
        resposta = _cli(tmp_path, "descoberta", "responder", identificador, "resposta de teste")
        assert resposta.returncode == 0, resposta.stdout + resposta.stderr

    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    assert "onde_roda" not in avaliacao.respondidas, "a resposta inválida foi gravada"
    assert "onde_roda" in {d.id for d in avaliacao.bloqueantes}
    assert not avaliacao.liberado_para_planejar
    assert avaliacao.plataformas == ()
    assert not set(RAMO_WEB) & _ids_abertos(tmp_path)

    status = _cli(tmp_path, "descoberta", "status")
    assert "onde_roda" in _ids_bloqueantes(status.stdout)
    assert _cli(tmp_path, "fase", "ANALISE").returncode == 1


def test_a_opcao_valida_fecha_a_lacuna_e_ativa_o_ramo(tmp_path):
    """Derrubaria este teste: a guarda recusar TUDO — inclusive a opção declarada.

    É o par obrigatório do teste acima, e o que impede o conserto preguiçoso de virar
    parede. Respondida com "WEB", `onde_roda` fecha **e** as quatro lacunas do bloco
    passam a existir, como decisões abertas assumíveis. A lista de assumíveis é o
    registro do que o motor escolheu não perguntar; antes deste conserto, essas quatro
    não estavam nem nela.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO_D1)

    saida = _cli(tmp_path, "descoberta", "responder", "onde_roda", "WEB")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    assert avaliacao.plataformas == (Plataforma.WEB,)
    assert set(RAMO_WEB) <= {d.id for d in avaliacao.assumiveis}
    assert "onde_roda" not in {d.id for d in avaliacao.abertas}


def test_lacuna_sem_opcoes_continua_aceitando_texto_livre(tmp_path):
    """Derrubaria este teste: exigir lista fechada de toda lacuna.

    "Que problema isso resolve" não tem resposta certa declarada, e inventar uma seria o
    formulário de múltipla escolha que o catálogo recusa. A regra vale só onde o próprio
    catálogo escreveu quais respostas existem — e o teste afirma, antes, que a lacuna
    usada aqui não tem opções, para não passar por acidente.
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO_D1)
    assert POR_ID["problema"].opcoes == ()

    saida = _cli(tmp_path, "descoberta", "responder", "problema", "o pedido se perde no papel")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    respostas = estado.carregar(tmp_path)[descoberta.CHAVE]["respostas"]
    assert respostas["problema"]["valor"] == "o pedido se perde no papel"


def test_acento_e_caixa_nao_reprovam_a_resposta_certa(tmp_path):
    """Derrubaria este teste: comparar as opções por igualdade crua de texto.

    "Senha própria" e "senha propria" são a mesma resposta escrita por duas pessoas.
    Reprovar uma delas transformaria a regra numa prova de digitação, e quem apanha de
    acento não aprende nada sobre o software que está especificando. O limite da
    tolerância é o teste de cima: "no navegador" continua não sendo "WEB".
    """
    _ligar(tmp_path)
    _cli(tmp_path, "descoberta", PEDIDO_D1)
    _cli(tmp_path, "descoberta", "responder", "onde_roda", "WEB")
    assert "senha propria" in POR_ID["web_autenticacao"].opcoes

    saida = _cli(tmp_path, "descoberta", "responder", "web_autenticacao", "Senha Própria")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    assert "web_autenticacao" in descoberta.avaliar_do_disco(tmp_path).respondidas


def test_pela_api_a_recusa_levanta_e_nao_toca_no_disco(tmp_path):
    """Derrubaria este teste: a CLI validar por fora e a API seguir aceitando.

    A trava tem de estar em `descoberta.responder`, e não no verbo: o gate e qualquer
    outro chamador de amanhã passam pela função, não pela linha de comando. Uma guarda só
    na CLI seria a porta trancada com a janela aberta.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    descoberta.registrar(tmp_path, PEDIDO_D1, agora="2026-08-05T10:01:00")
    antes = estado.caminho(tmp_path).read_bytes()

    with pytest.raises(RespostaForaDasOpcoes):
        descoberta.responder(tmp_path, "onde_roda", "no navegador")

    assert estado.caminho(tmp_path).read_bytes() == antes


def test_a_regra_de_admissibilidade_e_a_mesma_de_b1():
    """Derrubaria este teste: `exigir_resposta_admissivel` julgar por outro conjunto.

    B1 mede a mudança percorrendo `lacuna.opcoes` — "o conjunto de respostas admissíveis
    é `lacuna.opcoes`", está escrito na docstring do predicado. Se a guarda de gravação
    olhasse outro conjunto, o predicado passaria a prever o efeito de respostas que não
    podem ser dadas, ou a recusar as que ele mesmo considerou. A unidade é testada
    isolada porque é ela que sustenta as duas coisas.
    """
    for opcao in POR_ID["onde_roda"].opcoes:
        exigir_resposta_admissivel(POR_ID["onde_roda"], opcao)
    exigir_resposta_admissivel(POR_ID["problema"], "qualquer frase serve aqui")

    with pytest.raises(RespostaForaDasOpcoes) as erro:
        exigir_resposta_admissivel(POR_ID["onde_roda"], "no navegador")
    assert all(opcao in str(erro.value) for opcao in POR_ID["onde_roda"].opcoes)


# =========================================================================
# D2 — os palpites aparecem, e há como confirmá-los ou recusá-los
# =========================================================================


def _registrar_d2(raiz: Path) -> None:
    """O passo 1 do cenário D2. O pedido não traz sinal de intenção, e a CLI pergunta.

    A desambiguação é comportamento certo e testado em outro arquivo; aqui ela é só o
    caminho até os palpites, que são o assunto. Registrar com a intenção declarada é
    exatamente o que a mensagem de desambiguação manda fazer.
    """
    _ligar(raiz)
    saida = _cli(raiz, "descoberta", PEDIDO_D2, "--intencao", "MATERIALIZAR")
    assert saida.returncode == 0, saida.stdout + saida.stderr


def test_o_status_mostra_os_palpites_com_a_evidencia(tmp_path):
    """Derrubaria este teste: `resumo()` voltar a não imprimir `palpites_pendentes`.

    O campo era gravado, carregado e nunca lido — nenhum comando mostrava MOBILE nem
    LOJA_PAGAMENTOS. A evidência sai junto porque é ela que torna o palpite discutível:
    "por que você achou que era um aplicativo de celular?" tem de receber de volta o
    trecho do próprio pedido, e não a alegação de que o motor achou.
    """
    _registrar_d2(tmp_path)
    gravados = {p.valor: p for p in descoberta.avaliar_do_disco(tmp_path).palpites_pendentes}
    assert {"MOBILE", "LOJA_PAGAMENTOS"} <= set(gravados), "o preparo precisa dos dois palpites"

    saida = _cli(tmp_path, "descoberta", "status")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    for valor in ("MOBILE", "LOJA_PAGAMENTOS"):
        assert valor in saida.stdout
        assert gravados[valor].evidencia in saida.stdout, "o palpite saiu sem a evidência"
    assert "descoberta confirmar" in saida.stdout, "mostra o palpite e não diz como resolvê-lo"


def test_confirmar_pela_cli_aplica_o_eixo_e_traz_o_bloco_de_lacunas(tmp_path):
    """Derrubaria este teste: `descoberta confirmar` não existir, ou não aplicar o eixo.

    É o buraco inteiro do cenário D2: sem este verbo, `pag_cobranca_dupla` — peso 9, "se
    a mesma compra for cobrada duas vezes…" — e as cinco lacunas de MOBILE não apareciam
    em lugar nenhum, e a porta abria assim mesmo. Confirmar é o que as traz para a
    entrevista, e é por isso que confirmar palpite vem antes de perguntar.
    """
    _registrar_d2(tmp_path)
    assert not (set(RAMO_MOBILE) | {"pag_cobranca_dupla"}) & _ids_abertos(tmp_path)

    assert _cli(tmp_path, "descoberta", "confirmar", "MOBILE").returncode == 0
    saida = _cli(tmp_path, "descoberta", "confirmar", "LOJA_PAGAMENTOS")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    assert avaliacao.plataformas == (Plataforma.MOBILE,)
    assert Contexto.LOJA_PAGAMENTOS in avaliacao.contextos
    abertos = {d.id for d in avaliacao.abertas}
    assert set(RAMO_MOBILE) <= abertos
    assert "pag_cobranca_dupla" in abertos
    assert {p.valor for p in avaliacao.palpites_pendentes} == {"MULTIUSUARIO"}


def test_recusar_pela_cli_tira_da_pendencia_sem_aplicar_nada(tmp_path):
    """Derrubaria este teste: `recusar` virar sinônimo de `confirmar` — ou de ignorar.

    Ignorado, o palpite continua pendente e ninguém olhou para ele. Recusado, ele sai da
    lista e **não** deixa rastro de valor assumido em lugar nenhum: nem nos eixos, nem
    nas respostas, nem nas lacunas abertas. As três ausências são o teste.
    """
    _registrar_d2(tmp_path)

    saida = _cli(tmp_path, "descoberta", "recusar", "LOJA_PAGAMENTOS")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    assert "LOJA_PAGAMENTOS" not in {p.valor for p in avaliacao.palpites_pendentes}
    assert avaliacao.contextos == ()
    assert "pag_cobranca_dupla" not in {d.id for d in avaliacao.abertas}
    assert "LOJA_PAGAMENTOS" not in str(estado.carregar(tmp_path)[descoberta.CHAVE]["respostas"])


def test_palpite_que_ninguem_inferiu_e_recusado_sem_gravar(tmp_path):
    """Derrubaria este teste: `_resolver_palpite` seguir sendo um no-op silencioso.

    O filtro remove por igualdade de valor: um nome digitado errado — ou já resolvido —
    saía com código 0 sem tirar nada da lista e sem aplicar eixo nenhum, que é a mesma
    mentira de D1 em outro verbo. Pior no caso de `confirmar`: aceitar qualquer valor
    faria dele um jeito de mexer nos eixos por fora da entrevista, sem evidência e sem
    constar das respostas.
    """
    _registrar_d2(tmp_path)
    antes = _impressao_digital(tmp_path)

    for argumentos in (("confirmar", "XPTO"), ("confirmar", "WEB"), ("recusar", "SAUDE")):
        saida = _cli(tmp_path, "descoberta", *argumentos)
        assert saida.returncode == 1, saida.stdout
        assert "Traceback" not in saida.stdout + saida.stderr
        assert "MOBILE" in saida.stdout, "a recusa não disse quais palpites existem"

    assert _impressao_digital(tmp_path) == antes
    assert descoberta.avaliar_do_disco(tmp_path).plataformas == ()


def test_confirmar_duas_vezes_o_mesmo_palpite_avisa_na_segunda(tmp_path):
    """Derrubaria este teste: a segunda confirmação sair 0 como se tivesse feito algo.

    Depois da primeira, o palpite não está mais pendente. Repetir o comando não é erro de
    ninguém — é o efeito de rolar a tela e não ver que já foi —, e a resposta certa é
    dizer que não há o que resolver, nunca fingir que resolveu de novo.
    """
    _registrar_d2(tmp_path)
    assert _cli(tmp_path, "descoberta", "confirmar", "MOBILE").returncode == 0
    depois_da_primeira = _impressao_digital(tmp_path)

    segunda = _cli(tmp_path, "descoberta", "confirmar", "MOBILE")

    assert segunda.returncode == 1
    assert _impressao_digital(tmp_path) == depois_da_primeira


@pytest.mark.parametrize(
    "argumentos",
    [
        ("confirmar",),
        ("recusar",),
        ("confirmar", "MOBILE", "sobra"),
        ("confirmar", "   "),
        ("confirmar", "MOBILE"),  # sem descoberta registrada
        ("responder", "onde_roda", "no navegador"),
    ],
)
def test_nenhum_caminho_dos_verbos_novos_termina_em_traceback(tmp_path, argumentos):
    """Derrubaria este teste: deixar `PalpiteNaoPendente` (um `KeyError`) escapar.

    A CLI proíbe traceback no topo do próprio arquivo, e metade das exceções deste
    caminho herda de `KeyError` de propósito. É esta saída que a skill lê para decidir o
    que reportar ao usuário — um stack trace aqui vira "o motor está quebrado".
    """
    _ligar(tmp_path)

    saida = _cli(tmp_path, "descoberta", *argumentos)

    assert saida.returncode == 1
    assert "Traceback" not in saida.stdout + saida.stderr


# =========================================================================
# Os verbos estão anunciados — verbo que existe e não consta é portão sem saída
# =========================================================================


def test_o_uso_da_descoberta_anuncia_confirmar_e_recusar(tmp_path):
    """Derrubaria este teste: implementar os verbos e não anunciá-los.

    Verbo que existe e não consta do `uso` é o mesmo portão sem saída de antes, agora por
    desconhecimento: quem vê o palpite na tela não descobre o comando que o resolve.
    """
    saida = _cli(tmp_path, "descoberta")

    assert saida.returncode == 1
    assert "confirmar <PALPITE>" in saida.stdout
    assert "recusar <PALPITE>" in saida.stdout


def test_a_skill_documenta_os_cinco_verbos_de_descoberta():
    """Derrubaria este teste: a contagem da SKILL.md voltar a discordar da tabela.

    O texto dizia "os quatro verbos" com três linhas na tabela — e agora são cinco:
    registrar, `status`, `responder`, `confirmar` e `recusar`. A skill é a única
    documentação que o modelo lê antes de agir; contagem errada ali é verbo que ninguém
    usa, que foi exatamente como `confirmar` passou um ciclo inteiro sem chamador.
    """
    texto = (RAIZ_PLUGIN / "skills" / "engine" / "SKILL.md").read_text(encoding="utf-8")

    assert "Os cinco verbos de `descoberta`" in texto
    assert "descoberta confirmar <PALPITE>" in texto
    assert "descoberta recusar <PALPITE>" in texto
    assert "quatro verbos" not in texto


def test_os_verbos_novos_nao_gravam_estado_por_fora_do_cadeado():
    """Derrubaria este teste: trocar `descoberta.confirmar`/`recusar` por escrita direta.

    A trava geral varre o arquivo inteiro por texto; esta olha o corpo do verbo e cobra o
    caminho positivo — que a mutação passe pelas funções que tomam o cadeado. Escrita
    solta aqui é o *lost update* de volta, e ele some em silêncio até duas sessões se
    atropelarem.
    """
    fonte = (RAIZ_PLUGIN / "ferramentas" / "cli.py").read_text(encoding="utf-8")
    corpo = fonte.split("def _verbo_descoberta")[1].split("\ndef _prog_trilha")[0]

    assert "descoberta.confirmar" in corpo
    assert "descoberta.recusar" in corpo
    assert ".write_text(" not in corpo
    assert "json.dump" not in corpo
