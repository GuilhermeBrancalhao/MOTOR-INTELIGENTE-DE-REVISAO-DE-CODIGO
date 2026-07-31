from pathlib import Path

from ferramentas import validar


def _escrever_volume(raiz: Path, nome_dir: str, **campos) -> Path:
    diretorio = raiz / nome_dir
    diretorio.mkdir(parents=True, exist_ok=True)
    linhas = []
    for chave, valor in campos.items():
        if chave == "depende_de":
            itens = ", ".join('"{}"'.format(v) for v in valor)
            linhas.append(f"{chave}: [{itens}]")
        else:
            linhas.append(f"{chave}: {valor}")
    (diretorio / "_VOLUME.yml").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return diretorio


def test_sem_volumes_nao_ha_violacao(tmp_path):
    assert validar.validar(tmp_path / "prontos") == []


def test_volume_valido_sem_dependencia_nao_ha_violacao(tmp_path):
    _escrever_volume(
        tmp_path, "07-PROMPT-ENGINE",
        volume='"07"', nome="PROMPT-ENGINE", tipo="ENGINE",
        status="PRONTO", perecivel="false", depende_de=[],
    )
    assert validar.validar(tmp_path) == []


def test_campo_obrigatorio_ausente_e_violacao(tmp_path):
    diretorio = tmp_path / "07-PROMPT-ENGINE"
    diretorio.mkdir()
    (diretorio / "_VOLUME.yml").write_text('volume: "07"\nnome: PROMPT-ENGINE\n', encoding="utf-8")
    violacoes = validar.validar(tmp_path)
    assert any("campo obrigatório 'status'" in v for v in violacoes)
    assert any("campo obrigatório 'tipo'" in v for v in violacoes)


def test_depende_de_inexistente_e_violacao(tmp_path):
    _escrever_volume(
        tmp_path, "12-MEMORY",
        volume='"12"', nome="MEMORY", tipo="ENGINE",
        status="PRONTO", perecivel="false", depende_de=["11"],
    )
    violacoes = validar.validar(tmp_path)
    assert len(violacoes) == 1
    assert "depende-de-inexistente" in violacoes[0]
    assert "'11'" in violacoes[0]


def test_depende_de_existente_nao_e_violacao(tmp_path):
    _escrever_volume(
        tmp_path, "07-PROMPT-ENGINE",
        volume='"07"', nome="PROMPT-ENGINE", tipo="ENGINE",
        status="PRONTO", perecivel="false", depende_de=[],
    )
    _escrever_volume(
        tmp_path, "12-MEMORY",
        volume='"12"', nome="MEMORY", tipo="ENGINE",
        status="PRONTO", perecivel="false", depende_de=["07"],
    )
    assert validar.validar(tmp_path) == []


def test_diretorio_sem_volume_yml_e_ignorado_nao_e_violacao(tmp_path):
    (tmp_path / "99-VAZIO").mkdir()
    assert validar.validar(tmp_path) == []


def test_descobrir_volumes_indexa_pelo_numero_nao_pelo_nome_do_diretorio(tmp_path):
    _escrever_volume(
        tmp_path, "qualquer-nome-de-pasta",
        volume='"31"', nome="TESTING", tipo="PROCESSO",
        status="PRONTO", perecivel="false", depende_de=[],
    )
    volumes = validar.descobrir_volumes(tmp_path)
    assert "31" in volumes
    assert volumes["31"]["_diretorio"] == "qualquer-nome-de-pasta"


def test_principal_sai_0_sem_violacao_e_1_com_violacao(tmp_path, capsys):
    assert validar.principal([str(tmp_path)]) == 0
    _escrever_volume(
        tmp_path, "12-MEMORY",
        volume='"12"', nome="MEMORY", tipo="ENGINE",
        status="PRONTO", perecivel="false", depende_de=["99"],
    )
    assert validar.principal([str(tmp_path)]) == 1
    saida = capsys.readouterr().out
    assert "depende-de-inexistente" in saida


def test_volume_yml_com_encoding_invalido_e_violacao_nao_derruba_o_processo(tmp_path):
    diretorio = tmp_path / "07-PROMPT-ENGINE"
    diretorio.mkdir()
    (diretorio / "_VOLUME.yml").write_bytes(b"volume: \xff\xfe invalido")
    violacoes = validar.validar(tmp_path)
    assert len(violacoes) == 1
    assert "ilegível" in violacoes[0]


def test_volumes_reais_do_repositorio_nao_tem_violacao():
    """Regressão: os 3 volumes reais (07, 12, 31) devem sempre validar limpo."""
    raiz_volumes = Path(__file__).resolve().parent.parent.parent / "volumes" / "prontos"
    assert validar.validar(raiz_volumes) == []
