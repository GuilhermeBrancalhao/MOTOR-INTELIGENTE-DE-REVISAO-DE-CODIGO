"""Persistência: migração compatível, proveniência, concorrência otimista, retenção.

As regras A1-A6 formalizadas: `aplicar_migracao` rejeita incompatibilidade (A1);
`RegistroDeConteudo` exige `Procedencia` (A2); `Repositorio.salvar` detecta
conflito de concorrência (A3); `declarar_tabela` exige retenção (A4);
`ler_tolerante` preserva campo desconhecido (A5); `Repositorio.remover` verifica
referência ativa antes de excluir (A6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class MigracaoIncompativel(Exception):
    """A1: migração marcada como incompatível com a versão anterior."""


class ProcedenciaAusente(Exception):
    """A2: conteúdo gerado por IA sem modelo/versão de origem."""


class ConflitoDeConcorrencia(Exception):
    """A3: escrita concorrente com versão esperada divergente da real."""


class PoliticaDeRetencaoAusente(Exception):
    """A4: tabela declarada sem política de retenção."""


class ReferenciaAtiva(Exception):
    """A6: exclusão de registro ainda referenciado por outro."""


@dataclass(frozen=True)
class Migracao:
    nome: str
    compativel_com_versao_anterior: bool


def aplicar_migracao(historico: list, migracao: Migracao) -> None:
    if not migracao.compativel_com_versao_anterior:
        raise MigracaoIncompativel(f"migracao '{migracao.nome}' quebra compatibilidade (A1)")
    historico.append(migracao)


@dataclass(frozen=True)
class Procedencia:
    modelo: str
    versao: str


@dataclass
class RegistroDeConteudo:
    id: str
    conteudo: str
    procedencia: Procedencia
    versao_do_registro: int = 1
    campos_desconhecidos: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.procedencia is None:
            raise ProcedenciaAusente(f"registro {self.id} sem procedencia declarada (A2)")


_CAMPOS_CONHECIDOS = {"id", "conteudo", "procedencia", "versao_do_registro"}


@dataclass
class Repositorio:
    registros: dict = field(default_factory=dict)
    politicas_de_retencao: dict = field(default_factory=dict)
    referencias: dict = field(default_factory=dict)  # id -> set de ids que o referenciam

    def declarar_tabela(self, nome: str, dias_retencao: int | None = None) -> None:
        if dias_retencao is None:
            raise PoliticaDeRetencaoAusente(f"tabela '{nome}' sem politica de retencao (A4)")
        self.politicas_de_retencao[nome] = dias_retencao

    def salvar(self, registro: RegistroDeConteudo, versao_esperada: int) -> None:
        existente = self.registros.get(registro.id)
        versao_real = existente.versao_do_registro if existente is not None else 0
        if versao_real != versao_esperada:
            raise ConflitoDeConcorrencia(
                f"versao esperada {versao_esperada}, real {versao_real} (A3)"
            )
        registro.versao_do_registro = versao_esperada + 1
        self.registros[registro.id] = registro

    def ler_tolerante(self, bruto: dict) -> RegistroDeConteudo:
        desconhecidos = {k: v for k, v in bruto.items() if k not in _CAMPOS_CONHECIDOS}
        return RegistroDeConteudo(
            id=bruto["id"],
            conteudo=bruto["conteudo"],
            procedencia=Procedencia(**bruto["procedencia"]),
            versao_do_registro=bruto.get("versao_do_registro", 1),
            campos_desconhecidos=desconhecidos,
        )

    def remover(self, registro_id: str) -> None:
        refs = self.referencias.get(registro_id, set())
        if refs:
            raise ReferenciaAtiva(f"registro {registro_id} ainda referenciado por {refs} (A6)")
        del self.registros[registro_id]
