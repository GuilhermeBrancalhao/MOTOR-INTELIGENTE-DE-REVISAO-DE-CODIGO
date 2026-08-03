"""DAG de nos: ordem topologica, deteccao de ciclo e politica de falha por no.

Duas garantias sustentam o modulo:

1. **O grafo e validado por completo antes de qualquer no executar.** Ciclo e
   referencia a no inexistente sao erros de definicao, nao de execucao -- descobrir
   um ciclo no meio da execucao custa o tempo ate o impasse, depois que recursos ja
   foram consumidos.
2. **Fan-in exige TODAS as dependencias em sucesso.** Trocar esse `all` por `any`
   e a mutacao que `test_fan_in_com_uma_dependencia_falha_nunca_libera` derruba --
   sem esse teste, a troca passaria despercebida em qualquer grafo cujas
   dependencias sempre tivessem sucesso.

O algoritmo de deteccao de ciclo e a travessia em profundidade com marcacao de
tres estados -- a mesma tecnica que `ferramentas/validar.py` usa sobre `depende_de`
neste proprio acervo. Nao e coincidencia: qualquer grafo de dependencia aciclica
se beneficia dela.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Estado(str, Enum):
    PENDENTE = "PENDENTE"
    PRONTO = "PRONTO"
    EXECUTANDO = "EXECUTANDO"
    SUCESSO = "SUCESSO"
    FALHA_DEFINITIVA = "FALHA_DEFINITIVA"
    ABORTADO = "ABORTADO"


class Politica(str, Enum):
    ABORTAR_DEPENDENTES = "ABORTAR_DEPENDENTES"
    PULAR_DEPENDENTES = "PULAR_DEPENDENTES"


class GrafoInvalido(ValueError):
    """Erro de definicao. Levantado na submissao, nunca durante a execucao."""


@dataclass(frozen=True)
class No:
    id: str
    dependencias: tuple[str, ...] = ()
    politica: Politica = Politica.PULAR_DEPENDENTES


@dataclass
class Grafo:
    nos: dict[str, No]
    estados: dict[str, Estado] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validar()
        if not self.estados:
            self.estados = {i: Estado.PENDENTE for i in self.nos}

    def validar(self) -> None:
        for no in self.nos.values():
            for dep in no.dependencias:
                if dep not in self.nos:
                    raise GrafoInvalido(f"no '{no.id}' depende de '{dep}', que nao existe")
        self.ordem_topologica()  # levanta se houver ciclo

    def ordem_topologica(self) -> tuple[str, ...]:
        """Travessia com tres marcas: nao visitado, visitando, concluido.
        Reencontrar um no 'visitando' e ciclo -- inclusive ciclo indireto por
        tres ou mais nos, que e mais facil de introduzir por acidente."""
        VISITANDO, CONCLUIDO = 1, 2
        marca: dict[str, int] = {}
        saida: list[str] = []

        def visitar(id_: str, caminho: tuple[str, ...]) -> None:
            m = marca.get(id_)
            if m == CONCLUIDO:
                return
            if m == VISITANDO:
                ciclo = " -> ".join(caminho + (id_,))
                raise GrafoInvalido(f"ciclo em depende_de: {ciclo}")
            marca[id_] = VISITANDO
            for dep in self.nos[id_].dependencias:
                visitar(dep, caminho + (id_,))
            marca[id_] = CONCLUIDO
            saida.append(id_)

        for id_ in sorted(self.nos):
            visitar(id_, ())
        return tuple(saida)

    def prontos(self) -> tuple[str, ...]:
        """Nos cujas dependencias TODAS chegaram a SUCESSO. O `all` aqui e a
        garantia de fan-in; trocar por `any` libera agregacao com dado parcial."""
        saida = []
        for id_, no in sorted(self.nos.items()):
            if self.estados[id_] is not Estado.PENDENTE:
                continue
            if all(self.estados[d] is Estado.SUCESSO for d in no.dependencias):
                saida.append(id_)
        return tuple(saida)

    def marcar(self, id_: str, estado: Estado) -> None:
        self.estados[id_] = estado
        if estado is Estado.FALHA_DEFINITIVA:
            self._propagar_falha(id_)

    def _propagar_falha(self, falho: str) -> None:
        """Dependente de no falho vira ABORTADO -- herda falha por dependencia nao
        resolvida, nao por falha propria. Ramos independentes seguem."""
        mudou = True
        while mudou:
            mudou = False
            for id_, no in self.nos.items():
                if self.estados[id_] is not Estado.PENDENTE:
                    continue
                if any(
                    self.estados[d] in (Estado.FALHA_DEFINITIVA, Estado.ABORTADO)
                    for d in no.dependencias
                ):
                    self.estados[id_] = Estado.ABORTADO
                    mudou = True

    def resultado(self) -> dict[str, Estado]:
        """Status por no, sem campo agregado de sucesso/falha: falha parcial e
        resultado de primeira classe, e quem chama decide se e aceitavel."""
        return dict(self.estados)
