"""Testes de `ferramentas/sincronizar.py` — o gerador de `volumes/prontos/`.

O teste que importa de verdade é `test_a_copia_do_plugin_esta_em_dia`: ele roda
contra o repositório real e reprova a suíte se a cópia que o plugin carrega
divergir do acervo. É a porta que substitui a cópia manual, e sem ela este
módulo seria só conveniência.

Os demais provam que a porta não é decorativa: cada forma de deriva que já
aconteceu de fato (rascunho viajando como pronto, volume pronto que não viaja,
arquivo com conteúdo diferente, arquivo órfão que a fonte apagou) tem um teste
que a produz de propósito e exige que seja detectada.
"""
from pathlib import Path

from ferramentas import sincronizar


def _volume(raiz: Path, nome_dir: str, status: str, corpo: str = "conteudo\n") -> Path:
    """Cria um volume sintético no acervo, no formato real de `_VOLUME.yml`."""
    diretorio = raiz / nome_dir
    diretorio.mkdir(parents=True, exist_ok=True)
    numero = nome_dir.split("-")[0]
    nome = nome_dir.split("-", 1)[1]
    (diretorio / "_VOLUME.yml").write_text(
        f'volume: "{numero}"\n'
        f"nome: {nome}\n"
        "tipo: ENGINE\n"
        f"status: {status}\n"
        "perecivel: false\n"
        "depende_de: []\n",
        encoding="utf-8",
    )
    (diretorio / "01-Introducao.md").write_text(corpo, encoding="utf-8")
    return diretorio


def _acervo(tmp_path: Path) -> Path:
    acervo = tmp_path / sincronizar.PASTA_ACERVO
    acervo.mkdir(parents=True, exist_ok=True)
    return acervo


# --------------------------------------------------------------------------
# A porta contra a deriva, no repositório real
# --------------------------------------------------------------------------


def test_a_copia_do_plugin_esta_em_dia():
    """`volumes/prontos/` tem de ser exatamente o que `acervo/` diz.

    Se este teste ficar vermelho, NÃO edite `volumes/prontos/`: rode
    `python -m ferramentas.sincronizar`. O diretório é artefato derivado, e
    consertá-lo à mão é justamente o hábito que criou a deriva original.
    """
    achados = sincronizar.divergencias()
    assert achados == [], "cópia do plugin divergiu do acervo:\n  " + "\n  ".join(
        achados
    )


# --------------------------------------------------------------------------
# Seleção pelo status da FONTE
# --------------------------------------------------------------------------


def test_rascunho_nao_viaja_no_plugin(tmp_path):
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")
    _volume(acervo, "31-TESTING", "RASCUNHO")

    sincronizar.sincronizar(tmp_path)

    destino = tmp_path.joinpath(*sincronizar.PASTA_DESTINO)
    assert (destino / "07-PROMPT-ENGINE").is_dir()
    assert not (destino / "31-TESTING").exists()


def test_volume_que_deixou_de_ser_pronto_e_removido_da_copia(tmp_path):
    """O caso real: `31-TESTING` estava na cópia marcado PRONTO enquanto a fonte
    dizia RASCUNHO. Rebaixar na fonte tem de tirar da cópia."""
    acervo = _acervo(tmp_path)
    volume = _volume(acervo, "31-TESTING", "PRONTO")
    sincronizar.sincronizar(tmp_path)
    destino = tmp_path.joinpath(*sincronizar.PASTA_DESTINO)
    assert (destino / "31-TESTING").is_dir()

    conteudo = (volume / "_VOLUME.yml").read_text(encoding="utf-8")
    (volume / "_VOLUME.yml").write_text(
        conteudo.replace("status: PRONTO", "status: RASCUNHO"), encoding="utf-8"
    )

    assert sincronizar.divergencias(tmp_path) != []
    sincronizar.sincronizar(tmp_path)
    assert not (destino / "31-TESTING").exists()
    assert sincronizar.divergencias(tmp_path) == []


