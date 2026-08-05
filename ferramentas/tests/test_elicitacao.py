"""Testes do port de `acervo/exemplos/03-discovery` para `ferramentas/elicitacao`.

O exemplo já tinha suíte própria, e ela continua onde estava. Estes testes não a
repetem: eles provam o que o **port** poderia ter quebrado e a suíte da origem não
enxerga — que o pacote importa como pacote, que os imports relativos apontam para
os módulos certos, que o catálogo atravessou a cópia íntegro, e que nada de fora
da biblioteca padrão entrou junto.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

from ferramentas import elicitacao
from ferramentas.elicitacao import (
    CATALOGO,
    CatalogoInvalido,
    Contexto,
    Entrevista,
    Especificacao,
    Lacuna,
    Origem,
    Palpite,
    Plataforma,
    detectar_contextos,
    detectar_plataformas,
    gerar,
    lacunas_ativas,
    validar_catalogo,
)

PACOTE = Path(elicitacao.__file__).resolve().parent

#: Os quatro módulos do port, na ordem de dependência. `__init__.py` entra à parte
#: porque ele é código novo deste repositório, e não cópia do exemplo.
MODULOS = ("catalogo", "deteccao", "entrevista", "especificacao")

#: Código novo deste repositório, que nunca existiu no exemplo e por isso não entra
#: no `diff` que audita o port: o `__init__` do pacote e o eixo de intenção
#: (`taxonomia`, ciclo C2). Ficam em constante separada para que a contagem abaixo
#: continue sendo exata — uma lista que cresce sozinha deixaria de reprovar o dia em
#: que alguém largasse um módulo a mais aqui dentro sem dizer a ninguém.
MODULOS_LOCAIS = ("__init__", "taxonomia")


# --- O pacote existe e é importável como pacote -------------------------


def test_importa_sem_hack_de_sys_path():
    """Derrubaria este teste: transformar `elicitacao` em diretório solto de novo.

    A origem no acervo só se importa com um `conftest.py` que insere a pasta no
    `sys.path` — foi justamente isso que manteve 37 lacunas desligadas da máquina.
    Aqui o critério é `from ferramentas import elicitacao` e nada mais; se alguém
    apagar o `__init__.py` ou devolver os imports para a forma plana
    (`from catalogo import ...`), a coleta desta suíte falha na primeira linha.
    """
    assert (PACOTE / "__init__.py").is_file()
    for nome in MODULOS:
        assert (PACOTE / f"{nome}.py").is_file(), f"módulo {nome}.py não foi portado"
    assert elicitacao.__name__ == "ferramentas.elicitacao"


def test_reexporta_os_mesmos_objetos_dos_submodulos():
    """Derrubaria este teste: o `__init__.py` passar a redefinir algo em vez de reexportar.

    Um `__init__` que recria uma classe ou reembrulha uma função produz dois objetos
    com o mesmo nome: `isinstance` contra o importado do pacote passa a falhar para
    o construído pelo submódulo, e o defeito só aparece em quem mistura os dois
    caminhos de import. A identidade tem de ser a mesma, e não apenas o nome.
    """
    assert elicitacao.Lacuna is elicitacao.catalogo.Lacuna
    assert elicitacao.CATALOGO is elicitacao.catalogo.CATALOGO
    assert elicitacao.Palpite is elicitacao.deteccao.Palpite
    assert elicitacao.Entrevista is elicitacao.entrevista.Entrevista
    assert elicitacao.gerar is elicitacao.especificacao.gerar
    for nome in elicitacao.__all__:
        assert hasattr(elicitacao, nome), f"{nome} está no __all__ e não foi importado"


# --- O catálogo atravessou a cópia íntegro ------------------------------


def test_catalogo_real_passa_na_propria_validacao():
    """Derrubaria este teste: cópia truncada, id duplicado ou peso fora de 1..10.

    `validar_catalogo` é o gate que a origem escreveu contra os quatro defeitos que
    se pagam na primeira execução. Rodá-lo sobre o `CATALOGO` real depois do port é
    o que distingue "o arquivo foi copiado" de "o conteúdo chegou inteiro": uma
    cópia parcial que corte no meio de uma `Lacuna` nem importa, mas uma que
    duplique um id importa e sai por aqui.
    """
    validado = validar_catalogo()
    assert validado == CATALOGO
    assert len(validado) == 37, "o exemplo tem 37 lacunas; o port não pode perder nenhuma"
    assert len({lacuna.id for lacuna in validado}) == 37


def test_catalogo_malformado_continua_sendo_recusado():
    """Derrubaria este teste: o port perder o `raise` e passar a devolver silêncio.

    Validação que só devolve a tupla sem reprovar nada é validação que passou a
    mentir. A lacuna abaixo não é universal e não tem gatilho nenhum — é universal
    com a marca errada, e o exemplo levanta `CatalogoInvalido` para ela.
    """
    orfa = Lacuna(
        id="sem_gatilho",
        pergunta="Pergunta que nunca seria calada por contexto nenhum?",
        porque="Existe só para provar que a validação ainda reprova.",
        peso=5,
        universal=False,
    )
    try:
        validar_catalogo([orfa])
        raise AssertionError("deveria ter levantado CatalogoInvalido")
    except CatalogoInvalido:
        pass


# --- O gatilho de plataforma e contexto continua funcionando ------------


def test_lacunas_ativas_diferem_entre_plataformas():
    """Derrubaria este teste: `relevante_para` passar a devolver `True` sempre.

    É a prova de que o gatilho sobreviveu ao port, e não apenas o texto das
    perguntas. Web e mobile compartilham as universais e mais nada: se os dois
    conjuntos ficarem iguais, o filtro virou um `return catalogo` e a entrevista
    volta a ser o formulário de quarenta itens que o exemplo existe para evitar.
    """
    web = {lacuna.id for lacuna in lacunas_ativas([Plataforma.WEB], [])}
    mobile = {lacuna.id for lacuna in lacunas_ativas([Plataforma.MOBILE], [])}
    universais = {lacuna.id for lacuna in CATALOGO if lacuna.universal}

    assert web != mobile
    assert "web_autenticacao" in web and "web_autenticacao" not in mobile
    assert "mobile_offline" in mobile and "mobile_offline" not in web
    assert universais <= web and universais <= mobile
    assert web & mobile == universais, "web e mobile só podem compartilhar as universais"


def test_contexto_destrava_lacuna_que_plataforma_nenhuma_traz():
    """Derrubaria este teste: colapsar plataforma e contexto num gatilho só.

    As duas portas são independentes de propósito: contexto nenhum é obrigatório, e
    a pergunta de cobrança em duplicidade não pertence a plataforma alguma. Se
    alguém unificar os dois campos, `pag_cobranca_dupla` passa a entrar por WEB — ou
    a não entrar nunca — e nos dois casos o conjunto abaixo muda.
    """
    so_web = {lacuna.id for lacuna in lacunas_ativas([Plataforma.WEB], [])}
    com_pagamento = {
        lacuna.id
        for lacuna in lacunas_ativas([Plataforma.WEB], [Contexto.LOJA_PAGAMENTOS])
    }
    assert "pag_cobranca_dupla" not in so_web
    assert "pag_cobranca_dupla" in com_pagamento
    assert so_web < com_pagamento, "acrescentar contexto só pode acrescentar lacuna"


# --- Detecção, entrevista e especificação chegaram vivas -----------------


def test_deteccao_devolve_palpite_com_trecho_do_texto_original():
    """Derrubaria este teste: devolver o texto dobrado (sem acento) como evidência.

    O port copiou `_dobrar` e o mapa de posições junto; se o mapa se perder, a
    evidência sai em minúsculas e sem acento, e a pessoa recebe de volta uma versão
    deformada da própria frase. A checagem é literal: o trecho tem de ser uma
    substring do que foi escrito.
    """
    ideia = "Preciso de um aplicativo de celular para a clínica cobrar consulta por pix."
    plataformas = detectar_plataformas(ideia)
    contextos = detectar_contextos(ideia)

    assert plataformas, "esperava ao menos um palpite de plataforma"
    assert contextos, "esperava ao menos um palpite de contexto"
    for palpite in (*plataformas, *contextos):
        assert isinstance(palpite, Palpite)
        assert palpite.origem is Origem.INFERIDO
        assert palpite.evidencia in ideia, f"evidência {palpite.evidencia!r} não é do texto"

    assert str(Plataforma.MOBILE) in {p.valor for p in plataformas}
    valores = {p.valor for p in contextos}
    assert str(Contexto.SAUDE) in valores
    assert str(Contexto.LOJA_PAGAMENTOS) in valores


def test_confirmar_palpite_destrava_bloco_e_gera_especificacao():
    """Derrubaria este teste: `confirmar` deixar de aplicar a plataforma ao conjunto.

    Percurso completo pelos quatro módulos portados — detecção, confirmação,
    resposta e geração. É o teste que pega import relativo apontando para o módulo
    errado: `entrevista` importando um `catalogo` que não é o do pacote continuaria
    importável e daria contagem de lacunas diferente aqui.
    """
    entrevista = Entrevista("Um app de celular para a equipe registrar visitas.")
    antes = {lacuna.id for lacuna in entrevista.ativas()}
    assert "mobile_offline" not in antes

    for palpite in entrevista.palpites_pendentes():
        if palpite.valor == str(Plataforma.MOBILE):
            entrevista.confirmar(palpite)
            break
    else:
        raise AssertionError("a detecção não ofereceu MOBILE para confirmar")

    assert Plataforma.MOBILE in entrevista.plataformas()
    assert "mobile_offline" in {lacuna.id for lacuna in entrevista.ativas()}

    especificacao = gerar(entrevista)
    assert isinstance(especificacao, Especificacao)
    assert not especificacao.completa, "sobrou palpite pendente e lacuna universal aberta"
    assert "## Inferencias nao confirmadas" in especificacao.markdown()


def test_especificacao_nao_se_declara_completa_com_palpite_pendente():
    """Derrubaria este teste: `completa` passar a olhar só as lacunas universais.

    É a proibição de status que mente, na versão local do exemplo. Uma inferência
    que ninguém confirmou é uma afirmação que ninguém fez; se ela deixar de segurar
    a completude, suposição vira requisito sem nenhum registro de quando virou.
    """
    entrevista = Entrevista("Site com checkout.")
    for lacuna in CATALOGO:
        if lacuna.universal:
            entrevista.responder(lacuna.id, "respondido para este teste")
    assert entrevista.palpites_pendentes()
    assert not gerar(entrevista).completa

    for palpite in entrevista.palpites_pendentes():
        entrevista.recusar(palpite)
    assert not entrevista.palpites_pendentes()
    assert gerar(entrevista).completa


# --- A trava de dependência ---------------------------------------------


def test_pacote_so_importa_biblioteca_padrao():
    """Derrubaria este teste: um `import requests` (ou qualquer coisa de fora) aqui dentro.

    Esta é a regra dura do repositório: o plugin se instala em projeto alheio e não
    tem licença para arrastar dependência junto. A varredura é do código-fonte, por
    `ast`, e não do que já está carregado em memória — import dentro de função, ou
    módulo que ninguém importou ainda, também aparece. Import relativo (`from
    .catalogo import ...`) é interno e não conta.
    """
    externos: list[str] = []
    visitados = 0

    for arquivo in sorted(PACOTE.glob("*.py")):
        visitados += 1
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                nomes = [alias.name.split(".")[0] for alias in no.names]
            elif isinstance(no, ast.ImportFrom):
                if no.level:  # relativo: é o próprio pacote
                    continue
                nomes = [(no.module or "").split(".")[0]]
            else:
                continue
            for nome in nomes:
                if nome and nome not in sys.stdlib_module_names:
                    externos.append(f"{arquivo.name}: {nome}")

    esperados = len(MODULOS) + len(MODULOS_LOCAIS)
    assert visitados == esperados, (
        f"esperava {esperados} arquivos no pacote (os {len(MODULOS)} módulos "
        f"portados + {', '.join(MODULOS_LOCAIS)}), encontrei {visitados}"
    )
    assert not externos, (
        "ferramentas/elicitacao só pode importar biblioteca padrão; encontrei: "
        + ", ".join(externos)
    )


def test_a_varredura_de_dependencia_realmente_enxerga_import():
    """Derrubaria este teste: a varredura acima passar por vacuidade.

    Um `ast.walk` que não encontra nada passa igualzinho a um que encontra só
    stdlib, e aí a trava vira decoração. Este teste afirma que os imports esperados
    estão lá — se a coleta parar de ver `dataclasses` e `unicodedata`, o teste
    anterior não está provando coisa nenhuma.
    """
    encontrados: set[str] = set()
    for arquivo in sorted(PACOTE.glob("*.py")):
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                encontrados.update(alias.name.split(".")[0] for alias in no.names)
            elif isinstance(no, ast.ImportFrom) and not no.level:
                encontrados.add((no.module or "").split(".")[0])

    assert {"dataclasses", "enum", "re", "unicodedata"} <= encontrados
    assert encontrados <= set(sys.stdlib_module_names)
