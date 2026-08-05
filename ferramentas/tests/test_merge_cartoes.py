from __future__ import annotations

import json

from ferramentas import conhecimento, merge_cartoes


def _seed_backlog(raiz, itens):
    caminho = conhecimento.caminho_backlog(raiz)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "gerado_em": "2026-08-05T10:00:00",
        "ciclo": "2026-08-05-1",
        "resumo": {"critico": 1, "alto": 0, "medio": 0, "baixo": 0},
        "itens": itens,
    }
    caminho.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _seed_cartao(diretorio, tecnologia="python"):
    caminho = diretorio / f"{tecnologia}.md"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        """---
tecnologia: python
detectar: [\"pyproject.toml\"]
papeis: [arquiteto]
versao: 2026-08-05
---

## Convencoes
- manter nomenclatura consistente.

## Armadilhas
- evitar estado global mutavel.

## Checklist de review
- [ ] testar caminho feliz.
""",
        encoding="utf-8",
    )
    return caminho


def test_gerar_propostas_cria_pendencias_de_aprovacao(tmp_path):
    cartoes = tmp_path / "cartoes"
    _seed_cartao(cartoes)
    _seed_backlog(
        tmp_path,
        [
            {
                "id": "x1",
                "tecnologia": "python",
                "categoria": "pendencia",
                "categoria_semantica": "seguranca",
                "confianca": 0.88,
                "evidencia": "token exposto no log",
                "sugestao": "Adicionar regra para redigir token em logs.",
                "severidade": "critico",
            }
        ],
    )

    resumo = merge_cartoes.gerar_propostas(tmp_path, diretorio_cartoes=cartoes)

    assert resumo["novas"] == 1
    assert resumo["pendentes"] == 1
    assert merge_cartoes.caminho_aprovacoes(tmp_path).is_file()


def test_aprovar_aplica_merge_no_cartao(tmp_path):
    cartoes = tmp_path / "cartoes"
    cartao = _seed_cartao(cartoes)
    _seed_backlog(
        tmp_path,
        [
            {
                "id": "x1",
                "tecnologia": "python",
                "categoria": "pendencia",
                "categoria_semantica": "concorrencia",
                "confianca": 0.9,
                "evidencia": "race condition no lock",
                "sugestao": "Adicionar teste de corrida para lock de estado.",
                "severidade": "critico",
            }
        ],
    )

    resumo = merge_cartoes.gerar_propostas(tmp_path, diretorio_cartoes=cartoes)
    pid = resumo["propostas"][0]["id"]

    ok, _msg = merge_cartoes.aprovar(tmp_path, pid, diretorio_cartoes=cartoes)

    assert ok
    conteudo = cartao.read_text(encoding="utf-8")
    assert "Adicionar teste de corrida para lock de estado." in conteudo


def test_editar_e_rejeitar_proposta_pendente(tmp_path):
    cartoes = tmp_path / "cartoes"
    _seed_cartao(cartoes)
    _seed_backlog(
        tmp_path,
        [
            {
                "id": "x1",
                "tecnologia": "python",
                "categoria": "diff_pendente",
                "categoria_semantica": "testes",
                "confianca": 0.61,
                "evidencia": "diff sem teste de regressao",
                "sugestao": "Adicionar item de review para regressao.",
                "severidade": "medio",
            }
        ],
    )

    resumo = merge_cartoes.gerar_propostas(tmp_path, diretorio_cartoes=cartoes)
    pid = resumo["propostas"][0]["id"]

    ok_editar, _ = merge_cartoes.editar(tmp_path, pid, "Texto ajustado pelo revisor humano.")
    ok_rejeitar, _ = merge_cartoes.rejeitar(tmp_path, pid, "fora de escopo")

    assert ok_editar
    assert ok_rejeitar
    pendentes = merge_cartoes.listar_pendentes(tmp_path)
    assert pendentes == []


def test_detalhar_proposta_retorna_preview_da_secao(tmp_path):
    cartoes = tmp_path / "cartoes"
    _seed_cartao(cartoes)
    _seed_backlog(
        tmp_path,
        [
            {
                "id": "x1",
                "tecnologia": "python",
                "categoria": "pendencia",
                "categoria_semantica": "seguranca",
                "confianca": 0.77,
                "evidencia": "token em log",
                "sugestao": "Adicionar redacao de token em logs.",
                "severidade": "critico",
            }
        ],
    )
    resumo = merge_cartoes.gerar_propostas(tmp_path, diretorio_cartoes=cartoes)
    pid = resumo["propostas"][0]["id"]

    ok, detalhe = merge_cartoes.detalhar(tmp_path, pid, diretorio_cartoes=cartoes)

    assert ok
    assert isinstance(detalhe, dict)
    assert detalhe["id"] == pid
    assert "##" in detalhe["trecho"]
