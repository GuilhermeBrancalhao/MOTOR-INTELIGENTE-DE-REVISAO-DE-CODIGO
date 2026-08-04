"""Contrato de API: versionamento, tradução obrigatória, erro consistente, status consultável.

As regras T1-T6 formalizadas: `ContratoDeEndpoint.declarar_campo` rejeita mudança
de tipo sob a mesma versão (T1/T5); `traduzir_para_resposta` só inclui campos
permitidos (T2); `ErroDeAPI` é o único formato de erro (T3); `status_do_trabalho`
produz recurso consultável para qualquer estado (T4); `declarar_endpoint_sincrono`
exige orçamento de latência (T6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class MudancaQuebraContrato(Exception):
    """T1/T5: campo já exposto muda de tipo sob a mesma versão de contrato."""


class OrcamentoDeLatenciaAusente(Exception):
    """T6: endpoint síncrono declarado sem orçamento de latência."""


@dataclass(frozen=True)
class VersaoDeContrato:
    major: int
    minor: int


@dataclass
class ContratoDeEndpoint:
    nome: str
    versao_atual: VersaoDeContrato
    campos_expostos: dict = field(default_factory=dict)

    def declarar_campo(self, nome: str, tipo: str) -> None:
        tipo_existente = self.campos_expostos.get(nome)
        if tipo_existente is not None and tipo_existente != tipo:
            raise MudancaQuebraContrato(
                f"campo '{nome}' mudou de tipo ({tipo_existente} -> {tipo}) "
                f"na mesma versao {self.versao_atual} (T1/T5)"
            )
        self.campos_expostos[nome] = tipo


def traduzir_para_resposta(registro_interno: dict, campos_permitidos: set) -> dict:
    """T2: só campos explicitamente permitidos atravessam para o cliente."""
    return {k: v for k, v in registro_interno.items() if k in campos_permitidos}


@dataclass(frozen=True)
class ErroDeAPI:
    codigo: str
    mensagem: str
    detalhes: dict = field(default_factory=dict)


def formatar_erro(codigo: str, mensagem: str, detalhes: dict | None = None) -> ErroDeAPI:
    """T3: único formato de erro usado por qualquer endpoint."""
    return ErroDeAPI(codigo, mensagem, detalhes or {})


@dataclass(frozen=True)
class RecursoDeStatusDeTrabalho:
    id: str
    estado: str
    url_consulta: str


def status_do_trabalho(trabalho_id: str, estado: str) -> RecursoDeStatusDeTrabalho:
    """T4: recurso consultável, com a mesma estrutura para qualquer estado."""
    return RecursoDeStatusDeTrabalho(
        id=trabalho_id, estado=estado, url_consulta=f"/trabalhos/{trabalho_id}"
    )


@dataclass(frozen=True)
class OrcamentoDeLatencia:
    endpoint: str
    limite_ms: int


def declarar_endpoint_sincrono(nome: str, limite_ms: int | None) -> OrcamentoDeLatencia:
    if limite_ms is None:
        raise OrcamentoDeLatenciaAusente(
            f"endpoint '{nome}' sem orcamento de latencia declarado (T6)"
        )
    return OrcamentoDeLatencia(nome, limite_ms)