def test_volume_promovido_a_pronto_passa_a_viajar(tmp_path):
    """O outro caso real: `03-DISCOVERY` era PRONTO na fonte e nunca chegou."""
    acervo = _acervo(tmp_path)
    volume = _volume(acervo, "03-DISCOVERY", "RASCUNHO")
    sincronizar.sincronizar(tmp_path)
    destino = tmp_path.joinpath(*sincronizar.PASTA_DESTINO)
    assert not (destino / "03-DISCOVERY").exists()

    conteudo = (volume / "_VOLUME.yml").read_text(encoding="utf-8")
    (volume / "_VOLUME.yml").write_text(
        conteudo.replace("status: RASCUNHO", "status: PRONTO"), encoding="utf-8"
    )

    assert sincronizar.divergencias(tmp_path) != []
    sincronizar.sincronizar(tmp_path)
    assert (destino / "03-DISCOVERY" / "01-Introducao.md").exists()


def test_o_contrato_do_acervo_nao_e_volume(tmp_path):
    """`00-INTRODUCAO` casa com o padrão de nome mas não tem `_VOLUME.yml` —
    é o contrato do acervo, não conhecimento consultável."""
    acervo = _acervo(tmp_path)
    (acervo / "00-INTRODUCAO").mkdir()
    (acervo / "00-INTRODUCAO" / "contrato.json").write_text("{}", encoding="utf-8")
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")

    prontos = sincronizar.volumes_consultaveis(acervo)

    assert list(prontos) == ["07-PROMPT-ENGINE"]


# --------------------------------------------------------------------------
# A deriva de conteúdo — provada por mutação
# --------------------------------------------------------------------------


def test_um_byte_diferente_na_copia_e_detectado(tmp_path):
    """Prova que a comparação é por conteúdo, e não só por presença de arquivo.

    Sem esta asserção, a porta passaria a mão em exatamente o que aconteceu: os
    mesmos arquivos dos dois lados, com texto que já tinha divergido.
    """
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO", corpo="texto original\n")
    sincronizar.sincronizar(tmp_path)
    assert sincronizar.divergencias(tmp_path) == []

    copia = tmp_path.joinpath(*sincronizar.PASTA_DESTINO, "07-PROMPT-ENGINE")
    (copia / "01-Introducao.md").write_text("texto editado a mao\n", encoding="utf-8")

    achados = sincronizar.divergencias(tmp_path)
    assert any("conteúdo diferente" in achado for achado in achados), achados


def test_arquivo_apagado_na_fonte_some_da_copia(tmp_path):
    """Cópia incremental deixaria o órfão para trás; a reescrita completa não."""
    acervo = _acervo(tmp_path)
    volume = _volume(acervo, "12-MEMORY", "PRONTO")
    (volume / "99-Extra.md").write_text("some depois\n", encoding="utf-8")
    sincronizar.sincronizar(tmp_path)
    copia = tmp_path.joinpath(*sincronizar.PASTA_DESTINO, "12-MEMORY")
    assert (copia / "99-Extra.md").exists()

    (volume / "99-Extra.md").unlink()

    assert sincronizar.divergencias(tmp_path) != []
    sincronizar.sincronizar(tmp_path)
    assert not (copia / "99-Extra.md").exists()
    assert sincronizar.divergencias(tmp_path) == []


def test_lixo_de_execucao_nao_entra_no_artefato(tmp_path):
    acervo = _acervo(tmp_path)
    volume = _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")
    (volume / "__pycache__").mkdir()
    (volume / "__pycache__" / "x.cpython-314.pyc").write_bytes(b"\x00")

    sincronizar.sincronizar(tmp_path)

    copia = tmp_path.joinpath(*sincronizar.PASTA_DESTINO, "07-PROMPT-ENGINE")
    assert not (copia / "__pycache__").exists()
    assert sincronizar.divergencias(tmp_path) == []


# --------------------------------------------------------------------------
# Catálogo
# --------------------------------------------------------------------------


def test_catalogo_lista_so_o_que_viaja(tmp_path):
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")
    _volume(acervo, "31-TESTING", "RASCUNHO")

    sincronizar.sincronizar(tmp_path)

    texto = (tmp_path / "volumes" / "_catalogo.md").read_text(encoding="utf-8")
    assert "07-PROMPT-ENGINE" in texto
    assert "31-TESTING" not in texto
    assert "GERADO" in texto


def test_catalogo_editado_a_mao_e_divergencia(tmp_path):
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")
    sincronizar.sincronizar(tmp_path)

    (tmp_path / "volumes" / "_catalogo.md").write_text("editado\n", encoding="utf-8")

    achados = sincronizar.divergencias(tmp_path)
    assert any("_catalogo.md" in achado for achado in achados), achados


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def test_verificar_devolve_1_quando_divergiu(tmp_path, capsys):
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")

    codigo = sincronizar.main(["--verificar", "--raiz", str(tmp_path)])

    assert codigo == 1
    assert "divergiu" in capsys.readouterr().err


def test_verificar_devolve_0_depois_de_sincronizar(tmp_path):
    acervo = _acervo(tmp_path)
    _volume(acervo, "07-PROMPT-ENGINE", "PRONTO")

    assert sincronizar.main(["--raiz", str(tmp_path)]) == 0
    assert sincronizar.main(["--verificar", "--raiz", str(tmp_path)]) == 0


def test_acervo_ausente_nao_estoura(tmp_path):
    """Instalado como plugin, o motor não leva o acervo junto — só o artefato.
    Nesse contexto a ferramenta não tem o que sincronizar, e não pode quebrar."""
    assert sincronizar.volumes_consultaveis(tmp_path / "acervo") == {}


# --------------------------------------------------------------------------
# A trava: so o sincronizador escreve no acervo
# --------------------------------------------------------------------------

#: Chamadas que gravam em disco. Se um modulo tem uma destas E fala de `acervo`,
#: ele e candidato a sobrescrever conteudo real da fonte.
_ESCRITAS = (
    "write_text",
    "write_bytes",
    "mkdir",
    "rmtree",
    "unlink",
    "copytree",
)

#: Unico modulo do motor autorizado a gravar dentro de `acervo/` -- e mesmo ele
#: so LE de la: escreve em `volumes/prontos/`. Qualquer outro que ganhe essa
#: combinacao esta reintroduzindo a classe de defeito descrita abaixo.
_AUTORIZADO = {"sincronizar.py"}


def test_nenhum_modulo_do_motor_escreve_no_acervo():
    """O acervo e a FONTE. Ferramenta do motor nao grava nela.

    Esta trava existe porque dois geradores de andaime moraram aqui ate
    2026-08-04: `gerar_volumes_conteudo.py` fazia `write_text` incondicional em
    `acervo/{02..42}/*.md` -- rodar por engano substituia 702 arquivos de 39
    volumes PRONTO por stubs de dez linhas, e a sincronizacao seguinte levava os
    stubs para dentro do plugin sem que nenhum teste ficasse vermelho, porque a
    copia continuaria fiel a fonte destruida. O companheiro
    (`gerar_volumes_controladoria.py`) ainda apontava para o acervo errado.

    Nenhum dos dois era citado por doc, CHANGELOG ou teste: eram codigo morto
    armado. Foram removidos por `git rm` e continuam recuperaveis pelo historico.
    """
    modulos = sorted(
        p
        for p in (Path(__file__).resolve().parent.parent).glob("*.py")
        if p.name not in _AUTORIZADO
    )
    assert modulos, "esperava encontrar modulos do motor para inspecionar"

    culpados = []
    for modulo in modulos:
        fonte = modulo.read_text(encoding="utf-8", errors="ignore")
        if '"acervo"' not in fonte and "'acervo'" not in fonte:
            continue
        if any(escrita in fonte for escrita in _ESCRITAS):
            culpados.append(modulo.name)

    assert not culpados, (
        "modulo do motor que escreve no acervo (o acervo e a fonte, nao destino): "
        + ", ".join(culpados)
    )
